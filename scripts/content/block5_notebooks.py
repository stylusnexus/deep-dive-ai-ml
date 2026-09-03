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
]
