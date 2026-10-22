OUTDIR = "notebooks/09-electives"

_INTRO = '''# Quantize it yourself, and measure what it cost

Quantization stores each weight in fewer bits. Everyone says the loss is small. This
notebook lets you check, on a real model, on your own machine, with numbers that do not
move when something else is using the computer.

You will:

1. **Build a quantizer in 15 lines of NumPy** and see where the error comes from: bits,
   group size, and a single outlier weight.
2. **Quantize a real model** (Qwen2.5-0.5B-Instruct) at seven plain settings and one mixed
   recipe, one command each, and measure size, perplexity, KL divergence and how often it picks a different
   next word.
3. **Make GGUF files** with llama.cpp and see why `Q4_K_M` is not 4 bits all the way down.

**Needs:** an Apple Silicon Mac with `mlx-lm` (`pip install mlx-lm`) for part 2, and a
llama.cpp checkout with `llama-quantize` built for part 3. Part 1 needs only NumPy.
A couple of minutes once the model is downloaded. Run the cells top to bottom: the NumPy
parts share one random generator, so running a cell on its own gives different numbers.

**What this cannot tell you:** one 0.5-billion-parameter model on one text. Rerun it with
the model you actually plan to use before you trust any conclusion here.'''

_QUANTIZER = '''import numpy as np

rng = np.random.default_rng(7)

def quantize(w, bits, group):
    """Round-to-nearest, affine. One scale and one offset per `group` weights in a row.
    This is what `mlx_lm.convert -q` does, minus the packing."""
    rows, cols = w.shape
    g = w.reshape(rows, cols // group, group)
    lo, hi = g.min(-1, keepdims=True), g.max(-1, keepdims=True)
    levels = 2 ** bits - 1
    scale = np.maximum(hi - lo, 1e-12) / levels
    q = np.round((g - lo) / scale)              # the integers 0..levels: what gets stored
    return (q * scale + lo).reshape(rows, cols)

def rel_err(w, wq):
    return np.linalg.norm(w - wq) / np.linalg.norm(w)

# Weights that look like a trained layer: mostly small, a few large.
W = rng.standard_normal((512, 1024)) * 0.02
outliers = rng.random(W.shape) < 0.001
W[outliers] *= 15
print(f"{W.size:,} weights, {outliers.sum()} of them 15x larger than the rest")'''

_BITS = '''print(f"{'bits':>5} {'relative error':>16} {'vs one more bit':>17}")
prev = None
for bits in (8, 6, 4, 3, 2):
    e = rel_err(W, quantize(W, bits, 64))
    note = "" if prev is None else f"x{e / prev:.2f} over {prev_bits} bits"
    print(f"{bits:>5} {e:>16.4f} {note:>17}")
    prev, prev_bits = e, bits'''

_GROUPS = '''# Every group stores a 16-bit scale and a 16-bit offset, so a smaller group is more
# accurate and costs more bits per weight.
print(f"{'group':>6} {'relative error':>16} {'bits per weight':>17}")
for group in (16, 32, 64, 128, 256, 1024):
    e = rel_err(W, quantize(W, 4, group))
    print(f"{group:>6} {e:>16.4f} {4 + 32 / group:>17.2f}")'''

_OUTLIER = '''# One large weight stretches the range its whole group has to cover.
normal = rng.standard_normal(64) * 0.02
with_outlier = normal.copy()
with_outlier[0] = 0.4

for name, x in (("no outlier", normal), ("one outlier", with_outlier)):
    xq = quantize(x[None, :], 4, 64)[0]
    step = (x.max() - x.min()) / 15
    others = np.linalg.norm(x[1:] - xq[1:]) / np.linalg.norm(x[1:])
    print(f"{name:<12} step between levels {step:.4f}   error on the other 63 weights {others:.1%}")'''

