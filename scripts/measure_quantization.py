#!/usr/bin/env python3
"""Measure what quantizing a model cost, with numbers that do not depend on how busy
the machine is.

A speed figure moves with whatever else the computer is doing. These do not:

  size           bytes on disk, and bits per weight (size * 8 / the reference's weights)
  perplexity     how surprised the model is by a text it has not been tuned on
  KL divergence  how far the quantized model's whole next-token distribution has
                 moved from the full-precision model's, averaged over every position.
                 Perplexity can stay flat while answers change; KL moves first.
  top-1 agreement  how often the two models would pick the same next token

The reference is the full-precision model. The text is a folder of documents; by
default the course's own corpus, which no model here was calibrated on.

Needs an interpreter with mlx-lm installed (`pip install mlx-lm`, Apple Silicon):

    python3 scripts/measure_quantization.py --reference Qwen/Qwen2.5-0.5B-Instruct \\
        --model data/quant/q4-g64 --model data/quant/q3-g64

What it cannot tell you: perplexity and KL on one folder of documents say how much the
distribution moved on that text, not whether your task got worse. Check your own task
before you trust a quantization (see the benchmarking lesson).
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys

import mlx.core as mx
from mlx.utils import tree_flatten
from mlx_lm import load

ROOT = pathlib.Path(__file__).resolve().parent.parent


def dir_bytes(model_path: str) -> int | None:
    """Size of the weight files. None for a Hugging Face id that is not a folder here."""
    p = pathlib.Path(model_path)
    if not p.is_dir():
        from huggingface_hub import snapshot_download
        p = pathlib.Path(snapshot_download(model_path, allow_patterns=["*.safetensors", "*.json"]))
    return sum(f.stat().st_size for f in p.glob("*.safetensors"))


def n_weights(model) -> int:
    return sum(v.size for _, v in tree_flatten(model.parameters()))


def windows(tokenizer, text_dir: pathlib.Path, window: int, count: int):
    text = "\n\n".join(f.read_text() for f in sorted(text_dir.glob("*.md")))
    ids = tokenizer.encode(text)
    need = window * count
    if len(ids) < need:
        count = max(1, len(ids) // window)
    return [mx.array(ids[i * window:(i + 1) * window]) for i in range(count)]


def log_probs(model, ids):
    logits = model(ids[None])[0].astype(mx.float32)          # (window, vocab)
    return logits - mx.logsumexp(logits, axis=-1, keepdims=True)


def evaluate(ref, cand, wins):
    nll_ref = nll_c = kl = agree = 0.0
    n = 0
    for w in wins:
        lr, lc = log_probs(ref, w)[:-1], log_probs(cand, w)[:-1]   # predict token t+1 from <= t
        tgt = w[1:]
        idx = mx.arange(tgt.shape[0])
        pr = mx.exp(lr)
        kl_t = (pr * (lr - lc)).sum(axis=-1)
        a = (mx.argmax(lr, -1) == mx.argmax(lc, -1)).astype(mx.float32)
        mx.eval(kl_t, a, lr[idx, tgt], lc[idx, tgt])
        nll_ref += -float(lr[idx, tgt].sum())
        nll_c += -float(lc[idx, tgt].sum())
        kl += float(kl_t.sum())
        agree += float(a.sum())
        n += tgt.shape[0]
    return {"tokens": n, "ppl_ref": math.exp(nll_ref / n), "ppl": math.exp(nll_c / n),
            "kl": kl / n, "top1_agree": agree / n}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--reference", required=True, help="full-precision model, folder or Hugging Face id")
    ap.add_argument("--model", action="append", required=True, help="quantized model; repeatable")
    ap.add_argument("--text-dir", default=str(ROOT / "data" / "corpus"))
    ap.add_argument("--window", type=int, default=512)
    ap.add_argument("--windows", type=int, default=8)
    ap.add_argument("--json")
    ap.add_argument("--device", choices=["gpu", "cpu"], default="gpu",
                    help="cpu keeps a shared machine's GPU free; the numbers match to the digits shown")
    a = ap.parse_args()
    if a.device == "cpu":
        mx.set_default_device(mx.cpu)

    ref, tok = load(a.reference)
    wins = windows(tok, pathlib.Path(a.text_dir), a.window, a.windows)
    ref_w = n_weights(ref)
    ref_bytes = dir_bytes(a.reference)
    rows = [{"model": "reference", "bytes": ref_bytes, "bits_per_weight": ref_bytes * 8 / ref_w,
             "kl": 0.0, "top1_agree": 1.0, **{k: v for k, v in evaluate(ref, ref, wins).items()
                                               if k in ("ppl", "ppl_ref", "tokens")}}]
    for m in a.model:
        cand, _ = load(m)
        b = dir_bytes(m)
        rows.append({"model": m, "bytes": b, "bits_per_weight": b * 8 / ref_w, **evaluate(ref, cand, wins)})
        del cand

    print(f"device: {a.device}. {len(wins)} windows of {a.window} tokens = {rows[0]['tokens']} scored tokens; "
          f"reference holds {ref_w:,} weights\n")
    print(f"{'model':<28}{'MB':>8}{'bits/w':>8}{'perplexity':>12}{'KL':>9}{'top-1 same':>12}")
    for r in rows:
        name = pathlib.Path(r["model"]).name if r["model"] != "reference" else "16-bit reference"
        print(f"{name:<28}{r['bytes'] / 1e6:>8.0f}{r['bits_per_weight']:>8.2f}{r['ppl']:>12.3f}"
              f"{r['kl']:>9.4f}{r['top1_agree']:>11.1%}")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(rows, indent=2))


if __name__ == "__main__":
    sys.exit(main())
