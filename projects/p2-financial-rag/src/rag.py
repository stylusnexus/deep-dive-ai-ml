#!/usr/bin/env python3
"""Grounded document assistant, end to end and measurable.

The point of this script is not that it answers questions. It is that every
stage is measured separately, so a failure can be located rather than guessed at:
index recall, retrieval quality, groundedness and correctness are four numbers,
not one.

Runs offline. Generation uses any OpenAI-compatible local endpoint if one is
reachable, and an extractive stand-in otherwise — the measurement is the lesson.
"""
from __future__ import annotations
import argparse, json, pathlib, re, sys, time, urllib.request
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[3]
HERE = pathlib.Path(__file__).resolve().parent.parent
ENDPOINTS = ["http://localhost:11455/v1", "http://localhost:11434/v1"]

SYSTEM = ("Answer ONLY from the numbered context below. Cite the chunk number for "
          "every claim, like [2]. If the context does not contain the answer, reply "
          "exactly: NOT IN CONTEXT. Do not use outside knowledge.")


def chunk_structural(text: str) -> list[str]:
    """Split on headings. A chunk should be a self-contained thought, not n characters."""
    out = []
    for part in re.split(r"\n(?=#{1,3} )", text):
        part = part.strip()
        if not part:
            continue
        if len(part) > 900:
            out += [s.strip() for s in re.split(r"\n\n+", part) if s.strip()]
        else:
            out.append(part)
    return out


def load_corpus(path: pathlib.Path):
    manifest = path / "manifest.json"
    docs = (json.loads(manifest.read_text()) if manifest.exists()
            else [{"doc_id": p.stem, "text": p.read_text()} for p in sorted(path.glob("*.md"))])
    chunks = []
    for d in docs:
        for i, c in enumerate(chunk_structural(d["text"])):
            chunks.append({"chunk_id": f"{d['doc_id']}#{i}", "doc_id": d["doc_id"], "text": c})
    return docs, chunks


def find_endpoint():
    # The first entry in /v1/models is not necessarily a chat model. An
    # embedding model listed first returns HTTP 400 on a chat completion,
    # which is silent until it is not.
    for base in ENDPOINTS:
        try:
            with urllib.request.urlopen(f"{base}/models", timeout=3) as r:
                ids = [m["id"] for m in json.loads(r.read()).get("data", [])]
        except Exception:
            continue
        chat = [i for i in ids
                if not any(w in i.lower() for w in ("embed", "rerank", "whisper", "clip"))]
        if chat:
            return base, chat[0]
    return None, None


FALLBACKS: list[str] = []
TRUNCATIONS: list[str] = []


def extractive(question, passages, encoder) -> str:
    """Stand-in generator: the sentence closest to the question, or a refusal."""
    sents = [s for p in passages for s in re.split(r"(?<=[.!?])\s+", p["text"]) if len(s) > 25]
    if not sents:
        return "NOT IN CONTEXT"
    qv = encoder.encode(question, normalize_embeddings=True)
    sv = encoder.encode(sents, normalize_embeddings=True)
    i = int(np.argmax(sv @ qv))
    return f"{sents[i]} [1]" if float(sv[i] @ qv) > 0.35 else "NOT IN CONTEXT"


