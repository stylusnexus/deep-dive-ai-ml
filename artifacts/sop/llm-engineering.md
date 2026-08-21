# LLM engineering — agents, tools, loops, production

## Do you need an agent?
- [ ] ☠ A fixed workflow ruled out — most "agentic" tasks are workflows with a model in one slot
- [ ] The sequence genuinely cannot be known in advance
- [ ] Fewest agents that do the job; every handoff costs observability

## The loop
- [ ] ☠ Termination is **not** "the model says it's done"
- [ ] ☠ Hard ceiling on turns **and** on spend
- [ ] Repetition detection, so it cannot spin on the same failing action
- [ ] External signal enters the loop — a test, a validator, a retrieval hit. If nothing does, expect little
- [ ] Compounding error accounted for: ten steps at 95% is ~60%

## Prompt vs tool — decide per rule
- [ ] ☠ For every rule: **can the model tell when it has complied?**
- [ ] Mechanically checkable rules live in the tool as a precondition, not in prose
- [ ] No prompt instruction states a precondition a tool already enforces
- [ ] No prompt instruction gates the work without a completion test ("inspect thoroughly first" has none)
- [ ] Prompt states the mechanism and a bounded action, rather than requesting a behaviour
- [ ] Prompt carries only what tools cannot check: goals, priorities, ambiguity handling, when to stop and ask

## Tools
- [ ] Names and descriptions written as prompt engineering, because they are
- [ ] ☠ Least privilege — read-only first, widen per task, narrow back
- [ ] ☠ Scoped credentials, not account-wide
- [ ] Production connected last, never first
- [ ] Third-party MCP servers vetted like dependencies
- [ ] Execution sandboxed in a container if the agent runs code
- [ ] ☠ Timeouts kill the **process group**, not just the direct child — an orphaned tree survives its own timeout and compounds every iteration
- [ ] Process count checked after any run that timed out on a spawned command

## Adversarial
- [ ] ☠ Indirect prompt injection tested — hostile text in a document, issue, email or page
- [ ] Everything retrieved treated as data, never as instructions
- [ ] Exfiltration path considered: what could a compromised agent send, and where
- [ ] Defences architectural, not exhortations in the system prompt

## Context
- [ ] Budget allocated deliberately across instructions, tools, history, retrieval, answer
- [ ] Tool results truncated or summarised before they enter context
- [ ] History managed — window, compaction or structured memory
- [ ] Long-session degradation understood; fresh context preferred to fighting a poisoned one

## Production
- [ ] ☠ Human approval before anything irreversible or outward-facing
- [ ] Full action log — you cannot investigate what you didn't record
- [ ] Model versions pinned, not floating on an alias
- [ ] Eval set re-run on a schedule, not only when something looks wrong
- [ ] Rate limits on every paid endpoint
- [ ] Unattended runs: narrow job, scoped access, safe stopping points, someone reachable

## Smells
- Agent loops without progress → no external verifier; nothing tells it that it failed
- Wrong tool chosen repeatedly → rewrite descriptions before upgrading the model
- Works alone, fails in production → context differs; log what actually went in
