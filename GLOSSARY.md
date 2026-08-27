# Glossary

Accumulates block by block. Every term defined here is fed into engram spaced
repetition — the mechanism the original program has no equivalent for.

Terms are written to be *said out loud*, not recited. If you can't explain one
to someone non-technical in two sentences, it hasn't landed yet.

---

## Block 0 · Vocabulary

**Agent loop** — The while-loop that runs a model repeatedly, executing any tool it asks for and feeding the result back, until the model answers without needing a tool.

**Harness** — Everything around the loop: prompt assembly, tool registry, result formatting, turn limits, persistence. Most agent failures are harness failures. (Also used for *evaluation* harness — context disambiguates.)

**Token** — The unit a model actually reads, roughly ¾ of an English word. All cost, speed and limit figures are denominated in these.

**Context window** — The maximum tokens a model can consider at once, covering prompt, history, retrieved documents and the answer together. A capacity limit, not a promise of attention.

**KV cache** — Stored key/value vectors for tokens already processed, so they aren't recomputed each step. Grows with context length, and is usually what exhausts memory locally. Prompt caching is this, sold as a feature.

**Prefill / decode** — Processing the prompt (parallel, fast) versus generating the answer one token at a time (sequential, slower). Quoted tok/s almost always means decode.

**Weights / parameters** — The numbers that constitute a trained model. "7B" means seven billion of them.

**Quantization** — Storing each weight in fewer bits (4, 5, 8) instead of 16. Shrinks and speeds up the model at a small cost in precision.

**Q4_K_M** — Four-bit K-quant, medium size. The usual local default. Q = quantized, 4 = bits, K = k-quant method, M = medium.

**GGUF** — The self-contained file format holding quantized weights plus tokenizer and metadata. What llama.cpp and Ollama consume.

**llama.cpp** — The C++ inference engine doing the actual arithmetic, including on Apple Silicon via Metal.

**Ollama** — A wrapper over llama.cpp: model registry, local HTTP server with an OpenAI-shaped API, memory management. Optimised for one developer on one machine.

**tok/s** — Tokens per second. Below ~10 feels sluggish; 20–30 reads at conversational speed. Local inference is memory-bandwidth bound, so quantization improves it.

**Embedding** — A fixed-length list of numbers representing text, where similar meanings produce similar directions. Weak at negation and at identifiers.

**Cosine similarity** — The angle between two vectors, from 1 to -1. How "closeness of meaning" is actually measured.

**Semantic routing** — Picking a lane by embedding the incoming turn and comparing it to embedded examples. Milliseconds and fractions of a cent, versus asking an LLM to classify.

**Tool call** — Structured text the model emits requesting a function. The harness parses and executes it; the model never touches the tool.

**MCP (Model Context Protocol)** — A common protocol between agents and tool providers, so integrations are written once rather than once per framework. Carries tools, resources and prompts.

**Escalation** — Trying a cheap local model, verifying the result, and moving to a paid model only on observed failure. Requires a real verifier; useless where quality is subjective.

**Temperature** — Flattens or sharpens the next-token distribution. Use 0 for anything parsed by code.

**top-k / top-p** — Limit sampling to the k most likely tokens, or to the smallest set summing to probability p. top-p adapts to the distribution's shape and is usually preferred.

**Eval battery** — A fixed set of tasks with machine-checkable outcomes. Its value comes from staying fixed. The battery is the *data*; an eval harness is the *machinery* that runs it. Distinct again from an agent harness, which is the scaffolding around one agent run.

**Model-as-judge** — Using a model to grade another model's output. Flexible, biased, and circular if the judge is the model under test.

**Overfitting** — The model memorised the training data including its noise. Excellent on seen data, poor on new data. The dangerous failure, because it looks like success.

**Underfitting** — The model is too simple to capture the real pattern. Poor on both training and new data. The obvious failure.

**Train / validation / test split** — Learn on one slice, tune against a second, and measure once on a third you haven't looked at. The gap between train and validation performance is the diagnostic.

**Early stopping** — Halting training when validation loss stops improving. The cheapest defence against overfitting.

**Regularisation** — Penalising complexity (L1/L2) or dropping random units (dropout) so the model can't memorise as easily.

**Hallucination** — Confidently stated falsehood. Not a bug: the model samples plausible text and has no internal flag separating knowing from pattern-matching. Fluency carries no information about accuracy.

**Grounding** — Tying output to supplied sources rather than to parameters. What RAG is for, and the most effective mitigation — but not a guarantee.

