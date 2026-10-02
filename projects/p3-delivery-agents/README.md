# Project 3 · Multi-Agent Exception Handling

**Block 4 exit criterion.** The operations project.

> Improve last-mile logistics by implementing a multi-agent system that detects
> delivery exceptions from operational logs, applies policy-based reasoning to
> determine resolution actions, generates customer communications, and escalates
> complex cases while maintaining full auditability.

## What this actually demonstrates

Three things the course has argued for, made concrete:

1. **An approval gate that halts work in flight**, not just admission. The
   customer-communication step cannot proceed without a human decision, and the
   run persists while it waits.
2. **A trace that makes the run legible.** Every agent, every handoff, every
   guard - including the ones that did not fire.
3. **Handoffs as the place failures live.** The trace records what each summary
   dropped, which is where the multi-agent lesson says the errors hide.

## The agents

| agent | job | why separate |
|---|---|---|
| `triage` | classify the exception from the log entry | narrow, deterministic-first - rules handle most cases |
| `policy` | decide the resolution against written policy | needs the policy documents in context, nothing else |
| `comms` | draft the customer message | **gated** - outward-facing and irreversible |

Three agents because three contexts, not because three job titles. `triage` never
sees policy documents; `policy` never sees draft prose.

## What "done" looks like

- [ ] Intake sheet completed before building
- [ ] Deterministic path measured first - what fraction of exceptions need a model at all?
- [ ] Approval gate blocks an in-flight run, demonstrably
- [ ] Run resumes after approval without replaying earlier work
- [ ] Trace shows every handoff and what each summary dropped
- [ ] Every guard recorded, fired or not
- [ ] Escalation path defined for cases the system should not decide

## Running it

```bash
python src/pipeline.py                    # process the exception log
python src/pipeline.py --approve-all      # simulate approvals, for a full run
python src/pipeline.py --trace run-042    # replay one trace
```

Writes `report.md`, `traces/` and `pending/` - the last being approvals waiting
on a human, which is the point.

## The honest framing

Most delivery exceptions are handled correctly by a lookup table. The measurement
this project should produce is *what fraction genuinely needed judgement* - and
if that number is small, the right system is mostly rules with an agent for the
remainder. That finding is more valuable than a working multi-agent demo.
