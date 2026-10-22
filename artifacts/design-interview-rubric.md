# Design interview rubric

A scored mock interview for the questions AI system-design interviews keep asking.
It tests whether you can *say* the course, under a clock, to another person. Quizzes
test recall and the capstone tests building. This tests explanation.

Taught in [Designing the Whole System](../lessons/block8-deployment/) and the lessons
it points to.

## How to run it

- **Two people.** One asks, one answers, then swap. A single person can run it by
  recording themselves and scoring the recording the next day.
- **45 minutes.** Question 1 gets 12 minutes with a blank page. Questions 2 to 9 get
  3 minutes each. The last 9 minutes are for scoring.
- **No notes, no screen.** Draw by hand.
- **The interviewer may ask one follow-up per question.** "How would you know?" is
  always allowed.

## Scoring

Score each question 0, 1 or 2.

| Score | Meaning |
|---|---|
| 0 | Names a tool or a buzzword with no reason, or avoids the question |
| 1 | The right idea, with no failure named or no measurement named |
| 2 | The right idea, the failure it prevents, and the number that would show it failed |

Add three marks across the whole interview, 0 or 1 each:

- Asked for the five numbers (corpus size and churn, query rate, latency budget,
  cost of a wrong answer, who may see what) before drawing, or stated assumptions aloud.
- Named a failure of their own design before the interviewer did.
- Said what they would build first and what they would leave out until measured.

**Maximum 21.** 17 or more: ready. 12 to 16: one weak block, re-read the lessons below.
Under 12: redo the capstone failure drill and the Block 3 notebooks, then try again.

## The questions and what a 2 contains

| # | Question | A 2 answer includes | Lessons |
|---|---|---|---|
| 1 | Design a production-ready RAG system. | The five numbers first. Separate ingestion and query paths drawn. Each box with what it protects against: gateway (auth, limits), cache, query rewrite, hybrid retrieval with the access filter, rerank, context assembly with citations, generation under a deadline with a fallback ladder, a grounding check, traces. The four numbers it would report separately. | `building-a-rag-system`, `ranking-and-hybrid-retrieval`, `designing-the-whole-system` |
| 2 | When would you choose RAG over fine-tuning? | Knowledge that changes, must be cited or must be access-controlled goes in retrieval. Fixed format, tone or a narrow skill goes in tuning, after prompting and retrieval were measured. Cites the failure: a tuned model can learn the rule and its blind spot. | `when-fine-tuning-is-wrong`, `building-the-dataset` |
| 3 | How would you reduce latency without hurting quality? | Separates time to first token (prefill, grows with prompt) from tokens per second (decode). Fewer, better chunks; stable prefix; streaming; rerank a short list. Re-runs the eval set after each change. | `latency-and-caching`, `why-the-gpu-is-waiting` |
| 4 | What happens if your LLM provider goes down? | Distinguishes down, throttled, slow, partial and degraded. Deadline plus circuit breaker. A tested fallback ladder ending at the retrieved passages or an honest error. Does not fail over on a 429. Names that the fallback needs its own evaluation and data agreement. | `when-the-provider-goes-down`, `managed-cloud-surfaces` |
| 5 | How do you evaluate an AI system? | Reports index recall, retrieval quality, groundedness and correctness separately, on a private gold set with a non-completion column, and checks a difference is larger than noise. | `where-evaluation-lives`, `eval-data-you-can-trust`, `is-the-difference-real` |
| 6 | Where would you add caching? | Exact-match first, then provider prompt caching with the stable prefix first, then a similarity cache only where a wrong match is cheap and never shared across tenants. Measures hit rate and wrong-hit rate. | `latency-and-caching` |
| 7 | How do you prevent hallucinations? | Says they cannot be prevented, only made detectable: ground in retrieved text, require citations, check claims against sources, refuse when retrieval is empty. Measures groundedness and the false-refusal rate. | `hallucination-and-grounding`, `measuring-retrieval` |
| 8 | What would you monitor in production? | Up and right as separate questions. Latency percentiles, error and fallback rates, cost per request, cache hit rate, plus a scheduled quality run on a fixed set. Says what wakes a person. | `after-it-ships`, `drift`, `telemetry-and-instrumentation` |
| 9 | How would you scale to millions of documents? | Does the memory sum first. Compress and rerank, partition by tenant or source, shard only when needed and notes the slowest shard sets latency. Plans the re-index for a new embedding model. Measures recall against exact search. | `retrieval-at-scale`, `vector-search-algorithms` |

Drawing the complete architecture is question 1's figure, so it is not scored
separately.

## Score sheet

One row per question, 0 to 2. The three bonus marks are 0 or 1 each.

| Item | Score | Notes |
|---|---|---|
| 1. Production-ready RAG system (0-2) | | |
| 2. RAG or fine-tuning (0-2) | | |
| 3. Latency without hurting quality (0-2) | | |
| 4. Provider outage (0-2) | | |
| 5. Evaluating an AI system (0-2) | | |
| 6. Where to add caching (0-2) | | |
| 7. Preventing hallucinations (0-2) | | |
| 8. Monitoring in production (0-2) | | |
| 9. Scaling to millions of documents (0-2) | | |
| Bonus: asked for the five numbers or stated assumptions (0-1) | | |
| Bonus: named a failure of their own design first (0-1) | | |
| Bonus: said what to build first and what to leave out (0-1) | | |
| **Total (maximum 21)** | | |

## Failure patterns to listen for

- A product name where a reason should be.
- A cache or fallback with no mention of what it can get wrong.
- "We would evaluate it" with no set, no number and no comparison.
- Scaling answers that start with sharding and never mention how many vectors there are.
- A design with no failure named until the interviewer finds one.

## After the interview

For every question scored 0 or 1, write the missing sentence on the page and read the
lesson in the last column. Re-run only those questions a week later.
