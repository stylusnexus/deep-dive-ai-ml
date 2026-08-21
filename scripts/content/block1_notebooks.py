OUTDIR = "notebooks/01-python-eda"

_SETUP = """import pandas as pd, numpy as np
import matplotlib.pyplot as plt, seaborn as sns
from pathlib import Path

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 30)
sns.set_theme(style="whitegrid")

DATA = Path.cwd()
while not (DATA / "data" / "turbine_readings.csv").exists() and DATA != DATA.parent:
    DATA = DATA.parent
CSV = DATA / "data" / "turbine_readings.csv"
print("reading", CSV)"""

NOTEBOOKS = [
("01-first-contact.ipynb", [
("md", """# 01 · First Contact With a Dataset

The first fifteen minutes with unfamiliar data decide how much time you waste later.

This notebook is deliberately not a cleaning tutorial. It is the **survey** you do
before deciding anything — what's here, what shape it's in, what's obviously wrong.
Resist the urge to fix anything yet.

**Before you start:** open `artifacts/project-intake.md` and answer question 3
(*what data exists?*) from memory. Then check yourself against what you find below."""),
("code", _SETUP),
("code", """df = pd.read_csv(CSV)
df.shape"""),
("md", """## The four commands you always run

`shape`, `head`, `dtypes`, `describe`. Nothing clever — but read the output properly
rather than glancing at it."""),
("code", "df.head()"),
("code", """df.dtypes"""),
("md", """### Read those dtypes again

`operating_hours` came back as `object`, not a number. That means pandas found
something non-numeric in the column and gave up on parsing it. **A numeric column
that loads as `object` is always worth investigating** — it usually means the data
has text in it somewhere.

Let's see what."""),
("code", """print(df["operating_hours"].dropna().head(8).tolist())
print()
# rows that won't convert to a number
bad = pd.to_numeric(df["operating_hours"].str.replace(",", ""), errors="coerce").isna() \\
      & df["operating_hours"].notna()
print(f"{bad.sum()} values contain something non-numeric:")
print(df.loc[bad, "operating_hours"].head(5).tolist())"""),
("md", """Thousands separators, and some values carry a `hrs` suffix. Two different
formatting problems in one column — completely normal for data assembled by hand
or exported from more than one system.

## Missingness

How much is missing, and *where*."""),
("code", """miss = pd.DataFrame({
    "missing": df.isna().sum(),
    "pct": (df.isna().mean() * 100).round(1),
}).query("missing > 0").sort_values("pct", ascending=False)
miss"""),
("md", """## Duplicates

Two kinds, and they need different treatment: identical rows, and the same real-world
thing recorded twice under different identifiers."""),
("code", """print(f"exact duplicate rows : {df.duplicated().sum()}")
print(f"duplicate turbine_id  : {df['turbine_id'].duplicated().sum()}")
print(f"unique turbines       : {df['turbine_id'].nunique()} of {len(df)} rows")"""),
("md", """The exact duplicates are easy. But are there turbines logged twice under
*different* ids? Check for rows identical in everything except the identifier."""),
("code", """cols = [c for c in df.columns if c != "turbine_id"]
relogged = df.duplicated(subset=cols, keep=False) & ~df.duplicated(keep=False)
print(f"{relogged.sum()} rows look like the same turbine under a different id")
df.loc[relogged].sort_values("install_date").head(4)"""),
("md", """## The target

Always look at the target's balance before anything else. It determines which
metrics mean anything at all."""),
("code", """rate = df["failed_within_90d"].mean()
print(f"failure rate: {rate:.2%}")
print(f"always-predict-'no-failure' accuracy: {1 - rate:.2%}   <- the number to beat")"""),
("md", """Write that baseline down. Any accuracy figure you produce later is meaningless
without it — this is the intake sheet's question 2, and on imbalanced data it is the
whole interpretation.

## Categorical columns"""),
("code", """for c in ["site", "last_inspector", "maintenance_ticket_raised"]:
    print(f"--- {c}  ({df[c].nunique()} distinct)")
    print(df[c].value_counts(dropna=False).head(8))
    print()"""),
("md", """### Two things just surfaced

1. **`last_inspector` has the same people entered several ways** — `j.okafor` and
   `J. Okafor` are one person. Distinct counts are inflated and any grouping is wrong.

2. **`maintenance_ticket_raised` deserves suspicion.** Ask the intake sheet's
   question: *would I have this value, with this content, at the moment I need the
   prediction?* A maintenance ticket is raised **because** something failed. Check it."""),
("code", """pd.crosstab(df["maintenance_ticket_raised"].fillna("(none)"),
            df["failed_within_90d"], normalize="index").round(3)"""),
("md", """Every `URGENT` row is a failure. That column is a **leaking feature** — it
encodes the answer and would not exist at prediction time. Train on it and you'll see
a superb score and a worthless model.

Found in the first fifteen minutes, because we asked. That is the entire point of
this pass.

---

## Your turn

1. `gearbox_temp` has a range from about 30 to 234. Plot it grouped by `site`.
   What do you notice, and what would it do to a model trained on this column?
2. `rotor_speed_rpm` has a few values of exactly 9999.0. What are they, and why
   is that specific number a giveaway?
3. Fill in question 3 of the intake sheet properly now.

Notebook 02 takes these findings and does something about them."""),
]),

("02-cleaning-decisions.ipynb", [
("md", """# 02 · Cleaning Is a Sequence of Decisions

Every cleaning step throws information away or invents it. Neither is free, so
each one is a decision you should be able to defend.

This notebook works through the problems found in notebook 01. For each, the
question is not "what's the pandas command" but **"what am I claiming about the
world by doing this?"**"""),
("code", _SETUP),
("code", """df = pd.read_csv(CSV, parse_dates=["install_date"])
print(df.shape)"""),
("md", """## Decision 1 · Duplicates

Exact duplicates are almost always a logging artefact. Dropping them is safe.

Rows identical apart from the id are a judgement call: either the same turbine was
logged twice, or two turbines genuinely share every reading. Given continuous sensor
values, coincidence is implausible."""),
("code", """before = len(df)
df = df.drop_duplicates()
print(f"exact duplicates removed : {before - len(df)}")

cols = [c for c in df.columns if c != "turbine_id"]
before = len(df)
df = df.drop_duplicates(subset=cols)
print(f"re-logged rows removed   : {before - len(df)}")
print(f"remaining                : {len(df)}")"""),
("md", """## Decision 2 · The units problem

`gearbox_temp` runs from ~30 to ~234 in a column labelled as one unit. Two sites
are reporting Fahrenheit."""),
("code", """df.groupby("site")["gearbox_temp"].agg(["min", "median", "max", "count"]).round(1)"""),
("md", """Clyde and Beinn an Tuirc sit in a completely different range. Nothing in the
column name says so — the only way to catch this is to look at the distribution
per group.

Convert those two sites to Celsius. Note what we're assuming: that the *site* is what
determines the unit, and that no site switched partway through. Both are worth
confirming with whoever owns the data — and in a real project, that conversation
happens before this cell is written."""),
("code", """F_SITES = ["Clyde", "Beinn an Tuirc"]
mask = df["site"].isin(F_SITES)
df.loc[mask, "gearbox_temp"] = ((df.loc[mask, "gearbox_temp"] - 32) * 5 / 9).round(1)
df.rename(columns={"gearbox_temp": "gearbox_temp_c"}, inplace=True)

df.groupby("site")["gearbox_temp_c"].agg(["min", "median", "max"]).round(1)"""),
("md", """The ranges now agree. Renaming the column to carry its unit is cheap insurance
against exactly this bug recurring.

## Decision 3 · Parsing the string column"""),
("code", """df["operating_hours"] = (
    df["operating_hours"].astype(str)
      .str.replace(",", "", regex=False)
      .str.replace(r"\\s*hrs?\\s*$", "", regex=True)
      .replace({"nan": np.nan, "None": np.nan})
      .astype(float)
)
df["operating_hours"].describe().round(0)"""),
("md", """## Decision 4 · The sensor glitches

`rotor_speed_rpm` contains values of exactly 9999.0. A repeated, round, physically
impossible number is a **sentinel** — a placeholder some system writes when a reading
fails. It is missing data wearing a costume.

Treating it as a real value would badly distort every statistic. Treating it as
missing is the honest move."""),
("code", """glitch = df["rotor_speed_rpm"] == 9999.0
print(f"sentinel values: {glitch.sum()}")
print(f"mean rotor speed WITH them   : {df['rotor_speed_rpm'].mean():.1f}")
df.loc[glitch, "rotor_speed_rpm"] = np.nan
print(f"mean rotor speed WITHOUT them: {df['rotor_speed_rpm'].mean():.1f}")"""),
("md", """## Decision 5 · Standardising the inspector names"""),
("code", """def norm_name(v):
    if pd.isna(v):
        return v
    v = v.lower().replace(".", " ").replace("_", " ")
    parts = [p for p in v.split() if p]
    return f"{parts[0][0]}.{parts[-1]}" if len(parts) > 1 else parts[0]

print(f"before: {df['last_inspector'].nunique()} distinct")
df["last_inspector"] = df["last_inspector"].map(norm_name)
print(f"after : {df['last_inspector'].nunique()} distinct")
df["last_inspector"].value_counts(dropna=False)"""),
("md", """## Decision 6 · Missing values, and why the mechanism matters

The most common mistake here is filling gaps with the column mean without asking
**why** the values are missing. Three mechanisms, three consequences:

| Mechanism | Meaning | Consequence |
|---|---|---|
| MCAR | Missing completely at random | Filling is relatively safe |
| MAR | Missingness explained by *other* columns | Fill using those columns |
| MNAR | Missingness relates to the missing value itself | Filling introduces real bias |

Test whether vibration is missing at random by comparing rows where it's absent
against rows where it's present."""),
("code", """flag = df["vibration_mm_s"].isna()
comp = df.groupby(flag)[["age_years", "gearbox_temp_c", "failed_within_90d"]].mean().round(3)
comp.index = ["vibration present", "vibration MISSING"]
comp"""),
("md", """Rows with missing vibration have a **substantially higher failure rate**. The
values are not missing at random — the sensor tends to drop out on the turbines that
are shaking hardest.

That has two implications:

1. Filling with the median would pull the worst turbines toward normal and destroy
   the signal you care about most.
2. **The missingness is itself predictive.** Record it as a feature before filling."""),
("code", """df["vibration_missing"] = df["vibration_mm_s"].isna().astype(int)

print("failure rate by missingness flag:")
print(df.groupby("vibration_missing")["failed_within_90d"].mean().round(3))"""),
("md", """> **Do not impute here.** Any filling of `vibration_mm_s` must be fitted on the
> training split only, inside a pipeline — otherwise the test set's statistics leak
> into training. That's notebook 04's job, and doing it now would be the classic
> preprocessing leak.

## Decision 7 · Drop the leaking column"""),
("code", """df = df.drop(columns=["maintenance_ticket_raised"])
print("dropped maintenance_ticket_raised — it encodes the outcome")"""),
("md", """## Save the cleaned data"""),
("code", """out = CSV.parent / "turbine_clean.csv"
df.to_csv(out, index=False)
print(f"wrote {out.name}  {df.shape[0]} rows x {df.shape[1]} cols")
df.dtypes"""),
("md", """---

## What you decided

Every one of these is defensible and none is automatic:

- dropped duplicates, including re-logged rows
- converted two sites from Fahrenheit, **assuming site determines unit**
- treated 9999.0 as missing rather than real
- collapsed inspector name variants
- kept missingness as a feature instead of filling it
- dropped a leaking column

Write the assumptions down. When the model behaves oddly in three weeks, this list
is where you look first.

## Your turn

1. `install_date` and `age_years` should agree. Do they? What would you do if not?
2. Is `operating_hours` consistent with `age_years`? Any turbine running more hours
   than it has existed?
3. What would change if a site had switched from Fahrenheit to Celsius mid-year?
   How would you detect that?"""),
]),
("03-exploring-distributions.ipynb", [
("md", """# 03 · Exploring: What a Plot Is Actually For

A plot is not decoration and it is not a deliverable. It is a **question you're
asking the data**, and the only ones worth making are the ones where you'd act
differently depending on the answer.

This notebook asks five questions. Each has a decision attached."""),
("code", _SETUP),
("code", """df = pd.read_csv(CSV.parent / "turbine_clean.csv", parse_dates=["install_date"])
print(df.shape)
df.head(3)"""),
("md", """## Question 1 · What shape is each variable?

Before any modelling: is it symmetric, skewed, bimodal, or bounded? The answer
decides whether the mean means anything and whether a transform would help."""),
("code", """num = ["age_years", "rotor_speed_rpm", "vibration_mm_s", "gearbox_temp_c", "operating_hours"]

fig, axes = plt.subplots(2, 3, figsize=(14, 7))
for ax, c in zip(axes.flat, num):
    sns.histplot(df[c].dropna(), bins=40, ax=ax, color="#6c8fff")
    ax.set_title(c)
    ax.axvline(df[c].mean(), color="#f87171", ls="--", lw=1.4, label="mean")
    ax.axvline(df[c].median(), color="#34d399", ls="-", lw=1.4, label="median")
    ax.legend(fontsize=8)
axes.flat[-1].axis("off")
plt.tight_layout()"""),
("md", """### Read the gap between the two lines

Where the red mean sits noticeably right of the green median, the variable is
**right-skewed** — a long tail of high values pulling the average up. `age_years`
and `vibration_mm_s` both show this.

The decision it drives: for a skewed variable, "the average turbine" is a misleading
summary, and linear models may benefit from a log transform.

## Question 2 · Does the target relate to any of these?

This is the one that decides which features are worth having."""),
("code", """fig, axes = plt.subplots(1, 4, figsize=(16, 4))
for ax, c in zip(axes, ["vibration_mm_s", "gearbox_temp_c", "age_years", "operating_hours"]):
    sns.boxplot(data=df, x="failed_within_90d", y=c, ax=ax,
                palette=["#34d399", "#f87171"], hue="failed_within_90d", legend=False)
    ax.set_title(f"{c} by outcome")
    ax.set_xlabel("failed within 90d")
plt.tight_layout()"""),
("code", """df.groupby("failed_within_90d")[num].mean().round(3).T"""),
("md", """Vibration and gearbox temperature separate the two groups clearly. Age separates
them mildly. Rotor speed barely at all.

That is a **feature-selection finding**, arrived at before fitting anything.

## Question 3 · Are the features telling us the same thing twice?"""),
("code", """corr = df[num + ["failed_within_90d"]].corr()

plt.figure(figsize=(7, 5.5))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0,
            vmin=-1, vmax=1, square=True, cbar_kws={"shrink": .8})
plt.title("Pearson correlation")
plt.tight_layout()"""),
("md", """`age_years` and `operating_hours` are almost perfectly correlated — unsurprising,
since hours accumulate with age. Two near-identical inputs make linear-model
coefficients unstable and uninterpretable, even while predictions stay fine.

Decision: keep one, or combine them into something new (hours per year of age
captures *intensity of use*, which the raw pair does not).

> **Correlation only detects straight-line relationships.** A strong curved
> relationship can show a correlation near zero. Never conclude "no relationship"
> from a low correlation without looking at the scatter."""),
("code", """df["hours_per_year"] = df["operating_hours"] / df["age_years"].clip(lower=0.1)
print(df.groupby("failed_within_90d")["hours_per_year"].mean().round(0))"""),
("md", """## Question 4 · Do the sites behave differently?

If they do, site is a real feature. If they don't, it's noise you're inviting the
model to overfit."""),
("code", """site = df.groupby("site").agg(
    turbines=("turbine_id", "count"),
    failure_rate=("failed_within_90d", "mean"),
    mean_vibration=("vibration_mm_s", "mean"),
    mean_age=("age_years", "mean"),
).round(3).sort_values("failure_rate", ascending=False)
site"""),
("md", """### Careful here

If one site has a higher failure rate *and* older turbines, site may be standing in
for age rather than carrying information of its own. Check before believing it."""),
("code", """fig, ax = plt.subplots(figsize=(9, 4.5))
sns.barplot(data=df, x="site", y="failed_within_90d", ax=ax,
            hue="site", palette="Blues_d", legend=False, errorbar=("ci", 95))
ax.set_ylabel("failure rate (95% CI)")
ax.set_title("Failure rate by site — do the intervals overlap?")
plt.tight_layout()"""),
("md", """**Read the error bars.** Where confidence intervals overlap heavily, the apparent
difference between sites may be noise. This is the sample-size point from your
statistics course, applied to a bar chart — and the reason a bar chart without error
bars is frequently misleading.

## Question 5 · Does the missingness flag carry signal?

Notebook 02 kept `vibration_missing` as a feature on the grounds that the missingness
was informative. Confirm that."""),
("code", """print(df.groupby("vibration_missing")["failed_within_90d"].agg(["mean", "count"]).round(3))

overall = df["failed_within_90d"].mean()
lift = df.groupby("vibration_missing")["failed_within_90d"].mean() / overall
print(f"\\nlift vs overall rate: {lift.round(2).to_dict()}")"""),
("md", """A turbine with a missing vibration reading is substantially more likely to fail.
The *absence* of data is data. Keeping that flag was the right call.

---

## What this pass produced

- vibration and gearbox temperature are the strongest signals
- rotor speed looks close to useless
- age and operating hours are redundant — combine or drop one
- site differences may be confounded by age; needs care
- the missingness flag is genuinely predictive

None of that required fitting a model, and all of it shapes what you do next.

## Your turn

1. Plot `vibration_mm_s` against `gearbox_temp_c`, coloured by outcome. Is the
   boundary between classes roughly a straight line?
2. Compute the correlation between age and operating hours. Would you keep both?
3. Does `last_inspector` relate to failure? If it appears to, what would you check
   before believing it?"""),
]),

("04-split-and-pipeline.ipynb", [
("md", """# 04 · Splitting and the Pipeline

This is the shortest notebook in Block 1 and the one that prevents the most damage.

Everything so far was inspection. The moment you start *fitting* anything — a scaler,
an imputer, an encoder — you can leak information from your test set into training
without noticing. The defence is structural, not vigilance."""),
("code", _SETUP),
("code", """from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

df = pd.read_csv(CSV.parent / "turbine_clean.csv", parse_dates=["install_date"])
df["hours_per_year"] = df["operating_hours"] / df["age_years"].clip(lower=0.1)
print(df.shape)"""),
("md", """## The mistake, demonstrated

Here is the wrong order, which looks completely reasonable:

```python
df[num] = StandardScaler().fit_transform(df[num])   # fit on EVERYTHING
X_tr, X_te = train_test_split(df)                   # then split
```

The scaler computed its mean and standard deviation using every row, including the
test rows. Your training data has now seen the test set's statistics. The score comes
out slightly too good and nothing looks wrong — the train/validation gap you'd use to
spot overfitting shows nothing, because both sides were inflated together.

**Split first. Always.**"""),
("code", """FEATURES_NUM = ["age_years", "rotor_speed_rpm", "vibration_mm_s",
                "gearbox_temp_c", "hours_per_year", "vibration_missing"]
FEATURES_CAT = ["site"]
TARGET = "failed_within_90d"

X = df[FEATURES_NUM + FEATURES_CAT]
y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"train {X_train.shape}   test {X_test.shape}")
print(f"failure rate — train {y_train.mean():.3f}, test {y_test.mean():.3f}")"""),
("md", """### Why `stratify=y`

With a 15% failure rate, a random split can easily hand you a test set with a
noticeably different rate purely by chance. Stratifying preserves the class balance
in both halves so your scores are comparable.

## The pipeline

A `Pipeline` isn't tidiness. It makes leakage **structurally difficult**: every step
is fitted on training data only and merely applied elsewhere, including inside
cross-validation, where getting this right by hand is genuinely hard."""),
("code", """numeric = Pipeline([
    ("impute", SimpleImputer(strategy="median")),
    ("scale", StandardScaler()),
])
categorical = Pipeline([
    ("impute", SimpleImputer(strategy="most_frequent")),
    ("encode", OneHotEncoder(handle_unknown="ignore")),
])

prep = ColumnTransformer([
    ("num", numeric, FEATURES_NUM),
    ("cat", categorical, FEATURES_CAT),
])

model = Pipeline([
    ("prep", prep),
    ("clf", LogisticRegression(max_iter=1000, class_weight="balanced")),
])
model"""),
("md", """`handle_unknown="ignore"` matters: if a site appears in test data that wasn't in
training, the encoder must not crash. In production that situation is normal.

`class_weight="balanced"` tells logistic regression to penalise errors on the rare
class more heavily — the cheapest of the imbalance remedies, and the one to try first."""),
("code", """model.fit(X_train, y_train)
pred = model.predict(X_test)

baseline = 1 - y_test.mean()
print(f"always-predict-'no-failure' accuracy : {baseline:.3f}   <- the number to beat")
print(f"model accuracy                       : (y_test == pred).mean() below\\n")
print(classification_report(y_test, pred, target_names=["no failure", "failure"], digits=3))"""),
("md", """### Read this properly

Compare accuracy against the baseline first. If the model's accuracy is *below* the
always-predict-no-failure baseline, that is not necessarily failure — `class_weight`
deliberately trades accuracy for recall on the rare class, which is usually what you
want when a missed failure is expensive.

**Recall on the failure class** is the number that matters here. Precision tells you
how many maintenance call-outs would be wasted."""),
("code", """cm = confusion_matrix(y_test, pred)
fig, ax = plt.subplots(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False,
            xticklabels=["pred: no", "pred: fail"],
            yticklabels=["actual: no", "actual: fail"], ax=ax)
ax.set_title("Confusion matrix")
plt.tight_layout()

tn, fp, fn, tp = cm.ravel()
print(f"caught {tp} of {tp+fn} real failures  (recall {tp/(tp+fn):.1%})")
print(f"{fp} false alarms out of {tn+fp} healthy turbines")"""),
("md", """## Moving the threshold

The model outputs probabilities. `predict()` applies a 0.5 cut-off, which is a
convention, not a decision. Here is what other cut-offs would cost and buy."""),
("code", """proba = model.predict_proba(X_test)[:, 1]

rows = []
for t in [0.2, 0.3, 0.4, 0.5, 0.6, 0.7]:
    p = (proba >= t).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_test, p).ravel()
    rows.append({
        "threshold": t,
        "recall": round(tp / (tp + fn), 3),
        "precision": round(tp / (tp + fp), 3) if (tp + fp) else 0.0,
        "missed_failures": fn,
        "false_alarms": fp,
    })
pd.DataFrame(rows)"""),
("md", """**This table is the actual deliverable of a modelling exercise**, more than any
single score. It converts a model into a business decision: for each threshold, how
many real failures you miss and how many crews you send out for nothing.

Choosing a row requires knowing what a missed failure costs versus an unnecessary
inspection — intake sheet question 6. The model cannot answer that, and neither can
the data scientist alone.

## Cross-validation, done safely"""),
("code", """from sklearn.model_selection import cross_val_score, StratifiedKFold

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X_train, y_train, cv=cv, scoring="recall")
print(f"recall across 5 folds: {scores.round(3)}")
print(f"mean {scores.mean():.3f}  sd {scores.std():.3f}")"""),
("md", """Because the whole pipeline is passed to `cross_val_score`, imputation and scaling
are refitted inside every fold. Had you scaled beforehand, every fold would have been
contaminated and this number would be quietly optimistic.

---

## Block 1 complete

You have taken raw, messy data and produced a defensible, leakage-free modelling
setup with a decision table at the end.

**The habits worth keeping:**

1. Survey before fixing
2. Compute the trivial baseline before reading any score
3. Ask of every feature: would I have this at prediction time?
4. Split before fitting anything at all
5. Put preprocessing in a pipeline so leakage is structurally hard
6. Report a threshold table, not a single number

Block 2 replaces logistic regression with trees, ensembles and neural networks — on
this same pipeline, so the comparison is honest.

## Your turn

1. Add `last_inspector` as a categorical feature. Does recall improve? Should you
   keep it? (Think about what it would mean if it helped.)
2. Set `class_weight=None` and compare. Which metric moves most?
3. Pick a threshold and write one sentence defending it to an operations manager."""),
]),
]
