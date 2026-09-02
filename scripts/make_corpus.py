#!/usr/bin/env python3
"""A technical corpus with known ground truth, at a realistic document length.

Synthetic on purpose: it lets the evaluation labels be genuinely correct rather
than hand-waved, and it plants multi-hop chains so the agentic-RAG lesson has
questions that single-shot retrieval provably cannot answer.

Sized on purpose too. The first version of this corpus ran to 827 words, which
made every retrieved context about a hundred tokens — too short for prefill to
be a measurable part of a request, so Project 2 could report which stage was
expensive and never demonstrate why. Sections here are written close to the
chunker's 900-character split so each becomes one substantial chunk.

Every planted fact lives in exactly one document. The assertion at the bottom
enforces that, because gold labels are only correct by construction if the
construction is actually checked.
"""
import json, pathlib, re, textwrap

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "corpus"
OUT.mkdir(parents=True, exist_ok=True)

SITES = {
    "Ardrossan":      dict(code="ARD", turbines=42, region="North West", manager="J. Okafor",
                           commissioned=2014, model="V112-3.0", hub=84,
                           terrain="coastal, exposed to west-southwest prevailing wind"),
    "Whitelee":       dict(code="WHL", turbines=68, region="Central", manager="M. Lindqvist",
                           commissioned=2011, model="V90-2.0", hub=80,
                           terrain="upland moorland, peat substrate"),
    "Clyde":          dict(code="CLY", turbines=51, region="South", manager="S. Tran",
                           commissioned=2016, model="V117-3.6", hub=91,
                           terrain="ridge line, high shear across the rotor disc"),
    "Beinn an Tuirc": dict(code="BAT", turbines=29, region="West", manager="R. Achebe",
                           commissioned=2009, model="V80-1.8", hub=67,
                           terrain="steep-sided glen, frequent turbulent inflow"),
}

DOCS = []

def add(doc_id, title, kind, body):
    DOCS.append({"doc_id": doc_id, "title": title, "kind": kind,
                 "text": textwrap.dedent(body).strip()})

# ---------------------------------------------------------------- site profiles
# Site profiles carry site-specific facts only. Operating limits live in
# OPS-STD-04 and are referenced here, never restated, so each number has one home.

for name, m in SITES.items():
    add(f"site-{m['code'].lower()}", f"{name} Site Profile", "site", f"""
        # {name} Site Profile

        Site code: {m['code']}. Region: {m['region']}.
        Operational turbines: {m['turbines']}.
        Site manager: {m['manager']}.
        Commissioned: {m['commissioned']}. Turbine model: {m['model']}.
        Hub height: {m['hub']} metres.

        ## Site character

        The site sits on {m['terrain']}. Inflow conditions at {name} are
        characterised in the site suitability assessment held by the regional
        engineering desk, and the turbine model was selected against that
        assessment rather than against a fleet standard. Where the assessment
        and a fleet default disagree, the assessment governs and the difference
        is recorded as a site variance with an expiry date attached. Variances
        that reach expiry without renewal revert automatically to the fleet
        default, which has caused confusion during handovers and is the reason
        the variance register is reviewed at every quarterly site meeting.

        ## Operating envelope

        Turbines at {name} operate under the standard envelope defined in
        OPS-STD-04 unless a site variance is recorded against a specific
        parameter. This profile does not restate those limits; the standard is
        the single authority for them and local copies are not maintained,
        because a local copy that drifts from the standard is worse than no
        local copy at all. Gearbox temperature is logged every fifteen minutes
        and reported daily to the regional desk. Vibration is logged
        continuously and summarised hourly. Where a logger fails, the affected
        turbine is treated as operating outside monitored conditions until the
        logger is restored, which is a deliberately conservative reading of
        the standard and is not a fault state in its own right.

        ## Escalation and out-of-hours cover

        Faults at {name} escalate to the {m['region']} regional desk during
        working hours. Out of hours, escalation passes to the national control
        room, which holds authority to shut down but not to return to service.
        That asymmetry is intentional: stopping a turbine is reversible and
        starting one is not, so the out-of-hours role is deliberately limited
        to the reversible half. Any overnight shutdown is reviewed by the site
        manager the following working morning before any restart sequence
        begins, regardless of how routine the originating fault appears.

        ## Reporting

        The site reports availability, generation and fault counts to the
        regional desk weekly, and to the fleet performance summary quarterly.
        Site-level failure rates are calculated per hundred turbines so that
        sites of different sizes can be compared directly; comparing absolute
        fault counts across sites of different sizes is a recurring error in
        internal reporting and the per-hundred convention exists to prevent it.
        Availability is reported net of scheduled maintenance windows.
        """)

