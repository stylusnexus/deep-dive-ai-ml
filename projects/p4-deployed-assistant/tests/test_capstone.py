"""The capstone's failure drill must not leave the app pointed at its stubs."""
import importlib.util
import os
import pathlib

os.environ.setdefault("API_KEYS", "test-key-a,test-key-b")
os.environ.setdefault("RATE_LIMIT", "1000")
os.environ.setdefault("RATE_WINDOW_S", "3600")

from src import app as appmod  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent


def test_drill_restores_the_endpoints_and_timings_it_changes(monkeypatch):
    # test_app.py sets a low rate limit at import; the drill makes many calls on purpose.
    monkeypatch.setattr(appmod, "RATE_LIMIT", 100000)
    appmod._HITS.clear()
    spec = importlib.util.spec_from_file_location("run_capstone", ROOT / "capstone" / "run_capstone.py")
    capstone = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(capstone)
    before = {k: getattr(appmod, k) for k in
              ("ENDPOINTS", "GENERATION_DEADLINE_S", "BREAKER_THRESHOLD", "BREAKER_COOLDOWN_S")}
    results = capstone.run_drill()
    assert all(r["pass"] for r in results)
    after = {k: getattr(appmod, k) for k in before}
    assert after == before, "the gold-set run that follows would inherit closed stub servers"
