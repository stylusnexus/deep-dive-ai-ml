# Project 4 · Deployed Grounded Assistant

**Block 8 exit criterion.** The retrieval work from Projects 2 and 3, behind an
interface someone else can call.

> A deployed, authenticated, rate-limited endpoint with a public URL.

## What changes when it becomes a service

A notebook may assume one caller, a trusted question, unlimited time and a
failure that only you see. A service may assume none of those. Everything in
`src/app.py` that is not retrieval exists because of that difference:

| Concern | Why it is here |
|---|---|
| API key auth | The endpoint is reachable by anyone who finds it |
| Per-key rate limiting | A paid model call sits behind every request — the limit is about the bill, not the CPU |
| Request validation | Question length and `k` are bounded, because context is cost |
| Meaningful `/health` | Reports whether the corpus loaded and the model is reachable, and returns 503 when not |
| Versioned path | `/v1/ask`, so the contract can change without breaking callers |
| Refusal to start unconfigured | No `API_KEYS`, no service — better than a default that ships to production |
| Generic error responses | An exception message is the cheapest way to leak a path or a hostname |

## Running it

```bash
# locally
API_KEYS=dev-key uvicorn src.app:app --port 8000

# in a container, reaching a model on the host
docker build -t assistant .
docker run -p 8000:8000 -e API_KEYS=dev-key \
  --add-host=host.docker.internal:host-gateway assistant

curl -X POST localhost:8000/v1/ask \
  -H 'Content-Type: application/json' -H 'X-API-Key: dev-key' \
  -d '{"question":"What is the maximum gearbox oil temperature?"}'
```

## Tests

```bash
pytest tests/
```

The test boundary has three layers:

- **Training-system tests** (`tests/test_build_corpus_artifact.py`) prove that the
  build loads the intended corpus and writes a named artefact with its data identity —
  including a sensitivity check that the hash actually changes when the corpus does,
  not just that it runs.
- **Validation tests** belong to Project 2: the candidate is scored against the
  frozen held-out set and compared with the incumbent before promotion.
- **Functionality tests** (`tests/test_app.py`) are the ten API tests below:
  authentication, validation, rate limiting, health, corpus identity and a real
  corpus load through the service entry point.

Sixteen tests total, none of which check answer quality — that is Project 2's job
and it needs a model. The functionality tests check the interface contract: that an
unauthenticated caller cannot get in, that a wrong key is indistinguishable from a
missing one, that the rate limit is per key and actually limits, that validation
rejects what it should, and that the corpus genuinely loaded.

That last one exists because of a real failure. An early version resolved the
corpus path relative to the repository, which was wrong inside the container. The
service was therefore never ready, every request short-circuited to 503, and the
whole suite passed **without ever calling the model**. Green tests that exercise
nothing are worse than red ones, and the guard is there so it cannot recur.

## Data identity

```bash
python3 scripts/build_corpus_artifact.py
```

Writes `corpus/corpus_id.json`: a sha256 hash of `manifest.json`, the document
count and IDs, and a build timestamp. Regenerated alongside the corpus, the same
way `manifest.json` already is — not committed, since `corpus/` is gitignored
entirely (see "Reproducing the corpus from a fresh clone" below), and not rebuilt
inside the container, so it runs once per corpus generation rather than on every
image build. The running service loads it at startup and reports it at
`GET /version`, so a caller or an operator can answer "which exact corpus is this
instance serving" without SSH access to the container.

The build refuses to hash a manifest that disagrees with the `.md` files sitting
next to it — a hash over content nobody is actually serving is a confident wrong
answer, not a data identity.

## Serving benchmark

```bash
python3 bench_serving.py
```

Starts the real `src.app:app` via uvicorn and measures the real `/v1/ask` handler —
real auth, real rate limiting, real retrieval over the real corpus — under a
concurrency sweep (1, 2, 4, 8), reporting throughput and p50/p95 latency. The one
substitution: `GENERATION_ENDPOINTS` points at a local stub chat-completions server
rather than a real model, because this runs with no paid API key and no deployed
instance. The script names that substitution in its own output.

This is a genuine measurement of the service's own overhead — FastAPI, the
in-process rate limiter, the keyword-retrieval scoring — not a claim about model
latency or deployed capacity. Re-run it against the Render instance with a real
`GENERATION_ENDPOINTS` before treating the numbers as evidence for production.

## What "done" looks like

- [ ] Intake sheet completed before building
- [x] Auth, rate limiting, validation and health implemented and tested
- [x] Container builds, runs as non-root, and answers correctly end to end
- [x] Health check reports dependency state rather than "something is listening"
- [x] Dataset manifest/hash recorded with the model artefact (`scripts/build_corpus_artifact.py`
      writes `corpus/corpus_id.json`; the running service reports it at `/version`)
- [x] Serving benchmark run against the real entry point (`bench_serving.py`, not the
      notebook's fixture — see below for what it does and does not prove)
- [x] Deploy configuration committed (`render.yaml`), secrets not committed
- [ ] Deployed to a public URL — a human action, see below
- [ ] Rate limit verified against the deployed instance

## The deploy is deliberately not automated

`render.yaml` describes the service reproducibly and is not applied from here.
Publishing a public endpoint has a bill and an audience attached, and the API keys
belong in the dashboard rather than in this repository. Applying the blueprint and
setting `API_KEYS` is a decision, not a build step.

## The honest framing

This service retrieves by keyword, not by embedding. The embedding pipeline needs
`sentence-transformers` and `torch`, which turns a 200MB image into a
multi-gigabyte one, and for a project about deployment the image size is part of
the subject. The consequence is real: answers here are worse than Project 2's on
questions where wording differs from the corpus, and this is the same system with
a web interface only in the parts that are not retrieval. Deploying the embedding
version is a defensible different choice, and it is a different image.

## Reproducing the corpus from a fresh clone

`.gitignore` excludes `corpus/` entirely — the Dockerfile's claim that the corpus is
"versioned with the code" means versioned as a generator, not as committed files.
From the repository root:

```bash
python3 scripts/make_corpus.py
```

This writes `data/corpus/` for the retrieval lessons and, in the same run, syncs an
identical copy into `corpus/` here — the exact files `docker build` needs. Re-run
`scripts/build_corpus_artifact.py` afterward to refresh the data-identity hash, since
a freshly generated corpus needs a freshly computed one.