_AWQ = '''# The idea behind AWQ, in 12 lines. A few input channels carry much larger activations,
# so rounding error on THEIR weights is multiplied by big numbers. Scale those weights
# up before quantizing (and the activations down by the same amount) and they are
# rounded more finely, at no cost to the maths: (x / s) @ (W * s).T equals x @ W.T.
n_in = 1024
X = rng.standard_normal((2048, n_in))
salient = rng.choice(n_in, 10, replace=False)
X[:, salient] *= 20                          # 1% of channels are loud
Wt = rng.standard_normal((512, n_in)) * 0.02
Y = X @ Wt.T

def output_error(Wq, scale=None):
    x = X if scale is None else X / scale
    return np.linalg.norm(Y - x @ Wq.T) / np.linalg.norm(Y)

print(f"plain rounding, 3-bit: output error {output_error(quantize(Wt, 3, 128)):.4f}")
act = np.abs(X).mean(0)
for alpha in (0.25, 0.5, 0.75):
    s = act ** alpha
    s /= s.mean()
    print(f"scaled by activation**{alpha:<4}  : output error {output_error(quantize(Wt * s, 3, 128), s):.4f}")'''

_ENV = '''import json, os, pathlib, shutil, subprocess, sys

ROOT = pathlib.Path.cwd()
while not (ROOT / "artifacts").exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
WORK = ROOT / "data" / "quant"          # gitignored; safetensors and gguf files are large
WORK.mkdir(parents=True, exist_ok=True)

def interpreter_with(module, cli):
    """A Python that can import `module`: this one, or the one behind a CLI tool."""
    try:
        __import__(module)
        return sys.executable
    except ImportError:
        pass
    exe = shutil.which(cli)
    if exe:
        first = open(exe).readline()
        if first.startswith("#!"):
            return first[2:].strip()
    raise SystemExit(f"Need {module}. Try:  pip install {module.replace('_', '-')}")

MLX_PY = interpreter_with("mlx_lm", "mlx_lm.convert")
REF = "Qwen/Qwen2.5-0.5B-Instruct"
print("python with mlx-lm:", MLX_PY.replace(str(pathlib.Path.home()), "~"))
print("reference model   :", REF)
print("work folder       :", WORK.relative_to(ROOT))'''

_CONVERT = '''# One command per setting. This is the one-liner:
#   mlx_lm.convert --hf-path Qwen/Qwen2.5-0.5B-Instruct -q --q-bits 4 --q-group-size 64 --mlx-path data/quant/q4-g64
SETTINGS = [("q8-g64", 8, 64), ("q6-g64", 6, 64), ("q4-g32", 4, 32), ("q4-g64", 4, 64),
            ("q4-g128", 4, 128), ("q3-g64", 3, 64), ("q2-g64", 2, 64)]

def convert(name, bits, group, predicate=None):
    out = WORK / name
    if out.exists():
        q = json.loads((out / "config.json").read_text()).get("quantization", {})
        return f"{name:<10} reused ({q.get('bits')}-bit, group size {q.get('group_size')})"
    cmd = [MLX_PY, "-m", "mlx_lm.convert", "--hf-path", REF, "-q", "--q-bits", str(bits),
           "--q-group-size", str(group), "--mlx-path", str(out)]
    if predicate:
        cmd += ["--quant-predicate", predicate]
    run = subprocess.run(cmd, capture_output=True, text=True)
    line = [l for l in (run.stderr + run.stdout).splitlines() if "bits per weight" in l]
    return f"{name:<10} {line[-1].split('] ')[-1] if line else run.stderr[-200:]}"

for name, bits, group in SETTINGS:
    print(convert(name, bits, group))
# A mixed recipe: most layers at 4 bits, a chosen few at 6 (v_proj and down_proj in the
# first and last eighth of the layers and every third in between, plus the output head).
print(convert("mixed-4-6", 4, 64, predicate="mixed_4_6"))'''

