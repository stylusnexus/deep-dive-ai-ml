OUTDIR = "notebooks/03-retrieval"

_SETUP = '''import json, re, textwrap
import numpy as np, pandas as pd
from pathlib import Path

pd.set_option("display.width", 130); pd.set_option("display.max_colwidth", 70)

ROOT = Path.cwd()
while not (ROOT / "data" / "corpus").exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
CORPUS = ROOT / "data" / "corpus"
DOCS = json.loads((CORPUS / "manifest.json").read_text())
EVAL = json.loads((ROOT / "data" / "corpus_eval.json").read_text())
print(f"{len(DOCS)} documents, {len(EVAL)} eval questions")'''

NOTEBOOKS = [
("01-chunking-and-embedding.ipynb", [
("md", """# 01 · Chunking, Embedding and the Index

The corpus is small and synthetic on purpose: every fact lives in exactly one
document, so the evaluation labels are genuinely correct rather than estimated.
That makes recall@k measurable instead of arguable.

This notebook does the two stages that decide everything — chunking and
indexing — and shows what a bad chunking choice costs before you notice it."""),
("code", _SETUP),
("code", """for d in DOCS[:3]:
    print(f"--- {d['doc_id']}  ({d['kind']})  {len(d['text'].split())} words")
print("\\nkinds:", pd.Series([d["kind"] for d in DOCS]).value_counts().to_dict())"""),
("md", """## Two chunking strategies

The naive one splits on a fixed character count. The structural one splits on
markdown headings, which is what a self-contained thought looks like in this
corpus.

Both are defensible in the abstract. Read the output and only one of them is."""),
("code", """def chunk_fixed(text, size=350, overlap=50):
    out, i = [], 0
    while i < len(text):
        out.append(text[i:i+size])
        i += size - overlap
    return out

def chunk_structural(text):
    parts = re.split(r"\\n(?=#{1,3} )", text)
    out = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if len(p) > 900:                      # long section: split on blank lines
            out += [s.strip() for s in re.split(r"\\n\\n+", p) if s.strip()]
        else:
            out.append(p)
    return out

sample = next(d for d in DOCS if d["doc_id"] == "ops-std-04")["text"]
print("FIXED-SIZE — first three chunks\\n")
for c in chunk_fixed(sample)[:3]:
    print(repr(c[:150]), "\\n")"""),
("code", """print("STRUCTURAL — first three chunks\\n")
for c in chunk_structural(sample)[:3]:
    print(repr(c[:150]), "\\n")"""),
("md", """### Read those two outputs

The fixed-size chunks start and end mid-sentence. One of them begins with
`degrees the turbine enters` — that fragment has lost the number it refers to
and the condition it applies under. Embed it and you get a vector for a
half-thought.

The structural chunks are whole sections. Each one can be read alone.

**This is the ten minutes the lesson said not to skip.**"""),
("code", """chunks = []
for d in DOCS:
    for i, c in enumerate(chunk_structural(d["text"])):
        chunks.append({"chunk_id": f"{d['doc_id']}#{i}", "doc_id": d["doc_id"],
                       "kind": d["kind"], "text": c})
chunks = pd.DataFrame(chunks)
print(f"{len(chunks)} chunks from {len(DOCS)} documents")
print(f"words per chunk: median {chunks['text'].str.split().str.len().median():.0f}, "
      f"max {chunks['text'].str.split().str.len().max()}")
chunks.head(3)[["chunk_id","kind"]]"""),
("md", """## Embedding

A small local model — no API key, and it runs offline. 384 dimensions."""),
("code", """from sentence_transformers import SentenceTransformer

encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
vecs = encoder.encode(chunks["text"].tolist(), normalize_embeddings=True,
                      show_progress_bar=False)
print("embedding matrix:", vecs.shape)"""),
("md", """### Sanity-check the embeddings before trusting them

If a paraphrase does not score higher than an unrelated sentence, something is
wrong with the model or the text, and no amount of retrieval tuning will help."""),
("code", """probe = encoder.encode([
    "maximum gearbox oil temperature",       # 0
    "how hot can the gearbox get",           # 1 — paraphrase of 0
    "who manages the Clyde site",            # 2 — unrelated
], normalize_embeddings=True)

print(f"paraphrase pair   : {float(probe[0] @ probe[1]):.3f}")
print(f"unrelated pair    : {float(probe[0] @ probe[2]):.3f}")
print("✅ sensible" if probe[0] @ probe[1] > probe[0] @ probe[2] + 0.15
      else "❌ embeddings are not separating meaning — stop here")"""),
("md", """## Into pgvector

A real index rather than an in-memory list, because the lesson about index
recall only means something against a real index.

Requires the container: `make up` or `docker compose -f docker/compose.yaml up -d pgvector`."""),
("code", """import psycopg2
from psycopg2.extras import execute_values

DSN = "host=localhost port=5433 dbname=aiml user=aiml password=aiml"
try:
    conn = psycopg2.connect(DSN); conn.autocommit = True
    HAVE_PG = True
    print("connected to pgvector")
except Exception as e:
    HAVE_PG = False
    print("pgvector not reachable — the notebook falls back to numpy exact search")
    print(f"  ({e.__class__.__name__})  start it with: docker compose -f docker/compose.yaml up -d pgvector")"""),
("code", """if HAVE_PG:
    with conn.cursor() as cur:
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
        cur.execute("DROP TABLE IF EXISTS chunks")
        cur.execute(\"\"\"CREATE TABLE chunks (
                         chunk_id text PRIMARY KEY,
                         doc_id   text,
                         kind     text,
                         body     text,
                         embedding vector(384))\"\"\")
        execute_values(cur,
            "INSERT INTO chunks (chunk_id, doc_id, kind, body, embedding) VALUES %s",
            [(r.chunk_id, r.doc_id, r.kind, r.text, list(map(float, v)))
             for r, v in zip(chunks.itertuples(), vecs)])
        cur.execute("SELECT count(*) FROM chunks")
        print(f"{cur.fetchone()[0]} chunks indexed")"""),
("md", """### An index, and the parameter that decides recall

`ef_search` is the dial to move when recall is low — raise it before rebuilding
with a larger `M`."""),
("code", """if HAVE_PG:
    with conn.cursor() as cur:
        cur.execute(\"\"\"CREATE INDEX chunks_hnsw ON chunks
                       USING hnsw (embedding vector_cosine_ops)
                       WITH (m = 16, ef_construction = 64)\"\"\")
        cur.execute("SET hnsw.ef_search = 40")
        cur.execute(\"\"\"SELECT chunk_id, 1 - (embedding <=> %s::vector) AS score
                       FROM chunks ORDER BY embedding <=> %s::vector LIMIT 3\"\"\",
                    (list(map(float, encoder.encode("gearbox temperature limit",
                                                    normalize_embeddings=True))),) * 2)
        for cid, sc in cur.fetchall():
            print(f"  {sc:.3f}  {cid}")"""),
("md", """## Save the artefacts for the next notebook"""),
("code", """np.save(ROOT / "data" / "chunk_vecs.npy", vecs)
chunks.to_csv(ROOT / "data" / "chunks.csv", index=False)
print(f"saved {len(chunks)} chunks and their embeddings")"""),
("md", """---

## Your turn

1. Re-run with `chunk_fixed` instead of `chunk_structural` and keep the file.
   Notebook 02 will measure what it costs you.
2. Change `ef_search` to 4 and re-run the query. Do the top results change?
3. Print ten random chunks and read them. Would you be able to answer a question
   from any one of them alone?"""),
]),

("02-retrieval-quality.ipynb", [
("md", """# 02 · Measuring Retrieval

Three numbers, measured separately, because they fail independently.

You will measure index recall against exact search, compare four retrieval
strategies against gold labels, and see the specific questions that single-shot
retrieval cannot answer regardless of strategy."""),
("code", _SETUP),
("code", """import numpy as np, pandas as pd
from sentence_transformers import SentenceTransformer

chunks = pd.read_csv(ROOT / "data" / "chunks.csv")
vecs = np.load(ROOT / "data" / "chunk_vecs.npy")
encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
qvecs = encoder.encode([e["question"] for e in EVAL], normalize_embeddings=True)
print(f"{len(chunks)} chunks | {vecs.shape[1]}-dim | {len(EVAL)} questions")"""),
("md", """## Strategy 1 — dense vector search"""),
("code", """def dense(qv, k=5):
    scores = vecs @ qv
    idx = np.argsort(-scores)[:k]
    return chunks.iloc[idx]["chunk_id"].tolist()

def docs_of(chunk_ids):
    return {c.split("#")[0] for c in chunk_ids}

def recall_at_k(strategy, k=5):
    hits = []
    for e, qv in zip(EVAL, qvecs):
        if not e["gold_docs"]:
            continue                                  # unanswerable, scored separately
        got = docs_of(strategy(qv, k) if strategy is dense else strategy(e, k))
        hits.append(len(set(e["gold_docs"]) & got) / len(e["gold_docs"]))
    return float(np.mean(hits))

print(f"dense recall@5 : {recall_at_k(dense):.3f}")"""),
("md", """## Strategy 2 — BM25 keyword search

Best Matching 25. No model, no index, no GPU — and on identifier-heavy text it
is frequently the stronger of the two."""),
("code", """from rank_bm25 import BM25Okapi

def tok(s): return re.findall(r"[a-z0-9\\-]+", s.lower())
bm25 = BM25Okapi([tok(t) for t in chunks["text"]])

def keyword(e, k=5):
    scores = bm25.get_scores(tok(e["question"]))
    return chunks.iloc[np.argsort(-scores)[:k]]["chunk_id"].tolist()

print(f"BM25 recall@5  : {recall_at_k(keyword):.3f}")"""),
("md", """## Strategy 3 — hybrid, fused by rank

Reciprocal rank fusion. It uses only positions, so the incomparable scores of the
two systems never need normalising. Two lines."""),
("code", """def rrf(e, k=5, pool=20, kconst=60):
    qv = encoder.encode(e["question"], normalize_embeddings=True)
    d_ids = chunks.iloc[np.argsort(-(vecs @ qv))[:pool]]["chunk_id"].tolist()
    b_ids = chunks.iloc[np.argsort(-bm25.get_scores(tok(e["question"])))[:pool]]["chunk_id"].tolist()
    fused = {}
    for lst in (d_ids, b_ids):
        for rank, cid in enumerate(lst, 1):
            fused[cid] = fused.get(cid, 0) + 1 / (kconst + rank)
    return [cid for cid, _ in sorted(fused.items(), key=lambda kv: -kv[1])][:k]

print(f"hybrid recall@5: {recall_at_k(rrf):.3f}")"""),
("md", """## Strategy 4 — hybrid, then rerank

A cross-encoder scores query and chunk *together* rather than separately. Far
more accurate, and only affordable because it runs over a shortlist."""),
("code", """from sentence_transformers import CrossEncoder
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(e, k=5, pool=20):
    cand = rrf(e, k=pool, pool=pool)
    texts = [chunks.loc[chunks.chunk_id == c, "text"].iloc[0] for c in cand]
    scores = reranker.predict([(e["question"], t) for t in texts])
    return [c for _, c in sorted(zip(scores, cand), key=lambda p: -p[0])][:k]

print(f"reranked recall@5: {recall_at_k(rerank):.3f}")"""),
("md", """## The comparison"""),
("code", """board = pd.DataFrame([
    {"strategy": "dense (vector)",       "recall@5": round(recall_at_k(dense), 3)},
    {"strategy": "BM25 (keyword)",       "recall@5": round(recall_at_k(keyword), 3)},
    {"strategy": "hybrid (RRF)",         "recall@5": round(recall_at_k(rrf), 3)},
    {"strategy": "hybrid + rerank",      "recall@5": round(recall_at_k(rerank), 3)},
]).sort_values("recall@5", ascending=False)
board"""),
("md", """## Where each strategy fails

An aggregate hides which questions are broken. Look per question."""),
("code", """rows = []
for e, qv in zip(EVAL, qvecs):
    if not e["gold_docs"]:
        continue
    r = {"qid": e["qid"], "hops": e["hops"], "question": e["question"][:52]}
    for name, fn in [("dense", lambda: docs_of(dense(qv))),
                     ("bm25", lambda: docs_of(keyword(e))),
                     ("hybrid", lambda: docs_of(rrf(e))),
                     ("rerank", lambda: docs_of(rerank(e)))]:
        r[name] = round(len(set(e["gold_docs"]) & fn()) / len(e["gold_docs"]), 2)
    rows.append(r)
per_q = pd.DataFrame(rows)
per_q"""),
("md", """### Read the `hops` column

Look at where the scores drop. The multi-hop questions need facts from two
documents, and no single-shot strategy reliably retrieves both — because the
question embeds close to one of them and not the other.

**That is not a tuning problem.** It is the limit that agentic retrieval exists
to address, and notebook 03 shows the loop clearing it."""),
("code", """print(per_q.groupby("hops")[["dense","bm25","hybrid","rerank"]].mean().round(3))
print("\\nsingle-hop questions are largely solved; multi-hop are not.")"""),
("md", """## Index recall — the number nobody measures

Everything above assumed the index returned what exact search would. Check it."""),
("code", """try:
    import psycopg2
    conn = psycopg2.connect("host=localhost port=5433 dbname=aiml user=aiml password=aiml")
    conn.autocommit = True
    rows = []
    for ef in [4, 10, 40, 200]:
        agree = []
        for qv in qvecs:
            exact = set(chunks.iloc[np.argsort(-(vecs @ qv))[:5]]["chunk_id"])
            with conn.cursor() as cur:
                cur.execute("SET hnsw.ef_search = %s", (ef,))
                cur.execute("SELECT chunk_id FROM chunks ORDER BY embedding <=> %s::vector LIMIT 5",
                            (list(map(float, qv)),))
                approx = {r[0] for r in cur.fetchall()}
            agree.append(len(exact & approx) / 5)
        rows.append({"ef_search": ef, "recall@5_vs_exact": round(float(np.mean(agree)), 3)})
    display(pd.DataFrame(rows))
    print("\\nRaise ef_search before rebuilding the index. It costs latency, not a rebuild.")
except Exception as ex:
    print(f"pgvector not reachable ({ex.__class__.__name__}) — run notebook 01 first")"""),
("md", """---

## What this established

- Four strategies measured against gold labels, not impressions
- Where each one fails, per question, rather than as one average
- Multi-hop questions are not a tuning problem
- Index recall measured against exact search across `ef_search` settings

## Your turn

1. Re-run notebook 01 with `chunk_fixed`, then re-run this notebook. How much
   recall does bad chunking cost?
2. Set `pool` to 5 in `rrf`. Does reranking still help?
3. Add a question of your own with a gold label and see which strategies find it."""),
]),
("03-grounded-answers.ipynb", [
("md", """# 03 · Grounded Answers, and Measuring Them

Retrieval is only half the system. This notebook generates answers from the
retrieved context, then measures the two things that fail independently:

- **Groundedness** — is every claim supported by what was retrieved?
- **Correctness** — is the answer actually right?

And it tests the case most systems get wrong: a question the corpus cannot
answer, where the correct behaviour is refusal."""),
("code", _SETUP),
("code", """import numpy as np, pandas as pd, re
from sentence_transformers import SentenceTransformer, CrossEncoder

chunks = pd.read_csv(ROOT / "data" / "chunks.csv")
vecs = np.load(ROOT / "data" / "chunk_vecs.npy")
encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def retrieve(question, k=4, pool=12):
    qv = encoder.encode(question, normalize_embeddings=True)
    cand = chunks.iloc[np.argsort(-(vecs @ qv))[:pool]]
    scores = reranker.predict([(question, t) for t in cand["text"]])
    top = cand.assign(score=scores).nlargest(k, "score")
    return top[["chunk_id", "text"]].to_dict("records")

print(f"{len(chunks)} chunks ready")"""),
("md", """## A generator

Points at any OpenAI-compatible endpoint. LM Studio and Ollama both expose one,
so this runs locally with no API key. If nothing is reachable the notebook falls
back to an extractive stand-in so the **measurement** still runs — which is the
part this notebook is actually teaching."""),
("code", """import urllib.request, json as _json

ENDPOINTS = ["http://localhost:11455/v1", "http://localhost:11434/v1"]

def find_endpoint():
    # The first entry in /v1/models is not necessarily a chat model. An
    # embedding model listed first returns HTTP 400 on a chat completion,
    # which is silent until it is not.
    for base in ENDPOINTS:
        try:
            with urllib.request.urlopen(f"{base}/models", timeout=3) as r:
                ids = [m["id"] for m in _json.loads(r.read()).get("data", [])]
        except Exception:
            continue
        chat = [i for i in ids
                if not any(w in i.lower() for w in ("embed", "rerank", "whisper", "clip"))]
        if chat:
            return base, chat[0]
    return None, None

BASE, MODEL = find_endpoint()
print(f"using {MODEL} at {BASE}" if BASE else "no local endpoint — using the extractive fallback")"""),
("code", """SYSTEM = (
    "Answer ONLY from the numbered context below. "
    "Cite the chunk number for every claim, like [2]. "
    "If the context does not contain the answer, reply exactly: NOT IN CONTEXT. "
    "Do not use outside knowledge."
)

FALLBACKS = []

def extractive(question, passages):
    # stand-in generator: the sentence most similar to the question, or a refusal
    sents = [s for p in passages for s in re.split(r"(?<=[.!?])\\s+", p["text"]) if len(s) > 25]
    if not sents:
        return "NOT IN CONTEXT"
    qv = encoder.encode(question, normalize_embeddings=True)
    sv = encoder.encode(sents, normalize_embeddings=True)
    best = int(np.argmax(sv @ qv))
    return f"{sents[best]} [1]" if float(sv[best] @ qv) > 0.35 else "NOT IN CONTEXT"

def ask_model(question, passages):
    ctx = "\\n\\n".join(f"[{i+1}] {p['text']}" for i, p in enumerate(passages))
    if not BASE:
        return extractive(question, passages)
    body = _json.dumps({"model": MODEL, "temperature": 0, "max_tokens": 200,
                        "messages": [{"role": "system", "content": SYSTEM},
                                     {"role": "user",
                                      "content": f"Context:\\n{ctx}\\n\\nQuestion: {question}"}]}).encode()
    req = urllib.request.Request(f"{BASE}/chat/completions", data=body,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            out = _json.loads(r.read())["choices"][0]["message"]["content"]
        return re.sub(r"<think>.*?</think>", "", out, flags=re.S).strip()
    except Exception as ex:
        # A slow or busy endpoint must not break the notebook. Fall back per call
        # and record it — the measurement is what this notebook teaches.
        FALLBACKS.append((question[:40], ex.__class__.__name__))
        return extractive(question, passages)

demo_q = "What is the maximum gearbox oil temperature during continuous operation?"
print(ask_model(demo_q, retrieve(demo_q)))"""),
("md", """## Run the whole eval set"""),
("code", """results = []
for e in EVAL:
    passages = retrieve(e["question"])
    answer = ask_model(e["question"], passages)
    results.append({"qid": e["qid"], "hops": e["hops"], "question": e["question"],
                    "answer": answer,
                    "retrieved_docs": sorted({p["chunk_id"].split("#")[0] for p in passages}),
                    "gold_docs": e["gold_docs"], "expected": e["answer"],
                    "context": "\\n\\n".join(p["text"] for p in passages)})
res = pd.DataFrame(results)
if FALLBACKS:
    print(f"note: {len(FALLBACKS)} of {len(EVAL)} calls fell back to the extractive "
          f"stand-in ({FALLBACKS[0][1]}). The measurement below is still valid; the")
    print("answers for those questions are extractive rather than generated.")
res[["qid","hops","answer"]].head(10)"""),
("md", """## Measurement 1 — groundedness

Is every claim supported by the retrieved text? Scored here without a judge model
by checking whether the answer's substantive content appears in the context.

Crude on purpose: a judge would be more flexible and would introduce the biases
the judging lesson covers. For a corpus this literal, overlap is honest."""),
("code", """def groundedness(answer, context):
    if answer.strip().upper().startswith("NOT IN CONTEXT"):
        return None                                   # refusal, scored separately
    ctx = set(re.findall(r"[a-z0-9\\.]+", context.lower()))
    content = [w for w in re.findall(r"[a-z0-9\\.]+", answer.lower())
               if len(w) > 3 and w not in {"that","this","with","from","have","which","been"}]
    if not content:
        return 0.0
    return round(sum(w in ctx for w in content) / len(content), 3)

res["groundedness"] = [groundedness(a, c) for a, c in zip(res["answer"], res["context"])]
res[["qid","hops","groundedness","answer"]]"""),
("md", """## Measurement 2 — correctness

Separate question, and the combination is what tells you where to work."""),
("code", """def correct(row):
    if not row["gold_docs"]:
        return row["answer"].strip().upper().startswith("NOT IN CONTEXT")
    key = re.findall(r"[A-Za-z0-9\\.]+", row["expected"])
    key = [k for k in key if len(k) > 2 and k.lower() not in {"the","and","for","was","are"}][:6]
    return sum(k.lower() in row["answer"].lower() for k in key) >= max(2, len(key)//2)

res["correct"] = res.apply(correct, axis=1)
summary = res.groupby("hops").agg(n=("qid","size"),
                                  correct=("correct","sum"),
                                  mean_groundedness=("groundedness","mean")).round(3)
summary"""),
("md", """### The diagnostic table

Cross groundedness against correctness. Each cell means something different:"""),
("code", """def cell(r):
    if r["groundedness"] is None:
        return "refused"
    g = r["groundedness"] >= 0.7
    c = bool(r["correct"])
    return {(True,True): "grounded + correct",
            (True,False): "grounded + WRONG  -> retrieval problem",
            (False,True): "ungrounded + right -> answering from memory (warning)",
            (False,False): "ungrounded + wrong -> generation problem"}[(g,c)]

res["diagnosis"] = res.apply(cell, axis=1)
print(res["diagnosis"].value_counts().to_string())
print()
res[["qid","hops","diagnosis"]]"""),
("md", """**Grounded and wrong is a retrieval problem.** The model faithfully used what it
was given, and it was given the wrong thing. Look at the multi-hop questions here —
notebook 02 showed single-shot retrieval cannot reliably fetch both documents, and
this is what that failure looks like at the end of the pipeline.

**Ungrounded and right is a warning.** The model answered from its parameters and
happened to be correct. It will not always be."""),
("md", """## The refusal test

The most important single question in the set. `q10` asks something the corpus
does not contain. The correct behaviour is to say so."""),
("code", """r10 = res[res.qid == "q10"].iloc[0]
print("QUESTION :", r10["question"])
print("ANSWER   :", r10["answer"][:300])
refused = r10["answer"].strip().upper().startswith("NOT IN CONTEXT")
print(f"\\n{'✅ refused correctly — the system is genuinely grounded' if refused else '❌ answered anyway — the grounding is decorative'}")
print("\\nRetrieval still returned chunks (it always does — similarity is relative),")
print("so refusing depends entirely on the prompt handling the empty case:")
print(" ", r10["retrieved_docs"])"""),
("md", """### Why that one question matters most

Retrieval **always** returns something. Similarity is relative, so the nearest
chunks come back whether or not any of them are relevant.

If the prompt does not explicitly license refusal, the model will write a fluent,
cited-looking answer from whatever arrived plus its own parameters — and it will
be indistinguishable in tone from the answers that were genuinely grounded.

That is where grounded systems quietly stop being grounded."""),
("code", """res.to_csv(ROOT / "data" / "rag_eval_results.csv", index=False)
print(f"saved results for {len(res)} questions")
print(f"\\ncorrect        : {res['correct'].sum()}/{len(res)}")
print(f"mean groundedness (answered): {res['groundedness'].dropna().mean():.3f}")"""),
("md", """---

## Your turn

1. Remove the refusal instruction from `SYSTEM` and re-run `q10`. What comes back?
2. Set `k=1` in `retrieve`. Which questions break first, and are they the ones you
   expected?
3. Add a question whose answer is in the corpus but phrased completely differently.
   Does retrieval find it?"""),
]),
]
