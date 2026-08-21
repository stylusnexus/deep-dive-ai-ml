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
    ("p", "The Bullpen project spent months describing itself as a <em>cascader</em>: a system that tries a local model and escalates to progressively larger ones. That was a genuine, well-reasoned decision. Measurement later falsified the premise it rested on, and the project became a local agent that occasionally escalates. The architecture docs kept saying cascader, so new work kept being designed against a system that no longer existed."),
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
]
