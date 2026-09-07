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

    ("h2", "The harness is also the instrument, and that is the problem"),
    ("p", "The definition above says the harness is executed and therefore true by construction &mdash; whatever it says is what happens. That is right about the <em>system</em>, and it hides something. The harness is not only the thing that does the work; it is also the thing that reports on the work. Those are two jobs, they are usually built by the same person in the same afternoon, and only the first one fails loudly."),
    ("p", "The consequence is uncomfortable and specific: when the harness is wrong, the evidence about the harness comes from the harness. A rig that cannot tell success from inaction will say so in no way whatsoever. It will produce numbers, they will move when you change things, and every one of them will be noise &mdash; and the next lesson opens with two cases from this project where exactly that happened for months."),

    ("h3", "What a fixture is, and how it relates to the harness"),
    ("terms", [
      ("Fixture", "One case, with an answer",
       "A single scenario plus the check that decides whether it passed: the starting state, the inputs, and an assertion that is true afterwards and false before. It is the smallest unit of evidence the harness can produce."),
      ("The harness", "The rig that runs them",
       "Everything around the model plus everything around the fixtures &mdash; setting up the starting state, running the case, collecting what happened, deciding pass or fail. One harness, many fixtures."),
      ("The relation", "Runner and case",
       "A harness is to a fixture roughly what a test runner is to a test. The harness is reusable and says nothing about your task; the fixture is specific and carries the claim. Confusing them is how people conclude a model cannot do something when the rig was never able to see that it had."),
      ("What it must not be", "A check the work cannot fail",
       "A fixture that passes at the starting commit is measuring nothing, and one that fails whatever you do is measuring nothing either. Both look like results."),
    ]),

    ("figure", "One harness, many fixtures. The harness supplies the starting state and collects what happened; each fixture carries the claim that a specific thing became true.", '''<svg viewBox="0 0 540 168" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A harness sets up state, runs three fixtures, and collects a trace and a verdict from each.">
<rect x="10" y="14" width="120" height="128" rx="7" class="d-box-accent"/>
<text x="70" y="60" class="d-label-b" text-anchor="middle">harness</text>
<text x="70" y="78" class="d-label-sm" text-anchor="middle">sets up state,</text>
<text x="70" y="92" class="d-label-sm" text-anchor="middle">runs, records</text>
<path d="M130 44 L172 44" class="d-arrow"/>
<path d="M130 78 L172 78" class="d-arrow"/>
<path d="M130 112 L172 112" class="d-arrow"/>
<rect x="176" y="28" width="152" height="32" rx="5" class="d-box"/><text x="252" y="48" class="d-label-sm" text-anchor="middle">fixture: refuses out of scope</text>
<rect x="176" y="62" width="152" height="32" rx="5" class="d-box"/><text x="252" y="82" class="d-label-sm" text-anchor="middle">fixture: cites the source</text>
<rect x="176" y="96" width="152" height="32" rx="5" class="d-box"/><text x="252" y="116" class="d-label-sm" text-anchor="middle">fixture: escalates the refund</text>
<path d="M328 44 L370 44" class="d-arrow"/>
<path d="M328 78 L370 78" class="d-arrow"/>
<path d="M328 112 L370 112" class="d-arrow"/>
<rect x="374" y="44" width="152" height="60" rx="6" class="d-box-good"/>
<text x="450" y="68" class="d-label-b" text-anchor="middle">verdict + trace</text>
<text x="450" y="86" class="d-label-sm" text-anchor="middle">pass/fail, and what it did</text>
<text x="176" y="152" class="d-label-sm">each fixture must fail before the work and pass after it &#8212; or it is not evidence</text>
</svg>'''),

    ("know",
     "A harness you cannot measure is one you can only change, not improve.",
     "Every harness decision &mdash; a prompt line, a turn limit, a tool description, a retry &mdash; is a claim that behaviour will get better. Without fixtures the claim is untestable, so changes get made on plausibility and kept on attachment, and the rig accumulates modifications nobody can justify or safely remove. With fixtures the same changes become reversible: you can revert one and see the number move, which is the difference between engineering the harness and decorating it.",
     "The worked example below is a harness change that was a <em>deletion</em>. It was defensible only because a fixture existed that the deletion moved &mdash; without that, removing a line from a system prompt is indistinguishable from superstition, and nobody would have dared."),

    ("callout", "matters", "Build the fixture before the harness change, not after",
     "<p>A fixture written after a change tends to encode the change. You already know what the new behaviour is, so the assertion gets shaped to fit it, and it will pass forever afterwards without ever having been at risk. Write it first, watch it fail for the reason you expect, and only then make the change &mdash; at which point passing means something.</p><p>The other half is that the harness has to record <em>what happened</em>, not only the verdict. A pass/fail bit cannot distinguish a model that never understood the task from one that understood it and declined, and those two need opposite fixes. That distinction is what the next lesson calls process honesty, and it is a property of the harness rather than of the fixture.</p>"),

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
    ("related", ["spec-driven-development", "why-measurement-decides", "code-nobody-decided", "version-control-basics"]),
    ("links", [
      ('Documenting Architecture Decisions — Michael Nygard (2011)', 'https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions',
       'The original ADR write-up. Short, and still the clearest statement of what belongs in one.'),
      ('adr.github.io', 'https://adr.github.io/',
       'Templates and tooling that grew up around the idea.'),
      ('Building effective agents — Anthropic', 'https://www.anthropic.com/engineering/building-effective-agents',
       'On harness design: when a loop is warranted and when a fixed workflow beats one.'),
    ]),
    ("quiz", [
      ("You write down: “Retrieval uses Best Matching 25 (BM25) plus embeddings, reranked. We rejected pure vector search because recall on exact identifiers was 41% worse.” Which artifact is this?",
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
    ("p", "An architecture decision record (ADR) records a decision <em>and the evidence that forced it</em>. The decision persists in the document; the evidence decays in the world. When the two separate, the ADR becomes a rule enforced past its reason — and because it is written down and was once correct, it is unusually hard to argue with."),
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

    ("callout", "pitfall", "Read it carefully, though", "These submissions differ in many parts of the scaffold at once — prompts, retrieval, retry budgets and token spend all vary together. The spread is an upper bound on what harness work can buy, not a controlled experiment. It tells you the harness matters enormously; it does not tell you which harness change is responsible. That distinction is the whole of the next two lessons."),
    ("related", ["what-ai-makes-worse", "code-nobody-decided", "the-apprenticeship-problem", "deterministic-first"]),
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
    ("p", "Everything in the previous lesson failed the same way: an artifact stayed confident after its truth expired. None of the three can notice this about itself. A harness cannot tell you its own message is misleading; a recipe cannot tell you its first step is stale; an architecture decision record (ADR) cannot tell you its evidence was overturned. Only a measurement can."),

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

    ("know",
     'An instrument that cannot tell success from inaction produces noise, not numbers.',
     'Before trusting any measurement, prove the fixture fails at the starting state and passes with a known-good fix applied. If either half is untrue, every number it produces afterwards is meaningless.',
     'A benchmark reported six of eight tasks passing before any work had been done. The verification step was checking that the test command exited zero, and the command was piped through head, which exits zero regardless of what failed upstream. Weeks of comparisons had been run against that fixture.'),
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
    ("h2", "And the law that applies to everything above"),
    ("p", "This lesson argues that a number is the only thing that corrects a confident artefact. The honest counterweight is <strong>Goodhart&#39;s law</strong>: when a measure becomes a target, it ceases to be a good measure. The moment a number is what people are judged on, effort moves towards the number, and the number stops standing for the thing it was chosen to stand for."),

    ("p", "It is not a reason to measure less. An unmeasured system is corrected by nobody&#39;s opinion in particular, which is worse. It is a reason to expect the measure to decay once it matters, and to notice that most of this course&#39;s specific warnings are instances of it: a judge that quietly prefers longer answers, so a change that adds verbosity scores as quality; a public benchmark that has been optimised against for years, so it measures familiarity with the benchmark; a reward function a policy learns to satisfy by detecting the test fixture; a coverage percentage that rises while the tests assert nothing."),

    ("know",
     "Every metric in this course is a proxy, and a proxy under pressure drifts away from the thing it stood for.",
     "The metric was chosen because it correlated with something you actually wanted, in a period when nobody was trying to move it. Optimising against it selects precisely for the part of that correlation that was incidental &mdash; which is why a measure looks best just before it stops working, and why the phrase &ldquo;we hit the target&rdquo; is not a synonym for &ldquo;we got what we wanted&rdquo;.",
     "A support team is measured on time-to-first-response. The number improves substantially. What improved was the speed of an automated acknowledgement, and resolution time is unchanged &mdash; the measure moved, the thing it was standing in for did not, and no individual acted in bad faith at any point."),

    ("callout", "matters", "Three habits that keep a measure honest for longer",
     "<p><strong>Pair every target with a guardrail.</strong> The primary metric may improve only if the guardrail does not degrade. Latency, cost and refusal rate are the usual ones, and the point is that they are chosen <em>before</em> you look, so they cannot be selected to flatter the result.</p><p><strong>Hold something back from optimisation.</strong> A slice of evaluation data nobody tunes against, opened rarely. The moment every set is being optimised against, you have no uncorrupted reading left.</p><p><strong>Re-derive the metric periodically.</strong> Ask whether it still correlates with the outcome it was chosen for, rather than assuming the correlation that justified it survived being targeted. It usually has not survived intact.</p>"),
    ("related", ["how-to-measure", "confounds-you-cannot-see", "is-the-difference-real", "where-evaluation-lives"]),
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

    ("figure", "Dependency order, not importance order. Each step is worthless until the one above it holds — which is why step 0 is both the one people skip and the one that invalidates everything below it.", '''<svg viewBox="0 0 640 235" role="img" aria-label="The measurement procedure in dependency order"><defs><marker id="hm" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" class="d-fill-accent"/></marker></defs>
<rect x="12" y="14" width="450" height="34" rx="5" class="d-box-warn"/>
<text x="28" y="30" class="d-label-b">0 · Prove the instrument</text>
<text x="28" y="44" class="d-label-sm">fails before the work, passes after it</text>
<text x="476" y="30" class="d-fill-red" font-size="11" font-weight="600">skip this and</text>
<text x="476" y="46" class="d-fill-red" font-size="11" font-weight="600">everything below</text>
<text x="476" y="62" class="d-fill-red" font-size="11" font-weight="600">is noise</text>
<path d="M237 48 L237 62" class="d-arrow-accent" marker-end="url(#hm)"/>
<rect x="12" y="62" width="450" height="30" rx="5" class="d-box"/>
<text x="28" y="82" class="d-label-sm"><tspan class="d-label-b">1 · Fix the target</tspan> — metric and threshold, before the run</text>
<path d="M237 92 L237 106" class="d-arrow-accent" marker-end="url(#hm)"/>
<rect x="12" y="106" width="450" height="30" rx="5" class="d-box"/>
<text x="28" y="126" class="d-label-sm"><tspan class="d-label-b">2 · Baseline</tspan> — whole set, repeated, recorded</text>
<path d="M237 136 L237 150" class="d-arrow-accent" marker-end="url(#hm)"/>
<rect x="12" y="150" width="450" height="30" rx="5" class="d-box"/>
<text x="28" y="170" class="d-label-sm"><tspan class="d-label-b">3 · One treatment</tspan> — or a screen, with its cost stated aloud</text>
<path d="M237 180 L237 194" class="d-arrow-accent" marker-end="url(#hm)"/>
<rect x="12" y="194" width="450" height="34" rx="5" class="d-box-good"/>
<text x="28" y="210" class="d-label-b">4 · Read it, then 5 · revert the fix</text>
<text x="28" y="224" class="d-label-sm">did the number go back? if not, you learned the wrong lesson</text>
</svg>'''),
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
      ("After", "Interval not fraction. Guardrail checked. Fix reverted and the number moved back.", "Then it is a finding, and only then does it belong in a recipe or an architecture decision record (ADR)."),
    ]),
    ("callout", "matters", "Why this belongs in a module about documentation", "A recipe or an ADR built on an unmeasured result does not just fail \u2014 it hardens. It gets cited, followed, and defended long after the thing it claims was quietly falsified. Measurement is not a separate discipline from writing things down; it is the thing that earns you the right to."),
    ("related", ["why-measurement-decides", "is-the-difference-real", "confounds-you-cannot-see", "tracking-runs-and-automating-evals"]),
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

    ("figure", "One task, end to end. The two test sets are the instrument invariant made concrete — one proves the work happened, the other proves nothing else broke.", '''<svg viewBox="0 0 640 205" role="img" aria-label="Anatomy of a SWE-bench task"><defs><marker id="sb" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" class="d-fill-accent"/></marker></defs>
<rect x="12" y="14" width="180" height="60" rx="6" class="d-box"/>
<text x="26" y="36" class="d-label-b">Given</text>
<text x="26" y="54" class="d-label-sm">repo at base_commit</text>
<text x="26" y="68" class="d-label-sm">plus the issue text</text>
<path d="M192 44 L232 44" class="d-arrow-accent" marker-end="url(#sb)"/>
<rect x="232" y="14" width="160" height="60" rx="6" class="d-box-accent"/>
<text x="246" y="36" class="d-label-b">System under test</text>
<text x="246" y="58" class="d-label-sm">produces a patch</text>
<path d="M392 44 L432 44" class="d-arrow-accent" marker-end="url(#sb)"/>
<rect x="432" y="14" width="196" height="60" rx="6" class="d-box"/>
<text x="446" y="36" class="d-label-b">Graded in a container</text>
<text x="446" y="58" class="d-label-sm">repo and deps at that commit</text>
<rect x="12" y="94" width="300" height="56" rx="6" class="d-box-good"/>
<text x="28" y="116" class="d-label-b">FAIL_TO_PASS must now pass</text>
<text x="28" y="136" class="d-label-sm">an agent that changes nothing fails here</text>
<rect x="328" y="94" width="300" height="56" rx="6" class="d-box-good"/>
<text x="344" y="116" class="d-label-b">PASS_TO_PASS must stay passing</text>
<text x="344" y="136" class="d-label-sm">an agent that guts the suite fails here</text>
<text x="12" y="176" class="d-label-sm">Together they mean doing nothing and solving it cannot score the same. Most homemade benchmarks omit</text>
<text x="12" y="194" class="d-label-sm">the second half, and quietly reward vandalism.</text>
</svg>'''),
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

    ("know",
     'A benchmark must make doing nothing and solving it score differently.',
     'SWE-bench does this with two test sets. FAIL_TO_PASS proves the work happened; PASS_TO_PASS proves nothing else broke. Most homemade benchmarks implement only the first half.',
     "Score only on 'the failing test now passes' and an agent can delete the test. Score only on 'the suite is green' and an agent that changes nothing scores full marks on any task where the suite was already green. You need both halves, and the second is the one people leave out."),
    ("related", ["one-set-many-models", "how-to-measure", "localising-a-failure", "eval-battery"]),
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

    ("know",
     'A limit that can end a run and cannot be seen is not a guard, it is a confound.',
     'An invisible terminator does not merely stop the run. It stops it while looking exactly like the thing you were trying to measure, so the result gets attributed to whichever component you were already thinking about — which is almost always the model.',
     'Nine runs produced zero edits and were recorded as a model failing to commit changes. They had been terminated by six different mechanisms: a read budget, a phase clamp, a decomposition reassignment, a whole-run wall clock, a routing bug that served a smaller model than the one under test, and a config default that silently disabled verification. None appeared in the output.'),
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
    ("p", "A first smoke run on a single fixture showed a difference between two conditions of <strong>+1.00</strong> — one passed, one failed, an apparently decisive result. The full seven-fixture run showed <strong>+0.00</strong>. The single fixture wasn't representative, and nothing about the n=1 result signalled that."),
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
    ("related", ["is-the-difference-real", "localising-a-failure", "rungs-and-experiments", "data-leakage"]),
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

    ("figure", "The control is what separates the explanations. Same model, same harness, same domain — only difficulty differs, so the pattern of pass and fail tells you which component is the wall.", '''<svg viewBox="0 0 640 190" role="img" aria-label="Reading a control fixture against a hard fixture">
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
    ("related", ["confounds-you-cannot-see", "rungs-and-experiments", "how-to-measure", "swe-bench-and-how-to-run-it"]),
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

    ("know",
     'Ask not how accurate your grader is, but whether its error correlates with what you changed.',
     'Noise that is even across conditions costs you statistical power and nothing else. Bias that tracks the treatment manufactures an effect, and no amount of extra sampling removes it.',
     'Your judge mildly prefers longer answers. You test a prompt change that makes the model more verbose. The judge scores it higher. You ship a verbosity increase believing it was a quality improvement, and every additional sample makes the false result look more solid.'),
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
    ("related", ["rubrics-and-blind-reads", "is-the-difference-real", "judging-a-conversation", "eval-data-you-can-trust"]),
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
      ("Embeddings or keywords?", "Is the text jargon-heavy?", "Best Matching 25 (BM25) beats vector search outright on identifiers, error codes and rare terms, at a fraction of the cost."),
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

    ("know",
     'A model is the most expensive, slowest, least debuggable and least testable component you can put in a system.',
     'Sometimes it is the only thing that can do the job, and then it earns every one of those costs. Frequently it is not, and reaching for it anyway is a bill you pay on every request forever.',
     'Extracting an order number that always matches ORD-######. A regex is free, runs in microseconds, can be unit tested exhaustively, and cannot invent a number that was not in the text. An LLM call costs money per invocation, takes a second, and will occasionally return a plausible order number that does not exist.'),
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
    ("related", ["what-ai-makes-worse", "structured-output-json", "baseline-to-model", "asking-the-database-properly"]),
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
{
  "slug": "code-nobody-decided",
  "title": "Code Nobody Decided",
  "subtitle": "The previous lesson asked whether to use a model. This one asks who chose the behaviour when you did.",
  "body": [
    ("p", "A pull request looks good. Clean structure, real error handling, sensible names, tests passing, and it matches the API contract. The reviewer approves it and moves on. Three weeks later the on-call engineer is paged: the endpoint returns a conflict for cancelled orders. The product team is baffled — they never asked for that. The engineer who raised the pull request cannot explain where the rule came from either. She prompted for the endpoint, read the output, thought it looked reasonable, and shipped it."),

    ("p", "Nothing here is broken. The code works exactly as written. What went wrong is that <em>nobody chose this behaviour</em>, and the team is now maintaining business logic that arrived by autocomplete. That failure has no error message, no failing test and no bad reviewer. It has a three-week delay and somebody else's pager."),

    ("h2", "Why review stops working"),
    ("p", "Reviewing code and reviewing decisions are different activities, and generated code makes them easy to confuse. When a person writes something unusual, the oddity is a signal — they had a reason, and the reviewer asks about it. When a model writes something unusual, the oddity means nothing at all, because there was no reason. It was a plausible continuation."),

    ("p", "So the reviewer's usual instrument stops reading. Approving output that looks correct is not the same as approving a decision, and if there is no decision underneath, review has quietly become proofreading. The output arrives with the surface features of considered work — structure, handled edge cases, tests — and none of the substance."),

    ("terms", [
      ("Decided behaviour", "Someone can say why",
       "A person chose it, for a reason that survives being asked about, and the reason is recoverable later from a specification, a decision record or a commit message."),
      ("Invented behaviour", "Plausible, and unowned",
       "It appeared because it was a likely continuation. It may be sensible. Nobody weighed it, nobody can defend it, and nobody knows what it was trading off."),
      ("The delay", "Weeks, and it lands on someone else",
       "Invented behaviour is not detected at review, because it looks like the rest. It is detected in production by whoever is on call, which is the most expensive place and the least equipped person."),
    ]),

    ("know",
     "Generated code arrives with the appearance of considered work and none of the substance.",
     "Structure, error handling, naming and tests are the signals a reviewer uses to judge whether someone thought carefully. A model produces all of them regardless of whether anything was thought about, so the correlation those signals rely on is broken. This is why AI-assisted review degrades into rubber-stamping without anyone deciding to lower their standards — the instrument stopped measuring what it used to measure, and nothing announced it.",
     "The practical test is not &ldquo;is this code good&rdquo; but &ldquo;can anyone say why it does this?&rdquo; Ask it of any behaviour a specification did not require. If the answer is that it looked reasonable, the behaviour is unowned, whatever its quality."),

    ("figure", "The same output arrives by two routes. Review can distinguish them only if the intent was recorded somewhere before the code existed — afterwards the two are indistinguishable, which is why the check has to happen upstream.", '''<svg viewBox="0 0 640 204" role="img" aria-label="Decided and invented behaviour arriving at the same review"><defs><marker id="dec" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" class="d-fill-accent"/></marker></defs>
<rect x="14" y="18" width="196" height="46" rx="6" class="d-box"/><text x="26" y="38" class="d-label-b">intent, written down</text><text x="26" y="55" class="d-label-sm">spec, decision record, issue</text>
<path d="M210 41 L286 76" class="d-arrow-accent" marker-end="url(#dec)"/>
<rect x="14" y="112" width="196" height="46" rx="6" class="d-box-accent"/><text x="26" y="132" class="d-label-b">a plausible continuation</text><text x="26" y="149" class="d-label-sm">nobody weighed it</text>
<path d="M210 135 L286 100" class="d-arrow-accent" marker-end="url(#dec)"/>
<rect x="286" y="66" width="160" height="44" rx="6" class="d-box"/><text x="298" y="86" class="d-label-b">the same diff</text><text x="298" y="103" class="d-label-sm">clean, tested, plausible</text>
<path d="M446 88 L510 88" class="d-arrow-accent" marker-end="url(#dec)"/>
<rect x="510" y="66" width="116" height="44" rx="6" class="d-box"/><text x="522" y="92" class="d-label-sm">review</text>
<text x="14" y="192" class="d-label-sm">By the time it reaches review the two are the same object. The distinction exists only upstream of it.</text>
</svg>'''),

    ("h2", "What actually helps"),
    ("ul", [
      "<strong>Prompt for the decision, not the implementation.</strong> Asking for options with trade-offs produces something to choose between; asking for the endpoint produces something to accept. The first leaves a decision in the transcript, the second leaves an artefact.",
      "<strong>Write the intent before the code exists.</strong> The specification lesson that follows is this in practice, and its value here is specifically that it gives review something to check the diff <em>against</em>.",
      "<strong>Review behaviour, not lines.</strong> The question is what this now does that it did not do before, and whether anyone asked for each of those things.",
      "<strong>Treat unexplained behaviour as a defect.</strong> Not necessarily wrong — unowned. A behaviour nobody can justify is one nobody can safely change either, which is how it survives to become load-bearing.",
    ]),

    ("callout", "matters", "The cost is deferred, which is why it accumulates",
     "<p>Nothing punishes you at the moment this happens. The code works, the tests pass, the feature ships and the sprint looks good. The bill arrives later as a codebase whose behaviour nobody can account for, one plausible addition at a time — and by then the person who could have explained any single piece has long moved on to the next ticket.</p>"),
    ("related", ["what-ai-makes-worse", "spec-driven-development", "version-control-basics", "when-scaffolding-turns"]),
    ("quiz", [
      ("Why does a reviewer's usual judgement work less well on generated code?",
       ["Generated code contains subtler bugs than hand-written code",
        "Structure, error handling and tests normally signal that someone thought carefully — a model produces them regardless, so the signal no longer means what it did",
        "Reviewers read generated code faster and less carefully"],
       1),
      ("What makes unexplained behaviour a defect even when it is correct?",
       ["It is likely to be wrong in edge cases nobody tested",
        "Nobody can justify it, which means nobody can safely change it either — so it survives and becomes load-bearing",
        "It usually indicates the specification was incomplete"],
       1),
      ("What is the practical test proposed for any behaviour a specification did not require?",
       ["Whether it is covered by a test",
        "Whether anyone can say why it does that — if the answer is that it looked reasonable, it is unowned",
        "Whether it matches the conventions of the surrounding code"],
       1),
    ]),
  ],
},
{
  "slug": "what-ai-makes-worse",
  "title": "What AI Makes Worse",
  "subtitle": "You do not need to want to be a software engineer. You do need the parts of it that generation puts under pressure.",
  "body": [
    ("p", "This is the one lesson here that is not about models. If your goal is to build with them rather than to become a software engineer, it is tempting to treat everything below as somebody else's discipline — and that instinct is right about most of software engineering and wrong about a specific slice of it. Generation does not put uniform pressure on a codebase. It puts a great deal on four things, and those four are the ones worth knowing regardless of what you aspire to."),

    ("h2", "The four it presses on"),
    ("terms", [
      ("Comprehension, not typing", "The bottleneck moved",
       "Producing code stopped being the limit; understanding it did not get faster. A change you can generate in a minute and would need an hour to verify has not saved fifty-nine minutes — it has moved the cost somewhere less visible and usually onto someone else."),
      ("Undecided behaviour", "It accumulates quietly",
       "The previous lesson in full. Each plausible addition is individually fine and the sum is a system whose behaviour nobody can account for."),
      ("Coupling", "Adding got cheaper; untangling did not",
       "When writing a new call, a new field or a new dependency costs almost nothing, more of them get written. Every one is a connection that something later has to reason about, and the cost of removing one has not fallen at all."),
      ("The maintenance horizon", "It arrives sooner",
       "Code you did not write is code you have to maintain. Generation shortens the distance between a system being new and a system being legacy, because legacy means nobody remembers the reasoning, and the reasoning was never held by a person to begin with."),
    ]),

    ("know",
     "Generation multiplies output. It does not multiply the capacity to understand output.",
     "Everything difficult about a codebase scales with how much of it there is and how connected it is — reading it, changing it safely, onboarding someone, finding why it does something. Those costs were always there and were bounded by how fast people could type. Removing that bound does not remove the costs; it removes the thing that was limiting them, which is a different and much less comfortable situation.",
     "The useful question before accepting a generated change is not whether it works. It is whether you could explain it to someone in a month, and whether you would notice if it were subtly wrong. If both answers are no, the change has added capability and subtracted control."),

    ("figure", "Only one of these got faster. The uncomfortable part is that it was the one that used to set the pace for everything else.", '''<svg viewBox="0 0 640 176" role="img" aria-label="What generation accelerated and what it did not"><rect x="14" y="20" width="290" height="118" rx="8" class="d-box-accent"/>
<text x="28" y="46" class="d-label-b">much faster now</text>
<text x="28" y="76" class="d-label-sm">writing code</text>
<text x="28" y="100" class="d-label-sm">adding a dependency, a field, a call</text>
<rect x="336" y="20" width="290" height="118" rx="8" class="d-box"/>
<text x="350" y="46" class="d-label-b">exactly as slow as before</text>
<text x="350" y="70" class="d-label-sm">reading and understanding it</text>
<text x="350" y="90" class="d-label-sm">changing it without breaking things</text>
<text x="350" y="110" class="d-label-sm">explaining why it does that</text>
<text x="14" y="166" class="d-label-sm">The bottleneck did not disappear. It moved to the column nobody measures.</text>
</svg>'''),

    ("h2", "The minimum, for anyone"),
    ("ul", [
      "<strong>Be able to explain what you shipped.</strong> Not line by line — what it does, why it does that, and what you would look at first if it misbehaved.",
      "<strong>Prefer fewer connections.</strong> When something can be done with one less call into another part of the system, do that. This is most of what &ldquo;good design&rdquo; means in practice and it needs no vocabulary.",
      "<strong>Leave the reasoning behind.</strong> A commit message or a comment saying why, not what. The diff already says what. In six months the why is the only part that is gone.",
      "<strong>Make it reversible.</strong> Small changes, on branches, with a way back. Reversibility is worth more than correctness, because it is the thing that lets you be wrong cheaply.",
    ]),

    ("h2", "For engineers, or anyone who wants the deeper version"),
    ("p", "The four pressures above have proper names and a substantial literature, and if you are going to work on these systems for a while the vocabulary earns its place. This section is skippable if the previous one was enough."),

    ("terms", [
      ("Coupling and cohesion", "The pair that explains most design advice",
       "Coupling is how much one part must know about another; cohesion is how well the things inside one part belong together. Nearly every design guideline you will meet reduces to lowering the first or raising the second, and knowing that saves memorising the guidelines."),
      ("Interface as a contract", "The boundary is the promise",
       "What a component guarantees to callers, as distinct from how it currently achieves it. Generated code tends to reach through boundaries rather than across them, because the model can see everything and has no stake in what stays stable."),
      ("Technical debt, properly", "A deliberate loan, not a mess",
       "The term means a conscious trade — shipping something suboptimal now, knowing the interest. Code that is bad because nobody thought about it is not debt, it is just bad code, and calling it debt makes it sound like a decision was involved."),
      ("Refactoring under test", "Changing shape without changing behaviour",
       "Only meaningful when something can tell you the behaviour is unchanged. Without tests it is not refactoring, it is rewriting and hoping — a distinction that matters more when the code was generated, since nobody holds a mental model of what it did."),
      ("Legacy, defined usefully", "Code without a living rationale",
       "Not old code. Code whose reasoning is no longer held by anyone. On that definition generated code can be legacy the day it merges, which is the sharpest version of this lesson's point."),
    ]),

    ("callout", "insight", "The definition of legacy is the whole argument",
     "<p>If legacy means code whose reasoning nobody holds, then the speed at which a codebase becomes legacy is set by how much of its reasoning was ever held by a person. That is the connection between this lesson and the one before it — undecided behaviour is legacy on arrival, and the remedy in both cases is the same unglamorous act of writing down why before writing what.</p>"),
    ("related", ["deterministic-first", "code-nobody-decided", "when-scaffolding-turns", "the-apprenticeship-problem"]),
    ("quiz", [
      ("Why is comprehension described as the new bottleneck?",
       ["Models generate code faster than compilers can build it",
        "Producing code got much faster while reading, verifying and changing it did not, so the constraint moved to the part nobody measures",
        "Generated code is harder to read than hand-written code"],
       1),
      ("On the definition given, what makes code legacy?",
       ["Its age, and whether the original authors have left",
        "That nobody holds its reasoning any more — on which basis generated code can be legacy the day it merges",
        "The absence of tests covering it"],
       1),
      ("Why is calling careless code \"technical debt\" misleading?",
       ["Debt implies it can be repaid, and some code cannot be",
        "Debt means a conscious trade with known interest — code that is bad because nobody thought about it involved no decision at all",
        "The metaphor understates how expensive it is to fix"],
       1),
    ]),
  ],
},
{
  "slug": "spec-driven-development",
  "title": "Vibe Coding and Spec-Driven Development",
  "subtitle": "A spectrum, not a binary — and the question that tells you where on it a task belongs.",
  "body": [
    ("p", "When an agent writes the code, the most leveraged thing a person produces is no longer the code. It is whatever the agent works from. That observation has hardened into a named discipline, and it is worth understanding as a spectrum rather than as a doctrine, because both ends of the spectrum are correct for different work."),

    ("h2", "The two ends"),
    ("p", "<strong>Vibe coding</strong> is describing what you want, accepting what comes back, and iterating by reaction. It is fast, it has almost no ceremony, and it is genuinely the right mode for a prototype, a script, or anything you will read once and throw away."),
    ("p", "Its failure mode is documented and specific: output that is plausible and drifts from intent, invented APIs, and decay as the project grows — because nothing durable records what the thing was supposed to do, so each session re-derives intent from whatever is currently in context."),
    ("p", "<strong>Spec-driven development</strong> inverts the artifact order. A written, version-controlled specification is the source of truth; an implementation plan is derived from it; the plan is broken into tasks; code is generated last. When requirements change you edit the spec and regenerate, rather than editing code and hoping the spec catches up."),

    ("figure", "The spectrum, and what you buy at each point. Cost rises left to right and so does durability. Neither end is the answer — the task decides.", '''<svg viewBox="0 0 640 210" role="img" aria-label="Spectrum from vibe coding to spec-driven development">
<line x1="30" y1="120" x2="610" y2="120" class="d-arrow"/>
<rect x="20" y="46" width="140" height="56" rx="6" class="d-box-good"/>
<text x="34" y="68" class="d-label-b">Vibe</text>
<text x="34" y="86" class="d-label-sm">describe, accept, iterate</text>
<rect x="184" y="46" width="140" height="56" rx="6" class="d-box"/>
<text x="198" y="68" class="d-label-b">Prompt + tests</text>
<text x="198" y="86" class="d-label-sm">intent encoded as checks</text>
<rect x="348" y="46" width="140" height="56" rx="6" class="d-box"/>
<text x="362" y="68" class="d-label-b">Design note</text>
<text x="362" y="86" class="d-label-sm">approach agreed first</text>
<rect x="500" y="46" width="128" height="56" rx="6" class="d-box-accent"/>
<text x="514" y="68" class="d-label-b">Full spec</text>
<text x="514" y="86" class="d-label-sm">spec → plan → tasks</text>
<text x="20" y="146" class="d-fill-green" font-size="11" font-weight="600">minutes of overhead</text>
<text x="20" y="164" class="d-label-sm">throwaway · exploratory · one reader</text>
<text x="470" y="146" class="d-fill-accent" font-size="11" font-weight="600">hours of overhead</text>
<text x="386" y="164" class="d-label-sm">multi-session · multi-person · long-lived</text>
<text x="20" y="196" class="d-label-sm">The mistake is picking a point by taste rather than by task. Both ends are right somewhere.</text>
</svg>'''),

    ("h2", "The question that decides"),
    ("callout", "matters", "How many times will intent need to survive being forgotten?", "That is the whole test. A script you write and run once: never — vibe it. A feature built across four sessions, by two people and an agent, that someone will modify next quarter: many times, and every one of those is an opportunity for intent to drift. The spec is not documentation overhead. It is the mechanism by which intent survives a context window ending."),
    ("p", "Notice this is the same argument as the architecture decision record (ADR) from the artifacts lesson, applied forward instead of backward. An ADR records why a decision was made so nobody re-litigates it. A spec records what is being built so nobody re-derives it. Both exist because a model's context does not persist and a person's memory is worse than they think."),

    ("h2", "Why it works better with agents than it ever did with people"),
    ("p", "Specification-first is an old idea with a poor track record — waterfall's central failure was that specs went stale the moment implementation began, and nobody read them. Two things changed:"),
    ("ul", [
      "<strong>Regeneration is now cheap.</strong> The reason specs went stale was that updating the spec and updating the code were two expensive efforts, so only one happened. When code generation is minutes, editing the spec and regenerating is a real workflow rather than an aspiration.",
      "<strong>The reader is tireless and literal.</strong> A human implementer skims a forty-page spec. An agent reads all of it, every time, and will faithfully implement an ambiguity you would have silently resolved. That is both the strength and the trap.",
    ]),
    ("callout", "pitfall", "The trap in that second point", "An agent implementing a spec cannot tell the difference between a decision you made and a sentence you wrote carelessly. Every under-specified area becomes an invented answer, delivered confidently and consistently. Waterfall's specs were ignored; these are followed exactly, which surfaces vagueness as working code rather than as questions. Expect to discover what you actually meant by reading what you got."),

    ("h2", "What a workable spec contains"),
    ("terms", [
      ("The decision, not the prose", "What changes for whom", "A spec that reads like a brochure produces code that reads like a brochure."),
      ("Acceptance criteria", "Checkable, not aspirational", "\"Fast\" is not a criterion. \"p95 under 400ms on the existing fixture set\" is."),
      ("Explicit non-goals", "What this does not do", "The highest-value section, and the one most often missing. It is what stops an agent helpfully expanding scope."),
      ("Constraints and prior decisions", "The things it may not change", "Link the ADRs. An agent that does not know a constraint exists will cheerfully violate it."),
      ("Open questions", "Named, not silently resolved", "Anything you have not decided should be marked as undecided, or it will be decided for you."),
    ]),

    ("h2", "Where it fits with everything else here"),
    ("p", "The spec is not a fifth kind of artifact so much as the fourth member of a family you already know. The harness is executed by a machine; a recipe is followed by a person; an ADR is consulted when someone wants to know why they cannot do the obvious thing; a spec is what an agent builds from. And all four share the failure mode from the artifacts lesson — <strong>true when written, still asserting itself after its truth expired</strong>. A stale spec is worse than none, because it carries authority."),
    ("p", "It also composes with the loops material. A spec with checkable acceptance criteria is an external verifier, which is precisely what makes a build-test-fix loop work rather than spin. Spec-driven development and verifier-guided looping are the same idea meeting from opposite directions: one supplies the signal, the other consumes it."),

    ("h2", "The honest position"),
    ("p", "The methodology is young, the tooling is proliferating faster than the evidence, and much of what is written about it is advocacy. Treat claims about productivity gains the way you would treat any unmeasured claim in this course — as a hypothesis with a plausible mechanism. The mechanism here is sound, which is a reason to try it, not a reason to believe a number."),
    ("p", "The defensible version is modest and probably enough: when intent must survive multiple sessions, write it down before generating; keep it in version control; keep it current or delete it. Everything past that is tooling preference."),

    ("know",
     'An agent cannot tell a decision you made from a sentence you wrote carelessly.',
     "Waterfall's specs were ignored; these are followed exactly. Every under-specified area becomes an invented answer, delivered confidently and consistently, so vagueness surfaces as working code rather than as questions.",
     'Your spec says the export should handle large files. You meant streaming rather than loading into memory. The agent implemented a 100MB size limit with a clear error message — a reasonable reading, faithfully built, and not what you wanted. You discovered what you meant by reading what you got.'),
    ("related", ["three-artifacts", "rungs-and-experiments", "code-nobody-decided", "how-to-measure"]),
    ("links", [
      ("GitHub Spec Kit", "https://github.com/github/spec-kit",
       "The open-source toolkit that popularised the four-phase workflow. Agent-agnostic and CLI-first — the easiest place to see the shape of it."),
      ("Spec-Driven Development: a spec-first approach — Microsoft", "https://developer.microsoft.com/blog/spec-driven-development-ai-native-engineering/",
       "The rationale written out, including the honest account of why specification-first failed the first time."),
    ]),

    ("quiz", [
      ("What is the test for how much specification a task needs?",
       ["The size of the codebase it touches",
        "How many times intent will need to survive being forgotten — across sessions, people and months",
        "Whether the code will be reviewed by a human"], 1),
      ("Why did specification-first fail in the waterfall era but work better with agents?",
       ["Agents write better specifications than people did",
        "Regeneration is now cheap, so editing the spec and regenerating is a real workflow rather than an aspiration",
        "Modern specs are shorter"], 1),
      ("What happens to an under-specified area of a spec when an agent implements it?",
       ["The agent flags it as ambiguous and asks",
        "It becomes an invented answer, delivered confidently and consistently — vagueness surfaces as working code, not as questions",
        "The agent implements the most common convention"], 1),
      ("Which section of a spec is most often missing and most valuable?",
       ["The architecture diagram",
        "Explicit non-goals — what this does not do, which is what stops an agent helpfully expanding scope",
        "The list of files to be changed"], 1),
    ]),
  ],
},
{
  "slug": "version-control-basics",
  "title": "Version Control, and Why Agents Make It Non-Optional",
  "subtitle": "Git and GitHub from zero — plus the argument for why this matters more now, not less.",
  "body": [
    ("p", "If you have never used version control, this is the lesson that unlocks several others: the course has already told you to commit at phase boundaries, to revert a fix to confirm it caused the improvement, and to isolate agent work on a branch. All three assume git. Here is enough to do them."),

    ("h2", "The idea, in one paragraph"),
    ("p", "Git records snapshots of your project over time. Each snapshot — a <strong>commit</strong> — captures every file as it stood, with a message saying why. You can compare any two, return to any one, and work on several versions at once without them interfering. GitHub is a hosted copy of that history, which gives you a backup, a place to collaborate, and somewhere to review changes before they land."),

    ("h2", "The seven commands that cover most days"),
    ("code", """git status                    # what has changed but is not yet saved
git diff                      # exactly what changed, line by line
git add .                     # stage the changes you want in the next snapshot
git commit -m "fix: ..."      # take the snapshot, with a reason
git log --oneline             # the history, one line per commit
git push                      # send commits to GitHub
git pull                      # bring down what others (or another machine) pushed"""),
    ("callout", "matters", "Run the first two before every commit", "<code>git status</code> and <code>git diff</code> take five seconds and prevent the two commonest mistakes: committing something you did not mean to (a key, a large data file, a debugging change), and committing only half of a change because the other half was never staged. A feature that ships with its configuration flag but not the code that reads the flag is a real and common bug — the flag exists, nothing uses it, and no test fails."),

    ("h2", "Branches"),
    ("p", "A <strong>branch</strong> is an independent line of work. You start one, make commits on it, and the main line is untouched until you deliberately merge. This is what lets you try something risky without endangering anything that works."),
    ("code", """git switch -c feat/turbine-baseline   # start a branch and move onto it
# ... work, commit, work, commit ...
git push -u origin feat/turbine-baseline
# open a pull request on GitHub, review the diff, merge

git switch main && git pull            # back to the main line, now updated"""),
    ("p", "A <strong>pull request</strong> is a proposal to merge a branch, with the full diff laid out for review and discussion. Even working alone it is worth using, because reading your own change as a diff — separated from the act of writing it — catches things nothing else does."),

    ("h2", "Why this matters more with an agent, not less"),

    ("figure", "Without version control an agent's changes accumulate into one indivisible blob you can only accept or abandon. With it, every step is a place you can return to, and the diff is the review surface.", '''<svg viewBox="0 0 640 200" role="img" aria-label="Agent work with and without version control">
<text x="12" y="18" class="d-fill-red" font-size="12" font-weight="600">NO VERSION CONTROL</text>
<rect x="12" y="30" width="290" height="52" rx="6" class="d-box-warn"/>
<text x="28" y="52" class="d-label-sm">40 files changed across 3 hours</text>
<text x="28" y="70" class="d-label-sm">accept all of it, or lose all of it</text>
<text x="12" y="112" class="d-fill-green" font-size="12" font-weight="600">WITH VERSION CONTROL</text>
<circle cx="30" cy="146" r="7" class="d-fill-green"/>
<circle cx="98" cy="146" r="7" class="d-fill-green"/>
<circle cx="166" cy="146" r="7" class="d-fill-green"/>
<circle cx="234" cy="146" r="7" class="d-fill-red"/>
<circle cx="302" cy="146" r="7" class="d-fill-muted"/>
<line x1="30" y1="146" x2="302" y2="146" stroke="var(--border)" stroke-width="2"/>
<text x="12" y="176" class="d-label-sm">good · good · good · broke it · return here</text>
<path d="M234 158 Q200 182 172 160" stroke="var(--accent)" stroke-width="1.8" fill="none"/>
<rect x="340" y="30" width="288" height="140" rx="7" class="d-box"/>
<text x="356" y="52" class="d-label-b">What the history buys you</text>
<text x="356" y="74" class="d-label-sm">· the diff is how you review agent output</text>
<text x="356" y="94" class="d-label-sm">· revert the fix, re-run, confirm it was the fix</text>
<text x="356" y="114" class="d-label-sm">· branches isolate risky autonomous work</text>
<text x="356" y="134" class="d-label-sm">· bisect finds which change broke it</text>
<text x="356" y="154" class="d-label-sm">· the log says what changed when a run regressed</text>
</svg>'''),

    ("ul", [
      "<strong>The diff is your review surface.</strong> You did not write the code, so reading it as a diff is how you actually review it. Without commits there is no diff, only a changed working tree.",
      "<strong>Reverting is a measurement technique.</strong> The measurement checklist ends with removing the fix and re-running to confirm the number moves back. That step is impossible without version control, which is why it is the step people skip.",
      "<strong>Branches are isolation.</strong> An agent working autonomously on a branch cannot damage anything that works. This is the cheapest safety control available for unattended runs.",
      "<strong>Bisect finds the culprit.</strong> When something broke somewhere in forty commits, <code>git bisect</code> finds which one by binary search rather than by guesswork.",
      "<strong>Commits are the incident timeline.</strong> When an agent's behaviour regresses and nothing on your side changed, the log is the first place to check whether that is actually true.",
    ]),
    ("callout", "insight", "Commit more often than feels necessary", "The course tells you to commit at every phase boundary rather than at feature end, and agent work makes the case stronger. A three-hour autonomous run that produces one enormous commit is nearly unreviewable; the same work as twelve commits is a sequence you can read, and revert partially. Reverting from a clean checkpoint costs nothing. Reverting from a snarl costs an afternoon."),

    ("h2", "Three habits worth forming immediately"),
    ("terms", [
      ("Write why, not what", "The diff already says what", "\"fix: reject empty vibration readings before scaling\" beats \"updated file\". Six weeks later, only one of those helps."),
      ("Never commit secrets", "Once pushed, treat as leaked", "A <code>.env</code> in <code>.gitignore</code> before the first commit. History is hard to scrub and mirrors already exist."),
      ("Keep data out", "Large files bloat forever", "Git stores every version of everything. A 400MB CSV committed once is in the history permanently. Generate data from a seeded script instead — which is how the Block 1 dataset works."),
    ]),

    ("h2", "The two commands worth being careful with"),
    ("p", "<code>git push --force</code> rewrites history on a shared branch and can destroy someone else's work. <code>git reset --hard</code> discards uncommitted changes irrecoverably. Both have legitimate uses and neither should be typed reflexively. Everything else in git is recoverable, which is worth knowing when you are new — the fear of breaking something is mostly unfounded."),

    ("h2", "What GitHub adds"),
    ("p", "Beyond hosting: pull requests for review, issues for tracking work, and Actions for running your tests automatically on every push. That last one connects directly to the evaluation material — a benchmark that runs itself on every change is the difference between measuring occasionally and measuring always."),
    ("related", ["three-artifacts", "code-nobody-decided", "the-artifact-and-when-to-retrain", "spec-driven-development"]),
    ("links", [
      ("Git Book — chapters 1 to 3", "https://git-scm.com/book/en/v2",
       "Free and genuinely the best reference. The first three chapters cover everything above properly."),
      ("GitHub Quickstart", "https://docs.github.com/en/get-started/quickstart",
       "Account through first pull request, with the interface shown."),
      ("Conventional Commits", "https://www.conventionalcommits.org/",
       "The message format used throughout this course — type(scope): description. Machine-readable, so tooling can derive changelogs from it."),
    ]),

    ("quiz", [
      ("Why is reverting a change a measurement technique rather than just a recovery tool?",
       ["It restores a known-good state after a failed experiment",
        "Removing the fix and re-running confirms the fix was what moved the number — otherwise you have learned the wrong lesson",
        "It reduces the size of the repository"], 1),
      ("An agent runs autonomously for three hours. What should the output look like in git?",
       ["One commit, so the change is atomic and easy to revert",
        "Many commits, so the work is reviewable as a sequence and can be reverted partially",
        "No commits until a human has reviewed everything"], 1),
      ("What should you run before every commit?",
       ["git log, to see recent history",
        "git status and git diff — they catch unintended files and half-staged changes",
        "git pull, to avoid conflicts"], 1),
      ("Why keep large data files out of git?",
       ["GitHub rejects files over a size limit",
        "Git stores every version permanently, so a large file committed once bloats the history forever — generate it from a seeded script instead",
        "Binary files cannot be diffed"], 1),
    ]),
  ],
},
{
  "slug": "rungs-and-experiments",
  "title": "Rungs: Running Experiments on an Agent",
  "subtitle": "A ladder of progressively more assistance — and the only design that tells you where the wall actually is.",
  "body": [
    ("p", "You have a task an agent fails. You have a dozen ideas about why. Testing them one at a time takes a week and, worse, each result is ambiguous — a change that produces no improvement might be the wrong lever, or the right lever applied where a different problem was blocking."),
    ("p", "A <strong>rung</strong> is one configuration in an ordered ladder of increasing assistance. Run the same fixture across every rung and the pattern of where it starts passing localises the failure in a single sweep."),

    ("h2", "A ladder, bottom to top"),
    ("terms", [
      ("Bare", "The task, nothing else", "No scaffolding, no hints. If it passes here, everything above is unnecessary."),
      ("Test-first", "The failing test in context", "Supplies a checkable target. Passing here and not below means the agent could not work out what success looked like."),
      ("Reloop", "Failures fed back, retry allowed", "The verifier-guided loop. Passing here means it could not get it right first time but could correct itself given the signal."),
      ("Guards-off", "Budgets and limits relaxed", "Passing here means capability was never the issue — the harness was stopping it."),
      ("Decomposed", "Task pre-split into steps", "Passing here means the model could do each part and not the planning."),
      ("Oracle", "The answer, or most of it, supplied", "The control. Failing at this rung means the fixture or the rubric is broken, not the agent."),
    ]),

    ("figure", "Where a fixture starts passing is the diagnosis. Each rung isolates a different possible cause, and the top rung is a control on the instrument itself.", '''<svg viewBox="0 0 640 235" role="img" aria-label="A ladder of rungs and what each result means">
<rect x="12" y="14" width="300" height="30" rx="5" class="d-box"/><text x="26" y="34" class="d-label-sm">bare</text>
<text x="330" y="34" class="d-label-sm">passes → you had no problem</text>
<rect x="12" y="48" width="300" height="30" rx="5" class="d-box"/><text x="26" y="68" class="d-label-sm">+ test-first</text>
<text x="330" y="68" class="d-label-sm">passes → it could not tell what success was</text>
<rect x="12" y="82" width="300" height="30" rx="5" class="d-box"/><text x="26" y="102" class="d-label-sm">+ reloop</text>
<text x="330" y="102" class="d-label-sm">passes → needed feedback, not more capability</text>
<rect x="12" y="116" width="300" height="30" rx="5" class="d-box-accent"/><text x="26" y="136" class="d-label-sm">+ guards off</text>
<text x="330" y="136" class="d-accent">passes → the harness was the wall</text>
<rect x="12" y="150" width="300" height="30" rx="5" class="d-box"/><text x="26" y="170" class="d-label-sm">+ decomposed</text>
<text x="330" y="170" class="d-label-sm">passes → planning was the gap, not execution</text>
<rect x="12" y="184" width="300" height="30" rx="5" class="d-box-warn"/><text x="26" y="204" class="d-label-sm">oracle (control)</text>
<text x="330" y="204" class="d-fill-red" font-size="11" font-weight="600">fails → your fixture is broken</text>
<text x="12" y="228" class="d-label-sm">Never passes anywhere → a genuine capability limit, and now you have evidence rather than a suspicion.</text>
</svg>'''),

    ("know",
     "Where a task starts passing on the ladder is the diagnosis; a single failing run is not.",
     "One configuration failing is consistent with a dozen causes. A ladder turns an ambiguous zero into a located one, because each rung removes exactly one candidate explanation and the transition point names the cause.",
     "A fixture fails bare, fails test-first, fails reloop, and passes with guards off. That is not a model problem — the model could always do it, and a budget was stopping it before it got there. Nine experiments aimed at capability would all have measured flat."),

    ("h2", "Reading the ladder"),
    ("p", "The transitions carry the information, not the totals. Three patterns worth recognising:"),
    ("ul", [
      "<strong>Passes low, fails high.</strong> Almost always a bug in your ladder — a higher rung is supposed to be strictly more helpful. If added assistance makes things worse, that assistance is doing something you did not intend.",
      "<strong>Fails everywhere including the oracle.</strong> The fixture or the rubric is broken. Fix the instrument before drawing any conclusion about the agent.",
      "<strong>Passes only at the top.</strong> A real capability limit for this configuration. This is the only pattern that justifies reaching for a different model.",
    ]),
    ("callout", "matters", "The oracle rung is the one people leave out, and it is the one that saves you", "It is a control fixture doing its job continuously. Without it, a board of zeros is ambiguous between 'the agent cannot do this' and 'nothing could pass this fixture'. With it, that ambiguity resolves in one cell — and a broken fixture is far more common than people expect, because fixtures are written once and never tested against a known-good answer."),

    ("h2", "Running the sweep honestly"),
    ("terms", [
      ("Same fixtures on every rung", "Non-negotiable", "Change the tasks between rungs and you are comparing nothing."),
      ("Repeats per cell", "Three at minimum", "Agent runs are stochastic. A single run per cell gives you a board of coin flips presented as a table."),
      ("One variable per rung", "Strictly cumulative", "Each rung adds exactly one thing to the one below. Two changes at once and the transition tells you nothing."),
      ("Record the manifest", "Per cell", "Model, budgets, verification state, config version. Otherwise a surprising cell cannot be investigated later."),
      ("Classify non-completions", "Before aggregating", "An infrastructure error is not a failure to solve the task, and mixing them corrupts every cell it touches."),
    ]),

    ("know",
     "One run per cell produces a board of coin flips formatted as a table.",
     "Agent runs vary between attempts for reasons that have nothing to do with your treatment — sampling, retrieval order, timing. Without repeats you cannot distinguish a real transition between rungs from noise, and the tidy grid makes the result look more solid than it is.",
     "A smoke run on one fixture showed a difference of +1.00 between two conditions — one passed and one failed, which on a single fixture is the largest gap arithmetically available and looks decisive. The full seven-fixture run showed +0.00. Nothing about the single-run result signalled that it was unrepresentative, and it had already been written up."),

    ("h2", "When to stop climbing"),
    ("p", "The ladder is a diagnostic, not a product. Once you know which rung fixes the task you have your answer, and the engineering question becomes whether that rung is affordable in production. Guards-off is a diagnosis, not a configuration you ship. Decomposition that works in a benchmark may be too slow for an interactive path."),
    ("p", "That gap — between what makes the fixture pass and what you can actually run — is itself a finding worth recording. It tells you the size of the problem you still have."),

    ("h2", "The connection to everything else"),
    ("p", "This is the control-fixture idea from the localising lesson, made systematic. It is also the one-treatment-at-a-time rule from the measurement checklist, applied as a design rather than as discipline: because each rung differs by exactly one thing, the sweep is a set of controlled comparisons run in parallel rather than a sequence of experiments run over a fortnight."),
    ("related", ["localising-a-failure", "how-to-measure", "confounds-you-cannot-see", "spec-driven-development"]),
    ("links", [
      ("SWE-bench experiments", "https://github.com/swe-bench/experiments",
       "Submissions differing in scaffold on identical tasks — the same comparison as a rung ladder, run across teams instead of within one."),
      ("Building effective agents — Anthropic", "https://www.anthropic.com/engineering/building-effective-agents",
       "The argument for the simplest scaffold that works, which is what a ladder is for finding."),
    ]),

    ("quiz", [
      ("A fixture fails bare, test-first and reloop, and passes with guards off. What does that establish?",
       ["The model lacks the capability and needs upgrading",
        "The model could always do it — a budget or limit was stopping it before it got there",
        "The fixture is too difficult and should be split"], 1),
      ("Your ladder shows a task passing at a low rung and failing at a higher one. What does that mean?",
       ["The higher rung is genuinely harder",
        "Your ladder has a bug — higher rungs are supposed to be strictly more helpful",
        "The result is within normal variance"], 1),
      ("Why include an oracle rung where most of the answer is supplied?",
       ["To establish an upper bound on achievable score",
        "As a control — if it fails there, the fixture or rubric is broken rather than the agent",
        "To give weaker models something they can pass"], 1),
      ("Why are three repeats per cell the minimum?",
       ["To average out slow network calls",
        "Agent runs are stochastic, so a single run per cell cannot distinguish a real transition from noise",
        "Most benchmarks require it for submission"], 1),
    ]),
  ],
},
{
  "slug": "tracking-runs-and-automating-evals",
  "title": "Tracking Runs, and Running the Evals Automatically",
  "subtitle": "The measurement discipline this course teaches does not survive contact with fifty experiments unless something records them for you.",
  "body": [
    ("p", "Two lessons in this set already argue that a result you cannot locate is not a result: record the model, the configuration, the seed, the data version and the per-item outcomes, so that months later you can tell <em>never tried</em> from <em>tried and failed</em>. That discipline is correct and it is described as something you do by hand. By hand it works for five runs. At fifty it quietly stops happening, and the first symptom is somebody re-running an experiment that was settled six weeks ago because nobody could find the answer."),

    ("h2", "What a tracking server is for"),
    ("p", "An experiment tracker is a database with a run as its unit. Each run carries its parameters, its metrics, its artefacts and its timestamp, and the point is not the recording &mdash; it is that runs become <em>comparable</em> without you having planned the comparison in advance. Sorting forty runs by a metric, or asking which configuration produced the best result at a given cost, is the operation a directory of notebook outputs cannot do."),

    ("callout", "matters", "This repository has had one running the whole time",
     "<p>The lab containers are started with a tracking URI already pointing at an MLflow server, the compose file marks it for the classical-ML and fine-tuning blocks, and it serves a web interface on the machine you are reading this on. It has been available since the environments were built. If you have been keeping run notes in a cell at the bottom of a notebook, the thing that replaces them is already up.</p>"),

    ("terms", [
      ("Parameters", "The inputs you chose",
       "Model, configuration, learning rate, rank, prompt version, retrieval depth. Anything you would have to state to repeat the run."),
      ("Metrics", "The numbers it produced",
       "Logged over time rather than once, so a training curve is visible and a run that diverged is obvious at a glance rather than after re-reading a log."),
      ("Artefacts", "The things it made",
       "The adapter, the confusion matrix, the per-item results file. Held with the run that produced them, which is the part that makes a result auditable months later."),
      ("The code version", "The field people omit",
       "A commit hash logged alongside the run. Without it the parameters describe an experiment you can no longer reconstruct, because the code they were passed to has moved."),
    ]),

    ("know",
     "The value is not in logging the runs. It is in being able to compare runs you did not plan to compare.",
     "Anyone will record the experiment they are running now, because they care about it now. The question a tracker answers is the one that arrives later and unbidden: did we already try this, what did the version from before the refactor score, which of these forty configurations was best on cost rather than on accuracy. Notes written for your present self do not answer those, because your present self did not know they would be asked.",
     "A team spends two days tuning retrieval depth and settles on eight chunks. Four months later, after a chunking change, somebody asks whether eight is still right. With a tracker it is a query against runs that already exist. Without one it is two days again, and the second answer is not comparable with the first because the corpus moved in between."),

    ("h2", "The eval battery belongs in continuous integration"),
    ("p", "This course builds an evaluation battery and argues at length that measurement is what separates a claim from a result. It then leaves the battery to be run by a person who remembers to run it &mdash; which in practice means it runs when someone is confident enough to check, and that is exactly the wrong distribution of moments."),
    ("p", "Automating it is the same argument as the harness: a check that depends on discipline gets skipped under deadline, and a check that runs itself does not. The complication is that these evaluations are not unit tests. They cost money, they take minutes rather than milliseconds, and they do not return the same answer twice."),

    ("figure", "Three tiers, by what they cost. The cheap deterministic layer runs on every push; the expensive layer runs where it is worth waiting for.", '''<svg viewBox="0 0 540 158" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Three tiers of automated checks: fast deterministic on every push, sampled eval on pull requests, full battery before release.">
<rect x="10" y="16" width="330" height="34" rx="5" class="d-box-good"/>
<text x="24" y="38" class="d-label-sm">schema, parsing, refusal paths, golden fixtures &#8212; no model call</text>
<text x="352" y="38" class="d-label-sm">every push, seconds</text>
<rect x="10" y="58" width="330" height="34" rx="5" class="d-box"/>
<text x="24" y="80" class="d-label-sm">sampled evaluation set, fixed seed, threshold with spread</text>
<text x="352" y="80" class="d-label-sm">every pull request</text>
<rect x="10" y="100" width="330" height="34" rx="5" class="d-box-accent"/>
<text x="24" y="122" class="d-label-sm">full battery, adversarial suite, judged dimensions</text>
<text x="352" y="122" class="d-label-sm">before release, nightly</text>
<text x="10" y="150" class="d-label-sm">cost rises down the stack, so the gate that blocks a merge should be near the top of it</text>
</svg>'''),

    ("know",
     "A gate that flakes gets disabled, and it takes the discipline with it.",
     "The first time an evaluation fails on a change that was fine, somebody re-runs it and it passes. The second time, somebody adds a retry. The third time it is marked non-blocking and it never blocks anything again &mdash; and the damage is not the lost check, it is that the team has now learned the evaluations are noise. A threshold set without knowing the run-to-run spread guarantees this, which is why the repeats this course insists on are load-bearing here rather than pedantic.",
     "An evaluation scoring 0.82 with a run-to-run spread of plus or minus 0.03 is gated at 0.82. It fails roughly half the time on changes that did nothing. Gated at 0.75 it fails when something is actually wrong, which is the only failure anyone will keep paying attention to."),

    ("callout", "pitfall", "Two things that make an automated evaluation lie",
     "<p><strong>The eval set leaks into the work.</strong> Running the same set on every pull request for six months means every developer has seen its failures and fixed toward them. That is the tuning-against-the-test-set problem from the overfitting lesson, arriving through automation, and the defence is the same: hold a portion back that only runs before release, and never show it in a pull-request comment.</p><p><strong>Nobody reads a green tick.</strong> An evaluation that reports only pass or fail throws away the number, so a metric sliding from 0.88 to 0.79 over two months passes every check on the way down. Record the value to the tracker on every run and watch the series, not the tick.</p>"),

    ("h2", "What this costs, honestly"),
    ("p", "Every automated run of a model-backed evaluation is a bill and a wait, and a team that puts the full battery on every push will turn it off within a fortnight. Tier it by what a failure would cost you: the checks that need no model call are effectively free and should gate everything, a sampled set is affordable per pull request, and the full battery belongs on a schedule or a release. If the honest answer is that you cannot afford to run the evaluations often, that is worth knowing explicitly &mdash; it means the quality claims are being made on less evidence than the process implies."),
    ("related", ["how-to-measure", "eval-battery", "version-control-basics", "rungs-and-experiments"]),
    ("quiz", [
      ("What does an experiment tracker give you that careful notes do not?",
       ["A guarantee that runs are reproducible",
        "Comparability across runs you did not plan to compare — the question that arrives months later, which notes written for your present self cannot answer",
        "Automatic detection of when a result is statistically significant"],
       1),
      ("An automated evaluation is gated at exactly its observed score. What happens?",
       ["It correctly catches any regression, however small",
        "It fails often on changes that did nothing, gets retried, then marked non-blocking — and the team learns to treat the evaluations as noise",
        "It becomes more sensitive over time as the sample grows"],
       1),
      ("Why does running the same eval set on every pull request for months become a problem?",
       ["The set becomes stale relative to production traffic",
        "Everyone has seen its failures and fixed toward them, which is tuning against the test set arriving through automation",
        "Repeated runs accumulate cost without adding information"],
       1),
    ]),
  ],
},
{
  "slug": "the-artifact-and-when-to-retrain",
  "title": "The Artifact, and When to Retrain",
  "subtitle": "What actually ships is not the code — and the drift lesson tells you something moved without telling you what to do about it.",
  "body": [
    ("p", "Version control holds your code, and for ordinary software that is the whole system. For anything with a trained component it is roughly a quarter of it. What determines behaviour is a set of four things travelling together &mdash; the code, the weights or adapter, the data they were derived from, and the configuration they run under &mdash; and only the first is in the repository."),

    ("figure", "The code is versioned, and on its own it does not determine behaviour. Three other things have to be identified for a result to be reproducible or a rollback to be possible.", '''<svg viewBox="0 0 540 146" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Four components determine behaviour: code, weights, data and configuration.">
<rect x="10" y="20" width="118" height="44" rx="6" class="d-box-good"/>
<text x="69" y="40" class="d-label-b" text-anchor="middle">code</text>
<text x="69" y="56" class="d-label-sm" text-anchor="middle">in git</text>
<rect x="138" y="20" width="118" height="44" rx="6" class="d-box-accent"/>
<text x="197" y="40" class="d-label-b" text-anchor="middle">weights</text>
<text x="197" y="56" class="d-label-sm" text-anchor="middle">where?</text>
<rect x="266" y="20" width="118" height="44" rx="6" class="d-box-accent"/>
<text x="325" y="40" class="d-label-b" text-anchor="middle">data</text>
<text x="325" y="56" class="d-label-sm" text-anchor="middle">which version?</text>
<rect x="394" y="20" width="136" height="44" rx="6" class="d-box-accent"/>
<text x="462" y="40" class="d-label-b" text-anchor="middle">configuration</text>
<text x="462" y="56" class="d-label-sm" text-anchor="middle">prompt, thresholds</text>
<text x="10" y="92" class="d-label-sm">a commit hash identifies one of the four</text>
<text x="10" y="112" class="d-label-sm">rolling back the code while the other three stay put reverts almost nothing</text>
<text x="10" y="132" class="d-label-sm">so the artefact has to carry its own provenance, or the run cannot be reconstructed</text>
</svg>'''),

    ("h2", "What a trained artefact has to know about itself"),
    ("terms", [
      ("Its base", "What it was derived from",
       "For an adapter this is decisive: it is a difference against one specific base model at one specific version, and applied to a different base it is meaningless rather than merely worse."),
      ("Its data", "Which version, not which dataset",
       "The dataset moved between March and June. A record naming the dataset without naming the version identifies a family of possible training runs, which is not enough to reproduce one."),
      ("Its run", "The experiment that produced it",
       "A pointer back to the tracked run, so the parameters, metrics and evaluation results are attached rather than remembered."),
      ("Its evaluation", "Against the base, on the held-out set",
       "The numbers that justified shipping it, recorded with it. Otherwise the comparison that made the decision is gone by the time anyone questions the decision."),
    ]),

    ("know",
     "You can roll back code in seconds. Rolling back a model requires that the previous one still exists and can still be served.",
     "A code rollback is a pointer moving to a commit that is still there by construction. A model rollback is only as fast as the old artefact is retrievable &mdash; and if it was overwritten in place, produced by a training run nobody recorded, or depends on a base version the provider has since retired, there is nothing to go back to. The incident then becomes a training run, under time pressure, which is the worst circumstance in which to do one.",
     "A team replaces a fine-tuned classifier with a newer adapter and deletes the old one from the bucket, since it is in the repository&#39;s history. The new one is worse on a customer segment nobody sliced for. Recovery is a retrain, because the repository held the training <em>script</em> and neither the weights nor the exact data snapshot that produced them."),

    ("h2", "When to retrain, which the drift lesson deliberately left open"),
    ("p", "Detection was the subject there: what moved, and how you would know. This is the decision that detection exists to inform, and it has four common triggers with genuinely different failure modes."),

    ("terms", [
      ("On a schedule", "Simple, and wrong in both directions",
       "Monthly whether or not anything changed. Cheap to reason about, and it retrains when nothing moved while missing the week something did. Reasonable as a floor, poor as the only trigger."),
      ("On a drift threshold", "Responsive, and it needs a number you chose",
       "Fires when the input distribution has moved past a bound. Only as good as the threshold, which has to come from a period you know was healthy rather than from a default."),
      ("On a performance drop", "The one you actually care about",
       "The real signal, and it needs labels, which arrive late or never. Where they arrive late this is a trailing trigger: correct, and it tells you about a problem that has already been live for weeks."),
      ("On accumulated data", "Retrain when there is something new to learn",
       "Enough genuinely new examples to move the model. Predictable and cheap to compute, and it ignores whether the world changed &mdash; volume is not the same as novelty."),
    ]),

    ("know",
     "A retrain is a deployment, not a refresh, and it earns the same gate as any other change.",
     "The word makes it sound like maintenance &mdash; the same model, brought up to date &mdash; and it is not. It is a new model, trained on different data, which can be worse in ways the aggregate score will not show. Teams that would never ship a code change without review routinely promote a retrained model automatically, on the reasoning that the pipeline is unchanged. The pipeline is unchanged; the thing it produced is not.",
     "The rollout options are the ones deployment already gave you. Shadow the retrained model against live traffic before it serves anything, compare it to the incumbent on the same held-out set rather than to its own training metrics, and check the slices &mdash; because a retrain that improves the aggregate while losing a minority segment is the ordinary outcome of training on data the world has reweighted."),

    ("callout", "matters", "The cost nobody puts in the business case",
     "<p>The training run is usually the cheapest part. Each retrain also spends an evaluation cycle, a shadow period, a rollout and someone&#39;s attention, and if the model is judged rather than scored mechanically it spends human reading time too. A monthly retrain is a monthly evaluation commitment, and a team that budgets for the compute and not for that ends up promoting models on training metrics alone, which is the failure the evaluation block spends six lessons preventing.</p><p>The corollary is worth stating plainly: if you cannot afford to evaluate it, you cannot afford to retrain it. Retraining without evaluating is not maintenance, it is an unmeasured change to production made on a schedule.</p>"),

    ("h2", "When not to retrain"),
    ("ul", [
      "<strong>Drift detected, metric holding.</strong> The inputs moved and the model still performs. That is a model generalising, which is what you wanted; retraining on the new distribution may narrow it.",
      "<strong>The shift is seasonal.</strong> Retraining on December to serve January bakes in a pattern that is about to reverse, and the following retrain has to undo it.",
      "<strong>The labels are not in yet.</strong> Retraining on the period you have labels for means training on the past you already handled, not the present that is failing.",
      "<strong>The failure is not the model.</strong> The most common cause of a metric moving is an upstream data change &mdash; a feed, a schema, a unit. Retraining teaches the model to accommodate a bug rather than fixing it.",
    ]),
    ("related", ["drift", "after-it-ships", "tracking-runs-and-automating-evals", "lora-qlora-and-full-fine-tuning"]),
    ("quiz", [
      ("Why is a commit hash insufficient to identify what a trained system will do?",
       ["Commit hashes do not capture merge history accurately",
        "Behaviour comes from code, weights, data and configuration together, and only the first is in the repository",
        "The hash changes whenever the model is retrained, so it cannot be a stable reference"],
       1),
      ("A retrained model scores better than the incumbent on the aggregate. What should you check before promoting it?",
       ["That the training loss converged smoothly",
        "The slices — a retrain that improves the aggregate while losing a minority segment is the ordinary outcome of training on reweighted data",
        "That the new training set is larger than the previous one"],
       1),
      ("Drift is detected but the model's performance metric has not moved. What does that suggest?",
       ["A retrain is overdue and the metric will follow shortly",
        "The model is generalising across the shift — retraining on the new distribution may narrow it rather than help",
        "The drift detector's threshold is set too loosely"],
       1),
    ]),
  ],
},
]
