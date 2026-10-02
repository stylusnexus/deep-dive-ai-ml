#!/usr/bin/env python3
"""Measure the real /v1/ask entry point, not a stand-in for "a server."

notebooks/08-deploy-apis/02-serving-measured.ipynb benchmarks a sleeping
fixture to teach the methodology. This script runs the same methodology
against src.app:app itself — real auth, real rate limiting, real retrieval
over the real corpus, through a real HTTP connection to a real uvicorn
process in a child thread.

The one honest substitution: GENERATION_ENDPOINTS points at a local stub
chat-completions server instead of a real model, because this measurement
runs with no paid API key and no deployed instance. That substitution is
named in every line of output below it. Re-run this against the deployed
Render instance with a real GENERATION_ENDPOINTS before treating these
numbers as capacity evidence for production.

Run from the project root:
    /path/to/venv/bin/python bench_serving.py
"""
from __future__ import annotations

import json
import os
import pathlib
import statistics
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.request import Request, urlopen

ROOT = pathlib.Path(__file__).resolve().parent
STUB_MODEL_NAME = "local-stub-chat-v1"
API_KEY = "bench-key"


class StubGenerationHandler(BaseHTTPRequestHandler):
    """An OpenAI-chat-completions-shaped stand-in. Named loudly in every
    result this script prints — it is not a claim about a real model's
    latency, only a way to exercise the real service end to end."""

    def log_message(self, *_):
        pass

    def do_GET(self):
        if self.path == "/v1/models":
            body = json.dumps({"data": [{"id": STUB_MODEL_NAME}]}).encode()
            self._send(200, body)
        else:
            self._send(404, b"{}")

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        self.rfile.read(n)
        time.sleep(0.01)  # a trivial stand-in for generation latency
        payload = {
            "choices": [{"message": {"content": "The limit is 85C per OPS-STD-04."},
                        "finish_reason": "stop"}],
        }
        self._send(200, json.dumps(payload).encode())

    def _send(self, code, body):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def start_stub_generation_server() -> str:
    server = ThreadingHTTPServer(("127.0.0.1", 0), StubGenerationHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{server.server_port}/v1"


def start_real_app(generation_base: str):
    """Start src.app:app for real, via uvicorn, in this process's event loop
    running on a background thread — the actual FastAPI application object,
    not a reimplementation of its routes."""
    os.environ["API_KEYS"] = API_KEY
    os.environ["RATE_LIMIT"] = "100000"          # measuring the service, not the limiter
    os.environ["RATE_WINDOW_S"] = "60"
    os.environ["CORPUS_DIR"] = str(ROOT / "corpus")
    os.environ["GENERATION_ENDPOINTS"] = generation_base

    import uvicorn
    from src import app as appmod

    config = uvicorn.Config(appmod.app, host="127.0.0.1", port=0, log_level="warning")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    while not getattr(server, "started", False):
        time.sleep(0.01)
    port = server.servers[0].sockets[0].getsockname()[1]
    return server, f"http://127.0.0.1:{port}"


def request_once(base_url: str) -> float:
    started = time.perf_counter()
    body = json.dumps({"question": "What is the maximum gearbox oil temperature?"}).encode()
    req = Request(f"{base_url}/v1/ask", data=body, method="POST",
                  headers={"Content-Type": "application/json", "X-API-Key": API_KEY})
    with urlopen(req, timeout=10) as response:
        payload = json.loads(response.read())
        assert response.status == 200, payload
    return (time.perf_counter() - started) * 1000


def benchmark(base_url: str, concurrency: int, requests: int = 32) -> dict:
    started = time.perf_counter()
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        latencies = list(pool.map(lambda _: request_once(base_url), range(requests)))
    elapsed = time.perf_counter() - started
    ordered = sorted(latencies)
    p50 = statistics.median(ordered)
    p95 = ordered[max(0, int(len(ordered) * 0.95) - 1)]
    return {"concurrency": concurrency, "requests": requests,
            "throughput_rps": round(requests / elapsed, 1),
            "p50_ms": round(p50, 1), "p95_ms": round(p95, 1)}


def main():
    generation_base = start_stub_generation_server()
    server, base_url = start_real_app(generation_base)

    from src import app as appmod
    version = json.loads(urlopen(f"{base_url}/version").read())
    health = json.loads(urlopen(f"{base_url}/health").read())
    print("real entry point:", base_url)
    print("generation endpoint (named stand-in, see module docstring):", generation_base)
    print("run record:", json.dumps({
        "model": version["model"], "corpus_hash": version["corpus_hash"],
        "corpus_chunks": health["corpus_chunks"],
        "service_status": health["status"],
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }, indent=2))
    assert health["status"] == "ok", "service did not reach ready — nothing below is measuring /v1/ask"

    rows = [benchmark(base_url, c) for c in (1, 2, 4, 8)]
    print("\nconcurrency sweep against the real /v1/ask handler:")
    print(json.dumps(rows, indent=2))

    print("\nThese numbers describe this fixture corpus, this machine, and a 10ms local "
          "stub standing in for generation latency — not the deployed Render instance "
          "and not a real model. Re-run against the real deployed entry point with a "
          "real GENERATION_ENDPOINTS before using these as capacity evidence.")

    server.should_exit = True


if __name__ == "__main__":
    main()