_MEASURE = '''# The measurement is scripts/measure_quantization.py, so you can run it on any model.
names = [n for n, _, _ in SETTINGS] + ["mixed-4-6"]
# The scoring takes about a minute on a GPU, so a finished result is reused. Delete
# data/quant/results.json to measure again.
results = WORK / "results.json"
if results.exists():
    print("reusing", results.relative_to(ROOT), "from an earlier run of the script below")
cmd = [MLX_PY, str(ROOT / "scripts" / "measure_quantization.py"), "--reference", REF,
       "--json", str(results)]
for n in names:
    cmd += ["--model", str(WORK / n)]
if not results.exists():
    run = subprocess.run(cmd, capture_output=True, text=True)
    print("\\n".join(l for l in run.stdout.splitlines() if l.strip()))
    if run.returncode:
        print(run.stderr[-800:])
else:
    rows = json.loads(results.read_text())
    print(f"{'model':<28}{'MB':>8}{'bits/w':>8}{'perplexity':>12}{'KL':>9}{'top-1 same':>12}")
    for r in rows:
        name = "16-bit reference" if r["model"] == "reference" else pathlib.Path(r["model"]).name
        print(f"{name:<28}{r['bytes'] / 1e6:>8.0f}{r['bits_per_weight']:>8.2f}{r['ppl']:>12.3f}"
              f"{r['kl']:>9.4f}{r['top1_agree']:>11.1%}")'''

_READ = '''# Computed from the table above rather than typed in, so it cannot disagree with it.
R = {pathlib.Path(r["model"]).name: r for r in json.loads((WORK / "results.json").read_text())
     if r["model"] != "reference"}

def row(n):
    r = R[n]
    return f"{n}: {r['bits_per_weight']:.2f} bits/weight, KL {r['kl']:.3f}, same top-1 {r['top1_agree']:.0%}"

print("Each step down in bits, and the same step per bit removed:")
for a, b, bits in (("q8-g64", "q6-g64", 2), ("q6-g64", "q4-g64", 2), ("q4-g64", "q3-g64", 1), ("q3-g64", "q2-g64", 1)):
    k = R[b]["kl"] / R[a]["kl"]
    print(f"  {a} -> {b}: KL x{k:.1f} over {bits} bit(s), x{k ** (1 / bits):.1f} per bit")
print()
print("Same 4 bits, different group size:")
for n in ("q4-g32", "q4-g64", "q4-g128"):
    print("  ", row(n))
print()
print("A mixed recipe against its plain neighbours:")
for n in ("q4-g64", "mixed-4-6", "q6-g64"):
    print("  ", row(n))'''

_GGUF_ENV = '''# Part 3 needs llama.cpp. Point LLAMA_CPP at a checkout that has been built, or put
# llama-quantize on your PATH. GGUF_PY is a Python that has gguf, torch and transformers.
LLAMA = pathlib.Path(os.environ.get("LLAMA_CPP", pathlib.Path.home() / ".unsloth" / "llama.cpp"))
LQ = shutil.which("llama-quantize") or str(LLAMA / "build" / "bin" / "llama-quantize")
CONVERT = LLAMA / "convert_hf_to_gguf.py"
_candidates = [os.environ.get("GGUF_PY"), sys.executable,
               str(pathlib.Path.home() / ".unsloth" / "studio" / "unsloth_studio" / "bin" / "python")]

def _can_convert(py):
    ok = py and pathlib.Path(py).exists()
    return ok and subprocess.run([py, "-c", "import gguf, torch, transformers"],
                                 capture_output=True).returncode == 0

GGUF_PY = next((p for p in _candidates if _can_convert(p)), None)
if GGUF_PY is None:
    raise SystemExit("Need a Python with gguf, torch and transformers. Set GGUF_PY to one.")
HF_DIR = subprocess.run(
    [MLX_PY, "-c", "from huggingface_hub import snapshot_download as s; print(s('%s'))" % REF],
    capture_output=True, text=True).stdout.strip().splitlines()[-1]
if not (pathlib.Path(LQ).exists() and CONVERT.exists()):
    raise SystemExit(f"Need llama.cpp: a checkout with convert_hf_to_gguf.py and a built llama-quantize. "
                     f"Set LLAMA_CPP to it (looked for {LQ} and {CONVERT}).")
print("llama-quantize:", LQ.replace(str(pathlib.Path.home()), "~"))
print("converter     :", str(CONVERT).replace(str(pathlib.Path.home()), "~"))
print("model folder  :", HF_DIR.replace(str(pathlib.Path.home()), "~"))'''

