OUTDIR = "notebooks/02-classical-ml"

_INTRO = '''# 05 · MLP Patterns, Measured

A multi-layer perceptron (MLP) is a stack of layers, each a weight-matrix multiply followed
by a nonlinearity. Almost every larger model is built from that one layer wired in a
handful of ways. The lesson `mlp-patterns` names twelve wirings. This notebook runs the
ones that can be tested on a laptop, so every claim about *when to use* a wiring has a
number behind it.

Each experiment answers one question the lesson asks:

| Section | Pattern | Question |
|---|---|---|
| 1 | Perceptron, binary classifier | What can one layer not do? |
| 2 | Wide, deep | Does depth beat width at the same parameter count? |
| 3 | Encoder, decoder, autoencoder | Does the bottleneck find the true number of factors? |
| 4 | Expand then shrink, shrink then expand | When is a wide middle worth its cost, and when is a narrow one enough? |
| 5 | Two-tower | What does a joint model buy, and what does it cost at retrieval time? |
| 6 | GAN | What does a generator learn from a discriminator alone, and how often does it fail? |
| 7 | Heads | How much labelled data does a new head need on top of a trained trunk? |

**Needs:** PyTorch and NumPy, CPU only, a few minutes. Every dataset is synthetic and seeded,
so the ground truth is known and the numbers reproduce. Run the cells top to bottom.

**What this cannot tell you:** these are small networks on small synthetic problems. A
pattern that wins here has shown the mechanism, not that it wins on your data.'''

_SETUP = '''import time, math
import numpy as np
import torch, torch.nn as nn

torch.set_num_threads(2)
print("torch", torch.__version__, "| numpy", np.__version__, "| device: cpu")

def seed_all(s):
    torch.manual_seed(s); np.random.seed(s)

def n_params(m):
    return sum(p.numel() for p in m.parameters())

def fit(model, X, y, loss_fn, steps=600, lr=1e-2, batch=None):
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    for _ in range(steps):
        if batch:
            idx = torch.randint(0, len(X), (batch,))
            xb, yb = X[idx], y[idx]
        else:
            xb, yb = X, y
        opt.zero_grad()
        loss = loss_fn(model(xb), yb)
        loss.backward()
        opt.step()
    return model'''

_XOR = '''# Section 1. XOR: the classic problem a single layer cannot solve.
seed_all(0)
bits = torch.randint(0, 2, (800, 2)).float()
X = bits + 0.1 * torch.randn(800, 2)
y = (bits[:, 0] != bits[:, 1]).float().unsqueeze(1)
Xtr, ytr, Xte, yte = X[:600], y[:600], X[600:], y[600:]

bce = nn.BCEWithLogitsLoss()      # sigmoid + binary cross-entropy in one stable call

def acc(model, X, y):
    return ((model(X) > 0).float() == y).float().mean().item()

rows = []
for name, build in [("one layer (perceptron)", lambda: nn.Linear(2, 1)),
                    ("one hidden layer of 8", lambda: nn.Sequential(nn.Linear(2, 8), nn.Tanh(), nn.Linear(8, 1)))]:
    accs = []
    for s in range(5):
        seed_all(s)
        m = fit(build(), Xtr, ytr, bce, steps=800, lr=3e-2)
        accs.append(acc(m, Xte, yte))
    rows.append((name, n_params(build()), np.mean(accs), np.min(accs)))

print(f"{'model':26}{'params':>8}{'test acc (mean of 5)':>24}{'worst seed':>12}")
for name, p, a, w in rows:
    print(f"{name:26}{p:>8}{a:>24.3f}{w:>12.3f}")'''

_WIDEDEEP = '''# Section 2. Wide or deep, at about the same number of parameters.
# Target: a tent map applied three times. Each application folds the line in half, so the
# result has 8 linear pieces. A deep net can reuse one fold per layer.
def tent(x):
    return 1 - torch.abs(2 * x - 1)

def target(x):
    return tent(tent(tent(x)))

seed_all(1)
Xtr = torch.rand(2000, 1); ytr = target(Xtr)
Xte = torch.rand(2000, 1); yte = target(Xte)
mse = nn.MSELoss()

def wide(): return nn.Sequential(nn.Linear(1, 64), nn.ReLU(), nn.Linear(64, 1))
def deep(): return nn.Sequential(nn.Linear(1, 9), nn.ReLU(), nn.Linear(9, 9), nn.ReLU(),
                                 nn.Linear(9, 9), nn.ReLU(), nn.Linear(9, 1))

print(f"{'shape':8}{'params':>8}{'test MSE, mean':>18}{'best':>10}{'worst':>10}   (8 seeds)")
for name, build in [("wide", wide), ("deep", deep)]:
    errs = []
    for s in range(8):
        seed_all(s)
        m = fit(build(), Xtr, ytr, mse, steps=3000, lr=1e-2, batch=256)
        with torch.no_grad():
            errs.append(mse(m(Xte), yte).item())
    print(f"{name:8}{n_params(build()):>8}{np.mean(errs):>18.5f}{min(errs):>10.5f}{max(errs):>10.5f}")'''

