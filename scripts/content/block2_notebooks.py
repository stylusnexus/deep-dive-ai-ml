OUTDIR = "notebooks/02-classical-ml"

_SETUP = """import pandas as pd, numpy as np
import matplotlib.pyplot as plt, seaborn as sns
from pathlib import Path

pd.set_option("display.width", 120); pd.set_option("display.max_columns", 30)
sns.set_theme(style="whitegrid")

ROOT = Path.cwd()
while not (ROOT / "data" / "turbine_readings.csv").exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
CLEAN = ROOT / "data" / "turbine_clean.csv"
if not CLEAN.exists():
    raise SystemExit("Run Block 1 notebook 02 first — it produces turbine_clean.csv")
print("reading", CLEAN.name)"""

_PIPE = """from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

NUM = ["age_years","rotor_speed_rpm","vibration_mm_s","gearbox_temp_c",
       "hours_per_year","vibration_missing"]
CAT = ["site"]
TARGET = "failed_within_90d"

df = pd.read_csv(CLEAN, parse_dates=["install_date"])
df["hours_per_year"] = df["operating_hours"] / df["age_years"].clip(lower=0.1)

X, y = df[NUM + CAT], df[TARGET]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

def make_prep():
    return ColumnTransformer([
        ("num", Pipeline([("impute", SimpleImputer(strategy="median")),
                          ("scale", StandardScaler())]), NUM),
        ("cat", Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                          ("encode", OneHotEncoder(handle_unknown="ignore"))]), CAT),
    ])

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
print(f"train {X_train.shape}  test {X_test.shape}  failure rate {y.mean():.3f}")"""