# ------------------------------------------------------------ standards, policy

add("ops-std-04", "OPS-STD-04 Operating Envelope", "standard", """
    # OPS-STD-04 — Standard Operating Envelope

    ## Scope and authority

    This standard defines the operating envelope for every turbine in the
    fleet. It is the single authority for the limits below. Site profiles and
    local procedures reference it and must not restate its numbers, because a
    restated limit becomes a second source that drifts silently once one copy
    is revised. Where a site requires a different limit, the difference is
    recorded as a site variance against the specific parameter, with an owner
    and an expiry date, and the variance is listed in the site profile rather
    than written into a local copy of this document.

    ## Gearbox temperature

    The gearbox oil temperature must not exceed 82 degrees Celsius during
    continuous operation. Between 82 and 90 degrees the turbine enters derated
    operation automatically, reducing output until the temperature returns
    below the continuous limit. Above 90 degrees the turbine performs a
    controlled shutdown. Derated operation is a normal control response and is
    not a fault in itself, but sustained derating indicates a developing
    problem: a turbine that derates on temperature for more than four hours in
    any twenty-four is raised to the regional desk for review even where it
    never approaches the shutdown threshold.

    ## Vibration

    Nacelle vibration above 0.55 mm/s RMS sustained for more than thirty
    minutes triggers a Level 2 alert. Above 0.80 mm/s the turbine shuts down
    immediately and requires physical inspection before restart. The
    thirty-minute qualifier matters: transient excursions above the Level 2
    threshold are common in turbulent inflow and do not indicate a developing
    fault, so alerting on instantaneous readings produces noise that trains
    operators to ignore the alert. The immediate-shutdown threshold has no
    such qualifier because the failure modes it guards against develop faster
    than any averaging window would tolerate.

    ## Rotor speed and overspeed protection

    Rated rotor speed is 14.6 rpm. The overspeed trip is set at 17.2 rpm and
    is implemented independently of the main controller, so that a controller
    fault cannot disable it. The trip is tested at every routine inspection
    and the test result is recorded against the turbine rather than against
    the inspection, which allows a history to be read per machine. A failed
    overspeed test takes the turbine out of service immediately and is not
    subject to any deferral provision.

    ## Environmental limits

    Turbines shut down automatically above 25 m/s mean wind speed measured
    over ten minutes, and resume when the mean falls below 20 m/s for a
    sustained period. The gap between the two thresholds prevents repeated
    stop-start cycling in gusty conditions, which imposes more fatigue on the
    drivetrain than either continuous operation or a clean shutdown would.
    Icing detection triggers a shutdown independently of wind speed.
    """)

