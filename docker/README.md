# Environments

Two Jupyter stacks because TensorFlow and the newest Torch/pandas don't
coexist cleanly — and because a container per block means these labs still
run in two years.

| Service | What | URL |
|---|---|---|
| `torch` | PyTorch 2.10, transformers, peft, trl | http://localhost:8888 |
| `keras` | TensorFlow 2.21 / Keras 3.15 | http://localhost:8889 |
| `pgvector` | Postgres 17 + pgvector, Block 3 RAG | `localhost:5433` |
| `mlflow` | Experiment tracking | http://localhost:5001 |

```bash
make up        # start everything
make torch     # just the torch lab
make down      # stop
```

## Before Block 7 or 8

⚠️ Docker Desktop currently has **~10.4GB** allocated. That's fine for
Postgres and MLflow, nowhere near enough to serve a quantized model in a
container. Raise it to **48–64GB** in Docker Desktop → Settings → Resources
before the serving and fine-tuning blocks. You have 128GB; the default
allocation is leaving almost all of it unused.

## Note on GPU

Containers on macOS get **CPU only** — Docker can't pass through Apple's GPU.
That's deliberate here: containers are for *reproducibility* (labs, vector
store, tracking, serving practice). Actual training runs on the host with
`torch` + MPS, where the M4 Max's 128GB unified memory does real work. Use
`scripts/check-env.sh` to confirm the host side.
