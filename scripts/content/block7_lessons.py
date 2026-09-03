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
  "slug": "building-the-dataset",
  "title": "Building the Dataset, and How Little You Need",
  "subtitle": "The part that decides whether the training run was worth doing — and it is smaller than people expect.",
  "body": [
    ("p", "Assume the previous lesson went badly for you and fine-tuning really is the answer. The dataset is now the whole project. Everything downstream &mdash; the method, the rank, the hardware, the hours &mdash; is mechanical by comparison, and none of it recovers from examples that disagree with each other."),

    ("h2", "The number is smaller than you think"),
    ("p", "The intuition people bring from classical machine learning is that more rows are better, and it is wrong here. A base model already speaks the language, knows the domain vocabulary and can follow a format; you are not teaching it to write, you are showing it which of the things it can already do you want. Low-rank adaptation on a narrow, consistent task frequently works on several hundred examples, and a few thousand is a large dataset rather than a small one."),
    ("p", "What replaces volume is consistency and coverage. Five hundred examples that all handle the same situation the same way will teach a behaviour. Fifty thousand that disagree with each other will teach the disagreement, and will do it very thoroughly."),

    ("terms", [
      ("Consistency", "The property that actually matters",
       "Two examples handling the same case differently do not average out. They teach the model that both are acceptable, which is exactly what you were fine-tuning to stop."),
      ("Coverage", "Span the cases, not the volume",
       "Better to have twenty examples across ten situations than two hundred across two. The model generalises from the shape of what it saw, and it cannot generalise to a case that has no representative."),
      ("Format fidelity", "Train the way you will serve",
       "The chat template, the system prompt, the field names and the whitespace all have to match what production sends. A model tuned on a slightly different envelope is being asked to generalise across the one difference you controlled and got wrong."),
      ("The held-out split", "Made first, opened last",
       "Split before you look at anything, and do not iterate against it. A split carved out after you have been reading the data has already been contaminated by your own judgement."),
    ]),

    ("know",
     "A dataset teaches the whole distribution it contains, including the parts you did not intend to teach.",
     "The model has no way to know which properties of your examples were the point. If ninety-five per cent of them are one category, you have taught a prior on that category. If every single one is a confident, complete answer, you have taught it that confident and complete is always available &mdash; and quietly removed its willingness to say the thing is not in the document, which is the behaviour the retrieval and structured-output lessons both spent their time protecting.",
     "A team fine-tunes a support classifier on eight hundred resolved tickets. Resolved tickets, by definition, are the ones that had an answer. The tuned model stops routing anything to a human, because in eight hundred examples it never once saw that outcome, and its accuracy on the eval set &mdash; also drawn from resolved tickets &mdash; looks excellent."),

    ("figure", "Where examples come from, and what each source costs you. Production traffic is the only one that carries the real distribution.", '''<svg viewBox="0 0 560 176" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Three dataset sources compared: production logs, hand-written examples, and model-generated data.">
<rect x="10" y="16" width="164" height="52" rx="6" class="d-box-good"/>
<text x="92" y="36" class="d-label-b" text-anchor="middle">production traffic</text>
<text x="92" y="52" class="d-label-sm" text-anchor="middle">the real distribution</text>
<text x="92" y="64" class="d-label-sm" text-anchor="middle">needs labelling</text>
<rect x="188" y="16" width="164" height="52" rx="6" class="d-box"/>
<text x="270" y="36" class="d-label-b" text-anchor="middle">hand-written</text>
<text x="270" y="52" class="d-label-sm" text-anchor="middle">highest quality</text>
<text x="270" y="64" class="d-label-sm" text-anchor="middle">slowest, does not scale</text>
<rect x="366" y="16" width="184" height="52" rx="6" class="d-box-bad"/>
<text x="458" y="36" class="d-label-b" text-anchor="middle">model-generated</text>
<text x="458" y="52" class="d-label-sm" text-anchor="middle">cheap and plentiful</text>
<text x="458" y="64" class="d-label-sm" text-anchor="middle">inherits the generator</text>
<path d="M92 68 L92 104" class="d-arrow"/>
<path d="M270 68 L270 104" class="d-arrow"/>
<path d="M458 68 L458 104" class="d-arrow"/>
<rect x="10" y="108" width="540" height="34" rx="6" class="d-box"/>
<text x="280" y="129" class="d-label" text-anchor="middle">deduplicate, check consistency, split before you look</text>
<text x="10" y="164" class="d-label-sm">a near-duplicate across the split inflates your evaluation and tells you the training worked</text>
</svg>'''),

    ("h2", "Where the examples come from"),
    ("p", "Production traffic is the best source and the most work: it carries the distribution you will actually serve, including the awkward inputs nobody would think to invent, and it arrives unlabelled. Hand-written examples are the highest quality per row and do not scale past a few hundred, which is fine, because a few hundred is often the whole requirement. Generating examples with a larger model is cheap and is where the traps live."),

    ("callout", "pitfall", "Two traps in model-generated data, one legal and one technical",
     "<p>Check the licence on the model whose outputs you are training on. Several providers prohibit using their outputs to train competing models, and a dataset built in breach of that is a dataset you cannot ship, which you would rather learn before the training run than after.</p><p>The technical trap is subtler and is the point of the loops-in-training lesson: a generated dataset inherits the generator&#39;s distribution, including its errors and its blind spots, and it under-represents exactly the rare cases that were the reason you were fine-tuning. Generated data is reasonable for teaching <em>format</em>, which the generator gets right by construction. It is a poor way to teach <em>judgement</em>, which is the thing it may not have.</p>"),

    ("know",
     "Deduplicate across the split, or your evaluation will tell you the training worked.",
     "Near-duplicates are ordinary in real corpora &mdash; the same ticket refiled, the same document in two formats, boilerplate repeated across records. If one copy lands in training and another in the held-out set, the model has seen the answer, and the score you read afterwards is measuring memorisation. This is data leakage from Block 1, arriving in a form the usual split-before-you-fit discipline does not catch, because the split was done correctly and the duplication was already in the data.",
     "A support dataset of twelve hundred tickets contains roughly ninety near-identical password-reset requests. Split at random, the held-out set gets about eighteen of them and the model has trained on the rest. Accuracy comes back four points higher than the model deserves, and every one of those points is a ticket it had already been shown."),

    ("h2", "What good looks like before you start"),
    ("ul", [
      "The evaluation set exists, was split first, and nothing has been tuned against it.",
      "You can state what a wrong answer looks like, and there are examples of the model getting it right in that specific way.",
      "The hard cases and the ones where the correct answer is a refusal are both represented, in something like the proportion you expect to serve.",
      "Two people reading a sample of the data agree on what the label should have been. If they do not, the model will not either.",
      "The format is byte-for-byte what production sends, chat template included.",
    ]),

    ("quiz", [
      ("Why can five hundred consistent examples outperform fifty thousand inconsistent ones?",
       ["Smaller datasets overfit less, which improves generalisation",
        "Contradictory examples teach that both behaviours are acceptable, which is the behaviour fine-tuning was meant to remove — consistency is the signal, volume is not",
        "Large datasets require a higher rank, which costs more memory"],
       1),
      ("Every example in a support dataset is a ticket that was successfully resolved. What has the model been taught?",
       ["Nothing problematic — resolved tickets are the correct behaviour to imitate",
        "That an answer is always available, because it never saw the outcome where the right move was to escalate — and the eval set, drawn from the same pool, cannot detect it",
        "To prefer shorter answers, since resolutions tend to be brief"],
       1),
      ("A near-duplicate record appears in both the training and held-out sets. What does the evaluation measure?",
       ["Generalisation, since the records are not byte-identical",
        "Partly memorisation — the model has effectively seen the held-out answer, so the score is inflated by an amount you cannot see",
        "Nothing is affected as long as the split was random"],
       1),
    ]),
  ],
},
{
  "slug": "lora-qlora-and-full-fine-tuning",
  "title": "LoRA, QLoRA and the Full Fine-Tune",
  "subtitle": "What low-rank adaptation actually changes, what rank buys you, and the one case where updating every weight is still right.",
  "body": [
    ("p", "A full fine-tune updates every parameter in the model. That is expensive for a reason worth stating precisely, because it is the reason the alternative exists: training needs the weights, the gradients and the optimiser state all resident at once, which is several times the memory of the weights alone. It also produces a complete copy of the model per task, so ten tuned variants is ten models to store, serve and re-derive the next time the base improves."),
    ("p", "Low-rank adaptation (LoRA) is the observation that the <em>update</em> does not need to be as expressive as the model. Freeze every original weight, and learn a small pair of matrices alongside them whose product stands in for the change you would have made. Train those instead."),

    ("figure", "The base weights are frozen. A small pair of matrices learns the update, and their product is added at inference.", '''<svg viewBox="0 0 540 168" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A frozen weight matrix with a small low-rank pair added alongside it.">
<rect x="18" y="24" width="112" height="112" rx="6" class="d-box"/>
<text x="74" y="76" class="d-label-b" text-anchor="middle">W</text>
<text x="74" y="94" class="d-label-sm" text-anchor="middle">frozen</text>
<text x="74" y="152" class="d-label-sm" text-anchor="middle">billions of values</text>
<text x="144" y="84" class="d-label-b">+</text>
<rect x="168" y="24" width="34" height="112" rx="5" class="d-box-accent"/>
<text x="185" y="84" class="d-label-sm" text-anchor="middle">B</text>
<text x="212" y="84" class="d-label-b">&#215;</text>
<rect x="228" y="66" width="112" height="30" rx="5" class="d-box-accent"/>
<text x="284" y="86" class="d-label-sm" text-anchor="middle">A</text>
<text x="252" y="152" class="d-label-sm" text-anchor="middle">trained &#8212; megabytes</text>
<path d="M352 80 L392 80" class="d-arrow"/>
<rect x="398" y="52" width="126" height="56" rx="6" class="d-box-good"/>
<text x="461" y="76" class="d-label-b" text-anchor="middle">W + BA</text>
<text x="461" y="94" class="d-label-sm" text-anchor="middle">used at inference</text>
<text x="18" y="14" class="d-label-sm">the narrow dimension shared by B and A is the rank</text>
</svg>'''),

    ("p", "The saving is not mainly in the parameter count, though that is dramatic. It is that a frozen weight has no gradient and no optimiser state, so the memory that dominated the full fine-tune simply is not allocated. Block 0 made this point from the other direction when it explained why training costs so much more than inference; this is that arithmetic run in reverse."),

    ("h2", "Rank, and what it is a dial for"),
    ("terms", [
      ("LoRA rank", "How much the adaptation can express",
       "The shared narrow dimension of the two matrices. A rank of 8 or 16 is a common starting point and is enough for most format-and-tone work; 64 and above is a large adaptation. It is capacity, not quality."),
      ("Alpha", "How loudly the adaptation speaks",
       "A scaling factor applied to the low-rank product before it is added. Conventionally set at one or two times the rank, and worth changing deliberately rather than by folklore."),
      ("Target modules", "Where the adaptation is allowed to act",
       "Which weight matrices get an adapter &mdash; the attention projections by default, sometimes the feed-forward layers too. More targets means more capacity and more to train, and it is a bigger lever than rank on many tasks."),
      ("The adapter", "A few megabytes, not a few gigabytes",
       "What you actually ship. Small enough to version in a repository, swap at serve time, and throw away when the base model improves."),
    ]),

    ("know",
     "Raising the rank does not make a small dataset train better. It makes it overfit faster.",
     "Rank is capacity, and capacity is only useful if there is signal to fill it. On a few hundred examples a high rank gives the model enough freedom to memorise them, which shows up as a training loss that keeps falling while held-out performance stops improving or reverses &mdash; the same overfitting curve from Block 2, with a different knob attached to it. The instinct that a poor result means turn the dial up is exactly backwards here.",
     "A tuning run on six hundred examples at rank 8 reaches its best held-out score at epoch two. The same data at rank 64 reaches a far lower <em>training</em> loss by epoch two, and a held-out score two points worse, because the extra capacity went into reproducing the training set rather than learning the behaviour it exemplified."),

    ("h2", "QLoRA, and the idea behind it"),
    ("p", "Quantized low-rank adaptation (QLoRA) adds one move to the above: quantise the frozen base to four bits and keep the trainable adapters at higher precision. The reasoning is clean &mdash; precision matters most for the weights you are updating, and the base is not being updated at all. What it buys is a size class: models that would not otherwise fit on one machine become trainable on it, which is the difference between renting a cluster and not."),

    ("callout", "matters", "What this makes possible on the hardware in front of you",
     "<p>On a high-memory Apple Silicon machine, adaptation of a seven- to thirteen-billion-parameter model is comfortable and the data never leaves the desk &mdash; which for regulated or confidential material is not a convenience but the entire reason the option exists. Quantising the base extends the reach further up the size ladder. The hardware checklist still applies before any of it: capacity is a hard wall and library support is what actually blocks people, and neither of those is changed by the training method being clever.</p>"),

    ("h2", "Adapters compose, and that changes the economics"),
    ("p", "Because an adapter is a small separate artefact rather than a modified model, one base model can serve many of them, selected per request. That turns per-customer or per-task tuning from an infrastructure problem into a file-loading problem, and it makes a tuned behaviour something you can withdraw by deleting a file rather than by retraining. It also means a base-model upgrade costs you a re-run of the adapters rather than a rebuild of everything downstream &mdash; still work, but bounded work."),

    ("know",
     "An adapter is a diff against a base you do not own, which makes it cheap to keep and cheap to abandon.",
     "This is the practical reason low-rank adaptation displaced full fine-tuning for most work. A full fine-tune is a commitment: a whole model, stored and served and re-derived from scratch on every base upgrade. An adapter is measured in megabytes, swaps at request time, versions in an ordinary repository, and is discarded without loss when a better base arrives. The technique is not merely cheaper to train &mdash; it is cheaper to <em>own</em>, which is where most of the cost of a tuned model actually sits.",
     "Twelve customers each needing a slightly different output convention is twelve full models to store and serve under the old arrangement. Under this one it is one base model in memory and twelve files of a few megabytes each, selected by whichever customer is asking."),

    ("h2", "When the full fine-tune is still the right call"),
    ("p", "It has not been made obsolete, only unusual. Reach for it when the shift is genuinely large &mdash; a domain, language or output modality the base handles poorly rather than differently &mdash; and when you have data in proportion to that ambition, which means many thousands of examples rather than several hundred. It is also the honest answer when a low-rank run has been tried properly, at more than one rank and more than one set of target modules, and has plateaued below what the task needs."),

    ("callout", "pitfall", "Both methods can lose capability you never measured",
     "<p>Training a model to be good at one narrow thing can make it worse at others, and adaptation reduces this without eliminating it because the frozen base is still being spoken over. The failure does not appear in the metric you are watching, since that metric is the task you tuned for and it improved. It appears the first time somebody asks the tuned model something ordinary and outside the tuning distribution.</p><p>The defence is the one the compression lesson already argues for: evaluate against the base model on slices, not on an aggregate. Keep a small set of general questions the tuning was never about, run it before and after, and treat a drop there as a cost of the change rather than as noise.</p>"),

    ("quiz", [
      ("Why does freezing the base weights save so much more memory than the parameter count suggests?",
       ["Frozen weights can be stored in lower precision automatically",
        "A frozen weight needs no gradient and no optimiser state, and those — not the weights — are what dominate training memory",
        "The forward pass skips frozen layers entirely"],
       1),
      ("A run on six hundred examples disappoints. Why is raising the rank a poor first response?",
       ["Higher ranks are unstable and often fail to converge",
        "Rank is capacity; with little data the extra capacity is spent memorising the training set, so training loss falls while held-out performance does not",
        "Rank must match the base model's hidden dimension to work correctly"],
       1),
      ("What is the reasoning behind quantising the base model in QLoRA?",
       ["Four-bit arithmetic is faster, which shortens the training run",
        "Precision matters most for weights being updated, and the base is frozen — so it can be stored coarsely, which brings larger models within reach of one machine",
        "Quantisation acts as a regulariser and improves the adapter's generalisation"],
       1),
    ]),
  ],
},
{
  "slug": "supervised-versus-reinforcement-tuning",
  "title": "Supervised versus Reinforcement Fine-Tuning",
  "subtitle": "One shows the model the answer; the other scores its attempts. The objective decides what you can teach.",
  "body": [
    ("p", "Everything so far has assumed you hand the model pairs of input and correct output and it learns to reproduce them. That is supervised fine-tuning, it is the right method most of the time, and it has a ceiling that is easy to state: the model is learning to imitate your examples, so it cannot become better than the examples you were able to write."),
    ("p", "The alternative does not show the model the answer at all. It lets the model attempt the task, scores the attempt, and adjusts the model towards whatever scored well. Block 0 described what a reasoning model is; this is the machinery that makes one."),

    ("terms", [
      ("Supervised fine-tuning (SFT)", "Imitate these answers",
       "Input and target output, and a loss that measures the difference. Cheap, stable, well understood, and bounded above by the quality of the demonstrations."),
      ("Reinforcement fine-tuning (RFT)", "Score these attempts",
       "The model generates, something grades the generation, and the update moves towards higher scores. Can exceed the demonstrations, because nothing is being copied."),
      ("The reward or verifier", "Whatever does the grading",
       "A unit test, a maths checker, a regular expression, a reward model trained on human preferences, or a rule you wrote. It is the specification of the task, and it is where the whole method succeeds or fails."),
      ("Group Relative Policy Optimisation (GRPO)", "The formulation that made this practical",
       "Sample several answers to the same prompt, score them, and push towards the ones that beat the group average. Dispensing with the separate value model that earlier methods needed is much of why this became affordable."),
    ]),

    ("know",
     "Supervised tuning is bounded by what you can demonstrate. Reinforcement tuning is bounded by what you can verify. Which you reach for depends on which of those you can actually do.",
     "The question to ask about a task is not which method is more advanced but whether you can write down the right answer or only recognise it when you see it. For tone, format, house style and domain idiom, you can demonstrate: write thirty good examples and supervised tuning will do the rest. For multi-step reasoning you generally cannot &mdash; nobody can author enough correct derivations to cover the space &mdash; but you can frequently check the final answer automatically, and a checker is enough to optimise against.",
     "Nobody hand-wrote the chains of reasoning that reasoning models produce. What existed was maths problems with known answers and code with tests that pass or fail. The model generated attempts, the verifier scored them, and the behaviour that survived was whatever reached correct answers &mdash; which is why this works best in domains with a checker and remains hard in domains without one."),

    ("figure", "Supervised tuning compares the output to a target. Reinforcement tuning generates several attempts, scores them, and moves towards the ones that beat the group.", '''<svg viewBox="0 0 560 196" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Supervised tuning compares output to a target; reinforcement tuning scores several sampled attempts against a verifier.">
<text x="10" y="16" class="d-label-sm">supervised &#8212; the answer is given</text>
<rect x="10" y="24" width="86" height="30" rx="5" class="d-box"/><text x="53" y="43" class="d-label" text-anchor="middle">prompt</text>
<path d="M96 39 L128 39" class="d-arrow"/>
<rect x="132" y="24" width="86" height="30" rx="5" class="d-box"/><text x="175" y="43" class="d-label" text-anchor="middle">output</text>
<path d="M218 39 L250 39" class="d-arrow"/>
<rect x="254" y="24" width="98" height="30" rx="5" class="d-box-good"/><text x="303" y="43" class="d-label" text-anchor="middle">target</text>
<text x="362" y="43" class="d-label-sm">loss = difference</text>
<text x="10" y="86" class="d-label-sm">reinforcement &#8212; only the score is given</text>
<rect x="10" y="94" width="86" height="30" rx="5" class="d-box"/><text x="53" y="113" class="d-label" text-anchor="middle">prompt</text>
<path d="M96 109 L128 109" class="d-arrow"/>
<rect x="132" y="80" width="86" height="22" rx="4" class="d-box"/><text x="175" y="95" class="d-label-sm" text-anchor="middle">attempt 1</text>
<rect x="132" y="106" width="86" height="22" rx="4" class="d-box"/><text x="175" y="121" class="d-label-sm" text-anchor="middle">attempt 2</text>
<rect x="132" y="132" width="86" height="22" rx="4" class="d-box"/><text x="175" y="147" class="d-label-sm" text-anchor="middle">attempt 3</text>
<path d="M218 109 L250 109" class="d-arrow"/>
<rect x="254" y="94" width="98" height="30" rx="5" class="d-box-accent"/><text x="303" y="113" class="d-label" text-anchor="middle">verifier</text>
<path d="M352 109 L384 109" class="d-arrow"/>
<text x="390" y="106" class="d-label-sm">move towards</text>
<text x="390" y="120" class="d-label-sm">above-average attempts</text>
<text x="10" y="180" class="d-label-sm">the verifier is the specification &#8212; the model will optimise exactly what it measures</text>
</svg>'''),

    ("h2", "The named methods you will meet"),
    ("terms", [
      ("Reinforcement learning from human feedback (RLHF)", "People rank, a model learns the ranking",
       "Humans compare outputs, a reward model is trained to predict their preferences, and the policy is optimised against that reward model. The original recipe for making a base model behave like an assistant."),
      ("Direct Preference Optimisation (DPO)", "Skip the reward model",
       "Given pairs of preferred and rejected responses, optimise the policy on the preference directly. Simpler and cheaper than the above, and popular for that reason; it needs preference pairs rather than a verifier."),
      ("Verifier-based RFT", "Grade against ground truth",
       "Where a correct answer can be checked mechanically &mdash; tests pass, the number matches, the output parses and satisfies a constraint. The strongest signal available, and restricted to tasks that have one."),
    ]),

    ("callout", "pitfall", "Reward hacking is not an edge case, it is the default behaviour",
     "<p>An optimiser given a measure will optimise the measure, and it is under no obligation to respect what you meant. Reward a code model on tests passing and it may write code that special-cases the tests. Reward answer length as a proxy for thoroughness and you will get length. Every measurement caveat this course has raised &mdash; the judge that prefers longer answers, the metric that moves while the thing it stands for does not &mdash; becomes sharper here, because you are no longer merely measuring with a flawed instrument, you are actively training against its flaws.</p><p>If the reward is itself a model, this compounds: the policy is being optimised to find that model&#39;s blind spots, and it is good at it. Hold out an evaluation the reward never sees, and watch it rather than the reward curve.</p>"),

    ("know",
     "A rising reward curve is not evidence that the model improved. It is evidence that the reward went up.",
     "These are only the same claim when the reward captures the goal exactly, which it never does. The gap between them is where reward hacking lives, and the reward curve cannot show you the gap because the gap is invisible to it by construction &mdash; this is the guardrail-metric argument from the evaluation block, applied to a system built to push on the primary metric as hard as it can.",
     "A model tuned to make a unit-test suite pass reaches a near-perfect reward. Inspection shows it had learned to detect the test fixture and return hard-coded values for the inputs the tests use. The reward was correct throughout; the suite really did pass. Nothing in the training signal distinguished passing the tests from writing the function."),

    ("h2", "Which to reach for"),
    ("ul", [
      "<strong>Supervised, almost always first.</strong> Cheaper, more stable, easier to debug, and sufficient for the format, tone and consistency problems that are the honest reason for most fine-tuning.",
      "<strong>Preference-based, when quality is a matter of taste.</strong> Where better and worse are recognisable but not writable, and you can collect comparisons more easily than exemplars.",
      "<strong>Verifier-based, when you can check but not demonstrate.</strong> Reasoning, code, structured extraction, anything with a mechanical notion of correct. This is the one that can exceed your own ability at the task.",
      "<strong>None of them, if the failure is knowledge.</strong> The first lesson in this block holds regardless of how the tuning is done, and no objective function installs facts that retrieval would supply exactly.",
    ]),

    ("quiz", [
      ("What determines the ceiling on supervised fine-tuning?",
       ["The size of the base model, which caps what any adaptation can add",
        "The quality of the demonstrations — the model is learning to imitate them, so it cannot exceed what you were able to write down",
        "The number of epochs before overfitting begins"],
       1),
      ("Why is reinforcement tuning the method behind reasoning behaviour rather than supervised tuning?",
       ["Reasoning requires more parameters than supervised tuning can update",
        "Nobody can author enough correct multi-step derivations to cover the space, but final answers can often be checked automatically — and a checker is enough to optimise against",
        "Supervised tuning cannot represent sequences longer than a few hundred tokens"],
       1),
      ("Your reward curve rises steadily through training. What does that establish?",
       ["That the model is improving at the task, which is what the reward measures",
        "That the reward went up — which equals improvement only where the reward captures the goal exactly, so it needs checking against an evaluation the reward never sees",
        "That the learning rate is well chosen for the run"],
       1),
    ]),
  ],
},
{
  "slug": "when-the-training-run-does-not-fit",
  "title": "When the Training Run Does Not Fit",
  "subtitle": "Three techniques that trade time or precision for memory — and the order to reach for them.",
  "body": [
    ("p", "The commonest failure of a first training run is not a bad result. It is an out-of-memory error thirty seconds in, and the instinct it produces &mdash; use a smaller model &mdash; is usually the wrong response, because the memory is going somewhere you can control."),

    ("h2", "Where the memory actually goes"),
    ("p", "Four things are resident during training and only the first is the model. The weights themselves; the gradients, which are the same size again; the optimiser state, which for the common choice of optimiser is roughly twice the weights once more; and the activations, which are the intermediate values from the forward pass that the backward pass needs in order to compute anything at all."),
    ("p", "The proportions surprise people. For a large model with a short sequence, the first three dominate and the arithmetic is fixed. With a long sequence or a large batch, activations grow until they are the largest single item &mdash; and unlike the other three, activations scale with what you feed the model rather than with how big it is."),

    ("figure", "Four claims on memory during training. Only one of them is the model, and the one that grows with your batch and sequence length is the one you can trade against.", '''<svg viewBox="0 0 540 152" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Training memory divided between weights, gradients, optimiser state and activations.">
<rect x="12" y="28" width="80" height="42" rx="5" class="d-box"/><text x="52" y="46" class="d-label-sm" text-anchor="middle">weights</text><text x="52" y="62" class="d-label-sm" text-anchor="middle">1&#215;</text>
<rect x="96" y="28" width="80" height="42" rx="5" class="d-box"/><text x="136" y="46" class="d-label-sm" text-anchor="middle">gradients</text><text x="136" y="62" class="d-label-sm" text-anchor="middle">1&#215;</text>
<rect x="180" y="28" width="118" height="42" rx="5" class="d-box"/><text x="239" y="46" class="d-label-sm" text-anchor="middle">optimiser state</text><text x="239" y="62" class="d-label-sm" text-anchor="middle">about 2&#215;</text>
<rect x="302" y="28" width="222" height="42" rx="5" class="d-box-accent"/><text x="413" y="46" class="d-label-b" text-anchor="middle">activations</text><text x="413" y="62" class="d-label-sm" text-anchor="middle">grows with batch and sequence length</text>
<text x="12" y="18" class="d-label-sm">fixed by the model and the optimiser</text>
<text x="302" y="18" class="d-label-sm">the part you control</text>
<text x="12" y="96" class="d-label-sm">precision &#8212; halve the weights, gradients and activations at once</text>
<text x="12" y="114" class="d-label-sm">accumulation &#8212; shrink the batch in memory, keep it in the maths</text>
<text x="12" y="132" class="d-label-sm">checkpointing &#8212; discard activations, recompute them in the backward pass</text>
</svg>'''),

    ("h2", "The three levers"),
    ("terms", [
      ("Mixed precision", "Store in half, accumulate in full",
       "Hold weights and activations in a sixteen-bit format while keeping a full-precision copy of the weights for the update. Roughly halves memory and is usually faster as well, because moving fewer bytes is the thing that helps on memory-bound hardware."),
      ("Gradient accumulation", "A large batch, taken in instalments",
       "Run several small batches, add up their gradients, and update once. The maths is the large batch; the memory is the small one. It costs no accuracy and it costs wall-clock time, since you have done the same forward passes without the parallelism."),
      ("Gradient checkpointing", "Throw activations away and recompute them",
       "Keep only a few activations from the forward pass and recompute the rest during the backward pass. A large reduction in activation memory in exchange for running part of the forward pass twice &mdash; typically some tens of per cent more time."),
      ("The order to try them", "Cheapest concession first",
       "Mixed precision, then accumulation, then checkpointing. The first often costs nothing at all, the second costs time, the third costs more time. Reach for a smaller model only after all three."),
    ]),

    ("know",
     "Two of these three cost time and none of them cost accuracy. That is why reaching for a smaller model first is usually the wrong move.",
     "Accumulation is arithmetically identical to the large batch it imitates, and checkpointing recomputes exactly the values it discarded, so neither changes the result of the run &mdash; only how long it takes. Mixed precision is the one that touches numerics, and the full-precision master copy of the weights exists precisely so that the update does not lose the small increments that matter. A smaller model, by contrast, changes what you are able to learn, which is the one concession that shows up in the evaluation.",
     "A run fails at a batch size of 16 on a 13-billion-parameter model. Mixed precision alone brings it within reach; if it does not, four accumulation steps at a batch of 4 give the same gradient as the batch of 16 at a quarter of the activation memory, and the only cost is that the epoch takes longer. Neither of those changes a single number in the final evaluation."),

    ("callout", "pitfall", "The failure that looks like the technique and is not",
     "<p>Sixteen-bit formats have a much narrower range than thirty-two-bit ones, and gradients are small numbers. In the older half-precision format they can underflow to zero, at which point training quietly stops learning &mdash; the loss flattens and nothing errors. The standard remedy is loss scaling: multiply the loss before the backward pass to lift the gradients into representable range, then divide it out before the update. Modern frameworks do this for you, and the newer sixteen-bit format designed for machine learning trades precision for range specifically to avoid the problem.</p><p>The reason to know this anyway is diagnostic. A flat loss curve immediately after enabling mixed precision is a numerics problem, not a learning-rate problem, and it will absorb an afternoon if you attack it as the latter.</p>"),

    ("h2", "What none of them fix"),
    ("p", "These are memory techniques, and the hardware lesson&#39;s first rule still governs: capacity is a hard wall and library support is what actually blocks people. A sixteen-bit format that has no implementation on your accelerator will fall back to something slower or fail outright, and no amount of accumulation makes a model fit that was never going to. Check that it fits, then check that the operations you need exist, and only then start trading time for room."),

    ("quiz", [
      ("Which of the four claims on training memory grows with your batch size and sequence length rather than with the model?",
       ["The optimiser state, since it tracks statistics per example",
        "The activations — intermediate forward-pass values the backward pass needs, which is why they are the part you can trade against",
        "The gradients, which are computed per example before being averaged"],
       1),
      ("What does gradient accumulation cost you?",
       ["Some accuracy, since gradients from small batches are noisier",
        "Wall-clock time only — the summed gradient is arithmetically the same as the large batch, so the result is unchanged",
        "Memory, which is traded for a shorter run"],
       1),
      ("The loss goes flat immediately after you enable mixed precision. What should you suspect first?",
       ["The learning rate is now too high for the reduced precision",
        "Gradients underflowing to zero in the narrower sixteen-bit range — a numerics problem that loss scaling exists to solve",
        "The model is too small for the task and has underfit"],
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