_AUTOENC = '''# Section 3. Autoencoder: squeeze through a bottleneck, then rebuild.
# The data has 3 hidden factors spread across 20 columns, plus a little noise. The true
# answer to "how many numbers describe one row" is 3.
seed_all(3)
Z = torch.randn(3000, 3)
A = torch.randn(3, 20) / math.sqrt(3)
Xall = torch.tanh(Z @ A) + 0.05 * torch.randn(3000, 20)
Xtr, Xte = Xall[:2400], Xall[2400:]

def autoencoder(k):
    enc = nn.Sequential(nn.Linear(20, 32), nn.ReLU(), nn.Linear(32, k))
    dec = nn.Sequential(nn.Linear(k, 32), nn.ReLU(), nn.Linear(32, 20))
    return enc, dec

def pca_error(k):
    # the linear baseline: keep the top k directions of variance
    mu = Xtr.mean(0)
    U, S, Vt = torch.linalg.svd(Xtr - mu, full_matrices=False)
    P = Vt[:k]
    rec = (Xte - mu) @ P.T @ P + mu
    return ((rec - Xte) ** 2).mean().item()

print(f"noise floor (variance of the added noise): {0.05 ** 2:.5f}")
print(f"{'bottleneck':>11}{'autoencoder MSE':>18}{'PCA MSE':>12}")
for k in [1, 2, 3, 4, 8]:
    errs = []
    for s in range(3):
        seed_all(s)
        enc, dec = autoencoder(k)
        both = nn.Sequential(enc, dec)
        fit(both, Xtr, Xtr, nn.MSELoss(), steps=2500, lr=5e-3, batch=256)
        with torch.no_grad():
            errs.append(nn.MSELoss()(both(Xte), Xte).item())
    print(f"{k:>11}{np.mean(errs):>18.5f}{pca_error(k):>12.5f}")'''

_EXPANDSHRINK = '''# Section 4. The same two linear layers with the middle made wide, or narrow.
# Two teachers decide which shape is enough:
#   "rich":      a random network with a 64-wide hidden layer. Needs room to compute in.
#   "low-rank":  the identity plus a rank-2 correction. The change is small and thin.
# A narrow middle has to carry the whole input through the bottleneck, identity included.
# The third column gives it a skip connection, so it only has to learn the correction.
seed_all(4)
D = 16
Xtr = torch.randn(4000, D); Xte = torch.randn(2000, D)

rich = nn.Sequential(nn.Linear(D, 64), nn.Tanh(), nn.Linear(64, D))
U = torch.randn(D, 2) / 2; V = torch.randn(2, D) / 2
with torch.no_grad():
    y_rich_tr, y_rich_te = rich(Xtr), rich(Xte)
    y_low_tr, y_low_te = Xtr + torch.tanh(Xtr @ U) @ V, Xte + torch.tanh(Xte @ U) @ V

def student(h):
    return nn.Sequential(nn.Linear(D, h), nn.ReLU(), nn.Linear(h, D))

class WithSkip(nn.Module):
    def __init__(self, h):
        super().__init__()
        self.f = student(h)
    def forward(self, x):
        return x + self.f(x)

def run(build, ytr_, yte_):
    errs = []
    for s in range(3):
        seed_all(s)
        m = fit(build(), Xtr, ytr_, nn.MSELoss(), steps=1500, lr=5e-3, batch=256)
        with torch.no_grad():
            errs.append(nn.MSELoss()(m(Xte), yte_).item())
    return np.mean(errs)

print(f"signal variance: rich {y_rich_te.var().item():.3f}, low-rank {y_low_te.var().item():.3f}")
print(f"{'middle width':>13}{'params':>8}{'rich teacher':>16}{'low-rank teacher':>20}{'low-rank + skip':>18}   (test MSE)")
for h in [2, 4, 16, 64, 256]:
    a = run(lambda: student(h), y_rich_tr, y_rich_te)
    b = run(lambda: student(h), y_low_tr, y_low_te)
    c = run(lambda: WithSkip(h), y_low_tr, y_low_te)
    print(f"{h:>13}{n_params(student(h)):>8}{a:>16.4f}{b:>20.4f}{c:>18.4f}")'''