NOTEBOOKS = [
("01-metrics-and-thresholds.ipynb", [
("md", """# 01 · Metrics, Thresholds and the Curves

Block 1 ended with a logistic regression and a threshold table. This notebook
takes that model apart and asks what each number actually means.

You will build the confusion matrix by hand, derive precision and recall from it,
plot both curves, and see the specific case where AUC flatters a model that would
be unusable in production."""),
("code", _SETUP),
("code", _PIPE),
("code", """from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (confusion_matrix, classification_report,
                             roc_curve, roc_auc_score,
                             precision_recall_curve, average_precision_score)

model = Pipeline([("prep", make_prep()),
                  ("clf", LogisticRegression(max_iter=1000, class_weight="balanced"))])
model.fit(X_train, y_train)
proba = model.predict_proba(X_test)[:, 1]
pred = (proba >= 0.5).astype(int)
print("trained")"""),
("md", """## The four cells, by hand

`confusion_matrix` returns them in the order (TN, FP, FN, TP) when you ravel it.
Compute precision and recall from those four numbers rather than calling the
helpers — once — so the denominators are unambiguous."""),
("code", """tn, fp, fn, tp = confusion_matrix(y_test, pred).ravel()

print(f"true negative  {tn:>5}   healthy, called healthy")
print(f"false positive {fp:>5}   healthy, called failing   <- wasted call-out")
print(f"false negative {fn:>5}   failing, called healthy   <- missed failure")
print(f"true positive  {tp:>5}   failing, called failing")

precision = tp / (tp + fp)
recall    = tp / (tp + fn)
print(f"\\nprecision = tp/(tp+fp) = {tp}/{tp+fp} = {precision:.3f}   <- reads the predicted-positive COLUMN")
print(f"recall    = tp/(tp+fn) = {tp}/{tp+fn} = {recall:.3f}   <- reads the actual-positive ROW")
print(f"\\nsklearn agrees:")
print(classification_report(y_test, pred, target_names=["healthy","failure"], digits=3))"""),
("md", """## The ROC curve

Every point is one threshold. The diagonal is random guessing."""),
("code", """fpr, tpr, roc_thresholds = roc_curve(y_test, proba)
auc = roc_auc_score(y_test, proba)

fig, ax = plt.subplots(figsize=(6, 5.5))
ax.plot(fpr, tpr, lw=2.5, label=f"model (AUC = {auc:.3f})")
ax.plot([0, 1], [0, 1], "--", color="grey", lw=1.4, label="random (AUC = 0.500)")
i = np.argmin(np.abs(roc_thresholds - 0.5))
ax.plot(fpr[i], tpr[i], "o", ms=9, color="crimson", label="threshold = 0.5")
ax.set_xlabel("false positive rate"); ax.set_ylabel("true positive rate (recall)")
ax.set_title("ROC — receiver operating characteristic")
ax.legend(); plt.tight_layout()

print(f"AUC = {auc:.3f}")
print("Interpretation: given one random failing turbine and one random healthy one,")
print(f"the model scores the failing one higher {auc:.1%} of the time.")"""),
("md", """### Check that interpretation directly

The claim about AUC is testable, so test it rather than taking it on trust."""),
("code", """rng = np.random.default_rng(0)
pos = proba[y_test.values == 1]
neg = proba[y_test.values == 0]
draws = 200_000
wins = (rng.choice(pos, draws) > rng.choice(neg, draws)).mean()

print(f"AUC reported by sklearn : {auc:.4f}")
print(f"Random-pair experiment  : {wins:.4f}")
print("Same number, by construction — that is what AUC measures.")"""),
("md", """## The precision-recall curve, and why it disagrees

The ROC curve above looks respectable. Now look at the same model the other way."""),
("code", """prec, rec, pr_thresholds = precision_recall_curve(y_test, proba)
ap = average_precision_score(y_test, proba)
baseline = y_test.mean()

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
axes[0].plot(fpr, tpr, lw=2.5); axes[0].plot([0,1],[0,1],"--",color="grey",lw=1.2)
axes[0].set_title(f"ROC — AUC {auc:.3f}"); axes[0].set_xlabel("false positive rate"); axes[0].set_ylabel("recall")
axes[1].plot(rec, prec, lw=2.5, color="darkorange")
axes[1].axhline(baseline, ls="--", color="grey", lw=1.2, label=f"random = {baseline:.3f}")
axes[1].set_title(f"Precision-Recall — AP {ap:.3f}"); axes[1].set_xlabel("recall"); axes[1].set_ylabel("precision")
axes[1].legend(); plt.tight_layout()

print(f"AUC (ROC)             : {auc:.3f}   looks strong")
print(f"Average precision     : {ap:.3f}   much less flattering")
print(f"Random-guessing AP    : {baseline:.3f}")"""),
("md", """### Why the two disagree

The false positive rate divides by the number of genuine negatives, and there are
many of them. So a large *absolute* number of false alarms still produces a small
*rate*, and the ROC curve stays reassuring.

Precision divides by what you flagged. False alarms hurt it directly and visibly.

**On imbalanced problems, read the precision-recall curve.** The ROC curve is
answering a question your operations team did not ask."""),
("code", """# the same fact in call-out terms
for t in [0.3, 0.5, 0.7]:
    p = (proba >= t).astype(int)
    a, b, c, d = confusion_matrix(y_test, p).ravel()
    print(f"threshold {t}:  false-positive RATE {b/(a+b):.3f}   "
          f"but {b:>3} actual wasted call-outs, and {c:>3} missed failures")"""),
("md", """## Choosing the threshold from costs

The model cannot choose this. It is a business decision, and it becomes obvious
once you attach money to the two error types.

Suppose a wasted call-out costs £1,500 (a crew, a vehicle, a day) and a missed
failure costs £9,000 (an emergency repair and lost generation)."""),
("code", """COST_FALSE_ALARM = 1_500
COST_MISSED      = 9_000

rows = []
for t in np.arange(0.05, 0.96, 0.05):
    p = (proba >= t).astype(int)
    a, b, c, d = confusion_matrix(y_test, p).ravel()
    rows.append({"threshold": round(t, 2),
                 "recall": round(d/(d+c), 3),
                 "precision": round(d/(d+b), 3) if (d+b) else 0.0,
                 "missed": c, "false_alarms": b,
                 "cost": b*COST_FALSE_ALARM + c*COST_MISSED})
costs = pd.DataFrame(rows)
best = costs.loc[costs["cost"].idxmin()]
display(costs)
print(f"\\nlowest expected cost at threshold {best.threshold}: "
      f"£{best.cost:,.0f}  ({int(best.missed)} missed, {int(best.false_alarms)} false alarms)")"""),
("code", """fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(costs["threshold"], costs["cost"], marker="o", lw=2)
ax.axvline(best.threshold, ls="--", color="crimson",
           label=f"minimum at {best.threshold}")
ax.axvline(0.5, ls=":", color="grey", label="default 0.5")
ax.set_xlabel("threshold"); ax.set_ylabel("expected cost (£)")
ax.set_title("The threshold is a business decision")
ax.legend(); plt.tight_layout()"""),
("md", """Note where the default of 0.5 sits relative to the minimum. It is a convention
inherited from balanced problems, and on this data it is simply the wrong choice.

---

## Your turn

1. Set the missed-failure cost to £15,000 and re-run. The optimum moves to the
   lowest threshold on the grid — inspect everything. That is a correct answer,
   not a bug: at a 10:1 cost ratio on this failure rate, blanket inspection really
   is cheapest. Satisfy yourself that it is right before moving on.
2. At what cost ratio does 0.5 become optimal?
3. The model was trained with `class_weight="balanced"`. Refit without it and
   compare the ROC curves. Which metric moves most?"""),
]),

("02-model-ladder.ipynb", [
("md", """# 02 · Climbing the Ladder

Five models, same split, same folds, same metric. The point is not to find the
best one — it is to see how little separates them, and to build the habit of
proving that a step up the ladder was worth taking."""),
("code", _SETUP),
("code", _PIPE),
("md", """## Rung 0 and 1 — the baselines

`DummyClassifier` is the majority-class baseline, written down so it appears in
the comparison rather than living in someone's memory."""),
("code", """from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier

MODELS = {
    "0 majority class":     DummyClassifier(strategy="most_frequent"),
    "1 single tree (d=3)":  DecisionTreeClassifier(max_depth=3, class_weight="balanced", random_state=0),
    "2 logistic regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
    "3 random forest":      RandomForestClassifier(n_estimators=300, class_weight="balanced",
                                                   random_state=0, n_jobs=-1),
    "4 gradient boosting":  HistGradientBoostingClassifier(max_depth=4, learning_rate=0.06,
                                                           max_iter=300, early_stopping=True,
                                                           class_weight="balanced", random_state=0),
}
print(f"{len(MODELS)} models on the ladder")"""),
("md", """## Same folds, same metric, spread reported

Recall is the metric, chosen before looking at anything, because a missed failure
is the expensive error on this problem.

**One caution before reading the table.** Recall is measured at the default 0.5
threshold, and different model families produce differently-shaped probability
distributions. A model that is well calibrated at 0.5 will look better than one
that ranks just as well but concentrates its probabilities differently — which is
a fact about the threshold, not about the model.

So we report **average precision** alongside it. That one is threshold-free, and
it is the fair comparator between families."""),
("code", """import time
rows = []
for name, clf in MODELS.items():
    pipe = Pipeline([("prep", make_prep()), ("clf", clf)])
    t0 = time.perf_counter()
    rec = cross_val_score(pipe, X_train, y_train, cv=cv, scoring="recall", n_jobs=-1)
    ap  = cross_val_score(pipe, X_train, y_train, cv=cv, scoring="average_precision", n_jobs=-1)
    rows.append({"model": name,
                 "recall@0.5": rec.mean().round(3),
                 "recall_sd": rec.std().round(3),
                 "avg_precision": ap.mean().round(3),
                 "ap_sd": ap.std().round(3),
                 "fit_seconds": round(time.perf_counter() - t0, 1)})
ladder = pd.DataFrame(rows)
ladder"""),
("code", """fig, ax = plt.subplots(figsize=(9, 4.5))
fig, axes = plt.subplots(1, 2, figsize=(13, 4.5), sharey=True)
axes[0].errorbar(ladder["recall@0.5"], ladder["model"], xerr=ladder["recall_sd"],
                 fmt="o", ms=9, capsize=5, lw=2)
axes[0].set_xlabel("recall at threshold 0.5 (+/- 1 sd)")
axes[0].set_title("Threshold-dependent — compare with care")
axes[1].errorbar(ladder["avg_precision"], ladder["model"], xerr=ladder["ap_sd"],
                 fmt="o", ms=9, capsize=5, lw=2, color="darkorange")
axes[1].set_xlabel("average precision (+/- 1 sd)")
axes[1].set_title("Threshold-free — the fair comparison")
plt.tight_layout()"""),
("md", """### Read the error bars before the means

Where the intervals overlap heavily, the ranking is not established. Reporting the
top model as "best" in that situation is a claim the data does not support.

The honest sentence is usually: *these three are indistinguishable on this data,
so choose on cost, interpretability and operational burden instead.*"""),
("code", """# is the gap between the top two bigger than their variation?
top2 = ladder.nlargest(2, "avg_precision").reset_index(drop=True)
gap = top2.loc[0, "avg_precision"] - top2.loc[1, "avg_precision"]
noise = (top2.loc[0, "ap_sd"] + top2.loc[1, "ap_sd"]) / 2
print(f"{top2.loc[0,'model']}  vs  {top2.loc[1,'model']}")
print(f"gap between means : {gap:.3f}")
print(f"typical fold sd   : {noise:.3f}")
print(f"\\n{'The gap is inside the noise — not a demonstrated difference.' if gap < noise else 'The gap exceeds typical fold variation — worth investigating further.'}")"""),
("md", """## What each rung costs beyond its score

A score is one column of the decision. Here are the others."""),
("code", """cost_table = pd.DataFrame([
 {"model":"logistic regression","explains itself":"yes — coefficients","tuning":"almost none",
  "serving":"trivial","drift response":"refit, seconds"},
 {"model":"random forest","explains itself":"partly — importances","tuning":"almost none",
  "serving":"easy","drift response":"refit, seconds"},
 {"model":"gradient boosting","explains itself":"partly — importances","tuning":"real",
  "serving":"easy","drift response":"refit and retune"},
])
cost_table"""),
("md", """## Feature importance, and the trap in it

The default tree importance is biased toward high-cardinality features — a
continuous variable offers hundreds of split points, a binary flag offers one.
Permutation importance asks the question people think they are asking: does the
model actually rely on this?"""),
("code", """from sklearn.inspection import permutation_importance

rf = Pipeline([("prep", make_prep()),
               ("clf", RandomForestClassifier(n_estimators=300, class_weight="balanced",
                                              random_state=0, n_jobs=-1))]).fit(X_train, y_train)

r = permutation_importance(rf, X_test, y_test, n_repeats=10,
                           random_state=0, scoring="recall", n_jobs=-1)
imp = (pd.DataFrame({"feature": NUM + CAT,
                     "importance": r.importances_mean.round(4),
                     "sd": r.importances_std.round(4)})
       .sort_values("importance", ascending=False))
imp"""),
("md", """---

## What this notebook established

- The majority-class baseline, written down
- Five models on identical folds with the same metric
- Whether the top gap survives fold variation — usually it does not
- The costs that a score does not capture
- Which features the model actually relies on, measured by permutation

## Your turn

1. Add `hours_per_year` to the feature list and re-run. Does any model move
   beyond its error bar?
2. Change the metric to `average_precision` and re-run. Does the ranking change?
   What does it mean if it does?
3. Drop the strongest feature from `imp` and re-run the ladder. How much of the
   performance was that one column?"""),
]),
("03-neural-networks.ipynb", [
("md", """# 03 · Neural Networks, Both Backends

Two things happen here. You build the same network in Keras and in raw PyTorch,
and you run the Keras version under both backends to see for yourself that the
code is genuinely portable — and that the results are not bit-identical.

Then you compare it against the boosted tree from notebook 02, honestly."""),
("code", _SETUP),
("code", _PIPE),
("md", """## The Keras version

One environment variable chooses the engine. Set it **before** importing keras —
this is the part people get wrong, because the backend is fixed at import."""),
("code", """import os
os.environ["KERAS_BACKEND"] = "tensorflow"      # must be set before the import below

import keras
print("keras", keras.__version__, "| backend:", keras.backend.backend())"""),
("code", """from sklearn.metrics import average_precision_score, recall_score

prep = make_prep().fit(X_train)
Xtr = prep.transform(X_train); Xte = prep.transform(X_test)
Xtr = np.asarray(Xtr.todense() if hasattr(Xtr, "todense") else Xtr, dtype="float32")
Xte = np.asarray(Xte.todense() if hasattr(Xte, "todense") else Xte, dtype="float32")
ytr = y_train.values.astype("float32"); yte = y_test.values.astype("float32")
print("features after preprocessing:", Xtr.shape[1])"""),
("md", """### Normalisation is not optional

`make_prep()` already scales the numeric columns. That is the single most common
reason a network refuses to train — unscaled features make the loss surface
pathological, and no learning rate rescues it."""),
("code", """def build(seed=0):
    keras.utils.set_random_seed(seed)
    m = keras.Sequential([
        keras.layers.Input((Xtr.shape[1],)),
        keras.layers.Dense(32, activation="relu"),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(16, activation="relu"),
        keras.layers.Dense(1, activation="sigmoid"),
    ])
    m.compile(optimizer=keras.optimizers.Adam(1e-3),
              loss="binary_crossentropy", metrics=["accuracy"])
    return m

build().summary()"""),
("md", """## First: prove the loop works

Before tuning anything, overfit a single small batch. A correctly wired network
memorises eight examples trivially. If it cannot, the bug is in the wiring, the
data or the loss — and no hyperparameter will find it.

This takes seconds and it is the highest-value ninety seconds in deep learning."""),
("code", """tiny = build()
h = tiny.fit(Xtr[:8], ytr[:8], epochs=200, verbose=0)
print(f"loss on 8 examples after 200 epochs: {h.history['loss'][-1]:.5f}")
print("✅ loop is wired" if h.history['loss'][-1] < 0.05
      else "❌ cannot overfit 8 rows — stop and debug the loop, not the hyperparameters")"""),
("md", """## Now train properly

Class weights, because the rare class must cost more. Early stopping, because a
network will fit noise indefinitely if you let it."""),
("code", """cw = {0: 1.0, 1: float((ytr == 0).sum() / (ytr == 1).sum())}
print("class weights:", {k: round(v, 2) for k, v in cw.items()})

model = build()
hist = model.fit(Xtr, ytr, validation_split=0.2, epochs=200, batch_size=64,
                 class_weight=cw, verbose=0,
                 callbacks=[keras.callbacks.EarlyStopping(patience=15, restore_best_weights=True,
                                                          monitor="val_loss")])
print(f"stopped after {len(hist.history['loss'])} epochs")"""),
("code", """fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(hist.history["loss"], label="training loss", lw=2)
ax.plot(hist.history["val_loss"], label="validation loss", lw=2)
best = int(np.argmin(hist.history["val_loss"]))
ax.axvline(best, ls="--", color="crimson", label=f"best epoch = {best}")
ax.set_xlabel("epoch"); ax.set_ylabel("loss")
ax.set_title("Where the two curves separate is where it starts memorising")
ax.legend(); plt.tight_layout()"""),
("md", """## The same code, the other backend

Restarting the kernel to change backend is tedious, so run it as a subprocess.
The point is that **the model code is byte-identical** — only the environment
variable differs."""),
("code", """import subprocess, sys, textwrap, json

SCRIPT = textwrap.dedent('''
    import os, sys, json
    os.environ["KERAS_BACKEND"] = sys.argv[1]
    import numpy as np, keras
    X = np.load(sys.argv[2]); y = np.load(sys.argv[3])
    keras.utils.set_random_seed(0)
    m = keras.Sequential([
        keras.layers.Input((X.shape[1],)),
        keras.layers.Dense(32, activation="relu"),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(16, activation="relu"),
        keras.layers.Dense(1, activation="sigmoid"),
    ])
    m.compile(optimizer=keras.optimizers.Adam(1e-3), loss="binary_crossentropy")
    h = m.fit(X, y, epochs=5, batch_size=64, verbose=0)
    print(json.dumps({"backend": keras.backend.backend(),
                      "final_loss": round(float(h.history["loss"][-1]), 6)}))
''')

tmp = Path("/tmp"); np.save(tmp/"Xtr.npy", Xtr); np.save(tmp/"ytr.npy", ytr)
(tmp/"backend_test.py").write_text(SCRIPT)

for backend in ["tensorflow", "torch"]:
    r = subprocess.run([sys.executable, str(tmp/"backend_test.py"), backend,
                        str(tmp/"Xtr.npy"), str(tmp/"ytr.npy")],
                       capture_output=True, text=True)
    line = [l for l in r.stdout.splitlines() if l.startswith("{")]
    print(json.loads(line[-1]) if line else f"{backend}: not available in this environment")"""),
("md", """### Read that carefully

Same architecture, same seed, same data — and the final losses differ.

Random number generation and floating-point operation ordering are not identical
across backends. **Reproducibility in deep learning is approximate.** Any test or
evaluation you write must tolerate small differences rather than assert equality,
and any claim that a change "improved" something by a fraction of a percent needs
repeats before you believe it."""),
("md", """## The same network in raw PyTorch

Keras's `fit` is this loop. Writing it once makes that concrete."""),
("code", """import torch, torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader

torch.manual_seed(0)
net = nn.Sequential(nn.Linear(Xtr.shape[1], 32), nn.ReLU(), nn.Dropout(0.2),
                    nn.Linear(32, 16), nn.ReLU(), nn.Linear(16, 1))
loss_fn = nn.BCEWithLogitsLoss(pos_weight=torch.tensor([cw[1]]))
opt = torch.optim.Adam(net.parameters(), lr=1e-3)

loader = DataLoader(TensorDataset(torch.tensor(Xtr), torch.tensor(ytr).unsqueeze(1)),
                    batch_size=64, shuffle=True)

for epoch in range(30):
    net.train()
    for xb, yb in loader:
        opt.zero_grad()                       # 1 · clear last step's gradients
        loss = loss_fn(net(xb), yb)           # 2 · forward pass and loss
        loss.backward()                       # 3 · backpropagate
        opt.step()                            # 4 · apply the update
print(f"final batch loss: {loss.item():.4f}")"""),
("md", """Four lines, and they are exactly what `fit()` does for you. Everything else
Keras adds — batching, metrics, callbacks, early stopping, progress bars — is
convenience around those four."""),
("md", """## The honest comparison

Against the boosted tree from notebook 02, on the same test set, threshold-free."""),
("code", """from sklearn.ensemble import HistGradientBoostingClassifier

gb = Pipeline([("prep", make_prep()),
               ("clf", HistGradientBoostingClassifier(max_depth=4, learning_rate=0.06,
                                                      max_iter=300, early_stopping=True,
                                                      class_weight="balanced", random_state=0))])
gb.fit(X_train, y_train)

nn_proba = model.predict(Xte, verbose=0).ravel()
gb_proba = gb.predict_proba(X_test)[:, 1]

import time
comparison = pd.DataFrame([
  {"model": "neural network (Keras)",
   "average_precision": round(average_precision_score(yte, nn_proba), 3),
   "recall@0.5": round(recall_score(yte, (nn_proba >= 0.5).astype(int)), 3)},
  {"model": "gradient boosting",
   "average_precision": round(average_precision_score(yte, gb_proba), 3),
   "recall@0.5": round(recall_score(yte, (gb_proba >= 0.5).astype(int)), 3)},
])
comparison"""),
("md", """### What to make of that

If the tree matches or beats the network — which on tabular data it usually does —
that is the result, not a failure of your network. The network needed
normalisation, an architecture, a learning rate, an epoch budget, dropout and
early stopping. The tree needed none of those.

**Build the network to learn how. Ship the one that is cheaper to operate.**

---

## Your turn

1. Remove the scaling step from the pipeline and retrain the network. How badly
   does it break? Now do the same to the boosted tree.
2. Set `class_weight` to `None` in both. Which model's recall moves more, and why?
3. Add two more hidden layers. Does validation loss improve, or does the gap
   between the curves just widen sooner?"""),
]),

("04-time-series.ipynb", [
("md", """# 04 · Time Series and Walk-Forward Validation

A different dataset: `turbine_daily.csv`, two years of daily readings for forty
turbines. It has trend, weekly seasonality, a regime change, a telemetry gap, and
failures preceded by a rising run-up.

The task: predict whether a turbine will fail in the next 7 days.

You will build it wrong first — with a random split — see the excellent score,
then do it properly and watch the number fall to something honest."""),
("code", _SETUP),
("code", """ts = pd.read_csv(ROOT / "data" / "turbine_daily.csv", parse_dates=["date"])
ts = ts.sort_values(["turbine_id", "date"]).reset_index(drop=True)
print(f"{len(ts):,} rows | {ts['turbine_id'].nunique()} turbines")
print(f"{ts['date'].min().date()} to {ts['date'].max().date()}")
ts.head()"""),
("md", """## Always plot it first

Trend, seasonality, level shifts and gaps are visible in one chart and invisible
in `describe()`."""),
("code", """fig, axes = plt.subplots(2, 1, figsize=(13, 7), sharex=True)
for tid in ["T000", "T007", "T019"]:
    sub = ts[ts["turbine_id"] == tid]
    axes[0].plot(sub["date"], sub["vibration_mm_s"], lw=1, label=tid)
axes[0].set_ylabel("vibration mm/s"); axes[0].legend(); axes[0].set_title("Three turbines")

daily = ts.groupby("date")["vibration_mm_s"].mean()
axes[1].plot(daily.index, daily.values, lw=1.2, color="darkorange")
axes[1].set_ylabel("fleet mean"); axes[1].set_title("Fleet average — look for the step")
plt.tight_layout()"""),
("md", """### Two things that chart shows

**A step change** partway through — a sensor recalibration. Data before and after
are not on the same scale, which is an argument for a sliding window rather than
an expanding one.

**A gap** where six turbines stopped reporting for a fortnight. Lag features
computed naively across that gap will silently compare readings two weeks apart
as though they were consecutive."""),
("code", """gaps = (ts.groupby("turbine_id")["date"].apply(lambda d: d.diff().dt.days.max()))
print("largest gap between consecutive readings, per turbine:")
print(gaps.value_counts().to_string())
print("\\nTurbines with a gap longer than one day:", (gaps > 1).sum())"""),
("md", """## Build the target and the features

Target: does this turbine fail within the next 7 days?

Features must only ever look **backwards**. Every rolling window below is
computed within a turbine and shifted, so today's row never contains today's
value or any future one."""),
("code", """g = ts.groupby("turbine_id", group_keys=False)

# target: failure in the NEXT 7 days (looks forward — this is the label, not a feature)
ts["target"] = (g["failure"]
                .apply(lambda s: s.iloc[::-1].rolling(7, min_periods=1).max().iloc[::-1])
                .astype(int))

# features: backwards only. shift(1) so today's reading is excluded.
for col in ["vibration_mm_s", "gearbox_temp_c", "power_output_kw"]:
    prev = g[col].shift(1)
    ts[f"{col}_lag1"]   = prev
    ts[f"{col}_roll7"]  = prev.groupby(ts["turbine_id"]).rolling(7,  min_periods=3).mean().values
    ts[f"{col}_roll30"] = prev.groupby(ts["turbine_id"]).rolling(30, min_periods=7).mean().values
    ts[f"{col}_std7"]   = prev.groupby(ts["turbine_id"]).rolling(7,  min_periods=3).std().values

ts["vib_dev_from_norm"] = ts["vibration_mm_s_lag1"] - ts["vibration_mm_s_roll30"]
ts["dow"] = ts["date"].dt.dayofweek

FEATS = sorted({c for c in ts.columns if c.endswith(("_lag1","_roll7","_roll30","_std7"))} | {"vib_dev_from_norm", "dow"})
data = ts.dropna(subset=FEATS).reset_index(drop=True)
print(f"{len(data):,} usable rows, {len(FEATS)} features, target rate {data['target'].mean():.3%}")"""),
("md", """## The wrong way, so you can see the size of the lie"""),
("code", """from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import average_precision_score
from sklearn.model_selection import train_test_split

Xr, yr = data[FEATS], data["target"]
Xtr_r, Xte_r, ytr_r, yte_r = train_test_split(Xr, yr, test_size=0.25, random_state=0, stratify=yr)

m_random = HistGradientBoostingClassifier(max_depth=4, learning_rate=0.06, max_iter=250,
                                          class_weight="balanced", random_state=0).fit(Xtr_r, ytr_r)
ap_random = average_precision_score(yte_r, m_random.predict_proba(Xte_r)[:, 1])
print(f"RANDOM split  → average precision {ap_random:.3f}")
print(f"(random-guessing baseline is {yr.mean():.3f})")"""),
("md", """## The right way — split by time, with a gap

Two corrections. Train on the past and test on the future. And leave a **gap**
matching the horizon you are predicting: the target looks 7 days ahead, so
training rows within 7 days of the test period would share outcome information
with it."""),
("code", """cut = pd.Timestamp(data["date"].quantile(0.75))
gap_days = 7

GAP = np.timedelta64(gap_days, "D")   # pd.Timedelta(days=) warns under numpy 2.5
train = data[data["date"] <  cut - GAP]
test  = data[data["date"] >= cut]

print(f"train: {train['date'].min().date()} to {train['date'].max().date()}  ({len(train):,} rows)")
print(f"gap  : {gap_days} days")
print(f"test : {test['date'].min().date()} to {test['date'].max().date()}  ({len(test):,} rows)")

m_time = HistGradientBoostingClassifier(max_depth=4, learning_rate=0.06, max_iter=250,
                                        class_weight="balanced", random_state=0
                                        ).fit(train[FEATS], train["target"])
ap_time = average_precision_score(test["target"], m_time.predict_proba(test[FEATS])[:, 1])

print(f"\\nRANDOM split → {ap_random:.3f}")
print(f"TIME split   → {ap_time:.3f}")
print(f"\\nThe random split was optimistic by {ap_random - ap_time:+.3f}.")
print("Nothing about the model changed. Only the question it was asked.")"""),
("md", """## Walk-forward validation

One time split is one estimate. Walk the boundary forward and you get several,
which tells you whether performance is stable or drifting."""),
("code", """from sklearn.model_selection import TimeSeriesSplit

dates = np.sort(data["date"].unique())
folds, rows = TimeSeriesSplit(n_splits=5), []

for i, (tr_idx, te_idx) in enumerate(folds.split(dates), 1):
    tr_end, te_start, te_end = dates[tr_idx[-1]], dates[te_idx[0]], dates[te_idx[-1]]
    tr = data[data["date"] <= pd.Timestamp(tr_end) - GAP]
    te = data[(data["date"] >= te_start) & (data["date"] <= te_end)]
    if te["target"].sum() < 3:
        continue
    mdl = HistGradientBoostingClassifier(max_depth=4, learning_rate=0.06, max_iter=250,
                                         class_weight="balanced", random_state=0
                                         ).fit(tr[FEATS], tr["target"])
    rows.append({"fold": i,
                 "train_to": pd.Timestamp(tr_end).date(),
                 "test_from": pd.Timestamp(te_start).date(),
                 "n_test": len(te), "positives": int(te["target"].sum()),
                 "avg_precision": round(average_precision_score(
                     te["target"], mdl.predict_proba(te[FEATS])[:, 1]), 3)})
wf = pd.DataFrame(rows)
display(wf)
print(f"\\nmean {wf['avg_precision'].mean():.3f}   sd {wf['avg_precision'].std():.3f}")"""),
("code", """fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(wf["fold"], wf["avg_precision"], marker="o", lw=2, label="walk-forward folds")
ax.axhline(data["target"].mean(), ls="--", color="grey", label="random baseline")
ax.axhline(ap_random, ls=":", color="crimson", label=f"random split (optimistic) {ap_random:.3f}")
ax.set_xlabel("fold (later = further into the future)"); ax.set_ylabel("average precision")
ax.set_title("Performance across time, honestly measured")
ax.legend(); plt.tight_layout()"""),
("md", """### Reading the folds

If later folds are consistently worse, the process is drifting and you need to
retrain more often — or the regime change is hurting you and a sliding window
would beat an expanding one.

If they scatter without trend, that spread **is** your uncertainty. A single time
split would have given you one number from that spread and no way to know how
lucky it was."""),
("md", """## The naive baseline

The majority-class baseline of time series: predict that tomorrow looks like
today. Compute it before believing any model."""),
("code", """naive = test["vibration_mm_s_lag1"] > train["vibration_mm_s_lag1"].quantile(0.90)
ap_naive = average_precision_score(test["target"], naive.astype(float))

print(f"naive (yesterday's vibration in the top decile) : {ap_naive:.3f}")
print(f"model                                            : {ap_time:.3f}")
print(f"random guessing                                  : {test['target'].mean():.3f}")
print(f"\\n{'The model beats the naive rule.' if ap_time > ap_naive else 'The model does NOT beat a one-line rule — that is the finding.'}")"""),
("md", """---

## What this notebook established

- Plot before modelling: the regime change and the telemetry gap are both visible
- Rolling features must be shifted and computed within each turbine
- A random split was optimistic, and by how much
- The gap between train and test must match the prediction horizon
- Walk-forward gives you a spread rather than one lucky number
- The naive rule, computed and compared

## Your turn

1. Remove the `shift(1)` from the rolling features and re-run the time split.
   The score jumps. Explain precisely which future information leaked in.
2. Use a sliding window (drop data before the regime change) instead of an
   expanding one. Do the later folds improve?
3. Change the horizon from 7 days to 30. Does the task get easier or harder, and
   does the required gap change?"""),
]),
]