add("maint-pol-11", "MAINT-POL-11 Inspection Intervals", "policy", """
    # MAINT-POL-11 — Scheduled Inspection Intervals

    ## Routine inspection

    Every turbine receives a routine inspection every 180 days. The interval
    reduces to 90 days for any turbine older than twelve years. Age is counted
    from commissioning rather than from manufacture, and a turbine that has
    had a major component replaced does not reset its age: the interval
    reflects the accumulated fatigue of the structure as a whole rather than
    the age of any single part. Where a site operates turbines either side of
    the twelve-year boundary, the shorter interval is not applied fleet-wide
    for convenience, because doing so obscures which machines are genuinely in
    the reduced-interval population.

    ## Post-alert inspection

    A Level 2 vibration alert requires inspection within 14 days. A Level 3
    alert requires inspection before the turbine is returned to service. The
    distinction is that a Level 2 alert describes a turbine that may continue
    operating under observation, while a Level 3 alert describes one that has
    already stopped. Post-alert inspections are recorded separately from
    routine inspections and do not reset the routine interval, so a turbine
    inspected after an alert is still due its scheduled inspection on the
    original date.

    ## Deferral

    A routine inspection may be deferred once, by no more than 30 days, with
    written approval from the site manager. A post-alert inspection may not be
    deferred under any circumstances. The single-deferral provision exists to
    absorb genuine scheduling conflicts such as weather windows and crew
    availability, not to manage chronic under-resourcing; repeated use of
    deferrals across a site is treated as a resourcing signal and is reported
    to the regional desk quarterly rather than being handled turbine by
    turbine.

    ## Appendix A — filter seating verification

    Following incident 2026-014, filter seating is verified by a second
    engineer on every filter change. The verification is recorded against the
    work order and the identity of the verifying engineer is captured. This
    appendix was added rather than the main body being revised, so that the
    provenance of the requirement remains legible to anyone reading the policy
    later and asking why it exists.

    ## Records

    Inspection records are retained for the operating life of the turbine plus
    six years. Records are held against the turbine identifier rather than the
    site, so that a machine relocated between sites carries its history with
    it rather than starting fresh.
    """)

# -------------------------------------------------------------------- incidents

add("inc-2026-014", "Incident Report 2026-014", "incident", """
    # Incident Report 2026-014

    Date: 14 March 2026. Site: Whitelee. Turbine: WHL-031.
    Classification: thermal shutdown, no injury, no third-party impact.

    ## Summary

    Turbine WHL-031 performed a controlled shutdown after gearbox oil
    temperature reached 91.4 degrees Celsius. The turbine had been in derated
    operation for approximately six hours prior to shutdown. Derating began
    during the early afternoon and was visible on the regional dashboard
    throughout, but no alert was raised because sustained derating did not at
    that time trigger a review threshold. The shutdown itself operated
    correctly and within the expected sequence.

    ## Timeline

    The turbine entered derated operation at 13:20 and remained derated
    through the afternoon with oil temperature oscillating in the derated
    band. Temperature crossed the shutdown threshold at 19:44 and the
    controlled shutdown completed at 19:46. The site was notified
    automatically and the on-call engineer attended the following morning,
    the shutdown having occurred outside working hours and the machine being
    in a safe stopped state with no evidence of secondary damage.

    ## Root cause

    A partially blocked oil cooler restricted flow. The blockage was traced to
    debris ingress following a filter change on 2 March 2026 where the
    replacement filter seal was incorrectly seated. The seal displacement was
    small enough that the change passed its post-work checks, and the debris
    accumulated over the following twelve days until flow restriction was
    sufficient to push operating temperature into the derated band under
    normal load.

    ## Contributing factors

    Two factors extended the time to detection. Sustained derating was not
    itself an alerting condition, so a turbine could operate for hours in a
    degraded state without prompting review. Separately, the post-work check
    for a filter change confirmed that the filter was fitted rather than that
    the seal was seated, which are different checks and only one of them would
    have caught this.

    ## Corrective action

    Filter seating is now verified by a second engineer on every change. The
    verification requirement was added to MAINT-POL-11 as an appendix.
    Sustained derating was added to the operating standard as a review
    trigger, so that a turbine derating on temperature for an extended period
    is now raised to the regional desk before it approaches shutdown.
    """)

