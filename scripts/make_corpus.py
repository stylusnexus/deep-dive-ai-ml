#!/usr/bin/env python3
"""A small technical corpus with known ground truth.

Synthetic on purpose: it lets the evaluation labels be genuinely correct rather
than hand-waved, and it plants multi-hop chains so the agentic-RAG lesson has
questions that single-shot retrieval provably cannot answer.

Emits documents plus an eval set naming the exact document that answers each
question — which is what makes recall@k measurable rather than estimated.
"""
import json, pathlib, textwrap

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "corpus"
OUT.mkdir(parents=True, exist_ok=True)

SITES = {
    "Ardrossan":      dict(code="ARD", turbines=42, region="North West", manager="J. Okafor"),
    "Whitelee":       dict(code="WHL", turbines=68, region="Central",    manager="M. Lindqvist"),
    "Clyde":          dict(code="CLY", turbines=51, region="South",      manager="S. Tran"),
    "Beinn an Tuirc": dict(code="BAT", turbines=29, region="West",       manager="R. Achebe"),
}

# Planted facts. Each lives in exactly one document, so gold labels are exact.
DOCS = []

def add(doc_id, title, kind, body):
    DOCS.append({"doc_id": doc_id, "title": title, "kind": kind,
                 "text": textwrap.dedent(body).strip()})

for name, m in SITES.items():
    add(f"site-{m['code'].lower()}", f"{name} Site Profile", "site", f"""
        # {name} Site Profile

        Site code: {m['code']}. Region: {m['region']}.
        Operational turbines: {m['turbines']}.
        Site manager: {m['manager']}.

        ## Operating envelope

        Turbines at {name} operate under the standard envelope defined in
        OPS-STD-04 unless a site variance is recorded. Gearbox temperature is
        logged every fifteen minutes and reported daily to the regional desk.

        ## Escalation

        Faults are escalated to the {m['region']} regional desk. Out of hours,
        escalation passes to the national control room.
        """)

add("ops-std-04", "OPS-STD-04 Operating Envelope", "standard", """
    # OPS-STD-04 — Standard Operating Envelope

    ## Gearbox temperature

    The gearbox oil temperature must not exceed 82 degrees Celsius during
    continuous operation. Between 82 and 90 degrees the turbine enters
    derated operation automatically. Above 90 degrees the turbine performs a
    controlled shutdown.

    ## Vibration

    Nacelle vibration above 0.55 mm/s RMS sustained for more than thirty
    minutes triggers a Level 2 alert. Above 0.80 mm/s the turbine shuts down
    immediately and requires physical inspection before restart.

    ## Rotor speed

    Rated rotor speed is 14.6 rpm. The overspeed trip is set at 17.2 rpm.
    """)

add("maint-pol-11", "MAINT-POL-11 Inspection Intervals", "policy", """
    # MAINT-POL-11 — Scheduled Inspection Intervals

    ## Routine inspection

    Every turbine receives a routine inspection every 180 days. The interval
    reduces to 90 days for any turbine older than twelve years.

    ## Post-alert inspection

    A Level 2 vibration alert requires inspection within 14 days. A Level 3
    alert requires inspection before the turbine is returned to service.

    ## Deferral

    A routine inspection may be deferred once, by no more than 30 days, with
    written approval from the site manager. A post-alert inspection may not
    be deferred under any circumstances.
    """)

add("inc-2026-014", "Incident Report 2026-014", "incident", """
    # Incident Report 2026-014

    Date: 14 March 2026. Site: Whitelee. Turbine: WHL-031.

    ## Summary

    Turbine WHL-031 performed a controlled shutdown after gearbox oil
    temperature reached 91.4 degrees Celsius. The turbine had been in derated
    operation for approximately six hours prior to shutdown.

    ## Root cause

    A partially blocked oil cooler restricted flow. The blockage was traced to
    debris ingress following a filter change on 2 March 2026 where the
    replacement filter seal was incorrectly seated.

    ## Corrective action

    Filter seating is now verified by a second engineer on every change. The
    verification requirement was added to MAINT-POL-11 as an appendix.
    """)

add("inc-2026-021", "Incident Report 2026-021", "incident", """
    # Incident Report 2026-021

    Date: 2 June 2026. Site: Clyde. Turbine: CLY-008.

    ## Summary

    Nacelle vibration on CLY-008 exceeded 0.80 mm/s RMS, triggering an
    immediate shutdown. Vibration had been rising steadily for eleven days
    prior, crossing the Level 2 threshold on 22 May.

    ## Root cause

    Blade root bolt tension had relaxed below specification on two of three
    blades. The preceding routine inspection had been deferred by 28 days
    under the single-deferral provision.

    ## Corrective action

    Deferral is no longer permitted for turbines with an open Level 2 alert.
    """)

