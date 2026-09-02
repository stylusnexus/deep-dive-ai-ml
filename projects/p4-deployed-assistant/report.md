# Deployed Grounded Assistant — Report

## What was built

A FastAPI service exposing the Block 3 corpus as an authenticated, rate-limited
question-answering endpoint, containerised and verified end to end against a real
model. Nine tests cover the interface contract.

## Verified behaviour

| Check | Result |
|---|---|
| Container builds and runs as non-root | yes |
| Corpus loads inside the image | 56 chunks |
| Health reports dependency state | `ok` when reachable, `degraded` + 503 when not |
| Unauthenticated request | 401 |
| Wrong key vs missing key | indistinguishable |
| Rate limit per key | enforced, `Retry-After` returned |
| Starts without `API_KEYS` | refuses, with a message naming the variable |
| Grounded answer with citation | correct on the temperature and turbine-count questions |
| Refusal when the corpus cannot answer | correct on the bearing-lifespan question |

## Two failures worth recording

**The tests were green while testing nothing.** The corpus path was resolved
relative to the repository layout, which is wrong inside the container. The
service was never ready, every request returned 503 before reaching any behaviour
under test, and eight tests passed. Fixing the path turned the suite from 57
seconds to 200 and immediately broke a test that had never really run.

**The rate-limit test was measuring its own latency.** With a 60-second window and
requests making real model calls of 15 to 50 seconds, the window slid open
mid-test and the limit never tripped. The limiter was correct; the test was not.
The window is now an hour in tests, which is the fixture adapting to the thing
being measured rather than the other way round.

## Not done

The service is not deployed. `render.yaml` describes it and applying it is a human
action — a public URL has a bill and an audience, and the keys belong in a
dashboard. The two unticked boxes in the README are that step and verifying the
rate limit against the running instance.
