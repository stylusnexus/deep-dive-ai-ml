#!/usr/bin/env python3
"""Turn the split records into the chat JSONL that mlx_lm.lora expects.

The prompt deliberately does NOT contain the policies. That is the experiment: the
base model can be given the policy text every call and reason from it, which costs
tokens on every request forever. Fine-tuning is supposed to buy the same behaviour
without paying for that text. Training without the policies and evaluating the base
model both with and without them is what makes the comparison mean something.

    python3 scripts/make_finetune_jsonl.py
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "finetune"
OUT = SRC / "mlx"
OUT.mkdir(parents=True, exist_ok=True)

ACTIONS = ["reschedule", "return_to_depot", "request_address_correction",
           "refund_and_replace", "notify_delay", "request_documents", "refund",
           "return_to_sender", "hold_at_depot", "log_carrier_fault",
           "escalate_to_human"]

SYSTEM = ("You decide the action for a delivery exception. The note may contradict "
          "the event code; where it does, the note is what happened. Reply with the "
          "action only, one of: " + ", ".join(ACTIONS) + ".")


def user_text(r):
    parts = [f"event_code: {r['event_code']}"]
    if r.get("attempt") is not None:
        parts.append(f"attempt: {r['attempt']}")
    parts.append(f"order_value_gbp: {r['order_value_gbp']}")
    parts.append(f"customer_tier: {r['customer_tier']}")
    parts.append(f"note: {r['note']}")
    return "\n".join(parts)


def main():
    for name in ("train", "valid", "test"):
        rows = json.loads((SRC / f"{name}.json").read_text())
        lines = []
        for r in rows:
            lines.append(json.dumps({"messages": [
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": user_text(r)},
                {"role": "assistant", "content": r["gold_action"]},
            ]}))
        (OUT / f"{name}.jsonl").write_text("\n".join(lines) + "\n")
        print(f"{name:>6}: {len(lines):>5} examples -> data/finetune/mlx/{name}.jsonl")

    sample = json.loads((OUT / "train.jsonl").read_text().split("\n")[0])
    print("\nfirst training example:")
    for m in sample["messages"]:
        body = m["content"] if len(m["content"]) < 220 else m["content"][:200] + " ..."
        print(f"  [{m['role']}] {body}")


if __name__ == "__main__":
    main()