**Groundedness** — Whether an answer is actually supported by what was retrieved. Measured separately from whether the answer is correct.

**Zero-shot / few-shot / many-shot** — How many examples you put in the prompt. Few-shot (2–10) is the workhorse.

**In-context learning** — Changing behaviour via prompt examples without changing weights. Nothing persists after the call. Good at format and label space, weak at new knowledge and hard reasoning.

**Class imbalance** — One class dominates, so accuracy becomes misleading. Always compute what "always guess the majority class" scores before reporting any accuracy figure.

**Decision threshold** — The cut-off turning a probability into an action. 0.5 is a convention inherited from balanced problems, not an answer. Moving it trades precision against recall directly.

**SMOTE / class weights / resampling** — Ways to handle imbalance. Resample inside the pipeline after the split — doing it before is textbook leakage.

**Data drift** — The inputs change; the input-output relationship still holds. Usually fixed by retraining on recent data.

**Concept drift** — The relationship itself changes, so historical training data becomes misleading. Harder.

**Population Stability Index / KS test** — Statistics for detecting input distribution shift when ground-truth labels arrive too late to measure accuracy directly.

**Distillation** — Training a small student model to reproduce a large teacher's behaviour. The teacher's full probability distribution ("dark knowledge") carries more signal than hard labels.

**Chain-of-thought** — Prompting the model to produce intermediate steps. Works because it allocates more computation and lets the model build on its own partial results — not because it becomes smarter.

**Self-consistency** — Sampling several reasoning chains and taking the majority answer. Buys accuracy with tokens.

**Reasoning tokens** — Tokens a reasoning model generates before answering, often hidden and always billed. Cost tracks problem difficulty rather than visible output length.

**Faithfulness (of reasoning)** — Whether a stated chain is the actual reason for the answer. Frequently it isn't — treat chains as a debugging aid, never as an audit trail.

**Verifier-guided loop** — Generate, check against something external (tests, compiler, schema), retry on failure. The strongest inference-time loop, because the signal isn't the model's own opinion.

**Self-correction (unaided)** — Asking a model to review and fix its own answer with no external feedback. Often *degrades* correct answers on reasoning tasks; the instruction to find fault is itself pressure to change something.

**Best-of-N** — Generate N candidates, keep the highest-scoring. Quality is capped by the scorer.

**Termination condition** — What stops a loop. "Until the model says it's done" hands the decision to the component least able to judge success. Terminate on an external check, a turn cap and a spend cap.

**Rejection sampling / STaR** — Generate many attempts, keep only those reaching a verified correct answer, fine-tune on those. A self-training loop that works because the filter is external.

**Self-play** — Improving by competing against yourself. Needs a definite winner, which is why it transfers to code and maths and not to prose.

**Model collapse** — Successive generations trained on generated data lose the distribution's tails first, then narrow at the centre. Prevented by an external filter, fresh real data, and held-out evaluation the loop can't see.

**Deterministic-first** — A model is the most expensive, slowest, least testable component available. The judgement is knowing when it earns that: is there a bounded, checkable mechanism that does this job well?

**Compliance test (prompt vs tool)** — Can the model tell when it has complied? Mechanically checkable rules belong in tools as preconditions; prompts carry only what tools cannot check.

**Confound (in evaluation)** — A limit that can end a run and does not appear in the output. Indistinguishable from the thing you were measuring.

**Control fixture** — A deliberately easy task in the same domain and harness. When a board reads uniformly zero, it tells you whether the wall is capability or scaffolding.

**LLM-as-judge** — Using a model to grade output. Ships with position, verbosity, self-preference and score-compression biases. The fatal case is a grader whose error correlates with the treatment — that manufactures an effect sampling cannot remove.

**Attention budget** — Finite capacity to attend, degrading as a gradient rather than a cliff. The objective is the smallest set of high-signal tokens, not a full window.

**Compaction** — Replacing a long trace with a summary preserving decisions and open issues. Clearing old tool results is its safest, lightest form.

**Structured note-taking** — Agent writes durable notes outside the context window and reads them back after a reset.

**Sub-agent isolation** — Exploration in a clean context returning a condensed summary. The one argument for multi-agent that survives scrutiny.

**Tool search / programmatic tool calling** — Loading tool definitions on demand, and orchestrating tools in sandboxed code so intermediate results never enter context. Both reduce tokens *and* improve accuracy.

**Test-time compute** — Spending computation at inference rather than parameters at training. The capability axis you control without training anything.

