"""Tests for the things that make this a service rather than a script.

Deliberately not testing answer quality — that is Project 2's job and it needs a
model. These test the interface contract: that an unauthenticated caller cannot
get in, that a rate limit actually limits, that validation rejects what it should,
and that the health check reports the truth rather than that something is running.
"""
import os
import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("API_KEYS", "test-key-a,test-key-b")
os.environ.setdefault("RATE_LIMIT", "3")
# A long window on purpose. Requests here make real model calls taking tens of
# seconds, and a 60-second window slides open mid-test — the limiter is correct
# and the test was measuring its own latency.
os.environ.setdefault("RATE_WINDOW_S", "3600")

from src import app as appmod  # noqa: E402


@pytest.fixture
def client():
    with TestClient(appmod.app) as c:
        appmod._HITS.clear()
        yield c


def test_corpus_actually_loaded(client):
    """Guards the failure that made this suite green while testing nothing: a wrong
    corpus path left the service permanently not-ready, so every request returned
    503 before reaching any of the behaviour under test."""
    assert appmod.STATE["chunks"], "corpus did not load — CORPUS_DIR is wrong"
    assert len(appmod.STATE["chunks"]) > 10


def test_health_is_public_and_reports_state(client):
    r = client.get("/health")
    assert r.status_code in (200, 503)
    body = r.json()
    assert "corpus_chunks" in body and "generation_endpoint" in body
    # A degraded service must say so rather than returning 200 regardless.
    if not body["generation_endpoint"]:
        assert r.status_code == 503 and body["status"] == "degraded"


def test_ask_requires_a_key(client):
    r = client.post("/v1/ask", json={"question": "what is the temperature limit?"})
    assert r.status_code == 401


def test_wrong_key_is_indistinguishable_from_missing(client):
    missing = client.post("/v1/ask", json={"question": "what is the limit?"})
    wrong = client.post("/v1/ask", json={"question": "what is the limit?"},
                        headers={"X-API-Key": "not-a-real-key"})
    assert missing.status_code == wrong.status_code == 401
    assert missing.json() == wrong.json()


def test_validation_rejects_bad_input(client):
    h = {"X-API-Key": "test-key-a"}
    assert client.post("/v1/ask", json={"question": "hi"}, headers=h).status_code == 422
    assert client.post("/v1/ask", json={"question": "x" * 501}, headers=h).status_code == 422
    assert client.post("/v1/ask", json={"question": "a valid question", "k": 99},
                       headers=h).status_code == 422
    assert client.post("/v1/ask", json={}, headers=h).status_code == 422


def test_rate_limit_triggers_and_reports_retry_after(client):
    h = {"X-API-Key": "test-key-a"}
    payload = {"question": "what is the gearbox temperature limit?"}
    seen = [client.post("/v1/ask", json=payload, headers=h).status_code
            for _ in range(appmod.RATE_LIMIT + 1)]
    assert seen[-1] == 429, f"expected the {appmod.RATE_LIMIT + 1}th call to be limited, got {seen}"
    limited = client.post("/v1/ask", json=payload, headers=h)
    assert limited.status_code == 429
    assert "Retry-After" in limited.headers


def test_rate_limit_is_per_key(client):
    payload = {"question": "what is the gearbox temperature limit?"}
    for _ in range(appmod.RATE_LIMIT + 1):
        client.post("/v1/ask", json=payload, headers={"X-API-Key": "test-key-a"})
    # key-a is now limited; key-b must be unaffected, or one caller can deny others.
    other = client.post("/v1/ask", json=payload, headers={"X-API-Key": "test-key-b"})
    assert other.status_code != 429


def test_version_is_public(client):
    assert client.get("/version").status_code == 200


def test_version_reports_the_corpus_identity(client):
    """The data identity scripts/build_corpus_artifact.py writes must be
    queryable from the running service, or there is no way to answer which
    corpus a deployed instance is actually serving."""
    body = client.get("/version").json()
    assert "corpus_hash" in body
    assert body["corpus_hash"], "corpus_id.json was not built or not loaded"
    assert len(body["corpus_hash"]) == 64  # sha256 hex


def test_service_refuses_to_start_without_keys(monkeypatch):
    monkeypatch.setenv("API_KEYS", "")
    with pytest.raises(RuntimeError, match="API_KEYS"):
        with TestClient(appmod.app):
            pass
