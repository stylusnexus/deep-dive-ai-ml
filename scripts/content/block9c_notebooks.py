OUTDIR = "notebooks/09-electives"

_LANDSCAPE = '''import math, random

def landscape(x):
    """A deceptive 1D fitness landscape: an easy local peak near x=20 and a taller
    global peak near x=80, separated by a shallow valley. Reaching the global peak
    from the local one means the score must drop before it rises again."""
    local = 0.6 * math.exp(-((x - 20) ** 2) / (2 * 6 ** 2))
    global_peak = 1.0 * math.exp(-((x - 80) ** 2) / (2 * 8 ** 2))
    return max(local, global_peak, 0.02)

X_MIN, X_MAX = 0, 100
STEP_SIZES = [-5, -3, -1, 1, 3, 5]
THRESHOLD = 0.8   # a run "finds the real peak" once its best score clears this

SHADES = " .:-=+*#%@"
def sketch(fn, lo, hi, width=70):
    vals = [fn(lo + (hi - lo) * i / (width - 1)) for i in range(width)]
    scaled = [int(v / max(vals) * (len(SHADES) - 1)) for v in vals]
    print("".join(SHADES[s] for s in scaled))
    print(f"x={lo:<3d}" + " " * (width - 10) + f"x={hi}")

sketch(landscape, X_MIN, X_MAX)
print("\\nleft hump: the easy local peak. right hump: the taller, hidden global peak.")
print("the dip between them is the trap — any strictly-uphill walker that reaches")
print("the local peak can never take a single step toward the real one.")'''

_HILL_CLIMB = '''def hill_climb(start, steps, rng):
    """The ratchet: keep a move only when the score strictly rises."""
    x = start
    for _ in range(steps):
        cand = max(X_MIN, min(X_MAX, x + rng.choice(STEP_SIZES)))
        if landscape(cand) > landscape(x):
            x = cand
    return x

def success_rate(searcher, trials, seed0):
    hits = 0
    for i in range(trials):
        rng = random.Random(seed0 + i)
        x = searcher(rng)
        if landscape(x) >= THRESHOLD:
            hits += 1
    return hits / trials

TRIALS, START, BUDGET = 300, 10, 200

rate = success_rate(lambda rng: hill_climb(START, BUDGET, rng), TRIALS, seed0=1000)
print(f"hill-climb, {BUDGET} evaluations, {TRIALS} independent trials: {rate:.1%} find the real peak")'''

_POPULATION = '''def population_climb(k, steps_each, rng):
    """Spread k independent climbers across the landscape and keep the best result.
    Some start past the valley by luck alone, and from there the taller peak is uphill."""
    best = None
    for _ in range(k):
        start = rng.randint(X_MIN, X_MAX)
        x = hill_climb(start, steps_each, rng)
        if best is None or landscape(x) > landscape(best):
            best = x
    return best

K = 5
rate_pop = success_rate(lambda rng: population_climb(K, BUDGET // K, rng), TRIALS, seed0=2000)
print(f"population of {K}, {BUDGET} evaluations total, {TRIALS} trials: {rate_pop:.1%} find the real peak")'''

_ARCHIVE = '''BIN_WIDTH = 5
def bin_of(x):
    return x // BIN_WIDTH

def archive_search(start, steps, rng):
    """One elite kept per niche of the search space, regardless of its score, and
    never discarded. The next move mutates a uniformly-chosen discovered niche —
    a weak, neglected region keeps earning turns instead of losing them to the
    niches scoring well right now."""
    archive = {bin_of(start): start}
    for _ in range(steps):
        parent = archive[rng.choice(list(archive.keys()))]
        cand = max(X_MIN, min(X_MAX, parent + rng.choice(STEP_SIZES)))
        b = bin_of(cand)
        if b not in archive or landscape(cand) > landscape(archive[b]):
            archive[b] = cand
    return max(archive.values(), key=landscape)

rate_arch = success_rate(lambda rng: archive_search(START, BUDGET, rng), TRIALS, seed0=3000)
print(f"archive (never discards), {BUDGET} evaluations, {TRIALS} trials: {rate_arch:.1%} find the real peak")
print(f"\\nsame budget as hill-climb above ({BUDGET} evaluations): barely more than zero.")
print("the archive has not failed — it has not yet had enough tries to get lucky.")'''

