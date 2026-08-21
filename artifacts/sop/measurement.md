# Measurement — getting a number you can trust

In dependency order. Every step is worthless before the one above it.

## 0 · Prove the instrument ☠
- [ ] ☠ Fixture **fails** at the starting state, before the work
- [ ] ☠ Fixture **passes** with a known-good fix applied
- [ ] "Did nothing" and "solved it" cannot score the same
- [ ] Process recorded, not just outcome — you can tell *never attempted* from *attempted and failed*

If either half is untrue, stop. Everything below produces noise.

## 1 · Write the number down before you run
- [ ] Target metric named
- [ ] Threshold that would count as success, fixed in advance
- [ ] Guardrail metric chosen — what must not get worse

## 1b · Rule out the invisible
- [ ] ☠ Run manifest emitted: model, endpoint, every budget, verification state, config version
- [ ] Every terminator names itself when it fires — a wall clock must not look like a model stopping
- [ ] Effective values printed **after** all writers, not the values you requested
- [ ] Nothing truncated mid-measurement (output budget, context, tool-result clipping)
- [ ] Non-completions classified — infrastructure errors kept out of capability numbers
- [ ] Control fixture included, and read first when a board looks uniform

## 2 · Baseline
- [ ] Whole set, not a spot check
- [ ] Repeated, so you know the run-to-run spread
- [ ] Recorded with model, config, versions, date, per-item outcomes

## 3 · One treatment at a time
- [ ] One change, or a bundled screen with the cost stated: you'll know *something* worked, not *what*
- [ ] Everything else held fixed

## 3b · Make the result locatable
- [ ] Engagement reported separately from correctness — a metric that merges them hides what to fix
- [ ] Every model failing identically? Suspect the harness before the models
- [ ] For each passing test, what it does **not** establish, written down now

## 4 · Read it honestly
- [ ] Compared against baseline spread, not against zero
- [ ] Sample size big enough for the difference to mean anything
- [ ] Guardrail checked before declaring a win

## 4b · Turn the number into a decision
- [ ] ☠ Threshold chosen from the **costs of each error type**, not left at the 0.5 default
- [ ] Decision table produced: at each threshold, what is caught, what is missed, what it costs
- [ ] Error reported in units someone can act on — "out by about four days" beats "RMSE 0.34"
- [ ] Stated what would make you distrust this result in six months

## 5 · Revert the fix ☠
- [ ] ☠ Change removed and re-run — did the number go back?

If it didn't, the improvement came from somewhere else and you've learned the
wrong lesson. This is the step everyone skips.
