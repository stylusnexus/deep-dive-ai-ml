OUTDIR = "notebooks/04-agentic"

_SETUP = '''import json, re, textwrap, urllib.request
from pathlib import Path

ROOT = Path.cwd()
while not (ROOT / "data" / "corpus").exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

ENDPOINTS = ["http://localhost:11455/v1", "http://localhost:11434/v1"]

def find_endpoint():
    # The first entry in /v1/models is not necessarily a chat model. An
    # embedding model listed first returns HTTP 400 on a chat completion,
    # which is silent until it is not.
    for base in ENDPOINTS:
        try:
            with urllib.request.urlopen(f"{base}/models", timeout=3) as r:
                ids = [m["id"] for m in json.loads(r.read()).get("data", [])]
        except Exception:
            continue
        chat = [i for i in ids
                if not any(w in i.lower() for w in ("embed", "rerank", "whisper", "clip"))]
        if chat:
            return base, chat[0]
    return None, None

BASE, MODEL = find_endpoint()
print(f"endpoint: {MODEL} at {BASE}" if BASE else "no local endpoint — cells that call a model will be skipped")'''

NOTEBOOKS = [
("01-loop-by-hand.ipynb", [
("md", """# 01 · The Agent Loop, By Hand

Forty lines, no framework. Once you have written this, every framework afterwards
is a set of decisions you can evaluate rather than magic you have to trust.

The tools operate on the turbine corpus from Block 3, so the agent has something
real to do."""),
("code", _SETUP),
("md", """## Tools

Two of them. Note what each returns — shaped for a model to read, not copied out
of an API response."""),
("code", """DOCS = {d["doc_id"]: d for d in json.loads((ROOT / "data" / "corpus" / "manifest.json").read_text())}

def search_docs(query: str) -> str:
    \"\"\"Find documents mentioning a term. Returns ids and titles, not full text.\"\"\"
    q = query.lower()
    hits = [d for d in DOCS.values() if q in d["text"].lower() or q in d["title"].lower()]
    if not hits:
        return f"No documents mention '{query}'. Try a broader term."
    return "\\n".join(f"{d['doc_id']}: {d['title']}" for d in hits[:6])

def read_doc(doc_id: str) -> str:
    \"\"\"Read one document by id.\"\"\"
    if doc_id not in DOCS:
        return f"No document '{doc_id}'. Use search_docs first to find valid ids."
    return DOCS[doc_id]["text"]

TOOLS = {"search_docs": search_docs, "read_doc": read_doc}

TOOL_SPEC = [
  {"type": "function", "function": {
     "name": "search_docs",
     "description": "Find documents mentioning a term. Returns document ids and titles only — use read_doc to see contents.",
     "parameters": {"type": "object",
                    "properties": {"query": {"type": "string", "description": "a word or short phrase, e.g. 'vibration' or 'Clyde'"}},
                    "required": ["query"]}}},
  {"type": "function", "function": {
     "name": "read_doc",
     "description": "Read the full text of one document, by the id returned from search_docs.",
     "parameters": {"type": "object",
                    "properties": {"doc_id": {"type": "string", "description": "e.g. 'ops-std-04'"}},
                    "required": ["doc_id"]}}},
]
print(search_docs("vibration")[:200])"""),
("md", """### Read those two error messages again

`"No documents mention 'x'. Try a broader term."` and `"No document 'y'. Use
search_docs first to find valid ids."`

Both name the fix. In a loop with eight turns, an error that says only "not
found" burns one of them; an error that says what to do next gets corrected on
the next turn. This is the cheapest improvement available to any agent."""),
("md", """## The loop

Everything from the lesson, in one function."""),
("code", """SYSTEM = textwrap.dedent(\"\"\"
    You answer questions about wind farm operations using the tools provided.
    Search for relevant documents, read the ones you need, then answer.
    Cite document ids in your answer. If the documents do not contain the
    answer, say NOT IN CORPUS.
\"\"\").strip()

def call_model(messages):
    body = json.dumps({"model": MODEL, "temperature": 0, "max_tokens": 800,
                       "messages": messages, "tools": TOOL_SPEC}).encode()
    req = urllib.request.Request(f"{BASE}/chat/completions", data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read())["choices"][0]["message"]

def truncate(s, n=3000):
    return s if len(s) <= n else s[:n] + f"\\n...[truncated, {len(s)-n} chars omitted]"

def run(question, max_turns=6):
    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": question}]
    trace = []

    for turn in range(1, max_turns + 1):
        reply = call_model(messages)
        messages.append(reply)
        calls = reply.get("tool_calls") or []
        trace.append({"turn": turn, "tool_calls": [c["function"]["name"] for c in calls],
                      "content_len": len(reply.get("content") or "")})

        if not calls:                                    # observable event, not an opinion
            answer = re.sub(r"<think>.*?</think>", "", reply.get("content") or "", flags=re.S).strip()
            return {"answer": answer, "reason": "completed", "turns": turn, "trace": trace}

        for c in calls:
            name = c["function"]["name"]
            args = json.loads(c["function"]["arguments"] or "{}")
            result = TOOLS[name](**args) if name in TOOLS else f"No tool named {name}."
            trace[-1].setdefault("args", []).append(args)
            messages.append({"role": "tool", "tool_call_id": c["id"],
                             "content": truncate(str(result))})

    return {"answer": None, "reason": "turn_cap", "turns": max_turns, "trace": trace}

print("loop defined")"""),
("md", """## Run it on a single-hop question"""),
("code", """if BASE:
    r = run("What is the maximum gearbox oil temperature during continuous operation?")
    print(f"reason: {r['reason']}  turns: {r['turns']}\\n")
    for t in r["trace"]:
        print(f"  turn {t['turn']}: tools={t['tool_calls'] or '—'}  args={t.get('args', '')}")
    print(f"\\nANSWER: {r['answer']}")
else:
    print("skipped — no endpoint")"""),
("md", """### What the trace shows

Turn by turn: which tools were called, with what arguments, and when the model
stopped requesting them. That last event is the termination condition — not the
model saying it is finished, but the observable absence of a tool call.

This trace is the thing the telemetry lesson insists on. It cost four lines."""),
("md", """## Now a multi-hop question

Block 3 established that single-shot retrieval cannot answer these. An agent
can, because it retrieves twice — and you can watch it happen."""),
("code", """if BASE:
    r = run("Who is the site manager responsible for the site with the highest Q2 failure rate?")
    print(f"reason: {r['reason']}  turns: {r['turns']}\\n")
    for t in r["trace"]:
        print(f"  turn {t['turn']}: tools={t['tool_calls'] or '—'}  args={t.get('args', '')}")
    print(f"\\nANSWER: {r['answer']}")
    print("\\nexpected: S. Tran — Clyde had the highest rate, and S. Tran manages Clyde")
else:
    print("skipped — no endpoint")"""),
("md", """### That is the whole argument for agents

The answer needs two facts from two documents. A single retrieval embeds the
question, gets close to one of them, and misses the other — which notebook 02 of
Block 3 measured at 0.83 recall.

The loop finds the first fact, then uses it to ask a *different* question. No
better retrieval would have achieved that, because the second query did not exist
until the first result came back."""),
("md", """## The caps, demonstrated"""),
("code", """if BASE:
    r = run("Summarise every document in the corpus in detail.", max_turns=2)
    print(f"reason: {r['reason']}  turns: {r['turns']}")
    print("\\nThe run stopped because it hit the turn cap, and the caller can tell.")
    print("A loop with one exit would have returned None with no explanation —")
    print("indistinguishable from the model failing, which is the confounds lesson.")
else:
    print("skipped — no endpoint")"""),
("md", """---

## What this notebook established

- The loop is a while-statement, a tool executor and three exits
- Error messages that name the fix save turns
- Tool results are truncated because they are context
- The trace falls out of the loop for four lines of code
- Multi-hop works because the second query did not exist until the first returned

## Your turn

1. Remove the `truncate` call and run the multi-hop question. Watch the turn
   count and the context grow.
2. Change `read_doc` to return "not found" with no guidance. How many turns does
   the agent waste?
3. Add a `max_spend` cap alongside `max_turns`. Which one fires first, and on
   what kind of question?"""),
]),
]
