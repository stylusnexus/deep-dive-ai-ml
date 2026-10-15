OUTDIR = "notebooks/05-evaluation"

_SETUP = '''import math, random
from statistics import mean, pstdev, stdev

random.seed(11)   # every number below is reproducible; change this and re-read the lesson

def welch_p(a, b):
    """Unpaired two-sample test. Treats the two arms as unrelated piles of numbers."""
    na, nb = len(a), len(b)
    ma, mb = mean(a), mean(b)
    va = sum((x - ma) ** 2 for x in a) / (na - 1)
    vb = sum((x - mb) ** 2 for x in b) / (nb - 1)
    se = math.sqrt(va / na + vb / nb)
    if se == 0:
        return 1.0
    t = abs(ma - mb) / se
    return 2 * (1 - 0.5 * (1 + math.erf(t / math.sqrt(2))))

def paired_p(a, b):
    """Paired test. Works on the per-item differences, so shared difficulty cancels."""
    d = [x - y for x, y in zip(a, b)]
    n = len(d)
    md = mean(d)
    vd = sum((x - md) ** 2 for x in d) / (n - 1)
    se = math.sqrt(vd / n)
    if se == 0:
        return 1.0
    t = abs(md) / se
    return 2 * (1 - 0.5 * (1 + math.erf(t / math.sqrt(2))))

print("no model, no API key, no network — everything here is simulated with a fixed seed")'''


_PAIRING = '''TRIALS, N = 3000, 20

unpaired_wins = paired_wins = 0
for _ in range(TRIALS):
    # Question difficulty is the biggest source of variance in a real eval,
    # and BOTH systems face the same questions.
    difficulty = [random.gauss(0, 1.0) for _ in range(N)]
    a = [d + random.gauss(0, 0.25) for d in difficulty]
    b = [d + 0.30 + random.gauss(0, 0.25) for d in difficulty]   # B is genuinely better
    if welch_p(a, b) < 0.05:
        unpaired_wins += 1
    if paired_p(a, b) < 0.05:
        paired_wins += 1

print(f"{N} questions, a real effect of +0.30, difficulty varying by ~1.0\\n")
print(f"  unpaired test detects it : {100*unpaired_wins/TRIALS:5.1f}% of the time")
print(f"  paired   test detects it : {100*paired_wins/TRIALS:5.1f}% of the time")'''


_SHAPE = '''# Two systems. Identical mean score. Read only the mean and they are the same system.
random.seed(4)
N = 200
steady  = [random.gauss(0.70, 0.06) for _ in range(N)]
bimodal = [random.gauss(0.95, 0.03) if random.random() < 0.5 else random.gauss(0.45, 0.03)
           for _ in range(N)]

def histogram(xs, lo=0.3, hi=1.0, bins=14, width=44):
    counts = [0] * bins
    for x in xs:
        i = min(bins - 1, max(0, int((x - lo) / (hi - lo) * bins)))
        counts[i] += 1
    top = max(counts)
    for i, c in enumerate(counts):
        edge = lo + (hi - lo) * i / bins
        print(f"    {edge:4.2f}  {'#' * int(width * c / top)}")

for name, xs in (("steady", steady), ("bimodal", bimodal)):
    print(f"  {name}: mean {mean(xs):.3f}  sd {stdev(xs):.3f}  "
          f"min {min(xs):.2f}  max {max(xs):.2f}")
    histogram(xs)
    print()

print(f"  below 0.55: steady {sum(x < 0.55 for x in steady):3d}"
      f"   bimodal {sum(x < 0.55 for x in bimodal):3d}   out of {N}")'''


_BESSEL = '''print("true variance is 1.000 by construction\\n")
print(f"  {'n':>5}  {'divide by n':>20}  {'divide by n-1':>20}")
for n in (5, 10, 30, 100, 1000):
    biased, corrected = [], []
    for _ in range(20_000):
        s = [random.gauss(0.0, 1.0) for _ in range(n)]
        m = mean(s)
        ss = sum((x - m) ** 2 for x in s)
        biased.append(ss / n)
        corrected.append(ss / (n - 1))
    b, c = mean(biased), mean(corrected)
    print(f"  {n:>5}  {b:>11.3f} ({100*(b-1):+5.1f}%)  {c:>11.3f} ({100*(c-1):+5.1f}%)")'''


