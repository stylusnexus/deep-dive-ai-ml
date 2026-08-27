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
("02-graph-and-checkpoints.ipynb", [
("md", """# 02 · What the Graph Runtime Actually Buys

The previous notebook wrote the loop by hand. The lesson claims a graph runtime
buys five things, and that only one of them earns the dependency:

> Checkpointing is the feature; everything else is convenience.

This notebook checks that claim rather than repeating it. Same corpus, same two
tools, same model, same multi-hop question as notebook 01 — the only thing that
changes is where the control flow lives. Then the run is crashed on purpose, and
the cost of recovering from it is counted.

Requires `langgraph`. It is the first framework dependency in this repository,
which is itself part of the lesson: the cost of the graph starts at the install."""),
("code", _SETUP),
("md", """## The same two tools

Unchanged from notebook 01, so that the comparison has exactly one variable in
it. If the graph version answers differently, the difference is the runtime."""),
("code", """import operator
from typing import TypedDict, Annotated

DOCS = {d["doc_id"]: d for d in json.loads((ROOT / "data" / "corpus" / "manifest.json").read_text())}

def search_docs(query: str) -> str:
    q = query.lower()
    hits = [d for d in DOCS.values() if q in d["text"].lower() or q in d["title"].lower()]
    if not hits:
        return f"No documents mention '{query}'. Try a broader term."
    return "\\n".join(f"{d['doc_id']}: {d['title']}" for d in hits[:6])

def read_doc(doc_id: str) -> str:
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
print(f"{len(DOCS)} documents, {len(TOOLS)} tools")"""),
("md", """## State and nodes

The state is the explicit object the previous lesson said to add early. Here it
is a typed dictionary, and `operator.add` on the messages field means a node
returns only what it wants to *append* — it never rewrites the whole history.

Two counters are threaded in as well. `MODEL_CALLS` is the measurement this
notebook exists for; `FAIL_NEXT_TOOL_CALL` is the crash, armed on demand."""),
("code", """MODEL_CALLS = {"n": 0}
FAIL_NEXT_TOOL_CALL = {"armed": False}

SYSTEM = textwrap.dedent(\"\"\"
    You answer questions about wind farm operations using the tools provided.
    Search for relevant documents, read the ones you need, then answer.
    Cite document ids in your answer. If the documents do not contain the
    answer, say NOT IN CORPUS.
\"\"\").strip()

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]      # nodes append; they never rewrite

def call_model(state):
    MODEL_CALLS["n"] += 1
    body = json.dumps({"model": MODEL, "temperature": 0, "max_tokens": 800,
                       "messages": [{"role": "system", "content": SYSTEM}] + state["messages"],
                       "tools": TOOL_SPEC}).encode()
    req = urllib.request.Request(f"{BASE}/chat/completions", data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return {"messages": [json.loads(r.read())["choices"][0]["message"]]}

def run_tools(state):
    if FAIL_NEXT_TOOL_CALL["armed"]:
        FAIL_NEXT_TOOL_CALL["armed"] = False
        raise RuntimeError("simulated crash: the tool backend went away mid-run")
    out = []
    for c in state["messages"][-1].get("tool_calls") or []:
        name = c["function"]["name"]
        args = json.loads(c["function"]["arguments"] or "{}")
        result = TOOLS[name](**args) if name in TOOLS else f"No tool named {name}."
        out.append({"role": "tool", "tool_call_id": c["id"], "content": str(result)[:3000]})
    return {"messages": out}

def needs_tool(state):
    # The same observable termination condition as the hand-written loop:
    # the absence of a tool call, not the model claiming to be finished.
    return "tools" if (state["messages"][-1].get("tool_calls") or []) else "done"

print("nodes defined")"""),
("md", """## The graph

This is the snippet from the lesson, with the node bodies filled in. Note what
it is not doing: there is no `while` statement anywhere. The loop is the edge
from `tools` back to `model`, and the exit is the conditional edge to `END`.

`MemorySaver` is the checkpointer. It ships with `langgraph` and keeps state in
this process — which is enough to demonstrate the mechanism and not enough to
survive the process dying. Durable savers (SQLite, Postgres) are separate
installs; the interface is the same."""),
("code", """from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

def build_agent():
    g = StateGraph(AgentState)
    g.add_node("model", call_model)
    g.add_node("tools", run_tools)
    g.set_entry_point("model")
    g.add_conditional_edges("model", needs_tool, {"tools": "tools", "done": END})
    g.add_edge("tools", "model")                 # the loop
    return g.compile(checkpointer=MemorySaver())

def final_answer(state):
    return re.sub(r"<think>.*?</think>", "", state["messages"][-1].get("content") or "", flags=re.S).strip()

QUESTION = "Who is the site manager responsible for the site with the highest Q2 failure rate?"
print("graph compiled with a checkpointer")"""),
("md", """## First, the clean run

The same multi-hop question notebook 01 answered with a `for` statement. A
`thread_id` names the run; the checkpointer keys its state on it."""),
("code", """if BASE:
    agent = build_agent()
    MODEL_CALLS["n"] = 0
    clean_cfg = {"configurable": {"thread_id": "clean-run"}}
    out = agent.invoke({"messages": [{"role": "user", "content": QUESTION}]}, clean_cfg)
    CLEAN_CALLS = MODEL_CALLS["n"]
    print(f"model calls: {CLEAN_CALLS}")
    print(f"ANSWER: {final_answer(out)}")
    print("\\nexpected: S. Tran — Clyde had the highest rate, and S. Tran manages Clyde")
else:
    print("skipped — no endpoint")"""),
("md", """### So far the graph has bought nothing

Same answer, same tools, same model, more concepts and a new dependency. If the
notebook stopped here the honest conclusion would be that the hand-written loop
was better, and the lesson says exactly that about agents which never pause and
never fail.

Everything the framework is worth is in the next cell."""),
("md", """## The claim under test

Arm the crash and run the same question on a fresh thread. The tool node will
raise part-way through — after the model has already been called and paid for.

Three numbers matter: how many model calls happened before the crash, how many
the resumed run costs in total, and what a restart from scratch would have
cost instead."""),
("code", """if BASE:
    agent = build_agent()
    MODEL_CALLS["n"] = 0
    FAIL_NEXT_TOOL_CALL["armed"] = True
    cfg = {"configurable": {"thread_id": "crashed-run"}}

    try:
        agent.invoke({"messages": [{"role": "user", "content": QUESTION}]}, cfg)
    except RuntimeError as ex:
        print(f"crashed: {ex}")

    before = MODEL_CALLS["n"]
    snap = agent.get_state(cfg)
    print(f"\\nmodel calls before the crash : {before}")
    print(f"messages persisted           : {len(snap.values['messages'])}")
    print(f"next node to run             : {snap.next}")

    # Resuming means invoking with None: no new input, continue from the checkpoint.
    out = agent.invoke(None, cfg)
    total = MODEL_CALLS["n"]

    print(f"\\nmodel calls, crash + resume  : {total}")
    print(f"model calls, clean run       : {CLEAN_CALLS}")
    print(f"a restart would have cost    : {before + CLEAN_CALLS}")
    print(f"\\nrecovering cost {total - CLEAN_CALLS} extra model call(s).")
    print(f"ANSWER: {final_answer(out)}")
else:
    print("skipped — no endpoint")"""),
("md", """### What that measured

The crash happened *after* the model had been called. The checkpointer had
already written the state, so `next` still pointed at the node that failed — the
run knew where it was, not merely that it had died.

Resuming cost no extra model calls at all: the crashed-then-resumed run made the
same number as the clean run, while restarting from the top would have paid for
the pre-crash call a second time. On this corpus that is one wasted call out of
five. On the lesson's three-hour run that crashes at hour two, it is two hours.

Note what did *not* have to exist for this to work: no retry decorator, no
manual state serialisation, no resume logic in the loop. That is the whole of
the argument for the dependency."""),
("md", """## Inspectability, which comes free

The checkpointer wrote a record at every step, so the finished run can be walked
backwards. This is the trajectory log the telemetry lesson asks for, produced by
construction rather than by remembering to log."""),
("code", """if BASE:
    history = list(agent.get_state_history(cfg))
    print(f"{len(history)} checkpoints recorded for this run\\n")
    for h in reversed(history[:6]):
        last = h.values["messages"][-1] if h.values.get("messages") else {}
        kind = last.get("role") or ("assistant" if last.get("tool_calls") else "—")
        print(f"  next={str(h.next):22s} messages={len(h.values.get('messages', [])):2d}  last role={kind}")
else:
    print("skipped — no endpoint")"""),
("md", """## The cost, stated honestly

- The stack trace now runs through framework code. The crash above was raised in
  a node and surfaced through the runtime, not from a line you wrote.
- `langgraph` is a version surface. The application programming interface has
  moved before and will again; this notebook was checked against a 1.x release
  and may need editing on a future one.
- Two nodes and one conditional edge is more machinery than a `for` statement.
  For an agent that runs for seconds and never pauses, notebook 01 is the better
  implementation and this one is ceremony."""),
("md", """---

## What this notebook established

- The graph produces the same answer as the hand-written loop — the runtime is
  not what makes the agent work
- Checkpointed state means a crash resumes from where it stopped, at no extra
  model calls, where a restart pays for the completed work twice
- `next` after a failure tells you which node died, not merely that the run did
- The state history is a trajectory log nobody had to write
- Everything else the framework offers is reachable without it

## Your turn

1. Move the crash into `call_model` instead of `run_tools`. Does resumption
   still cost nothing, and why is the answer different?
2. Swap `MemorySaver` for a durable saver and kill the kernel between the crash
   and the resume. This is the version of the demonstration that matters in
   production.
3. Add a third node that summarises the messages when the history grows past a
   threshold. Which of the five things the lesson listed did you just use?"""),
]),
]
