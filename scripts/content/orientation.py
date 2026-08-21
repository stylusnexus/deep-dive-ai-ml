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
{
  "slug": "inside-an-llm",
  "title": "Inside an LLM: The Parts and What Each Does",
  "subtitle": "Follow one sentence all the way through — from text, to numbers, to the next word.",
  "body": [
    ("p", "You can use these models productively without knowing what's inside them. But almost every practical question — why context costs what it does, why a fine-tune changes behaviour, what quantization actually shrinks, why the tokenizer matters — has an answer that lives in the architecture. This lesson walks one sentence through the whole machine."),

    ("figure", "Text becomes numbers, numbers pass through a stack of identical blocks, and the last position gets turned back into a probability over every word the model knows. Everything else is detail.", '''<svg viewBox="0 0 640 420" role="img" aria-label="The full path of text through a large language model"><defs><marker id="la" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" class="d-fill-accent"/></marker></defs>
<rect x="180" y="10" width="280" height="34" rx="6" class="d-box"/>
<text x="196" y="32" class="d-label-sm">"The turbine is"</text>
<text x="470" y="32" class="d-label-sm">your text</text>
<path d="M320 44 L320 62" class="d-arrow-accent" marker-end="url(#la)"/>
<rect x="180" y="62" width="280" height="38" rx="6" class="d-box-accent"/>
<text x="196" y="80" class="d-label-b">1 · Tokenizer</text>
<text x="196" y="94" class="d-label-sm">[791, 66029, 374] — text becomes integers</text>
<path d="M320 100 L320 118" class="d-arrow-accent" marker-end="url(#la)"/>
<rect x="180" y="118" width="280" height="38" rx="6" class="d-box-accent"/>
<text x="196" y="136" class="d-label-b">2 · Embedding + position</text>
<text x="196" y="150" class="d-label-sm">each id becomes a vector; order is added</text>
<path d="M320 156 L320 174" class="d-arrow-accent" marker-end="url(#la)"/>
<rect x="120" y="174" width="400" height="146" rx="8" fill="none" stroke="var(--accent2)" stroke-width="2" stroke-dasharray="5 4"/>
<text x="136" y="194" style="fill:var(--accent2);font-size:12px;font-weight:600;font-family:-apple-system,sans-serif">3 · Transformer blocks — repeated 30 to 100+ times</text>
<rect x="150" y="204" width="160" height="46" rx="6" class="d-box"/>
<text x="164" y="222" class="d-label-b">Attention</text>
<text x="164" y="238" class="d-label-sm">tokens look at each other</text>
<rect x="330" y="204" width="160" height="46" rx="6" class="d-box"/>
<text x="344" y="222" class="d-label-b">Feed-forward</text>
<text x="344" y="238" class="d-label-sm">each token thinks alone</text>
<path d="M310 227 L330 227" class="d-arrow-accent" marker-end="url(#la)"/>
<rect x="150" y="262" width="340" height="44" rx="6" class="d-box"/>
<text x="164" y="280" class="d-label-sm">+ residual connections (keep the original signal)</text>
<text x="164" y="296" class="d-label-sm">+ layer normalisation (keep the numbers stable)</text>
<path d="M320 320 L320 338" class="d-arrow-accent" marker-end="url(#la)"/>
<rect x="180" y="338" width="280" height="38" rx="6" class="d-box-accent"/>
<text x="196" y="356" class="d-label-b">4 · Output head</text>
<text x="196" y="370" class="d-label-sm">last position → score for every known token</text>
<path d="M320 376 L320 392" class="d-arrow-accent" marker-end="url(#la)"/>
<rect x="180" y="392" width="280" height="26" rx="6" class="d-box-good"/>
<text x="196" y="410" class="d-label-sm">5 · Sample → " spinning"</text>
</svg>'''),

    ("h2", "1 · The tokenizer"),
    ("p", "Before any maths, text is split into tokens and each is looked up as an integer. The tokenizer is a fixed vocabulary — typically 32,000 to 200,000 entries — built once before training and never changed afterwards."),
    ("p", "It explains several things that otherwise look arbitrary: why models are bad at counting letters in a word (they never see letters), why unusual names cost more tokens than common ones, and why non-English text is often more expensive — the vocabulary was fitted mostly to English, so other languages fragment into more pieces."),

    ("h2", "2 · Embeddings and position"),
    ("p", "Each token id is looked up in an <strong>embedding matrix</strong> and becomes a vector of a few thousand numbers. This is the same idea as the embeddings used for retrieval, learned here as part of the model."),
    ("p", "Because attention compares all positions equally and has no inherent sense of order, position must be added explicitly — in most current models through <strong>rotary position embeddings</strong>. This is also why extending a model's context beyond what it was trained on is largely a positional-encoding problem rather than a memory one."),

    ("h2", "3 · The transformer blocks"),
    ("p", "The bulk of the model: the same block repeated dozens of times, each containing two operations that alternate."),
    ("terms", [
      ("Attention", "Tokens exchange information", "Each token gathers from every other, weighted by relevance. The mechanism the algorithms lesson covers in detail."),
      ("Feed-forward network", "Each token processes alone", "A small network applied to every position independently. Typically two-thirds of all parameters — most of the model's stored knowledge lives here, not in attention."),
      ("Residual connections", "Add the input back to the output", "Lets signal and gradients pass through 80 layers without degrading. Without these, deep networks don't train."),
      ("Layer normalisation", "Rescale the numbers", "Keeps values in a workable range so training stays stable."),
    ]),
    ("callout", "insight", "Where the knowledge actually sits", "It's tempting to think of attention as the clever part and the feed-forward layers as plumbing. It's closer to the reverse. Attention decides which information to route where; the feed-forward layers hold most of the learned facts, and they're where most of the parameters are. When you hear a model 'knows' something, it is largely these layers."),

    ("h2", "4 · The output head"),
    ("p", "After the final block, the vector at the last position is multiplied by an unembedding matrix to produce one score — a <strong>logit</strong> — for every token in the vocabulary. Softmax turns those scores into probabilities summing to one."),
    ("p", "Note what is thrown away: the model computed a rich representation at <em>every</em> position, and generation uses only the last. The others aren't wasted — they're cached, which is exactly what the KV cache holds."),

    ("h2", "5 · Sampling"),
    ("p", "A probability distribution over the vocabulary isn't yet a word. Temperature, top-k and top-p reshape that distribution and one token is drawn. Then the whole process runs again with that token appended — one full pass through the entire model per token generated."),

    ("h2", "The parts as files on disk"),
    ("p", "Download an open model and you get the same components, made concrete:"),
    ("terms", [
      ("config.json", "The architecture", "Layer count, hidden size, attention heads, vocabulary size, context length. The blueprint."),
      ("tokenizer.json", "The vocabulary", "Must match the weights exactly. Mismatch it and you get fluent nonsense — a classic and baffling bug."),
      ("*.safetensors", "The weights", "The actual learned numbers, at full precision. What fine-tuning modifies."),
      ("*.gguf", "Weights, quantized and packaged", "Config, tokenizer and quantized weights in one self-contained file for local serving."),
      ("chat template", "Turn structure", "How system, user and assistant turns are formatted into one string. Get this wrong and quality drops for no visible reason."),
    ]),
    ("callout", "matters", "What each technique actually touches", "Prompting changes the input only. Fine-tuning adjusts the weights — usually the feed-forward layers most. LoRA freezes the original weights and trains small add-on matrices alongside them. Quantization stores the same weights in fewer bits. RAG changes nothing about the model at all; it changes what's in the context. Knowing which layer of the machine each one touches tells you which problem each can and cannot solve."),

    ("h2", "The size numbers, made concrete"),
    ("p", "A 7-billion-parameter model has roughly 32 blocks, a hidden size around 4096, 32 attention heads, and a vocabulary near 32,000. At 16-bit precision the weights alone are about 14GB — most of it in the feed-forward layers. Every one of those parameters is touched for every token generated, which is why local inference is memory-bandwidth bound and why quantization speeds things up as well as shrinking them."),

    ("links", [
      ("The Illustrated Transformer", "https://jalammar.github.io/illustrated-transformer/",
       "The visual walkthrough of the same pipeline, one component at a time."),
      ("Build a Large Language Model (From Scratch)", "https://github.com/rasbt/LLMs-from-scratch",
       "You have this locally. Chapters 2–4 build the tokenizer, the attention block and the full model in PyTorch."),
      ("Hugging Face model file formats", "https://huggingface.co/docs/hub/gguf",
       "What each file in a model repository is for, and how GGUF packages them."),
    ]),

    ("quiz", [
      ("Why is a model bad at counting the letters in a word?",
       ["The task requires arithmetic it can't do",
        "It never sees letters — text is split into tokens before any processing",
        "Letters are stripped during normalisation"], 1),
      ("Where do most of a model's parameters — and most of its learned facts — sit?",
       ["In the attention layers",
        "In the feed-forward networks inside each block",
        "In the embedding matrix"], 1),
      ("You load a model with the wrong tokenizer. What happens?",
       ["It refuses to load",
        "It produces fluent nonsense — the ids no longer map to the text the weights were trained on",
        "It runs correctly but slower"], 1),
      ("Which part of the machine does RAG change?",
       ["The weights, by adding retrieved knowledge",
        "None of it — RAG changes what's in the context window, not the model",
        "The tokenizer, to handle the retrieved documents"], 1),
    ]),
  ],
},
]
