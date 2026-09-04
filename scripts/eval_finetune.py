#!/usr/bin/env python3
"""Score a model on the held-out delivery-exception test set.

Three conditions, because a fine-tune has to be measured against what you could
have done instead rather than against nothing:

  base            the base model, prompt as trained (no policies)
  base+policies   the base model, policies pasted into every prompt
  tuned           the base model plus the trained LoRA adapter

The lookup table's score on the same rows is printed alongside, because on this
corpus that is the honest floor and it is not a low one.

    .venv-train/bin/python scripts/eval_finetune.py --adapter adapters
"""
import argparse
import json
import pathlib
import re
import sys
import time
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_finetune_jsonl import ACTIONS, SYSTEM, user_text  # noqa: E402

from mlx_lm import generate, load  # noqa: E402
from mlx_lm.sample_utils import make_sampler  # noqa: E402

POLICIES = "\n\n".join(
    p["text"] for p in json.loads((ROOT / "data" / "exceptions" / "policies.json").read_text()))


def parse_action(text):
    """First allowed action named in the reply, or None."""
    low = (text or "").lower()
    hits = [(low.find(a), a) for a in ACTIONS if a in low]
    hits = [(i, a) for i, a in hits if i >= 0]
    return min(hits)[1] if hits else None


def score(model, tokenizer, rows, with_policies=False, label=""):
    sampler = make_sampler(temp=0.0)
    correct = unparsed = 0
    per_kind = Counter()
    t0 = time.time()
    for n, r in enumerate(rows, 1):
        system = SYSTEM if not with_policies else SYSTEM + "\n\nPolicies:\n" + POLICIES
        msgs = [{"role": "system", "content": system},
                {"role": "user", "content": user_text(r)}]
        prompt = tokenizer.apply_chat_template(msgs, add_generation_prompt=True)
        out = generate(model, tokenizer, prompt=prompt, max_tokens=12,
                       sampler=sampler, verbose=False)
        got = parse_action(out)
        if got is None:
            unparsed += 1
        ok = got == r["gold_action"]
        correct += ok
        per_kind["judgement" if r["needs_judgement"] else "routine"] += ok
        if n % 60 == 0:
            print(f"    {label} {n}/{len(rows)} …", flush=True)
    total_j = sum(1 for r in rows if r["needs_judgement"])
    total_r = len(rows) - total_j
    return {
        "label": label,
        "accuracy": correct / len(rows),
        "judgement": per_kind["judgement"] / total_j if total_j else 0.0,
        "routine": per_kind["routine"] / total_r if total_r else 0.0,
        "unparsed": unparsed,
        "seconds": round(time.time() - t0),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="mlx-community/Qwen2.5-1.5B-Instruct-4bit")
    ap.add_argument("--adapter", default=None)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--conditions", default="base,base+policies")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    rows = json.loads((ROOT / "data" / "finetune" / "test.json").read_text())
    if args.limit:
        rows = rows[:args.limit]
    rule_ok = sum(1 for r in rows if r["rule_action"] == r["gold_action"]) / len(rows)
    rule_j = [r for r in rows if r["needs_judgement"]]
    rule_r = [r for r in rows if not r["needs_judgement"]]
    rule_j_ok = sum(1 for r in rule_j if r["rule_action"] == r["gold_action"]) / len(rule_j)
    rule_r_ok = (sum(1 for r in rule_r if r["rule_action"] == r["gold_action"]) / len(rule_r)
                 if rule_r else 0.0)
    print(f"test rows: {len(rows)}  ({len(rule_j)} judgement)")
    print(f"lookup table: overall {rule_ok:.3f}   judgement {rule_j_ok:.3f}\n")

    results = []
    for cond in args.conditions.split(","):
        cond = cond.strip()
        adapter = args.adapter if cond == "tuned" else None
        model, tok = load(args.model, adapter_path=adapter)
        results.append(score(model, tok, rows,
                             with_policies=(cond == "base+policies"), label=cond))
        print(f"  {results[-1]}\n", flush=True)

    print(f"{'condition':<16}{'overall':>9}{'routine':>9}{'judgement':>11}{'unparsed':>10}{'sec':>7}")
    print("-" * 62)
    print(f"{'lookup table':<16}{rule_ok:>9.3f}{rule_r_ok:>9.3f}{rule_j_ok:>11.3f}{'-':>10}{'-':>7}")
    for r in results:
        print(f"{r['label']:<16}{r['accuracy']:>9.3f}{r['routine']:>9.3f}"
              f"{r['judgement']:>11.3f}{r['unparsed']:>10}{r['seconds']:>7}")

    if args.out:
        payload = {"rows": len(rows), "lookup_overall": rule_ok,
                   "lookup_routine": rule_r_ok, "lookup_judgement": rule_j_ok,
                   "results": results}
        pathlib.Path(args.out).write_text(json.dumps(payload, indent=1) + "\n")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
