#!/usr/bin/env python3
"""A grounded document assistant, served as an authenticated HTTP API.

This is Project 2's retrieval pipeline behind an interface someone else can call,
which changes what has to be true about it. A notebook may assume one caller, a
trusted question and unlimited time. A service may assume none of those, so the
work here is the difference: authentication, per-key rate limiting, request
validation, a health check that means something, a version in the path, and a
refusal to start rather than a failure at the first request.

Run locally:
    uvicorn src.app:app --reload --port 8000

Every endpoint except /health and /version requires an API key.
"""
from __future__ import annotations

import json
import os
import pathlib
import re
import time
import urllib.request
from collections import defaultdict, deque
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Header, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from .resilience import AllRungsFailed, Ladder, Rung

API_VERSION = "v1"
# Resolved from the environment first, because the repository layout and the
# container layout are different and hard-coding either one breaks the other.
_REPO_DEFAULT = pathlib.Path(__file__).resolve().parent.parent.parent.parent / "data" / "corpus"
CORPUS = pathlib.Path(os.environ.get("CORPUS_DIR", _REPO_DEFAULT))

# Rate limit: requests per key per window. Deliberately low — a paid model call
# sits behind every request, and the point of the limit is the bill, not the CPU.
RATE_LIMIT = int(os.environ.get("RATE_LIMIT", "10"))
RATE_WINDOW_S = int(os.environ.get("RATE_WINDOW_S", "60"))

# In-process, therefore per-instance. Honest about what it is: this is correct on
# one worker and approximate on several, and a real deployment moves it to Redis.
_HITS: dict[str, deque[float]] = defaultdict(deque)

STATE: dict = {"ready": False, "chunks": [], "encoder": None, "reranker": None,
               "base": None, "model": None, "corpus_hash": None, "ladder": None}

# Fallback ladder settings. The deadline is what turns a slow provider into a
# failure the ladder can act on; the breaker is what stops every later request
# paying that deadline again. See src/resilience.py.
GENERATION_DEADLINE_S = float(os.environ.get("GENERATION_DEADLINE_S", "60"))
BREAKER_THRESHOLD = int(os.environ.get("BREAKER_THRESHOLD", "3"))
BREAKER_COOLDOWN_S = float(os.environ.get("BREAKER_COOLDOWN_S", "30"))
RETRIEVAL_ONLY = "retrieval-only"


def _load_keys() -> set[str]:
    """Keys come from the environment, never from the repository. A service with
    no keys configured refuses to start rather than starting open."""
    raw = os.environ.get("API_KEYS", "").strip()
    return {k.strip() for k in raw.split(",") if k.strip()}


def chunk_structural(text: str) -> list[str]:
    out = []
    for part in re.split(r"\n(?=#{1,3} )", text):
        part = part.strip()
        if not part:
            continue
        if len(part) > 900:
            out += [s.strip() for s in re.split(r"\n\n+", part) if s.strip()]
        else:
            out.append(part)
    return out


# Inside a container, localhost is the container. The default is right for local
# development and wrong everywhere else, so it is overridable rather than assumed.
ENDPOINTS = [e.strip() for e in os.environ.get(
    "GENERATION_ENDPOINTS",
    "http://localhost:11455/v1,http://localhost:11434/v1").split(",") if e.strip()]


def discover_model(base: str) -> str | None:
    """The first chat model an endpoint advertises, or None if it cannot be reached."""
    try:
        with urllib.request.urlopen(f"{base}/models", timeout=3) as r:
            ids = [m["id"] for m in json.loads(r.read()).get("data", [])]
    except Exception:
        return None
    chat = [i for i in ids if not any(w in i.lower()
            for w in ("embed", "rerank", "whisper", "clip"))]
    return chat[0] if chat else None


def find_endpoint():
    for base in ENDPOINTS:
        model = discover_model(base)
        if model:
            return base, model
    return None, None


def build_ladder() -> Ladder:
    """One rung per configured endpoint, in order. Every endpoint becomes a rung
    whether or not it answered at startup, because a rung that was down at boot
    is exactly the one that may be back in a minute."""
    rungs = [Rung(name=f"rung-{i + 1}", base=b) for i, b in enumerate(ENDPOINTS)]
    return Ladder(rungs, deadline_s=GENERATION_DEADLINE_S,
                  threshold=BREAKER_THRESHOLD, cooldown_s=BREAKER_COOLDOWN_S)


def probe_at_boot(ladder: Ladder) -> None:
    """Find each rung's model now, and open the breaker of any rung that did not
    answer. A rung that is down at boot then starts in the state it is really in,
    and recovers through the same half-open probe as any other rung."""
    for rung in ladder.rungs:
        rung.model = discover_model(rung.base)
        if rung.model is None:
            for _ in range(ladder.threshold):
                ladder.breakers[rung.name].failure()


