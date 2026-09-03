OUTDIR = "notebooks/07-finetuning"

_SETUP = '''import json, math, re, random
from collections import Counter, defaultdict
from pathlib import Path

random.seed(7)
ROOT = Path.cwd()
while not (ROOT / "data" / "exceptions").exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

RECORDS = json.loads((ROOT / "data" / "exceptions" / "exceptions.json").read_text())
print(f"{len(RECORDS)} labelled records — a real dataset, not a toy one")
print(f"fields: {sorted(RECORDS[0])}")'''


_BALANCE = '''labels = Counter(r["gold_action"] for r in RECORDS)
total = sum(labels.values())
print(f"{'label':<28} {'n':>4}  {'share':>7}")
for k, v in labels.most_common():
    bar = "#" * int(40 * v / max(labels.values()))
    print(f"{k:<28} {v:>4}  {100*v/total:>6.1f}%  {bar}")

print(f"\\nmajority-class baseline: {100*max(labels.values())/total:.1f}%")
print(f"labels seen fewer than 5 times: "
      f"{[k for k, v in labels.items() if v < 5]}")'''


_COVERAGE = '''# Coverage is not volume. A label with 200 examples of one situation teaches less
# than 20 across ten. Cross the label against the situation that produced it.
grid = defaultdict(Counter)
for r in RECORDS:
    grid[r["gold_action"]][r["event_code"]] += 1

print(f"{'label':<28} {'n':>4} {'distinct events':>16}  events")
for label, events in sorted(grid.items(), key=lambda kv: -sum(kv[1].values())):
    n = sum(events.values())
    print(f"{label:<28} {n:>4} {len(events):>16}  "
          f"{', '.join(f'{e}:{c}' for e, c in events.most_common(3))}")

thin = [l for l, e in grid.items() if len(e) == 1]
print(f"\\nlabels that only ever appear with ONE event code: {thin}")
print("a model trained on these has no way to separate the label from the code —")
print("it will look correct on your eval and fail the first time the pair comes apart")'''


_CONSISTENCY = '''# Contradiction check: the same situation, labelled two different ways.
# These do not average out during training. They teach that both are acceptable.
by_situation = defaultdict(set)
for r in RECORDS:
    key = (r["event_code"], r["attempt"], r["customer_tier"])
    by_situation[key].add(r["gold_action"])

conflicts = {k: v for k, v in by_situation.items() if len(v) > 1}
print(f"situations with more than one label: {len(conflicts)} of {len(by_situation)}")
for k, v in list(conflicts.items())[:6]:
    print(f"  {k[0]:<22} attempt={str(k[1]):<5} {k[2]:<9} -> {sorted(v)}")

print("\\nnot all of these are errors — a note may legitimately decide between them.")
print("but each one is a case where the model cannot learn the rule from the fields alone,")
print("so if the note is what decides it, the note has to be in the training input.")'''


_DEDUP = '''def shingles(text, k=4):
    words = re.findall(r"[a-z]+", (text or "").lower())
    return {tuple(words[i:i+k]) for i in range(max(0, len(words) - k + 1))}

def jaccard(a, b):
    return len(a & b) / len(a | b) if (a | b) else 0.0

sh = {r["exception_id"]: shingles(r["note"]) for r in RECORDS}
ids = [r["exception_id"] for r in RECORDS]

pairs = []
for i, a in enumerate(ids):
    for b in ids[i+1:]:
        s = jaccard(sh[a], sh[b])
        if s >= 0.6:
            pairs.append((s, a, b))
pairs.sort(reverse=True)

print(f"near-duplicate pairs at Jaccard >= 0.6: {len(pairs)}")
for s, a, b in pairs[:5]:
    na = next(r["note"] for r in RECORDS if r["exception_id"] == a)
    nb = next(r["note"] for r in RECORDS if r["exception_id"] == b)
    print(f"  {s:.2f}  {a} / {b}")
    print(f"        {na[:70]}")
    print(f"        {nb[:70]}")'''


