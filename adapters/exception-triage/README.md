# exception-triage — a LoRA adapter that lost

A LoRA adapter for `Qwen2.5-1.5B-Instruct-4bit`, trained to pick the right action for
a delivery exception. It works, and it is **worse than the nine-entry lookup table it
was meant to replace**.

That is why it's kept. It's the evidence behind Block 7's argument that most
fine-tuning projects should stop before they start.

## The result

Scored on 295 held-out rows, single run, greedy decoding:

| Condition | Overall | Routine cases | Judgement cases |
|---|---|---|---|
| Lookup table | **0.458** | 1.000 | 0.000 |
| Base model | 0.281 | 0.319 | 0.250 |
| Base + policies in the prompt | 0.227 | 0.437 | 0.050 |
| **Tuned (this adapter)** | 0.393 | 0.859 | **0.000** |

Read the last column. The tuned model agrees with the lookup table 80% of the time
overall and 75% on judgement cases — and the table is *always wrong* on judgement
cases, because those are exactly the ones a rule can't decide.

So the adapter learned the rule, including its blind spot. It got much better at the
easy cases (0.319 → 0.859) by learning to be confidently wrong on the hard ones
(0.250 → 0.000). The base model, which knew nothing, was better at judgement than
the model trained on judgement data.

Pasting the policies into the prompt made things worse still, and produced 17
unparseable replies out of 295.

## What it is

| | |
|---|---|
| Base model | `mlx-community/Qwen2.5-1.5B-Instruct-4bit` |
| Method | LoRA, 8 layers, rank 8, scale 20, dropout 0 |
| Training | 600 iterations, batch 8, lr 1e-4, prompt masked, seed 23 |
| Data | 965 train / 120 validation / 295 test rows |
| Split | **Grouped by scenario** — 8 judgement scenarios trained on, 4 held out entirely |
| Peak memory | 4.16 GB |
| Trained tokens | 27,460 |

The split is the part worth copying. Splitting these rows at random would have put
near-identical scenarios on both sides and produced a much prettier number that meant
nothing.

## Using it

Needs `mlx-lm` on Apple Silicon. The base model downloads on first use.

```python
import sys; sys.path.insert(0, "scripts")
from make_finetune_jsonl import SYSTEM, user_text
from mlx_lm import load, generate
from mlx_lm.sample_utils import make_sampler

model, tok = load("mlx-community/Qwen2.5-1.5B-Instruct-4bit",
                  adapter_path="adapters/exception-triage")

row = {"event_code": "ADDRESS_INVALID", "attempt": 2, "order_value_gbp": 41.0,
       "customer_tier": "standard",
       "note": "driver says the flat number is missing from the label"}

msgs = [{"role": "system", "content": SYSTEM},
        {"role": "user", "content": user_text(row)}]
print(generate(model, tok, prompt=tok.apply_chat_template(msgs, add_generation_prompt=True),
               max_tokens=12, sampler=make_sampler(temp=0.0), verbose=False))
# -> 'request_address_correction'
```

It replies with one action from a fixed list of eleven: `reschedule`,
`return_to_depot`, `request_address_correction`, `refund_and_replace`, `notify_delay`,
`request_documents`, `refund`, `return_to_sender`, `hold_at_depot`,
`log_carrier_fault`, `escalate_to_human`.

## What it's for

Teaching. It is a worked example of a fine-tune that succeeded technically and failed
on the thing that mattered.

**Do not use it for anything real.** It scores 0.000 on the 160 cases needing
judgement. For the 80 of those where the right answer was to escalate to a human, it
never did — the failure mode you least want in an operations system.

## Reproducing

```bash
python3 scripts/make_finetune_data.py
python3 scripts/make_finetune_jsonl.py
mlx_lm.lora --train --data data/finetune/mlx --num-layers 8 --iters 600 ...
.venv-train/bin/python scripts/eval_finetune.py --conditions base,base+policies,tuned
```

Full numbers in [`artifacts/finetune-results.json`](../../artifacts/finetune-results.json).

## The lesson

Measure a fine-tune against **what you would have done instead**, not against
nothing. Against the base model this adapter is a clear win: 0.281 to 0.393. Against
the lookup table anyone would actually have shipped, it's a loss — and the comparison
that flatters it is the one most projects report.

Weights are gitignored; this card is not.
