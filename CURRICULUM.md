# Curriculum

~13 weeks. Each block has an exit criterion — a thing that runs, not a box ticked. Commit at every block boundary.

Three artifacts thread through every block rather than adding time:
the [intake sheet](artifacts/project-intake.md) before each build, the
[selection scorecard](artifacts/selection-scorecard.md) at each decision,
and the [glossary](GLOSSARY.md) accumulating throughout.

---

## Block 0 · Spine & Vocabulary — 0.5 week

Environment that runs, pacing map, and the vocabulary everything else assumes.

- Docker environments for Torch and Keras, pgvector, MLflow
- `lessons/orientation/` — one map placing every term in the program ✅
- `lessons/core-vocabulary/` — 28 lessons: the vocabulary an LLM system is built from, plus overfitting, agents and danger, RLHF and human-in-the-loop, context engineering, structured output, hallucination and grounding, in-context learning, class imbalance and thresholds, drift, distillation, chain-of-thought, and loops at inference and in training ✅
- `lessons/engineering-practice/` — 9 lessons: harnesses, recipes and ADRs; the measurement discipline that corrects them; SWE-bench; invisible confounds; localising a failure; LLM-as-judge; and deterministic-first ✅
- `lessons/algorithms/` — 9 lessons on the algorithms this domain runs on, from gradient descent to HNSW and data leakage ✅
- `lessons/engineering-practice/` — 4 lessons: the three artifacts an LLM project accumulates (harness, recipes, ADRs), how each one turns harmful, why measurement is the only thing that corrects them, and the measurement procedure itself ✅
- Wire in the two finished courses (statistics, governance) ✅

**Exit:** `make up` works, and you can define every term in the glossary without looking.

**Status: 89 lessons built, 89 diagrams, 13 executed notebooks.**

---

## Block 1 · Python, Data & EDA — 1 week
*Original: Pre-work + Module 01*

- pandas and the shape of tabular data — dtypes as a diagnostic, sentinels, units ✅
- Exploratory data analysis as a discipline, not a ritual ✅
- Missing data: MCAR, MAR, MNAR, and why the mechanism decides the fix ✅
- AI-assisted analysis, and where it lies to you ✅

5 lessons in `lessons/block1-data-eda/` and 4 runnable notebooks in
`notebooks/01-python-eda/`, all verified executing end to end.

**Exit:** A clean EDA notebook on a dataset nobody handed you pre-cleaned. ✅
Ends in a threshold decision table: at 0.2 you catch 93% of failures with 770 false
alarms; at 0.7 you catch 44% with 77. Choosing a row is a business decision.

---

## Block 2 · Classical ML — 2 weeks
*Original: Module 02, plus time series which they omit*

- The confusion matrix, precision and recall, ROC and AUC, and when AUC misleads ✅
- The model ladder: baseline → one rule → logistic → forest → boosting, compared honestly ✅
- Neural networks in **Keras 3** and raw PyTorch, with an honest account of when they are wrong ✅
- Time series — because three of the original's own case studies are time-series problems ✅

4 lessons in `lessons/block2-classical-ml/` and 2 notebooks in
`notebooks/02-classical-ml/`, both verified executing end to end.

4 lessons, 4 notebooks and the project, all verified running end to end.

**Exit:** Project 1 — wind turbine failure prediction — runs end to end. ✅
`python src/train.py` produces a report naming the baseline, the leakage audit,
a threshold-free model comparison with an honest verdict on whether the winner is
demonstrably better, and a threshold chosen from costs.

---

## Block 3 · Retrieval and Agentic RAG — 1.5 weeks
*Original: Module 03, extended — the original stops at single-shot retrieval*

- LLMs and prompt engineering
- Embeddings, chunking, vector search against real pgvector — not an in-memory list
- Hybrid retrieval: BM25 and vectors fused by rank; rerankers over the shortlist
- Retrieval quality: what actually makes RAG fail, and measuring index recall
- **Agentic RAG** — retrieval as a loop, its failure modes, and why it should be
  routed to rather than made the default ✅
