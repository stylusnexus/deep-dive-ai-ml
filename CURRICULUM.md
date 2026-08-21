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

**Status: 39 lessons built, 34 diagrams, 4 executed notebooks.**

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

3 lessons in `lessons/block3-retrieval/`. Notebooks and Project 2 still to build.

**Exit:** Project 2 — financial report assistant answers cited questions over a real 10-K.

---

## Block 4 · Agentic AI — 1.5 weeks
*Original: Module 04*

Built in **LangGraph / LangChain / LangSmith**, matching the original. The Microsoft agents course is Azure/AutoGen-based and lifts as reading only, not code.

- Single-agent loops: reasoning, memory, tools
- Multi-agent systems and handoffs
- Human-in-the-loop and escalation

**Exit:** Project 3 — multi-agent delivery-exception handler runs with human approval, traced in LangSmith.

---

## Block 5 · Evaluation — 0.5 week
*Not in the original as a module. It should be.*

- Why public benchmarks mislead: contamination, gaming, task mismatch
- Building a 20-item private eval set — the `honest-bench` premise
- Running one eval set across many models via HF Inference Providers
- LLM-as-judge, and when it's circular

**Exit:** Your own eval set, run across ≥6 models, with a defensible ranking.

---

## Block 6 · Security — 1 week
*Not in the original at all.*

- Prompt injection, direct and indirect
- Tool abuse and data exfiltration through agents
- Sandboxing agents in containers — the actual mitigation
- Red-teaming your own Block 4 agent with `agent-armor` and SecLists corpora

**Exit:** You break your own multi-agent system, then fix it.

---

## Block 7 · Training & Fine-Tuning — 1.5 weeks
*Not in the original at all.*

- When fine-tuning is the wrong answer (usually — prompt, then RAG, then this)
- Dataset construction, and how little data you actually need
- LoRA / QLoRA vs full fine-tune, locally on the M4 Max
- Evaluating before and after against a held-out set
- Quantization for serving — lands directly on a production agent's GGUF and Q4_K_M

Spine: `LLMS_from_Scratch` ch05–07 (Apache 2.0) plus the installed HF training skills.

**Exit:** A LoRA adapter you trained, evaluated against base, published to the `stylusnexus` HF org.

---

## Block 8 · Deployment & APIs — 2 weeks
*Original: Module 05, expanded — they teach portability in Colab, which cannot demonstrate it*

- Consuming APIs properly: auth, retries, backoff, streaming, idempotency, token budgeting
- Serving APIs: FastAPI, validation, auth, rate limiting, versioning, health checks
- Containerize a model; run locally; push the same image
- Deploy to Render and to an HF Space (ZeroGPU)
- Monitoring, drift, and when to retrain

**Exit:** Project 4 — a deployed, authenticated, rate-limited endpoint with a public URL.

---

## Block 9 · Electives — 2 weeks
*Original: the self-paced modules*

CNNs and computer vision · multimodal · recommendation systems · SQL · Claude workflows and MCP · cost and routing engineering.

**Exit:** Each elective has lessons and at least one runnable notebook.

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
