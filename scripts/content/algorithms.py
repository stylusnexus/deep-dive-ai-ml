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
    ("callout", "insight", "You already know this algorithm", "RAG is k-NN. Embed the query, find the nearest stored vectors, use them. The retrieval step in Block 3 is exactly this algorithm, run over embeddings instead of tabular features — which is why the failure modes below transfer directly."),

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

    ("p", "This is why embeddings are typically a few hundred to a couple of thousand dimensions rather than tens of thousands, why dimensionality reduction (PCA, UMAP) is worth knowing, and why hybrid retrieval — combining vector similarity with keyword matching — outperforms pure vector search on many real corpora. Pure distance is a weaker signal than it looks."),

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
<text x="12" y="164" class="d-label-sm">This is why long context is expensive, why the KV cache exists, and why context windows have limits at all.</text>
</svg>'''),

    ("h2", "What follows from the algorithm"),
    ("ul", [
      "<strong>Quadratic cost.</strong> n tokens means n² comparisons. Doubling context quadruples attention work — the reason long context is priced the way it is.",
      "<strong>Position must be added.</strong> Attention is order-blind by construction, so position information is injected separately (rotary embeddings, in most current models). Extending context beyond training length is largely a positional-encoding problem.",
      "<strong>The KV cache is a direct consequence.</strong> Keys and values for previous tokens don't change as generation proceeds, so they're cached rather than recomputed. Lesson 2 of the vocabulary set, arriving from the other direction.",
      "<strong>Parallel training.</strong> Unlike sequential architectures, all positions are processed at once during training. This is why transformers scaled and their predecessors didn't.",
    ]),
    ("callout", "insight", "Why 'attention' is a fair name", "The weights are interpretable in a limited way — you can see which earlier tokens most influenced a prediction. Treat that as a debugging aid rather than an explanation; attention weights show where information flowed, not why the model concluded what it did."),

    ("links", [
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
  "slug": "vector-search-algorithms",
  "title": "Nearest-Neighbour Search at Scale",
  "subtitle": "Exact search, HNSW, and the recall you quietly trade away for speed.",
  "body": [
    ("p", "The previous lesson on k-NN described finding the nearest vectors. Doing that across ten million embeddings, in under fifty milliseconds, is a different problem — and the algorithm you choose has a failure mode most people never measure."),

    ("h2", "Exact search, and when it's fine"),
    ("p", "Compare the query against every stored vector and keep the best matches. It's exhaustive, perfectly accurate, and linear in the number of vectors. For under roughly 100,000 vectors this is genuinely fine on modern hardware — often single-digit milliseconds."),
    ("callout", "matters", "Don't optimise this early", "Most RAG corpora are far smaller than people assume. A few thousand documents chunked into tens of thousands of vectors is comfortably exact-search territory. Reach for approximate indexing when you've measured that you need it, not because the tutorial used it."),

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
  "subtitle": "BM25, reciprocal rank fusion and rerankers — why pure vector search is rarely the best answer.",
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
