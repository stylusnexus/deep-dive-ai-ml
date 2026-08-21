# Training — any model, classical or deep

Run after the data checklist. ☠ = miss it and the result is wrong, not just worse.

## Before the run
- [ ] ☠ Train / validation / test split done, and test is untouched
- [ ] ☠ All preprocessing inside a pipeline, fitted on train only
- [ ] Group and time structure respected (`GroupKFold`, time-ordered split)
- [ ] Class imbalance handled — weights first, resampling only inside the pipeline
- [ ] Metric chosen for the problem, not by habit; accuracy rejected if classes are imbalanced
- [ ] Baseline scored: majority class, or predict-the-mean
- [ ] Seeds pinned; library versions recorded

## During
- [ ] Training and validation loss both tracked, on one chart
- [ ] Early stopping on validation, not on training loss
- [ ] Learning rate sane — loss falling, not NaN, not flat
- [ ] Run logged to something (MLflow) rather than scrollback

## Comparing models fairly
- [ ] ☠ Compared **threshold-free** (average precision or AUC) — recall or F1 at a fixed 0.5 is unfair across model families that shape probabilities differently
- [ ] Identical folds, identical seed, identical preprocessing pipeline for every candidate
- [ ] Metric chosen **before** looking at any result
- [ ] ☠ Spread reported alongside the mean — overlapping intervals are not a demonstrated difference
- [ ] If the top two are indistinguishable, said so plainly and chosen on interpretability and operating cost instead

## If the data is ordered in time
- [ ] ☠ Split by time, never randomly — a random split trains on the future
- [ ] ☠ Gap between train and test matching the prediction horizon
- [ ] Rolling and lag features shifted, computed within each entity, and inside the fold
- [ ] Walk-forward validation rather than one split, so you get a spread
- [ ] Naive baseline computed ("tomorrow equals today", or same period last season)
- [ ] Regime changes identified — a sliding window may beat an expanding one

## After
- [ ] ☠ Compared against the baseline, not just reported alone
- [ ] Gap between train and validation read — small gap + poor scores = underfit; large gap = overfit
- [ ] Cross-validated with the whole pipeline inside the folds
- [ ] Test set touched **once**, at the end, and never again
- [ ] Result recorded with config, data version, date, per-item outcomes

## Smells
- Score suspiciously high on a hard problem → suspect leakage before celebrating
- One model far worse than the rest at a fixed threshold → probably a threshold artefact, not a model problem; re-check threshold-free
- Time-ordered data scoring far better on a random split than a time split → the random split was leaking the future
- Validation better than training → check for a split bug or a leak
- Wild variance across folds → too little data, or grouped data split wrongly
