"""Provider fallback: a ladder of generation endpoints, a deadline, a breaker.

Taught in lessons/block8-deployment "When the Provider Goes Down". Standard
library only, so it adds nothing to the image.

A rung is one place a completion can come from. The ladder tries them in order.
A breaker per rung stops later requests paying the full deadline again once a
rung has failed repeatedly. When every rung fails or is skipped the caller
decides what the last step is; the service answers with the retrieved passages.
"""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field


class AllRungsFailed(Exception):
    """Every rung failed or was skipped by its breaker."""


@dataclass
class Rung:
    name: str
    base: str
    model: str | None = None


class Breaker:
    """closed -> open after `threshold` consecutive failures -> half-open after
    `cooldown_s`, admitting exactly one probe -> closed on success, open on failure."""

    def __init__(self, threshold: int = 3, cooldown_s: float = 30.0, clock=time.monotonic):
        self.threshold = threshold
        self.cooldown_s = cooldown_s
        self._clock = clock
        self._lock = threading.Lock()
        self._failures = 0
        self._opened_at: float | None = None
        self._probing = False

    @property
    def state(self) -> str:
        with self._lock:
            if self._opened_at is None:
                return "closed"
            if self._clock() - self._opened_at >= self.cooldown_s:
                return "half-open"
            return "open"

    def allow(self) -> bool:
        with self._lock:
            if self._opened_at is None:
                return True
            if self._clock() - self._opened_at < self.cooldown_s:
                return False
            if self._probing:
                return False  # one probe at a time
            self._probing = True
            return True

    def success(self) -> None:
        with self._lock:
            self._failures = 0
            self._opened_at = None
            self._probing = False

    def failure(self) -> None:
        with self._lock:
            self._failures += 1
            if self._probing or self._failures >= self.threshold:
                self._opened_at = self._clock()
            self._probing = False


@dataclass
class Ladder:
    rungs: list[Rung]
    deadline_s: float = 60.0
    threshold: int = 3
    cooldown_s: float = 30.0
    clock: object = time.monotonic
    breakers: dict[str, Breaker] = field(init=False)
    served: dict[str, int] = field(init=False)

    def __post_init__(self):
        self.breakers = {r.name: Breaker(self.threshold, self.cooldown_s, self.clock)
                         for r in self.rungs}
        self.served = {r.name: 0 for r in self.rungs}
        self._lock = threading.Lock()

    def complete(self, send):
        """Call `send(rung, deadline_s)` down the ladder; return (rung, result).

        `send` raises on any failure, including exceeding the deadline. Raises
        AllRungsFailed when nothing answered."""
        for rung in self.rungs:
            breaker = self.breakers[rung.name]
            if not breaker.allow():
                continue
            try:
                result = send(rung, self.deadline_s)
            except Exception:
                breaker.failure()
                continue
            breaker.success()
            with self._lock:
                self.served[rung.name] += 1
            return rung, result
        raise AllRungsFailed("no generation rung answered")

    def states(self) -> dict[str, str]:
        return {name: b.state for name, b in self.breakers.items()}
