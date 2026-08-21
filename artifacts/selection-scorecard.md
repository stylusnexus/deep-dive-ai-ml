# Selection Scorecard

For choosing a **model**, a **platform/vendor**, or a **framework**. Three
different decisions with three different failure modes, so three sections.

Score each line 1–5, but the score isn't the output — the **notes** are.
A decision you can defend out loud is the deliverable.

Calibrate on decisions you've already made (Render, Neon + Prisma, local
models in Bullpen) before using it on ones you haven't. You know those
answers, which is what makes them useful for testing the rubric.

---

## A. Choosing a model

| Criterion | Score | Notes |
|---|---|---|
| Capability on **your** task (not a benchmark) | | |
| Cost per unit of real work | | |
| Latency, p50 and p95 | | |
| Context window vs. what you actually need | | |
| Open weights / can you run it yourself | | |
| Provider stability and deprecation history | | |
| Data handling — is your input training someone's model | | |

**Non-negotiable:** score capability against a **private eval set of ~20 items
drawn from your real task**. Public benchmarks are contaminated, gamed, and
usually measuring something other than your problem. This is the `honest-bench`
premise: a model that scores well on someone else's test tells you very little.

> **Eval set used:**
> **Result:**
> **Decision:**

### Local vs. hosted

Most people can't seriously consider "run it yourself." With 128GB unified
memory you can. Ask it every time:

- Does this need frontier capability, or is it classification/extraction/routing that a 7B model does fine?
- What's the privacy value of the data never leaving the machine?
- What's the cost at your actual volume — is the API cheaper than your time?

---

## B. Choosing a platform or vendor

| Criterion | Score | Notes |
|---|---|---|
| Lock-in surface — how much of your code assumes them | | |
| Exit cost — how long to migrate off, honestly | | |
| Pricing shape (per-token / per-seat / per-hour / per-GB) | | |
| What breaks at 10x usage | | |
| Rate limits and quotas **in practice**, not on the pricing page | | |
| Data handling, residency, retention terms | | |
| Support reality when it breaks at 2am | | |

> **Decision:**
> **What would make us leave:**

---

## C. Choosing a framework or library

| Criterion | Score | Notes |
|---|---|---|
| Does the abstraction earn its weight, or is it a thin wrapper | | |
| Maintenance burden — release cadence, breaking changes | | |
| Dependency risk — what it drags in transitively | | |
| Can you read the source when it misbehaves | | |
| Could you replace it with ~200 lines of your own | | |

**House bias, stated openly:** prefer no third-party runtime dependency where
the standard library or a small amount of your own code will do. A wrapper that
saves twenty lines and adds a supply chain is a bad trade.

> **Decision:**

---

## Worked comparisons

Complete these three first — you already know the answers, so they calibrate the rubric.

- [ ] Why Render over Vercel/Fly/AWS for the Stylus services
- [ ] Why Neon + Prisma over Supabase for newer projects
- [ ] Why local models first in Bullpen, escalating only on failure

Then two live ones where you don't know the answer yet:

- [ ] Vector store for Block 3 — pgvector vs. Qdrant vs. Chroma
- [ ] Agent framework for Block 4 — LangGraph vs. raw SDK