_TWOTOWER = '''# Section 5. Two-tower retrieval against a joint scorer.
# 400 users and 2000 items each have 16 observable features. Hidden 8-dim tastes decide the
# true affinity, which is what we want to retrieve by. Task: for each held-out user, find the
# 10 best of the 2000 items. Two ground truths:
#   "dot":   affinity is the dot product of the hidden tastes. Two towers are built for this.
#   "match": affinity rewards closeness on one taste and a dot product on another, so it
#            depends on the pair in a way no 8-number summary of each side can reproduce.
seed_all(5)
NU, NI, F, L = 400, 2000, 16, 8
tu, ti = torch.randn(NU, L), torch.randn(NI, L)
Mu, Mi = torch.randn(L, F) / math.sqrt(L), torch.randn(L, F) / math.sqrt(L)
users = tu @ Mu + 0.05 * torch.randn(NU, F)
items = ti @ Mi + 0.05 * torch.randn(NI, F)
truths = {"dot": tu @ ti.T,
          "match": -2.0 * (tu[:, :1] - ti[:, :1].T).abs() + tu[:, 1:2] * ti[:, 1:2].T}

train_u = torch.arange(0, 300); test_u = torch.arange(300, 400)
pu = train_u[torch.randint(0, 300, (60000,))]; pi = torch.randint(0, NI, (60000,))

class TwoTower(nn.Module):
    def __init__(self):
        super().__init__()
        self.u = nn.Sequential(nn.Linear(F, 64), nn.ReLU(), nn.Linear(64, 8))
        self.i = nn.Sequential(nn.Linear(F, 64), nn.ReLU(), nn.Linear(64, 8))
    def forward(self, xu, xi):
        return (self.u(xu) * self.i(xi)).sum(1, keepdim=True)

class Joint(nn.Module):
    def __init__(self):
        super().__init__()
        self.f = nn.Sequential(nn.Linear(2 * F, 128), nn.ReLU(), nn.Linear(128, 64), nn.ReLU(), nn.Linear(64, 1))
    def forward(self, xu, xi):
        return self.f(torch.cat([xu, xi], 1))

def train_pairs(model, py, steps=4000):
    opt = torch.optim.Adam(model.parameters(), lr=3e-3)
    for _ in range(steps):
        idx = torch.randint(0, len(pu), (512,))
        opt.zero_grad()
        nn.functional.mse_loss(model(users[pu[idx]], items[pi[idx]]), py[idx]).backward()
        opt.step()
    return model

def recall_at_10(affinity, score_matrix):
    truth = affinity[test_u].topk(10, dim=1).indices
    got = score_matrix.topk(10, dim=1).indices
    return np.mean([len(set(t.tolist()) & set(g.tolist())) / 10 for t, g in zip(truth, got)])

print(f"{'ground truth':13}{'model':11}{'params':>8}{'recall@10':>11}{'ms to score 100 users x 2000 items':>38}")
for tname, aff in truths.items():
    py = aff[pu, pi].unsqueeze(1)
    for name, cls in [("two-tower", TwoTower), ("joint", Joint)]:
        seed_all(0)
        m = train_pairs(cls(), py)
        with torch.no_grad():
            t0 = time.perf_counter()
            if name == "two-tower":
                scores = m.u(users[test_u]) @ m.i(items).T          # item side could be precomputed
            else:
                scores = torch.stack([m(users[u].expand(NI, F), items).squeeze(1) for u in test_u])
            ms = (time.perf_counter() - t0) * 1000
        print(f"{tname:13}{name:11}{n_params(m):>8}{recall_at_10(aff, scores):>11.3f}{ms:>38.1f}")
print(f"random retrieval would score about {10 / NI:.3f}")'''