add("inc-2026-021", "Incident Report 2026-021", "incident", """
    # Incident Report 2026-021

    Date: 2 June 2026. Site: Clyde. Turbine: CLY-008.
    Classification: vibration shutdown, no injury, no third-party impact.

    ## Summary

    Nacelle vibration on CLY-008 exceeded the immediate-shutdown threshold
    defined in OPS-STD-04, triggering an immediate shutdown. Vibration had been rising steadily for eleven days
    prior, crossing the Level 2 threshold on 22 May. The Level 2 alert was
    raised correctly and the required inspection was scheduled within the
    permitted window, but the shutdown occurred before that inspection took
    place.

    ## Timeline

    Vibration first crossed the Level 2 threshold on 22 May and the alert was
    raised the same day. The required post-alert inspection was scheduled for
    5 June, inside the fourteen-day window. Vibration continued to rise
    through late May without crossing the immediate-shutdown threshold, and
    the turbine shut down on 2 June, three days before the scheduled
    inspection. The trend was visible in the hourly summaries throughout, but
    a rising trend inside an open alert did not at that time shorten the
    inspection deadline.

    ## Root cause

    Blade root bolt tension had relaxed below specification on two of three
    blades. The preceding routine inspection had been deferred by 28 days
    under the single-deferral provision. Bolt tension is checked at routine
    inspection and not at post-alert inspection, so the deferral moved the
    only check that would have detected the relaxation, while the alert that
    followed scheduled a different inspection that would not have.

    ## Contributing factors

    The deferral was approved correctly and within policy as it stood. What
    the policy did not account for was the interaction between a deferred
    routine inspection and a subsequently opened alert on the same machine:
    each was individually compliant, and together they left a developing
    fault unexamined for longer than either would have alone.

    ## Corrective action

    Deferral is no longer permitted for turbines with an open Level 2 alert.
    Where a routine inspection has already been deferred and an alert is
    subsequently raised, the deferred inspection is brought forward to the
    post-alert inspection date and both are completed together.
    """)

# ------------------------------------------------------------ report, procedure

add("perf-2026-q2", "Fleet Performance Summary Q2 2026", "report", """
    # Fleet Performance Summary — Q2 2026

    ## Availability

    Fleet availability averaged 94.2 percent. Whitelee recorded the highest
    availability at 96.1 percent. Beinn an Tuirc recorded the lowest at
    91.3 percent, attributed to two extended outages. Availability is reported
    net of scheduled maintenance, so a site with a heavy scheduled programme
    in the quarter is not penalised for completing it; this is worth stating
    because the raw figures are sometimes quoted without the qualifier and
    then compared against vendor availability guarantees, which are defined
    differently.

    ## Failure rate

    The fleet failure rate for the quarter was 3.1 failures per hundred
    turbines. Clyde recorded the highest site failure rate at 5.9 per hundred
    turbines. Ardrossan recorded 2.4 and Whitelee 2.1. The per-hundred
    convention allows sites of different sizes to be compared directly. A
    failure is counted when a turbine stops unscheduled, regardless of
    duration, so a brief self-clearing stop counts the same as a multi-day
    outage — a deliberate choice that makes the metric a measure of
    reliability rather than of lost generation.

    ## Reading the failure rate

    A single site standing well above the fleet rate warrants investigation
    rather than immediate action, because the metric counts events and not
    severity. The quarter's figure for the highest site is driven by a cluster
    of vibration-related stops rather than by a broad deterioration across the
    machines, and the two are different problems with different responses.
    Reading a site-level rate without its composition is the most common
    misuse of this report.

    ## Generation

    Total generation was 412 GWh, three percent above the quarterly forecast.
    The overperformance is attributable to wind resource rather than to
    availability, which sat close to plan. Forecast variance of this magnitude
    is within the normal range for a single quarter and is not treated as a
    forecasting error.

    ## Outlook

    Two extended outages carried into the quarter from Q1 and are now closed.
    No site is currently operating under a capacity restriction. The variance
    register carries four open entries across the fleet, all within their
    expiry dates.
    """)

