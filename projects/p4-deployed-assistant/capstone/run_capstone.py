#!/usr/bin/env python3
"""The Project 4 capstone run: one command, one report, honest about what it did not measure.

    python3 capstone/run_capstone.py              # from projects/p4-deployed-assistant
    python3 capstone/run_capstone.py --with-model # also use the configured model endpoints

Four parts, each tied to a lesson:

  1. Tests          the suite, including the fallback ladder and its breaker
  2. Failure drill  stub providers that fail on command; which rung answered, how
                    long the caller waited, and whether the breaker stopped the
                    calls  (lessons/block8-deployment: When the Provider Goes Down)
  3. Gold set       29 questions with a known document and a known fact, scored
                    through the real /v1/ask handler  (Block 5 and Block 3)
  4. Scale sum      the memory arithmetic for a vector index at larger corpora
                    (lessons/block3-retrieval: Retrieval at Scale)

By default no model is used: with no generation endpoint the service answers from
retrieval alone, so the gold-set score is a retrieval score and is labelled one.
Refusal on unanswerable questions needs a model and is reported "not measured"
without one. The stub providers in the drill exercise the service's own logic and
say nothing about any real provider.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ.setdefault("API_KEYS", "capstone-key")
os.environ.setdefault("CORPUS_DIR", str(ROOT / "corpus"))
os.environ["RATE_LIMIT"] = "100000"
os.environ["RATE_WINDOW_S"] = "3600"

try:
    from fastapi.testclient import TestClient
    from src import app as appmod
    from tests.stubs import StubProvider
except ImportError as exc:  # pragma: no cover
    sys.exit(f"missing dependency ({exc}); install requirements.txt plus pytest and httpx")

HEADERS = {"X-API-Key": os.environ["API_KEYS"].split(",")[0]}
Q = {"question": "What gearbox oil temperature triggers a controlled shutdown?"}


def norm(text: str) -> str:
    return " ".join(text.lower().split())


# 1. tests ---------------------------------------------------------------------

def run_tests() -> dict:
    # The suite sets its own keys and a deliberately low rate limit. Inheriting
    # this script's values makes it fail for reasons that have nothing to do with the code.
    clean_env = {k: v for k, v in os.environ.items()
                 if k not in ("API_KEYS", "RATE_LIMIT", "RATE_WINDOW_S")}
    proc = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                           "tests"], cwd=ROOT, capture_output=True, text=True,
                          env=clean_env)
    last = [ln for ln in proc.stdout.strip().splitlines() if ln.strip()][-1]
    return {"passed": proc.returncode == 0, "summary": last}


# 2. failure drill -------------------------------------------------------------

def _ask(client):
    started = time.perf_counter()
    body = client.post("/v1/ask", json=Q, headers=HEADERS).json()
    return body, round((time.perf_counter() - started) * 1000)


def run_drill() -> list[dict]:
    # The drill points the app at stub providers and shrinks its timings. Put the
    # real settings back afterwards, or the gold run that follows inherits stubs
    # that have already been closed.
    saved = {k: getattr(appmod, k) for k in
             ("ENDPOINTS", "GENERATION_DEADLINE_S", "BREAKER_THRESHOLD", "BREAKER_COOLDOWN_S")}
    try:
        return _run_drill()
    finally:
        for k, v in saved.items():
            setattr(appmod, k, v)


def _run_drill() -> list[dict]:
    deadline, cooldown = 1.0, 0.6
    primary, secondary = StubProvider("primary"), StubProvider("secondary")
    appmod.ENDPOINTS = [primary.base, secondary.base]
    appmod.GENERATION_DEADLINE_S = deadline
    appmod.BREAKER_THRESHOLD = 2
    appmod.BREAKER_COOLDOWN_S = cooldown
    results = []

    def fresh(client):
        primary.mode, primary.delay_s, secondary.mode = "ok", 5.0, "ok"
        appmod.STATE["ladder"] = appmod.build_ladder()

    def record(name, expect, got, detail):
        results.append({"scenario": name, "expected": expect, "observed": got,
                        "pass": got == expect, **detail})

    with TestClient(appmod.app) as client:
        fresh(client)
        body, ms = _ask(client)
        record("healthy primary", "rung-1", body["rung"], {"ms": ms})

        fresh(client)
        primary.mode = "error"
        for _ in range(2):
            _ask(client)  # trips the breaker
        calls_before = primary.calls
        rungs = [_ask(client)[0]["rung"] for _ in range(3)]
        record("primary erroring, breaker open", "rung-2", rungs[-1] if len(set(rungs)) == 1 else "mixed",
               {"primary_calls_after_open": primary.calls - calls_before})
        results[-1]["pass"] = results[-1]["pass"] and results[-1]["primary_calls_after_open"] == 0

        fresh(client)
        primary.mode, primary.delay_s = "slow", 3.0
        body, ms = _ask(client)
        record("primary slow, 1s deadline", "rung-2", body["rung"], {"ms": ms})
        results[-1]["pass"] = results[-1]["pass"] and ms < 2500

        fresh(client)
        primary.mode = secondary.mode = "error"
        default = client.post("/v1/ask", json=Q, headers=HEADERS)
        record("every provider down, default caller", 503, default.status_code,
               {"retry_after": default.headers.get("Retry-After")})
        started = time.perf_counter()
        r = client.post("/v1/ask", json={**Q, "allow_degraded": True}, headers=HEADERS)
        body, ms = r.json(), round((time.perf_counter() - started) * 1000)
        evidence = "90 degrees" in norm(" ".join(p["text"] for p in body["passages"]))
        record("every provider down, opted in", "retrieval-only", body["rung"],
               {"ms": ms, "degraded": body["degraded"], "x_degraded": r.headers.get("X-Degraded"),
                "answer_is_only_a_notice": "90 degrees" not in norm(body["answer"]),
                "evidence_in_passages": evidence})
        results[-1]["pass"] = (results[-1]["pass"] and body["degraded"] and evidence
                               and results[-1]["answer_is_only_a_notice"]
                               and results[-1]["x_degraded"] == "retrieval-only")

        fresh(client)
        primary.mode = "error"
        for _ in range(2):
            _ask(client)
        primary.mode = "ok"
        time.sleep(cooldown + 0.2)
        body, ms = _ask(client)
        record("primary recovers after cooldown", "rung-1", body["rung"], {"ms": ms})

    primary.close(); secondary.close()
    return results


# 3. gold set ------------------------------------------------------------------

def run_gold(with_model: bool) -> dict:
    gold = [json.loads(ln) for ln in (ROOT / "capstone" / "gold.jsonl").read_text().splitlines() if ln]
    if not with_model:
        appmod.ENDPOINTS = []  # retrieval-only: no rung exists, so no model is called
    appmod.GENERATION_DEADLINE_S = 120.0
    rows = []
    with TestClient(appmod.app) as client:
        appmod.STATE["ladder"] = appmod.build_ladder()
        for g in gold:
            r = client.post("/v1/ask", json={"question": g["question"],
                                             "allow_degraded": not with_model}, headers=HEADERS)
            body = r.json()
            rows.append({**g, "status": r.status_code, "rung": body.get("rung"),
                         "sources": body.get("sources", []),
                         "grounded": body.get("grounded"),
                         "answer": body.get("answer", "") + " " + " ".join(
                             p["text"] for p in body.get("passages", []))})
    answerable = [r for r in rows if r["answerable"]]
    hit = sum(r["doc"] in r["sources"] for r in answerable)
    fact = sum(norm(r["fact"]) in norm(r["answer"]) for r in answerable)
    unanswerable = [r for r in rows if not r["answerable"]]
    modelled = [r for r in unanswerable if r["rung"] not in (None, appmod.RETRIEVAL_ONLY)]
    refused = sum(r["grounded"] is False for r in modelled)
    return {
        "mode": "with model" if with_model else "retrieval-only (no model)",
        "answerable": len(answerable),
        "document_in_top_k": hit,
        "fact_in_answer": fact,
        "unanswerable": len(unanswerable),
        "refusal_measured": bool(modelled),
        "correct_refusals": refused if modelled else None,
        "misses": [{"id": r["id"], "question": r["question"], "expected_doc": r["doc"],
                    "expected_fact": r["fact"], "got": r["sources"],
                    "kind": "document" if r["doc"] not in r["sources"] else "fact"}
                   for r in answerable
                   if r["doc"] not in r["sources"] or norm(r["fact"]) not in norm(r["answer"])],
    }


# 4. scale sum -----------------------------------------------------------------

def scale_sum(chunks_now: int) -> list[dict]:
    """Arithmetic only: rows x bytes per vector. The 64-byte product-quantized code
    is an assumed setting, not a measurement."""
    out = []
    for rows in (chunks_now, 100_000, 1_000_000, 10_000_000):
        out.append({"chunks": rows,
                    "float32_1024_gb": round(rows * 1024 * 4 / 1e9, 3),
                    "int8_1024_gb": round(rows * 1024 / 1e9, 3),
                    "pq64_assumed_gb": round(rows * 64 / 1e9, 3)})
    return out


# serving numbers --------------------------------------------------------------

def run_bench() -> list[dict] | None:
    proc = subprocess.run([sys.executable, "bench_serving.py"], cwd=ROOT,
                          capture_output=True, text=True)
    if proc.returncode != 0 or "concurrency sweep" not in proc.stdout:
        return None
    blob = proc.stdout.split("concurrency sweep against the real /v1/ask handler:")[1]
    return json.loads(blob[blob.index("["):blob.index("]") + 1])


# report -----------------------------------------------------------------------

def render(r: dict) -> str:
    g, t = r["gold"], r["tests"]
    lines = [
        "# Project 4 capstone report", "",
        f"Run: {r['timestamp']}. Mode: {g['mode']}. Corpus hash: `{r['corpus_hash']}`.", "",
        "## 1. Tests", "", f"{'PASS' if t['passed'] else 'FAIL'}: {t['summary']}", "",
        "## 2. Failure drill (stub providers, deadline 1s, breaker opens after 2 failures)", "",
        "| Scenario | Expected rung | Observed | Result | Detail |", "|---|---|---|---|---|"]
    for d in r["drill"]:
        detail = ", ".join(f"{k}={v}" for k, v in d.items()
                           if k not in ("scenario", "expected", "observed", "pass"))
        lines.append(f"| {d['scenario']} | {d['expected']} | {d['observed']} | "
                     f"{'PASS' if d['pass'] else 'FAIL'} | {detail} |")
    lines += ["", "Without `allow_degraded` an outage is a 503 with `Retry-After`. With it, the reply "
              "is a 200 whose `answer` is only a notice and whose evidence is in `passages`.", "",
              "The stubs exercise this service's own fallback logic. They say nothing "
              "about any real provider's latency or failure behaviour.", "",
              "## 3. Gold set", "",
              f"- Answerable questions: {g['answerable']}",
              f"- Expected document in the returned sources: {g['document_in_top_k']} of {g['answerable']}",
              f"- Expected fact present in the answer: {g['fact_in_answer']} of {g['answerable']}"]
    if g["refusal_measured"]:
        lines.append(f"- Correct refusals on {g['unanswerable']} unanswerable questions: "
                     f"{g['correct_refusals']}")
    else:
        lines.append(f"- Refusal on {g['unanswerable']} unanswerable questions: not measured "
                     "(needs a model; run with --with-model)")
    if g["mode"].startswith("retrieval-only"):
        lines.append("- With no model these are retrieval scores: the answer is the retrieved passages.")
    if g["misses"]:
        lines += ["", "Misses:", ""] + [
            f"- {m['id']} ({m['kind']} missing): {m['question']} Expected `{m['expected_fact']}` in "
            f"{m['expected_doc']}; sources returned: {', '.join(m['got'])}" for m in g["misses"]]
    lines += ["", "## 4. Scale sum (arithmetic, not a benchmark)", "",
              "| Chunks | float32, 1,024 dims (GB) | int8 (GB) | 64-byte code, assumed (GB) |", "|---|---|---|---|"]
    for s in r["scale"]:
        lines.append(f"| {s['chunks']:,} | {s['float32_1024_gb']} | {s['int8_1024_gb']} | {s['pq64_assumed_gb']} |")
    lines += ["", "This service stores no vectors: it retrieves by keyword. The table is what an "
              "embedding index over the same corpus would need.", "", "## Serving overhead", ""]
    if r["bench"]:
        lines += ["| Concurrency | Requests/s | p50 ms | p95 ms |", "|---|---|---|---|"]
        lines += [f"| {b['concurrency']} | {b['throughput_rps']} | {b['p50_ms']} | {b['p95_ms']} |"
                  for b in r["bench"]]
        lines += ["", "Measured against a 10 ms local stub in place of a model, on this machine. "
                  "Not a statement about model latency or the deployed instance."]
    else:
        lines.append("Not measured: bench_serving.py did not complete.")
    lines += ["", "## Not done here", "",
              "- The public deploy and the rate-limit check against it (a human action).",
              "- Answer correctness and groundedness with a real model.",
              "- Any real provider's outage behaviour."]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--with-model", action="store_true",
                    help="use the configured GENERATION_ENDPOINTS for the gold set")
    ap.add_argument("--skip-bench", action="store_true")
    args = ap.parse_args()

    result = {"timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    result["tests"] = run_tests()
    result["drill"] = run_drill()
    result["gold"] = run_gold(args.with_model)
    with TestClient(appmod.app) as client:
        result["corpus_hash"] = client.get("/version").json()["corpus_hash"]
        chunks = client.get("/health").json()["corpus_chunks"]
    result["scale"] = scale_sum(chunks)
    result["bench"] = None if args.skip_bench else run_bench()

    out = ROOT / "capstone"
    (out / "results.json").write_text(json.dumps(result, indent=2) + "\n")
    (out / "report.md").write_text(render(result))
    print(render(result))
    ok = result["tests"]["passed"] and all(d["pass"] for d in result["drill"])
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
