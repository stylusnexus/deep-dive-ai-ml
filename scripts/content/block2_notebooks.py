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
]
