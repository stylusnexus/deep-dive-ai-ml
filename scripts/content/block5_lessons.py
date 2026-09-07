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
    ("related", ["why-measurement-decides", "eval-battery", "one-set-many-models", "after-it-ships"]),
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

    ("h2", "Ground truth you did not write yourself"),
    ("p", "Hand-labelling is slow and it carries the labeller&#39;s opinion, which is a problem when the labeller is also the person hoping the change worked. Before starting, look for ground truth that already exists in written form &mdash; a specification, an author&#39;s own stated contract for when something should apply, a config that declares the intended behaviour. Labels lifted from an artefact somebody else wrote are free and they cannot be bent towards the result you want."),

    ("know",
     "Then say which way your ground truth is biased, because it changes what the number means rather than merely qualifying it.",
     "Free labels are rarely neutral. If the phrases you are scoring against are the same phrases the mechanism was built from, then you are measuring under conditions chosen to flatter it, and the result is an <em>upper bound</em> rather than an estimate. Naming the direction converts a number people will argue about into one they can act on, and it usually converts it downwards.",
     "A retrieval mechanism scores 44 out of 97 against labels taken from the descriptions its own index was built on. Reported bare, that reads as mediocre and fixable. Reported with the direction &mdash; those labels are literal substrings of the indexed text, so this is the most favourable measurement available &mdash; it reads as the mechanism barely working under ideal conditions, which is a different finding and a different decision."),

    ("h2", "Rows that could never have reached the thing you are measuring"),
    ("p", "An evaluation set can be perfectly labelled and still measure nothing, if production would have rejected half its rows before they arrived. Systems accumulate gates &mdash; a router that sends the request elsewhere, a confidence floor, a permission check, a lane filter &mdash; and a harness that calls the ranking function directly steps around all of them."),
    ("p", "The failure is asymmetric and flattering in a specific way: the rows that never reach the mechanism are disproportionately the odd ones, so bypassing the gate loads your evaluation with negatives the system would never have been asked about. A precision figure computed that way is not pessimistic or optimistic in a way you can correct for, because you no longer know what population it describes. Before trusting a number, ask which rows can actually reach the code being measured, and apply production&#39;s gates to the set."),

    ("callout", "pitfall", "Two recording habits that stop a bad number outliving its correction",
     "<p><strong>Write down the invalidated result, not only the good one.</strong> A number measured on a configuration production never ran is void, and deleting it quietly means the next person finds it in a chat log and cites it as a baseline. Recording it alongside one paragraph on why it does not count costs almost nothing and stops that.</p><p><strong>State what a change does not fix.</strong> A fix that restores a broken path and leaves the ranking quality exactly where it was should say so, or it will be credited with a benefit it never delivered &mdash; and the next person to look will start from a belief that the area is already handled.</p>"),

    ("h2", "What a disagreement is telling you"),
    ("ul", [
      "<strong>The label is wrong</strong> — a rule elsewhere forbids it. Fix the rules or fix the label, and record which you chose.",
      "<strong>The rules are incomplete</strong> — two answers are equally defensible and your label picked one. Add the clause that distinguishes them, or accept both.",
      "<strong>The system is wrong</strong> — the label is genuinely derivable and it failed to derive it. This is the case you wanted, and it is the rarest of the three on a first run.",
    ]),

    ("callout", "insight", "This is why the corpus in Block 3 is synthetic",
     "<p>Every fact in that corpus lives in exactly one document, deliberately. That is what makes recall measurable rather than estimated — the gold set names the document, and the naming is correct because the document was written to contain the fact.</p>"),
    ("related", ["labels-and-holdouts", "data-leakage", "rubrics-and-blind-reads", "one-set-many-models"]),
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
    ("related", ["is-the-difference-real", "eval-data-you-can-trust", "where-evaluation-lives", "swe-bench-and-how-to-run-it"]),
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
    ("related", ["models-judging-models", "judging-a-conversation", "labels-and-holdouts", "eval-data-you-can-trust"]),
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
{
  "slug": "is-the-difference-real",
  "title": "Is the Difference Real?",
  "subtitle": "Pairing, spread, Bessel's correction and the peeking problem — the arithmetic that decides whether a number moved or wobbled.",
  "body": [
    ("p", "Block 2 says that when two models&#39; confidence intervals overlap you cannot claim a difference from those intervals alone. Nothing carried that into this block, so every score here has been read as though it were exact. This lesson is the repair, and its numbers come from simulations in <code>scripts/measure_eval_statistics.py</code> rather than from assertion."),

    ("h2", "What each of these costs you when you do not know it"),
    ("p", "This is the only lesson in the course that looks like statistics, so it is worth being blunt about why it earns its place. Each item below has a failure attached, and every one of them is a failure that looks like success at the time."),

    ("terms", [
      ("Not knowing about pairing",
       "You abandon improvements that worked",
       "You make a real change, test it wrongly, see nothing, and conclude the idea failed. The simulation later in this lesson takes a genuine effect from detected almost always to detected almost never purely by testing it the wrong way. The work was fine; the verdict was an artefact."),
      ("Reporting only means",
       "You ship a change that broke a subset",
       "The average moved up, so it looked good. Half your users got worse and nothing in the report said so, and you find out from them rather than from the measurement."),
      ("Dividing by n",
       "You are most overconfident exactly when you should be least",
       "It understates spread, and the error is largest at small sample sizes — which is every eval set in this course. Overstated confidence on ten questions is how a coin-flip difference gets written into a document as a finding."),
      ("Peeking at a running test",
       "You accumulate wins that never add up",
       "Each individual result looked significant when you stopped. None of them were, so none of them compound, and a year later the product is not better and nobody can say which of the twenty improvements failed to arrive."),
    ]),

    ("p", "None of this requires becoming a statistician. It requires knowing that a number produced by a measurement has a width, and four specific ways that width gets misread."),

    ("h2", "Pairing, which is the one that matters most"),
    ("p", "Two measurements are <strong>paired</strong> when each one in the first set has a natural partner in the second — the same unit, measured twice. An eval is paired by construction: question one is scored under system A and under system B, and those two numbers are about the same question. An A/B test on live traffic is not paired, because different users were assigned to different arms and no user appears in both."),

    ("p", "The distinction decides which test to run, and the cost of getting it wrong is larger than it sounds. Question difficulty varies enormously — some questions are hard for everything and some are easy for everything — and in a paired comparison that difficulty affects both members of each pair equally, so subtracting one from the other removes it. An unpaired test cannot subtract it and leaves it in the noise, where it usually dwarfs the effect you are looking for."),

    ("code", """20 questions, a real effect of +0.30, difficulty varying by ~1.0

  unpaired test detects it :   0.6% of the time
  paired   test detects it :  95.9% of the time"""),

    ("know",
     "The unpaired test is not wrong. It is answering a question nobody asked.",
     "It asks whether two unrelated piles of numbers have different means. The question you actually had was whether B beats A <em>question by question</em>, and the pairing is the information that turns one into the other. Throwing it away is not a conservative choice or a safe default — in the simulation above it took a real, large effect from almost always detected to almost never, on identical data.",
     "The rule is simple: if you can line the two sets up one-to-one and the pairing means something, use a paired test. Same questions through two models, same code before and after a change, same document scored by two judges."),

    ("h2", "Real is not the same as large"),
    ("p", "Everything above establishes whether a difference is <em>real</em> &mdash; whether it is more than noise. That is a different question from whether it is <strong>big enough to act on</strong>, and the two get run together constantly because significance is the number people report."),
    ("p", "The distinction has a direction that matters: a large enough sample makes almost any difference significant, including differences far too small to change a decision. Run enough items and a 0.2 percentage point improvement becomes unambiguously real, and it is still 0.2 percentage points. The size of the difference is its <strong>effect size</strong>, and it is the half that tells you whether to ship."),

    ("know",
     "Report the size alongside the significance, because significance alone cannot tell a discovery from a rounding error.",
     "A p-value answers one narrow question: if there were no real effect, how often would a difference at least this large turn up anyway? It is not the probability that your result is noise &mdash; that inversion is the same mistake as reading a 95 per cent interval as a 95 per cent chance the true value sits inside it. It says nothing about magnitude, and it gets easier to satisfy as the sample grows &mdash; so a team that reports only significance will, given enough data, keep finding real and worthless results. The two failure modes are symmetrical and both are common: acting on a difference that was noise, and acting on a difference that was real and negligible.",
     "Two prompt variants are compared over 4,000 items. B beats A by 0.3 percentage points, comfortably significant at that sample size. It is also 0.3 percentage points, against a change that doubles the prompt length and therefore the cost of every call forever. The result is real and the decision is still no."),

    ("h2", "Two intervals that get confused, and only one is about your next case"),
    ("p", "An interval around a result can answer two different questions and the notation does not distinguish them. A <strong>confidence interval</strong> is about the average: run the experiment many times and the true mean lies inside it as often as the confidence level says. A <strong>prediction interval</strong> is about a single new observation: where the next case is likely to land. The second is always wider, often much wider, because it carries both the uncertainty in the estimate and the ordinary spread of the data."),

    ("know",
     "A confidence interval on the mean tells you nothing about how wrong you can be on one case.",
     "Anything making a decision per item &mdash; a per-request latency budget, a per-customer forecast, a per-document score threshold &mdash; is asking a prediction question, and a confidence interval answers a different one. The gap between them is not a technicality: as the sample grows, the confidence interval shrinks towards nothing while the prediction interval converges on the actual spread of the data and stays wide, because knowing the mean perfectly still does not tell you what the next draw will be.",
     "A model&#39;s mean response time is 400ms with a 95 per cent confidence interval of 390 to 410. It would be easy to promise a 500ms budget on that basis. The prediction interval is 180 to 1,300, because individual requests vary enormously, and roughly one request in twenty will breach the promise. The confidence interval was never evidence about individual requests."),

    ("h2", "Report the distribution per arm, not just the mean"),
    ("p", "A mean is one number standing in for a shape, and two arms with identical means can behave completely differently. The one that catches people is bimodality: a change that helps half the population and hurts the other half moves the mean not at all, and the summary reports success by reporting nothing."),

    ("terms", [
      ("Per-arm spread", "The minimum honest report",
       "Mean and standard deviation for each arm separately, not a single difference. Note what the spread does <em>not</em> tell you: heavily overlapping distributions can still have clearly distinguishable means, because distinguishability depends on the standard error and therefore on how many items you ran. The pairing figure above is exactly that case — the two piles overlap completely and B still beats A on every question."),
      ("The shape, not only the width", "Where bimodality hides",
       "Look at the distribution. A change that improved most cases slightly and broke a few badly has a mean that moved up and a tail that should stop the release."),
      ("Slices as arms", "The connection to Block 7",
       "Uneven capability loss under compression is this same problem: an aggregate that barely moves while one population degrades. Per-arm distribution and per-slice evaluation are the same instrument pointed at different questions."),
    ]),

    ("figure", "The same nine questions under two systems. Read down the columns and the systems look indistinguishable; read across each row and B wins almost every one. Pairing is the second reading.", '''<svg viewBox="0 0 640 216" role="img" aria-label="Unpaired and paired readings of the same eval data"><defs><marker id="pr" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" class="d-fill-accent"/></marker></defs>
<text x="14" y="22" class="d-label-b">unpaired: two piles</text>
<rect x="14" y="32" width="120" height="120" rx="6" class="d-box"/><text x="26" y="54" class="d-label-sm">A: 0.2 0.9 0.4</text><text x="26" y="74" class="d-label-sm">0.8 0.3 0.7</text><text x="26" y="94" class="d-label-sm">0.5 0.9 0.1</text><text x="26" y="126" class="d-label-sm">mean 0.53</text>
<rect x="146" y="32" width="120" height="120" rx="6" class="d-box"/><text x="158" y="54" class="d-label-sm">B: 0.3 1.0 0.5</text><text x="158" y="74" class="d-label-sm">0.9 0.4 0.8</text><text x="158" y="94" class="d-label-sm">0.6 1.0 0.2</text><text x="158" y="126" class="d-label-sm">mean 0.63</text>
<text x="14" y="176" class="d-label-sm">spread within each pile is huge,</text><text x="14" y="194" class="d-label-sm">so the gap drowns in it</text>
<text x="330" y="22" class="d-label-b">paired: nine differences</text>
<rect x="330" y="32" width="296" height="120" rx="6" class="d-box-accent"/>
<text x="342" y="54" class="d-label-sm">q1 +0.1   q2 +0.1   q3 +0.1</text>
<text x="342" y="74" class="d-label-sm">q4 +0.1   q5 +0.1   q6 +0.1</text>
<text x="342" y="94" class="d-label-sm">q7 +0.1   q8 +0.1   q9 +0.1</text>
<text x="342" y="126" class="d-label-b">every difference the same sign</text>
<text x="330" y="176" class="d-label-sm">question difficulty cancelled out,</text><text x="330" y="194" class="d-label-sm">leaving only the effect</text>
</svg>'''),

    ("h2", "Bessel's correction, and when it matters"),
    ("p", "Sample variance divides by <em>n − 1</em> rather than <em>n</em>, and the reason is that the mean was fitted to the same data. The sample mean is by definition the value that makes the squared deviations smallest, so deviations measured from it are systematically smaller than deviations from the true mean would be. Dividing by n inherits that and underestimates the spread. Subtracting one accounts for the single degree of freedom spent estimating the mean."),

    ("code", """true variance is 1.000 by construction

      n           divide by n         divide by n-1
      5        0.796 (-20.4%)        0.995 ( -0.5%)
     10        0.897 (-10.3%)        0.997 ( -0.3%)
     30        0.968 ( -3.2%)        1.002 ( +0.2%)
    100        0.989 ( -1.1%)        0.999 ( -0.1%)
   1000        0.999 ( -0.1%)        1.000 ( +0.0%)"""),

    ("callout", "warning", "The same ceiling fails in both directions, and both are silent",
     "<p>The evaluation material here treats a low output ceiling as the hazard: a reasoning model spends the budget thinking, returns an empty string, and scores as wrong. The mirror is just as real. Set the ceiling high and a turn that degenerates into repeating itself will consume the entire budget before stopping — in one observed case, 31,999 tokens of a 32,000 limit and forty-five minutes of wall clock, producing nothing, twice in a row.</p><p>So &ldquo;raise it&rdquo; is not the safe default and neither is &ldquo;lower it&rdquo;. The ceiling bounds the damage from a loop that has already gone wrong; it does not prevent the loop, and choosing it well means knowing which of the two failures you are currently exposed to.</p>"),

    ("callout", "matters", "It matters at eval sizes and nowhere else",
     "<p>At a thousand samples the correction is invisible and arguing about it is pedantry. At ten — which is the size of the eval sets in this course — dividing by n understates the variance by a tenth, and understating variance means overstating confidence in exactly the situation where you have least of it. The correction is free, so the habit is simply to use it and stop thinking about it.</p>"),

    ("h2", "A/B testing, and the peek that ruins it"),
    ("p", "An A/B test assigns real traffic randomly between arms and compares outcomes. It answers a question an offline eval cannot — how the change behaves for actual users on actual requests — and it comes with a discipline the offline version does not need, because the data arrives continuously and you can watch it."),

    ("terms", [
      ("Random assignment", "What makes the arms comparable",
       "Assign by a stable identifier so a user stays in one arm; assigning per request means the same person experiences both and the comparison is neither paired nor independent."),
      ("Sample size decided in advance", "Before any data arrives",
       "The measurement procedure already says write the number down before you run. Here it is load-bearing: without a pre-declared stopping point there is no such thing as a significant result."),
      ("One primary metric, plus guardrails", "Decided beforehand",
       "One metric decides the call. Guardrail metrics are the things that must not get worse — latency, cost, refusal rate — and they are checked but do not get to declare victory."),
      ("Peeking", "The failure that manufactures results",
       "Checking repeatedly and stopping when it looks significant. Every look is another chance for noise to cross the line, and noise eventually will."),
    ]),

    ("code", """both arms drawn from the SAME distribution — every 'significant'
result below is a false positive by construction

  tested once, at the planned sample size : 5.3%
  peeked 10 times, stopped when p<0.05    : 20.1%"""),

    ("p", "Every figure in this lesson comes from <code>notebooks/05-evaluation/01-is-the-difference-real.ipynb</code>, which runs these simulations with a fixed seed and no model, network or API key. If a number here looks convenient, run it."),

    ("know",
     "Peeking turned a five percent error rate into nearly twenty, on data with no effect in it at all.",
     "The nominal rate is what you agreed to accept when you chose the threshold. Stopping the moment a running experiment crosses it converts a single test into ten, and the chance that at least one of ten crosses by luck is far higher than the chance that one does. Nothing about the arithmetic of the individual test is wrong; the error is in how many times it was consulted.",
     "The first line of that output is also the instrument check. A test that did not land near five percent on data with no effect would have told me the implementation was broken before it told me anything about peeking."),

    ("callout", "pitfall", "A t-test is the wrong tool for a proportion",
     "<p>Most of this course's headline numbers are proportions — six of nine correct, twenty-four of twenty-four flagged. A t-test assumes roughly normal continuous measurements and binary outcomes at small n are neither. Use a test built for proportions, or a bootstrap, and be aware that at nine items almost nothing will be significant. Project 2 moving from five of nine to six of nine is a direction, not a result, and this course said so at the time on judgement rather than on arithmetic.</p>"),
    ("related", ["how-to-measure", "confounds-you-cannot-see", "one-set-many-models", "models-judging-models"]),
    ("quiz", [
      ("Why is an eval on a fixed question set paired?",
       ["Because the questions were written together",
        "Because each question is scored under both systems, so the two numbers have a natural one-to-one correspondence",
        "Because the same model family produced both sets of answers"],
       1),
      ("What does pairing remove from the comparison?",
       ["The measurement noise in each individual score",
        "Question difficulty — it affects both members of a pair equally, so subtracting one from the other cancels it",
        "The bias introduced by scoring order"],
       1),
      ("Why does sample variance divide by n − 1?",
       ["To make small samples appear more variable as a safety margin",
        "The mean was fitted to the same data, so deviations from it are systematically too small — one degree of freedom was spent estimating it",
        "It compensates for measurement error in the individual observations"],
       1),
      ("What is wrong with stopping an A/B test as soon as it looks significant?",
       ["The effect may not have stabilised yet",
        "Every look is another chance for noise to cross the threshold, which inflates the false-positive rate well past the nominal one",
        "Early data is biased toward more engaged users"],
       1),
    ]),
  ],
},
{
  "slug": "judging-a-conversation",
  "title": "Judging a Conversation",
  "subtitle": "Every score so far graded one answer. An agent produces a trajectory, and the failure is usually three turns back.",
  "body": [
    ("p", "Everything this block has measured is a single response to a single question: was it grounded, was it correct, did it refuse when it should. Block 4 builds systems that do not work that way. An agent takes a sequence of turns, each one conditioned on everything before it, and grading the last message tells you almost nothing about what happened."),

    ("h2", "Why the last turn is the wrong unit"),
    ("p", "A final answer can be right after a run that was expensive, circular and lucky, or wrong after a run that reasoned correctly and hit a tool that was down. Scoring only the ending scores the outcome and not the behaviour, and the behaviour is the thing you can improve."),

    ("terms", [
      ("The failure has a location", "And it is rarely the last turn",
       "A wrong final answer usually traces to a specific earlier step: a retrieval that returned nothing useful, a tool result misread, a plan abandoned. Grading the ending records that something went wrong and discards where."),
      ("Right for the wrong reasons", "The score a single turn cannot catch",
       "An agent that guessed, or that recovered from its own mistake by luck, produces the same final answer as one that worked correctly. On a single-turn metric they are indistinguishable, and only one of them will keep working."),
      ("Recovery is a property worth scoring", "Not just success",
       "Agents will hit failures. What separates a usable one is whether it notices and adapts. A trajectory that failed a tool call, read the error and tried something sensible is better than one that succeeded first time by luck, and a final-answer score ranks them the other way round."),
      ("Cost is part of the outcome", "Turns, tokens and calls",
       "Two runs reaching the same answer in three turns and in eleven are not equally good. This is the one dimension people do remember to record and then leave out of the judgement."),
    ]),

    ("know",
     "Score the trajectory, and the final answer is one dimension of it rather than the whole grade.",
     "The trace from Block 4 already contains what you need — every turn, every tool call, every result, the termination reason. Judging it as a sequence turns a pass or fail into a diagnosis, and the diagnosis is what tells you which of the loop, the tools, the prompt or the retrieval to fix. A single-turn score gives you a number that moves without telling you why, which is the position this course spent Block 5 arguing against.",
     "This is the same argument as measuring index recall, retrieval quality and groundedness separately rather than as one accuracy number. Separate the dimensions that fail independently, because they have different fixes."),

    ("figure", "The final answer is the last box. Everything that decides whether the run was any good happened before it, and a single-turn grade sees none of it.", '''<svg viewBox="0 0 640 194" role="img" aria-label="Grading a trajectory rather than a final answer"><defs><marker id="mt" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" class="d-fill-accent"/></marker></defs>
<rect x="14" y="42" width="104" height="42" rx="6" class="d-box"/><text x="26" y="62" class="d-label-sm">turn 1</text><text x="26" y="78" class="d-label-sm">retrieve</text>
<path d="M118 63 L146 63" class="d-arrow-accent" marker-end="url(#mt)"/>
<rect x="146" y="42" width="104" height="42" rx="6" class="d-box-accent"/><text x="158" y="62" class="d-label-sm">turn 2</text><text x="158" y="78" class="d-label-sm">wrong doc</text>
<path d="M250 63 L278 63" class="d-arrow-accent" marker-end="url(#mt)"/>
<rect x="278" y="42" width="104" height="42" rx="6" class="d-box"/><text x="290" y="62" class="d-label-sm">turn 3</text><text x="290" y="78" class="d-label-sm">retries</text>
<path d="M382 63 L410 63" class="d-arrow-accent" marker-end="url(#mt)"/>
<rect x="410" y="42" width="104" height="42" rx="6" class="d-box"/><text x="422" y="62" class="d-label-sm">turn 4</text><text x="422" y="78" class="d-label-sm">recovers</text>
<path d="M514 63 L542 63" class="d-arrow-accent" marker-end="url(#mt)"/>
<rect x="542" y="42" width="84" height="42" rx="6" class="d-box"/><text x="554" y="68" class="d-label-sm">answer</text>
<text x="146" y="112" class="d-label-sm">the fault is here</text>
<text x="410" y="112" class="d-label-sm">the merit is here</text>
<text x="542" y="112" class="d-label-sm">the grade is here</text>
<text x="14" y="152" class="d-label-sm">A single-turn score sees a correct answer and records a pass. It cannot see the wasted turns,</text>
<text x="14" y="172" class="d-label-sm">the wrong retrieval, or the recovery — which is the only part that predicts the next run.</text>
</svg>'''),

    ("h2", "What to score, and by what"),
    ("terms", [
      ("Deterministically, wherever possible",
       "Turn count, tool calls, cost, termination reason, guards fired",
       "None of this needs a judge. It is in the trace already, it is exact, and it catches a large share of what goes wrong. Exhaust it before reaching for a model, exactly as the grading ladder says."),
      ("Per-step, against the step's own job",
       "Did this retrieval return the right document?",
       "Each step has a checkable purpose. Scoring steps individually localises the failure, which is the whole point of doing this rather than grading the ending."),
      ("The trajectory as a whole",
       "Where a judge earns its place",
       "Was the sequence sensible, did it recover, did it go in circles? This is the genuinely open-ended part and the one worth a rubric — and the rubric lesson's rules apply unchanged, including blinding."),
    ]),

    ("callout", "pitfall", "A judge shown a whole trajectory will grade the ending",
     "<p>Hand a model a full transcript and ask how the run went, and it anchors on the final answer — a good ending makes the path look purposeful in hindsight. If you want the path judged, ask about the path specifically and separately: was any turn wasted, was the tool result read correctly, was the plan abandoned without reason. One question per property, or you get a summary of the outcome wearing a rubric.</p>"),

    ("callout", "matters", "Multi-turn state is where the eval set gets expensive",
     "<p>A single-turn set is a list of questions. A multi-turn set is a list of <em>situations</em> — a starting state, the turns so far, and often a scripted counterpart to play the other side. That is considerably more work to build and to keep correct, which is why most teams claim to test agents and actually test the last message. Start with a handful of realistic trajectories rather than a large set of shallow ones.</p>"),

    ("h2", "Where this connects"),
    ("p", "Block 4's telemetry lesson insisted the trace falls out of the loop for a few lines of code, and this is what it was for. The trace is not only for debugging an incident — it is the object you evaluate. A system with traces and no trajectory evaluation is recording the evidence and never reading it."),
    ("related", ["rubrics-and-blind-reads", "models-judging-models", "session-lifecycle", "loop-tradeoffs"]),
    ("quiz", [
      ("Why is the final answer a poor unit for grading an agent?",
       ["Final answers are often truncated by token limits",
        "It records that something went wrong and discards where — and cannot distinguish a correct answer reached by luck from one reached by working",
        "Agents frequently produce several candidate answers"],
       1),
      ("What should be scored deterministically before any judge is involved?",
       ["Whether the reasoning in each turn was sound",
        "Turn count, tool calls, cost, termination reason and which guards fired — all already in the trace, all exact",
        "Whether the final answer matches a reference"],
       1),
      ("What happens when a judge is shown a whole trajectory and asked how the run went?",
       ["It weights early turns too heavily because of position bias",
        "It anchors on the ending — a good final answer makes the path look purposeful in hindsight, so you get an outcome summary rather than a path judgement",
        "It runs out of context before reaching the final turn"],
       1),
    ]),
  ],
},
]
