#!/usr/bin/env python3
"""Landing page for the program, in the same house style as the other courses."""
import html, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
STYLE = (ROOT / "scripts" / "_index_style.html").read_text()
E = html.escape

BLURBS = {
 "inside-an-llm": "Follow one sentence from text to next word — tokenizer, embeddings, transformer blocks, output head, and what each file on disk holds.",
 "tabular-data-and-dtypes": "The dtype a column loads as is a free diagnostic — and 22 sentinel values can shift a mean fourfold.",
 "first-fifteen-minutes": "Survey before you fix: the target's balance, the leaking feature, the duplicates, the missingness pattern.",
 "missing-data-mechanisms": "MCAR, MAR, MNAR — and why 'fill with the median' can destroy exactly the signal you need.",
 "what-a-plot-is-for": "Five questions with decisions attached, and the two chart mistakes that recur everywhere.",
 "ai-assisted-analysis": "Let it write the code, don't let it make the decisions — and check row counts after every transform.",
 "swe-bench-and-how-to-run-it": "How a SWE-bench task is built, how to run it on Apple Silicon, and how to build the same thing from your own merged PRs.",
 "confounds-you-cannot-see": "The limits, overrides and truncations that end a run silently — and get read as model capability.",
 "localising-a-failure": "Control fixtures, metric design, and why a true narrow observation keeps getting promoted to a false general one.",
 "models-judging-models": "LLM-as-judge: four documented biases, and the one failure mode that manufactures effects rather than adding noise.",
 "deterministic-first": "A model is the most expensive, slowest, least testable component you can use — the judgement is knowing when it earns that.",
 "skills": "Procedural knowledge as a loadable folder — progressive disclosure, bundled scripts, and when a skill beats a tool or an MCP server.",
 "operating-an-agent": "Logging trajectories, watching the right proxies, three control switches, and what rots when nothing on your side changed.",
 "building-an-mcp-server": "Six primitives not one, two transports, and the design choices that decide whether an agent uses your server well.",
 "mcp-dangers": "Named attack classes from the spec itself — and why it says the protocol cannot enforce its own security principles.",
 "spec-driven-development": "Vibe coding and spec-driven development as a spectrum — and the one question that tells you where a task belongs on it.",
 "version-control-basics": "Git and GitHub from zero — and why an agent writing the code makes version control more necessary, not less.",
 "local-hardware-limits": "CUDA versus Metal, why capacity beats bandwidth, and the silent CPU fallback that wastes days.",
 "latency-and-caching": "Prefill versus decode, warm and cold states, the cache prefix rule, and why the model is rarely the slow part.",
 "session-lifecycle": "A model has no memory — everything that looks like it is re-sent context, and all of it decays.",
 "rungs-and-experiments": "A ladder of progressively more assistance, where a task starts passing tells you what was wrong.",
 "confusion-matrix-and-metrics": "Four numbers, and every classification metric is built from them — plus what AUC actually means and when it misleads.",
 "baseline-to-model": "A ladder of increasing complexity, climbed only as far as the evidence justifies — and how to compare fairly.",
 "neural-networks-both-ways": "The same network in Keras and raw PyTorch, and an honest account of when it is the wrong tool.",
 "time-series": "Why random splits lie on ordered data, walk-forward validation, and the gap people leave out.",
 "building-a-rag-system": "Five stages, and the two that decide whether the other three matter.",
 "measuring-retrieval": "Index recall, retrieval quality and groundedness — three numbers that fail independently.",
 "agentic-rag": "When one retrieval cannot answer the question, and the failure modes the loop brings with it.",
 "labels-and-holdouts": "Label quality is a ceiling, and the data you refuse to look at is what makes any number believable.",
 "the-loop-by-hand": "Forty lines. Build it once and every framework afterwards is legible.",
 "what-a-graph-buys": "Checkpointing is the feature; everything else you could write in an afternoon.",
 "multi-agent-and-approval": "When splitting is justified, what handoffs cost, and why most approval gates do not stop what matters.",
 "telemetry-and-instrumentation": "You cannot reproduce an agent run, so the trace is the only evidence it happened the way you think.",
 "loop-tradeoffs": "Prefix caching, read accumulation, verification granularity and reasoning effort — each trades tokens against reliability.",
 "the-map": "AI, machine learning, deep learning and generative AI nest inside one another — and agentic AI sits outside because it's an architecture, not a model. Read this first.",
 "agent-loop-and-harness": "The two most-confused words in any agent codebase — and why most agent failures are harness failures, not model failures.",
 "tokens-context-and-kv-cache": "Why a model 'forgets', why long conversations get expensive quadratically, and what prompt caching is actually caching.",
 "weights-gguf-quantization": "What Q4_K_M means character by character, and why a heavily quantized big model beats a small precise one.",
 "serving-locally": "Ollama, llama.cpp and the metal underneath — plus how to read a tokens-per-second number without being misled.",
 "embeddings-and-retrieval": "How a machine decides two things mean the same, the routing it enables, and the three places it quietly fails.",
 "tool-calls-and-mcp": "How a text model comes to run your code, what MCP standardises, and where prompt injection gets its leverage.",
 "routing-and-escalation": "Try cheap, verify, escalate — plus temperature and top-k, which decide how a model picks words.",
 "eval-battery": "How you know any of it works, and why the only number worth trusting is one you built yourself.",
 "overfitting-and-underfitting": "The most important pair of words in machine learning, and the habit that catches the dangerous one.",
 "agents-autonomy-and-danger": "What actually makes something an agent, the autonomy ladder, and every way one can hurt you.",
 "feedback-rlhf-and-humans": "RLHF, DPO and Constitutional AI — plus the difference between in, on, and out of the loop.",
 "context-engineering": "Attention is U-shaped over position, distractors actively hurt, and tool results are context too.",
 "structured-output-json": "The ladder from 'asking nicely' to constrained decoding, and why valid JSON still isn't correct JSON.",
 "gradient-descent-and-backprop": "The one algorithm underneath every trained model, and why training needs so much more memory than inference.",
 "regression-algorithms": "The baseline everything else must beat — and why the threshold, not the model, makes the decision.",
 "decision-trees": "How a split gets chosen, and why depth is the overfitting dial.",
 "ensembles": "Bagging cancels variance, boosting corrects errors — and which to reach for first.",
 "clustering-and-knn": "Two algorithms built on distance, and why distance means less as dimensions rise.",
 "attention-and-transformers": "Query, key, value — and why doubling the context quadruples the cost.",
 "vector-search-algorithms": "HNSW, IVF, and the recall you quietly trade for speed without ever measuring it.",
 "ranking-and-hybrid-retrieval": "BM25, reciprocal rank fusion and rerankers — why pure vector search is rarely best.",
 "data-leakage": "The failure that inflates training and validation together, so nothing looks wrong until production.",
 "loops-at-inference": "Running the model more than once — why verifier-guided retry works, why unaided self-critique often makes things worse.",
 "loops-in-training": "Flywheels that improve a model across generations, and model collapse — the way the tails disappear first.",
 "hallucination-and-grounding": "Why a model states falsehoods confidently, and why telling it not to achieves nothing.",
 "shots-and-in-context-learning": "Zero-, few- and many-shot — what examples are genuinely good at, and when to stop paying for them.",
 "class-imbalance-and-thresholds": "Why 99% accuracy can mean a model that learned nothing, and why 0.5 is just a convention.",
 "drift": "The model didn't change, the world did — and why you monitor inputs when ground truth arrives late.",
 "distillation": "Training a small model to imitate a large one, and the licensing trap that catches people.",
 "chain-of-thought-and-reasoning": "Why thinking out loud works, and why the chain is not an audit trail.",
}

