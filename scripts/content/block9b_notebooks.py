OUTDIR = "notebooks/09-electives"

_IMAGE = '''import math, random
random.seed(9)

# A 16x16 greyscale image, built rather than loaded so the notebook needs nothing.
# A light square on a dark ground, with a little noise so nothing is suspiciously clean.
H = W = 16
img = [[0.1 + random.gauss(0, 0.02) for _ in range(W)] for _ in range(H)]
for y in range(4, 12):
    for x in range(5, 13):
        img[y][x] = 0.85 + random.gauss(0, 0.02)

SHADES = " .:-=+*#%@"
def show(grid, label=""):
    lo = min(min(r) for r in grid); hi = max(max(r) for r in grid)
    rng = (hi - lo) or 1.0
    print(label)
    for row in grid:
        print("   " + "".join(SHADES[min(9, int((v - lo) / rng * 9.999))] for v in row))
    print(f"   range {lo:+.2f} to {hi:+.2f}\\n")

show(img, "the image (light square on dark ground)")'''


_CONV = '''def convolve(grid, kernel):
    """Valid convolution, written out. No library — the sliding is the lesson."""
    kh, kw = len(kernel), len(kernel[0])
    out = []
    for y in range(len(grid) - kh + 1):
        row = []
        for x in range(len(grid[0]) - kw + 1):
            total = 0.0
            for ky in range(kh):
                for kx in range(kw):
                    total += grid[y + ky][x + kx] * kernel[ky][kx]
            row.append(total)
        out.append(row)
    return out

VERTICAL   = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]     # Sobel: left-right change
HORIZONTAL = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]     # Sobel: top-bottom change
BLUR       = [[1/9]*3 for _ in range(3)]

show(convolve(img, VERTICAL),   "vertical edges — the left and right sides of the square")
show(convolve(img, HORIZONTAL), "horizontal edges — the top and bottom")
show(convolve(img, BLUR),       "blur — same machinery, different nine numbers")'''


_SHARED = '''# The same kernel, the same square, moved. Weight sharing means no relearning.
moved = [[0.1 + random.gauss(0, 0.02) for _ in range(W)] for _ in range(H)]
for y in range(1, 8):
    for x in range(2, 9):
        moved[y][x] = 0.85 + random.gauss(0, 0.02)

a = convolve(img, VERTICAL)
b = convolve(moved, VERTICAL)
peak = lambda g: max(max(abs(v) for v in row) for row in g)
print(f"strongest vertical-edge response, original position : {peak(a):.2f}")
print(f"strongest vertical-edge response, square moved      : {peak(b):.2f}")
print("\\nsame nine weights, no retraining, no new parameters — the detector moved with it.")
print("a dense layer would have learned 'edge at column 12' and known nothing about column 8.")'''


_PARAMS = '''def dense_params(h, w, channels, units):
    return h * w * channels * units + units

def conv_params(k, in_ch, out_ch):
    return k * k * in_ch * out_ch + out_ch

print(f"{'layer':<46}{'parameters':>14}")
print("-" * 60)
print(f"{'dense: 224x224x3 image -> 1000 units':<46}{dense_params(224,224,3,1000):>14,}")
print(f"{'conv:  3x3 kernel, 3 in -> 64 filters':<46}{conv_params(3,3,64):>14,}")
print(f"{'conv:  3x3 kernel, 64 in -> 128 filters':<46}{conv_params(3,64,128):>14,}")

ratio = dense_params(224,224,3,1000) / conv_params(3,3,64)
print(f"\\nthe first conv layer has {ratio:,.0f}x fewer parameters than the dense one")
print("and unlike the dense layer it works on an image of any size,")
print("because the parameters belong to the kernel rather than to the pixels")'''