- Structured outputs and tool calling

5 lessons in `lessons/block3-retrieval/`, 3 notebooks in `notebooks/03-retrieval/`,
and Project 2 in `projects/p2-financial-rag/`.

The corpus is synthetic on purpose: every fact lives in exactly one document, so
the gold labels are genuinely correct and recall@k is measurable rather than
estimated. It plants three multi-hop chains that single-shot retrieval provably
cannot answer, and one question the corpus cannot answer at all.

**Exit:** Project 2 — grounded document assistant — runs end to end. ✅
`python src/rag.py` reports four numbers separately (index recall, retrieval
quality, groundedness, correctness) and states plainly which question types the
system cannot handle.

**Exit:** Project 2 — financial report assistant answers cited questions over a real 10-K.

---

## Block 4 · Agentic AI — 1.5 weeks
*Original: Module 04*

The original is built in **LangGraph / LangChain / LangSmith**. This rebuild uses
**LangGraph** only, and writes traces as local JSON rather than to LangSmith — a
hosted tracer needs an account and an API key, and the telemetry lesson's claim is
that the trace is the only evidence, not that it lives in a particular product. The
Microsoft agents course is Azure/AutoGen-based and lifts as reading only, not code.

- Single-agent loops: the loop written by hand before any framework ✅
- What a graph runtime buys, and what it costs ✅
- Multi-agent systems, handoffs, and approval gates that actually halt ✅
- Telemetry and instrumentation — the trace is the only evidence ✅

5 lessons in `lessons/block4-agentic/`, including the four loop levers and their tradeoffs.
2 notebooks in `notebooks/04-agentic/` — the loop by hand, then the same loop as a
checkpointed graph, which measures what resuming a crashed run costs. Project 3 is built:
`src/pipeline.py` applies the lookup table first, escalates by guard where policy
forbids automating a decision, and calls a model only on the exceptions whose
delivery note contradicts their event code — 98% correct against an 82% baseline.

**Exit:** Project 3 — multi-agent delivery-exception handler runs with human approval, traced to local JSON.

---

## Block 5 · Evaluation — 0.5 week
*Not in the original as a module. It should be.*

Most of this course's evaluation material was already written, scattered by design:
the vocabulary in Block 0, the procedure in engineering practice, the checklist in
`artifacts/sop/measurement.md`. Two of this block's original four topics — why public
benchmarks mislead, and building a private eval set — are taught in
`core-vocabulary/eval-battery`, and LLM-as-judge is taught in
`engineering-practice/models-judging-models`. Restating them here would have been
padding, so this block is a door plus the two genuine gaps.

- Where evaluation lives — the map, and the order that saves a week ✅
- Eval data you can trust: labels that follow from the rules, not from your opinion ✅
- One set, many models: the comparison, and the output budget that silently breaks it ✅

3 lessons in `lessons/block5-evaluation/`. No notebook yet — the natural one runs a
battery across providers, which needs API keys this repository does not assume.

**Exit:** Your own eval set, run across ≥6 models, with a defensible ranking — and a
non-completion column, without which the ranking is not defensible.

---

## Block 6 · Security — 1 week
*Not in the original at all.*

- Prompt injection, direct and indirect — and why the indirect form is the one this
  course's own architecture invites ✅
- Tool abuse and data exfiltration — every tool is a channel, and rendering is one too ✅
- Sandboxing and what actually works: the mitigations ranked by whether the model can
  talk its way past them ✅
- Red-teaming your own Block 4 agent with `agent-armor` and SecLists corpora ✅

4 lessons in `lessons/block6-security/`. No notebook yet — the exercise is run against
Project 3 rather than in isolation, which is the point of it.

**Exit:** You break your own multi-agent system, then fix it.

---

## Block 7 · Training & Fine-Tuning — 1.5 weeks
*Not in the original at all.*