def section(topic, heading, note):
    meta = json.loads((ROOT / "lessons" / topic / "meta.json").read_text())
    cards = []
    for l in meta["lessons"]:
        slug = l["file"].split("-", 2)[2].rsplit(".", 1)[0]
        cards.append(
            f'  <li><a class="card" href="lessons/{topic}/{l["file"]}">\n'
            f'    <h2>{E(l["title"])}</h2>\n'
            f'    <p>{E(BLURBS.get(slug, ""))}</p>\n  </a></li>')
    return (f'<h2 style="margin-top:44px">{heading}</h2>\n'
            f'<p class="lede" style="font-size:1em">{note}</p>\n'
            f'<ol class="lessons">\n{chr(10).join(cards)}\n</ol>'), len(meta["lessons"])

SECTIONS = [
    ("orientation", "Start here", "One picture that places every term in the program. Ten minutes, and the rest makes more sense."),
    ("core-vocabulary", "Block 0 · Vocabulary",
     "The terms the rest of the program assumes — each taught through the failure it explains, rather than as a definition."),
    ("algorithms", "Block 0 · Algorithms",
     "What each algorithm does and where it breaks. Your statistics course covers the maths; this covers the machinery."),
    ("block1-data-eda", "Block 1 · Python, Data and EDA",
     "Real tabular data, read properly. Paired with four runnable notebooks in <code>notebooks/01-python-eda/</code>."),
    ("block2-classical-ml", "Block 2 · Predictive Modelling",
     "Classical machine learning done properly — the metrics, the models, and knowing when a neural network is the wrong answer."),
    ("block3-retrieval", "Block 3 · Retrieval and Agentic RAG",
     "Building a retrieval system that works, measuring the part everyone skips, and the loop that answers multi-hop questions."),
    ("block4-agentic", "Block 4 · Agentic AI",
     "The loop by hand before the framework, what a graph runtime actually buys, and approval gates that halt what matters."),
    ("block5-evaluation", "Block 5 · Evaluation",
     "The front door to the measurement material scattered across this course, then labels you can defend and a cross-model comparison that does not lie."),
    ("block6-security", "Block 6 · Security",
     "Block 0 named the attack classes; this block runs them against the agent you built, starting with the injection your own retrieval pipeline invites."),
    ("block7-training", "Block 7 · Training and Fine-Tuning",
     "When changing the weights is the right answer — rarely — and the four ways to shrink a model, including the fact that compression does not remove capability evenly."),
    ("block8-deployment", "Block 8 · Deployment and APIs",
     "Calling an interface you do not control, serving one other people do not control, and what changes the moment either has a caller who is not you."),
    ("block9-electives", "Block 9 · Electives",
     "Three directions the spine does not cover: input that is not text, asking the database properly, and where the money actually goes."),
    ("engineering-practice", "Block 0 · Engineering Practice",
     "The three artifacts an LLM project accumulates — harness, recipes, decision records — how each one turns harmful, and the measurement procedure that corrects them."),
]