**Skill** — A folder packaging procedural knowledge: a SKILL.md with a name and a when-to-use description, plus optional reference files and executable scripts. A tool is a verb, an MCP server is a place, a skill is a method.

**Progressive disclosure** — Name and description always in context; the body loads on trigger; bundled files load only when reached. Lets a skill be arbitrarily detailed without that detail costing anything until used.

**Trajectory log** — Every turn, every tool call, and a named termination reason. The only artefact that survives an agent run, since runs cannot be reproduced.

**Termination reason** — Completed / turn cap / spend cap / timeout / error, recorded distinguishably. Without it a wall clock looks like a model giving up.

**Circuit breaker vs kill switch** — A breaker halts a pattern of runs on error rate or spend; a kill switch halts everything via one flag with no deploy. Both are needed, and neither stops in-flight work unless cancellation is checked between turns.

**Prompt accretion** — Defensive lines added per incident and never removed, until the instructions contradict each other. Date every addition and re-run the eval set with it removed.

**MCP primitives** — Server offers Tools (model-controlled), Resources (application-controlled, read-only by nature), Prompts (user-controlled templates). Client offers Sampling (server asks the model), Roots (server asks its boundaries), Elicitation (server asks the user).

**stdio vs Streamable HTTP** — stdio runs the server as a subprocess with nothing listening on a port; HTTP brings the full web threat model. Prefer stdio locally.

**Token passthrough** — A server accepting a token not issued to it and forwarding it downstream. Explicitly forbidden: breaks rate limiting, breaks the audit trail, enables proxied exfiltration.

**Confused deputy (MCP)** — A proxy server with a static client ID plus dynamic registration plus a consent cookie lets an attacker obtain authorization codes with no consent screen. Fixed by per-client consent before forwarding.

**Scope inflation** — Publishing every scope up front so one stolen token reaches everything. Fixed by minimal initial scopes and elevation on demand.

**Prefill / decode** — Processing your prompt (parallel, fast, scales with what you sent) versus generating the answer one token at a time (sequential, slow). Time-to-first-token is prefill; tokens-per-second is decode.

**Cold start** — Time before a system can serve any request: loading weights, allocating the cache, warming the runtime. Distinct from a cache miss, and fixed by keeping something warm rather than making it faster.

**Warm states** — Fully cold (nothing loaded), model-warm/cache-cold (the common case), fully warm (new tokens only), and evicted (was warm, silently is not any more).

**Cache prefix rule** — Prompt caching keys on an exact unchanged prefix. Anything variable — a timestamp, a session id — must go last, or the hit rate silently goes to zero.

**Queueing knee** — Below capacity, latency is roughly flat as load rises; past it, queue time grows without limit and p95 detaches from p50 sharply. Load-testing at 60% tells you little about 95%.

**Session decay** — Long sessions degrade because early mistakes stay in history, get re-read each turn, and are treated as established fact. Restarting with a short accurate summary usually beats fighting it.

**Compaction loss** — What a summary dropped is invisible to the agent, so it carries on confidently with a thinner picture. Constraints that must survive belong in the system prompt or a file.

**Rung** — One configuration in an ordered ladder of increasing assistance (bare, test-first, reloop, guards-off, decomposed, oracle). Where a task starts passing is the diagnosis.

**Oracle rung** — The control at the top of a ladder, supplying most of the answer. Failing there means the fixture is broken rather than the agent.

**Prefix caching** — Reusing the processed keys and values for an unchanged prompt prefix. The largest latency lever in a multi-turn loop, and it fails silently: a cache that stopped matching looks exactly like one that never existed, except on the bill.

**Read accumulation** — Tool results staying in the transcript and being re-sent every turn. A single large read early in a run is paid for on every turn after it.

**Verification granularity** — Whether you check after every edit, after a logical unit, or once at the end. Decides whether feedback names the cause or only the symptom. Per-edit checking breaks on changes that are atomic across files.

---

## Block 0 · Orientation

**AI ⊃ ML ⊃ Deep learning ⊃ Generative AI** — They nest, they aren't alternatives. AI is any system doing something intelligent; ML learns from data instead of rules; deep learning is many-layered neural networks that learn their own features; generative AI produces content rather than a label.

**Agentic AI** — Deliberately outside that nesting: an architecture, not a model type. A loop that lets a model choose actions and use tools.

**Predictive vs generative** — Predictive models answer closed questions with checkable answers. Generative models produce open-ended content, which is why evaluating them is a research problem rather than a formula.

