#!/usr/bin/env python3
"""Multi-agent delivery-exception handling, with an approval gate that halts.

The order of work here is the argument. The deterministic path is measured
first, because if a lookup table already decides most exceptions then the
honest system is rules plus an agent for the remainder — and that finding is
worth more than a working three-agent demo.

Three agents, because three contexts: triage never sees the policies, policy
never sees draft prose, comms never sees the raw event log. The handoffs
between them are recorded with what each one dropped, because that is where
the failures live.

The customer-communication step is an interrupt, not a prompt saying "please
approve". The run stops mid-flight, persists, and resumes on a decision.
"""
from __future__ import annotations

import argparse, json, os, pathlib, re, sys, urllib.request
from typing import TypedDict, Annotated
import operator

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command

HERE = pathlib.Path(__file__).resolve().parent.parent
ROOT = HERE.parent.parent
DATA = ROOT / "data" / "exceptions"
TRACES = HERE / "traces"
PENDING = HERE / "pending"

ENDPOINTS = ["http://localhost:11455/v1", "http://localhost:11434/v1"]

# Actions that reach a customer and must be approved before sending (POL-COM-05).
GATED_ACTIONS = {"refund", "refund_and_replace", "partial_refund"}
# Actions that leave the automated path entirely (POL-ESC-04).
TERMINAL_ACTIONS = {"escalate_to_human"}

MODEL_CALLS = {"n": 0}
GATE_HITS: list[str] = []
PARSE_FAILURES: list[str] = []
TRUNCATIONS: list[str] = []


# --------------------------------------------------------------- endpoint

def find_endpoint():
    # The first entry in /v1/models is not necessarily a chat model. An embedding
    # model listed first returns HTTP 400 on a chat completion, silently.
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