_PEEK = '''TRIALS, N, PEEKS = 4000, 200, 10

fixed = peeked = 0
for _ in range(TRIALS):
    # Both arms drawn from the SAME distribution. Every "significant"
    # result below is a false positive by construction.
    a = [random.gauss(0, 1) for _ in range(N)]
    b = [random.gauss(0, 1) for _ in range(N)]
    if welch_p(a, b) < 0.05:
        fixed += 1
    for step in range(1, PEEKS + 1):
        k = N * step // PEEKS
        if k > 5 and welch_p(a[:k], b[:k]) < 0.05:
            peeked += 1
            break

print(f"  tested once, at the planned sample size : {100*fixed/TRIALS:4.1f}%   <- the instrument check")
print(f"  peeked {PEEKS} times, stopped when p<0.05      : {100*peeked/TRIALS:4.1f}%   <- the same data, read greedily")
print(f"\\n  nominal false-positive rate is 5%; peeking multiplied it by {peeked/max(fixed,1):.1f}x")'''


_INTERVALS = '''# One system, scores with a real spread. How wrong can the MEAN be,
# and how wrong can a SINGLE NEXT CASE be? Different questions.
random.seed(7)
TRUE_MEAN, TRUE_SD = 0.70, 0.18

print(f"  {'n':>6}  {'95% CI on the mean':>26}  {'95% PI for one new case':>28}")
for n in (10, 30, 100, 1000, 10000):
    s = [random.gauss(TRUE_MEAN, TRUE_SD) for _ in range(n)]
    m, sd = mean(s), stdev(s)
    ci = 1.96 * sd / math.sqrt(n)                    # uncertainty in the estimate
    pi = 1.96 * sd * math.sqrt(1 + 1 / n)            # + the spread of the data itself
    print(f"  {n:>6}  {m-ci:>11.3f} to {m+ci:<11.3f}  {m-pi:>12.3f} to {m+pi:<12.3f}")

print(f"\\n  the confidence interval shrinks towards nothing as n grows")
print(f"  the prediction interval converges on the real spread (about {1.96*TRUE_SD:.2f} either side) and stays there")'''


_FMT_SETUP = '''import random, re, json, math, urllib.request
from collections import defaultdict

rng = random.Random(7)   # the graph, the questions and the gold answers all follow from this seed

SITES = ["Site A", "Site B", "Site C"]
SUPPLIERS = {"Norvane": "Denmark", "Kessler": "Germany", "Aldoro": "Spain", "Hallis": "Denmark"}
TURBINES = [f"T{i}" for i in range(1, 21)]
INSPECTORS = ["Rivera", "Okafor", "Lindqvist", "Tanaka"]

site_of, gearbox_of, supplier_of = {}, {}, {}
for i, t in enumerate(TURBINES):
    site_of[t] = SITES[i % 3]
    gearbox_of[t] = f"G{i + 1}"
    supplier_of[gearbox_of[t]] = rng.choice(list(SUPPLIERS))

facts = []
for t in TURBINES:
    facts.append((t, "is located at", site_of[t]))
    facts.append((t, "has gearbox", gearbox_of[t]))
for g, s in supplier_of.items():
    facts.append((g, "is supplied by", s))
for s, c in SUPPLIERS.items():
    facts.append((s, "is based in", c))

# Who said it, when, and how sure: one record per fact.
prov = {f: (rng.choice(INSPECTORS), f"2026-{rng.randint(1, 9):02d}-{rng.randint(1, 28):02d}",
            rng.choice(["low", "medium", "high"])) for f in facts}

# One deliberate conflict: T5 is also reported at a wrong site, by a different person, with low confidence.
CONFLICT = "T5"
true_site = site_of[CONFLICT]
wrong_site = next(s for s in SITES if s != true_site)
prov[(CONFLICT, "is located at", true_site)] = ("Okafor", "2026-03-02", "high")
wrong_fact = (CONFLICT, "is located at", wrong_site)
facts.append(wrong_fact)
prov[wrong_fact] = ("Tanaka", "2026-06-11", "low")

print(f"{len(TURBINES)} turbines, {len(facts)} facts, 1 planted conflict")'''


