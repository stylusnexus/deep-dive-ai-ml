# 09-electives

Labs for this block. See [CURRICULUM.md](../../CURRICULUM.md).

Start every substantial lab with [the intake sheet](../../artifacts/project-intake.md).

## 05-quantize-it-yourself

Quantize a real model at seven settings and measure size, perplexity, KL divergence and how often it
changes its answer; make GGUF files; see why Q4_K_M is not 4 bits. Part 1 needs only NumPy, part 2
needs Apple Silicon and `mlx-lm`, part 3 needs a built llama.cpp.

**The quantization one-liners**, run for real on Qwen2.5-0.5B-Instruct:

```bash
mlx_lm.convert --hf-path Qwen/Qwen2.5-0.5B-Instruct -q --q-bits 4 --q-group-size 64 --mlx-path data/quant/q4-g64
python convert_hf_to_gguf.py <model folder> --outfile m-f16.gguf --outtype f16
llama-quantize m-f16.gguf m-q4_k_m.gguf Q4_K_M
python3 scripts/measure_quantization.py --reference Qwen/Qwen2.5-0.5B-Instruct --model data/quant/q4-g64
```

The notebook starts a Python of its own for the MLX and GGUF steps, found from the `mlx_lm.convert`
command and from `GGUF_PY` and `LLAMA_CPP` if you set them, so an ordinary Python 3 kernel can run it.
Its quantized files go to `data/quant/`, which is gitignored.