add("perf-2026-q2", "Fleet Performance Summary Q2 2026", "report", """
    # Fleet Performance Summary — Q2 2026

    ## Availability

    Fleet availability averaged 94.2 percent. Whitelee recorded the highest
    availability at 96.1 percent. Beinn an Tuirc recorded the lowest at
    91.3 percent, attributed to two extended outages.

    ## Failure rate

    The fleet failure rate for the quarter was 3.1 failures per hundred
    turbines. Clyde recorded the highest site failure rate at 5.9 per hundred
    turbines. Ardrossan recorded 2.4 and Whitelee 2.1.

    ## Generation

    Total generation was 412 GWh, three percent above the quarterly forecast.
    """)

add("proc-restart-07", "PROC-RESTART-07 Return to Service", "procedure", """
    # PROC-RESTART-07 — Return to Service After Shutdown

    ## Applicability

    This procedure applies after any automatic shutdown, including overspeed,
    vibration and thermal shutdowns.

    ## Sequence

    1. Confirm the originating fault has been cleared and logged.
    2. Complete the inspection required by MAINT-POL-11 for the alert level.
    3. Obtain written release from the site manager.
    4. Restart under supervision and monitor for two hours at reduced output.

    ## Restriction

    A turbine that has shut down twice within 30 days may not be returned to
    service without regional engineering approval.
    """)

for d in DOCS:
    (OUT / f"{d['doc_id']}.md").write_text(d["text"] + "\n")
(OUT / "manifest.json").write_text(json.dumps(DOCS, indent=2) + "\n")

# --- evaluation set. gold_docs is exact because the facts were planted.
EVAL = [
 dict(qid="q01", question="What is the maximum gearbox oil temperature during continuous operation?",
      gold_docs=["ops-std-04"], hops=1,
      answer="82 degrees Celsius."),
 dict(qid="q02", question="How often must a turbine older than twelve years be inspected?",
      gold_docs=["maint-pol-11"], hops=1,
      answer="Every 90 days."),
 dict(qid="q03", question="What caused the shutdown of turbine WHL-031?",
      gold_docs=["inc-2026-014"], hops=1,
      answer="A partially blocked oil cooler, caused by an incorrectly seated filter seal."),
 dict(qid="q04", question="Which site had the highest failure rate in Q2 2026?",
      gold_docs=["perf-2026-q2"], hops=1,
      answer="Clyde, at 5.9 failures per hundred turbines."),
 dict(qid="q05", question="Who is the site manager responsible for the site with the highest Q2 failure rate?",
      gold_docs=["perf-2026-q2", "site-cly"], hops=2,
      answer="S. Tran — Clyde had the highest failure rate and S. Tran manages Clyde."),
 dict(qid="q06", question="Was the inspection deferral before incident 2026-021 permitted under policy at the time?",
      gold_docs=["inc-2026-021", "maint-pol-11"], hops=2,
      answer="Yes — a single deferral of up to 30 days was permitted, and 28 days was used."),
 dict(qid="q07", question="What vibration level triggers immediate shutdown, and how soon must inspection follow?",
      gold_docs=["ops-std-04", "maint-pol-11"], hops=2,
      answer="0.80 mm/s RMS triggers immediate shutdown; a Level 3 alert requires inspection before return to service."),
 dict(qid="q08", question="How many operational turbines are there at Whitelee?",
      gold_docs=["site-whl"], hops=1, answer="68."),
 dict(qid="q09", question="What approval is needed to return a turbine to service after two shutdowns in 30 days?",
      gold_docs=["proc-restart-07"], hops=1,
      answer="Regional engineering approval."),
 dict(qid="q10", question="What is the average lifespan of a gearbox bearing?",
      gold_docs=[], hops=0,
      answer="NOT IN CORPUS — the system should refuse rather than answer."),
]
(ROOT / "data" / "corpus_eval.json").write_text(json.dumps(EVAL, indent=2) + "\n")

print(f"wrote {len(DOCS)} documents to {OUT.relative_to(ROOT)}")
print(f"wrote {len(EVAL)} eval questions to data/corpus_eval.json")
print(f"  single-hop : {sum(1 for e in EVAL if e['hops']==1)}")
print(f"  multi-hop  : {sum(1 for e in EVAL if e['hops']==2)}  <- single-shot retrieval cannot answer these")
print(f"  unanswerable: {sum(1 for e in EVAL if e['hops']==0)}  <- the system should refuse")