_FIELD = '''# Receptive field: how much of the input one unit can see, by depth.
print(f"{'layer':>6}{'kernel':>8}{'stride':>8}{'sees (pixels)':>16}")
field, stride_prod = 1, 1
for layer, (k, s) in enumerate([(3,1),(3,1),(3,2),(3,1),(3,2),(3,1)], start=1):
    field += (k - 1) * stride_prod
    stride_prod *= s
    print(f"{layer:>6}{k:>8}{s:>8}{field:>16}")

print("\\nsix layers of 3x3 and a unit at the top sees a large patch of the original.")
print("no layer ever looked at more than nine numbers at once.")'''


NOTEBOOKS = [
("02-convolutions-by-hand.ipynb", [

("md", """# 09 · Convolutions, By Hand

The lesson argues that a convolution is an *assumption* rather than a trick: nearby
pixels are related, and a pattern means the same thing wherever it appears. This
writes the arithmetic out so that assumption is visible rather than asserted.

No libraries. The sliding window is the whole point, and calling a library function
would hide exactly the part worth seeing. Everything is a nested list and a loop,
which is slow and legible — the right trade for sixteen by sixteen pixels."""),

("code", _IMAGE),

("md", """## One operation, three behaviours

The kernel is nine numbers. Change the nine numbers and the same code detects vertical
edges, horizontal edges, or blurs — which is the point that gets lost when convolution
is introduced as "a filter". It is not a filter for anything in particular. It is a
patch-matcher, and what it matches is whatever you put in the window.

In a trained network nobody chooses these numbers. They are learned, and the early
layers of real CNNs reliably converge on something close to the edge detectors below."""),

("code", _CONV),

("md", """## What weight sharing actually buys

Move the square. Run the same kernel. Nothing is retrained and no parameter changes."""),

("code", _SHARED),

("md", """This is translation equivariance, and it is the assumption doing the work. A dense
layer would have to see the square in every position during training to respond to it
in every position. The convolution never learns a position at all."""),

("md", """## The parameter count, which is the headline argument"""),

("code", _PARAMS),

("md", """Read the second consequence as carefully as the first. The dense layer's parameters
are tied to a specific input size, so a 225-pixel image needs a different layer. The
convolution's parameters belong to the kernel, so the same trained filter runs on any
image — which is why convolutional networks handle variable input sizes naturally and
dense ones do not."""),

("md", """## How small windows end up seeing large objects"""),

("code", _FIELD),

("md", """The receptive field grows with depth, and faster wherever a stride halves the
resolution. This is the resolution of the apparent paradox in the lesson: a network
built entirely from three-by-three windows responds to whole objects, because a unit
high in the stack is looking at units that were themselves looking at units.

Compare this with attention, which reaches every position from the first layer and
pays quadratically for the privilege. The convolution reaches far more cheaply and
only in a fixed pattern; attention reaches anywhere and pays for it. That is the same
trade the lesson describes as a data budget, arriving as an architectural one."""),

("md", """## What to carry away

- A convolution is a **patch-matcher with shared weights**, not a filter for edges.
  Edges are just what these particular nine numbers happen to find.
- **Weight sharing is the assumption**, and it is what makes position irrelevant.
- The **parameter saving is enormous**, and the input-size independence that comes
  with it matters just as much in practice.
- **Depth buys reach.** Small windows stacked see large things, cheaply and in a
  fixed pattern — which is precisely what attention gives up in exchange for
  generality."""),
]),

("03-recommenders-and-their-loop.ipynb", [

("md", """# 09 · Recommenders, and the Loop They Sit In

The lesson's claim is that a recommender's central difficulty is not the algorithm but
the fact that it trains on data it produced. This builds a small collaborative filter,
watches it work, and then watches the loop close around it.

Stdlib only, seeded, no model calls."""),

("code", '''import math, random
from collections import Counter, defaultdict
random.seed(9)

USERS, ITEMS = 300, 400
# Three latent tastes. Users belong to one; items serve one. Nobody tells the model.
TASTES = 3
user_taste = [random.randrange(TASTES) for _ in range(USERS)]
item_taste = [random.randrange(TASTES) for _ in range(ITEMS)]
# Item quality, so popularity is not purely an artefact of taste.
item_quality = [random.uniform(0.3, 1.0) for _ in range(ITEMS)]

def would_like(u, i):
    """Ground truth we can check against, and that no recommender ever sees."""
    base = 0.75 if user_taste[u] == item_taste[i] else 0.10
    return base * item_quality[i]

print(f"{USERS} users, {ITEMS} items, {TASTES} hidden tastes")
print(f"if every user rated every item the matrix would hold {USERS*ITEMS:,} cells")'''),

("md", """## The matrix people actually have

Users see a fraction of the catalogue and interact with a fraction of that. Everything
below works from this — and note what it does *not* contain: any record of what was
shown and passed over."""),

("code", '''def simulate_exposure(slate_for, rounds=4, slate=5):
    """Each round every user is shown a slate and clicks probabilistically."""
    clicks = defaultdict(set)
    shown = defaultdict(set)
    for _ in range(rounds):
        for u in range(USERS):
            for i in slate_for(u, clicks[u]):
                shown[u].add(i)
                if random.random() < would_like(u, i):
                    clicks[u].add(i)
    return clicks, shown

def random_slate(u, seen, k=5):
    return random.sample(range(ITEMS), k)

clicks, shown = simulate_exposure(random_slate)
n_clicks = sum(len(v) for v in clicks.values())
print(f"interactions recorded : {n_clicks:,}")
print(f"matrix density        : {100*n_clicks/(USERS*ITEMS):.1f}%")
print(f"users with fewer than 3 interactions: "
      f"{sum(1 for u in range(USERS) if len(clicks[u]) < 3)}")'''),

("md", """## A collaborative filter, in twenty lines

No factorisation, no library. For a user, find similar users by overlap, and score
items by what those neighbours engaged with. It is the simplest thing that deserves
the name and it is enough to show every failure the lesson describes."""),

("code", '''def jaccard(a, b):
    return len(a & b) / len(a | b) if (a | b) else 0.0

def recommend(u, history, k=5, neighbours=20):
    sims = sorted(((jaccard(history, clicks[v]), v) for v in range(USERS) if v != u),
                  reverse=True)[:neighbours]
    score = Counter()
    for s, v in sims:
        if s <= 0:
            continue
        for i in clicks[v] - history:
            score[i] += s
    return [i for i, _ in score.most_common(k)]

def precision_at_k(recommender, k=5, trials=150):
    hits = total = 0
    for u in random.sample(range(USERS), trials):
        for i in recommender(u, clicks[u], k=k):
            hits += 1 if user_taste[u] == item_taste[i] else 0
            total += 1
    return hits / total if total else 0.0

print(f"precision@5, collaborative filter : {precision_at_k(recommend):.2f}")
print(f"precision@5, random baseline      : {precision_at_k(lambda u,h,k=5: random.sample(range(ITEMS),k)):.2f}")
print("\\nit works — it recovered the hidden tastes from interactions alone,")
print("having been told nothing about users or items")'''),

("md", """## Cold start, which is not a corner case"""),

("code", '''cold = [u for u in range(USERS) if len(clicks[u]) <= 1]
warm = [u for u in range(USERS) if len(clicks[u]) >= 8]

def precision_for(users, k=5):
    hits = total = 0
    for u in users:
        for i in recommend(u, clicks[u], k=k):
            hits += 1 if user_taste[u] == item_taste[i] else 0
            total += 1
    return (hits / total if total else 0.0), len(users)

pc, nc = precision_for(cold[:60])
pw, nw = precision_for(warm[:60])
print(f"users with <=1 interaction ({nc:>3}): precision@5 = {pc:.2f}")
print(f"users with >=8 interactions ({nw:>3}): precision@5 = {pw:.2f}")

never_clicked = [i for i in range(ITEMS) if not any(i in c for c in clicks.values())]
print(f"\\nitems nobody has ever clicked: {len(never_clicked)} of {ITEMS}")
print("collaborative filtering cannot recommend any of them, because it only knows items")
print("through the users who touched them — and nobody has")'''),

("md", """## Now close the loop

Everything so far used randomly chosen slates, which is not how a deployed system
behaves. Let the recommender choose what gets shown, feed the resulting clicks back in,
and repeat — which is the arrangement every production recommender is actually in."""),

("code", '''def run_loop(rounds=8, slate=5, explore=0.0):
    """Recommend, observe, retrain on what was observed. Repeat."""
    global clicks
    clicks = defaultdict(set)
    for u in range(USERS):                      # a small warm-up history
        for i in random.sample(range(ITEMS), 4):
            if random.random() < would_like(u, i):
                clicks[u].add(i)
    trace = []
    for r in range(rounds):
        exposed = Counter()
        for u in range(USERS):
            rec = recommend(u, clicks[u], k=slate)
            if len(rec) < slate:
                rec += random.sample(range(ITEMS), slate - len(rec))
            if explore:
                keep = int(slate * (1 - explore))
                rec = rec[:keep] + random.sample(range(ITEMS), slate - keep)
            for i in rec:
                exposed[i] += 1
                if random.random() < would_like(u, i):
                    clicks[u].add(i)
        coverage = len(exposed) / ITEMS
        top10 = sum(c for _, c in exposed.most_common(max(1, ITEMS // 10))) / sum(exposed.values())
        trace.append((r + 1, coverage, top10, sum(len(v) for v in clicks.values())))
    return trace

print(f"{'round':>6}{'catalogue coverage':>20}{'share in top 10% of items':>28}{'clicks':>9}")
for r, cov, top, cl in run_loop():
    print(f"{r:>6}{100*cov:>19.0f}%{100*top:>27.0f}%{cl:>9}")'''),

("md", """Read the columns together. Clicks rise steadily — engagement is improving, and a
dashboard showing only that column would report a system getting better every round.

Coverage falls, and the share of exposure going to a handful of items climbs. The
catalogue is narrowing in front of every user, and the clicks are rising *because* it
is narrowing: the system has found the items that reliably get clicked and is showing
them to more people. Nothing in the objective asked for this."""),

("md", """## The fix the lesson names, measured"""),

("code", '''print(f"{'exploration':>12}{'final coverage':>17}{'final concentration':>21}{'clicks':>9}")
for e in (0.0, 0.1, 0.2, 0.4):
    r, cov, top, cl = run_loop(explore=e)[-1]
    print(f"{100*e:>11.0f}%{100*cov:>16.0f}%{100*top:>20.0f}%{cl:>9}")

print("\\nexploration bought coverage. read the clicks column before assuming it cost any —")
print("on this run it did not, which means the greedy policy was leaving engagement on")
print("the table as well as narrowing the catalogue. one seeded run is not proof that")
print("exploration is free; it is proof that assuming it is expensive needs checking.")'''),

("md", """## What to carry away

- **A collaborative filter recovers structure nobody described**, from interactions
  alone. That is genuinely impressive and it is not the hard part.
- **Cold start is most of your users**, not an edge case — measure precision on the
  sparse ones separately or the average will hide them.
- **The loop closes on its own.** Coverage falls and concentration rises while
  engagement improves, and only the first two columns can tell you.
- **Exploration buys the one thing self-generated data cannot contain**: evidence
  about what you never showed. Whether it *costs* engagement is an empirical question
  and the answer here was no — the greedy policy had concentrated onto items that were
  reliably clicked rather than best-matched, so widening the slate found better ones.
  Do not carry that result to your own system; carry the habit of checking it.

The guardrail argument from the measurement lesson applies here with unusual force,
because the primary metric improves throughout the failure."""),
]),
]
