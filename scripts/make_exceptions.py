#!/usr/bin/env python3
"""A delivery-exception log with known ground truth, plus the policies that govern it.

Synthetic on purpose, for the same reason as the Block 3 corpus: the gold action
for every exception is correct by construction rather than hand-labelled, so the
question Project 3 exists to answer — what fraction of exceptions genuinely needs
judgement rather than a lookup table — has an exact answer to be measured against.

Most exceptions here are decided entirely by their event code. A minority carry a
note that contradicts the code, and those are the only ones a model earns its
place on. The split is deliberate and it is recorded in the data.
"""
import json, pathlib, random, textwrap

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "exceptions"
OUT.mkdir(parents=True, exist_ok=True)

rng = random.Random(11)

CARRIERS = ["Northgate", "Ardent Logistics", "Kestrel Freight", "Bowline Parcels"]
TIERS = ["standard", "standard", "standard", "priority", "business"]

# ---------------------------------------------------------------- policies

POLICIES = []

def policy(doc_id, title, body):
    POLICIES.append({"doc_id": doc_id, "title": title, "text": textwrap.dedent(body).strip()})

policy("pol-del-01", "POL-DEL-01 Delivery Attempts and Rescheduling", """
    # POL-DEL-01 Delivery Attempts and Rescheduling

    A carrier may attempt delivery three times. Attempts one and two are
    rescheduled automatically for the next working day. On the third failed
    attempt the parcel returns to the depot and the customer is notified that
    collection is available for ten days.

    Where the recipient is known to be away for an extended period — including
    hospitalisation — the parcel is held at the depot for that period rather
    than reattempted. Reattempting a delivery to an address the recipient is
    known to be away from wastes an attempt and is not permitted.

    Where a recipient asks for a parcel to be held following a bereavement or
    other personal circumstance, it is held at the depot. This is a hold, not a
    refusal, and the parcel is not returned to the sender.

    A failed attempt caused by the carrier — attending on the wrong day, or at
    the wrong address — does not count towards the three attempts. It is
    rescheduled and the counter is unchanged.

    An invalid or incomplete address is never a failed attempt. The customer is
    asked to correct the address and the attempt counter is reset.
    """)

policy("pol-dam-02", "POL-DAM-02 Damage, Refunds and Replacements", """
    # POL-DAM-02 Damage, Refunds and Replacements

    Goods recorded as damaged in transit are refunded and replaced without
    requiring the customer to return them, where the order value is below
    £250.

    Damage to outer packaging alone, where the recipient confirms the contents
    are intact and wishes to keep the goods, is not a damage event. No refund
    or replacement is issued; the packaging fault is logged against the carrier.

    Orders at or above £250 recorded as damaged require human review before any
    refund is issued, regardless of customer tier.
    """)

policy("pol-cus-03", "POL-CUS-03 Customs and Documentation", """
    # POL-CUS-03 Customs and Documentation

    A parcel held at customs pending documentation is released once the
    customer supplies the missing paperwork. The customer is asked once, then
    again after five days.

    A parcel held at customs for a prohibited or restricted item is not a
    documentation problem and must not be handled by requesting paperwork. It
    is escalated to the trade compliance team.

    Where the documentation has already been supplied and acknowledged and the
    hold has not lifted, asking again would loop. The case is escalated.
    """)

policy("pol-esc-04", "POL-ESC-04 Escalation and Human Review", """
    # POL-ESC-04 Escalation and Human Review

    The following are escalated to a human and never decided automatically:

    - Any order at or above £250 involving damage, loss or refund
    - Any exception where injury is reported in connection with the goods or
      the delivery itself
    - Any suspected prohibited or restricted item
    - Any consignment described as time-critical or temperature-controlled
      where the delay would exceed its stated window

    Illness or bereavement explaining why a recipient was absent is not on this
    list. That is an absence, and POL-DEL-01 says what to do with it.

    Escalation is a decision to not decide. It is recorded in the trace with the
    reason, and the case leaves the automated path entirely.
    """)

policy("pol-com-05", "POL-COM-05 Customer Communication Standards", """
    # POL-COM-05 Customer Communication Standards

    Every message to a customer states what happened, what is being done, and
    what if anything the customer must do. It does not apologise for events
    outside the carrier's control, and it never states a delivery date that has
    not been confirmed by the carrier.

    Messages about damage, loss or refunds are approved by a human before
    sending. No exception to this exists.
    """)

