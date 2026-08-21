# Block 2 · Predictive Modelling

Runs on `data/turbine_clean.csv`, produced by Block 1 notebook 02. Run that first.

| Notebook | What it does |
|---|---|
| `01-metrics-and-thresholds.ipynb` | Confusion matrix by hand, ROC and precision-recall side by side, AUC verified empirically, and a threshold chosen from costs |
| `02-model-ladder.ipynb` | Five models on identical folds, compared threshold-free, with permutation importance |

## What the outputs actually show

**The two curves disagree, and the disagreement is the point.** AUC 0.770 looks
respectable; average precision 0.465 against a 0.155 random baseline is far less
flattering. The false-positive *rate* stays small because there are many
negatives, while the false alarms pile up in absolute terms.

**The AUC interpretation is verified, not asserted.** The notebook draws 200,000
random positive/negative pairs and counts how often the positive scores higher:
0.7698 against sklearn's 0.7705.

**The cost curve has an interior minimum at 0.55**, not at the default 0.5 — and
an exercise shows that at a higher cost ratio the optimum moves to "inspect
everything", which is a correct answer rather than a bug.

**The model ladder is compared threshold-free.** Random forest looks poor on
recall at 0.5 (0.448) and is competitive on average precision (0.475). That gap is
a fact about the threshold, not the model — which is why the fair comparison uses
a threshold-free metric.

**The top three are indistinguishable.** Gap between the best two: 0.023.
Typical fold variation: 0.036. Not a demonstrated difference, so choose on
interpretability and operational cost instead.