---

## Block 0 · Algorithms

**Gradient descent** — Compute the slope of the loss with respect to each parameter, step the other way, repeat. The learning rate is the step size and the cause of most training instability.

**Backpropagation** — Computing all those gradients efficiently by applying the chain rule backwards from the loss. Why training needs more memory than inference: forward-pass activations must be kept.

**Epoch / batch / mini-batch** — One full pass through the data; how many examples per gradient step. Mini-batch (32–512) is what everyone uses.

**Adam** — The default optimiser. Adapts step size per parameter rather than using one global learning rate.

**Linear regression** — Fits a line minimising squared error. Interpretable coefficients. The baseline for numeric prediction.

**Logistic regression** — Fits a linear combination through a sigmoid to produce a probability. Classifies, despite the name. The threshold is a business decision, not a model output.

**Ridge (L2) / Lasso (L1) / Elastic Net** — Regularised regression. Ridge shrinks coefficients; Lasso drives some to exactly zero, selecting features.

**Gini impurity / entropy** — How a decision tree scores a candidate split. Both measure how purely a split separates classes.

**Pruning / max_depth** — The controls that stop a tree splitting until every leaf holds one row.

**Bagging** — Train many models on random samples of rows, average them. Cancels variance.

**Random forest** — Bagging plus random feature selection at each split, decorrelating the trees further. The strong, low-tuning tabular default.

**Gradient boosting** — Sequential trees, each fitted to the previous ensemble's errors. Higher ceiling than a forest, and will overfit without early stopping. XGBoost, LightGBM, CatBoost.

**k-means** — Assign points to nearest centre, move centres to the mean, repeat. You choose k. Requires scaled features.

**k-NN** — No training; find the k most similar examples at prediction time and vote. RAG retrieval is this algorithm over embeddings.

**Curse of dimensionality** — As dimensions rise, nearest and farthest distances converge, so "closest" carries less information.

**Attention (query, key, value)** — Each token compares its query against every key and takes a weighted blend of values. All-to-all, which is why cost is quadratic in sequence length.

**Transformer** — Stacked attention layers with multiple heads. Positional information must be added separately because attention is order-blind.

**HNSW / IVF** — Approximate nearest-neighbour indexes. HNSW navigates a layered graph; IVF searches only the nearest clusters. Both trade recall for speed.

**Recall@k** — The fraction of true nearest neighbours an index actually returned. The number nobody measures, and a common hidden cause of poor RAG.

**BM25** — Term-frequency keyword ranking, adjusted for rare terms and diminishing repeats. Beats embeddings on identifiers, error codes and rare terms.

**Reciprocal rank fusion** — Combine ranked lists using positions rather than scores: sum of 1/(k + rank), k≈60. No normalisation needed.

**Cross-encoder reranker** — Scores query and document together rather than separately. Much more accurate, far too slow for a whole corpus — so it reranks a shortlist.

**Data leakage** — Information available at training time but not at prediction time. Inflates training *and* validation together, so the usual overfitting gap shows nothing wrong.

---

## Block 1 · Python, Data & EDA

**dtype** — The type pandas inferred for a column. A numeric-looking column typed `object` means something non-numeric is in it. Free diagnostic; read it every time.

**Sentinel value** — A placeholder written instead of a null: 9999, -1, 1900-01-01. Missing data in disguise, and it silently pollutes every statistic.

**MCAR / MAR / MNAR** — The three missingness mechanisms. Completely at random (filling is safe); at random given other columns (fill using them); not at random (filling introduces bias).

**Missingness indicator** — A binary column recording that a value was absent, added before imputing. Preserves signal that imputation would destroy.

**Stratified split** — Splitting while preserving class balance in both halves. Necessary whenever a class is rare.

**Pipeline** — Chained preprocessing plus model, fitted on training data only. Makes leakage structurally difficult, including inside cross-validation.

**Threshold table** — Recall, precision, missed cases and false alarms across candidate cut-offs. More useful than any single score, because it converts a model into a business decision.

**Confounding** — A group difference explained by a third variable. A site with a higher failure rate and older turbines may just be old.

## Block 2 · Classical ML

**Model ladder** — Climbing from majority class, to one rule, to logistic regression, to a forest, to boosting, to a network — stopping at the first rung that is good enough. Each rung must beat the one below it on the same fixtures, or you have learned that the extra complexity bought nothing.