_GGUF_RUN = '''# The two lines:
#   python convert_hf_to_gguf.py <model folder> --outfile m-f16.gguf --outtype f16
#   llama-quantize m-f16.gguf m-q4_k_m.gguf Q4_K_M
f16 = WORK / "qwen05-f16.gguf"
if not f16.exists():
    subprocess.run([GGUF_PY, str(CONVERT), HF_DIR, "--outfile", str(f16), "--outtype", "f16"],
                   capture_output=True, text=True, check=True)
print(f"{'type':<8} {'MB':>8} {'bits/weight':>12}")
print(f"{'f16':<8} {f16.stat().st_size / 1e6:>8.0f} {16.0:>12.2f}")
for t in ("Q8_0", "Q4_K_M", "Q3_K_M", "Q2_K"):
    out = WORK / f"qwen05-{t}.gguf"
    run = subprocess.run([LQ, str(f16), str(out), t], capture_output=True, text=True)
    bpw = [l for l in run.stderr.splitlines() if "quant size" in l][-1].split("(")[-1].split(" BPW")[0]
    print(f"{t:<8} {out.stat().st_size / 1e6:>8.0f} {float(bpw):>12.2f}")'''

_GGUF_TENSORS = '''# "Q4_K_M" names a mixture, not a uniform 4 bits. Look inside the file: what type is each
# tensor, and is its row length a multiple of 256 (the block size K-quants work in)?
code = ("from gguf import GGUFReader; import json, sys\\n"
        "rows = []\\n"
        "for t in GGUFReader(sys.argv[1]).tensors:\\n"
        "    rows.append([t.name, int(t.shape[0]), t.tensor_type.name, int(t.n_elements)])\\n"
        "print(json.dumps(rows))")
raw = subprocess.run([GGUF_PY, "-c", code, str(WORK / "qwen05-Q4_K_M.gguf")], capture_output=True, text=True)
rows = json.loads(raw.stdout.strip().splitlines()[-1])
total = sum(n for *_, n in rows)
share = {}
for name, row_len, typ, n in rows:
    if typ == "F32":
        continue
    key = (row_len % 256 == 0, typ)
    share[key] = share.get(key, 0) + n
print(f"{'row length a multiple of 256?':<30} {'type':<6} {'share of weights':>17}")
for (fits, typ), n in sorted(share.items(), key=lambda kv: (not kv[0][0], -kv[1])):
    print(f"{'yes' if fits else 'no':<30} {typ:<6} {n / total:>17.1%}")
print()
print("row lengths in this model:", sorted({r[1] for r in rows if r[2] != "F32"}),
      "-> 896 % 256 =", 896 % 256, "; 4864 % 256 =", 4864 % 256)'''


_GGUF_REQUANT = '''# Never quantize from a file that is already quantized. The tool refuses unless you insist.
run = subprocess.run([LQ, str(WORK / "qwen05-Q8_0.gguf"), str(WORK / "qwen05-rq.gguf"), "Q4_K_M"],
                     capture_output=True, text=True)
msg = [l for l in run.stderr.replace("\\r", "\\n").splitlines() if "requantizing" in l][-1]
print(msg.split("llama_model_quantize: ")[-1])
(WORK / "qwen05-rq.gguf").unlink(missing_ok=True)

help_text = subprocess.run([LQ, "--help"], capture_output=True, text=True)
text = help_text.stdout + help_text.stderr
i = text.index("\\n  --allow-requantize") + 1
print()
print(text[i:i + 420].replace("\\n  ", "\\n"))'''

