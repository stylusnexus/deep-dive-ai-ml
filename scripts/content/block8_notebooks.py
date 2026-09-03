OUTDIR = "notebooks/08-deploy-apis"

_SERVER = '''import json, random, threading, time, urllib.error, urllib.request
from collections import Counter
from http.server import BaseHTTPRequestHandler, HTTPServer

random.seed(8)

# A server that fails on purpose, in a scripted order, so every client below meets
# exactly the same weather. No network, no key, no third party — the failures are
# the point and they have to be reproducible to be measurable.
SCRIPT = ["429", "500", "ok", "503", "ok", "429", "400", "ok", "504", "ok",
          "ok", "429", "500", "ok", "ok", "slow", "ok", "503", "ok", "ok"]

STATE = {"i": 0, "calls": 0, "applied": [], "keys": set()}

class Flaky(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_POST(self):
        STATE["calls"] += 1
        step = SCRIPT[STATE["i"] % len(SCRIPT)]
        STATE["i"] += 1
        n = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(n) or b"{}")
        key = self.headers.get("Idempotency-Key")

        if step == "429":
            self.send_response(429); self.send_header("Retry-After", "1")
            self.end_headers(); self.wfile.write(b'{"error":"rate limited"}'); return
        if step in ("500", "503", "504"):
            self.send_response(int(step)); self.end_headers()
            self.wfile.write(b'{"error":"upstream"}'); return
        if step == "400":
            self.send_response(400); self.end_headers()
            self.wfile.write(b'{"error":"malformed request"}'); return
        if step == "slow":
            # The dangerous case: the work IS done, the reply never arrives in time.
            if key is None or key not in STATE["keys"]:
                STATE["applied"].append(body.get("order"))
                if key: STATE["keys"].add(key)
            time.sleep(2.5)
            self.send_response(200); self.end_headers(); self.wfile.write(b'{"ok":true}'); return

        if key is not None and key in STATE["keys"]:
            self.send_response(200); self.end_headers()
            self.wfile.write(b'{"ok":true,"duplicate":true}'); return
        STATE["applied"].append(body.get("order"))
        if key:
            STATE["keys"].add(key)
        self.send_response(200); self.end_headers(); self.wfile.write(b'{"ok":true}')

srv = HTTPServer(("127.0.0.1", 0), Flaky)
PORT = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{PORT}/charge"
print(f"flaky server listening on {URL}")
print(f"scripted outcomes: {Counter(SCRIPT)}")'''


_CALL = '''def call(order, key=None, timeout=1.0):
    """One request. Returns (status, body) or raises on a transport-level failure."""
    data = json.dumps({"order": order}).encode()
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Idempotency-Key"] = key
    req = urllib.request.Request(URL, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, {"retry_after": e.headers.get("Retry-After")}
    except Exception:
        return None, {"error": "timeout"}   # you do not know whether it happened

def reset():
    STATE.update(i=0, calls=0, applied=[], keys=set())

print("call() returns a status, or None when the request timed out —")
print("and None is the interesting one, because it is the case you cannot interpret")'''


_NAIVE = '''# The client most people write first: retry everything, a fixed number of times,
# with a fixed delay. It is not obviously wrong until you count what it did.
def naive_client(orders, attempts=4, delay=0.15):
    ok = failed = 0
    for o in orders:
        for _ in range(attempts):
            status, _body = call(o)
            if status == 200:
                ok += 1
                break
            time.sleep(delay)
        else:
            failed += 1
    return ok, failed

reset()
t0 = time.time()
ok, failed = naive_client([f"ORD-{i:03d}" for i in range(10)])
naive = dict(ok=ok, failed=failed, server_calls=STATE["calls"],
             applied=len(STATE["applied"]), unique=len(set(STATE["applied"])),
             seconds=round(time.time() - t0, 1))
print(json.dumps(naive, indent=2))
print(f"\\nduplicate charges applied: {naive['applied'] - naive['unique']}")'''


_CORRECT = '''# Three changes, each from a different line of the lesson.
RETRYABLE = {429, 500, 502, 503, 504, None}    # None = timeout: unknown, so retry
TERMINAL  = {400, 401, 403, 404, 422}          # your fault: retrying cannot help

def careful_client(orders, attempts=4, base=0.1):
    ok = failed = gave_up_early = 0
    for i, o in enumerate(orders):
        key = f"key-{o}"                        # stable per order, so a retry is not a second charge
        for attempt in range(attempts):
            status, body = call(o, key=key)
            if status == 200:
                ok += 1
                break
            if status in TERMINAL:
                gave_up_early += 1              # do not spend three more calls on a 400
                break
            wait = float(body.get("retry_after") or 0) or base * (2 ** attempt)
            wait = min(wait, 0.8) * (0.5 + random.random())   # cap, and jitter
            time.sleep(wait)
        else:
            failed += 1
    return ok, failed, gave_up_early

reset()
t0 = time.time()
ok, failed, early = careful_client([f"ORD-{i:03d}" for i in range(10)])
careful = dict(ok=ok, failed=failed, gave_up_on_4xx=early, server_calls=STATE["calls"],
               applied=len(STATE["applied"]), unique=len(set(STATE["applied"])),
               seconds=round(time.time() - t0, 1))
print(json.dumps(careful, indent=2))
print(f"\\nduplicate charges applied: {careful['applied'] - careful['unique']}")'''


