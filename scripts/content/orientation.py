TITLE = "Start Here: The Map"
TOPIC = "orientation"
ICON = "🗺️"
DESCRIPTION = "How AI, machine learning, deep learning, generative AI and agents actually nest inside one another — and where every block of this program sits on that map."
TAGS = ["ai", "orientation"]
COLOR = "blue"
CREATED = "2026-08-20"
ID_BASE = "1787200000"

LESSONS = [
{
  "slug": "the-map",
  "title": "The Map: AI, ML, Deep Learning, GenAI and Agents",
  "subtitle": "Read this before anything else. Every term in the program has a place on one picture.",
  "body": [
    ("p", "These five words get used as though they were alternatives to each other. They aren't — they nest. Most confusion in this field comes from treating a category and one of its subsets as if they were rivals, and almost every vendor pitch you will ever read depends on that confusion going unnoticed."),

    ("figure", "Each ring is contained by the one outside it. Generative AI is a kind of deep learning, which is a kind of machine learning, which is a kind of artificial intelligence. Agentic AI sits outside the nesting because it is an architecture, not a model type — it wraps a model in a loop that can act.", '''<svg viewBox="0 0 640 400" role="img" aria-label="Nested relationship of AI, machine learning, deep learning and generative AI">
<rect x="12" y="12" width="450" height="376" rx="14" fill="none" stroke="var(--muted)" stroke-width="2"/>
<text x="28" y="38" class="d-label-b">ARTIFICIAL INTELLIGENCE</text>
<text x="28" y="56" class="d-label-sm">any system doing something we'd call intelligent</text>
<text x="28" y="74" class="d-label-sm">rule engines · search · planning · expert systems</text>

<rect x="40" y="88" width="394" height="288" rx="12" fill="none" stroke="var(--accent)" stroke-width="2"/>
<text x="56" y="112" class="d-accent">MACHINE LEARNING</text>
<text x="56" y="130" class="d-label-sm">learns patterns from data instead of being programmed with rules</text>
<text x="56" y="148" class="d-label-sm">regression · decision trees · random forests · k-means</text>

<rect x="68" y="162" width="338" height="200" rx="10" fill="none" stroke="var(--accent2)" stroke-width="2"/>
<text x="84" y="186" style="fill:var(--accent2);font-size:12px;font-weight:600;font-family:-apple-system,sans-serif">DEEP LEARNING</text>
<text x="84" y="204" class="d-label-sm">many-layered neural networks · learns its own features</text>
<text x="84" y="222" class="d-label-sm">CNNs for images · transformers for sequences</text>

<rect x="96" y="236" width="282" height="112" rx="8" fill="none" stroke="var(--green)" stroke-width="2"/>
<text x="112" y="260" style="fill:var(--green);font-size:12px;font-weight:600;font-family:-apple-system,sans-serif">GENERATIVE AI</text>
<text x="112" y="278" class="d-label-sm">produces new content rather than a label or number</text>

<rect x="124" y="292" width="226" height="44" rx="6" class="d-box-good"/>
<text x="140" y="312" class="d-label-b">LARGE LANGUAGE MODELS</text>
<text x="140" y="328" class="d-label-sm">generative AI over text</text>

<rect x="482" y="120" width="146" height="160" rx="12" class="d-box-warn"/>
<text x="498" y="146" style="fill:var(--red);font-size:12px;font-weight:600;font-family:-apple-system,sans-serif">AGENTIC AI</text>
<text x="498" y="168" class="d-label-sm">not a model type —</text>
<text x="498" y="184" class="d-label-sm">an architecture.</text>
<text x="498" y="208" class="d-label-sm">wraps any model in</text>
<text x="498" y="224" class="d-label-sm">a loop with tools,</text>
<text x="498" y="240" class="d-label-sm">so it can act rather</text>
<text x="498" y="256" class="d-label-sm">than only answer.</text>
<path d="M478 200 L360 250" class="d-arrow"/>
</svg>'''),

    ("h2", "Reading the rings from the outside in"),
    ("terms", [
      ("Artificial intelligence", "The whole field", "Any system doing something that looks intelligent. A chess engine from 1997 and a thermostat's scheduling logic both qualify. Broad enough that on its own the word carries very little information."),
      ("Machine learning", "Learns from data", "Rather than being given rules, it is given examples and infers the rules. Everything in Block 2 lives here — and it does not require a neural network."),
      ("Deep learning", "Neural networks, many layers", "Learns its own features rather than being handed them. Needs more data and more compute, and wins decisively on images, audio and language."),
      ("Generative AI", "Produces content", "Outputs text, images or audio instead of a label or a number. A spam classifier is ML but not generative; an image generator is both."),
      ("Agentic AI", "An architecture, not a model", "Sits outside the nesting deliberately. It is a loop that lets a model choose actions and use tools — you could build one around a small classical model, though in practice it's built around an LLM."),
    ]),

    ("h2", "The distinction that actually matters day to day"),
    ("p", "<strong>Predictive versus generative.</strong> A predictive model answers a closed question — which category, what number, how likely. Its output can be checked against a known right answer, which makes evaluation straightforward and the statistics well-established."),
    ("p", "A generative model produces open-ended content. There is usually no single right answer, which is why evaluating generative systems is a research problem rather than a formula, and why this program gives evaluation its own week."),
    ("callout", "insight", "Why the older material still matters", "It is tempting to skip Block 2's regression and decision trees to get to the LLM material. Don't. Overfitting, train/test splits, leakage, precision and recall, the bias–variance trade — these were all discovered in the predictive world and they apply unchanged to everything after it. Benchmark contamination is a test-set leak. Reward hacking is overfitting. The vocabulary transfers wholesale."),

    ("h2", "Where each block of this program sits"),

    ("figure", "The program runs roughly outside-in and then upward: foundations first, then the generative layer, then the architecture that puts a model in charge of actions, then everything needed to run it in production.", '''<svg viewBox="0 0 640 260" role="img" aria-label="Program blocks mapped onto the field"><defs><marker id="ma" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" class="d-fill-accent"/></marker></defs>
<rect x="12" y="16" width="180" height="52" rx="7" class="d-box-accent"/>
<text x="26" y="38" class="d-label-b">Blocks 1–2</text>
<text x="26" y="56" class="d-label-sm">ML · data, models, metrics</text>
<path d="M192 42 L226 42" class="d-arrow-accent" marker-end="url(#ma)"/>
<rect x="226" y="16" width="180" height="52" rx="7" class="d-box-accent"/>
<text x="240" y="38" class="d-label-b">Block 3</text>
<text x="240" y="56" class="d-label-sm">GenAI · LLMs and RAG</text>
<path d="M406 42 L440 42" class="d-arrow-accent" marker-end="url(#ma)"/>
<rect x="440" y="16" width="188" height="52" rx="7" class="d-box-warn"/>
<text x="454" y="38" class="d-label-b">Block 4</text>
<text x="454" y="56" class="d-label-sm">Agentic · loops and tools</text>
<rect x="12" y="94" width="180" height="52" rx="7" class="d-box"/>
<text x="26" y="116" class="d-label-b">Blocks 5–6</text>
<text x="26" y="134" class="d-label-sm">evaluation · security</text>
<rect x="226" y="94" width="180" height="52" rx="7" class="d-box"/>
<text x="240" y="116" class="d-label-b">Block 7</text>
<text x="240" y="134" class="d-label-sm">training and fine-tuning</text>
<rect x="440" y="94" width="188" height="52" rx="7" class="d-box"/>
<text x="454" y="116" class="d-label-b">Block 8</text>
<text x="454" y="134" class="d-label-sm">deployment and APIs</text>
<rect x="12" y="172" width="616" height="44" rx="7" class="d-box-good"/>
<text x="26" y="192" class="d-label-b">Block 0 · vocabulary and algorithms</text>
<text x="26" y="210" class="d-label-sm">underneath everything — the terms and the algorithms every block above assumes you already have</text>
<text x="12" y="244" class="d-label-sm">Statistical learning and responsible AI are already built, and slot in alongside Blocks 2 and 6.</text>
</svg>'''),

    ("h2", "One honest caveat about the picture"),
    ("p", "Neat diagrams like the one above are simplifications, and this one has a visible seam: reinforcement learning doesn't sit tidily inside any ring — it's a third learning paradigm alongside supervised and unsupervised, and it shows up both in classical ML and in how LLMs are aligned. Treat the rings as a map for orientation rather than a taxonomy to defend."),

    ("links", [
      ("Google ML Crash Course: framing", "https://developers.google.com/machine-learning/intro-to-ml/supervised",
       "The supervised/unsupervised framing that the middle ring rests on."),
      ("Building effective agents", "https://www.anthropic.com/engineering/building-effective-agents",
       "Why the outer box is an architecture rather than a model class — and when you don't need it."),
    ]),

    ("quiz", [
      ("Is every generative AI system also machine learning?",
       ["No — generative AI is a separate field that developed independently",
        "Yes — generative AI sits inside deep learning, which sits inside machine learning",
        "Only when it's built on a transformer"], 1),
      ("Why is agentic AI drawn outside the nested rings rather than inside them?",
       ["Because it's newer than the other categories",
        "Because it's an architecture that wraps a model in a loop with tools, not a type of model",
        "Because agents don't use machine learning"], 1),
      ("A spam classifier that outputs 'spam' or 'not spam' is which of these?",
       ["Machine learning but not generative AI",
        "Generative AI, because it produces an output",
        "Neither — it's a rule-based system"], 0),
      ("Why does the predictive material still matter once you're working with LLMs?",
       ["It doesn't — LLMs made those techniques obsolete",
        "Overfitting, leakage, train/test discipline and evaluation metrics all transfer directly; benchmark contamination is a test-set leak",
        "Because LLMs are built out of decision trees internally"], 1),
    ]),
  ],
},
]
