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

## After
- [ ] ☠ Compared against the baseline, not just reported alone
- [ ] Gap between train and validation read — small gap + poor scores = underfit; large gap = overfit
- [ ] Cross-validated with the whole pipeline inside the folds
- [ ] Test set touched **once**, at the end, and never again
- [ ] Result recorded with config, data version, date, per-item outcomes

## Smells
- Score suspiciously high on a hard problem → suspect leakage before celebrating
- Validation better than training → check for a split bug or a leak
- Wild variance across folds → too little data, or grouped data split wrongly