_LEAK = '''# What a random split does with those duplicates, and what it costs you.
random.seed(7)
order = ids[:]
random.shuffle(order)
cut = int(0.8 * len(order))
train, test = set(order[:cut]), set(order[cut:])

split_pairs = [(s, a, b) for s, a, b in pairs
               if (a in train) != (b in train)]
print(f"near-duplicate pairs SPLIT across train and test: {len(split_pairs)}")
print(f"test items with a near-twin in training          : "
      f"{len({b if b in test else a for _, a, b in split_pairs})} of {len(test)}")

leaked = len({b if b in test else a for _, a, b in split_pairs})
print(f"\\n{100*leaked/len(test):.1f}% of the test set has a near-twin the model trained on.")
print("that is not a score, it is the share of the test set that cannot be evidence")
print("the split was done correctly — the duplication was already in the data,")
print("which is why splitting properly does not protect you from it")'''


_MEMORY = '''def training_memory(params_b, bits=16, batch=8, seq=2048, layers=32, hidden=4096,
                    optimiser_states=2, checkpointing=False):
    """Bytes resident during training, in gigabytes. Approximate and honest about it:
    the point is the proportions and how the levers move them, not a exact figure."""
    p = params_b * 1e9
    w = p * bits / 8
    g = p * bits / 8
    o = p * optimiser_states * 4                 # optimiser state is kept in fp32
    a = batch * seq * hidden * layers * (bits / 8) * 2
    if checkpointing:
        a = a / math.sqrt(layers) * 2            # keep ~sqrt(L) checkpoints, recompute rest
    return {k: v / 1e9 for k, v in
            dict(weights=w, gradients=g, optimiser=o, activations=a).items()}

def show(label, m):
    tot = sum(m.values())
    parts = "  ".join(f"{k} {v:6.1f}" for k, v in m.items())
    print(f"  {label:<34} {parts}   TOTAL {tot:6.1f} GB")

print("A 7B model, batch 8, sequence 2048 — gigabytes resident\\n")
show("full fine-tune, fp32 throughout", training_memory(7, bits=32))
show("+ mixed precision (16-bit weights)", training_memory(7, bits=16))
show("+ gradient accumulation (batch 2)", training_memory(7, bits=16, batch=2))
show("+ gradient checkpointing", training_memory(7, bits=16, batch=2, checkpointing=True))'''


_LORA = '''# LoRA does not reduce the weights. It removes gradients and optimiser state for
# almost all of them, which is where the memory actually was.
def lora_memory(params_b, rank=16, bits=16, batch=2, seq=2048, layers=32, hidden=4096):
    p = params_b * 1e9
    trainable = layers * 4 * 2 * rank * hidden      # two matrices per projection
    w = p * bits / 8
    g = trainable * bits / 8
    o = trainable * 2 * 4
    a = batch * seq * hidden * layers * (bits / 8) * 2 / math.sqrt(layers) * 2
    return trainable, {k: v/1e9 for k, v in
                       dict(weights=w, gradients=g, optimiser=o, activations=a).items()}

for rank in (8, 16, 64):
    trainable, m = lora_memory(7, rank=rank)
    print(f"  rank {rank:>3}: {trainable/1e6:6.1f}M trainable "
          f"({100*trainable/7e9:.3f}% of the model)   TOTAL {sum(m.values()):5.1f} GB")

full = sum(training_memory(7, bits=16, batch=2, checkpointing=True).values())
_, lora16 = lora_memory(7, rank=16)
print(f"\\n  best full fine-tune above : {full:5.1f} GB")
print(f"  LoRA at rank 16           : {sum(lora16.values()):5.1f} GB")
print(f"  the difference is almost entirely gradients and optimiser state, not weights")'''


