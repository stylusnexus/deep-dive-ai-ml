"""The ladder and breaker on their own, with a fake clock and no network."""
import pytest

from src.resilience import AllRungsFailed, Breaker, Ladder, RequestRejected, Rung


class Clock:
    def __init__(self):
        self.t = 0.0

    def __call__(self):
        return self.t


def test_breaker_opens_after_threshold_consecutive_failures():
    clock = Clock()
    b = Breaker(threshold=3, cooldown_s=10, clock=clock)
    for _ in range(2):
        b.failure()
    assert b.state == "closed" and b.allow()
    b.failure()
    assert b.state == "open" and not b.allow()


def test_a_success_resets_the_failure_count():
    b = Breaker(threshold=3, cooldown_s=10, clock=Clock())
    b.failure(); b.failure(); b.success(); b.failure(); b.failure()
    assert b.state == "closed"


def test_half_open_admits_exactly_one_probe():
    clock = Clock()
    b = Breaker(threshold=1, cooldown_s=10, clock=clock)
    b.failure()
    clock.t = 10
    assert b.state == "half-open"
    assert b.allow() is True       # the probe
    assert b.allow() is False      # nobody else while it is in flight


def test_failed_probe_reopens_and_successful_probe_closes():
    clock = Clock()
    b = Breaker(threshold=1, cooldown_s=10, clock=clock)
    b.failure(); clock.t = 10; assert b.allow()
    b.failure()
    assert b.state == "open"
    clock.t = 20; assert b.allow()
    b.success()
    assert b.state == "closed" and b.allow()


def _ladder(clock=None, **kw):
    return Ladder([Rung("a", "http://a"), Rung("b", "http://b")],
                  clock=clock or Clock(), **kw)


def test_first_healthy_rung_answers():
    rung, out = _ladder().complete(lambda r, d: r.name)
    assert (rung.name, out) == ("a", "a")


def test_failure_moves_down_a_rung():
    def send(r, d):
        if r.name == "a":
            raise RuntimeError("down")
        return "ok"
    rung, _ = _ladder().complete(send)
    assert rung.name == "b"


def test_open_breaker_skips_the_rung_without_calling_it():
    calls = []

    def send(r, d):
        calls.append(r.name)
        if r.name == "a":
            raise RuntimeError("down")
        return "ok"
    ladder = _ladder(threshold=2)
    for _ in range(2):
        ladder.complete(send)
    calls.clear()
    ladder.complete(send)
    assert calls == ["b"], "rung a should be skipped, not tried and failed again"


def test_all_rungs_failing_raises():
    def send(r, d):
        raise RuntimeError("down")
    with pytest.raises(AllRungsFailed):
        _ladder().complete(send)


def test_deadline_is_passed_to_every_call():
    seen = []
    _ladder(deadline_s=7.5).complete(lambda r, d: seen.append(d))
    assert seen == [7.5]


def test_a_rejected_request_is_not_a_breaker_failure_and_frees_the_probe():
    clock = Clock()
    lad = _ladder(clock, threshold=1, cooldown_s=10)
    lad.breakers["a"].failure()
    clock.t = 11  # half-open: one probe allowed

    def send(r, d):
        if r.name == "a":
            raise RequestRejected("400")
        return "ok"

    rung, _ = lad.complete(send)
    assert rung.name == "b"
    assert lad.breakers["a"].state == "half-open", "probe slot must be given back, breaker not closed"
    assert lad.breakers["a"].allow(), "the next request may probe again"
