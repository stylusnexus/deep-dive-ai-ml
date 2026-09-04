OUTDIR = "notebooks/07-finetuning"

_LOAD = '''import json
from pathlib import Path

ROOT = Path.cwd()
while not (ROOT / "artifacts").exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

R = json.loads((ROOT / "artifacts" / "finetune-results.json").read_text())
run = R["run"]

print("what was run")
for k in ("base_model", "method", "split"):
    print(f"  {k:<16} {run[k]}")
print(f"  {'rows':<16} train {run['train_rows']}, valid {run['valid_rows']}, "
      f"test {run['test_rows']}")
print(f"  {'cost':<16} peak {run['peak_memory_gb']} GB, "
      f"{run['trained_tokens']:,} trained tokens, a few minutes on one laptop")'''


_TABLE = '''rows = [("lookup table", R["lookup_overall"], R["lookup_routine"], R["lookup_judgement"], "-")]
for r in R["results"]:
    rows.append((r["label"], r["accuracy"], r["routine"], r["judgement"], r["unparsed"]))

print(f"{'condition':<16}{'overall':>9}{'routine':>9}{'judgement':>11}{'unparsed':>10}")
print("-" * 55)
for name, o, rt, j, u in rows:
    mark = "  <-- best overall" if abs(o - max(x[1] for x in rows)) < 1e-9 else ""
    print(f"{name:<16}{o:>9.3f}{rt:>9.3f}{j:>11.3f}{str(u):>10}{mark}")'''


_AGREE = '''a = R["agreement_with_lookup_table"]
print(f"tuned predictions matching the lookup table, overall        : {a['overall']:.1%}")
print(f"tuned predictions matching the lookup table, judgement only : {a['on_judgement_cases']:.1%}")
print()
print("the judgement cases are the ones where the lookup table is wrong by construction.")
print("the fine-tune agreed with it on three quarters of them.")'''


_LOSS = '''print(f"final training loss   : {run['final_train_loss']:.3f}")
print(f"final validation loss : {run['final_val_loss']:.3f}")
print(f"judgement accuracy    : {R['results'][2]['judgement']:.3f}")
print()
print("the validation set was drawn from scenarios the model TRAINED on,")
print("so it measured how well the model reproduced what it had seen — which was perfectly.")
print("it had no way to report the failure, because the failure is on scenarios")
print("it was deliberately never shown.")'''


NOTEBOOKS = [
("02-the-training-run.ipynb", [

("md", """# 07 · The Training Run

Block 7's first lesson argues that most fine-tuning projects should stop before they
start. This is the one that did not stop, on this repository's own data, and the
result is the argument.

The run itself is not in this notebook. It needs MLX, a downloaded base model and a
few minutes of Apple Silicon, which is more than a reader should have to arrange to
read a result. What is here is the analysis of what came back, from
`artifacts/finetune-results.json`. To reproduce the run:

```
python3 scripts/make_finetune_data.py      # split BY SCENARIO, not at random
python3 scripts/make_finetune_jsonl.py     # chat format for mlx_lm
mlx_lm.lora --train --data data/finetune/mlx --num-layers 8 --iters 600 ...
python3 scripts/eval_finetune.py --conditions base,base+policies,tuned
```"""),

("code", _LOAD),

("md", """## The split is the experiment

The judgement cases in this corpus come from twelve hand-written scenarios. Repeat
them and split at random and a near-identical row lands on both sides, which measures
memorisation — the exact failure the previous notebook found in this dataset.

So the split is **by scenario**. Eight are trained on and four are held out entirely,
and the test set asks whether the model learned the *pattern* the lesson describes —
that a note can override the event code — rather than the eight notes it saw."""),

("md", """## The result

Four conditions. The lookup table is a dictionary from event code to action, written
before any of this and running in Project 3 today."""),

("code", _TABLE),

("md", """Read the routine column first, because that part worked. The fine-tune took routine
accuracy from 0.319 to 0.859 — it genuinely learned the mapping, on a laptop, in
minutes, for a few megabytes of adapter. As a demonstration that low-rank adaptation
does what it claims, this is a success.

Now read the judgement column. The base model, bad at everything, got a quarter of the
judgement cases right. The fine-tuned model got **none of them**. Fine-tuning made the
model worse at the only cases that needed a model at all.

And the lookup table beat all three."""),

("md", """## What the fine-tune actually learned"""),

("code", _AGREE),

("md", """This is the finding. The model did not learn the task; it learned the **rule** — and
it learned it well enough to reproduce the rule's blind spot. On the cases where the
event code is a lie and the note is the truth, it sided with the code three times in
four, because that is what 965 training examples overwhelmingly demonstrated.

It cost real time and produced a system strictly worse than the dictionary it
imitated, which had cost an afternoon."""),

("md", """## The previous notebook predicted this

Before any training, the dataset check in `01-before-the-training-run.ipynb` reported
seven labels that only ever appear alongside a single event code, and said:

> a model trained on these has no way to separate the label from the code — it will
> look correct on your eval and fail the first time the pair comes apart

That is exactly what happened, and it was visible for the cost of a label-crossing
table before a single GPU second was spent. The most valuable output of this whole
exercise was produced by the notebook that did no training."""),

("md", """## And the validation loss said everything was fine"""),

("code", _LOSS),

("md", """A validation loss of zero next to a judgement accuracy of zero, in the same run.

The validation set was drawn from the scenarios the model trained on — deliberately,
for early stopping — so it measured reproduction of what had been seen, and reported
it perfectly. It could not see the failure because the failure lives on scenarios it
was never given. A held-out set that shares structure with training is an instrument
that cannot fail, which is step 0 of the measurement procedure arriving at the one
place people reliably skip it."""),

("md", """## What this run actually establishes

- **Low-rank adaptation works and is cheap.** Four gigabytes of memory, minutes on a
  laptop, and a large gain on the part of the task that was learnable.
- **It learned the wrong thing anyway**, because that is what the data taught. The
  method was not the problem and no hyperparameter would have fixed it.
- **The dictionary won.** On this task, the honest system is rules plus a model for
  the remainder — which is the finding Project 3 was built to test and this confirms
  from the other direction.
- **The instrument agreed with the model.** Both were confident, both were wrong, and
  the group split is the only reason anyone found out.

The lesson to carry is the first one in this block, now with a number attached: the
gap was never *form*, which is what fine-tuning teaches. It was a judgement that
required reading a note against a policy, and no amount of showing the model correct
answers to other cases installs it."""),
]),
]
