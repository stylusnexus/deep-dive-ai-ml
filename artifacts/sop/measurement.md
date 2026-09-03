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
- [ ] ☠ On a reasoning model the output budget covers thinking **and** answer — too low a ceiling returns an *empty* string, not a short one, and an empty answer scores as a wrong one
- [ ] Output ceiling checked in **both** directions — too low truncates silently, too high lets a degenerate turn burn the whole budget producing nothing. Raising it is not the safe default
- [ ] Every detector asked what it *does* when it fires, and under what precondition it declines to — a detector that reports without interrupting is telemetry, not a control
- [ ] Non-completions classified — infrastructure errors kept out of capability numbers
- [ ] Control fixture included, and read first when a board looks uniform

## 2 · Baseline
- [ ] Before concluding you need more data: learning curve run on fractions of what you already
      hold. A flat validation curve means more of the same will not help, and it costs an afternoon
- [ ] Whole set, not a spot check
- [ ] Repeated, so you know the run-to-run spread
- [ ] Recorded with model, config, versions, date, per-item outcomes
- [ ] ☠ **Concurrent baseline** — the unchanged configuration re-run *alongside* the
      treatment, in the same session, on the same machine. A stored number from last
      month attributes every change since — a model updated under you, a grown corpus,
      a busier machine — to your treatment
- [ ] A previous run reused as the reference only when you can state what has not
      changed since, and are willing to be wrong about it

## 3 · One treatment at a time
- [ ] One change, or a bundled screen with the cost stated: you'll know *something* worked, not *what*
- [ ] Everything else held fixed

## 3b · Make the result locatable
- [ ] Engagement reported separately from correctness — a metric that merges them hides what to fix
- [ ] Every model failing identically? Suspect the harness before the models
- [ ] For each passing test, what it does **not** establish, written down now

## 4 · Read it honestly
- [ ] Any per-case promise (a latency budget, a per-customer forecast) stated from a
      *prediction* interval, not a confidence interval — the second is about the mean and says
      nothing about how wrong a single case can be
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

## Smells

- A surprisingly good result → suspect the instrument before celebrating; check step 0 again
- A null result on a change you were confident about → prove the treatment actually engaged before concluding it does not work
- Every configuration failing identically → suspect the harness, not the thing under test
- A number you cannot reproduce a week later → the manifest was incomplete
- A conclusion drawn from one run → that is an anecdote with a decimal point
