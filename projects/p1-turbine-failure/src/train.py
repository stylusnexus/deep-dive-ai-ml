#!/usr/bin/env python3
"""Wind turbine failure prediction, end to end.

Deliberately written as a script rather than a notebook: the deliverable is a
report someone can act on, and a script is reproducible in a way a notebook with
out-of-order cells is not.

Every step here is one the course argued for. The leakage audit, the baseline,
the threshold-free comparison and the cost-chosen threshold are not optional
extras — they are what separates a number from a decision.
"""
from __future__ import annotations
import argparse, json, pathlib, sys
import numpy as np, pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = pathlib.Path(__file__).resolve().parents[3]
NUM = ["age_years", "rotor_speed_rpm", "vibration_mm_s",
       "gearbox_temp_c", "hours_per_year", "vibration_missing"]
CAT = ["site"]
TARGET = "failed_within_90d"
SEED = 42

# Columns dropped in Block 1 because they encode the outcome. Kept here by name so
# the audit is visible in the code rather than remembered.
KNOWN_LEAKS = ["maintenance_ticket_raised"]


def load() -> pd.DataFrame:
    path = ROOT / "data" / "turbine_clean.csv"
    if not path.exists():
        sys.exit("turbine_clean.csv not found — run notebooks/01-python-eda/02 first.")
    df = pd.read_csv(path, parse_dates=["install_date"])
    df["hours_per_year"] = df["operating_hours"] / df["age_years"].clip(lower=0.1)
    return df


def audit_leakage(df: pd.DataFrame) -> list[str]:
    """Every feature answers: would I have this value, with this content, at
    prediction time? Anything perfectly separating the classes is a suspect."""
    findings = []
    for col in KNOWN_LEAKS:
        if col in df.columns:
            findings.append(f"**{col}** is present and must be dropped — it is populated "
                            "only after a failure has been recorded")
        else:
            findings.append(f"**{col}** already removed upstream (Block 1 notebook 02). "
                            "It encoded the outcome: every URGENT ticket corresponded to a failure")
    for col in NUM:
        if col not in df:
            continue
        grouped = df.groupby(TARGET)[col].mean()
        if grouped.isna().any():
            continue
        spread = abs(grouped.iloc[1] - grouped.iloc[0]) / (df[col].std() or 1)
        if spread > 3:
            findings.append(f"{col}: separates the classes by {spread:.1f} sd — verify it is not a leak")
    findings.append(f"Checked {len(NUM)} numeric features for implausible class separation "
                    "(>3 standard deviations), which is the signature of a leak")
    return findings


def md_table(df: pd.DataFrame, floatfmt: str = "{:.3f}") -> str:
    """Markdown table without pulling in tabulate. Stdlib and pandas only."""
    def cell(v):
        return floatfmt.format(v) if isinstance(v, float) else str(v)
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |",
             "|" + "|".join("---" for _ in cols) + "|"]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(cell(row[c]) for c in cols) + " |")
    return "\n".join(lines)


def build_prep() -> ColumnTransformer:
    return ColumnTransformer([
        ("num", Pipeline([("impute", SimpleImputer(strategy="median")),
                          ("scale", StandardScaler())]), NUM),
        ("cat", Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                          ("encode", OneHotEncoder(handle_unknown="ignore"))]), CAT),
    ])


def models() -> dict[str, object]:
    return {
        "baseline (majority class)": DummyClassifier(strategy="most_frequent"),
        "logistic regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
        "random forest": RandomForestClassifier(n_estimators=300, class_weight="balanced",
                                                random_state=SEED, n_jobs=-1),
        "gradient boosting": HistGradientBoostingClassifier(max_depth=4, learning_rate=0.06,
                                                            max_iter=300, early_stopping=True,
                                                            class_weight="balanced",
                                                            random_state=SEED),
    }


def compare(X, y) -> pd.DataFrame:
    """Threshold-free, identical folds. Recall at a fixed 0.5 is not a fair
    comparator across model families."""
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    rows = []
    for name, clf in models().items():
        pipe = Pipeline([("prep", build_prep()), ("clf", clf)])
        ap = cross_val_score(pipe, X, y, cv=cv, scoring="average_precision", n_jobs=-1)
        rows.append({"model": name, "avg_precision": ap.mean(), "sd": ap.std()})
    return pd.DataFrame(rows).sort_values("avg_precision", ascending=False).reset_index(drop=True)


def threshold_table(y_true, proba, cost_fa: float, cost_missed: float) -> pd.DataFrame:
    rows = []
    for t in np.arange(0.05, 0.96, 0.05):
        tn, fp, fn, tp = confusion_matrix(y_true, (proba >= t).astype(int)).ravel()
        rows.append({"threshold": round(t, 2),
                     "recall": round(tp / (tp + fn), 3) if (tp + fn) else 0.0,
                     "precision": round(tp / (tp + fp), 3) if (tp + fp) else 0.0,
                     "missed_failures": int(fn), "false_alarms": int(fp),
                     "expected_cost": int(fp * cost_fa + fn * cost_missed)})
    return pd.DataFrame(rows)


