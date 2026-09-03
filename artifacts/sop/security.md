# Security — before an agent touches anything real

Block 6 covers why these matter. This is the pre-flight, and it assumes the
threat is an instruction arriving inside content the system reads rather than
typed at it by the person using it.

## Before it is reachable
- [ ] ☠ Confirmed what the agent may *do*, not what the input may say — the input
      is unbounded and the action set is not
- [ ] ☠ Every credential scoped to the task, and read-only until a task needs write
- [ ] Reading and acting split where possible, so an injection in a document reaches
      a component holding nothing worth having
- [ ] Irreversible actions gated on a human, and the gate genuinely halts the run

## The exfiltration audit
- [ ] ☠ Tool set reviewed as a *set*, not tool by tool — the finding is always a pair
- [ ] Every tool listed with what it can read and what it can reach; any pair joining
      something sensitive to something outside is the path
- [ ] Rendering treated as a channel — if the interface renders model output, images
      and links fetch from the reader's browser, past your egress rules
- [ ] Traces and logs checked as a destination, not just a record

## Containment
- [ ] Agent-executed code runs where its filesystem and process access are enumerated
- [ ] ☠ Egress restricted to the hosts it needs — default container networking permits
      arbitrary outbound, which is the direction exfiltration uses
- [ ] Runs as a non-root user
- [ ] What the agent *read* is logged, not only what it did — otherwise an incident
      cannot be reconstructed

## Persistent memory, if the agent has any
- [ ] ☠ A memory write treated as an action with a gate, not as bookkeeping — it changes
      what every future session believes
- [ ] Every stored memory carries its source, so a fact learned from a fetched document is
      distinguishable from one the user stated
- [ ] Directives not persisted as directives — record that a document made a claim, never
      that a standing instruction is now in force
- [ ] ☠ The store scoped to the user or project it was written for; memory from one user's
      session never loads into another's
- [ ] Understood that restarting does not clear a poisoned store, and that the trace of the
      harmful session will not contain the read that caused it

## Before believing it is safe
- [ ] ☠ Tested against the whole system with real tools and real rendering, not a
      component in isolation
- [ ] Attack battery is fixed, private, and kept — with a decided criterion per case
- [ ] Baseline recorded before any mitigation, so a fix can be shown to have worked
- [ ] Re-run after every prompt, model or tool change — a tool added later reopens
      a hole closed earlier
- [ ] ☠ Written down what the fix does *not* cover

> Ask of every control: if the model were fully persuaded and cooperating with the
> attacker, would this still hold? A system prompt would not. A missing credential
> would.
