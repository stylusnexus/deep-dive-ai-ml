# SOP — Building LLM Systems

Checklists, in the aviation sense. Six of them: this master, and five focused
ones you jump to when you're in that phase.

## How to use these (this part matters)

Borrowed from flight decks, because the conventions there were paid for:

**A checklist is not the procedure.** Pilots fly the flow from training, *then*
run the checklist to verify. If you're reading these to find out what to do,
you're using them wrong — do the work, then come back and confirm nothing was
skipped. That's why every item is phrased as something you can answer yes or no
to, not as an instruction.

**Killer items are marked ☠.** Miss one of these and the work is wrong in a way
you probably won't detect until it's expensive. If you're short on time, run only
those.

**Gates are hard.** A gate means stop. Not "note it and continue" — the later
phases produce meaningless output if an earlier gate is open.

**Short beats complete.** A checklist nobody finishes protects nobody. If one of
these grows past a page, it's failing, and the fix is to cut items rather than
shrink the font.

**Non-normal checklists are separate.** [`incident.md`](incident.md) is the one
you reach for when something is already wrong. Don't mix it into normal flow.

---

## Master checklist

### Phase 0 · Before there is a project
- [ ] ☠ Confirmed this needs ML at all — a rule, a query or a lookup won't do it
- [ ] ☠ Dumb baseline built and scored, not just described
- [ ] The decision this output drives is named, with who makes it
- [ ] "Good enough" written down as a number, **before** seeing any result
- [ ] Cost of a false positive vs a false negative stated, and which hurts more
- [ ] Kill condition named while you're still objective
- [ ] [`project-intake.md`](../project-intake.md) filled in and dated

**GATE — do not build until every ☠ above is closed.**

### Phase 1 · Data
- [ ] ☠ Every feature interrogated: would I have this value, with this content, at prediction time?
- [ ] ☠ Split done **before** any scaler, imputer or encoder is fitted
- [ ] Class balance measured; majority-class score written down
- [ ] Missingness mechanism assessed (MCAR / MAR / MNAR), not just the percentage
- [ ] Duplicates checked — exact rows *and* the same entity under different ids
- [ ] Dtypes read; sentinel values and unit inconsistencies hunted
- [ ] Group and time structure respected in the split where they exist

**GATE — a leak here invalidates everything downstream and hides from the usual checks.**

### Phase 2 · Approach
- [ ] Simplest thing that could work tried first, in order: prompt → retrieval → fine-tune → train
- [ ] Model / vendor / framework choice run through [`selection-scorecard.md`](../selection-scorecard.md)
- [ ] Build-vs-call decided on cost at *your* volume, not at demo volume
- [ ] → jump to [`deep-learning.md`](deep-learning.md), [`generative-ai.md`](generative-ai.md) or [`llm-engineering.md`](llm-engineering.md)

### Phase 3 · Measurement
- [ ] ☠ Instrument validated: it fails before the work and passes after it
- [ ] ☠ Held-out set exists that no tuning has ever seen
- [ ] Target metric and threshold fixed **before** the run
- [ ] Baseline run on the whole set, with repeats — not a spot check
- [ ] Guardrail metric chosen before looking at results
- [ ] Process recorded, not only outcome — you can tell *never tried* from *tried and failed*
- [ ] → full procedure in [`measurement.md`](measurement.md)

**GATE — an unvalidated instrument makes every later number noise.**

### Phase 4 · Build
- [ ] ☠ Models compared threshold-free, on identical folds, with spread reported
- [ ] ☠ Ordered data split by time, with a gap matching the prediction horizon
- [ ] One change at a time, or a bundled screen with its cost stated out loud
- [ ] Preprocessing inside a pipeline, so leakage is structurally hard
- [ ] Seeds and versions pinned; run recorded with model, config, date, per-item outcomes
- [ ] Fix reverted once to confirm it was the fix

### Phase 5 · Before it touches anyone
- [ ] ☠ Threshold chosen deliberately, with its error trade written down
- [ ] ☠ Failure path defined — what happens when it's wrong, who hears about it
- [ ] ☠ Human approval gate on anything irreversible or outward-facing
- [ ] Adversarial pass done: injection, tool abuse, over-permission → [`llm-engineering.md`](llm-engineering.md)
- [ ] Credentials least-privilege and scoped; production connected last
- [ ] Cost at 100× computed; rate limits in place on anything paid
- [ ] Monitoring live: input distributions, prediction distribution, data quality
- [ ] Rollback tested, not just written down

**GATE — nothing ships with a ☠ open in this phase.**

---

## The five focused checklists

| Checklist | When |
|---|---|
| [`deep-learning.md`](deep-learning.md) | Training a neural network from scratch |
| [`training.md`](training.md) | Any training run, classical or deep |
| [`fine-tuning.md`](fine-tuning.md) | Adapting an existing model to your task |
| [`generative-ai.md`](generative-ai.md) | Prompting, RAG, structured output |
| [`llm-engineering.md`](llm-engineering.md) | Agents, tools, loops, production |
| [`hardware.md`](hardware.md) | Deciding whether a model can run on the machine in front of you |
| [`mcp.md`](mcp.md) | Connecting someone else's MCP server, or shipping your own |
| [`measurement.md`](measurement.md) | Any time you need a number you can trust |
| [`incident.md`](incident.md) | **Non-normal.** Something is already wrong |