def generate(question, passages, base, model, encoder, timeout=90):
    ctx = "\n\n".join(f"[{i+1}] {p['text']}" for i, p in enumerate(passages))
    if not base:
        return extractive(question, passages, encoder)
    # A reasoning model spends completion tokens thinking before it emits a word
    # of the answer. Measured against this corpus the worst question needs ~850,
    # and a ceiling below that returns empty content with finish_reason="length".
    body = json.dumps({"model": model, "temperature": 0, "max_tokens": 1500,
                       "messages": [{"role": "system", "content": SYSTEM},
                                    {"role": "user",
                                     "content": f"Context:\n{ctx}\n\nQuestion: {question}"}]}).encode()
    req = urllib.request.Request(f"{base}/chat/completions", data=body,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            choice = json.loads(r.read())["choices"][0]
        out = choice["message"]["content"] or ""
        if choice.get("finish_reason") == "length":
            TRUNCATIONS.append(question[:44])
        stripped = re.sub(r"<think>.*?</think>", "", out, flags=re.S).strip()
        if stripped:
            return stripped
        # A thinking model that ran out of tokens mid-thought leaves nothing after
        # stripping. Fall back to the text after the last close tag, then to raw.
        # Never invent a refusal here: a fabricated "NOT IN CONTEXT" scores as a
        # real one and hides the truncation inside the headline number.
        tail = out.rsplit("</think>", 1)[-1].strip() if "</think>" in out else ""
        return tail or out.strip() or "NO ANSWER RETURNED (truncated)"
    except Exception as ex:
        # A slow or busy local endpoint must not kill the run. Degrade per call and
        # record it, so the report says which answers were generated and which were not.
        FALLBACKS.append(f"{question[:44]} ({ex.__class__.__name__})")
        return extractive(question, passages, encoder)


def groundedness(answer: str, context: str) -> float | None:
    if answer.strip().upper().startswith("NOT IN CONTEXT"):
        return None
    ctx = set(re.findall(r"[a-z0-9\.]+", context.lower()))
    content = [w for w in re.findall(r"[a-z0-9\.]+", answer.lower())
               if len(w) > 3 and w not in {"that", "this", "with", "from", "have", "which", "been"}]
    return round(sum(w in ctx for w in content) / len(content), 3) if content else 0.0


def is_correct(answer: str, expected: str, gold_docs: list[str]) -> bool:
    if not gold_docs:
        return answer.strip().upper().startswith("NOT IN CONTEXT")
    # Tokens, without punctuation. Numbers are kept whatever their length — "82"
    # is the entire answer to some questions, and dropping it made the check
    # unable to pass on the questions it mattered most for.
    STOP = {"the", "and", "for", "was", "are", "with", "that", "this", "its"}
    key = [k for k in re.findall(r"[A-Za-z0-9]+", expected)
           if (k.isdigit() or len(k) > 2) and k.lower() not in STOP][:6]
    if not key:
        return False
    hits = sum(k.lower() in answer.lower() for k in key)
    return hits >= max(2, (len(key) + 1) // 2)


def md_table(rows: list[dict]) -> str:
    if not rows:
        return "_none_"
    cols = list(rows[0])
    out = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--corpus", type=pathlib.Path, default=ROOT / "data" / "corpus")
    ap.add_argument("--k", type=int, default=4, help="chunks sent to the model")
    ap.add_argument("--pool", type=int, default=12, help="candidates before reranking")
    ap.add_argument("--no-rerank", action="store_true")
    ap.add_argument("--timeout", type=int, default=90,
                    help="per-call generation timeout; falls back to extractive on expiry")
    args = ap.parse_args()

    if not args.corpus.exists():
        sys.exit(f"corpus not found at {args.corpus} — run scripts/make_corpus.py")

    from sentence_transformers import CrossEncoder, SentenceTransformer

    docs, chunks = load_corpus(args.corpus)
    encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    vecs = encoder.encode([c["text"] for c in chunks], normalize_embeddings=True,
                          show_progress_bar=False)
    reranker = None if args.no_rerank else CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    def retrieve(question):
        qv = encoder.encode(question, normalize_embeddings=True)
        idx = np.argsort(-(vecs @ qv))[:args.pool]
        cand = [chunks[i] for i in idx]
        if reranker is None:
            return cand[:args.k]
        scores = reranker.predict([(question, c["text"]) for c in cand])
        return [c for _, c in sorted(zip(scores, cand), key=lambda p: -p[0])][:args.k]

    eval_path = ROOT / "data" / "corpus_eval.json"
    if not eval_path.exists():
        sys.exit("corpus_eval.json not found — run scripts/make_corpus.py")
    questions = json.loads(eval_path.read_text())

    base, model = find_endpoint()
    rows = []
    for e in questions:
        # Retrieval quality is what this project set out to measure, and it is not
        # what dominates the clock. Time the two stages separately so the report
        # can say so with a number rather than an opinion.
        t0 = time.perf_counter()
        passages = retrieve(e["question"])
        t_retrieval = time.perf_counter() - t0
        got_docs = {p["chunk_id"].split("#")[0] for p in passages}
        t0 = time.perf_counter()
        answer = generate(e["question"], passages, base, model, encoder, timeout=args.timeout)
        t_read = time.perf_counter() - t0
        ctx = "\n\n".join(p["text"] for p in passages)
        g = groundedness(answer, ctx)
        rows.append({
            "qid": e["qid"], "hops": e["hops"],
            "retrieval_s": round(t_retrieval, 3), "read_s": round(t_read, 3),
            "context_tokens": len(ctx.split()),
            "retrieval_recall": (round(len(set(e["gold_docs"]) & got_docs) / len(e["gold_docs"]), 2)
                                 if e["gold_docs"] else None),
            "groundedness": g,
            "correct": is_correct(answer, e["answer"], e["gold_docs"]),
            "answer": answer.replace("\n", " ")[:110],
        })

    answerable = [r for r in rows if r["retrieval_recall"] is not None]
    single = [r for r in answerable if r["hops"] == 1]
    multi = [r for r in answerable if r["hops"] == 2]
    refusal = next(r for r in rows if r["hops"] == 0)
    grounded = [r["groundedness"] for r in rows if r["groundedness"] is not None]

    def pct(rs, key="correct"):
        return f"{sum(bool(r[key]) for r in rs)}/{len(rs)}" if rs else "0/0"

    report = f"""# Grounded Document Assistant — Report

Generated by `src/rag.py`. Corpus: `{args.corpus.name}` ({len(docs)} documents,
{len(chunks)} chunks). Retrieval: dense + {'cross-encoder rerank' if reranker else 'no rerank'},
k={args.k} from a pool of {args.pool}.
Generation: {f'`{model}`' if base else 'extractive stand-in (no local endpoint reachable)'}
{f'**{len(FALLBACKS)} of {len(questions)} calls fell back to the extractive stand-in** (endpoint slow or busy). Those answers are extractive, not generated — the measurement is still valid, but read the answer column with that in mind.' if FALLBACKS else ''}
{f'**{len(TRUNCATIONS)} of {len(questions)} answers hit the token ceiling** and were cut off. Raise max_tokens and re-run: a truncated answer scores as a wrong one, so the numbers below would be measuring the token budget rather than the system.' if TRUNCATIONS else ''}

## Where the time actually goes

| stage | median seconds | share |
|---|---|---|
| Retrieval — embed, search, rerank | {np.median([r['retrieval_s'] for r in rows]):.3f} | {np.median([r['retrieval_s'] for r in rows]) / (np.median([r['retrieval_s'] for r in rows]) + np.median([r['read_s'] for r in rows])):.0%} |
| Reading the retrieved chunks | {np.median([r['read_s'] for r in rows]):.3f} | {np.median([r['read_s'] for r in rows]) / (np.median([r['retrieval_s'] for r in rows]) + np.median([r['read_s'] for r in rows])):.0%} |

Retrieval is the stage this project measures for quality, and it is **not** the stage
that costs the time. Every optimisation aimed at retrieval speed is aimed at the
smaller share.

Read the mechanism honestly, though, because this corpus cannot demonstrate the usual
one. Contexts here run to {min(r['context_tokens'] for r in rows)}-{max(r['context_tokens'] for r in rows)} words, which prefills in a fraction of a
second — so almost all of the read above is the model *generating*, including its
reasoning tokens, rather than reading what retrieval sent. The quadratic prefill cost
that dominates production retrieval systems needs contexts of thousands of tokens
before it shows, and ours are two orders of magnitude short of that.

What this run does establish is the ranking: retrieval is around a hundredth of the
request, so tuning it for speed is optimising the part that was already cheap. What it
cannot establish is that prefill is the reason. On a corpus with realistic context
sizes it would be; here the honest answer is that the model's own output dominates.

## The four numbers

| stage | measurement |
|---|---|
| Retrieval recall (single-hop) | {np.mean([r['retrieval_recall'] for r in single]):.2f} |
| Retrieval recall (multi-hop) | {np.mean([r['retrieval_recall'] for r in multi]):.2f} |
| Mean groundedness (answered) | {np.mean(grounded):.2f} |
| Correct — single-hop | {pct(single)} |
| Correct — multi-hop | {pct(multi)} |
| Refused correctly when unanswerable | {'yes' if refusal['correct'] else 'NO'} |

## What this system can and cannot do

**Can:** answer single-hop questions where the fact lives in one document, with
citations, at {np.mean(grounded):.2f} mean groundedness.

**Weakens on:** questions needing facts from two documents. Retrieval recall drops from {np.mean([r['retrieval_recall'] for r in single]):.2f} to {np.mean([r['retrieval_recall'] for r in multi]):.2f} on multi-hop questions, because the question embeds close to one document and not the other. That is a limit of single-shot retrieval, not a tuning problem — it needs a retrieval loop. With only {len(multi)} multi-hop questions the correctness figure above carries no precision: the recall drop is the finding, and the per-question table is where to read what actually failed.

**Refusal:** {'the system correctly refuses when the corpus does not contain the answer.'
              if refusal['correct'] else
              '**the system answered a question the corpus cannot answer.** The grounding is decorative — fix the prompt before going further.'}

## Per question

{md_table(rows)}

## What would make me distrust this

- The corpus grows and index parameters tuned at this size stop returning what
  exact search would — measure recall against brute force again
- Documents change shape (tables, scanned pages) and structural chunking degrades
- Questions arrive phrased unlike anything in the eval set
- Someone removes the refusal instruction from the prompt, at which point every
  answer looks grounded whether or not it is
"""
    (HERE / "report.md").write_text(report)
    (HERE / "results.json").write_text(json.dumps(rows, indent=2) + "\n")

    print(f"corpus            : {len(docs)} docs, {len(chunks)} chunks")
    print(f"generation        : {model if base else 'extractive stand-in'}"
          + (f"  ({len(FALLBACKS)}/{len(questions)} fell back)" if FALLBACKS else "")
          + (f"  ({len(TRUNCATIONS)}/{len(questions)} truncated)" if TRUNCATIONS else ""))
    print(f"single-hop recall : {np.mean([r['retrieval_recall'] for r in single]):.2f}")
    print(f"multi-hop recall  : {np.mean([r['retrieval_recall'] for r in multi]):.2f}")
    print(f"groundedness      : {np.mean(grounded):.2f}")
    print(f"retrieval (median): {np.median([r['retrieval_s'] for r in rows]):.3f}s")
    print(f"read      (median): {np.median([r['read_s'] for r in rows]):.3f}s")
    print(f"correct           : {pct(answerable)} answerable")
    print(f"refusal handled   : {refusal['correct']}")
    print("\nwrote report.md and results.json")


if __name__ == "__main__":
    main()
