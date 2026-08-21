TITLE = "Recipes, Decisions and Harnesses"
TOPIC = "engineering-practice"
ICON = "\U0001F9EA"
DESCRIPTION = "The three artifacts every serious LLM project accumulates — the harness it runs inside, the recipes it works by, the decisions it records — how they reinforce each other, how each one turns harmful, and how to measure whether any of it is true."
TAGS = ["ai", "practice", "evaluation", "agents"]
COLOR = "amber"
CREATED = "2026-08-21"
ID_BASE = "1787400000"

LESSONS = [
{
  "slug": "three-artifacts",
  "title": "Recipes, ADRs and the Harness",
  "subtitle": "Three things every LLM project grows, answering three different questions.",
  "body": [
    ("p", "Build an LLM system for more than a few weeks and you will accumulate three kinds of writing that are not code. They get confused constantly, including by people who write all three, because they overlap in subject matter. They do not overlap in <em>purpose</em>, and keeping them apart is what makes each one useful."),

    ("h2", "The three, and the question each answers"),
    ("terms", [
      ("The harness", "What the system does", "Prompts, tool definitions, loop control, budgets, the evaluation rig. Everything around the model. It is <em>executed</em>, so it is true by construction — whatever it says is what happens."),
      ("A recipe", "How you work", "A reusable method: the trigger that tells you it applies, the procedure, and a worked example. A runbook, a debugging protocol, an eval procedure. It is <em>followed</em>, so it is only as good as its first step."),
      ("An ADR", "Why it is this way", "An architecture decision record: the context that forced a choice, the choice, and the consequences accepted. It is <em>consulted</em>, so its value decays with the evidence that produced it."),
    ]),
    ("p", "The test for which one you are writing is simple. If a machine executes it, it is harness. If a person follows it step by step, it is a recipe. If someone reads it to understand why they can't do the obvious thing, it is an ADR."),

    ("h2", "They form a cycle, not a hierarchy"),
    ("figure", "Each artifact produces the evidence the next one needs. Break any edge and the other two drift.", '''<svg viewBox="0 0 660 320" role="img" aria-label="Cycle diagram: harness produces evidence, recipes interpret it, ADRs constrain the harness"><defs><marker id="ep1" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" class="d-fill-accent"/></marker></defs>
<rect x="250" y="20" width="170" height="66" rx="10" class="d-box-accent"/>
<text x="300" y="48" class="d-label-b">HARNESS</text>
<text x="266" y="68" class="d-label-sm">what the system does</text>
<rect x="30" y="210" width="180" height="66" rx="10" class="d-box"/>
<text x="80" y="238" class="d-label-b">RECIPES</text>
<text x="52" y="258" class="d-label-sm">how you find things out</text>
<rect x="450" y="210" width="180" height="66" rx="10" class="d-box"/>
<text x="510" y="238" class="d-label-b">ADRs</text>
<text x="466" y="258" class="d-label-sm">why it is this way</text>
<path d="M255 86 L150 210" class="d-arrow-accent" marker-end="url(#ep1)"/>
<path d="M225 250 L450 250" class="d-arrow-accent" marker-end="url(#ep1)"/>
<path d="M520 210 L410 86" class="d-arrow-accent" marker-end="url(#ep1)"/>
<text x="120" y="150" class="d-label-sm">produces traces</text>
<text x="120" y="166" class="d-label-sm">and numbers</text>
<text x="280" y="242" class="d-label-sm">a finding worth keeping</text>
<text x="280" y="290" class="d-label-sm">becomes a decision</text>
<text x="500" y="150" class="d-label-sm">constrains what</text>
<text x="500" y="166" class="d-label-sm">the harness may do</text>
</svg>'''),
    ("p", "The harness runs and produces evidence — traces, scores, failures. A recipe is what turns that evidence into a finding rather than an anecdote. A finding that will outlive the person who found it becomes an ADR. And the ADR constrains the next harness change, so the cycle closes."),

    ("h2", "A worked example, end to end"),
    ("p", "A local coding agent kept failing one benchmark task. It read the code, ran the failing tests, correctly derived the fix in its own reasoning — and then asked to read one more file. Every time. Nine different scaffolding changes were tried against it and none moved the number."),
    ("p", "The <strong>recipe</strong> that broke it open was a procedure, not an idea: <em>before running another experiment, confirm the harness is recording what the model said, then read one trace end to end.</em> It was not. Reasoning was being parsed off the API response and discarded on every turn that also called a tool — which was nearly all of them. Nine experiments had been run against a system that could not report on itself."),
    ("p", "With logging restored, the trace showed the model obeying the first line of its own system prompt: <em>“Before changing code, inspect the real repo structure and relevant files.”</em> That instruction has no exit criterion. There is always one more file. A compliant model can satisfy it forever without ever being wrong."),
    ("p", "The <strong>harness</strong> change was a deletion, and the <strong>ADR</strong> was the general rule that made the deletion obviously right rather than a guess: <em>prompts set direction, tools set limits.</em> A rule a machine can check belongs in the tool, where reading one file satisfies it permanently. A rule that cannot be checked belongs in the prompt, and must never be something the work waits on."),
    ("callout", "insight", "Why the ADR was worth writing", "Without it, the fix reads as “someone deleted a sentence from a prompt.” The next person adds it back, reasonably, because inspecting before editing is obviously good practice. The ADR is what makes the deletion survive."),

    ("h2", "The test for whether an ADR is doing work"),
    ("p", "A decision record earns its place when it stops a future change that would otherwise look sensible. If you cannot name the reasonable-seeming thing it forbids, you have written a status update."),
    ("links", [
      ('Documenting Architecture Decisions — Michael Nygard (2011)', 'https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions',
       'The original ADR write-up. Short, and still the clearest statement of what belongs in one.'),
      ('adr.github.io', 'https://adr.github.io/',
       'Templates and tooling that grew up around the idea.'),
      ('Building effective agents — Anthropic', 'https://www.anthropic.com/engineering/building-effective-agents',
       'On harness design: when a loop is warranted and when a fixed workflow beats one.'),
    ]),
    ("quiz", [
      ("You write down: “Retrieval uses BM25 plus embeddings, reranked. We rejected pure vector search because recall on exact identifiers was 41% worse.” Which artifact is this?",
       ["A recipe — it describes how the system works",
        "An ADR — it records a choice, the alternative rejected, and the evidence",
        "Harness — it defines what the system does at runtime"],
       1),
      ("Why does the ADR in the worked example matter more than the code change it justified?",
       ["Because deleting a prompt line is a large change that needs review",
        "Because without it, re-adding the instruction looks like good practice and the fix silently reverts",
        "Because ADRs are required before merging"],
       1),
      ("An instruction in a system prompt says “thoroughly review all relevant context before answering.” What is structurally wrong with it?",
       ["It is too vague for the model to parse",
        "It has no exit criterion — the model can never determine it has complied, so it can obey forever",
        "It should be phrased more politely"],
       1),
    ]),
  ],
},
{
  "slug": "when-scaffolding-turns",
  "title": "When the Scaffolding Turns on You",
  "subtitle": "Each of the three artifacts has a characteristic way of becoming actively harmful.",
  "body": [
    ("p", "All three artifacts are usually presented as unambiguous goods: write more docs, record more decisions, build more tooling. Each has a specific failure mode, and in each case the harmful version is <em>indistinguishable from the useful version at a glance</em>. That is what makes them worth teaching."),

    ("h2", "The harness talks to the model, and can lie to it"),
    ("p", "A harness is usually debugged as though it were ordinary software: does it crash, does it return the right value. But an agent harness has a second output almost nobody audits — <strong>everything it says to the model</strong>. Tool results, error messages, injected guidance, the prompt itself. All of it is text the model reasons from, and none of it is covered by your tests."),
    ("p", "Five defects found in one afternoon in a single production agent harness, none of which failed a test, threw an exception, or appeared in any metric:"),
    ("terms", [
      ("“You already read this file”", "False", "The dedup key was the file path and ignored the requested line range. The model was paging a long file — the only way to read it — and every page after the first was reported as a repeat. It fired 21 times in one run, against 3 firings for every other message combined."),
      ("“Before changing code, inspect”", "Unsatisfiable", "No exit criterion. A compliant model obeys it indefinitely."),
      ("“[clipped: original bytes 68671]”", "True but unactionable", "Tool results were clipped to a character budget, head-only. The read tool put “read again from line N” at the end of its output, so the one actionable sentence was always the first thing cut."),
      ("“Its edits are already on disk”", "False", "Said to the second attempt regardless of whether the first had written anything. When the first wrote nothing, the second opened by hunting for work that never happened — and said so in its reasoning."),
      ("“…use search to explore”", "True, wrongly placed", "Appended last, in the highest-recency position, directly after a message demanding an immediate edit."),
    ]),
    ("callout", "warning", "The general form", "Not one of these was a logic bug. Every one was <em>speech</em> — the harness saying something to the model that was false, unsatisfiable, or true-but-useless. If your harness generates text the model reads, that text is part of your system and needs the same scrutiny as a return value."),
    ("p", "The sharpest version of this: a harness can <strong>suppress a capability the model already has</strong>. The failure then looks exactly like a model limitation, and every reasonable next step — a bigger model, more turns, better retrieval — is aimed at the wrong thing."),

    ("h2", "A recipe with a stale first step is worse than no recipe"),
    ("p", "A recipe's value is concentrated in its <em>first</em> instruction, because that is the one followed under pressure by someone who does not yet understand the problem. A first step that points the wrong way does not merely waste time; it lends institutional authority to the wrong hypothesis."),
    ("p", "A real triage table entry read: <em>“Model reads forever, never edits → count reads versus edits → the lever is the read budget.”</em> Four sections below, the same document listed that budget as its own worst tarpit — eleven separate commits of tuning it, with a stated lesson that tuning it for one model breaks another. The recipe was sending every reader straight to the lever the document itself said not to reach for."),
    ("callout", "matters", "The asymmetry", "A missing runbook makes you think. A confidently wrong runbook makes you stop thinking, at exactly the moment you were about to. Audit the first step of every recipe you own more often than the rest of it."),

    ("h2", "ADRs ossify"),
    ("p", "An ADR records a decision <em>and the evidence that forced it</em>. The decision persists in the document; the evidence decays in the world. When the two separate, the ADR becomes a rule enforced past its reason — and because it is written down and was once correct, it is unusually hard to argue with."),
    ("p", "One agent project spent months describing itself as a <em>cascader</em>: a system that tries a local model and escalates to progressively larger ones. That was a genuine, well-reasoned decision. Measurement later falsified the premise it rested on, and the project became a local agent that occasionally escalates. The architecture docs kept saying cascader, so new work kept being designed against a system that no longer existed."),
    ("terms", [
      ("Retrospective justification", "The common one", "An ADR written after the fact to legitimise a choice already made. It reads identically to a real one and contains no decision."),
      ("Consequence amnesia", "The costly one", "The “consequences” section is where an ADR states what it is giving up. Teams write it, then never re-read it when that cost starts being paid."),
      ("Status theatre", "The wasteful one", "Every change gets an ADR, so nothing is signal. If it does not forbid a sensible-looking future change, it is not a decision."),
    ]),

    ("h2", "The unifying diagnosis"),
    ("p", "All three failures share a shape: <strong>an artifact that was true when written, still asserting itself after its truth expired.</strong> The harness message that was accurate before the file grew. The recipe step that was right before the lever was exhausted. The ADR that was correct before the measurement came back."),
    ("p", "Which is why none of the three is self-correcting, and why the next lesson is about the only thing that corrects them."),
    ("h2", "The size of the harness effect, measured"),
    ("p", "This is usually asserted and rarely quantified, so here it is with numbers. SWE-bench Verified is 500 real GitHub issues. These five submissions all run <strong>the same model</strong> — <code>claude-3-5-sonnet-20241022</code> — and differ only in the scaffolding around it:"),

    ("figure", "Same model, same 500 tasks, five harnesses. The spread is 80 tasks — 16 percentage points — and none of it is model capability.", '''<svg viewBox="0 0 640 210" role="img" aria-label="SWE-bench Verified scores for one model across five scaffolds">
<text x="12" y="18" class="d-label-sm">claude-3-5-sonnet-20241022 on SWE-bench Verified (500 tasks), by scaffold</text>
<line x1="228" y1="32" x2="228" y2="182" stroke="var(--border)" stroke-width="1"/>
<rect x="228" y="34" width="148" height="22" rx="3" class="d-fill-red" opacity="0.55"/>
<text x="12" y="50" class="d-label-sm">AutoCodeRover v2.0</text><text x="386" y="50" class="d-label-sm">231 · 46.2%</text>
<rect x="228" y="64" width="157" height="22" rx="3" class="d-fill-muted" opacity="0.6"/>
<text x="12" y="80" class="d-label-sm">Tools</text><text x="395" y="80" class="d-label-sm">245 · 49.0%</text>
<rect x="228" y="94" width="163" height="22" rx="3" class="d-fill-muted" opacity="0.6"/>
<text x="12" y="110" class="d-label-sm">Agentless 1.5</text><text x="401" y="110" class="d-label-sm">254 · 50.8%</text>
<rect x="228" y="124" width="165" height="22" rx="3" class="d-fill-accent" opacity="0.7"/>
<text x="12" y="140" class="d-label-sm">AutoCodeRover v2.1</text><text x="403" y="140" class="d-label-sm">258 · 51.6%</text>
<rect x="228" y="154" width="199" height="22" rx="3" class="d-fill-green" opacity="0.85"/>
<text x="12" y="170" class="d-label-sm">CodeStory + swe-search</text><text x="437" y="170" class="d-label-sm">311 · 62.2%</text>
<path d="M470 45 L470 165" stroke="var(--yellow)" stroke-width="1.6" stroke-dasharray="4 4"/>
<text x="480" y="98" class="d-fill-yellow" font-size="11" font-weight="600">80 tasks of</text>
<text x="480" y="114" class="d-fill-yellow" font-size="11" font-weight="600">pure harness</text>
</svg>'''),

    ("callout", "matters", "What this licenses you to say", "A sixteen-point spread on identical model weights. If you swapped models and saw a gain that size you would call it a generational leap — here it is entirely scaffolding. Note also AutoCodeRover v2.0 to v2.1: the same team, the same model, 231 tasks to 258, from harness work alone. When something underperforms, the harness is the higher-yield place to look, and this is the evidence for it rather than the intuition."),

    ("callout", "pitfall", "Read it carefully, though", "These submissions differ in more than scaffold — different prompts, retrieval, retry budgets and token spend. The spread is an upper bound on what harness work can buy, not a controlled experiment. It tells you the harness matters enormously; it does not tell you which harness change is responsible. That distinction is the whole of the next two lessons."),

    ("links", [
      ('SWE-bench', 'https://www.swebench.com/',
       'Agentic coding benchmark. Compare leaderboard entries that share a model but differ in scaffold — the spread is the harness effect.'),
      ('SWE-bench experiments — raw submissions', 'https://github.com/swe-bench/experiments',
       'Where the numbers above come from: every submission\'s resolved-task list under evaluation/verified/. Recompute them yourself rather than trusting this lesson.'),
      ('Building effective agents — Anthropic', 'https://www.anthropic.com/engineering/building-effective-agents',
       'Argues for the simplest scaffold that works, partly because scaffolding is where these failures hide.'),
    ]),
    ("quiz", [
      ("An agent harness returns “(no matches)” from its search tool when the query was case-sensitive and the file used different casing. Why is this worse than an error?",
       ["It isn't — an empty result is honest",
        "“No matches” is indistinguishable from a true negative, so the model correctly concludes the code doesn't exist and stops looking",
        "It wastes a turn"],
       1),
      ("Your triage doc's first step for a symptom points at a fix that has failed eleven times. What is the cost?",
       ["Some wasted time, but the reader will figure it out",
        "The doc lends authority to the wrong hypothesis at the moment the reader is least able to challenge it",
        "None, as long as the rest of the doc is correct"],
       1),
      ("Which of these is the strongest sign an ADR has ossified?",
       ["It is more than a year old",
        "The measurement that justified it has since been contradicted, but the document still reads as current",
        "It was written by someone who has left"],
       1),
    ]),
  ],
},
{
  "slug": "why-measurement-decides",
  "title": "Why Measurement Decides",
  "subtitle": "The only thing that corrects a harness, a recipe or a decision is a number that disagrees with it.",
  "body": [
    ("p", "Everything in the previous lesson failed the same way: an artifact stayed confident after its truth expired. None of the three can notice this about itself. A harness cannot tell you its own message is misleading; a recipe cannot tell you its first step is stale; an ADR cannot tell you its evidence was overturned. Only a measurement can."),

    ("h2", "Plausible mechanisms are not findings"),
    ("p", "The failure mode is not laziness. It is the opposite — it is a good engineer reasoning carefully from a mechanism that makes sense, and shipping it. Some real examples, each of which sounded correct and was wrong:"),
    ("terms", [
      ("“Mean-centering will sharpen the router”", "Regressed, twice", "Standard practice for embedding similarity. Accuracy fell from 88% to 70% on the first attempt and 92% to 66% on the second."),
      ("“More exemplars will help classification”", "Regressed", "True only when paired with a different aggregation method. Alone, it made things worse."),
      ("“This model class can\u2019t drive tool loops”", "False", "A property of one model-and-runtime combination, generalised into a law that shaped months of architecture."),
      ("“The cheap tier is weak at agentic work, skip it”", "False", "It edited fine. The harness was strangling it with a read budget tuned for a different model."),
    ]),
    ("callout", "warning", "The rule that falls out of this", "If you are about to write “this should improve X”, stop and write the measurement that would prove it instead. The sentence is the same length. One of them can be wrong without anyone noticing."),

    ("h2", "The instrument lies before the result does"),
    ("p", "There is a failure worse than a wrong conclusion: a conclusion drawn from an instrument that cannot distinguish success from doing nothing. It produces confident numbers, they move when you change things, and every one of them is noise."),
    ("p", "A benchmark of eight coding tasks was used for months to decide model and architecture questions. An audit found that <strong>six of the eight passed their own verification at the starting commit</strong> — before any work was done. The tests that proved the feature had been added by the very change the agent was being asked to reproduce, so they were absent at the start, so the test suite passed vacuously. An agent that edited nothing scored the same as one that solved the task."),
    ("p", "Every architectural conclusion drawn from that board had to be thrown out, including a headline result that a whole escalation mechanism produced zero benefit. It produced zero <em>measured</em> benefit, because the instrument could not see benefit."),
    ("figure", "An honest fixture must fail before the work and pass after it. Fail either half and the instrument cannot tell the two columns apart.", '''<svg viewBox="0 0 640 240" role="img" aria-label="Diagram of the two honesty invariants for a test fixture"><rect x="30" y="40" width="250" height="70" rx="8" class="d-box"/><text x="52" y="68" class="d-label-b">At the starting commit</text><text x="52" y="90" class="d-label-sm">feature absent \u2192 verify MUST FAIL</text><rect x="360" y="40" width="250" height="70" rx="8" class="d-box"/><text x="382" y="68" class="d-label-b">With the known-good fix</text><text x="382" y="90" class="d-label-sm">feature present \u2192 verify MUST PASS</text><rect x="30" y="150" width="580" height="60" rx="8" class="d-box-accent"/><text x="52" y="176" class="d-label-b">If either half is untrue</text><text x="52" y="196" class="d-label-sm">“did nothing” and “solved it” score identically, and every number the instrument produces is noise</text></svg>'''),

    ("h2", "Two kinds of honesty"),
    ("p", "The invariant above is <strong>outcome honesty</strong> — can the instrument tell success from inaction? There is a second one, checked far less often. <strong>Process honesty</strong>: did the instrument record what the system actually did and said, or only whether it succeeded?"),
    ("p", "Two completely different failures score identically under outcome metrics alone:"),
    ("terms", [
      ("Never understood the task", "edit_attempted = false", "Needs better grounding, retrieval, or task framing."),
      ("Understood it and would not act", "edit_attempted = false", "Needs a prompt or tool change. Grounding is already fine, and every grounding fix will measure flat."),
    ]),
    ("p", "In the case that opened this module, nine consecutive experiments were run against the second failure using fixes aimed at the first — because the reasoning that would have distinguished them was being parsed off the API response and discarded on every tool-calling turn. One trace, once logging was restored, answered what nine experiments had not."),
    ("callout", "insight", "The older name for this", "Reading what a subject says while working, rather than only scoring the outcome, is <strong>think-aloud protocol analysis</strong> — formalised by Ericsson and Simon in the 1980s for human problem-solving. The machine-learning analogue is the distinction between <em>process supervision</em> and <em>outcome supervision</em>: scoring the steps rather than the final answer."),
    ("callout", "warning", "And the caveat that keeps it honest", "Verbalised reasoning is evidence, not ground truth. A model\u2019s stated chain of thought does not always reflect the computation that produced its answer, so a trace can be sincere and still misleading. Treat it as a witness statement: extremely valuable, independently checkable, occasionally wrong."),

    ("links", [
      ('Let\u2019s Verify Step by Step (Lightman et al., 2023)', 'https://arxiv.org/abs/2305.20050',
       'The process- versus outcome-supervision result: step-level feedback outperforms final-answer feedback.'),
      ('Protocol Analysis: Verbal Reports as Data \u2014 Ericsson & Simon', 'https://mitpress.mit.edu/9780262550239/protocol-analysis/',
       'The human-factors ancestor. Worth knowing that this method is forty years old before presenting it as new.'),
    ]),
    ("quiz", [
      ("Your eval score improves 12 points after a change. What is the first thing to check?",
       ["Whether the improvement holds at n=3",
        "Whether the instrument fails at the starting state — an eval that passes before the work cannot measure the work",
        "Whether the change is fast enough for production"],
       1),
      ("An agent scores edit_attempted=false on a task. What does that tell you about the cause?",
       ["The model lacked the capability",
        "Almost nothing — it cannot distinguish “never understood” from “understood and would not act”, which need opposite fixes",
        "The task was too hard"],
       1),
      ("Why is a model's stated reasoning still worth logging, given it may not reflect the real computation?",
       ["It is guaranteed to be accurate for reasoning models",
        "It is checkable evidence you otherwise do not have — and its absence guarantees you are guessing",
        "It improves the model's accuracy"],
       1),
    ]),
  ],
},
{
  "slug": "how-to-measure",
  "title": "How to Measure",
  "subtitle": "A procedure you can run on any change to an LLM system, in order, where every step is worthless before the one above it.",
  "body": [
    ("p", "This is deliberately a sequence rather than a checklist. Each step assumes the previous one passed, and running them out of order is how you get numbers that look rigorous and mean nothing."),

    ("h2", "0 · Prove the instrument before you trust it"),
    ("p", "Both honesty invariants, checked <em>before</em> the experiment, not after the results confuse you."),
    ("terms", [
      ("Outcome honesty", "Can it tell success from inaction?", "At the starting state the check must FAIL. With the known-good change applied it must PASS. Run both directions explicitly — a vacuous pass is invisible otherwise."),
      ("Process honesty", "Did it record what happened?", "Confirm the harness logs the model\u2019s reasoning and its tool arguments, then read one full trace end to end. Absence of an explanation in the log is not evidence there was none."),
    ]),
    ("callout", "matters", "Instrumentation is free; treatments are not", "Adding logging leaves the request to the model byte-identical, so it cannot change the result and needs no flag or A/B. Anything that changes what the model <em>sees</em> is a treatment and must be measured. Keeping this line sharp is what lets you fix your observability mid-investigation without invalidating it."),

    ("h2", "1 · Write the number down before you run"),
    ("p", "State the hypothesis as a prediction with a value: <em>“this should take edit-attempt rate from 0.25 to above 0.5.”</em> A hypothesis that predicts no particular number cannot be wrong, and one that cannot be wrong is not being tested. Written afterwards, any result confirms it."),

    ("h2", "2 · Baseline, whole set, repeats"),
    ("terms", [
      ("Against a baseline", "Change off, same conditions", "A number with nothing to compare to is a measurement of your setup, not your change."),
      ("The whole set", "Never one case", "One case has proved +1.00 where the full set said +0.00. Cherry-picking does not require dishonesty, only relief."),
      ("At least three repeats", "These systems are stochastic", "Report mean and spread, not a single run."),
      ("Read the interval, not the fraction", "1-of-3 is not a result", "At n=3, “1 of 3 versus 0 of 3” sits comfortably inside noise. Compute a credible interval and look at its width before claiming anything."),
    ]),

    ("h2", "3 · One treatment at a time \u2014 or a screen, knowingly"),
    ("p", "Four changes shipped together give one number and no attribution. The disciplined default is one variable per run."),
    ("p", "There is one legitimate exception, and it must be a deliberate choice rather than a shortcut: a <strong>screening run</strong>. Bundle everything, run once, and use the result as a gate. A null is highly informative — four independent fixes together failed to move a binary outcome, so the cause is elsewhere — and you learned that for one run instead of four. A positive earns you the budget to bisect. What you must not do is bundle for speed and then report the win as though you knew which change caused it."),

    ("h2", "4 · Pick a guardrail before you look"),
    ("p", "Name in advance the metric that must <em>not</em> get worse, and the threshold that rejects the change even if the primary metric improves. Chosen afterwards, a guardrail is a rationalisation. A faster agent that introduces more broken builds is not a better agent, and you will not notice unless you decided to look."),

    ("h2", "5 · Revert the fix"),
    ("p", "When something improves, put the old behaviour back and confirm the number falls again. This catches the case where the improvement came from something else you changed in the same window — a cache reset, a restarted server, a different machine load. It is the cheapest step here and the most often skipped."),
    ("callout", "insight", "Control the machine too", "For anything timing-sensitive, run one known case first and last. If the bookends disagree by more than about a third, the whole grid is void — the machine changed under you. A clean-looking finding about context-length limits was once refuted by exactly this: performance had decayed across the session, not at any threshold."),

    ("h2", "The short version"),
    ("terms", [
      ("Before", "Instrument honest? Prediction written with a number? Baseline defined? Guardrail named?", "All four, or do not start."),
      ("During", "Whole set, n \u2265 3, one variable, machine bookended.", "Deviations are fine if you say so in the result."),
      ("After", "Interval not fraction. Guardrail checked. Fix reverted and the number moved back.", "Then it is a finding, and only then does it belong in a recipe or an ADR."),
    ]),
    ("callout", "matters", "Why this belongs in a module about documentation", "A recipe or an ADR built on an unmeasured result does not just fail \u2014 it hardens. It gets cited, followed, and defended long after the thing it claims was quietly falsified. Measurement is not a separate discipline from writing things down; it is the thing that earns you the right to."),

    ("links", [
      ('SWE-bench', 'https://www.swebench.com/',
       'Useful for the exercise below: find two leaderboard entries with the same base model and different scaffolds.'),
      ('Building effective agents \u2014 Anthropic', 'https://www.anthropic.com/engineering/building-effective-agents',
       'On keeping the scaffold small enough that you can still attribute a result to it.'),
    ]),
    ("quiz", [
      ("You ship four prompt fixes together and the score improves. What may you claim?",
       ["That all four helped",
        "That the bundle helped, and nothing about which fix did it, unless you bisect",
        "That the largest of the four was responsible"],
       1),
      ("Why revert a fix that appears to have worked?",
       ["To confirm the code is reversible",
        "To rule out that something else changed in the same window — a cache, a restart, machine load",
        "It is only needed for performance work"],
       1),
      ("A screening run of five bundled changes comes back null. What have you learned?",
       ["Nothing — the run was wasted",
        "Something valuable: none of the five is sufficient even together, so the cause is elsewhere — learned in one run instead of five",
        "That the changes should be tried individually anyway"],
       1),
    ]),
  ],
},
{
  "slug": "swe-bench-and-how-to-run-it",
  "title": "SWE-bench, and How to Actually Run It",
  "subtitle": "The benchmark behind the numbers in lesson 2 — how it is built, how to run it, and what it does not tell you.",
  "body": [
    ("p", "Lesson 2 used SWE-bench to show a sixteen-point spread from scaffolding alone. This lesson is how that benchmark works and how to run it yourself — partly because it's the standard for agentic coding, and mostly because its design is the clearest worked example of the measurement discipline in lessons 3 and 4."),

    ("h2", "What a task actually is"),
    ("p", "Each instance is a real GitHub issue and the real pull request that closed it. The system under test gets the repository at the commit <em>before</em> the fix, plus the issue text. It must produce a patch. Nothing else."),
    ("terms", [
      ("repo + base_commit", "The starting state", "The repository exactly as it stood before anyone fixed this."),
      ("problem_statement", "The issue text", "What a human maintainer was given. Often incomplete, sometimes misleading — which is the point."),
      ("FAIL_TO_PASS", "The tests that must start passing", "Drawn from the real PR's tests. These fail at base_commit and pass after the genuine fix."),
      ("PASS_TO_PASS", "The tests that must keep passing", "Everything already green. This is what stops 'delete the failing test' from scoring."),
      ("patch / test_patch", "The reference answer", "Held back during the run and used only to validate the fixture."),
    ]),

    ("callout", "insight", "Look at what that pair of test sets is doing", "FAIL_TO_PASS and PASS_TO_PASS together are exactly the instrument invariant from lesson 3, implemented. The task must fail before the work and pass after it, and the system must not break anything else to get there. An agent that changes nothing fails FAIL_TO_PASS; an agent that guts the suite fails PASS_TO_PASS. Doing nothing and solving it cannot score the same. Most homemade benchmarks omit the second half and quietly reward vandalism."),

    ("h2", "The four variants, and which number people quote"),
    ("terms", [
      ("SWE-bench", "2,294 test instances", "The full set, twelve Python repositories. Plus a 225-instance dev split."),
      ("SWE-bench Lite", "300 instances", "Filtered toward self-contained problems. Cheaper to run, easier — do not compare its scores to the others."),
      ("SWE-bench Verified", "500 instances", "Human-validated with OpenAI Preparedness to remove tasks that were underspecified or impossible. This is the number almost everyone reports, including lesson 2."),
      ("Multimodal / Multilingual", "Beyond Python", "Multimodal keeps its test split private and is graded through a cloud CLI — a deliberate defence against contamination."),
    ]),
    ("callout", "pitfall", "The comparison people get wrong", "A Lite score and a Verified score are not the same measurement, and neither is comparable to the full set. If a vendor quotes 'SWE-bench' without saying which, the number is uninterpretable. Ask. This is lesson 4's step 1 — write down what you are measuring before you run — applied to reading someone else's claim."),

    ("h2", "Running it"),
    ("p", "Evaluation is Docker-based: each instance gets a container with the repo and its dependencies at the right commit. That's the only way per-repo environments stay reproducible, and it's why the harness needs real memory and disk."),
    ("code", """git clone git@github.com:SWE-bench/SWE-bench.git
cd SWE-bench && pip install -e ."""),
    ("p", "Then the step almost everyone skips — <strong>validate the fixture before trusting any result</strong> by running the reference patches through it:"),
    ("code", """# grade the known-good answer: this MUST resolve
swebench eval verified --gold -i sympy__sympy-20590 --run-id validate-gold"""),
    ("callout", "warning", "On Apple Silicon, add --namespace ''", "The harness pulls prebuilt Linux images from DockerHub by default. On an M-series Mac you want <code>--namespace ''</code> so images build locally instead. Expect this to be slow the first time and to want real disk — a full Verified run builds hundreds of containers. Build them ahead with <code>swebench images build verified -j 8</code>."),
    ("p", "Your own run takes a predictions file — one patch per instance — and reports a resolve rate:"),
    ("code", """swebench eval verified -p predictions.jsonl --run-id my-run-01 -j 8

# re-grade saved logs later without rebuilding any containers
swebench report my-run-01 -d verified"""),

    ("h2", "What the score does and doesn't mean"),
    ("p", "The headline is <strong>resolve rate</strong>: the fraction of instances where FAIL_TO_PASS passed and PASS_TO_PASS held. It is a genuinely honest metric — machine-checkable, no judge model, no partial credit for looking plausible. It is also narrower than it reads."),
    ("ul", [
      "<strong>Resolved is not correct.</strong> A patch that passes the tests may still be wrong in ways the tests don't cover. The tests are the ones that shipped, not an exhaustive spec.",
      "<strong>Contamination is real.</strong> These are public repositories and the issues predate most training cutoffs. Some fixes are memorised rather than derived. Verified reduces bad tasks; it cannot remove this.",
      "<strong>Hints leak.</strong> Some issue text contains most of the solution. That's faithful to real life and it means the benchmark measures a mix of reasoning and reading.",
      "<strong>Python, twelve repos.</strong> Performance here does not transfer automatically to your Go service or your TypeScript frontend.",
      "<strong>The harness dominates more than you expect.</strong> Which is lesson 2's point, and the reason a leaderboard entry describes a scaffold at least as much as a model.",
    ]),

    ("h2", "The part that actually applies to your work"),
    ("p", "You are unlikely to need a SWE-bench number. You are very likely to need a benchmark for <em>your</em> repository, and SWE-bench is the design worth copying — because your merged pull requests are already labelled data."),
    ("terms", [
      ("1 · Mine closed PRs", "That fixed something and touched tests", "The issue is the prompt, the merge commit's parent is the base, the PR is the reference answer."),
      ("2 · Derive both test sets", "Fail-to-pass and pass-to-pass", "Run the suite at base to find what fails; everything else must stay green."),
      ("3 · Validate with gold", "Reference patch must resolve", "If it doesn't, the fixture is broken and every later number is noise."),
      ("4 · Freeze the set", "Then leave it alone", "Its value comes from staying fixed. Edit it between runs and it measures nothing."),
      ("5 · Hold some back", "Never tune against all of it", "Tuning a scaffold against every task is leakage by hand."),
    ]),
    ("callout", "matters", "Why this beats the public number for you", "A benchmark built from your own merged PRs is in your language, your codebase, your conventions, and nobody has optimised against it. It is the twenty-item rule from the eval-battery lesson, applied to code, and it is what a replay harness does — running real closed pull requests so the outcome is established before the agent starts, which makes its self-report irrelevant."),

    ("links", [
      ('SWE-bench', 'https://www.swebench.com/',
       'Leaderboards for each variant. Read which variant a number refers to before comparing anything.'),
      ('SWE-bench on GitHub', 'https://github.com/SWE-bench/SWE-bench',
       'The harness, the CLI shown above, and the dataset definitions.'),
      ('Introducing SWE-bench Verified — OpenAI', 'https://openai.com/index/introducing-swe-bench-verified/',
       'How the 500 were validated, and what was wrong with the tasks removed.'),
      ('SWE-bench experiments — raw submissions', 'https://github.com/swe-bench/experiments',
       "Every submission's resolved-task list. The source of lesson 2's numbers, and recomputable yourself."),
    ]),

    ("quiz", [
      ("What stops a SWE-bench agent from scoring by deleting the failing test?",
       ["A human reviews every patch",
        "PASS_TO_PASS — the tests that were already green must stay green",
        "The patch is diffed against the reference answer"], 1),
      ("A vendor reports '62% on SWE-bench'. What must you ask first?",
       ["Which model they used",
        "Which variant — Lite, Verified and the full set are not comparable measurements",
        "How many samples they averaged over"], 1),
      ("Why run the harness against the reference patches (--gold) before your own predictions?",
       ["To warm the Docker image cache",
        "To confirm the fixture actually resolves a known-good patch — if it can't, every later number is noise",
        "It's required before submitting to the leaderboard"], 1),
      ("Why is a benchmark built from your own merged PRs more useful to you than a SWE-bench score?",
       ["It's larger and more statistically rigorous",
        "It's in your language and codebase, and nobody has optimised against it",
        "It avoids the need for Docker"], 1),
    ]),
  ],
},
{
  "slug": "confounds-you-cannot-see",
  "title": "Confounds You Cannot See",
  "subtitle": "The limits, overrides and truncations that end a run silently — and get read as capability.",
  "body": [
    ("p", "Lesson 3 asked whether your instrument can tell success from inaction. This lesson is about the layer beneath that: whether anything <em>else</em> ended the run, and whether you would know."),
    ("p", "The failure has a shape. A run stops early. The output shows no error. You attribute the result to the model — because the model is the only component you were thinking about — and you design your next experiment against that attribution. Then you do it eight more times."),

    ("callout", "matters", "The definition worth memorising", "<strong>A limit that can end a run and cannot be seen is not a guard, it is a confound.</strong> The distinction isn't whether the limit is reasonable — most of them are. It is whether its firing appears anywhere in the output you read afterwards. An invisible guard doesn't just stop the run; it stops it while looking exactly like the thing you were trying to measure."),

    ("h2", "A worked case: six mechanisms, one symptom"),
    ("p", "Nine runs of a local coding agent on one issue produced zero edits. The obvious reading was that the model wouldn't commit a change. The runs were in fact terminated by <strong>six different mechanisms</strong>, none of which appeared in the output:"),
    ("terms", [
      ("A read-budget nudge", "set to 3 by a task classifier", "Fired before the model reached the edit."),
      ("A phase transition", "clamped the pre-edit limit to 4", "Silently overwrote the operator's setting."),
      ("Decomposition", "reassigned the nudge to 3 for the rest of the run", "A third writer to the same number."),
      ("A whole-run wall clock", "separate from the per-call timeout", "Nothing in the log named it when it fired."),
      ("The wrong model", "the flag used a different config key", "Six runs credited to a 30B were served by a 9B."),
      ("A nil verifier", "one config default was false", "Which disabled turn-end verification, the fix-attempt loop and per-edit feedback at once."),
    ]),
    ("p", "Every one of those presents identically as \"the model won't commit an edit\". Two of them aren't even about the model — one is a clock, one is a routing bug that meant the measured system was never the system under test."),

    ("figure", "The same observation is consistent with every branch. Nothing in the output distinguishes them, so the reading defaults to whichever component you were already thinking about — which is the model.", '''<svg viewBox="0 0 640 220" role="img" aria-label="One symptom consistent with many hidden causes"><defs><marker id="ca" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" class="d-fill-muted"/></marker></defs>
<rect x="12" y="90" width="150" height="44" rx="7" class="d-box-warn"/>
<text x="26" y="112" class="d-label-b">zero edits</text>
<text x="26" y="128" class="d-label-sm">observed</text>
<path d="M162 100 L214 30" class="d-arrow" marker-end="url(#ca)"/>
<path d="M162 106 L214 66" class="d-arrow" marker-end="url(#ca)"/>
<path d="M162 112 L214 106" class="d-arrow" marker-end="url(#ca)"/>
<path d="M162 118 L214 146" class="d-arrow" marker-end="url(#ca)"/>
<path d="M162 124 L214 186" class="d-arrow" marker-end="url(#ca)"/>
<rect x="214" y="14" width="200" height="30" rx="5" class="d-box"/><text x="226" y="34" class="d-label-sm">read budget fired at 3</text>
<rect x="214" y="52" width="200" height="30" rx="5" class="d-box"/><text x="226" y="72" class="d-label-sm">wall clock expired</text>
<rect x="214" y="90" width="200" height="30" rx="5" class="d-box"/><text x="226" y="110" class="d-label-sm">wrong model served</text>
<rect x="214" y="128" width="200" height="30" rx="5" class="d-box"/><text x="226" y="148" class="d-label-sm">verifier nil, feedback off</text>
<rect x="214" y="166" width="200" height="30" rx="5" class="d-box-accent"/><text x="226" y="186" class="d-label-sm">the model genuinely refused</text>
<text x="432" y="186" class="d-accent">← the only one you tested</text>
</svg>'''),

    ("h2", "An override that runs before the thing it overrides is not an override"),
    ("p", "Two attempts to loosen that read budget did nothing while reporting success. Both were applied early and then overwritten — once by a phase-transition clamp, once by the task classifier. Both times the environment said 30 and the log printed 3, and both times the flat result was read as a model failure."),
    ("callout", "insight", "Setting a knob and proving it engaged are two different acts", "The fix is not a better default. It is that the effective value must be printed after everything that can write to it, and operator overrides must be applied last. If your experiment turns a dial, your output must show the dial's final position — otherwise a null result is ambiguous between \"the treatment doesn't work\" and \"the treatment never happened\"."),

    ("h2", "Truncation manufactures conclusions"),
    ("p", "A separate episode: three consecutive tests concluded that a model architecture could not reuse its cache. All three ran with an output budget so small that the model was cut off mid-thought. The fragment fed into the next turn could never match what was cached — guaranteeing the observed failure for a reason that had nothing to do with architecture. Raising the budget so the turn actually completed flipped the same test."),
    ("p", "The general form: <strong>a limit that truncates the thing being measured contaminates everything downstream of it.</strong> Output budgets, context windows, tool-result clipping, log rotation. Any of them can quietly convert your experiment into a measurement of the limit."),
    ("callout", "pitfall", "The dangerous version is when the story is good", "That architecture conclusion was plausible. There was a mechanism, it was consistent with the observation, and it would have made a nice slide. When a test result and an appealing explanation agree, that agreement is not confirmation — it is the moment to isolate the variable, because a satisfying story is precisely what stops people looking further."),

    ("h2", "Infrastructure errors are not capability failures"),
    ("p", "In one battery, roughly six of fourteen cells for a model failed on a tool-call parsing error in the serving layer, which the loop treated as fatal. That is pure harness noise sitting in the middle of a capability measurement. Until it was separated out, the model's score was partly a measurement of a parser."),
    ("p", "Classify every non-completion before you aggregate. A run that failed because the model couldn't do the task and a run that failed because a socket closed do not belong in the same number."),

    ("h2", "One prompt is not an experiment"),
    ("p", "A first smoke run on a single fixture showed a discriminator between two conditions of <strong>+1.00</strong> — an apparently decisive result. The full seven-fixture run showed <strong>+0.00</strong>. The single fixture wasn't representative, and nothing about the n=1 result signalled that."),
    ("p", "This is the sample-size point from your statistics course arriving in agent evaluation, where it bites harder because runs are slow and expensive and the temptation to conclude from one is correspondingly larger. Whole set, repeated, mean and spread, against a baseline — or you have an anecdote."),

    ("h2", "The checklist this produces"),
    ("ul", [
      "<strong>Emit a run manifest.</strong> Model, endpoint, every budget, verification state, config version. If it can end or alter the run, it goes in the manifest.",
      "<strong>Make every terminator name itself.</strong> A wall clock that expires should say so, distinguishably from a model that stopped.",
      "<strong>Print effective values, not requested ones.</strong> After all writers have run.",
      "<strong>Announce mid-run changes.</strong> If a phase transition rewrites a budget, that belongs in the output.",
      "<strong>Classify non-completions</strong> before aggregating anything.",
      "<strong>Check the instrument when a finding is surprising.</strong> Three wrong claims in one hour on that project came from the measuring tooling, not the system — a filename inside a search result read as a file the agent chose, a ratio read as parallelism, a counter misread because the grep pattern only matched single digits.",
    ]),
    ("callout", "warning", "And the cheap habit that beats all of it", "Count before theorising. A separate incident on the same project was misdiagnosed three times — as a bad timeout argument, then a dead shell, then, confidently and in writing, as a fork bomb from background loops. One command listing running processes by name would have named the real cause at any point. When something is broken, enumerate before you explain."),

    ("links", [
      ('Building effective agents — Anthropic', 'https://www.anthropic.com/engineering/building-effective-agents',
       'Argues for the simplest scaffold that works — partly because every added mechanism is another thing that can end a run invisibly.'),
      ('SWE-bench experiments — raw submissions', 'https://github.com/swe-bench/experiments',
       "Each submission records its own configuration. Worth reading a few as examples of what a run manifest should contain."),
    ]),

    ("quiz", [
      ("What makes a run limit a confound rather than a guard?",
       ["That it fires too early to be useful",
        "That its firing doesn't appear in the output you read afterwards, so it's indistinguishable from the thing you were measuring",
        "That it was set by the framework rather than by you"], 1),
      ("You set a budget to 30, the run behaves as though it were 3, and the result is flat. What can you conclude about the treatment?",
       ["It doesn't work",
        "Nothing — a null result is ambiguous between 'the treatment failed' and 'the treatment never happened'",
        "That the budget is the wrong lever"], 1),
      ("Three tests support an appealing architectural explanation. What should that agreement prompt?",
       ["Writing it up, since the mechanism and the data agree",
        "Isolating the variable — a satisfying story is what stops people looking further",
        "Running a fourth test under the same conditions"], 1),
      ("Six of fourteen eval cells fail on a serving-layer parsing error. What must you do before aggregating?",
       ["Retry them and average everything together",
        "Classify non-completions, so infrastructure failures don't sit inside a capability number",
        "Drop that model from the comparison"], 1),
    ]),
  ],
},
{
  "slug": "localising-a-failure",
  "title": "Localising a Failure",
  "subtitle": "Knowing something is broken is easy. Knowing which part is the whole job.",
  "body": [
    ("p", "A zero is ambiguous. \"The models scored 0 of 7\" is consistent with the models being incapable, the harness strangling them before they engage, the rubric being too strict, or the fixtures being broken. Every one of those calls for a different fix, and picking wrongly costs you weeks."),
    ("p", "Four techniques turn an ambiguous result into a located one. None is expensive."),

    ("h2", "1 · A control fixture"),
    ("p", "Add one task you are confident is easy, in the same domain, exercised by the same harness. Then read the pair:"),

    ("figure", "The control is the discriminator. Same model, same harness, same domain — only difficulty differs, so the pattern of pass and fail tells you which component is the wall.", '''<svg viewBox="0 0 640 190" role="img" aria-label="Reading a control fixture against a hard fixture">
<rect x="12" y="34" width="180" height="26" rx="4" class="d-box"/><text x="24" y="52" class="d-label-sm">control (easy)</text>
<rect x="12" y="66" width="180" height="26" rx="4" class="d-box"/><text x="24" y="84" class="d-label-sm">target (hard)</text>
<text x="228" y="26" class="d-label-sm">control ✓ / target ✗</text>
<rect x="228" y="34" width="180" height="58" rx="5" class="d-box-good"/>
<text x="240" y="56" class="d-label-sm">the wall is the specific</text>
<text x="240" y="72" class="d-label-sm">difficulty — scope, not ability</text>
<text x="440" y="26" class="d-label-sm">control ✗ / target ✗</text>
<rect x="440" y="34" width="188" height="58" rx="5" class="d-box-warn"/>
<text x="452" y="56" class="d-label-sm">the harness or the rubric,</text>
<text x="452" y="72" class="d-label-sm">not the model</text>
<text x="12" y="128" class="d-label-sm">Without the control, 0/7 is consistent with both columns and you cannot tell which you are looking at.</text>
<text x="12" y="150" class="d-label-sm">Worked case: a 30B model failed every multi-file fixture and passed the single-file control cleanly, under both guard</text>
<text x="12" y="168" class="d-label-sm">conditions — which located the wall at multi-file scope rather than at coding ability.</text>
</svg>'''),

    ("callout", "matters", "Build the control before you need it", "Every benchmark should carry at least one task you would be alarmed to fail. Its job is not to be scored — it is to tell you, on the day everything reads zero, whether the instrument is still working. This is instrument validity from lesson 3, running continuously rather than once at setup."),

    ("h2", "2 · Suspect the harness when every tier fails identically"),
    ("p", "A frontier model with a strong published benchmark score produced zero edit attempts and zero source recall on one battery — dying in the first few iterations, before it engaged with the task at all. A capable model failing <em>without trying</em> is not a capability signal. It is a harness signal."),
    ("p", "The general rule: when models of very different capability fail in the same way and at the same point, the thing they have in common is the scaffolding, not their weights. Capability differences should produce differently-shaped failures."),

    ("h2", "3 · Metric definition decides what you can see"),
    ("p", "One battery scored task-pass on recall over the full expected file set, including documentation and tests. Real near-misses — runs that found the right code and broke the build — scored zero alongside runs that never found anything, and the whole board read as uniform failure."),
    ("p", "Rescoring on source files only surfaced that the same model was reaching 0.50–0.67 on hard fixtures. Same runs, same data, different metric, and a completely different conclusion: not \"never found the code\" but \"found it and couldn't edit it correctly\" — two different problems with two different fixes."),
    ("callout", "insight", "Design the metric to separate the failures you care about", "A metric that collapses distinct failure modes into one number is not neutral — it actively hides the distinction you need. Report engagement separately from correctness. If your score cannot tell <em>never attempted</em> from <em>attempted and got it wrong</em>, it cannot tell you what to fix next, however precise it looks."),

    ("h2", "4 · State what a green result proves — and what it does not"),
    ("p", "An end-to-end test on a new serving runtime landed a correct single-file edit and it was tempting to record it as \"the new runtime works\". It proved the serving path and the integration. It said nothing about the multi-file capability that was the entire point of the investigation, because the runtime was serving the same weights."),
    ("p", "Every passing test has a scope. Writing down what it does <em>not</em> establish, at the moment you record the pass, is what stops \"the plumbing works\" quietly becoming \"the problem is solved\" three weeks later when nobody remembers the distinction."),

    ("h2", "The error underneath all four"),
    ("p", "One project logged the same reasoning failure at least three times in a fortnight, in unrelated areas:"),
    ("terms", [
      ("\"This model can't run on that engine\"", "One build format tested", "A different build of the same weights loaded first try."),
      ("\"This architecture can't reuse its cache\"", "Three tests, all truncated", "The truncation caused the failure, not the architecture."),
      ("\"This runtime is twice as fast\"", "Measured on the wrong engine mode", "The flag was inert in the configuration tested."),
    ]),
    ("callout", "pitfall", "A true narrow observation promoted to a false general one", "In each case the specific measurement was correct. What was wrong was the scope of the claim built on it. Before writing \"X cannot do Y\", name exactly what you tested — which build, which configuration, which budget, which mode — and ask whether the claim you are about to make is larger than the evidence under it. It usually is."),

    ("h2", "In practice"),
    ("ul", [
      "Put an easy control in every benchmark and read it first when a board looks uniform",
      "When every model fails identically, investigate the harness before the models",
      "Report engagement and correctness as separate numbers",
      "Record what each passing test does not establish, at the time you record the pass",
      "Write claims at the scope of the evidence — name the build, the config, the budget",
    ]),

    ("links", [
      ('SWE-bench', 'https://www.swebench.com/',
       'Note that variants exist precisely to separate difficulty from capability — Lite versus Verified is a control-fixture argument at benchmark scale.'),
      ("Let's Verify Step by Step (Lightman et al., 2023)", 'https://arxiv.org/abs/2305.20050',
       'Process versus outcome scoring — the same idea as separating engagement from correctness, done at the step level.'),
    ]),

    ("quiz", [
      ("Every model in your battery scores zero, from a small local one to a frontier model. What should you investigate first?",
       ["The models — the task may be beyond current capability",
        "The harness, since the thing they all share is the scaffolding, not their weights",
        "The fixtures, which are probably mislabelled"], 1),
      ("What is a control fixture for?",
       ["Establishing a floor score for the leaderboard",
        "Telling you, when everything reads zero, whether the instrument still works and where the wall is",
        "Giving weaker models something they can pass"], 1),
      ("Rescoring the same runs on a narrower metric changes 'uniform failure' into '0.50-0.67 on hard tasks'. What does that show?",
       ["The original metric was miscalculated",
        "A metric that collapses distinct failure modes hides the distinction you need to choose a fix",
        "The narrower metric is too generous"], 1),
      ("An integration test on a new runtime passes with a single-file edit. What have you established?",
       ["That the runtime works and the investigation can close",
        "That the serving path and integration work — and nothing about the multi-file question, since the weights are unchanged",
        "That the previous runtime was the bottleneck"], 1),
    ]),
  ],
},
{
  "slug": "models-judging-models",
  "title": "Models Judging Models",
  "subtitle": "LLM-as-judge — what it genuinely buys you, the four biases it ships with, and the failure that manufactures results.",
  "body": [
    ("p", "Deterministic grading is the top of the ladder and most interesting outputs don't have it. Summaries, explanations, tone, helpfulness, whether an answer is <em>grounded</em> in its sources — none compiles, none has a test suite. The pragmatic answer is to have another model grade it, and that answer is genuinely useful and genuinely dangerous in ways worth knowing precisely."),

    ("h2", "What it buys you"),
    ("terms", [
      ("Coverage", "Grades what nothing else can", "Open-ended text, where the alternative is no measurement at all rather than a better one."),
      ("Scale", "Hundreds of items, minutes, pennies", "Human labelling of the same set is days and real money."),
      ("Consistency", "Same rubric every time", "Human raters drift across a long session; a judge at temperature 0 does not."),
      ("Structure", "Rubric dimensions, not one score", "Groundedness, completeness and tone as separate numbers, which a single human score usually blurs."),
      ("Iteration speed", "The real win", "A judge you can run in ninety seconds changes how often you measure, and frequency of measurement matters more than precision of any single run."),
    ]),

    ("h2", "The four biases it ships with"),
    ("p", "These are documented, reproducible, and present by default. Treat them as properties of the instrument rather than as bugs to be prompted away."),
    ("terms", [
      ("Position bias", "Order changes the verdict", "Present the same two answers in the opposite order and judges flip a substantial fraction of their decisions. Mitigate by running both orders and discarding disagreements — or counting them as ties."),
      ("Verbosity bias", "Longer reads as better", "A judge rewards length beyond the point where length helps. If one of your variants is chattier, you will measure that."),
      ("Self-preference", "Models favour their own output", "Evaluators recognise and prefer their own generations. A judge from the same family as the system under test is not neutral."),
      ("Score compression", "Everything is a 7 or 8", "Absolute 1–10 scoring clusters hard. Pairwise comparison discriminates far better than asking for a number."),
    ]),
    ("callout", "pitfall", "Circularity is the version that voids the result entirely", "If the judge is the model under test, you are asking a system to score itself and the number carries no information about capability. The softer version is subtler and far more common: judging with a model from the same family, trained on overlapping data, sharing the same blind spots. It will not notice the errors it would have made itself — which are exactly the errors you most need to catch."),

    ("h2", "The failure that manufactures results"),
    ("p", "The biases above add noise, and noise is survivable. There is a worse case, and it is easy to walk into."),
    ("p", "On one project an automated flag called <code>edit_attempted</code> was used as a measurement. It had been built as a safety classifier, and it counted certain shell commands as evidence of an edit attempt. About 15% of the recorded attempts had no edit tool call behind them at all."),
    ("p", "That alone is tolerable — a known error rate can be corrected for. The problem was that <strong>the error was not uniform across conditions.</strong> The experimental condition relaxed budgets, which meant it ran more shell commands, which meant it accumulated more phantom credits. The difference between conditions was partly a measurement of shell activity rather than of editing."),

    ("figure", "Noise that is even across conditions costs you power. Bias that tracks the condition you are testing invents an effect, and no amount of extra sampling removes it.", '''<svg viewBox="0 0 640 190" role="img" aria-label="Uniform judge error versus condition-correlated judge error">
<text x="12" y="18" class="d-fill-green" font-size="12" font-weight="600">ERROR EVEN ACROSS CONDITIONS — survivable</text>
<rect x="12" y="30" width="120" height="24" rx="4" class="d-box"/><text x="26" y="47" class="d-label-sm">control</text>
<rect x="140" y="30" width="60" height="24" rx="4" class="d-fill-muted" opacity="0.5"/><text x="152" y="47" class="d-label-sm">+err</text>
<rect x="12" y="60" width="150" height="24" rx="4" class="d-box-accent"/><text x="26" y="77" class="d-label-sm">treatment</text>
<rect x="170" y="60" width="60" height="24" rx="4" class="d-fill-muted" opacity="0.5"/><text x="182" y="77" class="d-label-sm">+err</text>
<text x="248" y="62" class="d-label-sm">the gap survives — error cancels</text>
<line x1="12" y1="98" x2="628" y2="98" stroke="var(--border)"/>
<text x="12" y="122" class="d-fill-red" font-size="12" font-weight="600">ERROR TRACKS THE CONDITION — fatal</text>
<rect x="12" y="134" width="120" height="24" rx="4" class="d-box"/><text x="26" y="151" class="d-label-sm">control</text>
<rect x="140" y="134" width="26" height="24" rx="4" class="d-fill-red" opacity="0.45"/>
<rect x="12" y="164" width="120" height="22" rx="4" class="d-box-accent"/><text x="26" y="180" class="d-label-sm">treatment</text>
<rect x="140" y="164" width="120" height="22" rx="4" class="d-fill-red" opacity="0.6"/><text x="152" y="180" class="d-label-sm">much more error</text>
<text x="286" y="152" class="d-label-sm">the "effect" is the bias</text>
</svg>'''),

    ("callout", "warning", "Ask this before trusting any judge comparison", "Not \"how accurate is the judge?\" but <strong>\"is the judge's error correlated with the thing I changed?\"</strong> If one variant produces longer answers and your judge rewards length, you have a verbosity bias masquerading as an improvement. If one variant is more verbose because it explains itself more, you cannot tell those apart from the score alone. Extra samples will not save you — bias does not average out."),

    ("h2", "A judge that is silently off is worse than no judge"),
    ("p", "On the same project, one configuration default meant the verifier was nil. That single value disabled turn-end verification, the fix-attempt loop and per-edit feedback simultaneously — and nothing said so. The system continued producing results that looked like verified results."),
    ("p", "No judge at all is an obvious gap. A judge that has quietly stopped running is a number that carries authority it has not earned. Assert that your grader ran, on every run, and fail loudly when it did not."),

    ("h2", "How to use one properly"),
    ("terms", [
      ("Last resort on the ladder", "Not first reach", "Deterministic, then reference-match, then judge. Every rung down costs certainty."),
      ("Different family from the system", "Avoid self-preference", "And never the model under test."),
      ("Pairwise, not absolute", "Discriminates far better", "\"Which is better\" beats \"score this 1-10\", which clusters."),
      ("Both orders, every time", "Neutralises position bias", "Disagreement between orders is a tie, and its rate is a health metric for your judge."),
      ("Calibrate against humans", "The step nobody does", "Label 30-50 items by hand once. Measure agreement. If the judge disagrees with you on the cases you care about, it is not measuring what you think."),
      ("Report agreement alongside scores", "Honesty about the instrument", "A judge score without a known agreement rate is an opinion with a decimal point."),
    ]),
    ("callout", "matters", "When you can buy a deterministic verifier, buy it", "One agent project verifies its edits with typecheckers and a language server rather than a model judge. That is narrower than a judge and it is not an opinion, which is what a loop needs when the verdict decides whether to escalate. Reach for a judge where nothing checkable exists — not because it was quicker to build than a real check."),

    ("h2", "Where this connects"),
    ("p", "This is the same principle as the loops lesson, one level up: a loop or a score improves things only when signal enters from outside. A judge from the same family as the system under test is not outside. A grader whose error tracks your treatment is not outside. Human labels, a compiler, a test suite and a held-out answer key are."),

    ("links", [
      ('Judging LLM-as-a-Judge (Zheng et al., 2023)', 'https://arxiv.org/abs/2306.05685',
       'The MT-Bench paper. Documents position, verbosity and self-enhancement bias, and reports agreement rates against human raters.'),
      ('LLMs are not Fair Evaluators (Wang et al., 2023)', 'https://arxiv.org/abs/2305.17926',
       'Position bias in detail, and the swap-and-compare mitigation used above.'),
      ('LLM Evaluators Recognize and Favor Their Own Generations (Panickssery et al., 2024)', 'https://arxiv.org/abs/2404.13076',
       "Self-preference measured directly. The reason a judge from the same family as the system under test is not neutral."),
    ]),

    ("quiz", [
      ("What is the most dangerous property an automated grader can have?",
       ["A high overall error rate",
        "An error rate that correlates with the condition being tested, which manufactures an effect that more sampling cannot remove",
        "Slow evaluation speed"], 1),
      ("Why prefer pairwise comparison over absolute 1-10 scoring?",
       ["It is cheaper to run",
        "Absolute scores cluster tightly, while pairwise judgements discriminate far better",
        "It removes the need to randomise order"], 1),
      ("You judge your system's output using a model from the same family as the system. What is the risk?",
       ["The judge will be too harsh on familiar phrasing",
        "Self-preference, and shared blind spots — it will not catch the errors it would have made itself",
        "None, provided temperature is set to 0"], 1),
      ("A config default left the verifier nil for an entire run. Why is that worse than having no verifier?",
       ["It wastes compute on a disabled component",
        "The system keeps producing results that look verified, so the numbers carry authority they haven't earned",
        "It causes the loop to terminate early"], 1),
    ]),
  ],
},
{
  "slug": "deterministic-first",
  "title": "Deterministic First",
  "subtitle": "The best AI engineering decision is frequently to use less of it.",
  "body": [
    ("p", "This idea has appeared five times already in this course, each time as a footnote to something else. It deserves stating on its own, because it is the highest-leverage engineering judgement in the field and it is the one most often skipped."),
    ("p", "<strong>A model is the most expensive, slowest, least debuggable and least testable component you can put in a system.</strong> Sometimes it is the only thing that can do the job, and then it is worth every one of those costs. Frequently it is not, and reaching for it anyway is a choice you will pay for on every request forever."),

    ("h2", "Where it has already come up"),
    ("terms", [
      ("Intake question 1", "Is this even an ML problem?", "Could a rule, a lookup, a SQL query or a person twice a day solve it? Most projects that die should die here."),
      ("Agent or workflow?", "Did you decide the sequence?", "If you know the steps, write the steps. An agent is for when the sequence genuinely cannot be known in advance."),
      ("Prompt or tool?", "Can the model tell it complied?", "A mechanically checkable rule belongs in a tool as a precondition. Refusal beats hope."),
      ("Judge or verifier?", "Is there something checkable?", "A typechecker is narrower than a model judge and it is not an opinion. Where a real check exists, take it."),
      ("Embeddings or keywords?", "Is the text jargon-heavy?", "BM25 beats vector search outright on identifiers, error codes and rare terms, at a fraction of the cost."),
    ]),
    ("callout", "insight", "The pattern", "Every one of those is the same question at a different altitude: <em>is there a bounded, checkable mechanism that does this job?</em> When there is, it wins on cost, latency, testability and the ability to explain what happened — and it does not drift, hallucinate, or change behaviour when a provider updates a model behind an alias."),

    ("h2", "What a deterministic component gives you that a model cannot"),

    ("figure", "The comparison people skip. A model wins the top row decisively and loses every row beneath it — so the question is whether you actually need the top row.", '''<svg viewBox="0 0 640 230" role="img" aria-label="Deterministic component compared against a model">
<text x="250" y="20" class="d-accent">deterministic</text>
<text x="440" y="20" class="d-label-b">model</text>
<line x1="12" y1="28" x2="628" y2="28" stroke="var(--border)"/>
<text x="12" y="50" class="d-label-sm">handles open-ended input</text>
<text x="262" y="50" class="d-fill-red" font-size="13" font-weight="700">✗</text>
<text x="452" y="50" class="d-fill-green" font-size="13" font-weight="700">✓</text>
<line x1="12" y1="60" x2="628" y2="60" stroke="var(--border)" stroke-dasharray="3 3"/>
<text x="12" y="82" class="d-label-sm">same input, same output, always</text>
<text x="262" y="82" class="d-fill-green" font-size="13" font-weight="700">✓</text>
<text x="452" y="82" class="d-fill-red" font-size="13" font-weight="700">✗</text>
<text x="12" y="108" class="d-label-sm">cost per call</text>
<text x="252" y="108" class="d-fill-green" font-size="12" font-weight="600">~0</text>
<text x="446" y="108" class="d-fill-red" font-size="12" font-weight="600">per token</text>
<text x="12" y="134" class="d-label-sm">latency</text>
<text x="250" y="134" class="d-fill-green" font-size="12" font-weight="600">µs–ms</text>
<text x="450" y="134" class="d-fill-red" font-size="12" font-weight="600">100ms–60s</text>
<text x="12" y="160" class="d-label-sm">can be unit tested</text>
<text x="262" y="160" class="d-fill-green" font-size="13" font-weight="700">✓</text>
<text x="452" y="160" class="d-fill-yellow" font-size="12" font-weight="600">statistically</text>
<text x="12" y="186" class="d-label-sm">you can say why it did that</text>
<text x="262" y="186" class="d-fill-green" font-size="13" font-weight="700">✓</text>
<text x="452" y="186" class="d-fill-red" font-size="13" font-weight="700">✗</text>
<text x="12" y="212" class="d-label-sm">behaviour changes without you</text>
<text x="262" y="212" class="d-fill-green" font-size="13" font-weight="700">✗</text>
<text x="452" y="212" class="d-fill-red" font-size="13" font-weight="700">✓</text>
</svg>'''),

    ("h2", "The tasks people reach for a model on that don't need one"),
    ("ul", [
      "<strong>Extraction from structured or semi-structured text.</strong> Invoice numbers, dates, order ids in a known format. A regex is free, instant, and cannot invent a value that wasn't there.",
      "<strong>Routing on explicit signals.</strong> If the request contains an order number, it's an order query. Rules first; a classifier for what falls through.",
      "<strong>Validation.</strong> Schema checks, range checks, referential integrity. Never ask a model whether data is valid when you can assert it.",
      "<strong>Deduplication and matching on identifiers.</strong> A join, not a similarity search.",
      "<strong>Formatting and templating.</strong> If the output shape is fixed, a template with slots beats generation, and it cannot drift.",
      "<strong>Arithmetic and aggregation.</strong> Give the model the tool; do not ask it for the number.",
      "<strong>Anything with a lookup table.</strong> Country codes, tax rates, product mappings. A model will approximate a table it could simply have been given.",
    ]),
    ("callout", "matters", "The hybrid is usually the right answer", "This is not an argument for avoiding models. It is an argument for putting them where they earn their cost. Deterministic code handles the 80% that is structured, and the model handles the ambiguous remainder — which means it sees fewer calls, on harder inputs, where its judgement is actually worth paying for. Systems built this way are cheaper, faster, easier to debug, and usually more accurate, because each component is doing what it is good at."),

    ("h2", "How to make the call"),
    ("terms", [
      ("1 · Can you write the rule?", "If yes, write it", "If you can state the logic in a sentence, it is code, not a prompt."),
      ("2 · Is the input space bounded?", "Enumerable inputs mean rules", "Open-ended natural language is where models earn their place."),
      ("3 · What does a wrong answer cost?", "High cost favours determinism", "Because you can test a rule exhaustively and you cannot test a model exhaustively."),
      ("4 · Do you have to explain it?", "Regulators want mechanisms", "\"The model decided\" is not an answer to an auditor, or to a customer."),
      ("5 · What is the volume?", "Per-call cost compounds", "A model call that is fine at a thousand a day may be untenable at a million."),
    ]),

    ("h2", "The honest counter-argument"),
    ("p", "Rules have a real failure mode of their own: they accumulate. A routing system that starts as four clean conditions becomes two hundred over three years, each one added for a case nobody remembers, and no one dares delete any of them. That is a maintenance burden models genuinely do avoid, and it is why \"just write rules\" is not universally correct either."),
    ("p", "The distinction worth holding: rules are right where the logic is <em>stable and stateable</em>. Models are right where it is <em>fuzzy or evolving</em>. When you find yourself writing the fortieth special case, that is the signal to reconsider — not the fourth."),
    ("callout", "warning", "And the failure mode of this whole lesson", "Applied too enthusiastically, this becomes an argument for never using AI, which is just as wrong as reaching for it first. The test is not \"could this conceivably be done with rules\" — almost anything could, badly. It is \"does a bounded mechanism do this <em>well</em>?\" A hand-written rule system that approximates language understanding badly is worse than a model call, and considerably more work."),

    ("h2", "Where this lands"),
    ("p", "Every block of this program has a version of this decision in it, and the intake sheet asks it first for a reason. Before the model selection, before the prompt, before the fine-tune: is there a bounded mechanism that does this job? Ask it early, because the answer is easy to act on at the start of a project and very expensive to act on once the model is load-bearing."),

    ("links", [
      ('Building effective agents — Anthropic', 'https://www.anthropic.com/engineering/building-effective-agents',
       'Opens with the same argument: find the simplest solution possible, and only increase complexity when it demonstrably improves outcomes.'),
      ('Rules of Machine Learning — Google', 'https://developers.google.com/machine-learning/guides/rules-of-ml',
       "Rule 1 is: do not be afraid to launch a product without machine learning. Written for classical ML and it has aged well."),
    ]),

    ("quiz", [
      ("You need to pull order numbers out of support emails, and they always match a known format. What should you reach for?",
       ["An LLM with a structured-output schema, for robustness to format variation",
        "A regex — it is free, instant, and cannot invent a value that was not there",
        "An embedding model to find the most order-number-like span"], 1),
      ("What does a deterministic component give you that a model cannot?",
       ["Better handling of ambiguous input",
        "Same input to same output always, exhaustive testability, and an explanation of why it did that",
        "Lower engineering effort in every case"], 1),
      ("When is the rules-based approach the wrong call?",
       ["Whenever the input is natural language",
        "When the logic is fuzzy or evolving — the tell is finding yourself writing the fortieth special case",
        "Whenever a model would also work"], 1),
      ("What is the strongest form of this argument in practice?",
       ["Avoid models wherever a rule could conceivably do the job",
        "Handle the structured majority deterministically so the model sees fewer, harder calls where its judgement is worth paying for",
        "Use rules for prototypes and models in production"], 1),
    ]),
  ],
},
]
