#!/usr/bin/env python3
"""Training data for the Block 7 fine-tune, split by scenario rather than at random.

The committed corpus in data/exceptions/ is 132 rows and is left alone — Project 3
and three notebooks depend on it. This writes a larger set to data/finetune/ for
training only.

The split is the point. The judgement cases come from twelve hand-written scenarios,
so repeating them and splitting at random puts a near-identical row on both sides and
measures memorisation. Instead the twelve scenarios are split into groups: eight are
trained on, four are held out entirely, and the test set asks whether the model
learned the *pattern* — that the note can override the event code — rather than the
notes it saw.

    python3 scripts/make_finetune_data.py
"""
import json
import pathlib
import random
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

# make_exceptions writes its files at import time. It is seeded, so the bytes are
# identical to what is committed; the caller verifies that afterwards.
import make_exceptions as mx  # noqa: E402

OUT = ROOT / "data" / "finetune"
OUT.mkdir(parents=True, exist_ok=True)

rng = random.Random(23)

PER_SCENARIO = 40          # instances of each judgement scenario
ROUTINE = 900              # routine rows, which the lookup table already gets right
HELD_OUT_SCENARIOS = 4     # scenarios the model never sees in training


def instance(code, attempt, note, value, tier, gold, judgement, scenario):
    return {
        "carrier": rng.choice(mx.CARRIERS),
        "event_code": code,
        "attempt": attempt,
        "note": note,
        "customer_tier": tier,
        "order_value_gbp": value,
        "rule_action": mx.rule_action(code, attempt),
        "gold_action": gold,
        "needs_judgement": judgement,
        "scenario": scenario,
    }


def main():
    scenarios = list(range(len(mx.JUDGEMENT)))
    rng.shuffle(scenarios)
    held_out = set(scenarios[:HELD_OUT_SCENARIOS])
    trained = [s for s in scenarios if s not in held_out]

    judgement_rows = []
    for idx, j in enumerate(mx.JUDGEMENT):
        for _ in range(PER_SCENARIO):
            # vary only what a real record would vary; the note is the scenario
            value = round(j["value"] * rng.uniform(0.9, 1.1), 2)
            judgement_rows.append(instance(
                j["event_code"], j["attempt"], j["note"], value,
                rng.choice(mx.TIERS), j["gold"], True, idx))

    routine_rows = []
    for _ in range(ROUTINE):
        code = rng.choice(list(mx.ROUTINE_NOTES))
        attempt = rng.choice([1, 2, 3]) if code == "RECIPIENT_ABSENT" else None
        routine_rows.append(instance(
            code, attempt, rng.choice(mx.ROUTINE_NOTES[code]),
            round(rng.uniform(12, 240), 2), rng.choice(mx.TIERS),
            mx.rule_action(code, attempt), False, -1))

    rng.shuffle(routine_rows)
    cut = int(0.85 * len(routine_rows))

    train = [r for r in judgement_rows if r["scenario"] in trained] + routine_rows[:cut]
    test = [r for r in judgement_rows if r["scenario"] in held_out] + routine_rows[cut:]
    rng.shuffle(train)
    rng.shuffle(test)

    # a validation slice out of TRAIN scenarios, for early stopping only
    valid = train[:120]
    train = train[120:]

    for name, rows in (("train", train), ("valid", valid), ("test", test)):
        (OUT / f"{name}.json").write_text(json.dumps(rows, indent=1) + "\n")
        j = sum(1 for r in rows if r["needs_judgement"])
        rule_ok = sum(1 for r in rows if r["rule_action"] == r["gold_action"])
        print(f"{name:>6}: {len(rows):>5} rows  ({j:>4} judgement)  "
              f"lookup-table correct {100*rule_ok/len(rows):>5.1f}%")

    (OUT / "split.json").write_text(json.dumps({
        "trained_scenarios": sorted(trained),
        "held_out_scenarios": sorted(held_out),
        "held_out_notes": [mx.JUDGEMENT[i]["note"] for i in sorted(held_out)],
        "held_out_gold": [mx.JUDGEMENT[i]["gold"] for i in sorted(held_out)],
    }, indent=1) + "\n")

    print(f"\nscenarios trained on : {sorted(trained)}")
    print(f"scenarios HELD OUT   : {sorted(held_out)}")
    print("no held-out scenario's note appears anywhere in training or validation")


if __name__ == "__main__":
    main()