# A topic directory that exists on disk and is missing here would drop out of the
# index silently. That has happened; it is why this assertion is here.
_on_disk = {d.name for d in (ROOT / "lessons").iterdir() if (d / "meta.json").exists()}
_listed = {t for t, _, _ in SECTIONS}
assert not (_on_disk - _listed), (
    f"lesson set(s) on disk but missing from the index: {sorted(_on_disk - _listed)} "
    "— add them to SECTIONS above")

secs, total = [], 0
for topic, heading, note in SECTIONS:
    html_, n = section(topic, heading, note); secs.append(html_); total += n

doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PGP AI/ML — Program Home</title>
{STYLE}
</head>
<body>

<p class="eyebrow">🎯 Self-built program</p>
<h1>Post Graduate Program in AI &amp; Machine Learning</h1>
<p class="lede">A rebuild of the UT Austin / McCombs PGP AI&amp;ML curriculum as ~13 weeks of lessons, runnable notebooks and four portfolio projects — with the security, evaluation, cost and fine-tuning material the original leaves out.</p>

<div class="meta">
  <span class="chip">{total} lessons built</span>
  <span class="chip">10 blocks</span>
  <span class="chip">4 portfolio projects</span>
  <span class="chip">Docker environments</span>
</div>

{chr(10).join(secs)}

<h2 style="margin-top:44px">Already complete elsewhere</h2>
<ol class="lessons">
  <li><a class="card" href="https://github.com/stylusnexus/statistics-for-ai"><h2>Statistical Learning</h2>
    <p>Ten lessons — probability, distributions, the CLT, regression, information theory, evaluation metrics and LLM statistics.</p></a></li>
  <li><a class="card" href="https://github.com/stylusnexus/aigp-exam-prep"><h2>Responsible AI &amp; Governance</h2>
    <p>Twelve lessons — the EU AI Act, NIST AI RMF, ISO 42001, and the governance lifecycle.</p></a></li>
</ol>

<h2 style="margin-top:44px">The program</h2>
<ol class="lessons">
  <li><a class="card" href="CURRICULUM.md"><h2>Curriculum</h2>
    <p>All ten blocks, week by week, each with an exit criterion that runs rather than a box that ticks.</p></a></li>
  <li><a class="card" href="artifacts/project-intake.md"><h2>Project intake sheet</h2>
    <p>Ten questions to answer before writing code. Filled in before every project, reviewed after.</p></a></li>
  <li><a class="card" href="artifacts/selection-scorecard.md"><h2>Selection scorecard</h2>
    <p>For choosing a model, a vendor, or a framework — three decisions with three different failure modes.</p></a></li>
  <li><a class="card" href="things-to-know.html"><h2>Things to Know</h2>
    <p>Every compressed, load-bearing line in the course, collected and linked back to the lesson that earns it.</p></a></li>
  <li><a class="card" href="artifacts/sop/README.md"><h2>SOP checklists</h2>
    <p>Aviation-style: killer items marked, hard gates, and a separate non-normal checklist for when something is already wrong.</p></a></li>
  <li><a class="card" href="GLOSSARY.md"><h2>Glossary</h2>
    <p>Every term the program defines, accumulating block by block and feeding spaced repetition.</p></a></li>
</ol>

</body>
</html>
"""
(ROOT / "index.html").write_text(doc)
print(f"built index.html — {total} lessons across {len(secs)} sets")
