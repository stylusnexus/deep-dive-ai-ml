TITLE = "Block 5 · Evaluation"
TOPIC = "block5-evaluation"
ICON = "📏"
DESCRIPTION = "The front door to everything this course teaches about measurement, then the two things it did not yet teach: eval data whose labels are actually derivable, and running one set across many models without the comparison lying to you."
TAGS = ["ai", "evaluation", "measurement"]
COLOR = "teal"
CREATED = "2026-08-27"
ID_BASE = "1787800000"

LESSONS = [
{
  "slug": "where-evaluation-lives",
  "title": "Where Evaluation Lives",
  "subtitle": "The map. Which artefact answers which question, and the order that stops you wasting a week.",
  "body": [
    ("p", "Evaluation in this course is deliberately spread out. The vocabulary sits in Block 0 because you need it before anything else makes sense; the procedure sits in engineering practice because it is a working habit, not a topic; the checklist sits in the standard operating procedures because you run it rather than read it. That distribution is right, and it has one cost: there is no front door. This lesson is the door."),

    ("p", "Nothing here is new. If you have read the lessons it points at, you can skip it — and if you have not, reading them in this order will save you the week that reading them in a different order costs."),

    ("h2", "Four questions, four places"),
    ("terms", [
      ("Is my measurement trustworthy?",
       "How to Measure, step 0 — and measurement.md",
       "The fixture must fail before the work and pass after it. If &ldquo;did nothing&rdquo; and &ldquo;solved it&rdquo; can score the same, every number below is noise. This is the step people skip and the reason most evaluation effort is wasted."),
      ("What am I measuring against?",
       "The Eval Battery",
       "A fixed set of tasks with checkable outcomes, held privately, that reflect your work rather than the field's. Also why public benchmarks will not answer your question — contamination, gaming, and task mismatch."),
      ("How do serious people do it?",
       "SWE-bench, and How to Actually Run It",
       "A real harness, in detail: what a task actually is, the four variants and which number gets quoted, and what the score does not mean. Read it for the harness design, not the leaderboard."),
      ("How do I score something with no right answer?",
       "Models Judging Models, then Rubrics and Blind Reads in this block",
       "The first covers what a judge buys and the four biases it ships with. The second is the two mechanics that make one usable — a rubric careful readers can agree on, and blinding so the score is about the output rather than about what you hoped for."),
      ("Why did this number move?",
       "Confounds You Cannot See, and Localising a Failure",
       "The difference between a result and an explanation. A number that moved without a located cause is a number that will move back."),
    ]),

    ("figure", "The evaluation material and the order to take it in. Two lessons in this block fill gaps the others left: labels you can defend, and a comparison across models that does not lie.", '''<svg viewBox="0 0 640 250" role="img" aria-label="Map of evaluation material across the course"><defs><marker id="e5" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" class="d-fill-accent"/></marker></defs>
<rect x="10" y="20" width="140" height="56" rx="7" class="d-box-accent"/>
<text x="24" y="42" class="d-label-b">0 · Instrument</text>
<text x="24" y="60" class="d-label-sm">prove it first</text>
<path d="M150 48 L196 48" class="d-arrow-accent" marker-end="url(#e5)"/>
<rect x="196" y="20" width="140" height="56" rx="7" class="d-box"/>
<text x="210" y="42" class="d-label-b">1 · Battery</text>
<text x="210" y="60" class="d-label-sm">your tasks, held back</text>
<path d="M336 48 L382 48" class="d-arrow-accent" marker-end="url(#e5)"/>
<rect x="382" y="20" width="140" height="56" rx="7" class="d-box"/>
<text x="396" y="42" class="d-label-b">2 · Labels</text>
<text x="396" y="60" class="d-label-sm">derivable, not opinion</text>
<path d="M452 76 L452 112" class="d-arrow-accent" marker-end="url(#e5)"/>
<rect x="382" y="112" width="140" height="56" rx="7" class="d-box"/>
<text x="396" y="134" class="d-label-b">3 · Run it</text>
<text x="396" y="152" class="d-label-sm">baseline, then one change</text>
<path d="M382 140 L336 140" class="d-arrow-accent" marker-end="url(#e5)"/>
<rect x="196" y="112" width="140" height="56" rx="7" class="d-box"/>
<text x="210" y="134" class="d-label-b">4 · Compare</text>
<text x="210" y="152" class="d-label-sm">across models</text>
<path d="M196 140 L150 140" class="d-arrow-accent" marker-end="url(#e5)"/>
<rect x="10" y="112" width="140" height="56" rx="7" class="d-box"/>
<text x="24" y="134" class="d-label-b">5 · Explain</text>
<text x="24" y="152" class="d-label-sm">locate the cause</text>
<text x="24" y="204" class="d-label-sm">Steps 2 and 4 are this block. The rest already exist —</text>
<text x="24" y="222" class="d-label-sm">in Block 0 vocabulary, engineering practice, and the SOPs.</text>
</svg>'''),

    ("know",
     "Evaluation fails at step zero far more often than at the clever parts.",
     "Almost every wasted evaluation effort is a good procedure run on an instrument nobody checked. The fixture passed whatever you did, or failed whatever you did, and the elaborate comparison downstream was measuring the harness. The clever parts — judges, sweeps, statistics — cannot rescue a broken instrument, and they are what people reach for first.",
     "A set where every model scores identically is not a finding about models. It is a finding about your harness, and reading it as a finding about models has cost teams months."),

    ("h2", "What this block adds"),
    ("p", "Two things the material above does not cover. The first is where the labels come from: a battery with indefensible labels measures your opinions rather than the system, and the failure is invisible because everything still runs. The second is comparing across models, where the same set can produce a different ranking depending on a budget you set without thinking about it."),

    ("callout", "matters", "Read the procedure before the tools",
     "<p>How to Measure is six steps and takes ten minutes to read. Every tool in this block is worthless applied out of that order — a judge calibrated against an unproven instrument produces confident, reproducible, wrong numbers.</p>"),

    ("quiz", [
      ("Your eval set gives every model you try the same score. What is the first thing to suspect?",
       ["The models are genuinely equivalent on this task",
        "The harness — a fixture that scores identically regardless of what it is given is measuring itself",
        "The set is too small to separate them"], 1),
      ("Why is evaluation material spread across several parts of this course rather than gathered in one block?",
       ["Because the topics are unrelated to each other",
        "Because the vocabulary is needed before anything else, and the procedure is a working habit rather than a topic — this lesson is the index that distribution costs you",
        "Because evaluation is not important enough for its own block"], 1),
    ]),
  ],
},
{
  "slug": "eval-data-you-can-trust",
  "title": "Eval Data You Can Trust",
  "subtitle": "A gold label is only correct if you can name the rule that produces it.",
  "body": [
    ("p", "You write the rules the system must follow. You write the labels it will be scored against. Both came out of your head in the same afternoon, so it does not occur to you that they might disagree — and when they do, the system applies your written rule correctly, produces the answer the rule demands, and scores as wrong. You then spend a day improving a model that was right."),

    ("p", "This is not a rare failure. It is the default outcome of writing labels and rules separately, and it is silent: nothing errors, the run completes, and the report is confidently incorrect."),

    ("h2", "Synthetic on purpose"),
    ("p", "The instinct is to reach for real data because real data is honest. For evaluation, that instinct is often wrong. Real data comes with labels somebody else assigned for a purpose that was not yours, at a quality you cannot inspect. Synthetic data lets you plant the answer, which means the label is correct by construction rather than by trust."),

    ("terms", [
      ("Correct by construction",
       "You planted the fact, so you know the answer",
       "The document containing the answer is one you wrote, so the gold label is not an estimate. This is the only kind of label you can debug."),
      ("Derivable",
       "The label follows from rules the system can see",
       "Not merely correct in your judgement — reachable by applying the written policy to the written case. If it is not derivable, no amount of model capability will find it."),
      ("Under-determined label",
       "Two answers are equally defensible",
       "The rules do not distinguish them, so the label encodes a preference you never wrote down. Fix the rules, or accept both answers."),
      ("Self-contradicting rules",
       "A rule elsewhere forbids the label",
       "A general clause quietly overrides a specific one. The system obeys the general clause and is marked wrong for obeying it."),
    ]),

    ("h2", "The check that costs ten minutes"),
    ("p", "Before running anything end to end, run only the deciding stage against the labelled cases and confirm each label is reachable. Not to score the system — to score your data. Every disagreement is a question about which of the two is wrong, and the answer is frequently the label."),

    ("figure", "The check runs before the evaluation, not after. A disagreement at this stage is a question about the data; a disagreement after a full run looks like a question about the model, which is why the same bug survives for weeks.", '''<svg viewBox="0 0 640 210" role="img" aria-label="Checking label derivability before evaluating"><defs><marker id="e5b" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" class="d-fill-accent"/></marker></defs>
<rect x="12" y="18" width="150" height="62" rx="7" class="d-box"/>
<text x="26" y="42" class="d-label-b">Written rules</text>
<text x="26" y="62" class="d-label-sm">what the system sees</text>
<rect x="12" y="104" width="150" height="62" rx="7" class="d-box"/>
<text x="26" y="128" class="d-label-b">Gold labels</text>
<text x="26" y="148" class="d-label-sm">what you scored against</text>
<path d="M162 50 L226 84" class="d-arrow-accent" marker-end="url(#e5b)"/>
<path d="M162 134 L226 100" class="d-arrow-accent" marker-end="url(#e5b)"/>
<rect x="226" y="62" width="164" height="60" rx="7" class="d-box-accent"/>
<text x="240" y="86" class="d-label-b">Derivability check</text>
<text x="240" y="106" class="d-label-sm">one stage, labelled cases only</text>
<path d="M390 92 L446 92" class="d-arrow-accent" marker-end="url(#e5b)"/>
<rect x="446" y="18" width="180" height="58" rx="7" class="d-box"/>
<text x="460" y="42" class="d-label-b">Agrees → evaluate</text>
<text x="460" y="62" class="d-label-sm">the data is defensible</text>
<rect x="446" y="106" width="180" height="58" rx="7" class="d-box"/>
<text x="460" y="130" class="d-label-b">Disagrees → fix data</text>
<text x="460" y="150" class="d-label-sm">usually the label, not the model</text>
</svg>'''),

    ("know",
     "If you cannot name the rule that produces a label, the label is an opinion.",
     "An opinion is a perfectly good thing to hold, and a terrible thing to score a system against, because the system has no access to it. When a label and a written rule disagree, the system will follow the rule every time — so the disagreement is not a model failure to be fixed with a better prompt. It is a data defect, and every hour spent on the model is an hour spent on the wrong thing.",
     "A policy set said any case where the event code was contradicted by the note must be escalated to a human. Six labels said to handle those cases on their merits instead. The system escalated, exactly as written, and scored six failures. The model was right and the data was wrong."),

    ("callout", "pitfall", "The general clause that eats the specific ones",
     "<p>Escalation rules are the usual offender. A clause like &ldquo;escalate anything ambiguous&rdquo; sounds cautious and quietly overrides every specific rule you wrote, because almost everything interesting is ambiguous. When a system escalates far more than you expected, read your own escalation clause before blaming the model.</p>"),

    ("h2", "What a disagreement is telling you"),
    ("ul", [
      "<strong>The label is wrong</strong> — a rule elsewhere forbids it. Fix the rules or fix the label, and record which you chose.",
      "<strong>The rules are incomplete</strong> — two answers are equally defensible and your label picked one. Add the clause that distinguishes them, or accept both.",
      "<strong>The system is wrong</strong> — the label is genuinely derivable and it failed to derive it. This is the case you wanted, and it is the rarest of the three on a first run.",
    ]),

    ("callout", "insight", "This is why the corpus in Block 3 is synthetic",
     "<p>Every fact in that corpus lives in exactly one document, deliberately. That is what makes recall measurable rather than estimated — the gold set names the document, and the naming is correct because the document was written to contain the fact.</p>"),

    ("quiz", [
      ("Your system disagrees with a gold label. What is the first thing to check?",
       ["Whether a larger model gets it right",
        "Whether the label is derivable from the rules the system was given — a rule elsewhere may forbid it",
        "Whether the prompt needs more examples"], 1),
      ("Why is synthetic data often better than real data for an eval set?",
       ["It is faster to generate and cheaper to store",
        "You planted the answer, so the label is correct by construction rather than by trusting somebody else's annotation",
        "Real data is usually too noisy for models to handle"], 1),
      ("Two answers to a labelled case are equally defensible under your written rules. What does that mean?",
       ["The case is too hard and should be removed from the set",
        "The label encodes a preference you never wrote down — either add the rule that distinguishes them, or accept both answers",
        "The model needs a clearer system prompt"], 1),
    ]),
  ],
},
{
  "slug": "one-set-many-models",
  "title": "One Set, Many Models",
  "subtitle": "The comparison is the point, and a budget you set without thinking is what breaks it.",
  "body": [
    ("p", "A private battery answers whether a change helped. Running it across several models answers a different and more expensive question: which model should this system use. The second question is where most comparisons quietly stop being valid, because holding everything fixed across models is harder than it looks and nothing warns you when you have failed."),

    ("h2", "The thing that is not held fixed"),
    ("p", "You set a maximum output length once, sized against the model you developed on, and it becomes part of the harness nobody revisits. Then you add a reasoning model. A reasoning model spends output tokens thinking before it emits a single visible word, so a budget that comfortably fits an answer may not fit the thinking that precedes it. The reply comes back empty — not short, empty — and an empty answer scores as a wrong one."),

    ("p", "The comparison now says the reasoning model is worse. What it actually measured was your token budget, and the ranking will reverse the moment somebody raises a number nobody thought was a parameter."),

    ("terms", [
      ("Output budget",
       "Covers thinking and answer together",
       "On a reasoning model these come out of the same allowance. Size it against the model that needs the most, not the one you developed against."),
      ("Finish reason",
       "The model says why it stopped",
       "A completion that stopped because it ran out of budget reports that fact. Record it, and a truncated run can never be read as a failed one."),
      ("Empty is not short",
       "The failure mode that looks like an answer",
       "An empty string scores as a wrong answer rather than an error, which is why this survives review. Nothing in the report says the budget was the cause."),
      ("Non-completion",
       "Infrastructure, not capability",
       "Timeouts, rate limits and truncations are not the model being wrong. Classify them out, or they become the cheaper provider's score."),
    ]),

    ("figure", "The same question, the same set, two budgets. The left column is a measurement of the model; the right column is a measurement of the harness, and both look like results.", '''<svg viewBox="0 0 640 220" role="img" aria-label="How an output budget silently changes a model comparison"><rect x="14" y="16" width="290" height="180" rx="8" class="d-box"/>
<text x="30" y="42" class="d-label-b">Budget sized for the answer</text>
<text x="30" y="72" class="d-label-sm">standard model — thinks little</text>
<text x="30" y="92" class="d-label-sm">answer fits → scores well</text>
<text x="30" y="124" class="d-label-sm">reasoning model — thinks first</text>
<text x="30" y="144" class="d-label-sm">budget spent on thinking</text>
<text x="30" y="164" class="d-label-sm">reply is EMPTY → scores wrong</text>
<text x="30" y="186" class="d-label-sm">verdict: reasoning model is worse</text>
<rect x="336" y="16" width="290" height="180" rx="8" class="d-box-accent"/>
<text x="352" y="42" class="d-label-b">Budget sized for thinking</text>
<text x="352" y="72" class="d-label-sm">standard model — unchanged</text>
<text x="352" y="92" class="d-label-sm">answer fits → scores well</text>
<text x="352" y="124" class="d-label-sm">reasoning model — thinks first</text>
<text x="352" y="144" class="d-label-sm">then answers within budget</text>
<text x="352" y="164" class="d-label-sm">reply is complete → scores well</text>
<text x="352" y="186" class="d-label-sm">verdict: reversed</text>
</svg>'''),

    ("know",
     "An empty answer and a wrong answer score the same, and only one of them is about the model.",
     "Scoring treats a missing reply as a failure because that is the safe default, which means a harness problem enters the report wearing the costume of a capability problem. Nothing errors, no warning appears, and the number is reproducible — it will reproduce the same wrong result every time you run it. The only defence is recording why each completion stopped and refusing to score the ones that did not finish.",
     "Three of ten questions came back blank on a reasoning model with a two-hundred-token ceiling. All two hundred had gone to thinking. Raising the ceiling moved multi-hop correctness from zero out of three to two out of three — the model had not changed at all."),

    ("h2", "What has to be identical, and what cannot be"),
    ("ul", [
      "<strong>Identical:</strong> the set, the prompt, the scoring, the number of repeats, and the rule for classifying non-completions.",
      "<strong>Sized to the greediest model:</strong> the output budget and the timeout. A shared value tuned to the cheapest model is a handicap, not a control.",
      "<strong>Genuinely different, and worth reporting:</strong> cost and latency per item. A model that wins on accuracy and loses on both is a decision, not a result.",
      "<strong>Recorded every run:</strong> a manifest naming model, endpoint, every budget and the config version. Without it, a comparison cannot be rerun and therefore cannot be trusted.",
    ]),

    ("callout", "warning", "A ranking with no non-completion column is not finished",
     "<p>If the report does not say how many runs failed to complete and why, the ranking silently includes infrastructure failures as capability failures. The provider having a bad afternoon becomes the model being bad at your task, permanently, in a table somebody will cite next quarter.</p>"),

    ("callout", "matters", "Cost and latency are results, not footnotes",
     "<p>The question was which model this system should use, and that question is never answered by accuracy alone. Put cost per item and latency per item in the same table as the score, or the table quietly recommends the most expensive option every time.</p>"),

    ("quiz", [
      ("A reasoning model scores badly on your set while a simpler model scores well. What do you check before concluding anything?",
       ["Whether the reasoning model needs a different system prompt",
        "Whether replies came back empty because the output budget was spent on thinking — check the finish reason before the capability",
        "Whether the set is biased toward simple questions"], 1),
      ("Why must non-completions be classified separately from wrong answers?",
       ["To make the report longer and more thorough",
        "Because a timeout or truncation is an infrastructure failure, and scoring it as a capability failure attributes a bad afternoon to the model permanently",
        "Because providers charge differently for failed requests"], 1),
      ("What must be sized to the greediest model rather than shared at one value?",
       ["The number of repeats per item",
        "The output budget and the timeout — a value tuned to the cheapest model handicaps the others rather than controlling for them",
        "The scoring rubric"], 1),
    ]),
  ],
},
{
  "slug": "rubrics-and-blind-reads",
  "title": "Rubrics and Blind Reads",
  "subtitle": "A rubric makes a judgement checkable. Blinding makes it honest. Neither works without the other.",
  "body": [
    ("p", "The engineering-practice block covers what a judge buys you and the four biases it ships with. This lesson is the two mechanics that turn those principles into something you can run: how to write a rubric a judge can actually apply, and how to blind a read so the score is about the output rather than about what you were hoping for."),

    ("h2", "Why one number is the wrong output"),
    ("p", "Asking for a score out of ten produces a number nobody can act on. It clusters — almost everything lands on seven or eight — and when it moves you cannot tell which property changed. A rubric replaces it with several judgements, each of which names something specific enough that a disagreement is resolvable."),

    ("terms", [
      ("Dimensions that fail independently", "The test for whether you have the right ones",
       "Groundedness, completeness and tone can each be wrong while the others are right, so scoring them separately tells you what to fix. If two dimensions always move together you have one dimension written twice."),
      ("Observable criteria, not adjectives", "The difference between a rubric and a vibe",
       "&ldquo;Complete&rdquo; is an adjective and two readers will disagree. &ldquo;Answers all three parts of the question&rdquo; is observable and they will not. Every level of every dimension needs a criterion you could check by pointing at the text."),
      ("Three or four levels, not seven", "Because the judge cannot tell them apart",
       "A grader that cannot reliably distinguish a six from a seven produces noise in the low bits and a false sense of precision. Fewer levels, each clearly separated, beats a fine scale nobody can apply consistently."),
      ("An anchor example per level", "What makes it transferable",
       "One real output that sits at each level, kept with the rubric. This is what lets a second person — or a second model, or you in three months — apply the same standard rather than a similar-sounding one."),
    ]),

    ("know",
     "If two people cannot apply your rubric to the same output and agree, it is not a rubric.",
     "The purpose of writing it down is to move a judgement from taste to procedure, and the only test of whether that worked is agreement. A rubric that produces disagreement between careful readers has not failed to describe quality — it has failed to describe anything, and running a model against it will produce confident, reproducible, meaningless numbers.",
     "Check it before you automate anything. Take ten outputs, have two people score them independently against the rubric, and look at where they diverged. Every disagreement is a dimension that needs a sharper criterion or an anchor example, and finding those with ten items is far cheaper than discovering them after a thousand."),

    ("h2", "Blind reads, and what they are actually for"),
    ("p", "A blind read is a judgement made without knowing where the output came from — which model, which variant, whether it is the change you spent a week on or the baseline you expect it to beat. The point is not fairness in the abstract. It is that expectation is a measurable bias, it applies to people at least as strongly as to models, and it points in the direction of whatever you were hoping for."),

    ("terms", [
      ("Blind the source", "Which model or variant produced it",
       "The one everybody thinks of. A judge from the same family as the system under test recognises its own output; a human who knows which one is the new version finds reasons to like it."),
      ("Blind the condition", "Treatment or control",
       "The one people skip. If the reviewer knows this is the run that is supposed to be better, they are no longer measuring — and this matters most exactly when the change is yours."),
      ("Randomise the order", "And run both",
       "Position bias is already covered in the judging lesson; blinding does not remove it. Presenting the same pair in both orders and requiring agreement is what removes it."),
      ("Blind the calibration set too", "The step that gets missed",
       "When you hand-label thirty items to check the judge against, label them blind. A calibration set scored while knowing the answers measures how well the judge agrees with your expectations rather than with your judgement."),
    ]),

    ("figure", "The two do different jobs and neither substitutes for the other. A rubric without blinding gives you consistent bias; blinding without a rubric gives you honest noise.", '''<svg viewBox="0 0 640 210" role="img" aria-label="Rubric and blinding as two independent axes"><line x1="60" y1="176" x2="606" y2="176" class="d-arrow-accent"/>
<line x1="60" y1="176" x2="60" y2="24" class="d-arrow-accent"/>
<text x="240" y="200" class="d-label-sm">blinded →</text>
<text x="10" y="96" class="d-label-sm">rubric</text><text x="16" y="112" class="d-label-sm">↑</text>
<rect x="80" y="96" width="228" height="66" rx="6" class="d-box"/><text x="92" y="120" class="d-label-b">consistent bias</text><text x="92" y="140" class="d-label-sm">repeatable, and tilted</text><text x="92" y="156" class="d-label-sm">toward what you hoped</text>
<rect x="330" y="96" width="256" height="66" rx="6" class="d-box-accent"/><text x="342" y="120" class="d-label-b">what you want</text><text x="342" y="140" class="d-label-sm">checkable and honest</text><text x="342" y="156" class="d-label-sm">disagreements are resolvable</text>
<rect x="80" y="32" width="228" height="56" rx="6" class="d-box"/><text x="92" y="54" class="d-label-b">taste, with a decimal point</text><text x="92" y="74" class="d-label-sm">neither checkable nor honest</text>
<rect x="330" y="32" width="256" height="56" rx="6" class="d-box"/><text x="342" y="54" class="d-label-b">honest noise</text><text x="342" y="74" class="d-label-sm">unbiased, and unrepeatable</text>
</svg>'''),

    ("h2", "The loop that produces a judge worth running"),
    ("ul", [
      "<strong>Write the rubric first</strong>, with dimensions that fail independently and a criterion you could point at for each level.",
      "<strong>Score ten items with two people</strong>, independently, and sharpen wherever they disagreed. Cheap, and it finds the ambiguity while fixing it is still free.",
      "<strong>Hand-label thirty to fifty, blind</strong>, as the calibration set. This is the ground truth the judge is measured against, and it is worthless if it was labelled knowing the answers.",
      "<strong>Run the judge against that set</strong> and report the agreement rate. A judge score published without a known agreement rate is an opinion with a decimal point.",
      "<strong>Re-check agreement when anything changes</strong> — the judge model, the rubric wording, the prompt. All three are treatments, and a judge that drifted is worse than no judge because it is trusted.",
    ]),

    ("callout", "pitfall", "Some things cannot be blinded, and pretending otherwise is worse",
     "<p>Outputs carry style tells. One model formats lists differently, another opens with a summary, a fine-tuned variant has the house voice. A reader who knows the systems will often infer which is which despite the labels being stripped, and a judge from the same family may recognise its own output regardless. Blinding reduces the effect rather than removing it, so record that it was blinded <em>and</em> whether the reader could plausibly have guessed — an unblindable comparison needs a different design, usually a judge from an unrelated family.</p>"),

    ("callout", "matters", "Blind the calibration set, or the whole exercise is circular",
     "<p>This is the failure that quietly voids a result. You label the ground truth knowing which system produced each answer, the judge is then tuned until it agrees with those labels, and the reported agreement rate measures how well the judge reproduces your expectations. Everything downstream inherits it, and nothing in the numbers looks wrong.</p>"),

    ("quiz", [
      ("What is the test of whether a rubric is a rubric?",
       ["That it covers every dimension of quality that matters",
        "That two people can apply it to the same output and agree — disagreement means it has failed to describe anything",
        "That it produces scores which correlate with user satisfaction"],
       1),
      ("Which part of blinding is most often skipped?",
       ["Blinding which model produced each output",
        "Blinding whether a run is the treatment or the control, and blinding the hand-labelled calibration set",
        "Randomising the order in which outputs are presented"],
       1),
      ("Why does a rubric without blinding still fail?",
       ["Rubrics are only reliable when applied by more than one reader",
        "It gives you consistent bias — repeatable scores tilted toward whatever you were hoping for, which is worse than noise because it looks trustworthy",
        "Rubric dimensions drift over time without a control group"],
       1),
    ]),
  ],
},
]
