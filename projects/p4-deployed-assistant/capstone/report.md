# Project 4 capstone report

Run: 2026-10-15T02:47:30Z. Mode: retrieval-only (no model). Corpus hash: `5cf29b4172f79225943d7316318098230d10c169d68e9e213120389f9612fc70`.

## 1. Tests

PASS: 48 passed in 31.44s

## 2. Failure drill (stub providers, deadline 1s, breaker opens after 2 failures)

| Scenario | Expected rung | Observed | Result | Detail |
|---|---|---|---|---|
| healthy primary | rung-1 | rung-1 | PASS | ms=15 |
| primary erroring, breaker open | rung-2 | rung-2 | PASS | primary_calls_after_open=0 |
| primary slow, 1s deadline | rung-2 | rung-2 | PASS | ms=1011 |
| every provider down, default caller | 503 | 503 | PASS | retry_after=1 |
| every provider down, opted in | retrieval-only | retrieval-only | PASS | ms=5, degraded=True, x_degraded=retrieval-only, answer_is_only_a_notice=True, evidence_in_passages=True |
| primary recovers after cooldown | rung-1 | rung-1 | PASS | ms=5 |

Without `allow_degraded` an outage is a 503 with `Retry-After`. With it, the reply is a 200 whose `answer` is only a notice and whose evidence is in `passages`.

The stubs exercise this service's own fallback logic. They say nothing about any real provider's latency or failure behaviour.

## 3. Gold set

- Answerable questions: 24
- Expected document in the returned sources: 24 of 24
- Expected fact present in the answer: 22 of 24
- Refusal on 5 unanswerable questions: not measured (needs a model; run with --with-model)
- With no model these are retrieval scores: the answer is the retrieved passages.

Misses:

- g16 (fact missing): What was fleet availability in Q2 2026? Expected `94.2 percent` in perf-2026-q2; sources returned: inc-2026-014, inc-2026-021, perf-2026-q2
- g19 (fact missing): What was the root cause of the Clyde vibration shutdown in incident 2026-021? Expected `blade root bolt` in inc-2026-021; sources returned: inc-2026-014, inc-2026-021

## 4. Scale sum (arithmetic, not a benchmark)

| Chunks | float32, 1,024 dims (GB) | int8 (GB) | 64-byte code, assumed (GB) |
|---|---|---|---|
| 56 | 0.0 | 0.0 | 0.0 |
| 100,000 | 0.41 | 0.102 | 0.006 |
| 1,000,000 | 4.096 | 1.024 | 0.064 |
| 10,000,000 | 40.96 | 10.24 | 0.64 |

This service stores no vectors: it retrieves by keyword. The table is what an embedding index over the same corpus would need.

## Serving overhead

| Concurrency | Requests/s | p50 ms | p95 ms |
|---|---|---|---|
| 1 | 59.5 | 16.6 | 18.8 |
| 2 | 113.2 | 17.7 | 19.5 |
| 4 | 185.2 | 18.2 | 30.6 |
| 8 | 208.4 | 29.9 | 63.4 |

Measured against a 10 ms local stub in place of a model, on this machine. Not a statement about model latency or the deployed instance.

## Not done here

- The public deploy and the rate-limit check against it (a human action).
- Answer correctness and groundedness with a real model.
- Any real provider's outage behaviour.
