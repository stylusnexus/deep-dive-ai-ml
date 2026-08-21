TITLE = "Block 1 · Python, Data and EDA"
TOPIC = "block1-data-eda"
ICON = "🔍"
DESCRIPTION = "Working with real tabular data — reading dtypes properly, judging missingness, exploring with intent, and the split-before-you-fit discipline that prevents leakage."
TAGS = ["ai", "data", "eda"]
COLOR = "green"
CREATED = "2026-08-20"
ID_BASE = "1787300000"

LESSONS = [
{
  "slug": "tabular-data-and-dtypes",
  "title": "Tabular Data and the Lies dtypes Tell",
  "subtitle": "Rows, columns, types — and why the type a column loaded as is your first diagnostic.",
  "body": [
    ("p", "Most business machine learning is tabular: rows are things, columns are facts about them. It's the least glamorous data in AI and it remains where most real value sits — which is why the original syllabus opens here too."),

    ("h2", "The dtype is a diagnostic, not a detail"),
    ("p", "When pandas loads a CSV it infers a type per column. That inference is a free test result and most people skim past it. A column you expect to be numeric arriving as <code>object</code> means pandas found something it couldn't parse and fell back to text."),
    ("p", "In the Block 1 dataset, <code>operating_hours</code> loads as <code>object</code>. The cause turns out to be thousands separators plus a stray <code>hrs</code> suffix on some rows — two different formatting problems in one column, which is exactly what happens when data is assembled from more than one system."),
    ("callout", "matters", "The habit", "Run <code>df.dtypes</code> immediately after loading, every time, and read it. Any numeric-looking column typed as <code>object</code> is a question you must answer before doing anything else. It takes ten seconds and routinely saves an afternoon."),

    ("h2", "The types you'll meet"),
    ("terms", [
      ("int64 / float64", "Numbers", "Note that a column with any missing value becomes float, because NaN is a float. An integer column that arrives as float often just means 'has gaps'."),
      ("object", "Usually strings", "The catch-all. Also what a mixed-type column becomes, which is why it's worth investigating."),
      ("category", "Repeated labels", "Far less memory than object for low-cardinality columns, and it makes the intended set of values explicit."),
      ("datetime64", "Real dates", "Only if you asked for it. Dates loaded as strings sort alphabetically, which puts 2026-01 before 2025-12 — a silent and nasty bug."),
      ("bool", "True/False", "Becomes object the moment a missing value appears."),
    ]),

    ("h2", "Units and names"),
    ("p", "A column called <code>gearbox_temp</code> tells you nothing about whether it holds Celsius or Fahrenheit. In the Block 1 data, two of four sites report Fahrenheit in that same column — undetectable from the name, obvious the moment you look at the range per site."),
    ("callout", "pitfall", "Names are not contracts", "Column names are documentation written by someone who has since left. Verify the unit, the range, and the meaning against the actual values before trusting any of them. Renaming to <code>gearbox_temp_c</code> after you've confirmed it costs nothing and prevents the bug returning."),

    ("h2", "Sentinel values"),
    ("p", "Some systems write a placeholder rather than a null when a reading fails: <code>9999</code>, <code>-1</code>, <code>0</code>, <code>1900-01-01</code>. These are missing values in disguise, and because they're numeric they silently pollute every statistic."),
    ("p", "In the Block 1 data, 22 rotor-speed readings are exactly 9999.0. Left in place they drag the column mean from 14.4 to 53.3 — a nearly fourfold distortion from 22 rows in six thousand. The tell is a repeated, round, physically implausible value."),

    ("links", [
      ("pandas dtypes", "https://pandas.pydata.org/docs/user_guide/basics.html#dtypes",
       "What each type is, and how missing values force type changes."),
      ("Tidy Data (Wickham, 2014)", "https://vita.had.co.nz/papers/tidy-data.pdf",
       "The paper that defined what a well-shaped table looks like. Still the clearest statement of it."),
    ]),

    ("quiz", [
      ("A column of numbers loads with dtype 'object'. What does that tell you?",
       ["The column has too many distinct values to store as numbers",
        "pandas found something non-numeric in it and fell back to text — investigate before proceeding",
        "The column contains dates"], 1),
      ("Why do 22 sentinel values of 9999.0 in 6,000 rows matter so much?",
       ["They don't — 22 rows is a negligible fraction",
        "They're extreme enough to shift the column mean fourfold, distorting every statistic computed from it",
        "They cause pandas to change the column dtype"], 1),
      ("An integer-looking column loads as float64. What's the most likely reason?",
       ["The values exceed the integer range",
        "The column contains missing values, and NaN is a float",
        "The CSV was written with decimal points"], 1),
    ]),
  ],
},
{
  "slug": "first-fifteen-minutes",
  "title": "The First Fifteen Minutes",
  "subtitle": "A survey, not a clean-up — and the four things you must find before touching anything.",
  "body": [
    ("p", "There's a strong pull, on opening a new dataset, to start fixing things. Resist it for fifteen minutes. The first pass is reconnaissance, and going in with a repair instinct means you fix symptoms before understanding the problem."),

    ("h2", "The four findings that change everything downstream"),
    ("terms", [
      ("1. The target's balance", "Before any metric", "A 15% positive rate means 85% accuracy is free. Every score you read later is interpreted against that number."),
      ("2. Leaking features", "Before any model", "Any column that only exists because the outcome already happened. Catch it now or discover it in production."),
      ("3. Duplicates", "Two kinds", "Identical rows, and the same real thing recorded twice under different ids. The second kind is easy to miss and inflates your scores."),
      ("4. Missingness pattern", "Not just the amount", "Which columns, how much, and — the important part — whether the missing rows differ systematically from the rest."),
    ]),

    ("h2", "Finding the leak"),
    ("p", "The Block 1 dataset carries a column called <code>maintenance_ticket_raised</code>. It looks like a legitimate operational feature. Cross-tabulate it against the target and every <code>URGENT</code> value corresponds to a failure — because the ticket is raised <em>in response to</em> the failure."),
    ("p", "Train on it and you get a near-perfect model that cannot work in production, because at prediction time the ticket doesn't exist yet. The question that catches this is one line from your intake sheet: <em>would I have this value, with this content, at the moment I need the prediction?</em>"),
    ("callout", "insight", "Why the survey pass finds it and later passes don't", "Once you're tuning a model, a feature that helps enormously feels like good news. In the survey pass you have no investment in the result, which makes suspicion cheap. This is the strongest argument for doing reconnaissance before modelling rather than alongside it."),

    ("h2", "Baseline before anything"),
    ("p", "Write down what \"always guess the majority class\" scores, before you build anything. In the Block 1 data that's 84.6%. A model reporting 86% accuracy is then immediately legible as a modest gain rather than an impressive one — and a model reporting 84% is legible as no gain at all."),

    ("h2", "What not to do in this pass"),
    ("ul", [
      "<strong>Don't impute.</strong> You don't yet know why values are missing, and filling before understanding destroys the signal you'd have used.",
      "<strong>Don't drop columns for being messy.</strong> Messy and useless are different. The missingness flag in Block 1 turned out to be one of the better features.",
      "<strong>Don't fit anything.</strong> Not a scaler, not an encoder. That comes after the split, for reasons the pipeline lesson covers.",
      "<strong>Don't start engineering features.</strong> You'll build things you later throw away.",
    ]),

    ("links", [
      ("pandas: essential basic functionality", "https://pandas.pydata.org/docs/user_guide/basics.html",
       "head, describe, value_counts, dtypes — the survey toolkit, documented."),
    ]),

    ("quiz", [
      ("Why compute the majority-class baseline before building anything?",
       ["To decide which algorithm to use",
        "Because every accuracy figure afterwards is meaningless without it — on imbalanced data it's the whole interpretation",
        "Because scikit-learn requires a baseline estimator"], 1),
      ("What single question catches most leaking features?",
       ["Is this feature strongly correlated with the target?",
        "Would I have this value, with this content, at the moment I need the prediction?",
        "Does this feature have missing values?"], 1),
      ("Why avoid imputing during the first pass?",
       ["Imputation is computationally expensive",
        "You don't yet know why values are missing, and filling before understanding can destroy real signal",
        "Imputation must always happen after feature engineering"], 1),
    ]),
  ],
},
{
  "slug": "missing-data-mechanisms",
  "title": "Missing Data: The Mechanism Matters More Than the Amount",
  "subtitle": "Why 'fill it with the median' is a decision about the world, not a default.",
  "body": [
    ("p", "The standard reflex on encountering gaps is to fill them with the column's mean or median and move on. Whether that's reasonable depends entirely on <em>why</em> the values are absent — and that question has three standard answers with very different consequences."),

    ("h2", "The three mechanisms"),
    ("terms", [
      ("MCAR", "Missing completely at random", "The gap is unrelated to anything — a dropped packet, a corrupted row. Filling is relatively safe and you mainly lose statistical power."),
      ("MAR", "Missing at random, given other columns", "Missingness is explained by data you *do* have. One site's sensors fail more often. Fill using those other columns and you can do well."),
      ("MNAR", "Missing not at random", "Missingness depends on the missing value itself. High-vibration sensors drop out *because* of the vibration. Filling actively introduces bias."),
    ]),
    ("callout", "insight", "You cannot test for MNAR directly", "By definition you don't have the values that would prove it. What you can do is compare rows where a value is missing against rows where it's present, on every *other* column. If those groups differ systematically, treat MNAR as likely — and involve someone who knows how the data is collected."),

    ("h2", "The Block 1 case"),
    ("p", "Vibration readings are missing on about 7% of turbines. Comparing those rows against the rest: the missing group has a failure rate of 24% against 14.9% for the rest. Missingness is strongly associated with the outcome."),
    ("p", "The mechanism is physical — the sensors fail most on the turbines shaking hardest. So the missing values are disproportionately the <em>high</em> ones. Fill them with the median and you replace the most alarming readings in the dataset with typical ones, systematically hiding the risk you were hired to detect."),

    ("h2", "The move that turns a problem into a feature"),
    ("p", "Add a binary column recording that the value was missing, before filling anything. It costs one column and preserves the signal that the imputation is about to destroy. In the Block 1 pipeline, that flag ends up among the more predictive features — the absence of data <em>is</em> data."),
    ("callout", "matters", "The order that matters", "Record the flag, then impute — and impute inside a pipeline, after the split. Fitting an imputer on the full dataset means the training data has seen the test set's statistics. It's one of the most common leaks in practice precisely because it doesn't feel like model fitting."),

    ("h2", "Choosing a fill"),
    ("ul", [
      "<strong>Median</strong> — robust to skew and outliers. The sensible default for numeric columns.",
      "<strong>Mean</strong> — only for roughly symmetric distributions. Skew drags it.",
      "<strong>Most frequent</strong> — for categoricals, though a literal <code>\"missing\"</code> category is often more honest.",
      "<strong>Model-based (KNN, iterative)</strong> — predicts the gap from other columns. Genuinely better under MAR, and slower and easier to leak with.",
      "<strong>Leave it</strong> — gradient boosting implementations handle missing values natively and often do better than any fill you'd choose.",
    ]),

    ("links", [
      ("Imputation of missing values (scikit-learn)", "https://scikit-learn.org/stable/modules/impute.html",
       "Simple, iterative and KNN imputers, and the missing-indicator feature discussed above."),
      ("Statistical Analysis with Missing Data — overview", "https://stefvanbuuren.name/fimd/",
       "Van Buuren's open book on multiple imputation. Chapter 1 covers the three mechanisms properly."),
    ]),

    ("quiz", [
      ("Vibration sensors fail more often on high-vibration turbines. Which mechanism is that?",
       ["MCAR — the failures are random hardware faults",
        "MNAR — missingness depends on the value that's missing",
        "MAR — it's explained by the other columns"], 1),
      ("Why add a missingness flag before imputing?",
       ["It helps the imputer choose a better fill value",
        "The fact a value was missing may itself be predictive, and imputation destroys that information",
        "scikit-learn requires it for pipelines"], 1),
      ("Why must imputation happen inside a pipeline rather than before splitting?",
       ["Pipelines run faster",
        "Fitting the imputer on all the data lets the test set's statistics into training — a leak that shows no train/validation gap",
        "Pipelines handle categorical columns automatically"], 1),
    ]),
  ],
},
{
  "slug": "what-a-plot-is-for",
  "title": "What a Plot Is Actually For",
  "subtitle": "Exploration with intent — five questions worth asking, and the charts that answer them.",
  "body": [
    ("p", "Exploratory analysis becomes a ritual very easily: produce a grid of histograms, note that things look roughly as expected, move on. A plot earns its place only when you would <em>do something different</em> depending on what it shows."),

    ("h2", "Five questions with decisions attached"),
    ("terms", [
      ("What shape is it?", "Histogram", "Skewed, bimodal, bounded? Decides whether the mean is a meaningful summary and whether a transform would help."),
      ("Does it relate to the target?", "Box plot by class", "Decides which features are worth keeping before you fit anything."),
      ("Are features redundant?", "Correlation heatmap", "Two near-identical columns destabilise linear models. Decides what to combine or drop."),
      ("Do the groups really differ?", "Bar chart with error bars", "Decides whether an apparent group effect is real or sample noise."),
      ("Is the missingness informative?", "Rate by missing flag", "Decides whether the flag becomes a feature."),
    ]),

    ("h2", "Read the gap between mean and median"),
    ("p", "Draw both on a histogram. Where the mean sits noticeably to the right of the median, the variable is right-skewed — a long tail pulling the average up. It follows that \"the average turbine\" is a misleading summary, and that a linear model may do better on the log of the variable than on the variable."),

    ("h2", "The two mistakes that recur"),
    ("callout", "pitfall", "Correlation only sees straight lines", "Pearson correlation measures linear association. A strong curved relationship — performance rising then falling with temperature, say — can show a correlation near zero. Never conclude 'no relationship' from a low correlation without looking at the scatter plot."),
    ("callout", "pitfall", "A bar chart without error bars is an assertion", "Site A fails at 17% and site B at 15%. Real difference, or forty turbines' worth of noise? Without confidence intervals the chart cannot tell you, and it will be read as though it had. This is your statistics course's sample-size point, applied to the most common chart in business analysis."),

    ("h2", "Confounding, in one example"),
    ("p", "In the Block 1 data one site has both a higher failure rate and older turbines. Is the site risky, or is it just old? The chart cannot separate those, and reporting \"site X is our problem site\" on that basis would send maintenance budget to the wrong place."),
    ("p", "The honest answer is to compare like with like — failure rate by site <em>within</em> age bands — or to let a model with both features estimate their separate contributions. What you must not do is read a raw group difference as a causal claim about the group."),

    ("h2", "What the exploration pass should produce"),
    ("p", "Not a folder of charts. A short list of findings that change what you do next: which features carry signal, which are redundant, which groups differ, and where you're uncertain. In Block 1 that list is five lines long and every line shapes the modelling that follows."),

    ("links", [
      ("seaborn tutorial", "https://seaborn.pydata.org/tutorial.html",
       "Distribution, relational and categorical plots, with guidance on which to reach for."),
      ("Anscombe's quartet", "https://en.wikipedia.org/wiki/Anscombe%27s_quartet",
       "Four datasets with identical summary statistics and completely different shapes. The case for plotting, in one image."),
    ]),

    ("quiz", [
      ("The mean of a variable sits well to the right of its median. What does that indicate?",
       ["The data contains errors",
        "Right skew — a long tail of high values pulling the average up",
        "The variable is bimodal"], 1),
      ("A correlation near zero between two variables means what, exactly?",
       ["They are unrelated",
        "No strong *linear* relationship — a curved relationship can show near-zero correlation",
        "One variable is constant"], 1),
      ("A site shows a higher failure rate and also has older turbines. What can you conclude?",
       ["The site has a real operational problem",
        "Not much yet — age may be confounding the site effect, so compare within age bands",
        "Age is irrelevant since site is the stronger signal"], 1),
    ]),
  ],
},
{
  "slug": "ai-assisted-analysis",
  "title": "AI-Assisted Analysis, and Where It Lies to You",
  "subtitle": "The original syllabus promises 'Python with generative AI'. Here's the honest version.",
  "body": [
    ("p", "Using a model to help with data work is genuinely productive, and it fails in specific, predictable ways. Knowing which is which is the difference between a real speed-up and confidently wrong analysis."),

    ("h2", "Where it reliably helps"),
    ("ul", [
      "<strong>Syntax you'd otherwise look up.</strong> Reshaping, multi-level groupbys, the exact seaborn incantation. High value, low risk — the code either runs and does the visible thing or it doesn't.",
      "<strong>Boilerplate.</strong> Plot scaffolding, pipeline structure, docstrings.",
      "<strong>Explaining an error.</strong> Pasting a traceback is often faster than searching.",
      "<strong>Reviewing your approach.</strong> \"Here's my cleaning sequence — what have I not considered?\" It's good at generating candidate concerns for you to check.",
      "<strong>Naming and structure.</strong> Turning a working mess into something readable.",
    ]),

    ("h2", "Where it lies"),
    ("terms", [
      ("Invented methods", "Plausible, non-existent APIs", "A pandas method that sounds exactly right and doesn't exist. Easy to catch — it errors."),
      ("Silently wrong logic", "Runs, wrong answer", "The dangerous one. A groupby on the wrong key, a merge that drops rows, an off-by-one on a date window. No error, plausible output."),
      ("Confident domain claims", "Statistics stated as fact", "\"A VIF above 5 indicates multicollinearity\" — the sort of threshold that's conventional rather than true, delivered with certainty."),
      ("Context it cannot have", "About your specific data", "It hasn't seen your rows. Any claim about what your data contains is inference from the column names."),
    ]),
    ("callout", "pitfall", "The failure that actually costs you", "Not the hallucinated function — that errors immediately. It's the merge that silently drops 400 rows because the join key had different whitespace on each side. The code runs, the output looks fine, and your analysis is wrong. **After every AI-suggested transform, check the row count and the null counts.** Two lines, and it catches most of this."),

    ("h2", "A workflow that holds up"),
    ("terms", [
      ("1. You decide", "The question and the approach", "The model is bad at knowing what matters in your business. That judgement is the part you're actually paid for."),
      ("2. It drafts", "The code", "Where it's genuinely fast."),
      ("3. You verify", "Shape, nulls, a spot check", "Before and after. Non-negotiable."),
      ("4. You interpret", "What it means", "The model will happily explain a result it cannot see the context for."),
    ]),

    ("h2", "The trap specific to data work"),
    ("p", "Ask a model to \"clean this dataset\" and it will produce something reasonable-looking: fill the nulls, drop the duplicates, encode the categoricals. Every one of those is a decision with consequences, and it made all of them for you, invisibly."),
    ("p", "In the Block 1 data, the reasonable-looking action — filling vibration with the median — is precisely wrong, because the values are missing not at random. No model can know that from the column names. It requires knowing that vibration sensors fail on shaking turbines, which is domain knowledge you had to go and get."),
    ("callout", "matters", "The line worth holding", "Let it write the code. Don't let it make the decisions. Every entry on your cleaning-decisions list should be one you can defend, and 'the model suggested it' is not a defence you'd want to give to an operations manager whose maintenance schedule you got wrong."),

    ("h2", "The connection to everything else"),
    ("p", "This is the same principle as the rest of the program arriving early: verify rather than trust, hold something back that the optimiser can't see, and don't let the thing producing the work also be the thing judging it. Blocks 5 and 6 formalise it. Here it's just good practice."),

    ("links", [
      ("Building effective agents", "https://www.anthropic.com/engineering/building-effective-agents",
       "On knowing which parts of a task to hand over and which to keep — the same division applied to agents."),
    ]),

    ("quiz", [
      ("Which AI failure mode is most dangerous in data work?",
       ["Inventing a pandas method that doesn't exist",
        "Code that runs and produces plausible output while being logically wrong — a merge that silently drops rows",
        "Refusing to answer a question"], 1),
      ("What should you check after every AI-suggested transform?",
       ["Whether the code follows PEP 8",
        "Row count and null counts, before and after",
        "Whether a faster implementation exists"], 1),
      ("Why can't a model decide how to handle your missing values?",
       ["Models aren't trained on imputation techniques",
        "It hasn't seen your data or the physical process behind it — MNAR is domain knowledge, not a property of column names",
        "Imputation requires more context than fits in a prompt"], 1),
    ]),
  ],
},
]