- When fine-tuning is the wrong answer (usually — prompt, then RAG, then this) ✅
- Dataset construction, and how little data you actually need
- LoRA / QLoRA vs full fine-tune, locally on the M4 Max
- **Supervised versus reinforcement fine-tuning** — the objective decides what you get.
  Supervised tuning imitates answers; reinforcement tuning (GRPO and relatives) optimises
  against a reward or a verifier, which is how reasoning behaviour is trained rather than
  copied. Block 0 teaches what a reasoning model is and this is where it gets made.
- **The four ways to shrink a model** ✅ — quantization, pruning, distillation and
  low-rank factorisation as one family; which compose (pruning then distillation as
  repair) and which are alternatives; and that compression does not remove capability
  evenly, so it needs slice evaluation rather than an aggregate.

2 lessons in `lessons/block7-training/`. The remaining bullets need a training run and
a GPU budget, which is where this block gets expensive.
- Evaluating before and after against a held-out set
- Quantization for serving — lands directly on a production agent's GGUF and Q4_K_M

Spine: `LLMS_from_Scratch` ch05–07 (Apache 2.0) plus the installed HF training skills.

**Exit:** A LoRA adapter you trained, evaluated against base, published to the `stylusnexus` HF org.

---

## Block 8 · Deployment & APIs — 2 weeks
*Original: Module 05, expanded — they teach portability in Colab, which cannot demonstrate it*

- Calling an API you do not control — status-code semantics, idempotency for the
  timeout you cannot interpret, jittered backoff ✅
- Serving one yourself — auth, rate limiting, validation, versioning, a health check
  that reports readiness rather than liveness, worked against Project 4 ✅
- The image is the unit — what goes inside, what stays configuration, and image size
  as a decision rather than an outcome ✅
- After it ships — availability against correctness, and why drift needs a scheduled
  measurement rather than a dashboard ✅

4 lessons in `lessons/block8-deployment/`. Deploying to Render or an HF Space remains
a human action; `projects/p4-deployed-assistant/render.yaml` describes it.

**Exit:** Project 4 — an authenticated, rate-limited, containerised endpoint, built and
verified end to end ✅. The deploy itself is a human action: `render.yaml` describes it,
and a public URL has a bill and an audience attached.

---

## Block 9 · Electives — 2 weeks
*Original: the self-paced modules*

Originally six electives. Two are already taught: **Claude workflows and MCP** has four
lessons in Block 0 (`tool-calls-and-mcp`, `building-an-mcp-server`, `mcp-dangers`,
`skills`), and **routing** is covered by `routing-and-escalation`. Building either as an
elective would have duplicated them.

Built:
- When the input is not text — images as tokens, so every context-cost rule applies ✅
- Asking the database properly — the SQL behind intake question one ✅
- Where the money goes — spend attribution, and the four places cost hides. Complements
  Block 0's routing (architecture) with the measurement ✅

Still open: **CNNs and computer vision**, **recommendation systems**. Both are genuinely
missing and both want a training notebook rather than a lesson alone, which is why they
are not here yet.

**Exit:** Each elective has lessons and at least one runnable notebook — met for none of
the three yet; the lessons exist and the notebooks do not.

---

## Already complete

| Block | Where | Status |
|---|---|---|
| Statistical Learning | [`statistics-for-ai`](https://github.com/stylusnexus/statistics-for-ai) | ✅ 10 lessons |
| Responsible AI / Governance | `aigp-exam-prep` (private) | ✅ 12 lessons |

## Projects

| # | Project | Block | Mirrors |
|---|---|---|---|
| 1 | Wind turbine failure prediction | 2 | Original's energy project |
| 2 | Financial report RAG assistant | 3 | Original's finance project |
| 3 | Multi-agent delivery exceptions | 4 | Original's operations project |
| 4 | Deployed energy intelligence assistant | 8 | Original's deployed RAG project |

Each starts with the intake sheet and ends as a published HF Space.