NOTEBOOKS = [
("01-before-the-training-run.ipynb", [

("md", """# 07 · Before the Training Run

Block 7 argues that most fine-tuning projects should stop before they start, and that
the ones that proceed are decided by the dataset rather than by the method. This
notebook is the work you do *before* spending a GPU hour: check whether the data can
teach anything, then check whether the run will fit.

Neither half needs a GPU, an API key or a network. The training run itself is still
open in the curriculum, and it should be — a notebook that claims a fine-tune it did
not perform would be exactly the kind of unrun hypothesis this repository refuses to
commit.

The dataset is the delivery-exception corpus from Project 3: 132 real labelled
records, generated by a seeded script but with the structure and the awkwardness of
something collected rather than designed."""),

("code", _SETUP),

("md", """## 1 · What the label distribution already tells you

Before anything else: what would a model learn if it learned nothing but the prior?"""),

("code", _BALANCE),

("md", """Two readings. The majority-class number is the floor any fine-tune has to beat to
have done anything at all — the same baseline discipline as Block 2, arriving before
a single training step.

The labels appearing fewer than five times are the ones a training run will quietly
drop. They will not appear in a random validation split often enough to be measured,
so the model will get them wrong and the score will not notice."""),

("md", """## 2 · Coverage, which is not volume

The lesson's claim is that twenty examples across ten situations beat two hundred
across two. Here is why that is checkable rather than a slogan: cross each label
against the event code that produced it."""),

("code", _COVERAGE),

("md", """A label that only ever appears alongside one event code is not a label the model can
learn independently — it will learn the event code instead, and the two are
indistinguishable on your evaluation because your evaluation has the same structure.
The failure arrives the first time the pair comes apart in production."""),

("md", """## 3 · Contradictions, which do not average out

Two examples of the same situation with different labels teach that both are
acceptable. That is precisely the behaviour a fine-tune is usually being run to
remove."""),

("code", _CONSISTENCY),

("md", """Note the honest reading. Not every conflict is an error — in this dataset the free-text
note legitimately decides some of them. But that is a statement about what the model
needs to see: if the note decides the label, the note must be in the training input,
and if it is not, you have built a dataset that contradicts itself for reasons the
model cannot access."""),

("md", """## 4 · Near-duplicates, and what a correct split does with them

The dedup warning in the lesson is not about wasted rows. It is about evaluation."""),

("code", _DEDUP),

("md", """A Jaccard threshold of 0.6 finds a great many exact matches here, and that is worth
naming rather than glossing: this corpus is generated by a seeded script that draws
notes from a fixed phrase pool, so duplication is a property of how it was made.

Real corpora have the same problem for different reasons — the same ticket refiled,
boilerplate repeated across records, one document ingested twice. The mechanism
differs and the consequence does not, which is the next cell."""),

("code", _LEAK),

("md", """This is the uncomfortable part. The split above was done correctly — random,
before any fitting, exactly as the discipline requires. The duplication was already
in the data, so splitting properly does not protect you from it. The check has to be
run on the content, not on the procedure."""),

("md", """## 5 · Now the arithmetic: will the run fit?

Four things are resident during training and only the first is the model. The lesson
gives the ladder; this gives the numbers, so you can see which lever moves which
term."""),

("code", _MEMORY),

("md", """Read the columns rather than the totals. Mixed precision halves weights, gradients
and activations together. Accumulation touches only activations, because that is the
only term that scales with batch size. Checkpointing attacks the same term again and
harder, which is why the order in the lesson is the order it is — each lever is aimed
at what remains after the previous one.

Note also what none of them touch: the optimiser state, which is held in higher
precision because that is where the small updates would otherwise be lost."""),

("md", """## 6 · And what low-rank adaptation actually changes"""),

("code", _LORA),

("md", """The weights column does not move at all — the base model is still fully resident.
What disappears is gradients and optimiser state for 99.9% of the parameters, which
is where the memory was. This is the lesson's point stated as a number: the saving is
not mainly the parameter count, it is that a frozen weight needs neither a gradient
nor an optimiser slot.

Rank barely moves the total, which is the other half of the argument. If rank is
nearly free in memory, then choosing a high one is not a cost decision — it is a
capacity decision, and its failure mode is overfitting rather than an out-of-memory
error."""),

("md", """## What to take from this

- **Run the label distribution first.** The majority-class share is the number your
  fine-tune has to beat, and it is free.
- **Cross the label against what produced it.** A label with one context is a label
  the model will not learn.
- **Look for contradictions in the fields the model can see.** If something outside
  those fields decides the label, it belongs inside them.
- **Check duplicates on content, not on procedure.** A correct split does not save you.
- **Do the memory arithmetic before renting anything.** Three levers, in order, and
  none of them costs accuracy.

The checklist these plug into is `artifacts/sop/fine-tuning.md`, whose first section
is still the one that matters most: most fine-tuning projects should end there."""),
]),
]
