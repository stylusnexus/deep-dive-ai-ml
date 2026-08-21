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

**Eval battery** — A fixed set of tasks with machine-checkable outcomes. Its value comes from staying fixed.

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
*to come*