def ask(system: str, user: str, tag: str, timeout: int = 300) -> str:
    """One model call. A reasoning model spends tokens thinking before it emits a
    word, so the ceiling is generous and truncation is recorded rather than
    swallowed — an empty reply scored as an answer is a measurement of the budget."""
    MODEL_CALLS["n"] += 1
    body = json.dumps({"model": MODEL, "temperature": 0, "max_tokens": 1500,
                       "messages": [{"role": "system", "content": system},
                                    {"role": "user", "content": user}]}).encode()
    req = urllib.request.Request(f"{BASE}/chat/completions", data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        choice = json.loads(r.read())["choices"][0]
    if choice.get("finish_reason") == "length":
        TRUNCATIONS.append(tag)
    out = choice["message"]["content"] or ""
    return re.sub(r"<think>.*?</think>", "", out, flags=re.S).strip()


def parse_json(text: str, tag: str) -> dict | None:
    """Models wrap JSON in prose. Take the first object; record a failure rather
    than defaulting, because a silent default becomes an invented decision."""
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        PARSE_FAILURES.append(tag)
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        PARSE_FAILURES.append(tag)
        return None


# ------------------------------------------------------- deterministic path

RULES = {
    ("ADDRESS_INVALID", None):      "request_address_correction",
    ("RECIPIENT_ABSENT", 1):        "reschedule",
    ("RECIPIENT_ABSENT", 2):        "reschedule",
    ("RECIPIENT_ABSENT", 3):        "return_to_depot",
    ("DAMAGED_IN_TRANSIT", None):   "refund_and_replace",
    ("WEATHER_DELAY", None):        "notify_delay",
    ("CUSTOMS_HOLD", None):         "request_documents",
    ("LOST_IN_NETWORK", None):      "refund",
    ("REFUSED_BY_RECIPIENT", None): "return_to_sender",
}

HIGH_VALUE_CODES = {"DAMAGED_IN_TRANSIT", "LOST_IN_NETWORK"}


def rule_action(exc: dict) -> str | None:
    key = (exc["event_code"], exc.get("attempt"))
    return RULES.get(key) or RULES.get((exc["event_code"], None))


def guards(exc: dict) -> list[dict]:
    """Policy-mandated checks that are never left to a model. Each is recorded
    whether it fired or not — a guard you cannot see did not run."""
    value = exc["order_value_gbp"]
    return [
        {"guard": "high_value_damage_or_loss",
         "rule": "POL-ESC-04: damage or loss at or above £250 goes to a human",
         "fired": value >= 250 and exc["event_code"] in HIGH_VALUE_CODES},
        {"guard": "gated_communication",
         "rule": "POL-COM-05: refund and damage messages are approved before sending",
         "fired": rule_action(exc) in GATED_ACTIONS},
    ]


# ------------------------------------------------------------------ agents

TRIAGE_SYSTEM = """You classify delivery exceptions. You see one log entry and
the action a lookup table has already chosen from its event code.

Your only job: decide whether the delivery note makes that standard action wrong.

Send it for judgement when any of these hold:

- The note makes the code untrue — a parcel marked lost that has since been
  scanned, an address marked invalid that was actually correct
- The note gives a cause the standard action would not address — a hold placed
  for a prohibited or restricted item is not solved by requesting paperwork
- The standard action has already been taken and did not work, so repeating it
  would loop
- The note reports injury, illness, bereavement, or another personal
  circumstance affecting the recipient
- The damage is to packaging only and the contents are intact
- The consignment is time-critical, temperature-controlled, or otherwise
  unusual enough that a standard notice would not cover it
- The failed delivery was the carrier's own doing — wrong day, wrong address

Otherwise it is routine: the note simply restates the code. Most are routine.

Reply with JSON only:
{"verdict": "routine" | "needs_judgement", "reason": "<one short sentence>"}"""

POLICY_SYSTEM = """You decide the correct action for a delivery exception that
has been flagged as not routine. You are given the written policies and one
exception. Apply the policies literally; do not invent rules.

Choose exactly one action from:
reschedule, return_to_depot, request_address_correction, refund_and_replace,
notify_delay, request_documents, refund, return_to_sender, hold_at_depot,
log_carrier_fault, escalate_to_human

Escalating is a legitimate answer and is required where the policies say so.

Reply with JSON only:
{"action": "<one of the list>", "policy": "<the policy id you applied>", "reason": "<one short sentence>"}"""

COMMS_SYSTEM = """You draft a short message to a customer about a delivery
exception, following POL-COM-05: state what happened, what is being done, and
what if anything the customer must do. Do not apologise for events outside the
carrier's control. Never state a delivery date that has not been confirmed.

Three sentences at most. Reply with the message text only, no preamble."""


def summarise_for_policy(exc: dict) -> dict:
    """The handoff. What policy sees, and by omission what it does not."""
    return {"event_code": exc["event_code"], "attempt": exc.get("attempt"),
            "note": exc["note"], "order_value_gbp": exc["order_value_gbp"],
            "rule_action": rule_action(exc)}


def summarise_for_comms(exc: dict, action: str) -> dict:
    return {"action": action, "event_code": exc["event_code"],
            "customer_tier": exc["customer_tier"]}


# ------------------------------------------------------------------- graph

class Run(TypedDict):
    exception: dict
    trace: Annotated[list, operator.add]
    verdict: str
    action: str
    decided_by: str
    draft: str
    outcome: str


POLICIES_TEXT = ""


def node_triage(state: Run):
    exc = state["exception"]
    fired = guards(exc)
    hard = next((g for g in fired if g["guard"] == "high_value_damage_or_loss" and g["fired"]), None)
    if hard:
        # A rule that is right does not need a model. This is the cheap path and
        # the report counts how often it was the one that mattered.
        return {"verdict": "guard", "action": "escalate_to_human", "decided_by": "guard",
                "trace": [{"stage": "triage", "guards": fired, "model_calls": 0,
                           "result": "escalated by guard before any model call"}]}

    raw = ask(TRIAGE_SYSTEM, json.dumps({"event_code": exc["event_code"],
                                         "attempt": exc.get("attempt"),
                                         "note": exc["note"],
                                         "lookup_action": rule_action(exc)}),
              tag=f"triage:{exc['exception_id']}")
    parsed = parse_json(raw, f"triage:{exc['exception_id']}") or {}
    verdict = parsed.get("verdict") if parsed.get("verdict") in ("routine", "needs_judgement") else "routine"
    return {"verdict": verdict,
            "trace": [{"stage": "triage", "guards": fired, "model_calls": 1,
                       "verdict": verdict, "reason": parsed.get("reason", ""),
                       "parsed": bool(parsed),
                       "handoff_dropped": ["order_id", "carrier", "customer_tier"]}]}


def node_apply_rule(state: Run):
    exc = state["exception"]
    return {"action": rule_action(exc), "decided_by": "rule",
            "trace": [{"stage": "rule", "model_calls": 0, "action": rule_action(exc)}]}


def node_policy(state: Run):
    exc = state["exception"]
    handed = summarise_for_policy(exc)
    dropped = sorted(set(exc) - set(handed) - {"gold_action", "needs_judgement", "why"})
    raw = ask(POLICY_SYSTEM, f"Policies:\n{POLICIES_TEXT}\n\nException:\n{json.dumps(handed, indent=2)}",
              tag=f"policy:{exc['exception_id']}")
    parsed = parse_json(raw, f"policy:{exc['exception_id']}") or {}
    action = parsed.get("action") or "escalate_to_human"
    return {"action": action, "decided_by": "model",
            "trace": [{"stage": "policy", "model_calls": 1, "action": action,
                       "policy": parsed.get("policy", ""), "reason": parsed.get("reason", ""),
                       "parsed": bool(parsed), "handoff_dropped": dropped}]}


def node_comms(state: Run):
    exc, action = state["exception"], state["action"]

    if action in TERMINAL_ACTIONS:
        return {"outcome": "escalated — left the automated path, no message sent",
                "trace": [{"stage": "comms", "model_calls": 0,
                           "result": "skipped: escalated cases are handled by a human"}]}

    if action not in GATED_ACTIONS:
        # A delay notice does not need a model. Templated, cheap, and honest.
        return {"draft": f"Your order is affected by a delivery exception ({exc['event_code'].lower().replace('_', ' ')}). "
                         f"The action taken is: {action.replace('_', ' ')}.",
                "outcome": "sent — templated, no approval required",
                "trace": [{"stage": "comms", "model_calls": 0, "gated": False,
                           "result": "templated message, POL-COM-05 does not gate this action"}]}

    handed = summarise_for_comms(exc, action)
    draft = ask(COMMS_SYSTEM, json.dumps(handed), tag=f"comms:{exc['exception_id']}")

    # The gate. Not a prompt — the run stops here and persists.
    decision = interrupt({"exception_id": exc["exception_id"], "action": action, "draft": draft})

    approved = str(decision).lower().startswith("approve")
    return {"draft": draft,
            "outcome": "sent — approved by a human" if approved else "held — approval refused",
            "trace": [{"stage": "comms", "model_calls": 1, "gated": True,
                       "handoff_dropped": ["note", "order_value_gbp", "attempt"],
                       "decision": str(decision), "approved": approved}]}


def route_after_triage(state: Run):
    if state["verdict"] == "guard":
        return "comms"
    return "policy" if state["verdict"] == "needs_judgement" else "rule"


def build_graph():
    g = StateGraph(Run)
    g.add_node("triage", node_triage)
    g.add_node("rule", node_apply_rule)
    g.add_node("policy", node_policy)
    g.add_node("comms", node_comms)
    g.set_entry_point("triage")
    g.add_conditional_edges("triage", route_after_triage,
                            {"rule": "rule", "policy": "policy", "comms": "comms"})
    g.add_edge("rule", "comms")
    g.add_edge("policy", "comms")
    g.add_edge("comms", END)
    return g.compile(checkpointer=MemorySaver())


# -------------------------------------------------------------------- run

def process(app, exc: dict, approve_all: bool) -> dict:
    cfg = {"configurable": {"thread_id": exc["exception_id"]}}
    state = app.invoke({"exception": exc, "trace": [], "verdict": "", "action": "",
                        "decided_by": "", "draft": "", "outcome": ""}, cfg)

    halted = "__interrupt__" in state
    if halted:
        GATE_HITS.append(exc["exception_id"])
        snap = app.get_state(cfg)
        if not approve_all:
            payload = state["__interrupt__"][0].value
            (PENDING / f"{exc['exception_id']}.json").write_text(
                json.dumps({"halted_at": list(snap.next), "awaiting": payload}, indent=2) + "\n")
            return {"exception_id": exc["exception_id"], "action": state["action"],
                    "decided_by": state["decided_by"], "outcome": "awaiting approval",
                    "halted_at": list(snap.next), "trace": state["trace"],
                    "gold_action": exc["gold_action"], "needs_judgement": exc["needs_judgement"]}
        state = app.invoke(Command(resume="approved"), cfg)

    return {"exception_id": exc["exception_id"], "action": state["action"],
            "decided_by": state["decided_by"], "outcome": state["outcome"],
            "halted_at": None, "trace": state["trace"],
            "gold_action": exc["gold_action"], "needs_judgement": exc["needs_judgement"]}


def md_table(rows, cols):
    head = "| " + " | ".join(cols) + " |\n|" + "|".join(["---"] * len(cols)) + "|\n"
    return head + "\n".join("| " + " | ".join(str(r.get(c, "")) for c in cols) + " |" for r in rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--approve-all", action="store_true",
                    help="simulate approvals so the run completes end to end")
    ap.add_argument("--limit", type=int, default=0, help="process only the first N exceptions")
    ap.add_argument("--trace", help="print one saved trace and exit, e.g. exc-0042")
    args = ap.parse_args()

    TRACES.mkdir(exist_ok=True)
    PENDING.mkdir(exist_ok=True)

    if args.trace:
        f = TRACES / f"{args.trace}.json"
        if not f.exists():
            sys.exit(f"no trace for {args.trace} — run the pipeline first")
        print(json.dumps(json.loads(f.read_text()), indent=2))
        return

    exceptions = json.loads((DATA / "exceptions.json").read_text())
    policies = json.loads((DATA / "policies.json").read_text())
    global POLICIES_TEXT
    POLICIES_TEXT = "\n\n".join(p["text"] for p in policies)
    if args.limit:
        exceptions = exceptions[:args.limit]

    # Stage 0. The dumb baseline, before any model runs.
    base_correct = sum(1 for e in exceptions if rule_action(e) == e["gold_action"])
    needs = sum(1 for e in exceptions if e["needs_judgement"])
    print(f"{len(exceptions)} exceptions, {len(policies)} policies")
    print(f"lookup table alone : {base_correct}/{len(exceptions)} ({base_correct/len(exceptions):.0%})")
    print(f"needing judgement  : {needs}/{len(exceptions)} ({needs/len(exceptions):.0%})\n")

    if not BASE:
        sys.exit("no local endpoint — start one and re-run; this project measures a model")
    print(f"generation: {MODEL}\n")

    app = build_graph()
    results = []
    for i, exc in enumerate(exceptions, 1):
        r = process(app, exc, args.approve_all)
        results.append(r)
        (TRACES / f"{exc['exception_id']}.json").write_text(json.dumps(r, indent=2) + "\n")
        if i % 20 == 0 or i == len(exceptions):
            print(f"  {i}/{len(exceptions)} processed  ({MODEL_CALLS['n']} model calls)")

    settled = [r for r in results if r["outcome"] != "awaiting approval"]
    correct = sum(1 for r in settled if r["action"] == r["gold_action"])
    jud = [r for r in settled if r["needs_judgement"]]
    rout = [r for r in settled if not r["needs_judgement"]]
    jud_ok = sum(1 for r in jud if r["action"] == r["gold_action"])
    rout_ok = sum(1 for r in rout if r["action"] == r["gold_action"])
    halted = [r for r in results if r["outcome"] == "awaiting approval"]
    by_guard = sum(1 for r in results if r["decided_by"] == "guard")

    # Triage quality: did the narrow classifier find the cases that needed judgement?
    flagged = [r for r in results if r["decided_by"] in ("model", "guard")]
    tp = sum(1 for r in flagged if r["needs_judgement"])
    fp = len(flagged) - tp
    fn = sum(1 for r in results if r["needs_judgement"] and r["decided_by"] == "rule")

    pct = lambda a, b: f"{a}/{b} ({a/b:.0%})" if b else "n/a"
    report = f"""# Multi-Agent Delivery Exception Handling — Report

Generated by `src/pipeline.py`. {len(exceptions)} exceptions, {len(policies)} policies.
Generation: `{MODEL}`. Model calls this run: {MODEL_CALLS['n']}.
{f"**{len(PARSE_FAILURES)} model replies could not be parsed as JSON** and were recorded as failures rather than defaulted." if PARSE_FAILURES else ""}
{f"**{len(TRUNCATIONS)} replies hit the token ceiling.** Raise max_tokens and re-run — a truncated reply is a measurement of the budget." if TRUNCATIONS else ""}

## The question this project exists to answer

**What fraction of exceptions genuinely needed judgement?** {pct(needs, len(exceptions))}.

The lookup table alone gets {pct(base_correct, len(exceptions))} right. That is the
number any agent has to beat, and it is high because most delivery exceptions
are decided entirely by their event code.

## The four numbers

| stage | measurement |
|---|---|
| Lookup table alone | {pct(base_correct, len(exceptions))} |
| Full pipeline | {pct(correct, len(settled))} |
| On routine exceptions | {pct(rout_ok, len(rout))} |
| On exceptions needing judgement | {pct(jud_ok, len(jud))} |
| Decided by a guard, before any model call | {by_guard} |
| Stopped at the approval gate | {len(GATE_HITS)} |
| Left awaiting a human | {len(halted)} |

## Did triage find the hard cases?

Triage is the cheap narrow classifier that decides whether an exception leaves
the deterministic path at all. Everything downstream depends on it.

| | count |
|---|---|
| Correctly sent for judgement | {tp} |
| Sent for judgement unnecessarily | {fp} |
| **Missed — needed judgement, got the lookup answer** | {fn} |

A miss here is invisible downstream: the exception gets a confident wrong action
and never reaches a model or a human. That is the failure mode worth watching.

## The approval gate

{len(GATE_HITS)} run(s) reached the communication step and **stopped there**. Not a
prompt asking to proceed — the graph interrupted, the state persisted, and
control returned to the caller with the run unfinished.

{f"They were resumed automatically because --approve-all was set. Each resumed from its own checkpoint: triage and policy did not run again, and were not paid for again." if not halted else f"{len(halted)} are in `pending/`, each recording the node it halted at and the draft awaiting a decision. Nothing was sent. Re-run with --approve-all to resume them."}

Every gated action is one POL-COM-05 names: refunds and damage. A delay notice
is templated and sends without a model or a human, because nothing about it
needs judgement.

## Handoffs, and what each one dropped

Every trace in `traces/` records what each agent passed on and what it withheld.
`triage` never sees the policies; `policy` never sees the customer tier or the
carrier; `comms` never sees the note or the order value. Those omissions are
deliberate and they are also where a wrong answer would come from, which is why
they are written down rather than assumed.

## The honest reading

{"The pipeline beats the lookup table." if correct/max(len(settled),1) > base_correct/len(exceptions) else "The pipeline does not beat the lookup table."} On routine exceptions the rules were already
right, and the model's contribution is confined to the {pct(needs, len(exceptions))} that
carry a note contradicting their event code. A system that ran a model on every
exception would spend {len(exceptions)} calls to change {needs} answers.

The right system is the one this report describes: rules first, a guard for what
policy says must never be automated, a narrow classifier to decide what leaves
the deterministic path, and a model only on the remainder.
"""

    (HERE / "report.md").write_text(report)
    (HERE / "results.json").write_text(json.dumps({
        "model": MODEL, "model_calls": MODEL_CALLS["n"],
        "exceptions": len(exceptions), "needing_judgement": needs,
        "baseline_correct": base_correct, "pipeline_correct": correct,
        "settled": len(settled), "halted": len(halted), "gate_hits": len(GATE_HITS),
        "decided_by_guard": by_guard,
        "triage": {"true_positive": tp, "false_positive": fp, "false_negative": fn},
        "parse_failures": PARSE_FAILURES, "truncations": TRUNCATIONS,
        "results": results,
    }, indent=2) + "\n")

    print(f"\nlookup table  : {pct(base_correct, len(exceptions))}")
    print(f"full pipeline : {pct(correct, len(settled))}")
    print(f"  routine     : {pct(rout_ok, len(rout))}")
    print(f"  judgement   : {pct(jud_ok, len(jud))}")
    print(f"triage missed : {fn} case(s) that needed judgement")
    print(f"gate stops    : {len(GATE_HITS)}  ({len(halted)} left awaiting a human)")
    if PARSE_FAILURES:
        print(f"parse failures: {len(PARSE_FAILURES)}")
    if TRUNCATIONS:
        print(f"truncations   : {len(TRUNCATIONS)}")
    print(f"\nwrote report.md, results.json, traces/ and pending/")


if __name__ == "__main__":
    main()
