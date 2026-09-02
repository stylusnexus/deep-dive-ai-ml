TITLE = "Block 7 · Training and Fine-Tuning"
TOPIC = "block7-training"
ICON = "🔧"
DESCRIPTION = "When changing the weights is the right answer, which is rarely — then the four ways to make a model smaller, what each one costs, and the fact that compression does not remove capability evenly."
TAGS = ["ai", "training", "fine-tuning"]
COLOR = "violet"
CREATED = "2026-09-02"
ID_BASE = "1788000000"

LESSONS = [
{
  "slug": "when-fine-tuning-is-wrong",
  "title": "When Fine-Tuning Is the Wrong Answer",
  "subtitle": "Which is most of the time, and the order to exhaust before you reach for it.",
  "body": [
    ("p", "Fine-tuning is the intervention people reach for first and should reach for last. It is the only one that changes the model, which makes it the only one that cannot be undone by editing a file, the only one that has to be redone when the base model improves, and the only one whose failures are invisible until evaluation. This lesson is the order to work through before you get there."),

    ("h2", "The ladder"),
    ("terms", [
      ("Prompting", "Costs tokens, changes nothing permanent",
       "Reversible in a text editor, and it improves when the model does. Exhaust it properly — few-shot examples, output constraints, an explicit format — before concluding the model cannot do the task."),
      ("Retrieval", "Gives the model facts it never had",
       "If the failure is that the model does not <em>know</em> something, no amount of fine-tuning on your task format will fix it, and retrieval will. Confusing these two is the commonest expensive mistake in this area."),
      ("Fine-tuning", "Teaches form, not facts",
       "Changes how the model responds — tone, structure, adherence to a schema, a domain's conventions. It is poor at installing knowledge and good at installing behaviour, and the distinction decides whether it is the right tool."),
      ("Structural change", "Pruning, distillation, quantization",
       "A different axis entirely: not what the model does but how much of it there is. Covered in the next lesson, and usually driven by a serving constraint rather than a quality one."),
    ]),

    ("know",
     "Fine-tuning teaches form. Retrieval supplies facts. Most projects that reach for the first needed the second.",
     "A model that answers in the wrong register, ignores your schema or misses your domain's conventions has a form problem and fine-tuning addresses it directly. A model that does not know your product names, your policies or last quarter's numbers has a knowledge problem, and training on documents containing them is an expensive and unreliable way to install facts that a retrieval index would hold exactly and update in seconds.",
     "The tell is what a wrong answer looks like. If it is confidently wrong about a fact, you have a retrieval problem. If it is right but formatted, toned or structured wrongly, you have a fine-tuning problem — and only the second one is worth a training run."),

    ("figure", "Work down the ladder and stop at the first rung that holds. Each step costs more, reverses less easily, and has to be redone when the base model changes.", '''<svg viewBox="0 0 640 214" role="img" aria-label="The intervention ladder from prompting to structural change"><defs><marker id="ft" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" class="d-fill-accent"/></marker></defs>
<rect x="14" y="16" width="410" height="36" rx="6" class="d-box"/><text x="26" y="39" class="d-label-sm">prompting — reversible in an editor, improves when the model does</text>
<rect x="14" y="60" width="440" height="36" rx="6" class="d-box"/><text x="26" y="83" class="d-label-sm">retrieval — supplies facts, updates in seconds</text>
<rect x="14" y="104" width="500" height="36" rx="6" class="d-box-accent"/><text x="26" y="127" class="d-label-sm">fine-tuning — teaches form, must be redone on every base upgrade</text>
<rect x="14" y="148" width="560" height="36" rx="6" class="d-box-accent"/><text x="26" y="171" class="d-label-sm">structural change — a serving constraint, not a quality one</text>
<path d="M596 24 L596 180" class="d-arrow-accent" marker-end="url(#ft)"/>
<text x="470" y="206" class="d-label-sm">cost and irreversibility increase downward</text>
</svg>'''),

    ("callout", "pitfall", "Every base-model upgrade repeats the work",
     "<p>A fine-tuned model is a fork. The moment a better base appears, your adapter was trained against the old one and the choice is to retrain or to stay behind. Over a year of frequent releases that is a recurring cost nobody budgets at the point of deciding, and it is the strongest practical argument for exhausting the reversible options first.</p>"),

    ("quiz", [
      ("A model answers confidently and wrongly about your product's return policy. What is the right intervention?",
       ["Fine-tune on your policy documents so the model learns them",
        "Retrieval — this is a knowledge problem, and training is an expensive and unreliable way to install facts an index would hold exactly",
        "A longer system prompt describing the policy"],
       1),
      ("Why is fine-tuning described as less reversible than prompting?",
       ["The training data cannot be deleted afterwards",
        "It produces a fork of the model that must be retrained whenever the base improves, where a prompt change is an edit to a file",
        "Adapters cannot be removed once merged"],
       1),
    ]),
  ],
},
{
  "slug": "the-four-ways-to-shrink-a-model",
  "title": "The Four Ways to Shrink a Model",
  "subtitle": "Quantization, pruning, distillation and factorisation — what each removes, and which of them compose.",
  "body": [
    ("p", "Block 0 taught quantization and distillation separately, in the places they came up. They are two members of a family of four, and seeing the family is what tells you which to reach for, because they remove different things and only some of them combine."),

    ("terms", [
      ("Quantization", "Fewer bits per number",
       "The same architecture, the same parameter count, stored less precisely. Cheapest by a wide margin, needs no training, and is reversible in the sense that the original weights still exist. Usually the first and often the only thing needed."),
      ("Pruning", "Fewer parts",
       "Remove structure from the trained network. Depth pruning takes whole layers; width pruning takes neurons and attention heads within layers. Unlike quantization this changes the architecture, and the model is worse immediately afterwards."),
      ("Distillation", "A smaller model taught to imitate",
       "Train a student to reproduce a teacher's behaviour. The one that produces a genuinely different model rather than a modified one, and the most expensive of the four."),
      ("Low-rank factorisation", "The same layer, expressed with fewer numbers",
       "A large weight matrix approximated as the product of two smaller ones. Least used of the four at inference time and conceptually the most familiar, because it is what LoRA already does — an adapter is a low-rank pair standing in for a full-rank update."),
    ]),

    ("h2", "Pruning and distillation are the pair that compose"),
    ("p", "The other three are alternatives; these two are a sequence. Pruning removes structure and the model loses capability with it — the cut is blunt, and what falls out is whatever those layers or heads were contributing. Distillation is then used to <em>repair</em>, training the pruned model against the original as teacher so it recovers behaviour it just lost. Cut, then heal. This is the one place in the family where two techniques are used together rather than chosen between, and it is why a pruning pipeline is more work than the word suggests."),

    ("figure", "Three of the four are alternatives chosen by constraint. Pruning and distillation are a sequence — the second exists to repair what the first removed.", '''<svg viewBox="0 0 640 214" role="img" aria-label="The four compression techniques and how they relate"><defs><marker id="cmp" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" class="d-fill-accent"/></marker></defs>
<text x="14" y="20" class="d-label-b">removes precision</text>
<rect x="14" y="28" width="180" height="40" rx="6" class="d-box"/><text x="26" y="53" class="d-label-sm">quantization — no training</text>
<text x="14" y="94" class="d-label-b">removes structure</text>
<rect x="14" y="102" width="180" height="40" rx="6" class="d-box-accent"/><text x="26" y="127" class="d-label-sm">pruning — depth or width</text>
<path d="M194 122 L252 122" class="d-arrow-accent" marker-end="url(#cmp)"/>
<rect x="252" y="102" width="200" height="40" rx="6" class="d-box-accent"/><text x="264" y="127" class="d-label-sm">distillation — as repair</text>
<text x="252" y="164" class="d-label-sm">cut, then heal: the one pair that</text>
<text x="252" y="180" class="d-label-sm">composes rather than competes</text>
<text x="470" y="20" class="d-label-b">removes rank</text>
<rect x="470" y="28" width="156" height="40" rx="6" class="d-box"/><text x="482" y="53" class="d-label-sm">factorisation — LoRA</text>
<text x="14" y="200" class="d-label-sm">Reach for quantization first. It is the only one that costs no training and keeps the architecture.</text>
</svg>'''),

    ("know",
     "Compression does not remove capability evenly, and the loss is not visible in an average.",
     "A pruned or quantized model that scores within a point of the original on a general benchmark has not necessarily kept everything. Capability is not distributed uniformly across a network, so cutting parts of it removes some things and leaves others — and an aggregate score can absorb a large loss in a narrow area without moving. What disappears tends to be what was rare in the first place: less-represented languages, minority dialects, uncommon domains, the long tail generally.",
     "This is why compression is a fairness question and not only an efficiency one. If the capability lost falls disproportionately on the users who were already least well served, an average that barely moved has hidden exactly the harm worth knowing about. Evaluate compressed models on slices, not on a single number."),

    ("callout", "matters", "Slice the evaluation before and after",
     "<p>The measurement discipline from Block 5 applies directly and is usually skipped here. Record the baseline per slice — per language, per domain, per user population you can identify — and compare per slice afterwards. A single aggregate is precisely the instrument that cannot detect uneven loss, and reporting one is how a compressed model ships having quietly become worse for a subset of the people using it.</p>"),

    ("callout", "pitfall", "Quantization is the boring answer and usually the right one",
     "<p>It requires no training run, no dataset, no student model and no repair pass, and on most serving constraints it is sufficient on its own. Pruning and distillation pipelines are more interesting to build and considerably more work to maintain — a variant you now own, re-derived on every base-model upgrade. Reach for them when quantization has been tried and has not met the constraint, rather than because they are the more sophisticated option.</p>"),

    ("h2", "Where each one bites"),
    ("p", "Choose by the constraint you actually have. If the model will not fit in memory, quantization addresses it directly and cheaply. If it fits but generation is too slow, remember from Block 0 that generation is memory-bound — so fewer bytes helps and fewer operations does not, which favours quantization again over anything that only removes arithmetic. If you need a genuinely smaller model for a narrow task, distillation is the honest answer. Pruning sits between: real gains, real cost, and a repair pass attached."),

    ("quiz", [
      ("Which two of the four are used together rather than chosen between?",
       ["Quantization and pruning, since both reduce size",
        "Pruning and distillation — the cut removes capability and the distillation pass trains it back against the original as teacher",
        "Distillation and factorisation, since both produce a new model"],
       1),
      ("Why can a compressed model score within a point of the original and still be materially worse?",
       ["Benchmarks are usually too small to be reliable",
        "Capability is not distributed evenly across a network, so what is lost tends to be what was rare — and an aggregate score absorbs a large loss in a narrow slice without moving",
        "Compression introduces variance that averages out over enough questions"],
       1),
      ("You have a model that fits in memory but generates too slowly. Which technique is least likely to help?",
       ["Quantization, because it reduces the bytes that must be moved per token",
        "One that only reduces arithmetic per token, since generation is memory-bound and the arithmetic was not the constraint",
        "Distillation to a genuinely smaller student"],
       1),
    ]),
  ],
},
]