_COMPARE = '''rows = [("succeeded", naive["ok"], careful["ok"]),
        ("gave up", naive["failed"], careful["failed"]),
        ("calls made to the server", naive["server_calls"], careful["server_calls"]),
        ("charges applied", naive["applied"], careful["applied"]),
        ("DUPLICATE charges", naive["applied"] - naive["unique"],
                              careful["applied"] - careful["unique"]),
        ("seconds", naive["seconds"], careful["seconds"])]

print(f"{'':<28}{'naive':>10}{'careful':>10}")
print("-" * 48)
for label, a, b in rows:
    print(f"{label:<28}{a:>10}{b:>10}")'''


_LITTLE = '''# Little's law: requests resident = arrival rate x time in system.
# The sizing question, answered before you meet it in production.
def concurrency(rps, seconds_per_request):
    return rps * seconds_per_request

print(f"{'req/sec':>9}{'sec each':>10}{'resident':>10}   verdict at capacity 12")
for rps, dur in [(2, 4), (5, 4), (10, 4), (10, 1.5), (20, 0.8)]:
    n = concurrency(rps, dur)
    verdict = "fits" if n <= 12 else f"needs {n/12:.1f}x the capacity"
    print(f"{rps:>9}{dur:>10}{n:>10.0f}   {verdict}")

print("\\nread it backwards for the useful version: at 10 req/sec, fitting in 12 slots")
print(f"means {12/10:.1f}s per request or faster. That is a latency target derived from")
print("a capacity limit, rather than a number somebody picked.")'''


NOTEBOOKS = [
("01-the-client-that-survives.ipynb", [

("md", """# 08 · The Client That Survives

Every system in this course eventually calls something it does not control. The
lesson gives the rules — read the status code, make writes idempotent, back off with
jitter. This runs them against a server that fails on purpose, so the difference
between the two clients is a number rather than an argument.

There is no third-party API here. The notebook starts a small HTTP server in this
process that returns a **scripted** sequence of failures, which means both clients
meet identical weather and the comparison is fair. No key, no network, no cost."""),

("code", _SERVER),

("md", """Note the `slow` step in that script. It is the one that matters: the server does the
work and then takes longer than the client is willing to wait. The client sees a
timeout and has no way to know whether the charge was applied — which is the
condition the whole idea of idempotency exists to handle."""),

("code", _CALL),

("md", """## The client most people write first

Retry everything, a fixed number of times, with a fixed delay. It is not obviously
wrong. Count what it actually did."""),

("code", _NAIVE),

("md", """## The same job, three changes

- **Classify the status.** A 400 means you sent something wrong; sending it again
  unchanged cannot help, so three further attempts are three wasted calls and three
  extra seconds.
- **Send an idempotency key.** Stable per order, so a retry after a timeout is
  recognised as the same request rather than a second charge.
- **Back off, honour `Retry-After`, and jitter.** Exponential so a struggling server
  gets room, capped so a slow recovery does not become a hang, and jittered so many
  clients do not retry in lockstep."""),

("code", _CORRECT),

("code", _COMPARE),

("md", """The row to look at is duplicate charges. Everything else is efficiency; that one is
money moving twice. It comes entirely from the timeout case, where the naive client
could not distinguish "the request failed" from "the reply was lost" and chose the
interpretation that made it retry.

Now the two rows that look like the careful client losing, because both are it
behaving correctly and are worth reading slowly.

**It took longer.** Backing off properly means waiting, and honouring a `Retry-After`
of one second means waiting a full second. The naive client is faster precisely
because it hammers, and a server already returning 429 is a server that gets worse
when hammered. Speed measured against a scripted server that cannot fall over is
flattering the wrong thing.

**It succeeded once less.** That missing success is the 400. The naive client retried
a malformed request until the scripted weather changed underneath it and something
else returned 200 — so it recorded a success for a request the server had rejected as
invalid. That is not a tenth success, it is a client bulldozing past a real error and
reporting the outcome as fine. The careful client stopped, counted it separately, and
is the only one of the two whose success count means what it says."""),

("md", """## The sizing question, before production asks it

Little's law relates concurrency, arrival rate and duration. It holds regardless of
what the queue does internally, which makes it useful when you know nothing about the
internals — including when the thing you are sizing is somebody else's API."""),

("code", _LITTLE),

("md", """## What to carry into your own client

- **Retry only what retrying can fix.** 4xx is your bug and a repeat is a wasted call.
- **Treat a timeout as unknown, never as a failure.** It is the only status where the
  work may already be done, and it is the only one that needs an idempotency key.
- **Honour `Retry-After` when the server sends it.** It knows something you do not.
- **Jitter every backoff.** Without it, everything that failed together retries
  together, and the recovery is what takes the server down.
- **Derive the latency target from the capacity**, rather than choosing a round number
  and hoping.
- **Do not read "faster" as "better" from a comparison like this one.** A scripted
  server cannot be overwhelmed, so it cannot show you the cost of hammering — which is
  the entire reason backoff exists.

The checklist is `artifacts/sop/llm-engineering.md`, and the failure this notebook
makes concrete — a retry that charges twice — is the reason its idempotency line is
there."""),
]),
]
