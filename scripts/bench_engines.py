#!/usr/bin/env python3
"""Measure what a local serving engine's cache, batching and thinking settings
actually do, through the one interface they all share: an OpenAI-compatible
streaming /v1/chat/completions endpoint.

The latency-and-caching lesson makes claims about engines - prefix caches reuse
work, a disk tier keeps long prefixes alive, continuous batching stops a short
request waiting behind a long one, thinking costs tokens and time. This script
turns each into a measurement you can run against your own engine and model.
It talks plain HTTP with the standard library, so it works unchanged against
vllm-mlx, mlx_lm.server, llama-server, Ollama, LM Studio, and vLLM or SGLang
on an NVIDIA box.

Start a server, then run one subcommand against it:

    python3 scripts/bench_engines.py --model MODEL prefix
    python3 scripts/bench_engines.py --model MODEL evict   --state /tmp/evict.json
    python3 scripts/bench_engines.py --model MODEL revisit --state /tmp/evict.json
    python3 scripts/bench_engines.py --model MODEL batching
    python3 scripts/bench_engines.py --model MODEL staggered
    python3 scripts/bench_engines.py --model MODEL thinking \\
        --arm on='{}' --arm off='{"chat_template_kwargs":{"enable_thinking":false}}'

The server flags that matter for each test are in the latency-and-caching lesson;
the point is to change ONE flag between runs and compare, never to read a
single number in isolation.

What this cannot tell you, stated so it is not mistaken for something it does:
  - Prefix length is set by word count and reported from the server's own
    usage.prompt_tokens when it sends one. A server that does not is marked "~".
  - Every figure is from one machine, one model and one load. A speedup here is
    evidence about that setup. It is not a property of the engine.
  - Nothing here is a quality measurement except the `thinking` subcommand's
    small answer-correct column, which is 6 questions and shows direction, not
    a rate.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import statistics
import sys
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request, urlopen

# ---------------------------------------------------------------- transport

def stream_chat(base, model, messages, max_tokens, extra=None, timeout=900, on_first=None):
    """One streaming request. Returns timings and token counts.

    ttft          seconds to the first token of any kind, thinking included
    ttft_visible  seconds to the first token of the final answer
    """
    body = {"model": model, "messages": messages, "max_tokens": max_tokens,
            "temperature": 0, "stream": True,
            "stream_options": {"include_usage": True}}
    body.update(extra or {})
    req = Request(f"{base}/chat/completions", json.dumps(body).encode(),
                  {"Content-Type": "application/json", "Authorization": "Bearer x"})
    t0 = time.perf_counter()
    ttft = ttft_visible = None
    content, reasoning, chunks = [], [], 0
    usage, finish, error = {}, None, None
    with urlopen(req, timeout=timeout) as r:
        for raw in r:
            line = raw.decode("utf-8", "ignore").strip()
            if not line.startswith("data:"):
                continue
            data = line[5:].strip()
            if data == "[DONE]":
                break
            try:
                ev = json.loads(data)
            except json.JSONDecodeError:
                continue
            if ev.get("error"):
                error = str(ev["error"])[:160]
            if ev.get("usage"):
                usage = ev["usage"]
            for ch in ev.get("choices") or []:
                finish = ch.get("finish_reason") or finish
                d = ch.get("delta") or {}
                c = d.get("content") or ""
                rs = d.get("reasoning_content") or d.get("reasoning") or ""
                if not (c or rs):
                    continue
                now = time.perf_counter() - t0
                chunks += 1
                if ttft is None:
                    ttft = now
                    if on_first:
                        on_first()
                if rs:
                    reasoning.append(rs)
                if c:
                    content.append(c)
                    if ttft_visible is None:
                        ttft_visible = now
    total = time.perf_counter() - t0
    text = "".join(content)
    think = "".join(reasoning)
    # Engines that do not split thinking out leave it inline in the content.
    m = re.search(r"<think>(.*?)</think>", text, re.S)
    if m:
        think += m.group(1)
        text = text.replace(m.group(0), "")
        # visible time is then after the closing tag; unknowable from chunks
        # alone, so approximate it by the share of characters that were thinking
        ttft_visible = None
    ctoks = usage.get("completion_tokens")
    exact = ctoks is not None
    return {
        "ttft": ttft, "ttft_visible": ttft_visible, "total": total,
        "prompt_tokens": usage.get("prompt_tokens"),
        "completion_tokens": ctoks if exact else chunks,
        "tokens_exact": exact, "text": text.strip(), "thinking_chars": len(think),
        "finish": finish, "empty": ttft is None, "error": error,
        "cut": finish == "length",
    }


def pad(n):
    return f"{n:,}" if isinstance(n, int) else "?"


def med(xs):
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else None


def fmt(x, unit="s"):
    return "   n/a" if x is None else f"{x:6.2f}{unit}"


# ---------------------------------------------------------------- workloads

WORDS = ("turbine gearbox bearing vibration threshold inspection torque blade pitch "
         "yaw generator coolant sensor firmware telemetry maintenance interval "
         "lubricant alignment housing rotor stator inverter converter breaker "
         "anemometer nacelle tower foundation cable grid frequency voltage "
         "harmonic fault alarm reset schedule technician report audit").split()


def document(nonce, words, seed):
    """A deterministic block of plausible text. The nonce comes FIRST, so a new
    nonce is a prefix no cache has seen, and editing only the nonce invalidates
    everything after it - the behaviour the lesson warns about."""
    rng = random.Random(seed)
    body = " ".join(rng.choice(WORDS) for _ in range(words))
    return f"Reference document {nonce}. {body}"


def ask(base, model, system_text, question, max_tokens=8, extra=None, on_first=None):
    msgs = [{"role": "system", "content": system_text},
            {"role": "user", "content": question}]
    return stream_chat(base, model, msgs, max_tokens, extra, on_first=on_first)


# ---------------------------------------------------------------- prefix

def cmd_prefix(a):
    """Cold versus warm time to first token, by prefix length and by KIND of reuse.

    Engines differ in what they will reuse, and the difference decides whether a
    cache helps your workload at all:
      same request   the identical request again
      new question   same long opening, different final question (RAG, agents
                     with a fixed system prompt and tools)
      next turn      the earlier conversation plus its answer plus a new turn
                     (chat)
      front edit     one word changed at the very start: must be cold again

    Each length is repeated over --trials fresh prefixes and reported as a median,
    because one cold run on a machine that is also doing other things can be off
    by a factor of two."""
    cols = ("cold", "same request", "new question", "next turn", "front edit")
    print(f"{'words':>6} {'prompt tok':>10} " + " ".join(f"{c:>13}" for c in cols))
    rows = []
    for words in a.lengths:
        res = {c: [] for c in cols}
        ptoks = None
        for t in range(a.trials):
            nonce = uuid.uuid4().hex[:8]
            doc = document(nonce, words, seed=words)
            q0 = "Reply with the word OK. (q0)"
            cold = ask(a.base_url, a.model, doc, q0)
            ptoks = cold["prompt_tokens"]
            res["cold"].append(cold["ttft"])
            for i in range(a.repeats):
                res["same request"].append(ask(a.base_url, a.model, doc, q0)["ttft"])
                res["new question"].append(
                    ask(a.base_url, a.model, doc, f"Reply with the word OK. (q{i + 1})")["ttft"])
                turn = [{"role": "system", "content": doc},
                        {"role": "user", "content": q0},
                        {"role": "assistant", "content": cold["text"] or "OK"},
                        {"role": "user", "content": f"Now reply with the word DONE. (n{i})"}]
                res["next turn"].append(stream_chat(a.base_url, a.model, turn, 8)["ttft"])
            res["front edit"].append(
                ask(a.base_url, a.model, doc.replace(nonce, uuid.uuid4().hex[:8], 1),
                    "Reply with the word OK. (edit)")["ttft"])
        m = {c: med(res[c]) for c in cols}
        print(f"{words:>6} {pad(ptoks):>10} " + " ".join(f"{fmt(m[c]):>13}" for c in cols))
        rows.append({"words": words, "prompt_tokens": ptoks, **{c: m[c] for c in cols},
                     "cold_trials": res["cold"]})
    print(f"\n{a.trials} trials per length, {a.repeats} repeats of each warm kind per trial; medians of TTFT.")
    print("A warm column close to `cold` means that kind of reuse is NOT cached on this engine.")
    dump(a, rows)


# ---------------------------------------------------------------- evict / revisit

def cmd_evict(a):
    """Fill the cache with more distinct long prefixes than it can hold in
    memory, then ask for the first one again. Warm means it survived somewhere
    (memory or a disk tier); cold means it was evicted."""
    state = {"words": a.words, "prefixes": []}
    print(f"sending {a.count} distinct prefixes of ~{a.words} words each")
    for i in range(a.count):
        nonce = uuid.uuid4().hex[:8]
        r = ask(a.base_url, a.model, document(nonce, a.words, seed=i), f"OK? (fill {i})")
        state["prefixes"].append({"nonce": nonce, "seed": i, "cold_ttft": r["ttft"],
                                  "prompt_tokens": r["prompt_tokens"]})
        print(f"  #{i:<3} cold ttft {fmt(r['ttft'])}  prompt tokens {pad(r['prompt_tokens'])}")
    if a.state:
        with open(a.state, "w") as f:
            json.dump(state, f)
    # control: the most recent prefix is certainly still in memory
    last = state["prefixes"][-1]
    ctrl = revisit_one(a, last, "control (most recent)")
    first = state["prefixes"][0]
    got = revisit_one(a, first, "revisit (oldest)")
    verdict(first["cold_ttft"], ctrl, got)


def revisit_one(a, p, label):
    r = ask(a.base_url, a.model, document(p["nonce"], a.words_from(p), p["seed"]),
            "OK? (revisit)")
    print(f"  {label:<26} ttft {fmt(r['ttft'])}  (was cold {fmt(p['cold_ttft'])})")
    return r["ttft"]


def verdict(cold, warm_ctrl, revisited):
    if None in (cold, warm_ctrl, revisited) or cold <= warm_ctrl:
        print("\ninconclusive: the control was not faster than cold, so this prefix is "
              "too short for the cache to matter on this engine. Raise --words.")
        return
    frac = (cold - revisited) / (cold - warm_ctrl)
    print(f"\nrevisit recovered {frac:.0%} of the cold-to-warm gap "
          f"(0% = evicted and recomputed, 100% = as good as the control)")


def cmd_revisit(a):
    """After restarting the server, ask for the first prefix again. A warm
    result means a disk tier persisted it across the restart."""
    state = json.load(open(a.state))
    a.words = state["words"]
    a.words_from = lambda p: state["words"]
    p = state["prefixes"][0]
    got = revisit_one(a, p, "after restart (oldest)")
    again = revisit_one(a, p, "same again, now in memory")
    verdict(p["cold_ttft"], again, got)


# ---------------------------------------------------------------- batching

def cmd_batching(a):
    """Throughput and per-stream speed as concurrency rises. Compare the same
    sweep with and without the engine's continuous-batching option.

    A request that comes back with no tokens is a failure, not a fast success:
    some engines reject a second concurrent request instead of queueing it. The
    `ok` column says how many of the streams actually returned text, and only
    those count toward the rates."""
    print(f"{'streams':>7} {'ok':>5} {'aggregate tok/s':>16} {'per-stream tok/s':>17} {'wall':>8}")
    rows = []
    for c in a.concurrency:
        def one(i):
            return ask(a.base_url, a.model, "You are a concise assistant.",
                       f"Write a long numbered list of maintenance checks. (run {i}-{uuid.uuid4().hex[:6]})",
                       max_tokens=a.tokens)
        t0 = time.perf_counter()
        with ThreadPoolExecutor(c) as ex:
            rs = list(ex.map(one, range(c)))
        wall = time.perf_counter() - t0
        good = [r for r in rs if not r["empty"]]
        toks = sum(r["completion_tokens"] for r in good)
        per = [r["completion_tokens"] / max(r["total"] - (r["ttft"] or 0), 1e-9) for r in good]
        mark = "" if all(r["tokens_exact"] for r in good) else "~"
        agg = f"{mark}{toks / wall:.1f}" if good else "n/a"
        pst = f"{mark}{statistics.mean(per):.1f}" if good else "n/a"
        print(f"{c:>7} {f'{len(good)}/{c}':>5} {agg:>16} {pst:>17} {wall:7.1f}s")
        rows.append({"streams": c, "ok": len(good), "aggregate": toks / wall if good else None,
                     "per_stream": statistics.mean(per) if good else None})
    print("\nok          streams that returned text; the rest were rejected or empty")
    print("aggregate   all generated tokens divided by wall time")
    print("per-stream  one request's own decode speed; falls as streams share the hardware")
    dump(a, rows)


def cmd_staggered(a):
    """A short request arrives while a long one is already generating. Under
    static or one-at-a-time serving it waits for the long one; under continuous
    batching it joins on the next step. The number to read is the short
    request's wall time against the same request on an idle server.

    The shorts are released only once the long request has produced its first
    token, and the result is flagged if the long request had already finished
    when a short one arrived - in which case nothing was measured."""
    started = threading.Event()
    marks = {}

    def long_req():
        marks["long_begin"] = time.perf_counter()
        return ask(a.base_url, a.model, "You are a concise assistant.",
                   f"Write a very long numbered list of maintenance checks. ({uuid.uuid4().hex[:6]})",
                   max_tokens=a.long_tokens, on_first=started.set)

    def short_req(i):
        started.wait()
        time.sleep(0.3 * i)
        b = time.perf_counter()
        return b, ask(a.base_url, a.model, "You are a concise assistant.",
                      f"Reply with the word OK. ({uuid.uuid4().hex[:6]})", max_tokens=8)

    alone = ask(a.base_url, a.model, "You are a concise assistant.",
                f"Reply with the word OK. ({uuid.uuid4().hex[:6]})", max_tokens=8)
    with ThreadPoolExecutor(a.shorts + 1) as ex:
        lf = ex.submit(long_req)
        sf = [ex.submit(short_req, i) for i in range(a.shorts)]
        shorts = [f.result() for f in sf]
        long_r = lf.result()
    long_end = marks["long_begin"] + long_r["total"]
    print(f"short request alone, idle server   : {fmt(alone['total'])}")
    overlapped = True
    for i, (begin, s_) in enumerate(shorts):
        late = begin >= long_end
        overlapped &= not late
        print(f"short #{i} while a long one runs     : {fmt(s_['total'])}"
              + ("   (long one had already finished: no overlap)" if late else "")
              + (f"   (EMPTY: {s_['error'] or 'no tokens came back'})" if s_["empty"] else ""))
    print(f"long request total                 : {fmt(long_r['total'])}  "
          f"({long_r['completion_tokens']} tokens)")
    if not overlapped:
        print("\nNOT MEASURED: the long request ended before a short one arrived. Raise --long-tokens.")
    dump(a, {"alone": alone["total"], "shorts": [x["total"] for _, x in shorts],
             "long": long_r["total"], "overlapped": overlapped})


# ---------------------------------------------------------------- thinking

QUESTIONS = [
    ("What is 17 * 24 + 9?", 417),
    ("A train leaves at 9:40 and arrives at 14:15 the same day. How many minutes is the journey?", 275),
    ("If 3 machines make 3 parts in 3 minutes, how many minutes do 100 machines need to make 100 parts?", 3),
    ("How many integers from 1 to 100 inclusive are divisible by 3 or by 5?", 47),
    ("A bat and a ball cost 110 cents together. The bat costs 100 cents more than the ball. How many cents does the ball cost?", 5),
    ("What is the sum of all integers from 1 to 50 that are NOT divisible by 7?", 1079),
]
SUFFIX = " Finish with a line of the form ANSWER: <number>."


def cmd_thinking(a):
    """The same questions with thinking in each requested arm. Each arm is a
    name and a JSON object merged into the request body, because how thinking
    is switched differs by engine (chat_template_kwargs, a budget, a flag)."""
    arms = [parse_arm(s) for s in a.arm]
    print(f"{'arm':<10} {'q':>2} {'tokens':>7} {'think chars':>11} {'first token':>11} "
          f"{'first answer':>12} {'total':>8} {'right':>6}")
    agg = {name: [] for name, _ in arms}
    for qi, (q, want) in enumerate(QUESTIONS):
        for name, extra in arms:
            for _ in range(a.reps):
                r = stream_chat(a.base_url, a.model,
                                [{"role": "user", "content": q + SUFFIX}],
                                a.max_tokens, extra)
                m = re.findall(r"ANSWER:\s*\**\s*(-?[\d,\.]+)", r["text"])
                ok = bool(m) and m[-1].replace(",", "").rstrip(".") == str(want)
                agg[name].append((r, ok))
                print(f"{name:<10} {qi + 1:>2} {r['completion_tokens']:>7} {r['thinking_chars']:>11} "
                      f"{fmt(r['ttft']):>11} {fmt(r['ttft_visible']):>12} {r['total']:7.1f}s "
                      f"{'yes' if ok else 'NO':>6}")
    print("\nper arm: median tokens, median total time, answers right")
    for name, rs in agg.items():
        print(f"  {name:<10} {med([r['completion_tokens'] for r, _ in rs]):>7.0f} tok  "
              f"{med([r['total'] for r, _ in rs]):6.1f}s  "
              f"{sum(ok for _, ok in rs)}/{len(rs)} right, "
              f"{sum(r['cut'] for r, _ in rs)} cut off by --max-tokens")
    print("\nfirst answer is n/a when the engine leaves thinking inline in the content.")
    print("6 questions show direction, not a rate. Do not quote the right column as accuracy.")
    dump(a, {n: [{"tokens": r["completion_tokens"], "total": r["total"], "ok": ok}
                 for r, ok in rs] for n, rs in agg.items()})


def parse_arm(s):
    name, _, js = s.partition("=")
    return name, json.loads(js or "{}")


def dump(a, obj):
    if a.json:
        with open(a.json, "w") as f:
            json.dump(obj, f, indent=2)
        print(f"\nwrote {a.json}")


# ---------------------------------------------------------------- main

def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--base-url", default="http://127.0.0.1:8000/v1")
    p.add_argument("--model", required=True)
    p.add_argument("--json", help="also write the raw numbers here")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("prefix", help="cold vs warm TTFT by prefix length")
    s.add_argument("--lengths", type=int, nargs="+", default=[500, 2000, 6000, 12000],
                   help="prefix lengths in words (about 1.2 tokens per word on a Qwen tokenizer)")
    s.add_argument("--repeats", type=int, default=3)
    s.add_argument("--trials", type=int, default=3)
    s.set_defaults(fn=cmd_prefix)

    s = sub.add_parser("evict", help="fill the cache past its limit, revisit the oldest")
    s.add_argument("--count", type=int, default=12)
    s.add_argument("--words", type=int, default=6000)
    s.add_argument("--state", help="save here so `revisit` can run after a restart")
    s.set_defaults(fn=cmd_evict, words_from=lambda p: None)

    s = sub.add_parser("revisit", help="after a server restart, ask for the oldest prefix")
    s.add_argument("--state", required=True)
    s.set_defaults(fn=cmd_revisit)

    s = sub.add_parser("batching", help="aggregate and per-stream tok/s by concurrency")
    s.add_argument("--concurrency", type=int, nargs="+", default=[1, 2, 4, 8])
    s.add_argument("--tokens", type=int, default=200)
    s.set_defaults(fn=cmd_batching)

    s = sub.add_parser("staggered", help="short requests arriving behind a long one")
    s.add_argument("--long-tokens", type=int, default=1500)
    s.add_argument("--shorts", type=int, default=3)
    s.set_defaults(fn=cmd_staggered)

    s = sub.add_parser("thinking", help="thinking arms compared on verifiable questions")
    s.add_argument("--arm", action="append", required=True, metavar="NAME=JSON")
    s.add_argument("--reps", type=int, default=1)
    s.add_argument("--max-tokens", type=int, default=4096)
    s.set_defaults(fn=cmd_thinking)

    a = p.parse_args()
    load = os.getloadavg()[0]
    print(f"machine load average {load:.1f} on {os.cpu_count()} cores"
          + ("  <- busy: close other apps or expect noisy numbers" if load > os.cpu_count() / 4 else ""))
    # The first request to a fresh server pays one-time costs (kernel compilation,
    # lazy allocation) that have nothing to do with the thing being measured.
    stream_chat(a.base_url, a.model, [{"role": "user", "content": "Say OK."}], 4)
    if a.cmd == "evict":
        a.words_from = lambda pr, w=a.words: w
    a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