**Accuracy** — The fraction of all predictions that were correct. Meaningless when one class dominates, so always read it against the majority-class baseline before quoting it.

**Precision** — Of the cases you flagged, how many were real. Low precision means effort wasted chasing false alarms.

**Recall (sensitivity)** — Of the cases that were real, how many you caught. Low recall means missed cases, which is the expensive error whenever missing something is worse than a false alarm.

**Specificity** — Of the genuinely negative cases, how many you correctly left alone. The mirror of recall, and the number that matters when false alarms are costly.

**F1** — The harmonic mean of precision and recall, used when you need one number and both errors matter. It hides which of the two is failing, so read the pair as well.

**Mean absolute error (MAE)** — Average distance from the truth in the original units. Robust to outliers and easy to explain to anyone.

**Root mean squared error (RMSE)** — Like MAE but penalising large errors disproportionately. Use it when one big miss is worse than several small ones.

**Mean absolute percentage error (MAPE)** — Error in percentage terms, which travels well between stakeholders. It breaks badly when true values approach zero.

**R-squared** — The proportion of variance the model explains. Comparable across problems and easy to over-read: a high value on a trivially predictable target means nothing.

**Derived feature** — A column built from others to expose what a raw value hides: a rate rather than a total, a deviation from the group norm rather than a level, days since an event rather than a date. Usually worth more than a bigger model.

**Lag feature** — The value from n periods ago. Frequently the single strongest predictor in a time series, and the first one to build.

**Rolling statistic** — A mean, maximum or standard deviation over a moving window. A rolling mean smooths noise; a rolling standard deviation captures instability, which is often the real signal.

**Differencing** — Replacing a level with the change since the last period. Converts "how much" into "what moved", which is usually the question.

**Calendar feature** — Day of week, month, holiday. Cheap, and they capture seasonality that no lag will.

**Expanding window** — Backtesting where the training set grows with each fold, using all available history. The default when older data stays relevant.

**Sliding window** — Backtesting with a fixed-length training set that moves forward, deliberately discarding old data. Right when the process itself has changed and history has become misleading.

**Train-test gap** — Leaving a deliberate time gap between training and test data, matching how far ahead the prediction is actually used. Without it you are testing with information the deployed model would not have.

**Input normalisation** — Rescaling features to comparable ranges before training a network. Non-negotiable: unscaled features make the loss surface pathological, and this is the commonest reason a network will not train.

**Overfit one batch** — Deliberately training on a single batch until the loss collapses, to prove the training loop is wired correctly. Ninety seconds, before tuning anything.

**Early stopping** — Halting training when validation performance stops improving. Networks will fit noise indefinitely if you let them.

**Class weights** — Making errors on the rare class cost more during training. Without them a model on imbalanced data learns to predict the majority and calls it accuracy.


---

## Block 3 · Retrieval and Agentic RAG

**Chunking** — Cutting documents into retrievable pieces before embedding them. Split on structure — headings, sections, functions — because a chunk that ends mid-sentence embeds badly and reads worse.

**Chunk overlap** — Repeating a little of each chunk in its neighbour, usually 10–15%. Without it, a passage that straddles a boundary is lost by both sides.

**Parent-document retrieval** — Match on a small chunk, then hand the model the larger section it came from. You get the precision of a small chunk and the context of a big one.

**Index recall** — Whether your approximate index returns what an exhaustive search would have. It is a property of the index alone, measured against brute force, and almost nobody checks it.

**Retrieval quality** — Whether the right chunk reaches the top k. Distinct from index recall: the index can be perfect and the embedding still wrong, and the two failures have different fixes.

**Mean reciprocal rank (MRR)** — How high the right answer ranked, averaged over questions. Rewards putting the answer first rather than fifth.

**Hit rate at k=1** — Did the best chunk come back first? Blunt and honest — when this is low, a reranker is the highest-value thing you can add.

**Answer correctness** — Whether the answer is actually right, scored separately from whether it was grounded. High groundedness with low correctness means retrieval handed the model the wrong material, which is fixable upstream.

**Distractor** — A retrieved chunk that is topically close but does not answer the question. Models do not politely ignore them; they actively degrade the answer, which is why you send three to five chunks rather than twenty.

**Multi-hop question** — One whose answer needs two facts that live in different documents. Single-shot retrieval embeds the question, lands near one of them, and misses the other.

**Comparative question** — One that needs several sources assembled and contrasted, such as how this year's policy differs from last year's. Retrieving one of them is worse than useless.

