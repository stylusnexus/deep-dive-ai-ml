TITLE = "Block 2 · Predictive Modelling"
TOPIC = "block2-classical-ml"
ICON = "📈"
DESCRIPTION = "Classical machine learning done properly — reading a confusion matrix, choosing a threshold, comparing models honestly, and knowing when a neural network is the wrong answer."
TAGS = ["ai", "ml", "evaluation"]
COLOR = "cyan"
CREATED = "2026-08-21"
ID_BASE = "1787500000"

LESSONS = [
{
  "slug": "confusion-matrix-and-metrics",
  "title": "The Confusion Matrix and What Comes Out of It",
  "subtitle": "Four numbers, and every classification metric you will ever meet is built from them.",
  "body": [
    ("p", "Almost every argument about model quality is really an argument about which of four numbers matters most. Get the four straight and the metrics stop being a vocabulary test."),

    ("h2", "The four cells"),

    ("figure", "Every classification metric in this lesson is a ratio of these four numbers. Learn the grid once and the formulas stop needing memorisation.", '''<svg viewBox="0 0 640 235" role="img" aria-label="The confusion matrix with its four cells">
<text x="250" y="20" class="d-label-sm">predicted</text>
<text x="196" y="42" class="d-label-sm">negative</text>
<text x="368" y="42" class="d-label-sm">positive</text>
<text x="16" y="100" class="d-label-sm">actual</text>
<text x="16" y="122" class="d-label-sm">negative</text>
<text x="16" y="182" class="d-label-sm">actual</text>
<text x="16" y="204" class="d-label-sm">positive</text>
<rect x="150" y="54" width="160" height="72" rx="6" class="d-box-good"/>
<text x="166" y="80" class="d-label-b">True negative</text>
<text x="166" y="100" class="d-label-sm">healthy, called healthy</text>
<text x="166" y="118" class="d-fill-green" font-size="11" font-weight="600">correct</text>
<rect x="322" y="54" width="160" height="72" rx="6" class="d-box-warn"/>
<text x="338" y="80" class="d-label-b">False positive</text>
<text x="338" y="100" class="d-label-sm">healthy, called failing</text>
<text x="338" y="118" class="d-fill-red" font-size="11" font-weight="600">false alarm · wasted call-out</text>
<rect x="150" y="136" width="160" height="72" rx="6" class="d-box-warn"/>
<text x="166" y="162" class="d-label-b">False negative</text>
<text x="166" y="182" class="d-label-sm">failing, called healthy</text>
<text x="166" y="200" class="d-fill-red" font-size="11" font-weight="600">missed case</text>
<rect x="322" y="136" width="160" height="72" rx="6" class="d-box-good"/>
<text x="338" y="162" class="d-label-b">True positive</text>
<text x="338" y="182" class="d-label-sm">failing, called failing</text>
<text x="338" y="200" class="d-fill-green" font-size="11" font-weight="600">caught it</text>
<text x="500" y="86" class="d-label-sm">precision reads</text>
<text x="500" y="102" class="d-label-sm">this column</text>
<text x="500" y="170" class="d-label-sm">recall reads</text>
<text x="500" y="186" class="d-label-sm">this row</text>
</svg>'''),

    ("h2", "The metrics, and the question each answers"),
    ("terms", [
      ("Accuracy", "All correct, over everything", "Meaningless when one class dominates. Always compare it against the majority-class baseline before saying it aloud."),
      ("Precision", "Of what I flagged, how much was real", "Reads the predicted-positive column. Low precision means wasted effort chasing false alarms."),
      ("Recall (sensitivity)", "Of what was real, how much did I catch", "Reads the actual-positive row. Low recall means missed cases."),
      ("F1", "The harmonic mean of the two", "One number when you must have one. It hides the trade-off rather than resolving it, so report the pair alongside."),
      ("Specificity", "Of the genuinely negative, how many did I leave alone", "The mirror of recall. Matters when false alarms are the expensive error."),
    ]),
    ("callout", "matters", "Precision and recall are not properties of the model", "They are properties of the model <em>at a chosen threshold</em>. The same model can be tuned to catch 93% of failures with 770 false alarms, or 44% with 77. Quoting a precision figure without the threshold it was measured at is quoting half a result."),

    ("know",
     "Precision reads a column of the matrix; recall reads a row.",
     "Precision asks what fraction of your positive predictions were correct — it divides by everything you flagged. Recall asks what fraction of the real positives you found — it divides by everything that was actually positive. Different denominators, which is why they trade against each other.",
     "A turbine model flags 392 machines, of which 124 genuinely fail. Precision is 124/392 = 32% — most call-outs are wasted. There were 187 real failures, so recall is 124/187 = 66% — a third were missed. Same model, same run, two very different complaints from two different departments."),

    ("h2", "ROC and the area under it"),
    ("p", "A classifier outputs probabilities, so it is really a family of classifiers — one for every threshold. The <strong>ROC curve</strong> — receiver operating characteristic, a name inherited from radar operators in the 1940s — plots how the model behaves across all of them."),
    ("p", "The vertical axis is the true positive rate, which is recall. The horizontal axis is the false positive rate, the fraction of genuine negatives wrongly flagged. Sweeping the threshold from strict to permissive traces a curve from the bottom-left corner to the top-right."),

    ("figure", "Each point is one threshold. A model that separates the classes well bows toward the top-left, catching most real cases before it starts raising many false alarms. The diagonal is random guessing.", '''<svg viewBox="0 0 640 220" role="img" aria-label="ROC curves for a good model, a weak model and random guessing">
<line x1="70" y1="180" x2="70" y2="24" class="d-arrow"/>
<line x1="70" y1="180" x2="330" y2="180" class="d-arrow"/>
<text x="8" y="80" class="d-label-sm">true positive</text>
<text x="8" y="96" class="d-label-sm">rate (recall)</text>
<text x="110" y="204" class="d-label-sm">false positive rate</text>
<line x1="70" y1="180" x2="330" y2="24" stroke="var(--muted)" stroke-width="1.6" stroke-dasharray="5 4"/>
<text x="248" y="120" class="d-label-sm">random</text>
<path d="M70 180 Q86 74 160 48 Q240 30 330 24" stroke="var(--green)" stroke-width="2.5" fill="none"/>
<text x="150" y="40" class="d-fill-green" font-size="11" font-weight="600">good · AUC 0.91</text>
<path d="M70 180 Q120 128 190 96 Q260 62 330 24" stroke="var(--yellow)" stroke-width="2.5" fill="none"/>
<text x="196" y="120" class="d-fill-yellow" font-size="11" font-weight="600">weak · 0.68</text>
<circle cx="132" cy="66" r="5" class="d-fill-accent"/>
<text x="142" y="70" class="d-label-sm">one threshold</text>
<rect x="368" y="30" width="260" height="150" rx="7" class="d-box"/>
<text x="384" y="52" class="d-label-b">Reading the number</text>
<text x="384" y="74" class="d-label-sm">1.00 — perfect separation</text>
<text x="384" y="94" class="d-label-sm">0.90 — strong</text>
<text x="384" y="114" class="d-label-sm">0.70 — modest</text>
<text x="384" y="134" class="d-label-sm">0.50 — no better than guessing</text>
<text x="384" y="162" class="d-label-sm">below 0.50 — check for a flipped label</text>
</svg>'''),

    ("p", "<strong>AUC</strong> — area under the curve — collapses that whole curve into one number between 0 and 1. It has an interpretation worth remembering: it is the probability that the model scores a randomly chosen positive case higher than a randomly chosen negative one. An AUC of 0.91 means it gets that ordering right 91 times in 100."),
    ("callout", "insight", "Why AUC is useful and why it is not enough", "It is threshold-free, so it measures ranking ability rather than any particular operating point — which makes it good for comparing models before you have chosen a threshold. That same property is its weakness: it says nothing about whether the threshold you will actually deploy is any good, and it is optimistic on heavily imbalanced data because the false positive rate has an enormous denominator."),

    ("know",
     "AUC is the probability that the model ranks a random positive above a random negative.",
     "It measures ordering, not decisions. That makes it the right tool for comparing two models before a threshold exists, and the wrong tool for judging whether a deployed system is behaving acceptably.",
     "Two fraud models both score 0.87 AUC. One is usable and one is not — at the threshold that catches 80% of fraud, the first raises 200 false alarms a day and the second raises 4,000. The AUC could not have told you that, because it averaged over thresholds you would never choose."),

    ("h2", "When to use the precision-recall curve instead"),
    ("p", "On heavily imbalanced data, prefer a precision-recall curve. The reason is the denominator: the false positive rate divides by the number of genuine negatives, and when negatives outnumber positives a hundred to one, even a large absolute number of false alarms produces a small false positive rate. The ROC curve looks reassuring while your team drowns in call-outs."),
    ("p", "The precision-recall curve has no such comfort. Precision divides by what you flagged, so false alarms hurt it directly and visibly."),

    ("h2", "Regression metrics, briefly"),
    ("terms", [
      ("MAE", "Mean absolute error", "Average distance from the truth, in the original units. Robust to outliers and easy to explain to anyone."),
      ("RMSE", "Root mean squared error", "Penalises large errors disproportionately. Use it when one big miss is worse than several small ones."),
      ("R-squared", "Proportion of variance explained", "Comparable across problems, and easy to over-read — a high value on a trivially predictable target means nothing."),
      ("MAPE", "Mean absolute percentage error", "Percentage terms, so it travels well between stakeholders. Breaks badly when true values approach zero."),
    ]),
    ("callout", "pitfall", "Report the error in units someone can act on", "\"RMSE 0.34\" means nothing to an operations manager. \"On average we are out by about four days, and occasionally by three weeks\" is the same information in a form that supports a decision. Translate before presenting, every time."),

    ("links", [
      ("Model evaluation — scikit-learn", "https://scikit-learn.org/stable/modules/model_evaluation.html",
       "Every metric above with its formula and API, plus the ones this lesson leaves out."),
      ("Precision-recall — scikit-learn", "https://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html",
       "Worked curves, and the argument for preferring them to ROC on imbalanced data."),
    ]),

    ("books", [
      ("Hands-On Machine Learning with Scikit-Learn and PyTorch", "Aurelien Geron",
       "Chapter 3 builds the confusion matrix, the precision-recall trade-off and ROC from scratch on a real dataset."),
    ]),

    ("quiz", [
      ("Precision and recall differ in what, fundamentally?",
       ["Precision is for balanced data and recall for imbalanced",
        "Their denominators — precision divides by what you flagged, recall by what was actually positive",
        "Precision is computed on training data and recall on test data"], 1),
      ("What does an AUC of 0.91 actually mean?",
       ["The model is correct 91% of the time",
        "It ranks a randomly chosen positive above a randomly chosen negative 91 times in 100",
        "91% of positives are caught at the default threshold"], 1),
      ("Why prefer a precision-recall curve on heavily imbalanced data?",
       ["It is faster to compute",
        "The ROC false positive rate divides by a huge number of negatives, so it looks reassuring while false alarms pile up",
        "ROC curves cannot be computed when classes are imbalanced"], 1),
      ("Someone quotes a model's precision as 82%. What is missing?",
       ["The recall figure",
        "The threshold it was measured at — precision is a property of the model at an operating point, not of the model",
        "The size of the test set"], 1),
    ]),
  ],
},
]