_SWEEP = '''print(f"{\'budget\':>8} {\'hill-climb\':>12} {\'archive\':>10}")
for budget in (200, 500, 1000, 2000):
    r_hill = success_rate(lambda rng, b=budget: hill_climb(START, b, rng), TRIALS, seed0=1000)
    r_arch = success_rate(lambda rng, b=budget: archive_search(START, b, rng), TRIALS, seed0=3000)
    print(f"{budget:>8} {r_hill:>11.1%} {r_arch:>10.1%}")'''

NOTEBOOKS = [
("04-self-improvement-search.ipynb", [

("md", """# 09 · Self-Improvement Search

Three ways to search for a better version of something, run against the same toy
landscape with the same evaluation budget. Nothing here calls a model — the point is
structural, not about any particular algorithm, and a synthetic landscape makes the
structure checkable rather than asserted.

This is a minimal illustration of the ideas behind hill-climbing, population search
(GEPA) and archive-based search (the Darwin Gödel Machine), not a reimplementation of
any of them — see the *Agents That Improve Themselves* lesson for the real algorithms
and their sources."""),

("code", _LANDSCAPE),

("md", """## 1 · Hill-climbing: a ratchet that cannot go downhill first

Keep a move only when the score strictly rises. Cheap, and it makes exactly one
promise: the score never falls. That promise is also the trap — once it reaches the
local peak, every neighbouring move scores worse, so it never moves again."""),

("code", _HILL_CLIMB),

("md", """Run it for longer and the number does not change. This is not bad luck — it is
structural. From the local peak, *every* single step scores worse than staying put,
so a strictly-uphill walker has no way to begin crossing the valley at any budget."""),

("md", """## 2 · Population: spread beats depth

Evolution's answer is not a cleverer climber, it is many of them. Scatter several
independent climbers across the landscape and keep whichever does best. Some start
to the left of the valley and get stuck exactly like before — but some start to the
right of it, where the taller peak is already uphill."""),

("code", _POPULATION),

("md", """Same total evaluation budget as the single climber above, split across five starting
points instead of spent on one. The improvement is not a smarter search, it is
diversity of starting position — the same reason GEPA keeps a Pareto front of
candidates rather than collapsing to one ranked winner."""),

("md", """## 3 · Archive: an elite per niche, never discarded

Keep the best candidate found so far *in each region* of the space, however poorly it
scores, and never throw one out. The next move mutates a region chosen uniformly from
what has been discovered so far, not just the best region — so a step that landed in
the valley stays available as a stepping stone instead of being pruned for scoring
worse than the local peak."""),

("code", _ARCHIVE),

("md", """## 4 · What the archive is actually buying: patience, not luck

Population wins at a fixed budget because it only needs one of five starting points to
be lucky. The archive's bet is different — it needs *one single mutation, at any point
in an arbitrarily long run,* to land in the valley, and once it does that foothold is
never lost. Sweep the budget and the two methods tell very different stories:"""),

("code", _SWEEP),

("md", """Hill-climbing's number does not move — it is a structural ceiling, not a sample size
problem. The archive's number climbs steeply with budget, because every niche it finds
is kept forever, so each additional step is one more chance to extend a foothold it
already banked rather than one more chance to get lucky from scratch.

That is the Darwin Gödel Machine's actual claim: not that an archive beats a
population on a single run, but that an archive's odds keep improving with spend in a
way a ratchet's structurally cannot, because nothing the archive finds is ever thrown
away."""),

("md", """## What to carry away

- **Hill-climbing is a ratchet.** It cannot cross a dip at any budget — this is a
  structural property of only accepting strictly-improving moves, not bad luck.
- **A population wins through diversity of starting position**, not through being a
  smarter climber — some members are already past the trap by chance.
- **An archive wins through patience.** It never discards a weak foothold, so its odds
  of recovering the real peak climb with budget in a way hill-climbing's cannot.
- **None of this is free.** Population and archive searches spend more evaluations per
  improvement than a single climber. Spend the extra budget when the landscape is
  genuinely deceptive, not as a default.

This is runnable evidence for the *Agents That Improve Themselves* lesson's claim that
spend should match the landscape, not a preference for one algorithm over another."""),
]),
]