def main() -> None:
    ap_ = argparse.ArgumentParser(description=__doc__)
    ap_.add_argument("--costs", nargs=2, type=float, default=[1500.0, 9000.0],
                     metavar=("FALSE_ALARM", "MISSED_FAILURE"))
    args = ap_.parse_args()
    cost_fa, cost_missed = args.costs

    out = pathlib.Path(__file__).resolve().parent.parent
    (out / "artifacts").mkdir(exist_ok=True)

    df = load()
    X, y = df[NUM + CAT], df[TARGET]
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2,
                                              random_state=SEED, stratify=y)

    leaks = audit_leakage(df)
    baseline_acc = 1 - y.mean()
    board = compare(X_tr, y_tr)

    best_name = board.loc[0, "model"]
    best = Pipeline([("prep", build_prep()), ("clf", models()[best_name])]).fit(X_tr, y_tr)
    proba = best.predict_proba(X_te)[:, 1]

    table = threshold_table(y_te, proba, cost_fa, cost_missed)
    chosen = table.loc[table["expected_cost"].idxmin()]

    # is the winner demonstrably better than the runner-up?
    gap = board.loc[0, "avg_precision"] - board.loc[1, "avg_precision"]
    noise = (board.loc[0, "sd"] + board.loc[1, "sd"]) / 2
    demonstrable = gap > noise

    report = f"""# Wind Turbine Failure Prediction — Report

Generated by `src/train.py`. Costs assumed: £{cost_fa:,.0f} per wasted call-out,
£{cost_missed:,.0f} per missed failure.

## Baseline

Always predicting "no failure" is **{baseline_acc:.1%} accurate**. Every accuracy
figure below is judged against that number, and the failure rate is {y.mean():.1%}.

## Leakage audit

{chr(10).join('- ' + f for f in leaks)}

## Model comparison

Five-fold cross-validated average precision — threshold-free, so the comparison is
fair across model families.

{md_table(board)}

Gap between the top two: **{gap:.3f}**. Typical fold variation: **{noise:.3f}**.

**{'The winner is demonstrably better than the runner-up.' if demonstrable else
   'The top two are NOT distinguishable on this data. Choose on interpretability and operating cost, not on the score.'}**

## The decision

Selected model: **{best_name}**, at a threshold of **{chosen.threshold}**.

At that threshold, on the held-out set:

- catches **{chosen.recall:.1%}** of failures ({int(chosen.missed_failures)} missed)
- raises **{int(chosen.false_alarms)}** false alarms
- expected cost **£{int(chosen.expected_cost):,}** against
  £{int(table['expected_cost'].max()):,} at the worst threshold on the grid

Note where the conventional 0.5 sits: cost
£{int(table.loc[table.threshold == 0.5, 'expected_cost'].iloc[0]):,}. It is a
convention inherited from balanced problems, not an answer.

## Threshold table

{md_table(table)}

## What would make me distrust this in six months

- The sensor fleet is recalibrated, shifting the vibration distribution
- The maintenance policy changes, which changes what "failure within 90 days" means
- Missingness stops being informative because the faulty sensors get replaced —
  the `vibration_missing` flag is predictive *because* sensors fail on shaking
  turbines, and that relationship is a property of the current hardware
- Input distributions drift far enough that the chosen threshold is no longer
  cost-optimal, even if the ranking still holds
"""
    (out / "report.md").write_text(report)
    board.to_csv(out / "artifacts" / "model_comparison.csv", index=False)
    table.to_csv(out / "artifacts" / "threshold_table.csv", index=False)
    (out / "artifacts" / "summary.json").write_text(json.dumps({
        "baseline_accuracy": round(baseline_acc, 4),
        "selected_model": best_name,
        "threshold": float(chosen.threshold),
        "recall": float(chosen.recall),
        "false_alarms": int(chosen.false_alarms),
        "expected_cost": int(chosen.expected_cost),
        "top_two_distinguishable": bool(demonstrable),
    }, indent=2) + "\n")

    print(f"baseline accuracy      : {baseline_acc:.1%}")
    print(f"selected model         : {best_name}")
    print(f"top two distinguishable: {demonstrable}")
    print(f"chosen threshold       : {chosen.threshold}  "
          f"(recall {chosen.recall:.1%}, {int(chosen.false_alarms)} false alarms)")
    print(f"expected cost          : £{int(chosen.expected_cost):,}")
    print(f"\nwrote report.md and artifacts/")


if __name__ == "__main__":
    main()