_GAN = '''# Section 6. A tiny GAN on a one-dimensional target with two modes.
# The generator never sees the real data. It only gets the discriminator's verdicts.
def real_batch(n):
    modes = torch.randint(0, 2, (n, 1)).float() * 4 - 2          # -2 or +2
    return modes + 0.3 * torch.randn(n, 1)

def w1(a, b):
    # Wasserstein-1 distance between two equal-size 1-D samples: mean gap between sorted values
    return (torch.sort(a.flatten()).values - torch.sort(b.flatten()).values).abs().mean().item()

def run_gan(seed, steps=3000):
    seed_all(seed)
    G = nn.Sequential(nn.Linear(4, 16), nn.ReLU(), nn.Linear(16, 16), nn.ReLU(), nn.Linear(16, 1))
    Dn = nn.Sequential(nn.Linear(1, 16), nn.ReLU(), nn.Linear(16, 16), nn.ReLU(), nn.Linear(16, 1))
    og = torch.optim.Adam(G.parameters(), lr=1e-3, betas=(0.5, 0.9))
    od = torch.optim.Adam(Dn.parameters(), lr=1e-3, betas=(0.5, 0.9))
    bce = nn.BCEWithLogitsLoss()
    for _ in range(steps):
        real = real_batch(128); fake = G(torch.randn(128, 4))
        od.zero_grad()
        (bce(Dn(real), torch.ones(128, 1)) + bce(Dn(fake.detach()), torch.zeros(128, 1))).backward()
        od.step()
        og.zero_grad()
        bce(Dn(G(torch.randn(128, 4))), torch.ones(128, 1)).backward()   # fool the discriminator
        og.step()
    with torch.no_grad():
        g = G(torch.randn(4000, 4)); r = real_batch(4000)
        left = ((g > -3.0) & (g < -1.0)).float().mean().item()
        right = ((g > 1.0) & (g < 3.0)).float().mean().item()
    return w1(g, r), left, right

seed_all(99)
untrained = nn.Sequential(nn.Linear(4, 16), nn.ReLU(), nn.Linear(16, 16), nn.ReLU(), nn.Linear(16, 1))
with torch.no_grad():
    base = w1(untrained(torch.randn(4000, 4)), real_batch(4000))
print(f"untrained generator, W1 distance to real: {base:.3f}")
print(f"{'seed':>5}{'W1 to real':>12}{'share near -2':>15}{'share near +2':>15}")
for s in range(6):
    d, l, r = run_gan(s)
    print(f"{s:>5}{d:>12.3f}{l:>15.2f}{r:>15.2f}")
print("real data: about 0.50 of samples near each mode")'''


_GANRING = '''# The same game on a harder target: eight tight clusters on a ring in two dimensions.
# Count how many of the eight clusters the generator actually reaches.
ANG = torch.arange(8).float() * (2 * math.pi / 8)
CENTRES = torch.stack([2 * torch.cos(ANG), 2 * torch.sin(ANG)], 1)

def ring_batch(n):
    return CENTRES[torch.randint(0, 8, (n,))] + 0.05 * torch.randn(n, 2)

def run_ring(seed, steps=4000):
    seed_all(seed)
    G = nn.Sequential(nn.Linear(8, 64), nn.ReLU(), nn.Linear(64, 64), nn.ReLU(), nn.Linear(64, 2))
    Dn = nn.Sequential(nn.Linear(2, 64), nn.ReLU(), nn.Linear(64, 64), nn.ReLU(), nn.Linear(64, 1))
    og = torch.optim.Adam(G.parameters(), lr=1e-3, betas=(0.5, 0.9))
    od = torch.optim.Adam(Dn.parameters(), lr=1e-3, betas=(0.5, 0.9))
    bce = nn.BCEWithLogitsLoss()
    for _ in range(steps):
        real = ring_batch(128); fake = G(torch.randn(128, 8))
        od.zero_grad()
        (bce(Dn(real), torch.ones(128, 1)) + bce(Dn(fake.detach()), torch.zeros(128, 1))).backward()
        od.step()
        og.zero_grad()
        bce(Dn(G(torch.randn(128, 8))), torch.ones(128, 1)).backward()
        og.step()
    with torch.no_grad():
        g = G(torch.randn(4000, 8))
        dist = torch.cdist(g, CENTRES)
        near = (dist.min(1).values < 0.15)                 # within three cluster widths of a centre
        owner = dist.argmin(1)
        covered = sum(1 for k in range(8) if ((owner == k) & near).float().mean().item() > 0.02)
        return covered, near.float().mean().item()

print(f"{'seed':>5}{'clusters reached (of 8)':>26}{'share of samples on a cluster':>32}")
for s in range(6):
    c, q = run_ring(s)
    print(f"{s:>5}{c:>26}{q:>32.2f}")'''