add("proc-restart-07", "PROC-RESTART-07 Return to Service", "procedure", """
    # PROC-RESTART-07 — Return to Service After Shutdown

    ## Applicability

    This procedure applies after any automatic shutdown, including overspeed,
    vibration and thermal shutdowns. It applies equally to shutdowns that
    appear self-explanatory: a turbine that stopped for an obvious reason
    still passes through the full sequence, because the purpose of the
    procedure is to establish that the originating condition has cleared
    rather than to explain why it occurred.

    ## Sequence

    1. Confirm the originating fault has been cleared and logged.
    2. Complete the inspection required by MAINT-POL-11 for the alert level.
    3. Obtain written release from the site manager.
    4. Restart under supervision and monitor for two hours at reduced output.

    The monitoring period is not optional and is not shortened for turbines
    that restart cleanly. Faults that recur tend to recur under load, and the
    reduced-output window is where a recurrence is cheapest to observe.

    ## Authority

    The site manager holds release authority during working hours. Out of
    hours, the national control room may stop a turbine but may not release
    one, so an overnight shutdown waits for the following working morning.
    This is deliberate rather than a staffing limitation: the decision to stop
    is reversible and the decision to start is not, and the authority to take
    each is set accordingly.

    ## Restriction

    A turbine that has shut down twice within 30 days may not be returned to
    service without regional engineering approval. The counter runs on
    shutdowns rather than on faults, so two stops from unrelated causes still
    trigger the restriction. The intent is to catch machines that are
    developing a problem the individual investigations have each missed.

    ## Records

    The release is recorded against the turbine with the identity of the
    releasing manager, the inspection reference, and the observed behaviour
    during the monitoring window. An incomplete monitoring record invalidates
    the release and the turbine is returned to a stopped state pending review.
    """)

# ------------------------------------------------- uniqueness of planted facts
# Gold labels are only correct by construction if the construction is checked.
# Each string below must appear in exactly one document; the longer documents in
# this version make accidental restatement much easier than it used to be.

UNIQUE_TO = {
    "82 degrees":                 "ops-std-04",
    "0.80 mm/s":                  "ops-std-04",
    "0.55 mm/s":                  "ops-std-04",
    "14.6 rpm":                   "ops-std-04",
    "17.2 rpm":                   "ops-std-04",
    "180 days":                   "maint-pol-11",
    "90 days":                    "maint-pol-11",
    "14 days":                    "maint-pol-11",
    "WHL-031":                    "inc-2026-014",
    "oil cooler":                 "inc-2026-014",
    "CLY-008":                    "inc-2026-021",
    "blade root bolt":            "inc-2026-021",
    "5.9 per hundred":            "perf-2026-q2",
    "412 GWh":                    "perf-2026-q2",
    "S. Tran":                    "site-cly",
    "M. Lindqvist":               "site-whl",
    "J. Okafor":                  "site-ard",
    "R. Achebe":                  "site-bat",
    "regional engineering approval": "proc-restart-07",
}

by_id = {d["doc_id"]: d["text"] for d in DOCS}
problems = []
for fact, expected in UNIQUE_TO.items():
    holders = sorted(i for i, t in by_id.items() if fact.lower() in t.lower())
    allowed = expected.split(",")
    if len(holders) != 1 or holders[0] not in allowed:
        problems.append(f"  {fact!r}: expected only in {allowed}, found in {holders}")

# The refusal question depends on the corpus saying nothing about bearing life.
for banned in ("bearing lifespan", "bearing life", "bearings last"):
    hits = sorted(i for i, t in by_id.items() if banned in t.lower())
    if hits:
        problems.append(f"  {banned!r} must not appear anywhere (q10 is the refusal test), found in {hits}")

if problems:
    raise SystemExit("planted facts are not unique:\n" + "\n".join(problems))

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

words = sum(len(d["text"].split()) for d in DOCS)
print(f"wrote {len(DOCS)} documents to {OUT.relative_to(ROOT)}")
print(f"  {words} words total (~{int(words * 1.3)} tokens), median {sorted(len(d['text'].split()) for d in DOCS)[len(DOCS)//2]} words per document")
print(f"  planted facts verified unique: {len(UNIQUE_TO)}")
print(f"wrote {len(EVAL)} eval questions to data/corpus_eval.json")
print(f"  single-hop : {sum(1 for e in EVAL if e['hops']==1)}")
print(f"  multi-hop  : {sum(1 for e in EVAL if e['hops']==2)}  <- single-shot retrieval cannot answer these")
print(f"  unanswerable: {sum(1 for e in EVAL if e['hops']==0)}  <- the system should refuse")
