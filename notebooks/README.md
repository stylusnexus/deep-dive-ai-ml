# Notebooks

One folder per block. Each folder has its own README describing that block's labs;
this page is about running them.

## They arrive already run

Every notebook here is committed **with its executed outputs**, because a notebook
that hasn't been run is a hypothesis. So the first way to use one is to read it —
open it on GitHub or in Jupyter and the results are already there, charts included.

The second way is to run it yourself, which is the point.

## What each block needs

Blocks 5 and 7 to 9 need **nothing installed at all** — verified by running them on a
bare Python 3.14 with no virtual environment. The rest have real dependencies.

| Block | Needs | Run it with |
|---|---|---|
| 01 · Python & EDA | pandas, numpy, matplotlib, seaborn, scikit-learn | `make torch` → localhost:8888 |
| 02 · Classical ML | the above, plus torch and keras | `make torch` / `make keras` |
| 03 · Retrieval | psycopg, sentence-transformers, pgvector running — and notebook 3 needs a local model server | `make up` |
| 04 · Agentic | a local model server. Notebook 2 also needs `langgraph` | `make torch` |
| 05 · Evaluation | nothing — standard library only | any Python 3 |
| 06 · Security | a local model server, and about 15 minutes | any Python 3 |
| 07 · Fine-tuning | nothing, to read the analysis (see below) | any Python 3 |
| 08 · Deploy & APIs | nothing — standard library only | any Python 3 |
| 09 · Electives | nothing — standard library only | any Python 3 |

### The local model server

Four notebooks call a real model rather than a mock — `03/03-grounded-answers`,
both Block 4 notebooks, and `06/01-red-team-your-own-agent`. They look for an
OpenAI-compatible endpoint on `localhost:11434` then `localhost:11455`, take the
first chat model offered, and are otherwise indifferent to which model it is.
Ollama or LM Studio both work.

The recorded Block 6 run used `qwen3.8-27b-mlx-dwq` on port 11455. That notebook is
slow for an honest reason: it makes 36 real model calls — 6 to establish a baseline,
then 5 attack families across 6 cases — and the committed run took **15 minutes**.
It isn't sleeping; it's being attacked.

Blocks 1 to 3 are the ones that genuinely need the containers — see
[`../docker/README.md`](../docker/README.md).

## The exception: Block 7's training run

`07-finetuning/02-the-training-run.ipynb` **analyses** a training run rather than
performing one. The analysis reads `artifacts/finetune-results.json` and needs
nothing installed.

Actually reproducing the run needs MLX, Apple Silicon and the base model
downloaded — which is more than anyone should have to arrange in order to read a
result. If you do want to reproduce it:

```bash
python3 scripts/make_finetune_data.py    # split BY SCENARIO, not at random
python3 scripts/make_finetune_jsonl.py   # chat format for mlx_lm
mlx_lm.lora --train --data data/finetune/mlx --num-layers 8 --iters 600 ...
.venv-train/bin/python scripts/eval_finetune.py --conditions base,base+policies,tuned
```

See [`../adapters/exception-triage/README.md`](../adapters/exception-triage/README.md)
for what came out of it.

## Doing a notebook yourself

To work through one properly, clear the outputs first so you're not reading the
answers:

```bash
jupyter nbconvert --clear-output --inplace notebooks/05-evaluation/01-*.ipynb
```

Then run it cell by cell. `git checkout` that file to get the committed results back.

## Running one end to end

```bash
jupyter nbconvert --to notebook --execute --inplace \
  --ExecutePreprocessor.timeout=600 notebooks/01-python-eda/01-first-contact.ipynb
```

## The trap

Notebooks are **generated** from `scripts/content/*_notebooks.py`, and rebuilding one
strips its executed outputs:

```bash
python3 scripts/build_notebooks.py block1_notebooks   # outputs now gone
```

Re-execute after every rebuild or you commit an unrun notebook. `make notebooks`
checks for exactly this and fails if any notebook is missing its outputs.

Never hand-edit a `.ipynb` to fix prose — edit the content module and rebuild.