_HEADS = '''# Section 7. A trunk trained on one task, a new head for another.
# Inputs hide 3 factors. Task A (lots of labels): which of 8 sign-combinations of the factors.
# Task B (few labels): is the product of the three signs positive. B needs what A taught the trunk.
seed_all(7)
Zall = torch.randn(30000, 3)
Wf = torch.randn(3, 20) / math.sqrt(3)
Xall = torch.tanh(Zall @ Wf) + 0.1 * torch.randn(30000, 20)
signs = (Zall > 0).long()
yA = signs[:, 0] * 4 + signs[:, 1] * 2 + signs[:, 2]
yB = ((signs.sum(1) % 2) == 1).long()                 # parity of the three signs

def trunk(): return nn.Sequential(nn.Linear(20, 64), nn.ReLU(), nn.Linear(64, 32), nn.ReLU())

seed_all(0)
tr = trunk(); headA = nn.Linear(32, 8)
fit(nn.Sequential(tr, headA), Xall[:20000], yA[:20000], nn.CrossEntropyLoss(), steps=1500, lr=3e-3, batch=256)
print("task A, held-out accuracy of the trained trunk + head:",
      round((nn.Sequential(tr, headA)(Xall[20000:25000]).argmax(1) == yA[20000:25000]).float().mean().item(), 3))

Xtest, ytest = Xall[25000:], yB[25000:]
def eval_B(model):
    with torch.no_grad():
        return (model(Xtest).argmax(1) == ytest).float().mean().item()

print()
print(f"{'task-B labels':>14}{'frozen trunk + new head':>26}{'fine-tune everything':>24}{'from scratch':>16}   (mean of 5 draws)")
for n in [20, 50, 200, 1000]:
    out = {"frozen": [], "tuned": [], "scratch": []}
    for s in range(5):
        seed_all(100 + s)
        idx = torch.randperm(20000)[:n]
        Xb, yb = Xall[idx], yB[idx]
        t1 = trunk(); t1.load_state_dict(tr.state_dict())
        for p in t1.parameters(): p.requires_grad = False
        h1 = nn.Linear(32, 2)
        fit(nn.Sequential(t1, h1), Xb, yb, nn.CrossEntropyLoss(), steps=400, lr=1e-2)
        out["frozen"].append(eval_B(nn.Sequential(t1, h1)))
        t2 = trunk(); t2.load_state_dict(tr.state_dict()); h2 = nn.Linear(32, 2)
        fit(nn.Sequential(t2, h2), Xb, yb, nn.CrossEntropyLoss(), steps=400, lr=2e-3)
        out["tuned"].append(eval_B(nn.Sequential(t2, h2)))
        t3 = trunk(); h3 = nn.Linear(32, 2)
        fit(nn.Sequential(t3, h3), Xb, yb, nn.CrossEntropyLoss(), steps=400, lr=3e-3)
        out["scratch"].append(eval_B(nn.Sequential(t3, h3)))
    print(f"{n:>14}{np.mean(out['frozen']):>26.3f}{np.mean(out['tuned']):>24.3f}{np.mean(out['scratch']):>16.3f}")
print("chance is 0.500")'''