_FMT_FORMATS = '''def as_flat():
    return "\\n".join(f"{s} {p} {o}." for s, p, o in facts)

def as_annotated():
    # the shape RDF-star gives you: a statement, then statements about the statement
    return "\\n".join(f"<<{s} | {p} | {o}>> asserted_by {prov[(s, p, o)][0]}; "
                     f"asserted_on {prov[(s, p, o)][1]}; confidence {prov[(s, p, o)][2]}."
                     for s, p, o in facts)

def as_prose():
    return "\\n".join(f"{s} {p} {o}, as recorded by {prov[(s, p, o)][0]} on "
                     f"{prov[(s, p, o)][1]} with {prov[(s, p, o)][2]} confidence."
                     for s, p, o in facts)

FORMATS = {"flat": as_flat(), "annotated": as_annotated(), "prose": as_prose()}
for name, text in FORMATS.items():
    print(f"--- {name}: {len(text):,} characters, {len(text.splitlines())} lines")
    print("\\n".join(text.splitlines()[:2]))'''


_FMT_QUESTIONS = '''# Gold answers are computed from the graph, so they are correct by construction.
others = [t for t in TURBINES if t != CONFLICT]   # T5's site is deliberately contested
relational = []   # answerable from the facts alone, so answerable in every format
for t in rng.sample(TURBINES, 16):
    relational.append(("two-hop", f"Which country is the supplier of the gearbox in turbine {t} based in?",
                       SUPPLIERS[supplier_of[gearbox_of[t]]]))
for t in rng.sample(TURBINES, 12):
    relational.append(("two-hop", f"Which supplier made the gearbox in turbine {t}?",
                       supplier_of[gearbox_of[t]]))
for s in SUPPLIERS:
    n = sum(1 for t in TURBINES if supplier_of[gearbox_of[t]] == s)
    relational.append(("count", f"How many turbines use a gearbox supplied by {s}?", str(n)))
for t in rng.sample(others, 8):
    relational.append(("lookup", f"Which site is turbine {t} located at?", site_of[t]))

epistemic = []    # answerable only if the provenance is present
for f in rng.sample([f for f in facts if f[1] == "has gearbox"], 6):
    epistemic.append(("who", f"Who recorded that {f[0]} has gearbox {f[2]}?", prov[f][0]))
for f in rng.sample([f for f in facts if f[1] == "is supplied by"], 6):
    epistemic.append(("when", f"On what date was it recorded that {f[0]} is supplied by {f[2]}?", prov[f][1]))
epistemic.append(("conflict", "Turbine T5 has two recorded locations. Which site does the higher-confidence record give?", true_site))
epistemic.append(("conflict", "Turbine T5 has two recorded locations. Who recorded the one with low confidence?", "Tanaka"))

from collections import Counter
print("relational:", len(relational), dict(Counter(k for k, _, _ in relational)))
print("epistemic: ", len(epistemic), dict(Counter(k for k, _, _ in epistemic)))'''


_FMT_ENDPOINT = '''ENDPOINTS = ["http://localhost:11455/v1", "http://localhost:11434/v1", "http://localhost:1234/v1"]

def find_models():
    # Every chat model on every reachable OpenAI-compatible endpoint. Embedding models are
    # listed too and return HTTP 400 on a chat call, so they are filtered out by name.
    found = []
    for base in ENDPOINTS:
        try:
            with urllib.request.urlopen(f"{base}/models", timeout=3) as r:
                ids = [m["id"] for m in json.loads(r.read()).get("data", [])]
        except Exception:
            continue
        found += [(base, i) for i in ids
                  if not any(w in i.lower() for w in ("embed", "rerank", "whisper", "clip"))]
    return found

MODELS = find_models()
print(f"{len(MODELS)} chat model(s) reachable:", [m for _, m in MODELS] or "none")
if not MODELS:
    print("No local endpoint. Start LM Studio or Ollama and re-run; this notebook has no fallback "
          "because the measurement IS the model's answers.")'''