_WRAP = '''## Before you ship a quantization

- [ ] Started from the 16-bit original, never from an already-quantized file
- [ ] Compared at equal bits per weight, not equal "4-bit" labels
- [ ] Measured KL divergence and how often the top choice changes, not perplexity alone
- [ ] Held out text the quantizer never saw, in the domain you will use it in
- [ ] Ran your own task, because a small average shift can hide a different set of wrong answers
- [ ] Wrote down the tool and its version, the base model revision, the settings and any calibration data

**GGUF quality is not measured here.** This llama.cpp build has no `llama-perplexity`.
llama.cpp documents a KL-divergence workflow for it: run `llama-perplexity` on the 16-bit
file with `--kl-divergence-base <file>` to save its outputs, then on each quantized file with
both `--kl-divergence-base <file>` and `--kl-divergence`.

**Next:** the *Quantization Recipes* lesson covers what to do when plain rounding at the
bit width you want is not good enough: GPTQ, AWQ, DWQ, importance matrices and where to
find them already made.'''

_CELLS = [
    ("md", _INTRO),
    ("md", "## Part 1: a quantizer in NumPy\n\nThe same rounding, group by group, that a real tool does. No model, no download."),
    ("code", _QUANTIZER),
    ("md", "**Each bit you remove roughly doubles the error.** Going from 8 to 6 bits is two steps, so about four times; each step below that is about two."),
    ("code", _BITS),
    ("md", "**Smaller groups are more accurate and cost more bits**, because every group stores its own scale and offset. That is why the \"4-bit\" models in this course are really about 4.5 bits per weight."),
    ("code", _GROUPS),
    ("md", "**One outlier hurts everyone in its group.** The scale has to stretch to reach it, so the step between levels grows and the ordinary weights are rounded coarsely. Outliers are why plain rounding struggles, and why recipes exist."),
    ("code", _OUTLIER),
    ("md", "**Recipes protect the weights that matter.** AWQ's observation is that the important weights are the ones fed by large activations. This is its core move in a dozen lines. Real AWQ searches for the best scale per channel on calibration data. This uses a fixed rule, so it shows the mechanism and not the result, and note that the last setting is *worse* than plain rounding: a bad scale hurts, which is why the search exists."),
    ("code", _AWQ),
    ("md", "## Part 2: a real model\n\nThe reference is the full 16-bit model. Everything else is compared to it."),
    ("code", _ENV),
    ("code", _CONVERT),
    ("md", "Now measure. `scripts/measure_quantization.py` reports, for each model: size, perplexity on the course's own corpus, **KL divergence** from the 16-bit model (how far the whole next-word distribution moved, averaged over every position) and **top-1 same** (how often both would pick the same next word). None of these depend on how busy the machine is, which a speed figure would."),
    ("code", _MEASURE),
    ("code", _READ),
    ("md", "**Reading it.** Compare rows at similar *bits per weight*, not similar labels. Watch KL and top-1 before perplexity: perplexity can stay nearly flat while the model starts choosing different words. And remember what this is: one small model, one text, and a distribution measure. It says how far the model moved, not whether *your task* got worse."),
    ("md", "## Part 3: GGUF with llama.cpp"),
    ("code", _GGUF_ENV),
    ("code", _GGUF_RUN),
    ("code", _GGUF_TENSORS),
    ("md", "**Q4_K_M is a mixture, and for this model most of it is not 4-bit.** K-quants store weights in blocks of 256 along each row. Where a row's length is a multiple of 256 the file uses `Q4_K` or `Q6_K`. Where it is not, as with this model's hidden size of 896 (3.5 blocks), llama.cpp falls back to older block types, `Q5_0` and `Q8_0`, which cost more bits. That is why the file is 6.35 bits per weight rather than the 4.9 llama.cpp lists for an 8-billion-parameter model, whose dimensions are multiples of 256. The table above is the evidence; the fallback itself is our reading of the pattern and we did not read llama.cpp's code. The lesson is to read bits per weight off the file, never off the label."),
    ("code", _GGUF_REQUANT),
    ("md", _WRAP),
]

NOTEBOOKS = [("05-quantize-it-yourself.ipynb", _CELLS)]