NOTEBOOKS = [
("05-mlp-patterns-measured.ipynb", [
("md", _INTRO),
("code", _SETUP),
("md", """## 1 · Perceptron and binary classifier: what one layer cannot do

A perceptron is one weight-matrix multiply and an activation. As a binary classifier it
puts a single straight line through the inputs and passes the score through a sigmoid to get
a probability. XOR is the smallest problem no straight line solves: the two classes sit on
opposite diagonals."""),
("code", _XOR),
("md", """One layer sits near chance because no line separates the diagonals. One hidden layer
fixes it. This is the whole case for stacking: the second layer can bend the space the first
one cut."""),
("md", """## 2 · Wide and deep

Both networks below have about 200 parameters. The target folds the input line in half
three times, so a network that can reuse a fold once per layer has an easier job than one that
must draw all eight pieces in a single layer."""),
("code", _WIDEDEEP),
("md", """Read the spread as well as the mean. The question is not only which shape scores
lower on average but which one trains reliably from a random start."""),
("md", """## 3 · Encoder, decoder, autoencoder

An encoder maps a row to a short code. A decoder maps a code back to a row. An autoencoder
chains them and trains the output to equal the input, so the code is forced to keep what is
needed to rebuild the row. The bottleneck width is the knob: too narrow loses signal, too
wide copies the input and learns nothing."""),
("code", _AUTOENC),
("md", """Look for the elbow. Error should stop falling once the bottleneck matches the number of
hidden factors, and the floor should sit near the noise. The PCA column is the honest
baseline: if a straight-line method matches the network, the network earned nothing."""),
("md", """## 4 · Expand then shrink, shrink then expand

Both wirings are two linear layers around a nonlinearity. They differ only in whether the
middle is wider than the ends. A wide middle gives room to compute in, and costs parameters
on every token. A narrow middle is cheap and can only express a change that is itself thin."""),
("code", _EXPANDSHRINK),
("md", """The two teachers pull in opposite directions. When the needed change is rich, width
pays. When it is a small low-rank correction, a narrow middle is already enough and width
is wasted."""),
("md", """## 5 · Two-tower

A two-tower model encodes the query side and the item side separately and scores with a dot
product, so every item embedding can be computed once and stored. A joint model reads the pair
together and can capture interactions, but must be run once per candidate."""),
("code", _TWOTOWER),
("md", """The trade is accuracy against the cost of looking at every candidate. This is the same
shape as the bi-encoder and cross-encoder funnel in the retrieval lessons, and the same
conclusion follows: use the cheap scorer to shortlist and the expensive one to order the
shortlist."""),
("md", """## 6 · GAN

A generative adversarial network trains a generator to produce samples and a discriminator to
tell them from real ones. The generator is never shown the real data, only the discriminator's
verdicts. That makes it flexible and unstable."""),
("code", _GAN),
("md", """Read every seed, not the best one. A run that finds one mode and ignores the other has
a respectable-looking distance and a failed generator, which is why the share near each mode
is printed beside it. Two modes in one dimension is the easy case."""),
("code", _GANRING),
("md", """On the harder target, how many clusters the generator reaches, and how many of its
samples land on any cluster at all, is the measurement that matters. A generator can lose whole
clusters while producing sharp samples of the ones it kept."""),
("md", """## 7 · Heads

A head is the last layer or two, mapping a shared representation to a specific output. A
trained trunk can serve many heads. The practical question is how many labels a new head
needs when the trunk already knows the inputs."""),
("code", _HEADS),
("md", """## What to take to your own work

Each line is a rule and the number from this notebook that backs it.

- **Add a hidden layer when no straight line separates your classes.** One layer scored
  0.525 on XOR and one hidden layer of eight scored 1.000.
- **Do not assume depth wins at a fixed parameter budget.** The deep net's average error
  was 0.0389 against 0.0250 for the wide one, and both had bad seeds. Depth buys a shorter
  description of folded structure, not an easier optimisation.
- **Try the linear baseline before an autoencoder.** The autoencoder reached 0.0033 at a
  bottleneck of 3, the true number of factors, where PCA needed 8 to reach 0.0031.
- **Spend width where there is computation to do, and give a narrow middle a skip
  connection.** On the rich teacher, error fell from 0.0428 at width 2 to 0.0004 at width
  256. On the low-rank teacher a width-2 middle scored 0.8229 alone and 0.0212 with a skip.
- **Use two towers when the score is a dot product, and a joint model when it depends on the
  pair.** When affinity was a dot product, two towers won (0.865 against 0.819) and scored
  the whole catalogue in 0.1 ms against about 25 ms. When it depended on the pair, the joint
  model won (0.746 against 0.623) at over 100 times the scoring cost. Shortlist cheap, then
  reorder the shortlist.
- **Judge a generator by coverage, not by the quality of its samples.** On the ring of eight
  clusters the six seeds reached 2, 8, 4, 2, 3 and 0 of them.
- **Freeze the trunk when labels are scarce and tune it when they are not.** With 20 labels
  a frozen trunk scored 0.711 and training from scratch 0.604. With 1000 labels fine-tuning
  scored 0.929 and the frozen trunk 0.888.

All of it is small synthetic networks. Treat each line as a hypothesis worth testing on your
own data, with the same seeds-and-spread discipline used here."""),
]),
]