policy("pol-gen-06", "POL-GEN-06 Records and Delivery Notes", """
    # POL-GEN-06 Records and Delivery Notes

    An event code is recorded by the carrier's system; a delivery note is
    written by the person who was there. Where the note contradicts the code,
    the note is authoritative, and the exception is handled according to what
    the note actually describes rather than what the code says.

    A parcel marked lost that has since been scanned is not lost. It re-enters
    the network and the customer is notified that the delivery is delayed; a
    parcel already moving is not rescheduled, because no attempt has failed.

    An address marked invalid that the driver simply could not find is not
    invalid.

    Where the note contradicts the code and leaves no clear correct action, the
    case is escalated rather than guessed.
    """)

# ------------------------------------------------------- deterministic rules

# The lookup table. This is the dumb baseline the intake sheet demands, and it
# is genuinely correct for the routine cases — which is the finding, not a flaw.
RULES = {
    ("ADDRESS_INVALID", None):     "request_address_correction",
    ("RECIPIENT_ABSENT", 1):       "reschedule",
    ("RECIPIENT_ABSENT", 2):       "reschedule",
    ("RECIPIENT_ABSENT", 3):       "return_to_depot",
    ("DAMAGED_IN_TRANSIT", None):  "refund_and_replace",
    ("WEATHER_DELAY", None):       "notify_delay",
    ("CUSTOMS_HOLD", None):        "request_documents",
    ("LOST_IN_NETWORK", None):     "refund",
    ("REFUSED_BY_RECIPIENT", None):"return_to_sender",
}

def rule_action(event_code, attempt):
    return RULES.get((event_code, attempt)) or RULES.get((event_code, None))

ROUTINE_NOTES = {
    "ADDRESS_INVALID":      ["postcode does not match street", "flat number missing",
                             "street name not recognised by carrier"],
    "RECIPIENT_ABSENT":     ["no answer at door", "no safe place available",
                             "card left, no response"],
    "DAMAGED_IN_TRANSIT":   ["corner crushed, contents rattling", "seal broken, item visibly damaged",
                             "water damage to contents"],
    "WEATHER_DELAY":        ["depot closed, flooding on access road", "named storm, network suspended",
                             "snow, rural routes not running"],
    "CUSTOMS_HOLD":         ["commercial invoice missing", "value declaration incomplete",
                             "EORI number not supplied"],
    "LOST_IN_NETWORK":      ["no scan for eleven days", "last scan at outbound hub, no further movement",
                             "parcel not found at declared depot"],
    "REFUSED_BY_RECIPIENT": ["recipient says not ordered", "recipient refused at door",
                             "recipient declined, no reason given"],
}

# ------------------------------------------------- cases that need judgement

