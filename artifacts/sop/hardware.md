# Hardware — can I run this locally?

Run top to bottom. Most people fail at step 3 and spend their time on step 2.

## Things to know

> **Capacity is a hard wall; bandwidth is only a slope.**
> A model that does not fit does not run at any speed. A model that fits but
> runs slowly still runs. Check that it fits before comparing tokens per second.

> **What blocks you is usually neither memory nor speed — it is library support.**
> CUDA-only kernels do not run on Metal regardless of how much memory you have.
> Check the library before you check the chip.

> **A heavily quantised large model beats a precise small one.**
> A 4-bit 70B almost always outperforms a 16-bit 13B of similar file size.
> Prefer the bigger model, more compressed.

---

## 0 · Does it need to be local at all?
- [ ] A real reason exists: privacy, cost at volume, or offline operation
- [ ] Preference is not a reason — an API call is frequently cheaper than the electricity
- [ ] Cost compared honestly at *your* volume, not at demo volume

## 1 · Will it fit? ☠
- [ ] ☠ Weights computed: parameters × bits ÷ 8 (70B at 4-bit ≈ 35GB)
- [ ] ☠ For a mixture-of-experts model, **total** parameters used for this sum, not the
      activated count — every expert stays resident because the router may pick any of
      them next. Active parameters decide roughly how fast a token is, not whether it fits
- [ ] ☠ KV cache budgeted — grows with context and batch, and is what usually exhausts memory
- [ ] Runtime and activation overhead added (a few GB)
- [ ] Compared against **addressable** memory, not total system memory
  - NVIDIA: VRAM only. Spilling to system RAM collapses throughput
  - Apple Silicon: the wired limit, ~75% of RAM by default and adjustable
- [ ] If it does not fit: quantise further, or take a smaller model — in that order

## 2 · Is it supported? ☠
- [ ] ☠ The *library* checked, not the chip — this is the step that actually blocks people
- [ ] No CUDA-only kernels in the path (several quantisation and attention implementations)
- [ ] For PyTorch on Apple Silicon: fallback-to-error enabled during development, so an
      unimplemented operation announces itself instead of silently running on CPU
- [ ] Containers understood to be CPU-only on macOS — reproducibility, not training

## 3 · Is it fast enough for the job?
- [ ] For a mixture-of-experts model, remembered that skipping experts removes arithmetic
      and not bytes — it does not help a decode that was already memory-bound
- [ ] Decode speed measured, not quoted — vendor figures are usually decode-only
- [ ] Time-to-first-token measured with a *realistic* prompt length, since prefill dominates it
- [ ] Below ~10 tok/s interactive use is unpleasant; batch work tolerates much less
- [ ] Prefix-KV reuse available if this is a multi-turn agent loop — usually the biggest lever
- [ ] Speculative decoding considered if one user is waiting rather than a thousand — it spends
      spare compute to cut latency, so it wins at low concurrency and does nothing for a server
      already compute-saturated by batching. It costs no quality: the output distribution is unchanged

## 4 · Before concluding "it cannot run here"
- [ ] Which artifact did you actually test? A load failure in one build format is not a
      fact about the model — another build of the same weights may load fine
- [ ] Was anything truncated? A too-small output budget manufactures false conclusions
- [ ] Was the documented control mechanism used, or the folklore one?

## Quick reference

| Setup | Good for | Ceiling |
|---|---|---|
| Apple Silicon, high memory | Large quantised models, inference, LoRA on 7B–13B | Bandwidth, and library gaps |
| Consumer NVIDIA 8–24GB | Small models, real training, full ecosystem | Capacity — a hard wall |
| Rented cloud GPU | Anything big and fast | Hourly cost |
| No GPU | Embeddings, classical ML, API work | Nothing — most of Block 2 runs on CPU |

## Smells

- Model loads fine, then fails on a long document → the KV cache, not the weights
- Correct results at a twentieth of expected speed on Apple Silicon → silent CPU fallback for an unimplemented operation
- Fast in development, unusably slow in production → bursty traffic means most requests are cold starts
- "It cannot run here" after one failed load → which build format did you actually test? Another may work
- Vendor quotes a large speed multiple → ask which phase it measures, and whether that phase is your bottleneck