_FMT_RUN = '''SYSTEM = ("Answer using ONLY the records below. Reply with the answer alone: a name, a date, "
          "a country, a site or a number. If the records do not contain the answer, reply exactly: NOT IN RECORDS.")

def ask(base, model, records, question):
    body = json.dumps({"model": model, "temperature": 0, "max_tokens": 40,
                       "messages": [{"role": "system", "content": SYSTEM},
                                    {"role": "user", "content": f"Records:\\n{records}\\n\\nQuestion: {question}"}]}).encode()
    req = urllib.request.Request(f"{base}/chat/completions", data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        out = json.loads(r.read())["choices"][0]["message"]["content"]
    return re.sub(r"<think>.*?</think>", "", out, flags=re.S).strip()

def correct(answer, gold):
    # whole-token match, so "Site A" is not credited for "Site AB" and "1" is not credited for "12"
    return re.search(r"(?<![\\w-])" + re.escape(gold.lower()) + r"(?![\\w-])", answer.lower()) is not None

results = {}      # (model, set, format) -> list of (kind, question, gold, answer, ok)
ERRORS = []
for base, model in MODELS:
    for qset, questions, fmts in (("relational", relational, ["flat", "annotated", "prose"]),
                                  ("epistemic", epistemic, ["flat", "annotated", "prose"])):
        for fmt in fmts:
            rows = []
            for kind, q, gold in questions:
                try:
                    a = ask(base, model, FORMATS[fmt], q)
                except Exception as ex:
                    ERRORS.append((model, fmt, q[:40], ex.__class__.__name__))
                    a = "ERROR"
                rows.append((kind, q, gold, a, correct(a, gold)))
            results[(model, qset, fmt)] = rows
print(f"{sum(len(v) for v in results.values())} answers collected, {len(ERRORS)} request errors")'''


_FMT_TABLE = '''for model in dict.fromkeys(m for _, m in MODELS):
    print(f"model: {model}")
    print(f"{'':12}" + "".join(f"{f:>14}" for f in ("flat", "annotated", "prose")))
    for qset in ("relational", "epistemic"):
        cells = []
        for fmt in ("flat", "annotated", "prose"):
            rows = results[(model, qset, fmt)]
            cells.append(f"{sum(r[4] for r in rows)}/{len(rows)}")
        print(f"{qset:12}" + "".join(f"{c:>14}" for c in cells))
    print()
    print("relational, by question type (correct/asked)")
    kinds = list(dict.fromkeys(k for k, _, _ in relational))
    for kind in kinds:
        cells = []
        for fmt in ("flat", "annotated", "prose"):
            rows = [r for r in results[(model, "relational", fmt)] if r[0] == kind]
            cells.append(f"{sum(r[4] for r in rows)}/{len(rows)}")
        print(f"{kind:12}" + "".join(f"{c:>14}" for c in cells))
    print()'''


_FMT_PAIRED = '''def sign_test_p(b, c):
    # exact two-sided sign test on the discordant pairs: b right-only-in-one, c right-only-in-the-other
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)

for model in dict.fromkeys(m for _, m in MODELS):
    print(f"model: {model}   (relational questions, same items in every format)")
    base_rows = results[(model, "relational", "flat")]
    for other in ("annotated", "prose"):
        rows = results[(model, "relational", other)]
        only_flat = sum(1 for a, b in zip(base_rows, rows) if a[4] and not b[4])
        only_other = sum(1 for a, b in zip(base_rows, rows) if b[4] and not a[4])
        print(f"  flat vs {other:9}  right only in flat: {only_flat:2}   right only in {other}: {only_other:2}   "
              f"sign-test p = {sign_test_p(only_flat, only_other):.2f}")'''


_FMT_MISSES = '''for model in dict.fromkeys(m for _, m in MODELS):
    for fmt in ("flat", "annotated", "prose"):
        misses = [r for r in results[(model, "relational", fmt)] if not r[4]]
        print(f"{fmt}: {len(misses)} relational misses" + (" (first four)" if len(misses) > 4 else ""))
        for kind, q, gold, a, _ in misses[:4]:
            print(f"   [{kind}] {q[:62]}  gold={gold!r}  answered={a[:36]!r}")
    print()
    print("epistemic misses on the annotated format:")
    for kind, q, gold, a, ok in results[(model, "epistemic", "annotated")]:
        if not ok:
            print(f"   [{kind}] {q[:62]}  gold={gold!r}  answered={a[:36]!r}")'''


