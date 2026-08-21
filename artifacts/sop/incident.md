# NON-NORMAL — something is already wrong

Separate from normal flow on purpose. Work top to bottom; do not skip.

## Stop the bleeding
- [ ] Is it still happening? Disable the feature or flag before diagnosing
- [ ] Is anything irreversible in flight? Halt agents with write access first
- [ ] Cost runaway? Kill the loop, then look

## Establish what is true
- [ ] ☠ Reproduce it before theorising — a plausible mechanism is not a finding
- [ ] Check the data before the model: schema change, units, new categories, silently dropped rows
- [ ] Check whether anything deployed — model version, prompt, dependency, upstream job
- [ ] Read the actual trace, not the summary

## Common causes, cheapest first
- [ ] Upstream pipeline changed (most likely)
- [ ] Model version moved under a floating alias
- [ ] Retrieval index degraded or empty
- [ ] Temperature or max-tokens changed on a structured task
- [ ] Context grown past the point where mid-prompt material is used
- [ ] Genuine drift (least likely, and the one everyone reaches for first)

## Before you call it fixed
- [ ] ☠ Fix verified by reverting it — the number moves back
- [ ] Eval set re-run whole, not just the failing case
- [ ] Guardrail metrics checked
- [ ] Monitoring added for the thing that just bit you
- [ ] One line written down: what broke, why, what would have caught it earlier