# Each names the action the rule table would take, the action that is actually
# correct, and why. The "why" is what makes this data a test rather than a demo.
JUDGEMENT = [
 dict(event_code="DAMAGED_IN_TRANSIT", attempt=None, value=38.0,
      note="outer box crushed but recipient opened it with the driver present, contents intact, wants to keep the item",
      gold="log_carrier_fault",
      why="POL-DAM-02: packaging-only damage with contents confirmed intact is not a damage event"),
 dict(event_code="DAMAGED_IN_TRANSIT", attempt=None, value=410.0,
      note="item damaged, recipient wants refund",
      gold="escalate_to_human",
      why="POL-ESC-04: order at or above £250 involving damage requires human review"),
 dict(event_code="RECIPIENT_ABSENT", attempt=2, value=64.0,
      note="neighbour says recipient is in hospital and will be for a fortnight",
      gold="hold_at_depot",
      why="POL-DEL-01: a known extended absence is held at the depot, not reattempted"),
 dict(event_code="CUSTOMS_HOLD", attempt=None, value=95.0,
      note="held as restricted item, customs cite prohibited goods schedule",
      gold="escalate_to_human",
      why="POL-CUS-03: a prohibited-item hold is not a documentation problem"),
 dict(event_code="LOST_IN_NETWORK", attempt=None, value=52.0,
      note="marked lost on Tuesday but tracking updated this morning, parcel scanned at local depot",
      gold="notify_delay",
      why="POL-GEN-06: the note is authoritative — a parcel scanned at a depot is not lost"),
 dict(event_code="REFUSED_BY_RECIPIENT", attempt=None, value=88.0,
      note="recipient refused because of a bereavement in the household and asked us to hold",
      gold="hold_at_depot",
      why="POL-DEL-01: a hold requested after a bereavement is held, not returned to sender"),
 dict(event_code="WEATHER_DELAY", attempt=None, value=310.0,
      note="storm delay, consignment is temperature-controlled medical supply with 48-hour window",
      gold="escalate_to_human",
      why="POL-ESC-04: a temperature-controlled consignment whose window the delay would exceed"),
 dict(event_code="ADDRESS_INVALID", attempt=None, value=120.0,
      note="address is correct, driver went to the wrong town with the same street name",
      gold="reschedule",
      why="POL-GEN-06: the note is authoritative — the address was correct"),
 dict(event_code="RECIPIENT_ABSENT", attempt=3, value=45.0,
      note="third attempt, but recipient had rearranged for Friday and carrier attended Thursday",
      gold="reschedule",
      why="POL-DEL-01: a carrier-caused failed attempt does not count towards the three"),
 dict(event_code="LOST_IN_NETWORK", attempt=None, value=630.0,
      note="no scan for two weeks, customer chasing",
      gold="escalate_to_human",
      why="POL-ESC-04: loss at or above £250 requires human review"),
 dict(event_code="DAMAGED_IN_TRANSIT", attempt=None, value=71.0,
      note="recipient reports cut hand opening the damaged packaging",
      gold="escalate_to_human",
      why="POL-ESC-04: injury reported in connection with the goods"),
 dict(event_code="CUSTOMS_HOLD", attempt=None, value=140.0,
      note="paperwork was supplied a week ago and acknowledged, hold not lifted",
      gold="escalate_to_human",
      why="POL-CUS-03: documentation already supplied and acknowledged — asking again would loop"),
]

# ------------------------------------------------------------------ generate

EXCEPTIONS = []

def add(event_code, attempt, note, value, tier, gold, needs_judgement, why):
    n = len(EXCEPTIONS) + 1
    EXCEPTIONS.append({
        "exception_id": f"exc-{n:04d}",
        "order_id": f"ORD-{rng.randint(100000, 999999)}",
        "carrier": rng.choice(CARRIERS),
        "event_code": event_code,
        "attempt": attempt,
        "note": note,
        "customer_tier": tier,
        "order_value_gbp": value,
        "rule_action": rule_action(event_code, attempt),
        "gold_action": gold,
        "needs_judgement": needs_judgement,
        "why": why,
    })

# Routine cases: the note agrees with the code, so the lookup table is right.
for _ in range(108):
    code = rng.choice(list(ROUTINE_NOTES))
    attempt = rng.choice([1, 2, 3]) if code == "RECIPIENT_ABSENT" else None
    value = round(rng.uniform(12, 240), 2)
    add(code, attempt, rng.choice(ROUTINE_NOTES[code]), value, rng.choice(TIERS),
        rule_action(code, attempt), False, "routine — the event code decides it")

# Judgement cases: the note overrides the code.
for j in JUDGEMENT:
    for _ in range(2):
        add(j["event_code"], j["attempt"], j["note"], j["value"],
            rng.choice(TIERS), j["gold"], True, j["why"])

rng.shuffle(EXCEPTIONS)
for i, e in enumerate(EXCEPTIONS, 1):
    e["exception_id"] = f"exc-{i:04d}"

(OUT / "policies.json").write_text(json.dumps(POLICIES, indent=2) + "\n")
(OUT / "exceptions.json").write_text(json.dumps(EXCEPTIONS, indent=2) + "\n")

need = sum(1 for e in EXCEPTIONS if e["needs_judgement"])
agree = sum(1 for e in EXCEPTIONS if e["rule_action"] == e["gold_action"])
print(f"wrote {len(POLICIES)} policies to data/exceptions/policies.json")
print(f"wrote {len(EXCEPTIONS)} exceptions to data/exceptions/exceptions.json")
print(f"  routine            : {len(EXCEPTIONS) - need}")
print(f"  needing judgement  : {need}  ({need / len(EXCEPTIONS):.0%})")
print(f"  lookup table correct: {agree}/{len(EXCEPTIONS)}  ({agree / len(EXCEPTIONS):.0%})  <- the number to beat")
