# Tuning a working agent loop

**Different moment from [`llm-engineering.md`](llm-engineering.md).** That one asks
*am I building this correctly?* This one asks *this works — how do I make it
cheaper and more reliable without breaking it?*

## Things to know

> **Each lever trades tokens and latency against reliability.**
> There is no free setting. The correct position for each is a property of your
> failure distribution, not a best practice you can copy.

> **They interact, so change one at a time.**
> Truncating reads improves cache hit rates by stabilising the prompt. Per-edit
> verification adds turns, which makes read accumulation worse. Adjust two and
> the result tells you something moved, not what.

---

## Before you tune anything ☠

- [ ] ☠ **Read the trace.** Where do runs actually fail — turn cap, spend cap, wrong tool, broken edit, or just cost? Each points at a different lever
- [ ] ☠ Baseline recorded on the whole battery, repeated, with spread
- [ ] The metric you are trying to move, named, before you start
- [ ] A guardrail metric chosen — usually correctness, since every lever here can trade it away

**GATE — tuning without a trace is guessing with extra steps.**

## 1 · Truncate tool results

Cheapest real win. One line, and it caps the worst case immediately.

- [ ] Every tool result capped at ingest
- [ ] Cap chosen from actual result sizes, not guessed
- [ ] Truncation marker present, so the model knows content was omitted
- [ ] Large reads scoped at the source where possible — fetch the relevant slice, not the file

## 2 · Order the prompt for caching

- [ ] Stable content first: system prompt, tool definitions, long documents
- [ ] Variable content last: the user turn, anything with a timestamp or session id
- [ ] ☠ **Nothing variable near the front** — one changing character invalidates everything after it
- [ ] ☠ Cache hit rate instrumented and alerted on. A cache that stopped matching looks exactly like one that never existed, except on the bill
- [ ] Reuse count checked against the write premium — caching a prefix used twice is roughly break-even

## 3 · Set verification granularity

- [ ] Change shape identified: are edits independent, or atomic across files?
- [ ] Independent edits → verify per edit, for precise attribution
- [ ] Atomic changes → verify per logical unit; per-edit checking reports failures the next edit would resolve
- [ ] The agent can tell which regime it is in
- [ ] Verification cost measured — it is a turn, and turns compound

## 4 · Tune reasoning effort last

- [ ] Routed by turn shape, not set globally
- [ ] High effort where the model must plan or diagnose
- [ ] Low or none where it is executing a decision already made, extracting, or formatting
- [ ] Reasoning tokens counted — they are billed whether or not you see them
- [ ] Measured, not assumed: on recall and extraction the gain is usually zero

## After each change

- [ ] ☠ One lever moved, not two
- [ ] Whole battery re-run, not a spot check
- [ ] Guardrail metric checked before declaring a win
- [ ] ☠ Change reverted once to confirm it caused the improvement
- [ ] Manifest updated — the settings are now part of what a score means

## Smells

- Cost fell and correctness fell with it → you traded away the thing you were protecting; check the guardrail
- Cache hit rate near zero with no code change → something variable crept into the prefix
- Agent spinning on a build error it keeps re-fixing → per-edit verification on an atomic change
- Reasoning tokens high on extraction turns → one global effort setting instead of routing
- Turn counts rising over weeks with no deploy → read accumulation growing as the corpus or tool set grows
- A tuning win you cannot reproduce → two levers moved, or no manifest
