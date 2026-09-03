TITLE = "Algorithms That Matter Here"
TOPIC = "algorithms"
ICON = "⚙️"
DESCRIPTION = "The algorithms this domain actually runs on — from gradient descent to HNSW — explained by what they do and where they break, not by their derivations."
TAGS = ["ai", "algorithms", "ml"]
COLOR = "purple"
CREATED = "2026-08-20"
ID_BASE = "1787100000"

LESSONS = [
{
  "slug": "gradient-descent-and-backprop",
  "title": "Gradient Descent and Backpropagation",
  "subtitle": "The one algorithm underneath every trained model you will ever use.",
  "body": [
    ("p", "Your statistics course covers <em>why</em> a loss function measures wrongness. This one covers <em>how</em> a model uses that measurement to change itself. Every model in this program — linear regression, a neural network, a fine-tuned LLM — is trained by the same two-step algorithm."),

    ("h2", "Gradient descent: walking downhill in fog"),
    ("p", "You have a loss — a number saying how wrong the model currently is — and millions of parameters you could adjust. The <strong>gradient</strong> is the slope of the loss with respect to each parameter: for every knob, which direction makes things worse, and how steeply. Move each parameter a small step the other way. Recompute. Repeat."),

    ("figure", "Learning rate is the step size. Too small and training crawls; too large and you overshoot the minimum repeatedly and never settle. Most training instability is this parameter.", '''<svg viewBox="0 0 640 200" role="img" aria-label="Effect of learning rate on gradient descent">
<g>
<text x="40" y="18" class="d-fill-red" font-size="12" font-weight="600">too small</text>
<path d="M20 40 Q100 170 180 40" stroke="var(--border)" stroke-width="2" fill="none"/>
<circle cx="40" cy="100" r="4" class="d-fill-red"/><circle cx="52" cy="122" r="4" class="d-fill-red"/>
<circle cx="63" cy="138" r="4" class="d-fill-red"/><circle cx="73" cy="150" r="4" class="d-fill-red"/>
<text x="24" y="190" class="d-label-sm">creeps — may never arrive</text>
</g>
<g>
<text x="255" y="18" class="d-fill-green" font-size="12" font-weight="600">about right</text>
<path d="M230 40 Q310 170 390 40" stroke="var(--border)" stroke-width="2" fill="none"/>
<circle cx="248" cy="98" r="4" class="d-fill-green"/><circle cx="278" cy="147" r="4" class="d-fill-green"/>
<circle cx="305" cy="164" r="4" class="d-fill-green"/><circle cx="312" cy="166" r="4" class="d-fill-green"/>
<text x="244" y="190" class="d-label-sm">converges</text>
</g>
<g>
<text x="470" y="18" class="d-fill-red" font-size="12" font-weight="600">too large</text>
<path d="M440 40 Q520 170 600 40" stroke="var(--border)" stroke-width="2" fill="none"/>
<circle cx="455" cy="112" r="4" class="d-fill-red"/><circle cx="588" cy="60" r="4" class="d-fill-red"/>
<circle cx="462" cy="102" r="4" class="d-fill-red"/><circle cx="595" cy="48" r="4" class="d-fill-red"/>
<path d="M457 108 L585 64 M586 62 L464 100" class="d-arrow"/>
<text x="440" y="190" class="d-label-sm">overshoots, diverges</text>
</g>
</svg>'''),

    ("h2", "The three flavours you will see named"),
    ("terms", [
      ("Batch", "Whole dataset per step", "Accurate gradient, impossibly slow at scale. Rarely used as-is."),
      ("Stochastic (SGD)", "One example per step", "Fast and noisy. The noise sometimes helps escape bad minima."),
      ("Mini-batch", "32–512 examples per step", "What everyone actually uses. Batch size is a memory-versus-stability trade."),
    ]),
    ("p", "An <strong>epoch</strong> is one full pass through the training data. Modern optimisers — <strong>Adam</strong> most commonly — adapt the step size per parameter rather than using one global learning rate, which is why they're the default in nearly every framework you'll touch."),

    ("h2", "Backpropagation: getting the gradient cheaply"),
    ("p", "In a network with many layers, a parameter in layer one affects the loss only through everything that comes after it. <strong>Backpropagation</strong> computes all those gradients efficiently by applying the chain rule backwards from the loss, reusing intermediate results rather than recomputing them per parameter."),
    ("p", "That efficiency is the whole reason deep learning is feasible. Computing gradients naively — nudging each parameter and re-measuring — would take a forward pass per parameter. For a 7-billion-parameter model that is not a slow approach; it is an impossible one."),
    ("callout", "insight", "What this explains", "Backprop's cost is why training needs so much more memory than inference: the intermediate activations from the forward pass must be kept so the backward pass can use them. It's also why LoRA is cheap — freeze most parameters and you neither store nor compute their gradients."),

    ("h2", "Where it goes wrong"),
    ("ul", [
      "<strong>Diverging loss.</strong> Loss climbs or becomes NaN. Learning rate too high, almost always. Lower it by 10× first.",
      "<strong>Plateau.</strong> Loss stops moving early. Learning rate too low, or gradients vanishing through many layers.",
      "<strong>Loss falls, validation doesn't.</strong> Not an optimisation problem — that's overfitting, and more training makes it worse.",
    ]),

    ("h2", "The numbers that make it concrete"),
    ("p", "Abstractly this is downhill walking. Concretely, here is what a training run costs. A 7-billion-parameter model at 16-bit precision is about 14GB of weights. Training it needs roughly four times that again: gradients (one per parameter), plus the optimiser's own state — Adam keeps two running averages per parameter, which is where most of the surprise comes from."),
    ("terms", [
      ("Weights", "~14 GB", "The model itself, at 16-bit."),
      ("Gradients", "~14 GB", "One per parameter, alive during the backward pass."),
      ("Optimiser state", "~28 GB", "Adam's two moments per parameter. Frequently the largest single item."),
      ("Activations", "Varies with batch and sequence", "Kept from the forward pass so backprop can use them. The knob you actually tune when you run out of memory."),
    ]),
    ("callout", "insight", "Why LoRA is not a small optimisation", "Freeze the base weights and train small adapter matrices instead, and you eliminate gradients and optimiser state for almost every parameter. The 56GB above collapses toward the 14GB of frozen weights plus a rounding error. That is the difference between fine-tuning needing a datacentre and needing your laptop, and it is pure bookkeeping rather than a cleverer algorithm."),

    ("h2", "Reading a loss curve"),
    ("terms", [
      ("Falls then flattens", "Healthy", "The flattening is where early stopping earns its place."),
      ("Spikes then recovers", "Usually fine", "A hard batch. Persistent spiking means the learning rate is too high or gradients need clipping."),
      ("Goes to NaN", "Broken", "Learning rate first, always. Then check for division by zero or a log of zero in a custom loss."),
      ("Flat from step one", "Wiring bug", "Not a learning-rate problem. Labels not connected, loss computed on the wrong tensor, or gradients not flowing. Overfit one batch to find out."),
      ("Falls, validation rises", "Not optimisation", "That is overfitting. More training makes it worse, not better."),
    ]),
    ("callout", "matters", "The debugging move worth doing first, every time", "Take one batch of about eight examples and train on it repeatedly with everything else held constant. A correctly-wired network will drive that loss to nearly zero — it can memorise eight things trivially. If it cannot, the bug is in the loop, the data pipeline or the loss, and no amount of hyperparameter tuning will find it. This takes two minutes and it separates 'the model cannot learn this' from 'the code does not work'."),

    ("books", [
      ("The Principles of Deep Learning Theory", "Roberts, Yaida & Hanin",
       "For when the intuition stops being enough. Rigorous, and the treatment of initialisation and why depth is hard is the real thing rather than an analogy."),
      ("Hands-On Machine Learning with Scikit-Learn and PyTorch", "Aurelien Geron",
       "The practical counterpart — training loops, optimisers and schedules with code you can run."),
    ]),

    ("know",
     'Overfit a single batch before anything else.',
     'A correctly-wired network can memorise eight examples trivially, driving loss to near zero. If it cannot, the bug is in the loop, the data pipeline or the loss function — and no amount of hyperparameter tuning will find it.',
     'Your loss sits flat at 2.3 from the first step and you spend an afternoon sweeping learning rates. Training on one batch would have shown the same flat line in ninety seconds and told you it was not a learning-rate problem. The labels were being passed in the wrong argument position.'),
    ("related", ["neural-networks-both-ways", "when-the-training-run-does-not-fit", "overfitting-and-underfitting", "loops-in-training"]),
    ("links", [
      ("Google ML Crash Course: gradient descent", "https://developers.google.com/machine-learning/crash-course/linear-regression/gradient-descent",
       "Interactive treatment of step size and convergence."),
      ("PyTorch autograd", "https://docs.pytorch.org/docs/stable/notes/autograd.html",
       "How backprop is actually implemented in the framework you'll use."),
    ]),

    ("quiz", [
      ("Training loss becomes NaN after a few hundred steps. First thing to try?",
       ["Add more layers", "Lower the learning rate by roughly 10×", "Train for more epochs"], 1),
      ("Why does training need far more memory than inference?",
       ["The optimiser stores a second copy of the model",
        "Intermediate activations from the forward pass must be kept for the backward pass",
        "Gradients are stored at higher precision than weights"], 1),
      ("Why is backpropagation necessary rather than just nudging each parameter to see what happens?",
       ["Nudging would need one forward pass per parameter — impossible at billions of parameters",
        "Nudging gives the wrong direction",
        "Nudging only works for linear models"], 0),
    ]),
  ],
},
{
  "slug": "regression-algorithms",
  "title": "Linear and Logistic Regression",
  "subtitle": "The two algorithms you should try before anything clever — and the baseline everything else must beat.",
  "body": [
    ("p", "These are the workhorses. They're also the <strong>dumb baseline</strong> your intake sheet demands, which makes them the most useful algorithms in this lesson set — not because they win often, but because they tell you whether winning was hard."),

    ("h2", "Linear regression predicts a number"),
    ("p", "Fit a straight line (or plane, in more dimensions) through the data so that squared error is smallest. Each input gets a coefficient saying how much it moves the output. That's it."),
    ("p", "The underrated property is <strong>interpretability</strong>: the coefficients are readable. \"Each extra year of equipment age adds 0.4 to predicted failure risk\" is a sentence you can take to a stakeholder. A gradient-boosted ensemble that scores two points higher gives you nothing you can say out loud."),

    ("h2", "Logistic regression predicts a probability"),
    ("p", "Despite the name, it classifies. It fits a linear combination of inputs and then squashes the result through a sigmoid into the range 0–1, giving a probability rather than a hard label."),
    ("callout", "matters", "Where the threshold lives", "Logistic regression outputs 0.73, not \"fraud\". Turning that into a decision requires a threshold, and choosing it is a business decision about the cost of false positives versus false negatives — question 6 on your intake sheet. The default of 0.5 is a convention, not an answer."),

    ("figure", "Linear regression fits a line through values. Logistic regression fits an S-curve through probabilities, and the threshold you draw across it — not the model — decides what counts as a positive.", '''<svg viewBox="0 0 640 190" role="img" aria-label="Linear versus logistic regression">
<g>
<text x="70" y="18" class="d-accent">LINEAR — predicts a value</text>
<line x1="30" y1="160" x2="290" y2="160" class="d-arrow"/>
<line x1="30" y1="160" x2="30" y2="30" class="d-arrow"/>
<circle cx="70" cy="130" r="3.5" class="d-fill-muted"/><circle cx="110" cy="118" r="3.5" class="d-fill-muted"/>
<circle cx="150" cy="92" r="3.5" class="d-fill-muted"/><circle cx="190" cy="84" r="3.5" class="d-fill-muted"/>
<circle cx="230" cy="56" r="3.5" class="d-fill-muted"/><circle cx="260" cy="52" r="3.5" class="d-fill-muted"/>
<path d="M50 140 L278 44" stroke="var(--accent)" stroke-width="2.5"/>
</g>
<g>
<text x="380" y="18" class="d-accent">LOGISTIC — predicts a probability</text>
<line x1="350" y1="160" x2="620" y2="160" class="d-arrow"/>
<line x1="350" y1="160" x2="350" y2="30" class="d-arrow"/>
<path d="M360 148 Q450 146 485 96 Q520 46 610 42" stroke="var(--accent)" stroke-width="2.5" fill="none"/>
<line x1="350" y1="96" x2="620" y2="96" stroke="var(--red)" stroke-width="1.6" stroke-dasharray="5 4"/>
<text x="556" y="90" class="d-fill-red" font-size="11" font-weight="600">threshold</text>
<text x="336" y="46" class="d-label-sm">1.0</text>
<text x="336" y="164" class="d-label-sm">0</text>
<circle cx="400" cy="148" r="3.5" class="d-fill-muted"/><circle cx="440" cy="146" r="3.5" class="d-fill-muted"/>
<circle cx="540" cy="52" r="3.5" class="d-fill-muted"/><circle cx="580" cy="44" r="3.5" class="d-fill-muted"/>
</g>
</svg>'''),

    ("h2", "Regularised variants worth knowing by name"),
    ("terms", [
      ("Ridge (L2)", "Shrinks coefficients toward zero", "Handles correlated inputs gracefully. Keeps every feature, just smaller."),
      ("Lasso (L1)", "Drives some coefficients to exactly zero", "Performs feature selection for you. Useful when you suspect most inputs are noise."),
      ("Elastic Net", "Both penalties combined", "The pragmatic default when you don't know which you want."),
    ]),

    ("h2", "Assumptions that break quietly"),
    ("ul", [
      "<strong>Linearity.</strong> The relationship really is roughly a straight line. Plot it before assuming.",
      "<strong>Independence.</strong> Rows don't influence each other. Time series violate this badly — consecutive days are not independent samples.",
      "<strong>No extreme multicollinearity.</strong> Two nearly-identical inputs make coefficients unstable and uninterpretable, even while predictions stay fine.",
      "<strong>Outlier sensitivity.</strong> Squared error means one extreme point can drag the whole line.",
    ]),
    ("callout", "pitfall", "The thing to actually do", "Run logistic or linear regression first, on every tabular problem, before touching a neural network. If it gets within a couple of points of your fancy model, ship the simple one — it trains in seconds, deploys anywhere, and you can explain its decisions when someone asks."),

    ("h2", "Reading the coefficients, which is the point"),
    ("p", "Fit a model on the turbine data and you get a number per feature. Those numbers are the deliverable as much as the predictions are — but only if you read them carefully."),
    ("terms", [
      ("Scale changes everything", "Standardise before comparing", "A coefficient on vibration in mm/s and one on hours are not comparable magnitudes. Standardise the inputs first, then relative sizes mean something."),
      ("Sign can flip", "When features correlate", "Add a correlated feature and a coefficient can reverse sign while predictions barely move. That is multicollinearity, and it is why an unstable coefficient is a warning about your features rather than about the world."),
      ("Log-odds, not probability", "For logistic regression", "A coefficient of 0.7 does not mean 70%. Exponentiate it for an odds ratio — about 2.0, meaning the odds roughly double per unit."),
      ("Association, not cause", "Always", "Coefficients describe the fitted surface. They are not effects, and reporting them as effects is the commonest way a good model produces a bad decision."),
    ]),

    ("h2", "What to try before concluding it is too simple"),
    ("ul", [
      "<strong>Transform the inputs.</strong> Linear in the <em>parameters</em> does not mean linear in the data. Adding a squared term or a log fits a curve while staying a linear model.",
      "<strong>Add interactions.</strong> Vibration multiplied by age captures 'old and shaking' as its own signal, which neither term carries alone.",
      "<strong>Bin a stubborn variable.</strong> Sometimes the relationship is a step, not a slope.",
      "<strong>Check the residuals.</strong> Plot errors against predictions. Structure in that plot — a curve, a fan — tells you what the model is missing far more precisely than a single score does.",
    ]),
    ("callout", "insight", "The residual plot is the most under-used diagnostic in tabular ML", "A well-fitted model leaves residuals that look like noise: no pattern, constant spread. A curve means you are missing a non-linear term. A fan shape — errors growing with the prediction — means the variance is not constant, and your confidence intervals are wrong even where the predictions are fine. One plot, and it tells you which of those you have."),

    ("books", [
      ("Hands-On Machine Learning with Scikit-Learn and PyTorch", "Aurelien Geron",
       "Chapter 4 works through linear and logistic regression with the regularised variants, including the geometry of why Lasso zeroes coefficients and Ridge does not."),
    ]),
    ("related", ["decision-trees", "baseline-to-model", "overfitting-and-underfitting", "is-the-difference-real"]),
    ("links", [
      ("Linear models (scikit-learn)", "https://scikit-learn.org/stable/modules/linear_model.html",
       "Ridge, Lasso and Elastic Net with the maths and the API side by side."),
    ]),

    ("quiz", [
      ("Logistic regression outputs 0.73 for a transaction. What has the model decided?",
       ["That it's fraud", "Nothing — it gave a probability; the threshold you choose makes the decision",
        "That it's 73% of the way to the decision boundary"], 1),
      ("Why prefer Lasso over Ridge when you suspect most of your features are noise?",
       ["Lasso trains faster", "Lasso drives useless coefficients to exactly zero, selecting features for you",
        "Lasso handles correlated features better"], 1),
      ("Your boosted model beats logistic regression by 1.5 points. What should you weigh?",
       ["Always ship the higher score",
        "Whether 1.5 points is worth losing interpretability, fast training and simple deployment",
        "Whether the boosted model used more features"], 1),
    ]),
  ],
},
{
  "slug": "decision-trees",
  "title": "Decision Trees: How a Split Gets Chosen",
  "subtitle": "The one algorithm you can read end to end — and the reason it overfits so eagerly.",
  "body": [
    ("p", "A decision tree asks a sequence of yes/no questions about the inputs and follows the answers to a prediction. Its appeal is total transparency: you can print the tree and read exactly why any single prediction was made. No other competitive algorithm offers that."),

    ("h2", "Choosing the split"),
    ("p", "At each node the algorithm tries every feature and every threshold, and picks the split that makes the resulting groups most <em>pure</em> — most dominated by a single class. Purity is measured two ways in practice:"),
    ("terms", [
      ("Gini impurity", "Probability of mislabelling a random item", "0 means perfectly pure. The scikit-learn default, and marginally faster."),
      ("Entropy", "Information-theoretic disorder", "The same quantity your statistics course covers. Gives near-identical trees to Gini in practice."),
      ("Variance reduction", "For regression trees", "Pick the split that most reduces variance within each group."),
    ]),
    ("p", "Then it recurses on each group. That's the whole algorithm — greedy, local, and never revisiting an earlier split even if a later one would have justified a different choice."),

    ("figure", "Each split partitions the data further. Left unchecked, the tree keeps splitting until every leaf holds a single training example — which is memorisation, not learning.", '''<svg viewBox="0 0 640 210" role="img" aria-label="Decision tree splitting and depth">
<rect x="250" y="12" width="140" height="34" rx="6" class="d-box-accent"/>
<text x="264" y="34" class="d-label-sm">age &gt; 4 years?</text>
<path d="M290 46 L190 76" class="d-arrow"/><text x="212" y="62" class="d-label-sm">no</text>
<path d="M350 46 L450 76" class="d-arrow"/><text x="404" y="62" class="d-label-sm">yes</text>
<rect x="120" y="76" width="140" height="34" rx="6" class="d-box"/>
<text x="132" y="98" class="d-label-sm">vibration &gt; 0.3?</text>
<rect x="380" y="76" width="140" height="34" rx="6" class="d-box"/>
<text x="392" y="98" class="d-label-sm">temp &gt; 80°?</text>
<path d="M160 110 L110 142" class="d-arrow"/><path d="M220 110 L262 142" class="d-arrow"/>
<path d="M420 110 L378 142" class="d-arrow"/><path d="M480 110 L528 142" class="d-arrow"/>
<rect x="60" y="142" width="96" height="30" rx="5" class="d-box-good"/>
<text x="80" y="162" class="d-label-sm">healthy</text>
<rect x="216" y="142" width="96" height="30" rx="5" class="d-box-warn"/>
<text x="240" y="162" class="d-label-sm">at risk</text>
<rect x="332" y="142" width="96" height="30" rx="5" class="d-box-good"/>
<text x="352" y="162" class="d-label-sm">healthy</text>
<rect x="488" y="142" width="96" height="30" rx="5" class="d-box-warn"/>
<text x="512" y="162" class="d-label-sm">at risk</text>
<text x="12" y="196" class="d-label-sm">Keep going and every leaf ends up holding one training row. Depth is the overfitting dial — limit it, or prune after.</text>
</svg>'''),

    ("h2", "Why trees overfit so readily"),
    ("p", "Nothing in the algorithm says stop. Given enough depth a tree can isolate every training example in its own leaf, achieving perfect training accuracy and learning nothing generalisable. This is the overfitting lesson made concrete — and it's why the controls all constrain growth:"),
    ("ul", [
      "<code>max_depth</code> — how many questions deep the tree may go",
      "<code>min_samples_leaf</code> — refuse splits that would create tiny leaves",
      "<code>min_samples_split</code> — don't split a node with too few examples",
      "<strong>Pruning</strong> — grow fully, then cut back branches that don't help validation performance",
    ]),
    ("callout", "pitfall", "The instability nobody warns you about", "Change a handful of training rows and a decision tree can restructure completely — a different feature wins at the root and everything below changes. That variance is exactly what ensembles exist to cancel out, which is the next lesson."),

    ("h2", "What they're good and bad at"),
    ("p", "Good: mixed numeric and categorical inputs, no scaling required, non-linear relationships, missing values handled natively by some implementations, and complete interpretability. Bad: smooth relationships (they approximate a line with a staircase), extrapolation beyond the training range (impossible — they predict a constant per leaf), and stability."),

    ("h2", "A split, computed"),
    ("p", "Worth doing once by hand, because it demystifies the whole family. Take 100 turbines, 20 of which failed. Before any split, Gini impurity is 1 minus the sum of squared class proportions: 1 − (0.8² + 0.2²) = 0.32."),
    ("p", "Now try splitting on vibration above 0.5. Suppose that puts 30 turbines on one side, 15 of them failures, and 70 on the other, 5 of them failures:"),
    ("terms", [
      ("High-vibration group", "30 rows, 15 failures", "Gini = 1 − (0.5² + 0.5²) = 0.50. Worse than the parent — a coin flip."),
      ("Low-vibration group", "70 rows, 5 failures", "Gini = 1 − (0.93² + 0.07²) = 0.13. Much purer."),
      ("Weighted result", "0.3 × 0.50 + 0.7 × 0.13 = 0.24", "Down from 0.32. That reduction of 0.08 is the split's score."),
    ]),
    ("p", "The algorithm computes that number for every feature at every candidate threshold and keeps the best. Then it recurses. Everything else — random forests, gradient boosting, the whole tabular-ML establishment — is built on top of that one greedy calculation."),
    ("callout", "insight", "Why the split can look like it makes things worse", "The high-vibration group came out at 0.50, above the parent's 0.32, and the split is still excellent. Purity is judged on the weighted average of the children, not on each child, because you have isolated 70 rows you can now be confident about. A group that is uncertain but small costs little."),

    ("h2", "Feature importance, and why it misleads"),
    ("p", "Trees report which features drove the splits, and this is one of the most trusted and most misread outputs in machine learning. The default measure — total impurity reduction attributed to each feature — is biased toward high-cardinality features. A continuous variable offers hundreds of candidate thresholds; a binary flag offers one. The continuous variable wins more splits partly on opportunity rather than on merit."),
    ("callout", "pitfall", "Use permutation importance when the answer matters", "Shuffle one feature's values and measure how much performance drops. That directly answers the question people think they are asking — does the model actually rely on this? — and it is computed on held-out data, so it reflects generalisation rather than how the tree happened to be built. Slower, and worth it whenever the importance ranking will be shown to anyone who might act on it."),

    ("books", [
      ("Grokking AI Algorithms", "Rishal Hurbans",
       "Visual, patient treatment of tree construction if the split calculation above went past too quickly."),
      ("Hands-On Machine Learning with Scikit-Learn and PyTorch", "Aurelien Geron",
       "Chapter 6 on trees, including exporting one as readable text — worth doing once on a real model."),
    ]),
    ("related", ["ensembles", "baseline-to-model", "overfitting-and-underfitting", "regression-algorithms"]),
    ("links", [
      ("Decision trees (scikit-learn)", "https://scikit-learn.org/stable/modules/tree.html",
       "Splitting criteria, the pruning parameters, and how to export a tree as readable text."),
    ]),

    ("quiz", [
      ("What does a decision tree optimise for when choosing a split?",
       ["The split that produces the most balanced groups",
        "The split that makes the resulting groups purest — most dominated by one class",
        "The split on the feature with highest correlation to the target"], 1),
      ("A tree scores 100% on training data and 68% on validation. What happened?",
       ["The validation set is mislabelled",
        "It grew until each leaf isolated individual training rows — memorisation",
        "The splitting criterion was wrong"], 1),
      ("Why can a decision tree never extrapolate beyond its training range?",
       ["It refuses inputs outside the range",
        "Each leaf predicts a constant, so anything beyond the last split gets that leaf's value",
        "The splits are computed on normalised data"], 1),
    ]),
  ],
},
{
  "slug": "ensembles",
  "title": "Ensembles: Bagging, Forests and Boosting",
  "subtitle": "Why many mediocre models beat one good one — and which kind to reach for.",
  "body": [
    ("p", "A single decision tree is unstable and overfits. Combine many of them correctly and you get one of the strongest algorithm families available for tabular data — still, in 2026, routinely beating neural networks on the kind of data most businesses actually have."),

    ("h2", "Two strategies, opposite in spirit"),

    ("figure", "Bagging trains many independent models in parallel and averages away their variance. Boosting trains models in sequence, each one correcting what the last got wrong.", '''<svg viewBox="0 0 640 220" role="img" aria-label="Bagging versus boosting">''' + '<defs><marker id="ea" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" class="d-fill-muted"/></marker></defs>' + '''
<text x="12" y="20" class="d-accent">BAGGING — parallel, independent</text>
<rect x="12" y="32" width="70" height="26" rx="4" class="d-box"/><text x="30" y="50" class="d-label-sm">tree 1</text>
<rect x="12" y="64" width="70" height="26" rx="4" class="d-box"/><text x="30" y="82" class="d-label-sm">tree 2</text>
<rect x="12" y="96" width="70" height="26" rx="4" class="d-box"/><text x="30" y="114" class="d-label-sm">tree 3</text>
<path d="M82 45 L140 72" class="d-arrow" marker-end="url(#ea)"/>
<path d="M82 77 L140 77" class="d-arrow" marker-end="url(#ea)"/>
<path d="M82 109 L140 82" class="d-arrow" marker-end="url(#ea)"/>
<rect x="140" y="60" width="90" height="34" rx="5" class="d-box-good"/>
<text x="152" y="82" class="d-label-sm">average</text>
<text x="12" y="146" class="d-label-sm">cancels variance</text>
<text x="12" y="162" class="d-label-sm">hard to overfit</text>
<line x1="270" y1="20" x2="270" y2="190" stroke="var(--border)" stroke-width="1"/>
<text x="300" y="20" class="d-accent">BOOSTING — sequential, corrective</text>
<rect x="300" y="60" width="76" height="34" rx="4" class="d-box"/><text x="318" y="82" class="d-label-sm">tree 1</text>
<path d="M376 77 L404 77" class="d-arrow" marker-end="url(#ea)"/>
<rect x="404" y="60" width="76" height="34" rx="4" class="d-box"/><text x="422" y="82" class="d-label-sm">tree 2</text>
<path d="M480 77 L508 77" class="d-arrow" marker-end="url(#ea)"/>
<rect x="508" y="60" width="76" height="34" rx="4" class="d-box"/><text x="526" y="82" class="d-label-sm">tree 3</text>
<text x="300" y="118" class="d-label-sm">each trained on what</text>
<text x="300" y="134" class="d-label-sm">the previous got wrong</text>
<text x="300" y="162" class="d-label-sm">higher ceiling · will overfit if unchecked</text>
</svg>'''),

    ("h2", "Bagging and random forests"),
    ("p", "<strong>Bagging</strong> (bootstrap aggregating) trains each tree on a random sample of the rows, drawn with replacement, then averages their predictions. Because the trees see different data, their errors are partly independent, and averaging cancels them."),
    ("p", "A <strong>random forest</strong> adds a second source of randomness: at each split, only a random subset of features is considered. This stops every tree from picking the same dominant feature at the root, decorrelating them further. More decorrelation, more variance cancelled."),
    ("callout", "matters", "Why forests are the safe default", "A random forest is remarkably hard to overfit by adding trees — more trees converge toward a stable answer rather than degrading. It needs almost no tuning, handles mixed data types, and gives usable feature importances. When you need a strong tabular baseline in ten minutes, this is it."),

    ("p", "Bagging gives you a validation set for nothing, which is worth knowing about. Each tree is trained on a bootstrap sample, so roughly a third of the rows were not used to build any given tree &mdash; those are its <strong>out-of-bag</strong> rows. Score every row using only the trees that never saw it and you have an honest held-out estimate without ever splitting the data. It is free, it is available during training, and for a forest it is usually close enough to cross-validation to skip running one."),

    ("h2", "Boosting"),
    ("p", "<strong>Boosting</strong> works sequentially. Train a weak, shallow tree. Look at what it got wrong. Train the next tree specifically to fix those errors. Repeat, adding each new tree's contribution scaled by a learning rate."),
    ("p", "<strong>Gradient boosting</strong> formalises this: each new tree is fitted to the gradient of the loss — the residual errors — which is the same gradient descent idea from lesson 1, applied by adding models instead of adjusting weights. XGBoost, LightGBM and CatBoost are optimised implementations, and they win a great many tabular competitions."),
    ("callout", "pitfall", "Boosting will overfit if you let it", "Unlike forests, adding boosting rounds past the optimum makes the model worse. You need early stopping against a validation set, plus a low learning rate and shallow trees. More rounds is not more better."),

    ("h2", "Choosing between them"),
    ("terms", [
      ("Random forest", "Fast to a good answer", "Little tuning, resistant to overfitting, strong default. Start here."),
      ("Gradient boosting", "Higher ceiling, more care", "Usually wins on tuned performance. Needs early stopping and learning-rate tuning."),
      ("Single tree", "When you must explain it", "Occasionally the right answer purely because a human has to read the logic."),
    ]),
    ("p", "For the turbine project in Block 2, run a random forest before the neural network. If the forest wins — which happens more often than the marketing around deep learning suggests — that is a real result, not a failure."),

    ("h2", "Why averaging works, in one line of intuition"),
    ("p", "Every model's error splits into three parts: bias (wrong on average), variance (jumpy from sample to sample), and noise you cannot touch. Averaging many independent models leaves bias where it was and shrinks variance — roughly by the number of models, if their errors were truly independent."),
    ("p", "They never are. Trees trained on overlapping data make correlated mistakes, and that correlation is the ceiling on what averaging can buy you. Which is exactly why a random forest samples features at each split: not to be clever, but to drive correlation down so the averaging has more to cancel."),
    ("callout", "insight", "Boosting attacks the other term", "Bagging reduces variance and leaves bias alone. Boosting reduces bias by fitting each new model to what the ensemble still gets wrong — which is why it reaches higher and why it will happily fit noise once the real signal is exhausted. Two methods, two different terms of the same decomposition. That is the whole distinction, and it tells you which to reach for: unstable model, use bagging; underfitting model, use boosting."),

    ("h2", "The parameters that actually matter"),
    ("terms", [
      ("n_estimators (forest)", "More is safe", "Converges to a stable answer. Set it as high as you can afford and stop thinking about it."),
      ("n_estimators (boosting)", "More is dangerous", "Past the optimum it degrades. This is why early stopping is mandatory here and optional there."),
      ("learning_rate (boosting)", "The main dial", "Lower means each tree contributes less, so you need more of them and generalise better. 0.05 with early stopping is a sane default."),
      ("max_depth (boosting)", "Keep it shallow", "3 to 6. Deep trees in a boosted ensemble overfit fast — the ensemble supplies the complexity, not the individual tree."),
      ("subsample / colsample", "Randomness helps here too", "Sampling rows and columns per tree regularises boosting for the same reason it helps forests."),
    ]),
    ("callout", "pitfall", "The tuning trap", "Grid-searching a boosted model against your validation set for hours is a very efficient way to overfit the validation set. Tune a handful of parameters, keep the test set untouched, and remember that a forest at defaults is usually within a couple of points of a boosted model tuned for a day."),

    ("books", [
      ("Hands-On Machine Learning with Scikit-Learn and PyTorch", "Aurelien Geron",
       "Chapter 7 covers bagging, forests, boosting and stacking with the parameter guidance that matters in practice."),
    ]),
    ("related", ["decision-trees", "baseline-to-model", "overfitting-and-underfitting", "confusion-matrix-and-metrics"]),
    ("links", [
      ("Ensemble methods (scikit-learn)", "https://scikit-learn.org/stable/modules/ensemble.html",
       "Forests, gradient boosting and the histogram-based implementations, with parameter guidance."),
      ("XGBoost documentation", "https://xgboost.readthedocs.io/",
       "The tuning parameters that matter, and why early stopping is not optional."),
    ]),

    ("quiz", [
      ("Why does a random forest sample features at each split as well as sampling rows?",
       ["To train faster on wide datasets",
        "To stop every tree picking the same dominant feature, decorrelating them so averaging cancels more error",
        "To handle missing values"], 1),
      ("You add 500 more rounds to a gradient boosting model and validation performance drops. Why?",
       ["Boosting keeps fitting residuals, so past the optimum it starts fitting noise",
        "The learning rate decayed to zero",
        "The model ran out of features to split on"], 0),
      ("Which is the better ten-minute baseline on a new tabular problem?",
       ["Gradient boosting, because it has the higher ceiling",
        "Random forest, because it's resistant to overfitting and needs almost no tuning",
        "A neural network, because it handles any data type"], 1),
    ]),
  ],
},
{
  "slug": "clustering-and-knn",
  "title": "k-Means, k-NN and the Curse of Dimensionality",
  "subtitle": "Two algorithms built on distance — and the reason distance stops meaning much in high dimensions.",
  "body": [
    ("p", "Both algorithms in this lesson rest on the same assumption: that things close together are similar. That assumption is powerful, and it degrades in a specific way you need to recognise, because it also affects the embeddings and vector search you'll use in Block 3."),

    ("h2", "k-means: finding groups nobody labelled"),
    ("p", "You pick <em>k</em>, the number of clusters. The algorithm places k centres at random, then repeats two steps until nothing moves: assign every point to its nearest centre, then move each centre to the average of its assigned points. That's the entire algorithm."),
    ("terms", [
      ("You must choose k", "It cannot find it for you", "The elbow method and silhouette scores help, but this is a judgement call, not an output."),
      ("Assumes round clusters", "Of similar size", "Elongated or nested groups are found badly. k-means will still return an answer — a confident, wrong one."),
      ("Scale matters enormously", "Standardise first", "Income in pounds and age in years puts income in charge of every distance. This is the most common k-means mistake."),
      ("Random start", "Different runs, different answers", "Use k-means++ initialisation and multiple restarts."),
    ]),

    ("h2", "k-NN: no training at all"),
    ("p", "<strong>k-nearest neighbours</strong> doesn't build a model. To predict, it finds the k most similar training examples and takes their majority vote or average. All the work happens at prediction time, which makes training instant and inference expensive — the opposite profile from everything else here."),
    ("callout", "insight", "You already know this algorithm", "retrieval-augmented generation (RAG) is k-NN. Embed the query, find the nearest stored vectors, use them. The retrieval step in Block 3 is exactly this algorithm, run over embeddings instead of tabular features — which is why the failure modes below transfer directly."),

    ("h2", "The curse of dimensionality"),
    ("p", "As dimensions increase, points spread out and the distances between them converge. In very high dimensions the nearest and farthest neighbours of a point end up almost equidistant — so \"nearest\" carries progressively less meaning."),

    ("figure", "As dimensions rise, the gap between nearest and farthest neighbour collapses toward zero. 'Closest' becomes a weaker and weaker signal.", '''<svg viewBox="0 0 640 190" role="img" aria-label="Distance concentration in high dimensions">
<line x1="60" y1="150" x2="600" y2="150" class="d-arrow"/>
<line x1="60" y1="150" x2="60" y2="24" class="d-arrow"/>
<text x="4" y="80" class="d-label-sm">distance</text>
<text x="250" y="176" class="d-label-sm">dimensions →</text>
<path d="M80 130 Q200 96 340 80 Q460 70 590 66" stroke="var(--green)" stroke-width="2.5" fill="none"/>
<text x="500" y="58" class="d-fill-green" font-size="11" font-weight="600">nearest</text>
<path d="M80 40 Q200 50 340 60 Q460 62 590 62" stroke="var(--red)" stroke-width="2.5" fill="none"/>
<text x="500" y="36" class="d-fill-red" font-size="11" font-weight="600">farthest</text>
<path d="M90 44 L90 126" stroke="var(--muted)" stroke-width="1.4" stroke-dasharray="3 3"/>
<text x="98" y="90" class="d-label-sm">large gap — 'near' is meaningful</text>
<path d="M580 64 L580 68" stroke="var(--muted)" stroke-width="1.4"/>
<text x="404" y="100" class="d-label-sm">gap collapses — everything is</text>
<text x="404" y="116" class="d-label-sm">roughly equally far away</text>
</svg>'''),

    ("p", "This is why embeddings are typically a few hundred to a couple of thousand dimensions rather than tens of thousands, why dimensionality reduction (principal component analysis (PCA), uniform manifold approximation and projection (UMAP)) is worth knowing, and why hybrid retrieval — combining vector similarity with keyword matching — outperforms pure vector search on many real corpora. Pure distance is a weaker signal than it looks."),

    ("h2", "Choosing k, honestly"),
    ("p", "Two standard methods, and the honest caveat that neither is decisive."),
    ("terms", [
      ("Elbow method", "Plot within-cluster variance against k", "Look for where the curve bends. Real data frequently has no visible elbow, and then the method tells you nothing."),
      ("Silhouette score", "How well each point fits its cluster vs the next-nearest", "Ranges -1 to 1; pick the k that maximises the mean. More decisive than the elbow, and slower."),
      ("Domain constraint", "Usually the real answer", "You need four maintenance tiers because you have four crews. That beats both methods, and it is not a cop-out — k-means has no opinion about what a cluster means."),
    ]),
    ("callout", "matters", "Clusters are always returned, whether or not they exist", "Run k-means on uniform random noise with k set to five and you get five tidy clusters with a respectable-looking plot. The algorithm partitions; it does not detect structure. Before believing a clustering, check that the same k on shuffled data looks meaningfully worse. If it does not, you have found the algorithm's behaviour rather than your data's."),

    ("h2", "When k-means is the wrong shape"),
    ("ul", [
      "<strong>Elongated or curved groups.</strong> k-means draws straight boundaries around round blobs. density-based spatial clustering of applications with noise (DBSCAN) follows density instead and finds arbitrary shapes.",
      "<strong>Very different group sizes.</strong> A large cluster tends to get split while a small one gets absorbed.",
      "<strong>Outliers.</strong> Every point must join a cluster, so a few extreme values drag a centre toward them. DBSCAN can label points as noise; k-means cannot.",
      "<strong>Unknown k.</strong> If k is genuinely unknown, hierarchical clustering gives you the whole tree of possible groupings to cut where you like.",
    ]),

    ("books", [
      ("A Programmer's Guide to Data Mining", "Ron Zacharski",
       "Free online. The nearest-neighbour and similarity chapters build the intuition slowly, which is what this material needs."),
      ("Mining of Massive Datasets", "Leskovec, Rajaraman & Ullman",
       "Chapter 7 on clustering at scale, including what changes when the data does not fit in memory."),
    ]),

    ("know",
     'Clusters are always returned, whether or not they exist.',
     'k-means partitions; it does not detect structure. Ask for five clusters and you get five, with centroids and a plot that looks entirely convincing, regardless of whether the data has any grouping in it.',
     "Run k-means with k=5 on uniform random noise. You get five tidy, roughly equal clusters and a plot you could put in a deck. Before believing a real clustering, run the same k on shuffled data — if the silhouette score is similar, you have found the algorithm's behaviour rather than your data's."),
    ("related", ["vector-search-algorithms", "embeddings-and-retrieval", "what-a-plot-is-for", "confusion-matrix-and-metrics"]),
    ("links", [
      ("Clustering (scikit-learn)", "https://scikit-learn.org/stable/modules/clustering.html",
       "k-means alongside DBSCAN and hierarchical clustering, with a comparison chart of what each finds."),
      ("Nearest neighbours (scikit-learn)", "https://scikit-learn.org/stable/modules/neighbors.html",
       "k-NN, distance metrics, and the tree structures that make it tractable."),
    ]),

    ("quiz", [
      ("You run k-means on customer data with income in pounds and age in years, without scaling. What happens?",
       ["The algorithm refuses to run",
        "Income dominates every distance calculation, so clusters are effectively grouped by income alone",
        "Age is ignored entirely because it has fewer digits"], 1),
      ("Why is RAG retrieval essentially k-NN?",
       ["Both use decision trees internally",
        "Both find the k most similar stored examples and use them — over embeddings instead of tabular features",
        "Both require choosing k in advance and clustering the data"], 1),
      ("What does the curse of dimensionality do to nearest-neighbour search?",
       ["It makes it slower to compute",
        "Nearest and farthest distances converge, so 'closest' carries less information",
        "It causes numeric overflow in distance calculations"], 1),
    ]),
  ],
},
{
  "slug": "attention-and-transformers",
  "title": "Attention and the Transformer",
  "subtitle": "The algorithm every model in this program is built from.",
  "body": [
    ("p", "Every LLM you use is a transformer, and the transformer's central mechanism is <strong>attention</strong>. You don't need the matrix algebra to work effectively with these models, but you do need the shape of the idea — because it explains context limits, cost curves, and why the KV cache exists."),

    ("h2", "The problem attention solves"),
    ("p", "To predict the next word in \"The turbine that the engineers inspected last week finally ___\", the model must connect \"turbine\" to \"finally\" across ten intervening words. Earlier architectures processed text in order and carried a running summary, which meant long-range connections faded. Attention lets every position look directly at every other position, at any distance, in one step."),

    ("h2", "Query, key, value"),
    ("p", "Each token produces three vectors. The <strong>query</strong> is what this token is looking for. The <strong>key</strong> is what each token offers. The <strong>value</strong> is the content it contributes. Compare one token's query against every key, turn the resulting scores into weights, and take a weighted sum of the values."),
    ("p", "That's it: each token's new representation is a blend of all tokens, weighted by relevance. Stack this operation dozens of times, with several independent attention \"heads\" per layer learning different relationships, and you have a transformer."),

    ("figure", "Every token attends to every other token. That all-to-all comparison is what gives transformers their long-range reach — and why cost grows with the square of sequence length.", '''<svg viewBox="0 0 640 200" role="img" aria-label="All-to-all attention and its quadratic cost">
<text x="12" y="18" class="d-accent">each token looks at every token</text>
<g class="d-label-sm">
<rect x="40" y="34" width="72" height="26" rx="4" class="d-box"/><text x="60" y="52">The</text>
<rect x="130" y="34" width="72" height="26" rx="4" class="d-box-accent"/><text x="142" y="52">turbine</text>
<rect x="220" y="34" width="72" height="26" rx="4" class="d-box"/><text x="238" y="52">that</text>
<rect x="310" y="34" width="72" height="26" rx="4" class="d-box"/><text x="330" y="52">was</text>
<rect x="400" y="34" width="72" height="26" rx="4" class="d-box-accent"/><text x="416" y="52">finally</text>
</g>
<path d="M436 34 Q300 0 166 34" stroke="var(--accent)" stroke-width="2" fill="none"/>
<path d="M430 60 Q380 88 346 60" class="d-arrow"/>
<path d="M424 60 Q340 96 256 60" class="d-arrow"/>
<path d="M418 60 Q250 104 76 60" class="d-arrow"/>
<text x="196" y="18" class="d-accent">strongest link, ten words apart</text>
<line x1="12" y1="120" x2="628" y2="120" stroke="var(--border)"/>
<text x="12" y="144" class="d-label-sm">n tokens → n × n comparisons. Double the context and attention cost quadruples.</text>
<text x="12" y="164" class="d-label-sm">This is why the KV cache exists, and why very long context eventually stops being affordable.</text>
</svg>'''),

    ("p", "Two details in that description have names worth having. The scores are turned into weights by a <strong>softmax</strong>, which forces them to be positive and to sum to one &mdash; so attention is always distributing a fixed budget of attention rather than adding more of it. And before the softmax the scores are divided by the square root of the key dimension, which is why the operation is properly called <strong>scaled dot-product attention</strong>. Without that division the scores grow with dimension, the softmax saturates, and gradients vanish; it is a small correction that the whole thing depends on."),

    ("figure", "One token's query scored against every key, softmaxed into weights, and used to take a weighted sum of the values.", '''<svg viewBox="0 0 560 186" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A query is scored against three keys, the scores are softmaxed into weights, and the values are combined in proportion.">
<rect x="10" y="16" width="72" height="28" rx="5" class="d-box-accent"/><text x="46" y="35" class="d-label" text-anchor="middle">query</text>
<text x="10" y="62" class="d-label-sm">from the token doing the looking</text>
<rect x="120" y="76" width="60" height="24" rx="4" class="d-box"/><text x="150" y="92" class="d-label-sm" text-anchor="middle">key 1</text>
<rect x="120" y="104" width="60" height="24" rx="4" class="d-box"/><text x="150" y="120" class="d-label-sm" text-anchor="middle">key 2</text>
<rect x="120" y="132" width="60" height="24" rx="4" class="d-box"/><text x="150" y="148" class="d-label-sm" text-anchor="middle">key 3</text>
<path d="M60 44 L140 72" class="d-arrow"/>
<text x="196" y="70" class="d-label-sm">score</text>
<text x="200" y="92" class="d-label-sm">8.2</text>
<text x="200" y="120" class="d-label-sm">1.1</text>
<text x="200" y="148" class="d-label-sm">0.7</text>
<path d="M226 112 L262 112" class="d-arrow"/>
<text x="268" y="70" class="d-label-sm">&#247; &#8730;d, softmax</text>
<text x="272" y="92" class="d-label-sm">0.79</text>
<text x="272" y="120" class="d-label-sm">0.13</text>
<text x="272" y="148" class="d-label-sm">0.08</text>
<text x="268" y="166" class="d-label-sm">sums to 1</text>
<path d="M320 112 L356 112" class="d-arrow"/>
<rect x="360" y="76" width="60" height="24" rx="4" class="d-box"/><text x="390" y="92" class="d-label-sm" text-anchor="middle">value 1</text>
<rect x="360" y="104" width="60" height="24" rx="4" class="d-box"/><text x="390" y="120" class="d-label-sm" text-anchor="middle">value 2</text>
<rect x="360" y="132" width="60" height="24" rx="4" class="d-box"/><text x="390" y="148" class="d-label-sm" text-anchor="middle">value 3</text>
<path d="M424 112 L460 112" class="d-arrow"/>
<rect x="464" y="94" width="86" height="36" rx="5" class="d-box-good"/>
<text x="507" y="117" class="d-label" text-anchor="middle">output</text>
<text x="464" y="150" class="d-label-sm">mostly value 1</text>
</svg>'''),

    ("h2", "What follows from the algorithm"),
    ("ul", [
      "<strong>Quadratic cost, in attention specifically.</strong> n tokens means n² comparisons, so doubling the context quadruples the <em>attention</em> work. Be careful carrying that to the whole model: attention is one part of a forward pass, the projections and feed-forward layers are linear in context, and the squared term does not overtake them until the context approaches the model’s hidden dimension. Block 3 measures this and finds prefill close to linear at retrieval-sized contexts.",
      "<strong>Position must be added.</strong> Attention is order-blind by construction, so position information is injected separately (rotary embeddings, in most current models). Extending context beyond training length is largely a positional-encoding problem.",
      "<strong>The KV cache is a direct consequence.</strong> Keys and values for previous tokens don't change as generation proceeds, so they're cached rather than recomputed. Lesson 2 of the vocabulary set, arriving from the other direction.",
      "<strong>Parallel training.</strong> Unlike sequential architectures, all positions are processed at once during training. This is why transformers scaled and their predecessors didn't.",
    ]),
    ("callout", "insight", "Why 'attention' is a fair name", "The weights are interpretable in a limited way — you can see which earlier tokens most influenced a prediction. Treat that as a debugging aid rather than an explanation; attention weights show where information flowed, not why the model concluded what it did."),

    ("h2", "What multiple heads are for"),
    ("p", "One attention operation produces one weighted blend. A layer runs several in parallel — typically eight to a hundred and twenty-eight — each with its own learned projections, and concatenates the results."),
    ("p", "The reason is that a token relates to its context in more than one way at once. \"Turbine\" needs to connect to the verb that governs it, the adjective describing it, and the earlier mention it refers back to. One set of attention weights has to compromise across all three; several sets can specialise. Interpretability work has found heads that appear to track syntactic dependencies and heads that track coreference, though attributing clean single functions to heads is less reliable than early results suggested."),

    ("h2", "The variants you will meet by name"),
    ("terms", [
      ("Multi-head attention (MHA)", "The original", "Every head has its own keys and values. Most expressive, largest KV cache."),
      ("Multi-query attention (MQA)", "One set of keys and values for all heads", "The far end of the same idea: every query head shares a single key-value head. Smallest possible cache, and it gives up more quality than the compromise below, which is why it is the less common of the two."),
            ("Grouped-query attention (GQA)", "The current default", "Heads share key and value projections in groups. Cuts the KV cache substantially with little quality loss, which is why nearly every recent open model uses it."),
      ("Sliding window", "Bounded context per layer", "Each token attends only to a nearby span, making cost linear rather than quadratic. Information still travels further by passing up through layers."),
      ("Causal masking", "Not a variant, a requirement", "During generation a token must not see the future, so the upper triangle of the attention matrix is masked out. This is what makes the model autoregressive."),
    ]),
    ("callout", "insight", "GQA is why long context got affordable", "The KV cache scales with the number of key-value heads, not query heads. Sharing them across groups cuts cache memory by a large factor — often four to eight times — with quality differences small enough to be hard to measure. That single architectural change did more for practical long-context serving than any increase in window size, and it is invisible from the outside."),

    ("h2", "FlashAttention, and why it is not on that list"),
    ("p", "Everything above changes <em>what</em> attention computes. FlashAttention changes only <em>how</em>, and it is the single most consequential attention result of recent years for anyone actually running a model."),
    ("p", "The observation is the one the hardware lesson makes about the whole machine, applied here: the arithmetic was never the bottleneck, the memory traffic was. Standard attention builds the full n-by-n score matrix in the accelerator&#39;s main memory, writes it, reads it back for the softmax, writes it again, reads it once more for the weighted sum. For a long sequence that matrix is enormous and every one of those trips crosses the slow gap. FlashAttention never materialises it: it works in tiles small enough to stay in fast on-chip memory, keeps a running softmax as it goes, and recomputes what it needs during the backward pass rather than storing it."),

    ("know",
     "FlashAttention is exact. It computes the same numbers as standard attention, and the speed comes entirely from moving fewer bytes.",
     "This is what separates it from every other entry in the variants list. Grouped-query attention, sliding windows and sparse patterns all change the function being computed and therefore trade quality for cost, which means they need evaluating. FlashAttention returns the same result and needs no quality re-check &mdash; the paper&#39;s title says <em>exact</em> for exactly this reason. It is a rearrangement of the memory access pattern, not an approximation, which is why it was adopted everywhere almost immediately and why you are already using it without having chosen it.",
     "Dao and colleagues report a 3&times; end-to-end speedup on GPT-2 and 15 per cent on BERT-large, with no change to the model or its outputs. The gain is entirely in not writing an intermediate matrix to slow memory and reading it back twice."),

    ("callout", "matters", "The pattern to carry away from this",
     "<p>Three times faster, no quality cost, no change to what the model computes &mdash; from noticing that the expensive part was data movement rather than arithmetic. That is the same finding as the memory-bound decode, the same finding as prefix caching, and the same finding behind quantization helping more than pruning. When something is slower than the arithmetic suggests it should be, the answer is nearly always bytes crossing a gap, and the fix is nearly always to move fewer of them rather than to compute less.</p>"),

    ("h2", "Self-attention, cross-attention, and where the queries come from"),
    ("p", "Everything so far has tokens attending to other tokens in the same sequence, which is <strong>self-attention</strong>. The machinery does not require that. In <strong>cross-attention</strong> the queries come from one sequence and the keys and values from another, which is how one representation reads from a different one &mdash; a decoder attending to an encoder&#39;s output in translation, or a language model attending to the output of an image encoder in a vision-language model. The arithmetic is identical; only the source of the three vectors changes. It is worth knowing because it is the join between modalities: when a model &ldquo;sees&rdquo; an image, cross-attention is frequently the mechanism by which the text side reads the vision side."),

    ("h2", "The alternatives, so the transformer does not look inevitable"),
    ("p", "Attention won decisively and the search did not stop. <strong>Linear attention</strong> approximates the softmax so the computation can be reordered into something linear in sequence length rather than quadratic, trading exactness for scaling. <strong>State-space models</strong> take a different route entirely, carrying a fixed-size recurrent state like the architectures attention displaced, but designed so training still parallelises &mdash; which was the thing the old recurrent models could not do. Several current systems are hybrids, interleaving a few full-attention layers among cheaper ones, on the reasoning that you need exact long-range lookup occasionally rather than at every layer. None of this changes what you should learn first; it is here so that a name you meet reads as a live alternative rather than a mystery."),

    ("books", [
      ("Hands-On Large Language Models", "Alammar & Grootendorst",
       "By the author of the Illustrated Transformer. The visual explanations are the best available, and the code makes them concrete."),
    ]),
    ("related", ["inside-an-llm", "tokens-context-and-kv-cache", "why-the-gpu-is-waiting", "mixture-of-experts"]),
    ("links", [
      ('FlashAttention (Dao et al., 2022)', 'https://arxiv.org/abs/2205.14135',
       'Exact attention made fast by moving fewer bytes — the memory-bandwidth argument applied to the attention kernel itself.'),
      ("Attention Is All You Need (Vaswani et al., 2017)", "https://arxiv.org/abs/1706.03762",
       "The original paper. Section 3.2 is the mechanism; the rest is scaffolding."),
      ("The Illustrated Transformer", "https://jalammar.github.io/illustrated-transformer/",
       "The clearest visual walkthrough available, and the one most people learn from."),
      ("Build a Large Language Model (From Scratch)", "https://github.com/rasbt/LLMs-from-scratch",
       "You have this repo locally — ch03 implements attention line by line in PyTorch."),
    ]),

    ("quiz", [
      ("Why does doubling the context length more than double the cost of attention?",
       ["Longer sequences need more layers",
        "Every token is compared with every other, so n tokens means n² comparisons",
        "The KV cache has to be rebuilt from scratch"], 1),
      ("Why do transformers need positional encoding added separately?",
       ["To compress the input",
        "Attention compares all positions equally and is inherently order-blind",
        "To keep the vocabulary size manageable"], 1),
      ("What can attention weights legitimately tell you?",
       ["Why the model reached its conclusion",
        "Where information flowed — useful for debugging, not a full explanation",
        "How confident the model is in its answer"], 1),
    ]),
  ],
},
{
  "slug": "mixture-of-experts",
  "title": "Mixture of Experts",
  "subtitle": "How a model gets larger without getting slower — and why that trade lands badly on the machine under your desk.",
  "body": [
    ("p", "The previous lesson built the transformer block: attention, then a feed-forward network applied to every position. Scaling that block means making both parts bigger, and the cost of running it rises in step. Mixture of experts breaks that link. It keeps the parameter count large and activates only a fraction of it per token, so capacity grows without compute growing with it."),

    ("h2", "What actually changes"),
    ("p", "Attention is untouched. The change is confined to the feed-forward part of each block, which is replaced by several smaller feed-forward networks — the experts — and a router that decides which of them a given token goes through."),

    ("terms", [
      ("Experts", "Several small feed-forward networks in place of one large one",
       "Each is an ordinary feed-forward network. There is no specialisation designed in: what each expert becomes good at emerges during training and is generally not interpretable."),
      ("Router", "A classifier over experts, trained with the network",
       "It produces a score for every expert and the top K are selected. It is learned rather than configured, which means routing quality is a property the model can get wrong."),
      ("Per token, per layer", "The choice is made again everywhere",
       "Different tokens in the same sentence take different experts, and the same token takes different experts at each layer. A sequence does not travel one path through the model."),
      ("Active versus total parameters", "The number that gets quoted is not the number you load",
       "A model described as eight experts of seven billion holds roughly forty-seven billion parameters and activates around thirteen billion per token. Both figures are real and they answer different questions."),
    ]),

    ("figure", "Only the feed-forward half of the block changes. The router picks a few experts per token, so the arithmetic per token falls while every expert still has to be resident in memory.", '''<svg viewBox="0 0 640 236" role="img" aria-label="A transformer block beside a mixture-of-experts block"><defs><marker id="moe" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" class="d-fill-accent"/></marker></defs>
<text x="14" y="18" class="d-label-b">Transformer block</text>
<rect x="14" y="28" width="240" height="34" rx="6" class="d-box"/><text x="26" y="50" class="d-label-sm">attention</text>
<path d="M134 62 L134 82" class="d-arrow-accent" marker-end="url(#moe)"/>
<rect x="14" y="82" width="240" height="44" rx="6" class="d-box"/><text x="26" y="102" class="d-label-sm">one large feed-forward network</text><text x="26" y="118" class="d-label-sm">every token goes through all of it</text>
<text x="330" y="18" class="d-label-b">Mixture-of-experts block</text>
<rect x="330" y="28" width="296" height="34" rx="6" class="d-box"/><text x="342" y="50" class="d-label-sm">attention — unchanged</text>
<path d="M478 62 L478 78" class="d-arrow-accent" marker-end="url(#moe)"/>
<rect x="330" y="78" width="296" height="26" rx="6" class="d-box-accent"/><text x="342" y="96" class="d-label-sm">router — scores every expert, keeps top K</text>
<rect x="330" y="112" width="66" height="40" rx="5" class="d-box-accent"/><text x="342" y="136" class="d-label-sm">E1</text>
<rect x="404" y="112" width="66" height="40" rx="5" class="d-box"/><text x="416" y="136" class="d-label-sm">E2</text>
<rect x="478" y="112" width="66" height="40" rx="5" class="d-box-accent"/><text x="490" y="136" class="d-label-sm">E3</text>
<rect x="552" y="112" width="66" height="40" rx="5" class="d-box"/><text x="564" y="136" class="d-label-sm">E4</text>
<text x="330" y="172" class="d-label-sm">shaded = active for this token. All four are resident in memory.</text>
<text x="14" y="204" class="d-label-sm">Arithmetic per token falls with the number of experts you skip.</text>
<text x="14" y="222" class="d-label-sm">Bytes held does not fall at all — which is the half that decides decode speed.</text>
</svg>'''),

    ("h2", "Two things that go wrong in training"),
    ("p", "A learned router creates a feedback loop, and both of its failure modes are worth knowing because the fixes look arbitrary until you have seen the problem."),

    ("terms", [
      ("The rich get richer", "One expert wins early and keeps winning",
       "At the start every expert is equally poor, so the first choice is effectively random. The chosen expert improves, which makes it more likely to be chosen, which improves it further. Left alone, a handful of experts absorb the training and the rest stay undertrained."),
      ("Noise and masking", "The fix for it",
       "Noise is added to the router's scores so other experts occasionally win, and everything outside the top K is set to negative infinity before the softmax so it contributes nothing. Together they keep the field open long enough for the others to learn."),
      ("Load imbalance", "Some experts see far more tokens than others",
       "A different problem with the same symptom. The fix is a capacity limit: an expert that has taken its quota of tokens refuses more, and the overflow goes to the next best choice."),
    ]),

    ("know",
     "A mixture of experts lowers arithmetic per token and does not lower bytes held — which is the wrong half for generation.",
     "Generating a token is already memory-bound: the hardware spends the step waiting on weights rather than doing arithmetic. Skipping experts removes arithmetic that was not the constraint, while every expert still has to be resident because the router might select it for the next token. Work per byte therefore goes <em>down</em>, which is the opposite of what a memory-bound workload wants. The saving is real, but it lands on the cost you were not paying.",
     "This is why a mixture-of-experts model can be uncomfortable to run locally despite an activated-parameter count that sounds small. You buy memory for the total and you get the speed of the active fraction, and on a machine chosen for its memory ceiling the total is the number that decides whether it runs at all."),

    ("callout", "matters", "Read both parameter counts, and know which question each answers",
     "<p>Total parameters tell you whether the model fits. Active parameters tell you roughly how fast a token will be. A specification quoting only one of them is answering only half of the question you have, and the half usually quoted is the flattering one.</p>"),

    ("callout", "pitfall", "Serving one is a routing problem, not just a bigger model",
     "<p>At scale the experts are split across devices while attention is replicated, so each device holds only some experts. The router then decides not merely which expert but effectively which machine a token is sent to, and that flow changes token by token. This is why mixture-of-experts models depend on a capable inference engine rather than running acceptably on a naive one.</p>"),

    ("h2", "Where it sits against the other levers"),
    ("p", "This course has now met three ways of making a large model cheaper to run, and they act on different quantities. Grouped-query attention shrinks the key-value cache, which is bytes. Quantization shrinks the weights, which is also bytes. A mixture of experts shrinks the arithmetic per token and leaves the bytes alone. Only the first two help a memory-bound decode directly; the third buys capacity at fixed compute, which is a training and quality argument more than a serving one."),
    ("related", ["attention-and-transformers", "the-four-ways-to-shrink-a-model", "local-hardware-limits", "why-the-gpu-is-waiting"]),
    ("quiz", [
      ("What part of a transformer block does a mixture of experts replace?",
       ["The attention mechanism, which is split across experts",
        "The feed-forward network, which becomes several smaller networks plus a router that selects among them",
        "The residual connections between layers"],
       1),
      ("A model is described as eight experts of seven billion parameters. What must you hold in memory?",
       ["Roughly seven billion, since only one expert runs at a time",
        "Roughly forty-seven billion — every expert has to be resident because the router may select any of them for the next token",
        "Roughly thirteen billion, the activated count"],
       1),
      ("Why does skipping experts help less than it appears during generation?",
       ["Routing overhead cancels most of the saving",
        "Generation is memory-bound, so it removes arithmetic that was not the constraint while the bytes that were the constraint still have to be loaded",
        "The experts are too small for the saving to matter"],
       1),
    ]),
  ],
},
{
  "slug": "vector-search-algorithms",
  "title": "Nearest-Neighbour Search at Scale",
  "subtitle": "Exact search, HNSW, and the recall you quietly trade away for speed.",
  "body": [
    ("p", "The previous lesson on k-NN described finding the nearest vectors. Doing that across ten million embeddings, in under fifty milliseconds, is a different problem — and the algorithm you choose has a failure mode most people never measure."),

    ("h2", "Exact search, and when it's fine"),
    ("p", "Compare the query against every stored vector and keep the best matches. It's exhaustive, perfectly accurate, and linear in the number of vectors. For under roughly 100,000 vectors this is genuinely fine on modern hardware — often single-digit milliseconds."),
    ("callout", "matters", "Don't optimise this early", "Most retrieval-augmented generation (RAG) corpora are far smaller than people assume. A few thousand documents chunked into tens of thousands of vectors is comfortably exact-search territory. Reach for approximate indexing when you've measured that you need it, not because the tutorial used it."),

    ("h2", "Approximate nearest neighbour"),
    ("p", "Above that scale, <strong>ANN</strong> algorithms trade a small amount of accuracy for a large amount of speed. They don't guarantee finding the true nearest neighbours — they find <em>most</em> of them, most of the time."),
    ("terms", [
      ("HNSW", "Hierarchical navigable small world", "A layered graph. Search starts in a sparse top layer that covers ground quickly, then descends into denser layers to refine. The dominant choice — fast and accurate, at the cost of memory."),
      ("IVF", "Inverted file index", "Cluster the vectors, then search only the nearest few clusters. Lower memory, and misses anything sitting just outside a searched cluster."),
      ("Product quantization", "Compress the vectors themselves", "Often paired with IVF to cut memory dramatically. Quantization again — same trade, different object."),
    ]),

    ("figure", "HNSW navigates a layered graph: coarse hops at the top cover distance fast, finer layers refine. Speed comes from never examining most of the data — which is also where recall is lost.", '''<svg viewBox="0 0 640 200" role="img" aria-label="HNSW layered graph search">
<text x="12" y="18" class="d-label-sm">layer 2 — sparse, long hops</text>
<circle cx="120" cy="36" r="5" class="d-fill-accent"/><circle cx="330" cy="30" r="5" class="d-fill-muted"/><circle cx="520" cy="38" r="5" class="d-fill-muted"/>
<line x1="120" y1="36" x2="330" y2="30" class="d-arrow"/><line x1="330" y1="30" x2="520" y2="38" class="d-arrow"/>
<text x="12" y="86" class="d-label-sm">layer 1 — denser</text>
<circle cx="120" cy="104" r="4.5" class="d-fill-muted"/><circle cx="230" cy="110" r="4.5" class="d-fill-muted"/>
<circle cx="330" cy="98" r="4.5" class="d-fill-accent"/><circle cx="430" cy="112" r="4.5" class="d-fill-muted"/>
<circle cx="520" cy="104" r="4.5" class="d-fill-muted"/>
<line x1="120" y1="104" x2="230" y2="110" class="d-arrow"/><line x1="230" y1="110" x2="330" y2="98" class="d-arrow"/>
<line x1="330" y1="98" x2="430" y2="112" class="d-arrow"/><line x1="430" y1="112" x2="520" y2="104" class="d-arrow"/>
<text x="12" y="150" class="d-label-sm">layer 0 — every vector</text>
<g class="d-fill-muted">
<circle cx="80" cy="172" r="3.5"/><circle cx="140" cy="176" r="3.5"/><circle cx="200" cy="170" r="3.5"/>
<circle cx="260" cy="178" r="3.5"/><circle cx="320" cy="172" r="3.5"/><circle cx="440" cy="176" r="3.5"/>
<circle cx="500" cy="170" r="3.5"/><circle cx="560" cy="178" r="3.5"/>
</g>
<circle cx="380" cy="174" r="5" class="d-fill-green"/>
<text x="392" y="164" class="d-fill-green" font-size="11" font-weight="600">answer</text>
<path d="M120 44 L120 96" class="d-arrow-accent"/><path d="M330 106 L376 166" class="d-arrow-accent"/>
</svg>'''),

    ("h2", "The number nobody measures"),
    ("p", "<strong>Recall@k</strong> is the fraction of true nearest neighbours your index actually returned. An HNSW index at 95% recall silently misses one in twenty of the results it should have found — and because the results it does return look perfectly reasonable, nothing appears broken."),
    ("callout", "pitfall", "How this fails in production", "RAG quality drops and everyone investigates the prompt, the chunking, the model. The actual cause is an index tuned for speed that never retrieves the right chunk in the first place. Measure recall against exact search on a sample before blaming anything downstream — it takes an hour and rules out an entire category of problem."),
    ("p", "The tuning knobs trade directly: HNSW's <code>ef_search</code> and <code>M</code> raise recall and cost latency and memory. There is no setting that gives you both."),

    ("h2", "The two knobs, and what each costs"),
    ("terms", [
      ("M", "Connections per node, set at build time", "Higher means a denser graph: better recall, more memory, slower to build. Changing it means rebuilding the index."),
      ("ef_construction", "Effort spent while building", "Higher builds a better graph, once, for a longer build. Cheap to be generous with — you pay it only at index time."),
      ("ef_search", "Candidates examined per query", "The one you tune live. Raise it for recall, pay in latency. This is the dial to move first when recall is low."),
    ]),
    ("callout", "matters", "Tune ef_search before rebuilding anything", "Low recall is far more often an ef_search that was left at a library default than a fundamentally wrong index. It costs nothing to raise, takes effect immediately, and its cost is latency you can measure. Only rebuild with a larger M when you have established that ef_search alone cannot reach the recall you need."),

    ("h2", "Measuring recall, in about an hour"),
    ("p", "Take a sample of real queries — two hundred is plenty. Run each through exact search over the full set and keep the true top-k. Run each through your index. Recall@k is the mean overlap. That number is the honest description of your retrieval layer, and almost nobody computes it."),
    ("p", "Do this once at build time and re-run it on a schedule, because recall degrades as a corpus grows and shifts. An index tuned when you had 50,000 documents is not necessarily the same index at 500,000."),

    ("h2", "The other reason to keep vectors in Postgres"),
    ("p", "Specialist vector databases are faster at pure vector search. What they are not good at is the query you actually write, which almost always has a filter attached — this customer, this date range, this document type. Filtered vector search is genuinely hard: filter first and you may search too few candidates to find good neighbours; search first and you may filter away everything you found."),
    ("callout", "insight", "Filtering is where the real engineering is", "A database that already holds your relational data can combine a vector search with a SQL predicate in one planner. Two separate stores means doing that join yourself, in application code, badly. At the scale most teams operate, one database that does both adequately beats two that each do half the job well."),

    ("books", [
      ("Mining of Massive Datasets", "Leskovec, Rajaraman & Ullman",
       "Chapter 3 on locality-sensitive hashing is the theoretical ancestor of everything in this lesson. Free online, and worth it for the intuition about why approximate methods work at all."),
    ]),
    ("related", ["embeddings-and-retrieval", "ranking-and-hybrid-retrieval", "measuring-retrieval", "clustering-and-knn"]),
    ("links", [
      ("pgvector indexing", "https://github.com/pgvector/pgvector",
       "HNSW and IVFFlat in Postgres, with the parameters and their recall implications."),
      ("Efficient and robust ANN search using HNSW (Malkov & Yashunin)", "https://arxiv.org/abs/1603.09320",
       "The HNSW paper. The layered-graph intuition is in the first few pages."),
    ]),

    ("quiz", [
      ("You have 40,000 vectors. What should you use?",
       ["HNSW, since it's the industry standard",
        "Exact search — at this scale it's fast enough and perfectly accurate",
        "IVF with product quantization to save memory"], 1),
      ("What does 'recall@10 = 0.95' mean for an ANN index?",
       ["95% of returned results are relevant to the user",
        "The index returns 95% of the true nearest neighbours it should have found",
        "The index is 95% as fast as exact search"], 1),
      ("RAG answers have got worse and the prompt hasn't changed. What should you rule out first?",
       ["The embedding model has drifted",
        "Index recall — measure against exact search before investigating anything downstream",
        "The LLM provider changed the model version"], 1),
    ]),
  ],
},
{
  "slug": "ranking-and-hybrid-retrieval",
  "title": "Ranking and Hybrid Retrieval",
  "subtitle": "Best Matching 25 (BM25), reciprocal rank fusion and rerankers — why pure vector search is rarely the best answer.",
  "body": [
    ("p", "The context-engineering lesson concluded that ranking matters more than recall — that getting the right chunk into the first position beats retrieving more chunks. This lesson is the algorithms that do the ranking."),

    ("h2", "BM25: keyword search, done properly"),
    ("p", "<strong>BM25</strong> scores a document against a query using term frequency, adjusted two ways: rare terms count for more than common ones, and repeated occurrences give diminishing returns. It's decades old, needs no training, no GPU and no embedding model, and it is a genuinely strong baseline."),
    ("callout", "matters", "Where BM25 beats embeddings outright", "Exact identifiers, error codes, product SKUs, function names, file paths, proper nouns, and any rare term. Embeddings compress meaning and lose precise tokens; BM25 matches them exactly. For a technical corpus this is not a small difference — it is frequently the difference between finding the answer and not."),

    ("h2", "Why hybrid wins"),
    ("p", "Vector search finds paraphrases and misses exact terms. BM25 finds exact terms and misses paraphrases. Their failures are largely independent, which is precisely the condition under which combining two methods helps — the same logic as ensembles in lesson 4."),

    ("h2", "Reciprocal rank fusion"),
    ("p", "The problem with combining them is that a BM25 score of 14.2 and a cosine similarity of 0.83 aren't comparable quantities. <strong>Reciprocal rank fusion</strong> sidesteps this entirely by ignoring the scores and using only the ranks: each document scores the sum of <code>1 / (k + rank)</code> across the lists it appears in, with k typically 60."),
    ("p", "A document ranked highly by both methods rises to the top; one ranked highly by a single method still places well. No score normalisation, no tuning, no training. It's a two-line algorithm that reliably outperforms either input list."),

    ("figure", "Two independent rankings fused by position rather than score. The document both methods liked wins, without ever comparing incomparable numbers.", '''<svg viewBox="0 0 640 200" role="img" aria-label="Reciprocal rank fusion of two result lists">
<text x="20" y="18" class="d-accent">BM25</text>
<rect x="20" y="28" width="150" height="24" rx="4" class="d-box"/><text x="32" y="45" class="d-label-sm">1. doc-C</text>
<rect x="20" y="58" width="150" height="24" rx="4" class="d-box"/><text x="32" y="75" class="d-label-sm">2. doc-A</text>
<rect x="20" y="88" width="150" height="24" rx="4" class="d-box"/><text x="32" y="105" class="d-label-sm">3. doc-F</text>
<text x="230" y="18" class="d-accent">Vector</text>
<rect x="230" y="28" width="150" height="24" rx="4" class="d-box"/><text x="242" y="45" class="d-label-sm">1. doc-B</text>
<rect x="230" y="58" width="150" height="24" rx="4" class="d-box"/><text x="242" y="75" class="d-label-sm">2. doc-C</text>
<rect x="230" y="88" width="150" height="24" rx="4" class="d-box"/><text x="242" y="105" class="d-label-sm">3. doc-A</text>
<text x="440" y="18" class="d-fill-green" font-size="12" font-weight="600">Fused</text>
<rect x="440" y="28" width="170" height="24" rx="4" class="d-box-good"/><text x="452" y="45" class="d-label-sm">1. doc-C  (1/61 + 1/62)</text>
<rect x="440" y="58" width="170" height="24" rx="4" class="d-box"/><text x="452" y="75" class="d-label-sm">2. doc-A  (1/62 + 1/63)</text>
<rect x="440" y="88" width="170" height="24" rx="4" class="d-box"/><text x="452" y="105" class="d-label-sm">3. doc-B  (1/61)</text>
<text x="20" y="146" class="d-label-sm">score(d) = Σ 1 / (k + rank), k = 60. Only positions are used, so incomparable scores never need normalising.</text>
<text x="20" y="168" class="d-label-sm">doc-C placed well in both lists and wins. doc-B was first in one list and still ranks.</text>
</svg>'''),

    ("h2", "Rerankers: the expensive final pass"),
    ("p", "Retrieval embeds queries and documents separately, so it can never see them together. A <strong>cross-encoder reranker</strong> does — it takes the query and one document as a single input and scores their relevance directly. Far more accurate, and far too slow to run over a whole corpus."),
    ("p", "So the standard architecture is a funnel: retrieve 100 candidates cheaply with hybrid search, rerank those 100 properly, keep the top 5 for the model. You get cross-encoder quality at nearly bi-encoder cost, and the top-of-list precision that context engineering demands."),

    ("h2", "The pipeline worth defaulting to"),
    ("terms", [
      ("1. Retrieve wide", "BM25 + vector, ~50 each", "Independent failure modes, so coverage is better than either alone."),
      ("2. Fuse", "Reciprocal rank fusion", "Two lines of code, no tuning, no normalisation."),
      ("3. Rerank", "Cross-encoder over ~100", "The accuracy step. Only affordable because the candidate set is small."),
      ("4. Truncate", "Top 3–5 into context", "Precision beats volume — distractors actively cost you."),
    ]),

    ("h2", "What BM25 is actually computing"),
    ("p", "Three ideas, each fixing a flaw in the one before it."),
    ("terms", [
      ("Term frequency", "A word appearing often signals relevance", "But not linearly. Ten mentions is not ten times more relevant than one, so BM25 saturates — the fifth occurrence adds far less than the second."),
      ("Inverse document frequency", "Rare words carry more information", "A document matching \"gearbox\" tells you much more than one matching \"the\". Weight each term by how rare it is across the corpus."),
      ("Length normalisation", "Long documents match everything", "A 50-page manual contains most words by accident. Divide the benefit by length, tuned so that being long is penalised but not fatal."),
    ]),
    ("callout", "insight", "Saturation is the part people miss", "Plain term-frequency scoring can be gamed by repetition, and worse, it genuinely misranks — a short document that says \"gearbox\" once is often more relevant than a long one that says it fifteen times in passing. BM25's saturation curve is a small piece of mathematics that encodes a real judgement about how language works, and it is most of why a 1990s algorithm still competes with embeddings."),

    ("h2", "Chunking, which decides more than your retriever does"),
    ("p", "Every retrieval method here operates on chunks you chose. Choose them badly and no amount of ranking recovers."),
    ("ul", [
      "<strong>Too small</strong> and a chunk lacks the context to be understood — a paragraph referring to \"this threshold\" with the threshold defined two chunks earlier.",
      "<strong>Too large</strong> and the embedding averages several topics into a vector that represents none of them well, while burning context when retrieved.",
      "<strong>Split on structure, not on character count.</strong> Headings, sections, function boundaries. A chunk that ends mid-sentence embeds badly and reads worse.",
      "<strong>Overlap a little</strong> so a passage spanning a boundary is not lost by both chunks.",
      "<strong>Keep the parent reference.</strong> Retrieve the chunk, then optionally expand to its section for context — small to match, larger to read.",
    ]),
    ("callout", "pitfall", "Look at your chunks before tuning anything downstream", "Print twenty at random and read them. If you cannot tell what a chunk is about without its neighbours, your retrieval will not be able to either, and every hour spent on embedding models or rerankers is spent on the wrong layer. This takes ten minutes and it is skipped almost universally."),

    ("books", [
      ("Mining of Massive Datasets", "Leskovec, Rajaraman & Ullman",
       "Chapter 5 on link analysis and ranking. Older than BM25's current use in retrieval-augmented generation (RAG) and still the clearest account of what ranking is doing."),
      ("Enterprise RAG", "Manning MEAP",
       "Chunking strategies and hybrid retrieval in a production framing, which is where this lesson's practical advice comes from."),
    ]),
    ("related", ["vector-search-algorithms", "measuring-retrieval", "building-a-rag-system", "transforming-the-query"]),
    ("links", [
      ("Reciprocal Rank Fusion (Cormack et al.)", "https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf",
       "The original paper. Short, and the algorithm is a single formula."),
      ("Cross-encoders in Sentence Transformers", "https://sbert.net/examples/applications/cross-encoder/README.html",
       "How to run the rerank step, with pretrained models you can use directly."),
    ]),

    ("quiz", [
      ("Why does BM25 often beat embeddings on a technical corpus?",
       ["It's faster, so more documents can be searched",
        "Embeddings compress meaning and lose exact tokens; BM25 matches identifiers and rare terms precisely",
        "BM25 is trained on technical documentation"], 1),
      ("What problem does reciprocal rank fusion avoid?",
       ["Having to run two retrieval systems",
        "Comparing scores from different systems that aren't on the same scale — it uses only rank positions",
        "The need for an embedding model"], 1),
      ("Why can't you just run the cross-encoder reranker over the whole corpus?",
       ["It only works on short documents",
        "It scores query and document together, so cost is one model pass per document — far too slow at corpus scale",
        "It requires the documents to be pre-embedded"], 1),
    ]),
  ],
},
{
  "slug": "data-leakage",
  "title": "Data Leakage",
  "subtitle": "The failure that produces a brilliant model and a worthless one, simultaneously.",
  "body": [
    ("p", "Your statistics course covers overfitting thoroughly. <strong>Leakage</strong> is its more dangerous cousin, and it isn't covered there. Overfitting shows up as a gap between training and validation scores — visible, diagnosable. Leakage inflates <em>both</em>, so every number looks excellent right up until production, where the model collapses."),

    ("h2", "What it is"),
    ("p", "Leakage is when information reaches the model during training that will not be available at prediction time. The model learns to use it, scores brilliantly on your held-out data — because the leak is in that data too — and then fails completely on real inputs where the information doesn't exist."),

    ("figure", "Overfitting announces itself as a gap. Leakage lifts both curves together, so the usual diagnostic shows nothing wrong.", '''<svg viewBox="0 0 640 180" role="img" aria-label="Overfitting versus leakage in validation scores">
<g>
<text x="40" y="18" class="d-label-b">Overfitting</text>
<line x1="30" y1="140" x2="270" y2="140" class="d-arrow"/>
<line x1="30" y1="140" x2="30" y2="34" class="d-arrow"/>
<path d="M40 120 Q120 70 260 48" stroke="var(--accent)" stroke-width="2.5" fill="none"/>
<text x="196" y="42" class="d-accent">train</text>
<path d="M40 124 Q120 100 260 104" stroke="var(--red)" stroke-width="2.5" fill="none"/>
<text x="192" y="122" class="d-fill-red" font-size="11" font-weight="600">validation</text>
<path d="M264 52 L264 100" stroke="var(--muted)" stroke-width="1.4" stroke-dasharray="3 3"/>
<text x="120" y="166" class="d-fill-green" font-size="11" font-weight="600">visible gap — you can see it</text>
</g>
<g>
<text x="380" y="18" class="d-label-b">Leakage</text>
<line x1="370" y1="140" x2="610" y2="140" class="d-arrow"/>
<line x1="370" y1="140" x2="370" y2="34" class="d-arrow"/>
<path d="M380 120 Q460 66 600 44" stroke="var(--accent)" stroke-width="2.5" fill="none"/>
<text x="536" y="38" class="d-accent">train</text>
<path d="M380 124 Q460 74 600 52" stroke="var(--red)" stroke-width="2.5" fill="none"/>
<text x="500" y="70" class="d-fill-red" font-size="11" font-weight="600">validation</text>
<text x="424" y="166" class="d-fill-red" font-size="11" font-weight="600">no gap — nothing looks wrong</text>
</g>
</svg>'''),

    ("know",
     'Overfitting announces itself as a gap; leakage lifts both curves together.',
     'That is what makes leakage the more dangerous of the two. The train-versus-validation gap you would normally use to spot a problem shows nothing, because the leak is present in both halves.',
     'A churn model reaches 0.99 area under the curve (AUC) and validation agrees. The feature list includes account_closed_date, populated only for customers who already churned. Every metric is excellent and the model is worthless, because at prediction time that field is empty for everyone you care about.'),
    ("h2", "The forms it takes"),
    ("terms", [
      ("Target leakage", "A feature encodes the answer", "Predicting customer churn using 'cancellation_date'. Predicting failure using 'maintenance_ticket_raised'. The feature only exists because the outcome already happened."),
      ("Train-test contamination", "The same rows in both sets", "Duplicates, near-duplicates, or the same customer appearing under two IDs. Very common in scraped or merged data."),
      ("Preprocessing leakage", "Fitting on all the data", "Scaling or imputing before splitting means your training set has seen the test set's statistics. Subtle, extremely common."),
      ("Temporal leakage", "Training on the future", "Random splits on time-ordered data let the model learn from events after the ones it predicts. Split by time instead."),
      ("Group leakage", "Related rows split apart", "Multiple readings from one turbine, or several notes on one patient, spread across train and test."),
    ]),
    ("callout", "pitfall", "The tell", "A model that seems too good — 0.99 AUC on a hard problem — is far more likely to be leaking than to be brilliant. Treat a surprisingly good result as a bug report, not a success. The intake sheet's baseline question helps here: if your baseline also scores 0.97, something is wrong with the data, not right with your modelling."),

    ("h2", "How to prevent it"),
    ("ul", [
      "<strong>Split first, always.</strong> Before any scaling, imputation, encoding or feature selection. Everything is fitted on train and merely applied to validation and test.",
      "<strong>Use a pipeline.</strong> scikit-learn's <code>Pipeline</code> enforces fit-on-train mechanically inside cross-validation. This is what it's for.",
      "<strong>Split by time when time matters.</strong> Train on the past, validate on the future — matching how the model will actually be used.",
      "<strong>Split by group, not by row.</strong> All of a turbine's readings go to one side. <code>GroupKFold</code> exists for this.",
      "<strong>Interrogate every feature.</strong> For each one ask: would I have this value, with this content, at the moment I need the prediction? That single question catches most target leakage.",
    ]),

    ("h2", "Where it reappears later"),
    ("p", "Benchmark contamination in Block 5 is leakage at industry scale — the test set was in the training data, so the score measures memory. Tuning a prompt against the same examples you evaluate on is leakage by hand. The defence never changes: keep something back that the optimiser cannot see."),

    ("h2", "Two more forms worth recognising"),
    ("terms", [
      ("Feature selection before the split", "Subtle and common", "Choosing the top 20 features by correlation with the target, using all the data, then splitting. Your feature set has already seen the test rows. Select inside the pipeline."),
      ("Tuning against the test set", "Leakage by repetition", "Every time you look at the test score and change something, a little of that set leaks into your choices. After thirty iterations it has become a validation set with a misleading name."),
    ]),

    ("h2", "How to actually catch it"),
    ("ul", [
      "<strong>Rank the features by importance and interrogate the top one.</strong> If a single feature dominates a hard problem, ask why it is so informative. That question catches most target leakage.",
      "<strong>Drop your best feature and re-run.</strong> If performance collapses to near-baseline, you have a one-feature model, and that feature deserves scrutiny.",
      "<strong>Sort by time and re-split.</strong> If a time-ordered split scores far worse than a random one, you were learning from the future.",
      "<strong>Check for duplicate and near-duplicate rows across splits.</strong> Cheap, and it catches contamination in merged or scraped data.",
      "<strong>Ask what a human would need.</strong> If a person could not make this prediction from this information at that moment, your model should not be able to either.",
    ]),
    ("callout", "matters", "The organisational version of this problem", "Leakage often enters through a column someone else created — a flag set by a downstream process, a field populated by the resolution workflow, a status updated after the fact. You cannot detect that from the data alone. Ask whoever owns the pipeline when each field is written, not just what it means. That conversation catches more leakage than any statistical check."),

    ("books", [
      ("Designing Machine Learning Systems", "Chip Huyen",
       "Chapter 4 covers leakage, train-test contamination and the sampling decisions that produce them, in a production framing rather than an academic one."),
    ]),
    ("related", ["overfitting-and-underfitting", "labels-and-holdouts", "first-fifteen-minutes", "eval-data-you-can-trust"]),
    ("links", [
      ("Common pitfalls: data leakage (scikit-learn)", "https://scikit-learn.org/stable/common_pitfalls.html",
       "The canonical treatment, with code showing the preprocessing mistake and its fix."),
      ("Pipelines (scikit-learn)", "https://scikit-learn.org/stable/modules/compose.html",
       "The mechanism that makes preprocessing leakage structurally difficult to commit."),
    ]),

    ("quiz", [
      ("Why is leakage harder to spot than overfitting?",
       ["It only appears in very large datasets",
        "It inflates training and validation scores together, so the usual train/validation gap shows nothing",
        "It only affects neural networks"], 1),
      ("You standardise your features, then split into train and test. What went wrong?",
       ["Nothing — scaling is not a model",
        "The scaler saw the test set's statistics, so information about test data leaked into training",
        "Standardising should happen after model fitting"], 1),
      ("You get 0.99 AUC on a hard churn problem, first attempt. What's the right reaction?",
       ["Ship it — the features must be unusually informative",
        "Suspect leakage and audit every feature for whether it exists at prediction time",
        "Add regularisation to bring the score down"], 1),
    ]),
  ],
},
]
