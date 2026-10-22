#!/usr/bin/env python3
"""Landing page for the program, in the same house style as the other courses."""
import html, json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from seo_meta import head_meta, course_jsonld, plain
from lesson_map import slug_map
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
 "benchmarks-what-to-trust": "Quality benchmarks, leaderboards, serving benchmarks and load tests answer different questions — how public ones fail, which tools exist, and when to build your own.",
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
 "quantization-recipes": "Plain rounding, GPTQ, AWQ, DWQ, importance matrices and mixed precision — same bits, chosen better — with where to get them and how to judge one.",
 "serving-locally": "Ollama, llama.cpp and the metal underneath — plus how to read a tokens-per-second number without being misled.",
 "formats-and-engines": "Container, method and kernel are three different things called the format — GGUF, MLX and the NVIDIA checkpoints, measured on a Mac and cited for NVIDIA.",
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

SECTIONS = [
    ("orientation", "Start here", "One picture that places every term in the program. Ten minutes, and the rest makes more sense."),
    ("core-vocabulary", "Block 0 · Vocabulary",
     "The terms the rest of the program assumes — each taught through the failure it explains, rather than as a definition."),
    ("algorithms", "Block 0 · Algorithms",
     "What each algorithm does and where it breaks. Your statistics course covers the maths; this covers the machinery."),
    ("block1-data-eda", "Block 1 · Python, Data and Exploratory Analysis",
     "Real tabular data, read properly. Paired with four runnable notebooks in <code>notebooks/01-python-eda/</code>."),
    ("block2-classical-ml", "Block 2 · Predictive Modelling",
     "Classical machine learning done properly — the metrics, the models, and knowing when a neural network is the wrong answer."),
    ("block3-retrieval", "Block 3 · Retrieval-Augmented Generation (RAG)",
     "Building a retrieval system that works, measuring the part everyone skips, the loop that answers multi-hop questions, and what changes at millions of documents."),
    ("block4-agentic", "Block 4 · Agentic AI",
     "The loop by hand before the framework, what a graph runtime actually buys, and approval gates that halt what matters."),
    ("block5-evaluation", "Block 5 · Evaluation",
     "The front door to the measurement material scattered across this course, then labels you can defend and a cross-model comparison that does not lie."),
    ("block6-security", "Block 6 · Security",
     "Block 0 named the attack classes; this block runs them against the agent you built, starting with the injection your own retrieval pipeline invites."),
    ("block7-training", "Block 7 · Training and Fine-Tuning",
     "When changing the weights is the right answer — rarely — and the four ways to shrink a model, including the fact that compression does not remove capability evenly."),
    ("block8-deployment", "Block 8 · Deployment and Interfaces",
     "Calling an interface you do not control, serving one, failing over when the provider does not answer, and the design walk-through that ties the course to the questions interviewers ask."),
    ("block9-electives", "Block 9 · Electives",
     "Directions the spine does not cover: input that is not text, asking the database properly, where the money goes, convolutions, recommenders, and agents that improve themselves."),
    ("closing-future-of-work", "Closing · The Future of Work",
     "The only chapter that argues rather than instructs — what the 2026 labour evidence shows, and a thesis about which capability becomes scarce, with its counter-argument attached."),
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


GH = "https://github.com/stylusnexus/deep-dive-ai-ml/blob/main/"

TITLE = "Building and Measuring LLM Systems | Free applied AI course"
DESC = ("Free, runnable applied AI course on evaluation, retrieval, agents, security and "
        "fine-tuning for large language models, with notebooks that ship their outputs.")
assert len(TITLE) <= 60 and 140 <= len(DESC) <= 158, (len(TITLE), len(DESC))

# Expanded on first use on this page. Names with no settled expansion (GGUF, GPTQ, DWQ,
# NN, NVIDIA, PyTorch, SWE-bench) are left alone rather than guessed.
ACRONYMS = {
    "AI": "artificial intelligence", "ML": "machine learning", "GenAI": "generative AI",
    "LLM": "large language model", "KV": "key-value", "MCP": "Model Context Protocol",
    "RLHF": "reinforcement learning from human feedback", "DPO": "direct preference optimization",
    "JSON": "JavaScript Object Notation", "CUDA": "Compute Unified Device Architecture",
    "CPU": "central processing unit", "GPU": "graphics processing unit",
    "MLP": "multilayer perceptron", "HNSW": "hierarchical navigable small world",
    "IVF": "inverted file index", "EDA": "exploratory data analysis",
    "MCAR": "missing completely at random", "MAR": "missing at random",
    "MNAR": "missing not at random", "AUC": "area under the curve",
    "RAG": "retrieval-augmented generation", "LoRA": "low-rank adaptation",
    "QLoRA": "quantized low-rank adaptation", "API": "application programming interface",
    "CNN": "convolutional neural network", "ADR": "architecture decision record",
    "PR": "pull request", "SOP": "standard operating procedure",
    "AWQ": "activation-aware weight quantization",
}
_ACR_RE = re.compile(r"\b(" + "|".join(sorted(ACRONYMS, key=len, reverse=True)) + r")(s?)\b")


def expand_first_use(fragment, seen):
    """Spell out each acronym the first time it appears in visible text.

    Works on text between tags only, so attributes and markup are untouched. `seen`
    carries across fragments in document order and is pre-filled with whatever the
    hand-written parts of the page already spell out.
    """
    def sub(m, at_start, text):
        key, plural = m.group(1), m.group(2)
        if key in seen:
            return m.group(0)
        if text[:m.start()].endswith("(") and text[m.end():].startswith(")"):
            seen.add(key)          # the lesson title already spells it out
            return m.group(0)
        seen.add(key)
        phrase = ACRONYMS[key] + plural
        if at_start:
            phrase = phrase[0].upper() + phrase[1:]
        return f"{phrase} ({key}{plural})"

    out = []
    for part in re.split(r"(<[^>]+>)", fragment):
        if part.startswith("<"):
            out.append(part)
            continue
        pieces, pos = [], 0
        for m in _ACR_RE.finditer(part):
            pieces.append(part[pos:m.start()])
            pieces.append(sub(m, m.start() == 0, part))
            pos = m.end()
        pieces.append(part[pos:])
        out.append("".join(pieces))
    return "".join(out)


def lesson_href(topic, slug):
    meta = json.loads((ROOT / "lessons" / topic / "meta.json").read_text())
    for l in meta["lessons"]:
        if l["file"].split("-", 2)[2].rsplit(".", 1)[0] == slug:
            return f'lessons/{topic}/{l["file"]}'
    raise KeyError(slug)


SUBTITLES = {slug: info["subtitle"] for slug, info in slug_map().items()}


def section(topic, heading, note, alt):
    meta = json.loads((ROOT / "lessons" / topic / "meta.json").read_text())
    rows = []
    for l in meta["lessons"]:
        slug = l["file"].split("-", 2)[2].rsplit(".", 1)[0]
        rows.append(
            f'    <li><a href="lessons/{topic}/{l["file"]}">{E(l["title"])}</a>\n'
            f'      <p>{E(BLURBS.get(slug) or plain(SUBTITLES.get(slug, ""), 200))}</p></li>')
    sid = E(topic)
    return (f'<section class="set{" alt" if alt else ""}" id="set-{sid}" aria-labelledby="h-{sid}">\n'
            f'  <div class="wrap">\n'
            f'  <h3 id="h-{sid}">{E(heading.replace(" · ", ": "))}</h3>\n'
            f'  <p class="note">{note}</p>\n'
            f'  <ol>\n{chr(10).join(rows)}\n  </ol>\n  </div>\n</section>'), len(meta["lessons"])


# --- figures computed from the repo, never typed -----------------------------------
first_file = json.loads((ROOT / "lessons" / "orientation" / "meta.json").read_text())["lessons"][0]["file"]
START = f"lessons/orientation/{first_file}"
sec_html, total = [], 0
for i, (topic, heading, note) in enumerate(SECTIONS):
    h, n = section(topic, heading, note, i % 2 == 1)
    sec_html.append(h)
    total += n
blocks = len({m.group(1) for _, h, _ in SECTIONS if (m := re.match(r"Block (\d+)", h))})
notebooks = len(list((ROOT / "notebooks").rglob("*.ipynb")))
projects = len([d for d in (ROOT / "projects").iterdir() if re.match(r"p\d+-", d.name)])

# --- claims: each links to the lesson that settles it ------------------------------
CLAIMS = [
    ("99% accuracy", "Can mean a model that learned nothing.",
     lesson_href("core-vocabulary", "class-imbalance-and-thresholds")),
    ("22 sentinels", "Twenty-two sentinel values can shift a mean fourfold.",
     lesson_href("block1-data-eda", "tabular-data-and-dtypes")),
    ("Random splits", "Lie on ordered data. Walk-forward validation does not.",
     lesson_href("block2-classical-ml", "time-series")),
    ("Self-critique", "Often makes things worse unless a verifier checks it.",
     lesson_href("core-vocabulary", "loops-at-inference")),
    ("29 questions", "The gold set the capstone run is graded against.",
     "docs/p4-deployed-assistant.html#capstone"),
]
claims_html = "\n".join(
    f'    <li class="claim" data-rise style="--d:{i * 70}ms"><a href="{h}">{E(t)}</a><p>{E(d)}</p></li>'
    for i, (t, d, h) in enumerate(CLAIMS))

PROGRAM = [
    ("Curriculum", "All ten blocks, week by week, each with an exit criterion that runs rather than a box that ticks.", "docs/curriculum.html"),
    ("Project intake sheet", "Ten questions to answer before writing code. Filled in before every project, reviewed after.", "docs/project-intake.html"),
    ("Selection scorecard", "For choosing a model, a vendor, or a framework — three decisions with three different failure modes.", "docs/selection-scorecard.html"),
    ("Worksheets and references", "The intake sheets, scorecard, exam and rubric as pages you can fill in, then download or print.", "docs/"),
    ("Capstone run", "Project 4's graded run: its tests, a provider-failure drill, a 29-question gold set and the memory arithmetic, in one report.", "docs/p4-deployed-assistant.html#capstone"),
    ("Cumulative exam", "Ten scenarios across Blocks 3 to 8, each needing two or more lessons, with a marking key.", "docs/cumulative-exam.html"),
    ("Design interview rubric", "A scored 45-minute mock interview on the nine system-design questions AI roles keep asking.", "docs/design-interview-rubric.html"),
    ("Things to Know", "Every compressed, load-bearing line in the course, collected and linked back to the lesson that earns it.", "things-to-know.html"),
    ("SOP checklists", "Aviation-style: killer items marked, hard gates, and a separate non-normal checklist for when something is already wrong.", "artifacts/sop/index.html"),
    ("Glossary", "Every term the program defines, accumulating block by block and feeding spaced repetition.", "docs/glossary.html"),
]
program_html = "\n".join(
    f'    <li><a href="{h}">{E(t)}</a>\n      <p>{E(d)}</p></li>' for t, d, h in PROGRAM)

ELSEWHERE = [
    ("Statistical Learning", "Nineteen lessons — probability, distributions, the CLT, hypothesis tests, Bayesian inference, regression, information theory, evaluation metrics and LLM statistics.", "https://github.com/stylusnexus/statistics-for-ai"),
    ("Math for AI", "Seven lessons — vectors, matrices, SVD, derivatives, gradients, backpropagation and integrals.", "https://stylusnexus.github.io/statistics-for-ai/math.html"),
    ("Responsible AI &amp; Governance", "Twelve lessons — the EU AI Act, NIST AI RMF, ISO 42001, and the governance lifecycle.", "https://github.com/stylusnexus/aigp-exam-prep"),
]
elsewhere_html = "\n".join(
    f'    <li><a href="{h}">{t}</a><p>{E(d) if "&amp;" not in d else d}</p></li>' for t, d, h in ELSEWHERE)

# the map, drawn: nested fills, no outlines
NEST = """<svg viewBox="0 0 700 420" role="img" aria-label="Nested shapes: artificial intelligence contains machine learning, which contains deep learning, which contains generative AI and large language models. Agents sit beside them.">
<rect x="0" y="0" width="470" height="420" fill="var(--n1)"/>
<text x="22" y="44" class="nest-t">Artificial intelligence (AI)</text>
<rect x="20" y="64" width="430" height="340" fill="var(--n2)"/>
<text x="42" y="108" class="nest-t">Machine learning (ML)</text>
<rect x="40" y="128" width="390" height="260" fill="var(--n3)"/>
<text x="62" y="172" class="nest-t">Deep learning</text>
<rect x="60" y="192" width="350" height="180" fill="var(--lime)"/>
<text x="82" y="236" class="nest-l">Generative AI</text>
<text x="82" y="272" class="nest-ls">Large language models</text>
<text x="82" y="302" class="nest-ls">(LLMs)</text>
<rect x="490" y="192" width="190" height="180" fill="var(--agent)"/>
<text x="508" y="236" class="nest-a">Agents</text>
<text x="508" y="272" class="nest-as">a loop</text>
<text x="508" y="302" class="nest-as">around a model</text>
</svg>"""

# Acronyms the hand-written parts of the page already spell out.
seen = {"AI", "LLM", "ML", "RAG"}
lessons_body = expand_first_use("\n".join(sec_html), seen)
program_body = expand_first_use(program_html, seen)
elsewhere_body = expand_first_use(elsewhere_html, seen)

wordmark = "Stylus Nexus"
title_lines = ("Building and Measuring", "LLM Systems")
hero_title = (f'<h1 class="hero-title"><span class="ln"><span>{title_lines[0]}</span></span>'
              f'<span class="ln"><span>{title_lines[1]}</span></span></h1>')

doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{E(TITLE)}</title>
{head_meta(TITLE, DESC, "", course_jsonld(DESC), og_type="website")}
<meta name="color-scheme" content="dark light">
<script>document.documentElement.classList.add('js')</script>
{STYLE}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<header class="bar">
  <a class="mark" href="./">{wordmark}</a>
  <nav aria-label="Primary">
    <ul>
      <li><a href="#lessons">Lessons</a></li>
      <li><a href="#program">Program</a></li>
      <li><a href="#elsewhere">Other courses</a></li>
    </ul>
  </nav>
</header>

<main id="main">

<section class="hero" aria-label="Introduction">
  <div class="up"></div>
  {hero_title}
  <div class="down">
    <div class="hero-copy">
      <p>Applied artificial intelligence (AI) with large language models (LLMs): evaluation, retrieval, agents, security and fine-tuning. Free, and every notebook ships with its outputs.</p>
      <a class="btn" href="{START}">Start with the map</a>
      <small>Ten minutes, and the rest makes more sense.</small>
    </div>
  </div>
</section>

<section class="claims" aria-labelledby="claims-h">
  <div class="wrap">
    <div class="head" data-rise>
      <h2 class="h2" id="claims-h">Claims, and the runs that settle them</h2>
      <p>Five results the lessons are built around. Each one links to the lesson that earns it.</p>
    </div>
    <ol>
{claims_html}
    </ol>
  </div>
</section>

<section class="about" aria-labelledby="about-h">
  <div class="wrap">
    <h2 class="h2" id="about-h" data-rise>A course that shows its work</h2>
    <p class="note" data-rise style="--d:100ms">Notebooks ship with their executed outputs, because a notebook that has not been run is a hypothesis. Every external link is checked before it is committed. Numbers in lessons come from runs, not from memory.</p>
    <ul class="facts">
      <li data-rise><strong>{total}</strong><span>lessons in {len(SECTIONS)} sets, each readable on its own</span></li>
      <li data-rise style="--d:70ms"><strong>{blocks}</strong><span>blocks, from vocabulary to deployment</span></li>
      <li data-rise style="--d:140ms"><strong>{notebooks}</strong><span>notebooks, saved with their outputs</span></li>
      <li data-rise style="--d:210ms"><strong>{projects}</strong><span>portfolio projects, each a script you can run</span></li>
    </ul>
    <figure class="figure" data-rise>
      {NEST}
      <figcaption>The first lesson draws this: how the terms nest, and where the rest of the course sits on it.</figcaption>
    </figure>
    <div class="start" data-rise>
      <p>Read the map before anything else. Every term in the program has a place on that one picture.</p>
      <a class="btn" href="{START}">Open the map</a>
    </div>
  </div>
</section>

<div id="lessons">
<section class="lessons-intro" aria-labelledby="lessons-h">
  <div class="wrap">
    <h2 class="h2" id="lessons-h" data-rise>All {total} lessons, in course order</h2>
    <p data-rise>{len(SECTIONS)} sets. Lessons are read standalone, so every term is explained where it first appears.</p>
  </div>
</section>
{lessons_body}
</div>

<section class="program paper" id="program" aria-labelledby="program-h">
  <div class="wrap">
    <h2 class="h2" id="program-h">The program</h2>
    <p class="lead">The checklists, exams and records that surround the lessons.</p>
    <ul class="rows">
{program_body}
    </ul>
  </div>
</section>

<section class="elsewhere" id="elsewhere" aria-labelledby="elsewhere-h">
  <div class="wrap">
    <h2 class="h2" id="elsewhere-h">Already complete elsewhere</h2>
    <ul>
{elsewhere_body}
    </ul>
  </div>
</section>

<section class="cta" aria-labelledby="cta-h">
  <h2 id="cta-h">Now run it yourself.</h2>
  <div class="foot">
    <p>Open the first lesson, then the notebook that goes with it. The environments are in Docker, so your run matches ours.</p>
    <a class="btn" href="{START}">Start with the map</a>
  </div>
</section>

</main>

<footer>
  <nav aria-label="Project">
    <ul class="places">
      <li><a href="https://github.com/stylusnexus/deep-dive-ai-ml">Source on GitHub</a></li>
      <li><a href="docs/curriculum.html">Curriculum</a></li>
      <li><a href="docs/glossary.html">Glossary</a></li>
      <li><a href="docs/">Worksheets</a></li>
      <li><a href="things-to-know.html">Things to Know</a></li>
    </ul>
  </nav>
  <p class="name" aria-hidden="true">{wordmark}</p>
  <p class="legal">Published by Stylus Nexus. Building and Measuring LLM Systems.</p>
</footer>

<script>
(function () {{
  var d = document.documentElement;
  if (!('IntersectionObserver' in window)) {{ d.classList.remove('js'); return; }}
  var io = new IntersectionObserver(function (es) {{
    es.forEach(function (e) {{ if (e.isIntersecting) {{ e.target.classList.add('in'); io.unobserve(e.target); }} }});
  }}, {{ rootMargin: '0px 0px -6% 0px' }});
  document.querySelectorAll('[data-rise]').forEach(function (el) {{ io.observe(el); }});
}})();
</script>
</body>
</html>
"""
(ROOT / "index.html").write_text(doc)
print(f"built index.html — {total} lessons across {len(sec_html)} sets")
