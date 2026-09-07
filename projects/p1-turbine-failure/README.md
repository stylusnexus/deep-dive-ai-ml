# Project 1 · Wind Turbine Failure Prediction

**Block 2 exit criterion.** The energy project.

> Analyse equipment data from a wind energy provider, build models to identify
> potential failures, and enable timely repairs before equipment breaks down.

## Before you write any code

Fill in [`intake.md`](intake.md). All ten questions, dated, before touching the
data. That is not ceremony — question 2 (the dumb baseline) and question 6 (the
cost of each error type) both determine how you will read every later result, and
neither is answerable once you have seen a score you like.

## What "done" looks like

Not a notebook with a good number in it. A deliverable someone can act on:

- [ ] Intake sheet completed **before** modelling, and reviewed after
- [ ] Baseline scored and written down
- [ ] A leakage audit: every feature interrogated against *would I have this at prediction time?*
- [ ] At least three models compared on identical folds with a threshold-free metric
- [ ] Spread reported, not just means — and a statement about whether the best model is *demonstrably* better
- [ ] A threshold chosen from costs, with the reasoning written out
- [ ] A decision table an operations manager could act on
- [ ] One paragraph naming what would make you distrust this model in six months

## Running it

```bash
python src/train.py                 # end to end: load, split, train, evaluate, report
python src/train.py --costs 1500 9000   # false alarm, missed failure
```

Writes `report.md` and `artifacts/` — the model, the metrics, the threshold table.

## The honest framing

The interesting output of this project is **not** the model. It is the sentence
"at a threshold of X we catch Y% of failures for Z wasted call-outs, which costs
about £N a year against £M for doing nothing." The model is how you get that
sentence; the sentence is what anyone will actually use.
