"""A stand-in model provider whose behaviour the test controls.

Shared by the failover tests and the capstone failure drill. Named loudly as a
stub wherever it is used: it exercises the real service's fallback logic and
says nothing about any real provider's latency or failure behaviour.
"""
from __future__ import annotations

import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class StubProvider:
    """mode: "ok" answers, "error" returns 500, "slow" sleeps `delay_s` first, "drip"
    answers one byte every `delay_s` seconds (every read succeeds, the whole is slow),
    "status" returns `self.status`."""

    def __init__(self, name: str, mode: str = "ok", delay_s: float = 5.0):
        self.name, self.mode, self.delay_s = name, mode, delay_s
        self.status = 400  # used by mode "status"
        self.calls = 0
        owner = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_):
                pass

            def _send(self, code, body):
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def do_GET(self):
                if self.path == "/v1/models":
                    self._send(200, json.dumps({"data": [{"id": f"stub-{owner.name}"}]}).encode())
                else:
                    self._send(404, b"{}")

            def do_POST(self):
                self.rfile.read(int(self.headers.get("Content-Length", 0)))
                owner.calls += 1
                if owner.mode == "slow":
                    time.sleep(owner.delay_s)
                if owner.mode == "status":
                    self._send(owner.status, b'{"error":"stub status"}')
                    return
                if owner.mode == "error":
                    self._send(500, b'{"error":"stub failure"}')
                    return
                payload = {"choices": [{"message": {"content": f"answer from {owner.name} [1]"},
                                        "finish_reason": "stop"}]}
                data = json.dumps(payload).encode()
                if owner.mode == "drip":
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Content-Length", str(len(data)))
                    self.end_headers()
                    try:
                        for i in range(len(data)):
                            self.wfile.write(data[i:i + 1])
                            self.wfile.flush()
                            time.sleep(owner.delay_s)
                    except OSError:
                        pass
                    return
                self._send(200, data)

        self._server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.base = f"http://127.0.0.1:{self._server.server_port}/v1"
        threading.Thread(target=self._server.serve_forever, daemon=True).start()

    def close(self):
        self._server.shutdown()
        self._server.server_close()