NOTEBOOKS = [
("01-is-the-difference-real.ipynb", [

("md", """# 05 · Is the Difference Real?

Every claim in the *Is the Difference Real?* lesson is a number, and a number you
have not seen produced is a number you are taking on trust. This notebook produces
them.

Nothing here calls a model. There is no API key, no network and no cost — each
result is a simulation with a known right answer, which is the only setting in which
you can check whether a statistical method actually recovers the truth. Once you
have watched a method fail on data whose answer you already knew, you will recognise
the failure on data whose answer you do not.

Four things, in the order they cost you money:

1. **Pairing** — the same data tested two ways, with wildly different power
2. **The shape of each arm** — two systems with an identical mean and nothing else in common
3. **Bessel's correction** — why you divide by `n-1`, and when it stops mattering
4. **Peeking** — how checking a running experiment turns a 5% error rate into 20%

Then the interval distinction that decides whether you can make a per-case promise."""),

("code", _SETUP),

("md", """## 1 · Pairing

An evaluation runs *the same questions* through both systems. That means the two
score sets are paired, and question difficulty — usually the largest source of
variance in the whole exercise — is shared by each pair rather than being noise.

A paired test subtracts it out. An unpaired test leaves it in the noise term and
drowns in it. Below, both tests see identical data containing a real effect."""),

("code", _PAIRING),

("md", """Same data. Same effect. The unpaired test is not *wrong* — it is answering a
question nobody asked, namely whether two unrelated piles of numbers differ, when
the question was whether B beats A **question by question**.

The practical consequence: a team using the unpaired test on this eval concludes
there is no difference, and ships nothing, on evidence that was there all along."""),

("md", """## 2 · Report the distribution per arm, not just the mean

Two systems below have the same mean score to three decimal places. One is steady.
The other is excellent half the time and unusable the other half."""),

("code", _SHAPE),

("md", """A mean cannot see the difference and a standard deviation barely hints at it — the
shape is the finding. The bimodal system fails badly on half its inputs, and if
those correlate with anything a user cares about (a language, a document type, a
customer segment) you have shipped a system that is broken for that group and
reported it as equivalent.

This is why the lesson asks for the distribution per arm and for slices as arms.
The count under 0.55 tells you more here than either summary statistic."""),

("md", """## 3 · Bessel's correction

Sample variance divided by `n` is biased low, because the mean was fitted to the
same data: deviations from a fitted mean are systematically smaller than deviations
from the true one. Dividing by `n-1` corrects it.

The question worth answering is not whether it is correct — it is whether the size
of the error matters at *your* n."""),

("code", _BESSEL),

("md", """At eval sizes the error is large enough to change a conclusion. At n=1000 it is
noise. That is the whole practical content of the correction: it matters at the
sample sizes evaluations actually run at, and nowhere else."""),

("md", """## 4 · Peeking

The most expensive mistake in this notebook, because it does not look like a
mistake. You run an A/B test, you check it each morning, and you stop when it
reaches significance.

Below, both arms are drawn from the *same* distribution. There is no effect. Every
"significant" result is a false positive by construction, so the rate you see is
the rate at which the procedure lies to you."""),

("code", _PEEK),

("md", """The first line is the instrument check: a correctly run test lands on its nominal
5%, which tells you the simulation is trustworthy before you read the second line.

The second line is what a stopping rule does. Nothing was faked and no arm was
better — the procedure simply gets many chances to cross a threshold and stops the
moment it does. Decide the sample size in advance, or accept that "significant"
means nothing."""),

("md", """## 5 · Two intervals, and only one is about your next case

A **confidence interval** describes the mean. A **prediction interval** describes a
single new observation. Anything making a per-item promise — a latency budget, a
per-customer forecast, a per-document threshold — is asking the second question."""),

("code", _INTERVALS),

("md", """The confidence interval shrinks towards nothing, because with enough data you know
the mean precisely. The prediction interval does not, because knowing the mean
perfectly still tells you nothing about how far the next draw lands from it.

Quote the first as a per-case guarantee and you will breach it roughly one time in
twenty, having done the arithmetic correctly throughout."""),

("md", """## What to take to your own evaluation

- Run the same items through both systems and **test paired**. Free power.
- Report **spread and shape per arm**, not one number per system.
- Divide by `n-1`. At eval sizes it is not pedantry.
- Fix the sample size **before** you start, and do not read the result early.
- If the number becomes a per-case promise, quote a **prediction** interval.

The procedure these plug into is `artifacts/sop/measurement.md`, and step 0 of that
checklist is the one this notebook keeps demonstrating: prove the instrument before
you trust what it says."""),
]),
("02-does-the-format-change-the-answer.ipynb", [

("md", """# 05 · Does the Format Change the Answer?

An essay published in April 2026 argues that language models fail at questions over
knowledge graphs because a bare list of triples does not look like the text they were
trained on, and that annotating each triple with who asserted it, when and how sure
makes the same graph easier for a model to use. The author says the claim is untested.
This notebook tests one slice of it.

**The prediction under test:** for the same facts and the same questions, accuracy
should rise as the serialisation gets richer.

**What is held fixed:** one synthetic graph (20 wind turbines, their gearboxes,
suppliers and sites), the same questions, temperature 0, and gold answers computed
from the graph rather than written by hand.

**What varies:** the format only.

- `flat`: one short sentence per fact, nothing else
- `annotated`: each fact followed by who asserted it, when, and with what confidence
- `prose`: each fact as a sentence that carries the same who, when and confidence

**What this cannot show.** One synthetic graph, one question set, and only the models
that happen to be running on this machine. A result here is a measurement of those
models on this graph, not a test of the essay's theory."""),

("code", _FMT_SETUP),

("md", """## 1 · Three serialisations of the same facts

The planted conflict matters later: one turbine has two recorded sites, and only the
annotated and prose formats say which record to believe."""),

("code", _FMT_FORMATS),

("md", """## 2 · Two kinds of question

**Relational** questions are answerable from the facts alone, so every format can in
principle answer them. In the annotated and prose formats the extra provenance is
*noise* for these questions, which is exactly what the prediction needs to survive.

**Epistemic** questions ask who recorded something, when, or which of two records to
trust. The flat format has no way to answer them, so it is included only as a control:
a model that answers them from flat records is guessing."""),

("code", _FMT_QUESTIONS),

("md", """## 3 · Find the models

Any OpenAI-compatible endpoint works: LM Studio, Ollama and llama.cpp's server all
expose one, so no API key is needed. Every chat model found is run."""),

("code", _FMT_ENDPOINT),

("md", """## 4 · Ask every question in every format"""),

("code", _FMT_RUN),

("md", """## 5 · The result"""),

("code", _FMT_TABLE),

("md", """## 6 · Is the gap bigger than the noise?

The same 40 questions went through every format, so the right comparison is paired:
count the questions where exactly one format got it right. A sign test on those
discordant pairs says how often a gap that size would appear if the two formats were
equally good."""),

("code", _FMT_PAIRED),

("md", """## 7 · Look at the misses

An accuracy table cannot say whether a miss was the model misreading the format or
declining to answer, and those lead to different fixes."""),

("code", _FMT_MISSES),

("md", """## What to take to your own evaluation

- **Hold the content fixed and vary only the format.** The annotated and prose versions
  carry the same facts as the flat one, so any difference is the format and not the
  information.
- **Split the questions by whether the extra information is needed.** On the relational
  questions the provenance is clutter. On the epistemic ones it is the answer. Pooling
  them would hide both results.
- **The relational result did not follow the prediction.** On this model the annotated
  format lost eight questions the flat one got right and won two, the reverse of the
  predicted direction, though a sign test on ten disagreements cannot separate that from
  noise. Prose matched flat.
- **The epistemic gain proves nothing about legibility.** Flat scored zero because the
  answer is not in it. Annotated and prose scored 12 of 14 because the answer is there.
  That is the information being present, not the format being easier to read.
- **This is one model, one synthetic graph and 40 questions.** The counting questions
  were weak in every format. A result like this is a reason to run your own graph through
  your own models with `ENDPOINTS` changed, not a verdict on the essay."""),
]),
]
