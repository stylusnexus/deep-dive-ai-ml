"""The real service against stub providers that fail on command.

These answer one question: when the primary misbehaves, which rung answers and
how long does the caller wait. They run the real handler over HTTP-shaped calls
and a stub that stands in for a provider. They do not measure any real provider.
"""
import os
import time

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("API_KEYS", "test-key-a,test-key-b")
os.environ.setdefault("RATE_LIMIT", "1000")
os.environ.setdefault("RATE_WINDOW_S", "3600")

from src import app as appmod  # noqa: E402
from tests.stubs import StubProvider  # noqa: E402

H = {"X-API-Key": "test-key-a"}
Q = {"question": "What gearbox oil temperature triggers a controlled shutdown?"}


@pytest.fixture
def world(monkeypatch):
    primary, secondary = StubProvider("primary"), StubProvider("secondary")
    monkeypatch.setattr(appmod, "ENDPOINTS", [primary.base, secondary.base])
    # test_app.py sets a low limit at import; these tests make many calls on purpose.
    monkeypatch.setattr(appmod, "RATE_LIMIT", 1000)
    monkeypatch.setattr(appmod, "GENERATION_DEADLINE_S", 1.0)
    monkeypatch.setattr(appmod, "BREAKER_THRESHOLD", 2)
    monkeypatch.setattr(appmod, "BREAKER_COOLDOWN_S", 0.5)
    with TestClient(appmod.app) as client:
        appmod._HITS.clear()
        appmod.STATE["ladder"] = appmod.build_ladder()
        yield client, primary, secondary
    primary.close(); secondary.close()


def ask(client):
    return client.post("/v1/ask", json=Q, headers=H)


def test_healthy_primary_answers(world):
    client, primary, secondary = world
    body = ask(client).json()
    assert body["rung"] == "rung-1" and not body["degraded"]
    assert secondary.calls == 0


def test_primary_errors_fall_to_secondary(world):
    client, primary, secondary = world
    primary.mode = "error"
    body = ask(client).json()
    assert body["rung"] == "rung-2" and "secondary" in body["answer"]


def test_breaker_stops_calling_a_failing_primary(world):
    client, primary, secondary = world
    primary.mode = "error"
    for _ in range(2):
        ask(client)
    before = primary.calls
    for _ in range(3):
        assert ask(client).json()["rung"] == "rung-2"
    assert primary.calls == before, "an open breaker must not keep sending to the primary"


def test_slow_primary_is_abandoned_at_the_deadline(world):
    client, primary, secondary = world
    primary.mode, primary.delay_s = "slow", 3.0
    started = time.perf_counter()
    body = ask(client).json()
    waited = time.perf_counter() - started
    assert body["rung"] == "rung-2"
    assert waited < 2.5, f"waited {waited:.1f}s; the 1s deadline should have cut it off"


def test_a_provider_that_drips_bytes_is_cut_off_at_the_total_deadline(world):
    """Every socket read succeeds within the deadline, so a per-read timeout never
    fires. The wall-clock limit must."""
    client, primary, secondary = world
    primary.mode, primary.delay_s = "drip", 0.3
    started = time.perf_counter()
    body = ask(client).json()
    waited = time.perf_counter() - started
    assert body["rung"] == "rung-2"
    assert waited < 2.5, f"waited {waited:.1f}s; the 1s deadline is a total, not per read"


def test_both_down_is_an_error_by_default(world):
    """A caller that knows nothing about degraded replies must still see a failure."""
    client, primary, secondary = world
    primary.mode = secondary.mode = "error"
    r = ask(client)
    assert r.status_code == 503
    assert "Retry-After" in r.headers
    assert "passages" not in r.json()


def test_opt_in_returns_labelled_passages_not_an_answer(world):
    client, primary, secondary = world
    primary.mode = secondary.mode = "error"
    r = client.post("/v1/ask", json={**Q, "allow_degraded": True}, headers=H)
    body = r.json()
    assert r.status_code == 200
    assert r.headers["X-Degraded"] == "retrieval-only"
    assert body["rung"] == "retrieval-only" and body["degraded"] is True
    assert body["grounded"] is False and body["model"] == "none"
    assert "90 degrees" not in body["answer"], "answer must be a notice, not the passages"
    assert "90 degrees" in " ".join(" ".join(p["text"].split()) for p in body["passages"])


def test_healthy_reply_is_not_marked_degraded(world):
    client, primary, secondary = world
    r = client.post("/v1/ask", json={**Q, "allow_degraded": True}, headers=H)
    assert r.json()["degraded"] is False and r.json()["passages"] == []
    assert "X-Degraded" not in r.headers


def test_primary_recovers_after_the_cooldown(world):
    client, primary, secondary = world
    primary.mode = "error"
    for _ in range(2):
        ask(client)
    primary.mode = "ok"
    time.sleep(0.6)  # past the 0.5s cooldown: one probe is admitted
    assert ask(client).json()["rung"] == "rung-1"


def test_health_is_ok_while_a_rung_is_reachable(world):
    client, primary, secondary = world
    body = client.get("/health").json()
    assert body["status"] == "ok" and body["generation_endpoint"] is True


def test_health_degrades_when_every_breaker_is_open(world):
    """The check has to follow the providers, not report the state at startup."""
    client, primary, secondary = world
    primary.mode = secondary.mode = "error"
    for _ in range(2):
        assert ask(client).status_code == 503
    r = client.get("/health")
    assert r.status_code == 503
    assert r.json()["status"] == "degraded" and r.json()["generation_endpoint"] is False
    assert set(r.json()["rungs"].values()) == {"open"}


def test_health_recovers_once_a_provider_is_back(world):
    client, primary, secondary = world
    primary.mode = secondary.mode = "error"
    for _ in range(2):
        ask(client)
    assert client.get("/health").status_code == 503
    primary.mode = secondary.mode = "ok"
    time.sleep(0.6)  # past the 0.5s cooldown: the health check admits one probe
    assert client.get("/health").status_code == 200
    assert ask(client).json()["rung"] == "rung-1"


def test_booting_with_no_reachable_model_starts_degraded_and_says_so(monkeypatch):
    monkeypatch.setattr(appmod, "ENDPOINTS", ["http://127.0.0.1:9/v1"])  # nothing listens
    with TestClient(appmod.app) as client:
        r = client.get("/health")
        assert r.status_code == 503 and r.json()["status"] == "degraded"
        assert r.json()["rungs"] == {"rung-1": "open"}


def test_health_stays_degraded_while_the_provider_lists_models_but_cannot_answer(world):
    """The stub lists its models even in error mode, as an overloaded provider does.
    Closing the breaker on the model list would send real questions into the failure."""
    client, primary, secondary = world
    primary.mode = secondary.mode = "error"
    for _ in range(2):
        ask(client)
    time.sleep(0.6)  # past the cooldown, so the health check probes
    calls_before = primary.calls + secondary.calls
    assert client.get("/health").status_code == 503
    assert primary.calls + secondary.calls > calls_before, "the probe must be a real completion"
    assert set(client.get("/health").json()["rungs"].values()) <= {"open", "half-open"}