HEALTH_PROBE_DEADLINE_S = float(os.environ.get("HEALTH_PROBE_DEADLINE_S", "10"))


def model_reachable() -> bool:
    """True when at least one rung can take a request right now. A rung whose
    breaker is half-open is probed here, once per cool-down, so an instance that
    health-checks itself out of rotation still notices the model coming back.

    The probe is a real one-token completion, not a request for the model list. A
    provider that is overloaded still lists its models, so the list would close the
    breaker while every real question kept failing. The cost is one tiny call per
    cool-down for each rung that is down, and none while every rung is healthy."""
    ladder = STATE.get("ladder")
    if not ladder:
        return False
    for rung in ladder.rungs:
        breaker = ladder.breakers[rung.name]
        state = breaker.state
        if state == "closed":
            return True
        if state == "half-open" and breaker.allow():
            try:
                generate(rung, min(ladder.deadline_s, HEALTH_PROBE_DEADLINE_S),
                         "Reply with one word.", "ok", max_tokens=1)
            except Exception:
                rung.model = None  # a rung that swapped its model must be looked up again
                breaker.failure()
                continue
            breaker.success()
            return True
    return False


def generate(rung: Rung, deadline_s: float, system: str, user: str,
             max_tokens: int = 1500) -> dict:
    """One completion from one rung. Raises on any failure, including the deadline."""
    if rung.model is None:
        rung.model = discover_model(rung.base)
        if rung.model is None:
            raise RuntimeError("endpoint unreachable")
    body = json.dumps({"model": rung.model, "temperature": 0, "max_tokens": max_tokens,
                       "messages": [{"role": "system", "content": system},
                                    {"role": "user", "content": user}]}).encode()
    request = urllib.request.Request(f"{rung.base}/chat/completions", data=body,
                                     headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=deadline_s) as r:
        return json.loads(r.read())["choices"][0]