**Under-specified question** — One whose real meaning only emerges after a first look, like "why did output drop?". It cannot be embedded usefully until you know which site and which period.

**Aggregative question** — One that needs many chunks rather than the best five, such as how many incidents mentioned a term. A counting problem wearing a retrieval costume.

**Agentic RAG** — Retrieval as a loop rather than a single shot: retrieve, read what came back, then ask a better question. It works because the second query did not exist until the first result arrived.

**Hop limit** — A hard cap on how many retrieval rounds the loop may take, usually three or four, plus a token budget. The gains flatten quickly and the costs do not.

---

## Block 4 · Agentic AI

**Graph runtime** — A framework that models an agent as nodes and edges rather than a while-loop, so the control flow becomes data something else can get between. LangGraph is the one this course uses.

**State (graph)** — The typed dictionary threaded through every node, holding the plan, the history and what is known. Nodes receive it and return updates to it rather than rewriting it.

**Node** — A function that transforms state: call the model, run a tool, summarise, validate. Ordinary functions, with no framework magic inside them.

**Edge** — What runs next. A conditional edge that points back to an earlier node is how a graph expresses a loop.

**Checkpointer** — The component that persists state after every node. This is the feature that changes what is possible; branching and typed state you could write yourself in an afternoon.

**Resumption** — Continuing a crashed or paused run from its last checkpoint rather than the beginning. A crash on turn nine restarts at turn nine, so the eight turns of model calls before it are not paid for twice.

**Interrupt** — A deliberate stop before a node, which persists state and hands control back to the caller. This is an approval gate that genuinely halts, as opposed to a prompt politely asking to proceed.

**Thread id** — The key a checkpointer stores a run's state under. Resuming means invoking the graph again with the same thread id and no new input.

**Approval gate** — A point where work stops until a human decides. It only counts if the run persists while it waits; a gate that lets the work continue is decoration.

**Audit trail** — Who approved, when, and exactly what. "Approved" without those three is not an audit trail.

**Termination condition** — The observable event that ends an agent loop, normally the model ceasing to request tools. Asking the model whether it is finished is an opinion, not an event.

**Turn cap** — A hard limit on loop iterations, which must name itself when it fires. A run that returns nothing with no reason is indistinguishable from the model failing.

**Trace** — Everything that happened in service of one request, tied together by a single identifier. The unit you look at when asking what happened to this particular run.

**Span** — One unit of work inside a trace: a model call, a retrieval, a tool execution. Spans nest, so a tool span sits inside the turn that requested it.

**Attributes** — Structured facts attached to a span — model name, token counts, latency, tool arguments. Queryable, unlike a line of prose in a log.

**Events** — Timestamped occurrences within a span, such as a retry, a cache miss, or a guard firing.

**Baggage** — Context carried across process boundaries, most often the trace id following a request into a sub-agent so the whole tree stays connected.

**Logs** — What happened, in prose. Good for the unexpected, terrible at answering "how often" or "how slow".

**Metrics** — Aggregates over time. Good for "is this getting worse", useless for "why did this one fail".

**Orchestrator and workers** — One agent plans, several execute in parallel. Works when the subtasks are genuinely independent, and fails expensively when they need each other's intermediate results.

**Planner, generator, evaluator** — Splitting conflicting roles across separate contexts so the evaluator is not marking the generator's homework. The independence requirement from the judging lesson, expressed as architecture.

**Sub-agent as a tool** — A child agent the parent calls like any other tool: it runs, returns, and disappears. The simplest useful form of multi-agent, and the one to reach for first.

**Prompt caching** — Reusing the processed prefix of a prompt across calls so prefill is largely skipped. The single largest latency and cost lever in an agent loop, and it keys on an exact byte-identical prefix.

**Cache hit rate** — The fraction of calls that actually reused a cached prefix. Nothing errors on a miss, so a cache that quietly stopped working looks exactly like never having had one, except on the bill.

**Truncate on ingest** — Capping each tool result as it enters the context. One line of code, and it prevents a single large file read from dominating the window for the rest of the run.

**Summarise as you go** — Replacing a read with a short statement of what was learned. Preserves the finding and drops the bulk, but is lossy in a way the agent cannot see.

**Drop after use** — Clearing old tool results once the work derived from them is done. The safest form of compaction, because a read that has already produced an edit is rarely needed verbatim again.

**Verification granularity** — How often you check the agent's work: at the end, per logical unit, or per edit. Verifying at the end is cheapest and tells you least; per edit names the failure immediately and costs the most.
