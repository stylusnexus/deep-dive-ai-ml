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
{
  "slug": "baseline-to-model",
  "title": "From Baseline to Model",
  "subtitle": "A ladder of increasing complexity, climbed only as far as the evidence justifies.",
  "body": [
    ("p", "The temptation on a new problem is to reach for the strongest thing you know. The disciplined approach is a ladder, and it is faster in practice because most rungs take minutes and each one tells you something the next cannot."),

    ("h2", "The ladder"),
    ("terms", [
      ("0 · Majority class", "Seconds", "Predict the most common answer for everything. This is the number every later result is judged against."),
      ("1 · One rule", "Minutes", "Threshold the single most predictive feature. Surprisingly often within a point or two of everything above it."),
      ("2 · Logistic regression", "Minutes", "Interpretable coefficients, fast, deployable anywhere. The real baseline for tabular problems."),
      ("3 · Random forest", "Minutes", "Strong, needs almost no tuning, resistant to overfitting. Usually your first genuinely competitive score."),
      ("4 · Gradient boosting", "Hours, with care", "Higher ceiling, requires early stopping and a learning rate you chose deliberately."),
      ("5 · Neural network", "Days", "For tabular data this is rarely the answer, and the next lesson explains why."),
    ]),

    ("know",
     "Climb the ladder until the gain stops justifying the cost, then stop.",
     "Each rung costs more to build, tune, explain and operate than the one below it. A two-point gain that turns an interpretable model into an opaque one is frequently a bad trade, and it is a trade nobody makes explicitly if the ladder is skipped.",
     "On the turbine data, logistic regression reaches 71% recall cross-validated. A tuned boosted model reaches 74%. Three points, in exchange for a model you cannot explain to a maintenance manager, that needs a serving runtime, and that will need retuning when the data drifts. Sometimes worth it. Not automatically."),

    ("h2", "Comparing honestly"),
    ("p", "Most model comparisons are quietly unfair, in ways that all favour the newer model. Four rules make them fair:"),
    ("ul", [
      "<strong>Same split, same folds, same seed.</strong> A different random split can move a score by more than a real modelling improvement.",
      "<strong>Same preprocessing pipeline.</strong> If one model gets scaled and imputed features and another gets raw ones, you are comparing pipelines, not models.",
      "<strong>Same metric, chosen before you looked.</strong> Picking the metric that flatters your preferred model afterwards is the most common form of self-deception in this work.",
      "<strong>Report the spread, not just the mean.</strong> A model at 74% ± 4 and one at 71% ± 3 are not clearly different, and presenting them as though they were is a claim the data does not support.",
    ]),

    ("figure", "Five models, cross-validated, with their variation shown. The apparent ranking is real only where the intervals separate — and here the top three do not.", '''<svg viewBox="0 0 640 210" role="img" aria-label="Model comparison with error bars">
<line x1="180" y1="182" x2="600" y2="182" class="d-arrow"/>
<text x="330" y="202" class="d-label-sm">recall, cross-validated</text>
<text x="12" y="36" class="d-label-sm">majority class</text>
<line x1="196" y1="30" x2="196" y2="30" stroke="var(--muted)" stroke-width="3"/>
<circle cx="196" cy="30" r="5" class="d-fill-muted"/>
<text x="208" y="34" class="d-label-sm">0.00</text>
<text x="12" y="66" class="d-label-sm">one rule</text>
<line x1="300" y1="60" x2="360" y2="60" stroke="var(--muted)" stroke-width="2"/>
<circle cx="330" cy="60" r="5" class="d-fill-muted"/>
<text x="372" y="64" class="d-label-sm">0.52</text>
<text x="12" y="96" class="d-label-sm">logistic regression</text>
<line x1="392" y1="90" x2="452" y2="90" stroke="var(--accent)" stroke-width="2"/>
<circle cx="422" cy="90" r="5" class="d-fill-accent"/>
<text x="464" y="94" class="d-label-sm">0.71 ± 0.04</text>
<text x="12" y="126" class="d-label-sm">random forest</text>
<line x1="400" y1="120" x2="466" y2="120" stroke="var(--accent)" stroke-width="2"/>
<circle cx="433" cy="120" r="5" class="d-fill-accent"/>
<text x="478" y="124" class="d-label-sm">0.73 ± 0.05</text>
<text x="12" y="156" class="d-label-sm">gradient boosting</text>
<line x1="408" y1="150" x2="468" y2="150" stroke="var(--green)" stroke-width="2"/>
<circle cx="438" cy="150" r="5" class="d-fill-green"/>
<text x="480" y="154" class="d-label-sm">0.74 ± 0.04</text>
<rect x="386" y="76" width="90" height="88" rx="5" fill="none" stroke="var(--yellow)" stroke-dasharray="4 4"/>
<text x="500" y="176" class="d-fill-yellow" font-size="11" font-weight="600">these three overlap</text>
</svg>'''),

    ("know",
     "Two models whose confidence intervals overlap are not distinguishable, however different their means look.",
     "Cross-validation folds vary. A three-point difference with four points of spread on each side is consistent with the models being equally good, and reporting it as an improvement is a claim the evidence does not support.",
     "A team ships a boosted model over logistic regression on a 2.8-point gain, then spends a quarter maintaining a serving stack for it. Re-run with different fold seeds, the gap is 0.4 points. The original difference was fold assignment, not modelling."),

    ("h2", "What to do when nothing beats the baseline"),
    ("p", "This happens, and it is information rather than failure. Work through it in order:"),
    ("ul", [
      "<strong>Is the signal there at all?</strong> Plot the strongest feature against the target. If the classes overlap almost entirely, no algorithm will separate them.",
      "<strong>Is the target well defined?</strong> \"Failure within 90 days\" may be recorded inconsistently, which puts a ceiling on any model.",
      "<strong>Is there a feature you have not built?</strong> Ratios, differences and time-since events frequently carry signal that raw columns do not — hours per year of age beat both hours and age on the turbine data.",
      "<strong>Is the problem framed correctly?</strong> Predicting <em>which week</em> a failure falls in may be answerable when predicting <em>whether</em> it happens is not.",
      "<strong>Is it genuinely unpredictable?</strong> A defensible finding, and much cheaper to deliver in week two than in month six.",
    ]),
    ("callout", "matters", "A negative result delivered early is a real deliverable", "\"We cannot predict this from the data we have, and here is what we would need\" is a better outcome than six months of model-tuning that ends in the same place. The intake sheet asks for a kill condition precisely so this conversation is easy to have."),

    ("h2", "Feature engineering, which beats model selection"),
    ("p", "On tabular problems, a good feature usually moves the number more than a better algorithm does. The productive kinds:"),
    ("terms", [
      ("Ratios and rates", "Intensity, not totals", "Hours per year of age separates a hard-worked young turbine from a coasting old one. Neither raw column carries that."),
      ("Differences from a norm", "Deviation, not level", "Temperature relative to the site median matters more than temperature."),
      ("Time since an event", "Recency", "Days since last inspection, days since last fault."),
      ("Aggregates over a group", "Context", "This turbine's vibration against its site's average."),
      ("Missingness indicators", "Absence as signal", "Already covered in Block 1, and worth repeating because it is so often left out."),
    ]),

    ("links", [
      ("Model selection — scikit-learn", "https://scikit-learn.org/stable/model_selection.html",
       "Cross-validation, nested validation and the search utilities, with the leakage-safe patterns."),
      ("Rules of Machine Learning — Google", "https://developers.google.com/machine-learning/guides/rules-of-ml",
       "Rules 1 to 20 cover exactly this ladder, from a team that learned it expensively."),
    ]),

    ("quiz", [
      ("Model A scores 0.74 ± 0.04 and model B scores 0.71 ± 0.04, cross-validated. What can you conclude?",
       ["A is better and should be shipped",
        "Not much — the intervals overlap, so the difference may be fold assignment rather than modelling",
        "The experiment needs a larger test set before any comparison"], 1),
      ("Nothing beats your majority-class baseline. What is the first thing to check?",
       ["Whether a neural network would do better",
        "Whether the signal exists at all — plot the strongest feature against the target and look at the overlap",
        "Whether the cross-validation folds are large enough"], 1),
      ("On a tabular problem, what usually moves the score most?",
       ["Switching to a more powerful algorithm",
        "A well-constructed feature — a ratio, a deviation from a norm, a time-since",
        "Increasing the number of training epochs"], 1),
    ]),
  ],
},
{
  "slug": "neural-networks-both-ways",
  "title": "Neural Networks, in Keras and in PyTorch",
  "subtitle": "The same network written twice — and an honest account of when it is the wrong tool.",
  "body": [
    ("p", "The original syllabus specifies TensorFlow and Keras. Most current research and tooling is PyTorch. You do not have to choose, because Keras 3 runs on either — and seeing the same network expressed both ways is the fastest route to understanding what the framework is actually doing."),

    ("h2", "Keras 3 is multi-backend, and that is not marketing"),
    ("p", "One environment variable selects the engine underneath. The model code does not change:"),
    ("code", """import os
os.environ["KERAS_BACKEND"] = "tensorflow"    # or "torch", or "jax"
import keras

model = keras.Sequential([
    keras.layers.Input((6,)),
    keras.layers.Dense(16, activation="relu"),
    keras.layers.Dense(1, activation="sigmoid"),
])
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
model.fit(X, y, epochs=3)"""),
    ("p", "Run verbatim on this course's environment, that identical code trains under both backends. It is worth doing yourself once, because the result also demonstrates something the documentation glosses over."),

    ("callout", "insight", "The two runs are not bit-identical, and that is expected", "The same code, the same seed, the same data: final loss 0.6694 under TensorFlow and 0.6799 under PyTorch. Random number generation and floating-point operation ordering differ between backends. This is a useful thing to meet early — reproducibility in deep learning is approximate, and any evaluation you build must tolerate small differences rather than assert equality."),

    ("h2", "The same network in raw PyTorch"),
    ("p", "Worth writing once, because it makes visible what Keras is doing for you:"),
    ("code", """import torch, torch.nn as nn

model = nn.Sequential(nn.Linear(6, 16), nn.ReLU(), nn.Linear(16, 1))
loss_fn = nn.BCEWithLogitsLoss()
opt = torch.optim.Adam(model.parameters())

for epoch in range(3):
    for xb, yb in loader:            # you write the batching
        opt.zero_grad()              # you clear the gradients
        loss = loss_fn(model(xb), yb)
        loss.backward()              # you trigger backprop
        opt.step()                   # you apply the update"""),
    ("p", "Keras's <code>fit</code> is that loop, plus batching, metrics, callbacks, early stopping and progress reporting. Nothing more mysterious than that."),

    ("figure", "The same four operations either way. Keras writes the loop for you; PyTorch hands you the pieces. Neither is more powerful — one is more convenient and the other more visible.", '''<svg viewBox="0 0 640 200" role="img" aria-label="Keras fit compared with a manual PyTorch training loop">
<rect x="12" y="26" width="290" height="150" rx="7" class="d-box-accent"/>
<text x="28" y="50" class="d-label-b">Keras</text>
<rect x="28" y="62" width="258" height="30" rx="4" class="d-box"/>
<text x="42" y="82" class="d-label-sm">model.fit(X, y, epochs=3)</text>
<text x="28" y="116" class="d-label-sm">batching, gradient clearing, backprop,</text>
<text x="28" y="134" class="d-label-sm">optimiser step, metrics, callbacks —</text>
<text x="28" y="152" class="d-label-sm">all inside that one call</text>
<rect x="338" y="26" width="290" height="150" rx="7" class="d-box"/>
<text x="354" y="50" class="d-label-b">PyTorch</text>
<rect x="354" y="62" width="258" height="24" rx="4" class="d-box"/>
<text x="366" y="79" class="d-label-sm">opt.zero_grad()</text>
<rect x="354" y="90" width="258" height="24" rx="4" class="d-box"/>
<text x="366" y="107" class="d-label-sm">loss = loss_fn(model(xb), yb)</text>
<rect x="354" y="118" width="258" height="24" rx="4" class="d-box"/>
<text x="366" y="135" class="d-label-sm">loss.backward()</text>
<rect x="354" y="146" width="258" height="24" rx="4" class="d-box-good"/>
<text x="366" y="163" class="d-label-sm">opt.step()</text>
</svg>'''),

    ("h2", "Which to use"),
    ("terms", [
      ("Keras", "Standard architectures, fast", "Sequential models, transfer learning, anything where the training loop is conventional. Less code, fewer bugs."),
      ("PyTorch directly", "Research and custom loops", "Custom losses, unusual training schedules, multi-model setups, and nearly all published research code."),
      ("Keras on the torch backend", "Both", "Keras convenience with a PyTorch ecosystem underneath. A genuinely good default for this course."),
    ]),

    ("h2", "The honest part: neural networks and tabular data"),
    ("p", "The syllabus builds toward a neural network on the turbine data, so this needs saying plainly. <strong>On tabular problems, gradient-boosted trees usually win.</strong> Not occasionally — consistently, across published comparisons and in practice."),
    ("ul", [
      "<strong>Trees handle mixed types natively.</strong> Categorical and numeric together, no scaling, no encoding decisions.",
      "<strong>Trees are robust to irrelevant features.</strong> A network has to learn to ignore them, which costs data.",
      "<strong>Trees need far less data.</strong> Neural networks are data-hungry, and most business tables are not large.",
      "<strong>Trees train in seconds.</strong> The iteration speed alone changes what you can try.",
      "<strong>Trees give usable feature importances</strong> without extra machinery.",
    ]),
    ("p", "Neural networks earn their place on images, audio, text and sequences — anywhere the raw input has structure the model should learn its own features from. A table of engineered columns is the case where that advantage does not apply, because you already did the feature engineering."),

    ("know",
     "On tabular data, start with gradient-boosted trees and treat a neural network as the thing you have to justify.",
     "Networks earn their advantage where the model should discover its own features from raw structure — pixels, waveforms, tokens. A table of engineered columns is precisely the case where that advantage does not exist, and the costs remain.",
     "The turbine project has six engineered features and 6,000 rows. A random forest trains in under a second and needs no scaling. A network needs normalisation, an architecture choice, a learning rate, an epoch budget and early stopping — and lands in the same place. Build it to learn how, then ship the forest."),

    ("h2", "If you are building one anyway"),
    ("terms", [
      ("Normalise the inputs", "Non-negotiable", "Unscaled features make the loss surface pathological. This is the commonest cause of a network that will not train."),
      ("Start small", "One or two hidden layers", "Depth is for structured raw input. On tabular data, depth mostly buys overfitting."),
      ("Overfit one batch first", "Ninety seconds", "Proves the loop is wired before you tune anything."),
      ("Early stopping on validation", "Always", "Networks will fit noise indefinitely if you let them."),
      ("Class weights for imbalance", "Same as elsewhere", "The rare class needs to cost more, or the network learns to predict the majority."),
    ]),

    ("links", [
      ("Keras 3 — multi-backend", "https://keras.io/getting_started/",
       "Backend selection, and what changes and does not when you switch."),
      ("PyTorch — training loop basics", "https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html",
       "The manual loop written out and explained, step by step."),
    ]),

    ("books", [
      ("Hands-On Machine Learning with Scikit-Learn and PyTorch", "Aurelien Geron",
       "The neural network chapters, with the same architectures built both ways."),
      ("AI and Machine Learning for Coders in PyTorch", "Laurence Moroney",
       "On your shelf. Written by the author of the Keras-era edition, so the framing of the transition is unusually clear."),
    ]),

    ("quiz", [
      ("The same Keras code trains under two backends and produces slightly different losses. What does that indicate?",
       ["A bug in one of the backends",
        "Normal behaviour — random number generation and floating-point ordering differ, so reproducibility is approximate",
        "The seed was not set correctly"], 1),
      ("What does Keras's fit() do that a manual PyTorch loop makes you write?",
       ["It uses a different optimisation algorithm",
        "Batching, gradient clearing, backpropagation, the optimiser step, metrics and callbacks",
        "It automatically selects the architecture"], 1),
      ("Why do gradient-boosted trees usually beat neural networks on tabular data?",
       ["Trees are mathematically more expressive",
        "Networks earn their advantage by learning features from raw structure, and an engineered table has none left to learn",
        "Neural networks cannot handle categorical features at all"], 1),
      ("Your network's loss will not move from its starting value. What should you do first?",
       ["Lower the learning rate and train longer",
        "Try to overfit a single batch — if it cannot, the bug is in the loop or the data, not the hyperparameters",
        "Add more layers to increase capacity"], 1),
    ]),
  ],
},
{
  "slug": "time-series",
  "title": "Time Series, and Why Random Splits Lie",
  "subtitle": "The original syllabus omits this while three of its own case studies are time-series problems.",
  "body": [
    ("p", "Predictive maintenance, demand forecasting, ride-share volume — the syllabus uses all three as examples and never teaches the thing they have in common. Every one is ordered in time, and ordered data breaks the standard workflow in a way that produces excellent scores and worthless models."),

    ("h2", "Why the random split fails"),
    ("p", "A random split scatters rows from every period into both halves. The model trains on Tuesday and Thursday and is tested on Wednesday — surrounded, on both sides, by data it has already seen."),

    ("figure", "The random split lets the model interpolate between points it has already learned. Production never offers that; it only ever asks about the future.", '''<svg viewBox="0 0 640 210" role="img" aria-label="Random split versus time-ordered split">
<text x="12" y="18" class="d-fill-red" font-size="12" font-weight="600">RANDOM SPLIT — leaks the future</text>
<line x1="12" y1="58" x2="620" y2="58" stroke="var(--border)" stroke-width="2"/>
<g class="d-fill-accent">
<circle cx="40" cy="58" r="6"/><circle cx="130" cy="58" r="6"/><circle cx="200" cy="58" r="6"/>
<circle cx="330" cy="58" r="6"/><circle cx="440" cy="58" r="6"/><circle cx="560" cy="58" r="6"/>
</g>
<g class="d-fill-red">
<circle cx="85" cy="58" r="6"/><circle cx="265" cy="58" r="6"/><circle cx="385" cy="58" r="6"/><circle cx="500" cy="58" r="6"/>
</g>
<text x="12" y="84" class="d-label-sm">blue = train, red = test. Every test point sits between two training points.</text>
<line x1="12" y1="104" x2="628" y2="104" stroke="var(--border)"/>
<text x="12" y="130" class="d-fill-green" font-size="12" font-weight="600">TIME-ORDERED SPLIT — matches production</text>
<line x1="12" y1="164" x2="620" y2="164" stroke="var(--border)" stroke-width="2"/>
<g class="d-fill-accent">
<circle cx="40" cy="164" r="6"/><circle cx="100" cy="164" r="6"/><circle cx="160" cy="164" r="6"/>
<circle cx="220" cy="164" r="6"/><circle cx="280" cy="164" r="6"/><circle cx="340" cy="164" r="6"/>
</g>
<line x1="378" y1="140" x2="378" y2="188" stroke="var(--yellow)" stroke-width="2" stroke-dasharray="4 4"/>
<g class="d-fill-red">
<circle cx="420" cy="164" r="6"/><circle cx="480" cy="164" r="6"/><circle cx="540" cy="164" r="6"/><circle cx="600" cy="164" r="6"/>
</g>
<text x="12" y="196" class="d-label-sm">train on the past, test on the future — the only split that answers the question you are actually asking</text>
</svg>'''),

    ("know",
     "A random split on time-ordered data trains on the future and tests on the past.",
     "Real deployment only ever asks about the future. A model validated by interpolating between known points has been asked an easier question than the one it will face, and the gap between the two shows up as a launch-day collapse.",
     "A demand model scores 0.91 R-squared on a random split and 0.62 when re-validated on a time-ordered one. Nothing changed but the split. The first number was measuring how well it could fill gaps in a period it had already learned."),

    ("h2", "Walk-forward validation"),
    ("p", "The time-series equivalent of cross-validation. Train on everything up to a point, test on what comes next, then move the boundary forward and repeat. You get several estimates, each of which is honest about direction."),
    ("terms", [
      ("Expanding window", "Train set grows each fold", "Uses all history. The default when older data stays relevant."),
      ("Sliding window", "Fixed-length train set that moves", "Discards old data deliberately. Right when the process changes and history becomes misleading."),
      ("Gap between train and test", "Often necessary", "If your prediction is used a week ahead, leave a week's gap — otherwise you are testing with information the deployed model will not have."),
    ]),
    ("callout", "matters", "The gap is the part people leave out", "You predict failures 90 days ahead. If your test period starts the day after your training period ends, the model is being scored on a task it will never be given — it had data up to yesterday and is predicting tomorrow, when in production it will have data from 90 days ago. Insert the gap and the honest score is usually noticeably lower."),

    ("h2", "Features that only exist in time series"),
    ("terms", [
      ("Lags", "The value n periods ago", "Yesterday's reading, last week's total. Frequently the single strongest predictor, and the one to build first."),
      ("Rolling statistics", "Mean, max, standard deviation over a window", "A seven-day rolling mean smooths noise; a rolling standard deviation captures instability, which is often the real signal."),
      ("Differences", "Change since last period", "Converts a level into a movement, which is usually what matters."),
      ("Time since an event", "Days since last fault or service", "Encodes recency directly rather than hoping the model infers it."),
      ("Calendar features", "Day of week, month, holiday", "Cheap, and they capture seasonality no lag will."),
    ]),
    ("callout", "pitfall", "Every rolling feature is a leakage opportunity", "A rolling mean computed over the whole series before splitting includes future values in every row. The window must only ever look backwards, and the calculation must happen inside the fold. This is the single commonest bug in time-series pipelines, and it produces a beautiful score."),

    ("know",
     "Any feature computed across the whole series before splitting has put the future into your training rows.",
     "Rolling means, normalisations, target encodings and imputations all aggregate over rows. Compute them before the split and each training row carries information from dates after it — invisible in the metrics and fatal in production.",
     "A team normalises a sensor column by its overall mean and standard deviation, then splits by time. Every training row is now scaled using statistics that include the test period. The model looks excellent, ships, and degrades immediately — the scaler it needs at inference cannot see the future it was calibrated against."),

    ("h2", "What to check before modelling"),
    ("ul", [
      "<strong>Plot it.</strong> Trend, seasonality, level shifts and obvious breaks are visible in one chart and invisible in summary statistics.",
      "<strong>Check the sampling.</strong> Irregular intervals, missing periods and duplicated timestamps all break lag features silently.",
      "<strong>Look for regime changes.</strong> A sensor recalibration or a process change means older data may be actively misleading, which is the argument for a sliding window.",
      "<strong>Establish the naive baseline.</strong> \"Tomorrow equals today\" is remarkably hard to beat on many series, and it is the number your model must clear.",
    ]),
    ("callout", "insight", "The naive forecast is the majority-class baseline of time series", "Predicting that the next value equals the last one — or the value from the same day last week, for seasonal data — costs nothing and beats a surprising number of models. Compute it first, and if your model cannot clear it, you have learned that early and cheaply."),

    ("links", [
      ("Time series splitting — scikit-learn", "https://scikit-learn.org/stable/modules/cross_validation.html#time-series-split",
       "TimeSeriesSplit, which implements walk-forward validation with the correct ordering."),
      ("Forecasting: Principles and Practice", "https://otexts.com/fpp3/",
       "Hyndman and Athanasopoulos, free online. The standard reference, and unusually readable."),
    ]),

    ("quiz", [
      ("Why does a random split inflate scores on time-ordered data?",
       ["Random splits always produce optimistic estimates",
        "Test points sit between training points, so the model interpolates rather than forecasting — an easier task than production asks",
        "Time series have more autocorrelation than tabular data"], 1),
      ("Your model will be used to predict 90 days ahead. What must your validation include?",
       ["A larger test set to cover the period",
        "A 90-day gap between the end of training and the start of testing, matching the information the deployed model will have",
        "Only the most recent 90 days as training data"], 1),
      ("You compute a rolling mean over the full series, then split by time. What went wrong?",
       ["Rolling means should be computed after modelling",
        "Every training row now includes information from dates after it — the future is in your training data",
        "The window length was probably too long"], 1),
      ("What is the naive baseline for a time series?",
       ["The mean of the training period",
        "The next value equals the last one, or the same period last season",
        "A linear trend fitted to the whole series"], 1),
    ]),
  ],
},
]