def retrieve(question: str, k: int) -> list[dict]:
    """Keyword scoring with rare-term weighting and length normalisation — the BM25
    shape from Block 3, without the dependency.

    This service retrieves by keyword rather than by embedding on purpose: the
    embedding pipeline needs sentence-transformers and torch, which turns a 200MB
    image into a multi-gigabyte one. That is a deliberate trade and it has a cost —
    answers here are worse than Project 2's, and the report says so rather than
    presenting this as the same system with a web interface on it."""
    terms = [w for w in re.findall(r"[a-z0-9]+", question.lower()) if len(w) > 2]
    if not terms:
        return STATE["chunks"][:k]
    n = len(STATE["chunks"]) or 1
    df = {t: sum(1 for c in STATE["chunks"] if t in c["lower"]) for t in terms}
    avg_len = sum(c["len"] for c in STATE["chunks"]) / n

    def score(c: dict) -> float:
        total = 0.0
        for t in terms:
            tf = c["lower"].count(t)
            if not tf:
                continue
            # Rare terms count for more; long chunks do not win on length alone.
            idf = max(0.1, (n - df[t] + 0.5) / (df[t] + 0.5))
            total += (tf / (tf + 1.2 * (0.25 + 0.75 * c["len"] / avg_len))) * idf
        return total

    return sorted(STATE["chunks"], key=score, reverse=True)[:k]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load once at start, not per request. A service that loads a model inside a
    handler pays the cost on every call and times out on the first one."""
    if not _load_keys():
        raise RuntimeError(
            "API_KEYS is empty. Set it to a comma-separated list before starting — "
            "this service will not run without authentication configured.")
    manifest = CORPUS / "manifest.json"
    if manifest.exists():
        docs = json.loads(manifest.read_text())
        STATE["chunks"] = [{"doc_id": d["doc_id"], "text": c,
                            "lower": c.lower(), "len": len(c.split())}
                           for d in docs for c in chunk_structural(d["text"])]
    # The data-identity artefact from scripts/build_corpus_artifact.py, committed
    # alongside the corpus the same way manifest.json is. Its absence is not fatal —
    # an older corpus built before this existed should still serve — but its hash is
    # how a caller or an operator answers "which corpus is this instance running."
    artifact = CORPUS / "corpus_id.json"
    if artifact.exists():
        STATE["corpus_hash"] = json.loads(artifact.read_text()).get("corpus_hash")
    STATE["base"], STATE["model"] = find_endpoint()
    STATE["ladder"] = build_ladder()
    probe_at_boot(STATE["ladder"])
    STATE["ready"] = bool(STATE["chunks"])
    yield
    STATE.clear()


app = FastAPI(title="Grounded Document Assistant", version=API_VERSION,
              lifespan=lifespan)


class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=500,
                          description="A question about the corpus.")
    k: int = Field(default=4, ge=1, le=16,
                   description="Chunks to retrieve. Bounded because context is cost.")
    allow_degraded: bool = Field(
        default=False,
        description="Accept the retrieved passages, unsummarised, when no model answers. "
                    "Off by default so a caller that does not know about degraded replies "
                    "gets an error it can see, not passages it might show as an answer.")


class Passage(BaseModel):
    doc_id: str
    text: str


class AskResponse(BaseModel):
    answer: str
    sources: list[str]
    grounded: bool
    model: str
    rung: str = Field(description="Which step of the fallback ladder answered.")
    degraded: bool = Field(default=False,
                           description="True when no model answered. `answer` is then only a "
                                       "notice and the evidence is in `passages`.")
    passages: list[Passage] = Field(default_factory=list,
                                    description="Retrieved text, filled only when degraded.")


def require_key(x_api_key: str | None = Header(default=None)) -> str:
    keys = _load_keys()
    if not x_api_key or x_api_key not in keys:
        # Same response for missing and wrong, so the endpoint does not confirm
        # which keys exist.
        raise HTTPException(status_code=401, detail="invalid or missing API key")
    return x_api_key


def enforce_rate_limit(key: str) -> None:
    now = time.monotonic()
    hits = _HITS[key]
    while hits and now - hits[0] > RATE_WINDOW_S:
        hits.popleft()
    if len(hits) >= RATE_LIMIT:
        retry = int(RATE_WINDOW_S - (now - hits[0])) + 1
        raise HTTPException(status_code=429, detail="rate limit exceeded",
                            headers={"Retry-After": str(retry)})
    hits.append(now)


@app.get("/health")
def health():
    """Liveness and readiness in one place, and it reports its dependencies.
    A health check that returns 200 whatever the state of the thing it fronts is
    a check that something is listening, which is not the question anyone asks."""
    reachable = model_reachable()
    ok = bool(STATE.get("chunks")) and reachable
    body = {"status": "ok" if ok else "degraded",
            "corpus_chunks": len(STATE.get("chunks", [])),
            "generation_endpoint": reachable,
            "rungs": STATE["ladder"].states() if STATE.get("ladder") else {},
            "version": API_VERSION}
    return JSONResponse(body, status_code=200 if ok else 503)


@app.get("/version")
def version():
    return {"version": API_VERSION, "model": STATE.get("model"),
            "corpus_hash": STATE.get("corpus_hash")}


@app.post(f"/{API_VERSION}/ask", response_model=AskResponse)
def ask(req: AskRequest, response: Response, key: str = Depends(require_key)):
    enforce_rate_limit(key)
    # Ready means the corpus loaded. A missing model is not "not ready" any more:
    # the last rung of the ladder answers with the retrieved passages.
    if not STATE.get("chunks"):
        raise HTTPException(status_code=503, detail="service not ready")

    picked = retrieve(req.question, req.k)
    ctx = "\n\n".join(f"[{i+1}] {c['text']}" for i, c in enumerate(picked))

    system = ("Answer ONLY from the numbered context. Cite chunk numbers like [2]. "
              "If the context does not contain the answer, reply exactly: NOT IN CONTEXT.")
    user = f"Context:\n{ctx}\n\nQuestion: {req.question}"
    try:
        rung, choice = STATE["ladder"].complete(
            lambda r, deadline: generate(r, deadline, system, user))
    except AllRungsFailed:
        if not req.allow_degraded:
            # The contract callers already had: no model, no answer, and a status
            # that says so. Retrying after the breaker's cool-down is sensible.
            raise HTTPException(status_code=503, detail="generation unavailable",
                                headers={"Retry-After": str(max(1, int(BREAKER_COOLDOWN_S)))})
        # Opted in: the evidence retrieval already found, labelled as what it is.
        # `answer` carries only a notice, so a client that prints it cannot present
        # passages as an answer; the header lets a proxy or log see it without parsing.
        response.headers["X-Degraded"] = RETRIEVAL_ONLY
        return AskResponse(
            answer="Generation is unavailable. The passages below are unsummarised "
                   "retrieval results, not an answer.",
            sources=sorted({c["doc_id"] for c in picked}),
            grounded=False, model="none", rung=RETRIEVAL_ONLY, degraded=True,
            passages=[Passage(doc_id=c["doc_id"], text=c["text"]) for c in picked])

    answer = re.sub(r"<think>.*?</think>", "",
                    choice["message"]["content"] or "", flags=re.S).strip()
    if choice.get("finish_reason") == "length":
        raise HTTPException(status_code=502, detail="generation truncated")

    return AskResponse(answer=answer,
                       sources=sorted({c["doc_id"] for c in picked}),
                       grounded=not answer.upper().startswith("NOT IN CONTEXT"),
                       model=rung.model, rung=rung.name)


@app.exception_handler(Exception)
async def unhandled(request: Request, exc: Exception):
    """Never return an exception message to a caller. It is the cheapest way to
    leak a path, a hostname or a key."""
    return JSONResponse({"detail": "internal error"}, status_code=500)
