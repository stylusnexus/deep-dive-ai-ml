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

## 2 · Baseline
- [ ] Whole set, not a spot check
- [ ] Repeated, so you know the run-to-run spread
- [ ] Recorded with model, config, versions, date, per-item outcomes

## 3 · One treatment at a time
- [ ] One change, or a bundled screen with the cost stated: you'll know *something* worked, not *what*
- [ ] Everything else held fixed

## 4 · Read it honestly
- [ ] Compared against baseline spread, not against zero
- [ ] Sample size big enough for the difference to mean anything
- [ ] Guardrail checked before declaring a win

## 5 · Revert the fix ☠
- [ ] ☠ Change removed and re-run — did the number go back?

If it didn't, the improvement came from somewhere else and you've learned the
wrong lesson. This is the step everyone skips.
