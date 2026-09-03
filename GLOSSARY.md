# Glossary

Accumulates block by block. Every term defined here is fed into engram spaced
repetition — the mechanism the original program has no equivalent for.

Terms are written to be *said out loud*, not recited. If you can't explain one
to someone non-technical in two sentences, it hasn't landed yet.

---

## Block 0 · Vocabulary

**ReAct (reason and act)** — Interleaving a reasoning step with an action: think, call a tool, read the result, think again. Named when it was a technique you chose; it is now simply what an agent loop is, which is why you meet the term in papers and not in code.

**Agent loop** — The while-loop that runs a model repeatedly, executing any tool it asks for and feeding the result back, until the model answers without needing a tool.

**Harness** — Everything around the loop: prompt assembly, tool registry, result formatting, turn limits, persistence. Most agent failures are harness failures. (Also used for *evaluation* harness — context disambiguates.)

**Token** — The unit a model actually reads, roughly ¾ of an English word. All cost, speed and limit figures are denominated in these.

**Context window** — The maximum tokens a model can consider at once, covering prompt, history, retrieved documents and the answer together. A capacity limit, not a promise of attention.

**KV cache** — Stored key/value vectors for tokens already processed, so they aren't recomputed each step. Grows with context length, and is usually what exhausts memory locally. Prompt caching is this, sold as a feature.

**Prefill / decode** — Processing the prompt (parallel, fast) versus generating the answer one token at a time (sequential, slower). Quoted tok/s almost always means decode.

**Speculative decoding** — A small draft model proposes several tokens; the target model verifies them all in a single forward pass and keeps the run up to the first disagreement. With the standard acceptance rule the output distribution is identical to the target model's, so it costs no quality — unlike quantisation, pruning or distillation. It buys latency by spending spare compute, so the win is large at batch size one and small on a compute-saturated server.

**Draft model** — The small, cheap model that proposes tokens in speculative decoding. It never decides anything: every proposal is checked against the target model before it survives.

**Acceptance rate** — How often the draft model's proposals survive verification. It sets the speedup, which is why predictable text speculates well and genuinely surprising text does not.

**Prompt lookup / n-gram speculation** — Speculative decoding that drafts by copying from the prompt instead of running a second model. Nearly free, and effective on work with heavy quoting — editing, summarising with quotations, rewriting code in place.

**Weights / parameters** — The numbers that constitute a trained model. "7B" means seven billion of them.

**Quantization** — Storing each weight in fewer bits (4, 5, 8) instead of 16. Shrinks and speeds up the model at a small cost in precision.

**Q4_K_M** — Four-bit K-quant, medium size. The usual local default. Q = quantized, 4 = bits, K = k-quant method, M = medium.

**GGUF (*.gguf)** — The self-contained file format holding quantized weights plus tokenizer and metadata. What llama.cpp and Ollama consume.

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

**min-p** — Keep only tokens above a fraction of the top token's probability, so the cutoff moves with the model's confidence. A newer open-weights control, increasingly preferred over top-p in local serving; hosted APIs generally do not expose it.

**Greedy decoding** — Always taking the highest-probability token. What temperature 0 does, under the name you will meet in papers.

**Beam search** — Keeping several candidate continuations alive and scoring whole sequences. Right for machine translation, bland for open-ended generation, and rarely used with modern LLMs — worth recognising in older material.

**Stop sequence** — A string that ends generation the moment it appears, normally without being returned. It truncates output; it does not prevent the model from generating it, and it fires inside legitimate content too.

**Log probability (logprobs)** — The probability a model assigned to each token it chose, returned by some providers. A confidence signal that does not rely on the model's self-report, but it describes one token given its prefix, not the truth of the claim. The Anthropic Messages API does not expose them.

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

**Cold start** — Time before a system can serve any request: loading weights, allocating the cache, warming the runtime. Distinct from a cache miss, and fixed by keeping something warm rather than making it faster.

**Warm states** — Fully cold (nothing loaded), model-warm/cache-cold (the common case), fully warm (new tokens only), and evicted (was warm, silently is not any more).

**Cache prefix rule** — Prompt caching keys on an exact unchanged prefix. Anything variable — a timestamp, a session id — must go last, or the hit rate silently goes to zero.

**Queueing knee** — Below capacity, latency is roughly flat as load rises; past it, queue time grows without limit and p95 detaches from p50 sharply. Load-testing at 60% tells you little about 95%.

**Session decay** — Long sessions degrade because early mistakes stay in history, get re-read each turn, and are treated as established fact. Restarting with a short accurate summary usually beats fighting it.

**Compaction loss** — What a summary dropped is invisible to the agent, so it carries on confidently with a thinner picture. Constraints that must survive belong in the system prompt or a file.

**Rung** — One configuration in an ordered ladder of increasing assistance (bare, test-first, reloop, guards-off, decomposed, oracle). Where a task starts passing is the diagnosis.

**Oracle rung** — The control at the top of a ladder, supplying most of the answer. Failing there means the fixture is broken rather than the agent.

**Prefix caching** — A serving engine reusing already-computed keys and values when a new request begins with a prefix it has seen. Automatic and unbilled — you do not mark anything, which is why a second identical request is often faster with no code change. See [[prompt-caching]] for the same mechanism sold as a product.

**Read accumulation** — Tool results staying in the transcript and being re-sent every turn. A single large read early in a run is paid for on every turn after it.

**Verification granularity** — Whether you check after every edit, after a logical unit, or once at the end. Decides whether feedback names the cause or only the symptom. Per-edit checking breaks on changes that are atomic across files.

**Chatbot** — Model in, text out, no actions. It cannot affect the world, which makes it safe by construction and limited by the same fact.

**Workflow** — Fixed steps you decided, with the model filling gaps inside them. Predictable and auditable, because the sequence is not the model's to choose.

**Agent** — A system where the model chooses which tool to use, in what order, and when to stop. Flexible, and the flexibility is exactly what makes it dangerous.

**Supervised learning** — Learning from labelled examples: here is an input, here is the right answer. Most of classical machine learning.

**Unsupervised learning** — Finding structure without labels, as in clustering or embeddings. Nobody said what the groups are, so nobody can tell you the answer is wrong.

**Reinforcement learning** — Learning from consequences rather than answers. No correct output is given, only a signal about whether an outcome was good.

**Human in the loop** — The action waits for a person to approve it. Slowest and safest, and correct for anything irreversible or outward-facing.

**Human on the loop** — The action proceeds while a person watches and can stop it. Requires real observability, or the watching is decorative.

**Human out of the loop** — Nobody watching. Appropriate only where actions are reversible, bounded and logged.

**Least privilege** — Starting an integration read-only and widening only for the task in hand, then narrowing again. Production is the last thing you connect, never the first.

**Scoped credentials** — Access to what the task needs rather than to the whole account. A repository connection does not need every repository.

**Sandboxing** — Running agent-executed code somewhere it cannot reach anything that matters. Containers, not promises.

**Bounded loop** — Turn and cost ceilings plus repetition detection, so a loop cannot spin silently until somebody notices the bill.

**Action log** — A record of what an agent did, in order, with arguments and results. You cannot investigate what you did not record, and this is where an injection shows up.

**Tool** — A single capability with a schema: one function the agent can invoke. The unit of what an agent is able to do.

**Resources** — Things a Model Context Protocol server offers for reading rather than invoking — files, records, documents, addressed by URI.

**Prompts (MCP)** — Named, reusable prompt templates a server offers its clients, as distinct from tools it offers to call.

**Sampling (MCP)** — A server asking its client to run an inference on its behalf, so the server needs no API key or model choice of its own.

**Roots** — A server asking its client where it is allowed to operate, so it can discover its sandbox rather than assume one.

**Elicitation** — A server asking the user for a missing parameter mid-operation, instead of failing or inventing a value.

**stdio** — A Model Context Protocol transport where the client launches the server as a subprocess and talks over standard input and output. Nothing listens on a port, which removes a class of attacks outright.

**Streamable HTTP** — The network transport for Model Context Protocol servers that are shared, remote, or need to outlive a client session. It brings the usual network exposure with it.

**Local server compromise** — The commonest Model Context Protocol threat: a server is a binary running on your machine with your client's privileges. Installing one is a trust decision, not a configuration step.

**Session hijacking** — A guessed or stolen session identifier used to impersonate a client on an HTTP transport, or to inject into its stream.

**Deterministic grading** — Scoring by something that cannot be argued with: it compiles, the tests pass, the schema validates. Cheap and trustworthy, so use it wherever the task allows.

**Reference match** — Scoring against a known-good answer, exactly or fuzzily. Brittle whenever many different answers would be correct.

**One-shot** — Giving a single example in the prompt. Frequently enough to pin down output format, which is often the actual problem.

**Zero-shot chain-of-thought** — Asking the model to think step by step with no examples. One line, and a real improvement on reasoning tasks.

**Few-shot chain-of-thought** — Examples that show the working rather than only the answers, to demonstrate the reasoning style you want.

**Presence penalty** — A flat penalty applied to any token that has already appeared, regardless of how often. Pushes a model toward new material rather than what it has already said.

**Frequency penalty** — A penalty that scales with how many times a token has appeared, discouraging overuse rather than reuse. Presence asks whether a token has appeared; frequency asks how often.

**repetition_penalty** — The open-weights formulation of the same idea, a multiplicative penalty on the logits of seen tokens. Same intent as the two above, different arithmetic, not interchangeable with them.

**Logit bias** — An adjustment added to named tokens' logits before sampling, forbidding or forcing specific tokens rather than shaping the whole distribution. Surgical, and tokenizer-specific: you are naming tokens rather than words, so banning one spelling leaves the model free to reach the same idea another way — and a bias table stops meaning anything when the model is swapped.

**Constrained decoding** — Restricting generation so that invalid output cannot be produced at all: at each step the tokens that would break the required format are given zero probability before a token is drawn. The strongest rung of the structured-output ladder, because non-compliance is unrepresentable rather than merely discouraged.

**Grammar** — The set of strings that count as valid, written formally. Backus-Naur Form and its variants are the usual notation, and llama.cpp's GBNF is one of them. A JSON Schema compiles to one; a regular expression is a small one.

**GBNF** — GGML Backus-Naur Form, the grammar notation llama.cpp accepts for constrained decoding. Naming it matters because a grammar is only usable by the serving stack that parses that notation.

**Masking at sampling time** — Setting the probability of illegal tokens to zero before sampling, which is where a constrained decoder's guarantee comes from. The distinction that matters: the failure is not made unlikely, it is made impossible.

**Tokenizer reconciliation** — Working out which tokens are consistent with which grammar states, because grammars are written over characters and sampling happens over tokens. The same mismatch that makes logit bias frustrating, one layer up and solved properly.

**Per-step masking overhead** — The cost of computing the legal token set at every decoding step. Usually worth paying, and worth measuring rather than assuming, particularly with a large grammar.

**Reasoning model** — A model trained to produce an extended internal chain before its visible answer. That chain costs output tokens, which is why budgets sized for an answer alone return nothing.

**Undersampling** — Discarding majority-class rows to balance a dataset. Fast, and it throws away real data, which is reasonable only when the majority class is enormous.

**Threshold tuning** — Moving the decision cut-off rather than changing the model. Frequently the most effective option available and the most often skipped.

**Response distillation** — Generating answers with a teacher model and fine-tuning a student on them. The simplest form and the usual starting point.

**Logit distillation** — Training the student to match the teacher's full output distribution rather than its final answers. The classical form, and it needs access to raw outputs.

**Rationale distillation** — Having the student learn the teacher's reasoning as well as its conclusions. Effective where the reasoning is the hard part.

**Task-specific distillation** — Distilling for one narrow job, which is where the wins are largest: a small student can match a frontier teacher on a single well-defined task.

**Verifier-guided retry** — Generate, run the tests, feed the failures back. The strongest inference-time loop, because the verifier is ground truth rather than an opinion.

**Context distillation** — Distillation where teacher and student are the same model, differing only in what they have been handed: the teacher has a long document in its context, the student has a small trained cache standing in for it. The student learns to answer as though it had read something it never sees at inference.

**Pruning (neural)** — Removing parts of a trained network outright: whole layers (depth) or neurons and attention heads within layers (width). Distinct from the decision-tree sense used in Block 0 — and usually followed by a distillation pass to recover the capability the cut cost.

**Distillation flywheel** — A large model generating training data for a smaller one, round after round. The teacher is the external signal that keeps it from collapsing.

**Held-out evaluation** — A set the training loop cannot see. If the loop can read the set that judges it, it will optimise the set rather than the task.

**Diversity monitoring** — Tracking the variety of outputs across generations, not just their quality. Model collapse shows up in the tails first, where nobody is looking.

**Queueing** — Time spent waiting for a slot rather than doing work. Invisible until you measure it, and past saturation it dominates latency entirely.

**Batching** — Grouping requests so hardware is used efficiently. Raises total throughput and can raise the latency of any individual request.

**Conversation history** — The default form of agent memory: everything re-sent every turn. Simple, and it grows without limit until something manages it.

**External notes** — Memory an agent writes to a file and reads back. It survives resets because it was never in the context to begin with, which makes it the most durable kind.

**Instruction file** — A markdown file at the project root, read by an agent at startup: `AGENTS.md` as the cross-tool convention, `CLAUDE.md` and others as tool-specific names. Authored rather than learned — it is static, and it is loaded in full whether or not the task needs it, so every line is spent from every session's context budget.

**AGENTS.md** — The cross-tool instruction-file convention. Plain markdown, no required fields and no schema; used by 60,000+ open-source projects across 30+ tools, and stewarded by the Agentic AI Foundation under the Linux Foundation. Not a memory system: it does not learn or update itself.

**Notes or memory directory** — Accumulated written memory, typically one fact per file, searched rather than read in full. The retrieval half of written memory, where the instruction file is the preloading half.

**Linked notes (markdown wiki)** — A notes directory whose entries cross-reference each other, so recall is a few small reads along a thread rather than one large one. What keeps an accumulating store usable past a few dozen entries.

**Task or state file** — The plan and statuses for the current piece of work. Distinct from accumulated memory in being disposable: it belongs to this run and is meant to be discarded after.

**Memory write policy** — The rule deciding what gets persisted: the model's own judgement (cheap, drifts), a fixed category rule (predictable, misses things), or human confirmation (accurate, does not scale). The hard problem in a memory system, and usually the unspecified one.

**Consolidation** — A periodic pass over a memory store to merge duplicates, resolve contradictions and delete what has died. Without it a store only grows, and growth alone degrades it.

**Memory poisoning** — Indirect prompt injection that reaches persistent memory, so it is reloaded into later sessions that never saw the original content. It defeats restarting, because the restart reloads the store, and it defeats trace review, because the harmful action happens in a different session from the read that caused it.

**Memory scoping** — Confining a memory store to the user or project it was written for. Memory written serving one user loading into a session serving another is a leak in the ordinary case and a delivery mechanism in the adversarial one.

**Memory staleness** — A written memory records what was true when written. Once wrong it is worse than absent, because absence prompts a look while a stale note prompts confident action on something that no longer exists. Date entries; verify anything naming a file or flag before acting.

**Retrieved memory** — Facts stored and fetched when relevant, by semantic search over past interactions. Powerful, and it means you now have a retrieval quality problem as well.

**Arithmetic intensity** — Operations performed per byte fetched from main memory. A property of the work rather than the chip, and the number that decides whether the arithmetic units are the constraint or are sitting idle waiting on memory.

**Break-even intensity** — A chip's peak arithmetic rate divided by its memory bandwidth, in operations per byte. Work above the line is compute-bound, work below it is memory-bound, and token generation sits roughly two orders of magnitude below.

**High-bandwidth memory (HBM)** — The off-die memory where model weights live, around 300 times slower to reach than a register. Every byte the arithmetic units consume crosses this gap, which is why inference is usually a data-movement problem.

**Shared memory (L1)** — On-chip scratchpad memory, roughly 100KB per unit, that you control directly. The lever behind kernel fusion and FlashAttention: work done here never crosses to main memory.

**L2 cache** — Memory shared across the whole chip, tens of megabytes, managed by hardware rather than by you. You influence it only through access patterns.

**Registers** — Per-thread storage holding a value while it is being operated on. Effectively instant, and the top of the memory hierarchy.

**Warp** — The fixed group of thirty-two threads that execute one instruction together. Threads within a warp taking different branches idle each other; different warps taking different paths cost nothing.

**Occupancy** — How much work a unit keeps resident relative to what it can execute at once. High occupancy is what hides memory latency: when one warp stalls, the scheduler switches to another in a single clock cycle.

**Kernel fusion** — Combining chained operations so intermediate values stay on-chip. Three elementwise operations become one round trip to main memory instead of three.

**Shared-memory tiling** — Loading a block of data into on-chip memory and doing many operations on it before writing back. FlashAttention is the well-known case, keeping the attention matrix out of main memory entirely.

**Dispatch overhead** — The fixed cost of launching each operation on the device. A workload of very many tiny operations can be limited by this alone, rather than by memory or arithmetic.

---

## Block 0 · Orientation

**AI ⊃ ML ⊃ Deep learning ⊃ Generative AI** — They nest, they aren't alternatives. AI is any system doing something intelligent; ML learns from data instead of rules; deep learning is many-layered neural networks that learn their own features; generative AI produces content rather than a label.

**Agentic AI** — Deliberately outside that nesting: an architecture, not a model type. A loop that lets a model choose actions and use tools.

**Artificial intelligence** — The whole field: any system doing something that looks intelligent. A 1997 chess engine counts, which is why the term tells you almost nothing on its own.

**Machine learning** — Systems given examples rather than rules, which infer the rules themselves. Everything in Block 2 lives here.

**Deep learning** — Neural networks with many layers, which learn their own features instead of being handed them. Needs more data and more compute, and wins decisively when both are available.

**Generative AI** — Models that produce content — text, images, audio — rather than a label or a number. A spam classifier is machine learning but not generative.

**Feed-forward network** — The part of a transformer layer that processes each token on its own, with no reference to its neighbours. Typically two-thirds of all parameters, so most of a model's size is here rather than in attention.

**Residual connection** — Adding a layer's input back onto its output. This is what lets signal and gradients travel through eighty layers without degrading; without it, deep networks do not train.

**Layer normalisation** — Rescaling the numbers flowing through a layer to keep them in a workable range. Unglamorous, and training is unstable without it.

**config.json** — A model's architecture blueprint: layer count, hidden size, attention heads, vocabulary size, context length.

**tokenizer.json** — The vocabulary, which must match the weights exactly. Mismatch it and the model emits fluent nonsense, which is a classic and baffling bug.

**safetensors (*.safetensors)** — The learned weights at full precision, in a format that cannot execute code on load. What fine-tuning modifies.

**chat template** — How system, user and assistant turns get formatted into the single string a model actually sees. Get it wrong and quality drops for reasons that look like the model being bad.

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

**Stochastic gradient descent (SGD)** — Updating the weights from one example, or a small batch, at a time rather than the whole dataset. Fast and noisy, and the noise sometimes helps escape a bad minimum.

**Activations** — The intermediate values kept from the forward pass so backpropagation can use them. They scale with batch size and sequence length, and they are the knob you actually turn when you run out of memory.

**Loss curve** — Training loss plotted against steps, read as a diagnostic rather than a score. Falling then flattening is healthy; flat from step one is a wiring bug, not a learning-rate problem; training falling while validation rises is overfitting.

**Log-odds** — What a logistic regression's coefficients are expressed in, not probabilities. A coefficient of 0.7 is not 70% — exponentiate it for an odds ratio of about 2.0, meaning the odds roughly double.

**Variance reduction** — The splitting criterion for regression trees: choose the split that most reduces variance within each resulting group. The regression counterpart to Gini impurity.

**n_estimators** — How many trees an ensemble builds. In a random forest more is safe and converges; in gradient boosting more is dangerous past the optimum, which is why early stopping is mandatory for one and optional for the other.

**learning_rate (boosting)** — How much each tree contributes. Lower means you need more trees and generalise better; 0.05 with early stopping is a reliable starting point.

**max_depth (boosting)** — How deep each tree may go, kept to roughly 3 to 6. The ensemble supplies the complexity, so deep individual trees overfit quickly.

**subsample / colsample** — Sampling rows and columns per tree in boosting. Randomness regularises here for the same reason it helps a forest.

**Elbow method** — Plotting within-cluster variance against k and looking for the bend. Real data frequently has no visible elbow, at which point the method has told you nothing.

**Silhouette score** — How well each point fits its own cluster against the next-nearest, from -1 to 1. More decisive than the elbow method and slower.

**Mixture of experts (MoE)** — An architecture that replaces each block's feed-forward network with several smaller ones and activates only a few per token. Capacity grows without arithmetic growing with it — but every expert stays resident in memory, so the saving lands on compute rather than on the bytes that limit generation.

**Expert** — One of the small feed-forward networks in a mixture-of-experts block. What each becomes good at emerges during training and is generally not interpretable.

**Router (MoE)** — The learned classifier that scores every expert per token and keeps the top few. Trained alongside the network, so routing quality is something a model can get wrong.

**Active versus total parameters** — Total is what you must hold in memory; active is roughly what decides token speed. A mixture-of-experts model quotes both, and a specification giving only one is answering half the question.

**Expert load imbalance** — Some experts receiving far more tokens than others during training, leaving the rest undertrained. Managed with a per-expert capacity limit that overflows surplus tokens to the next best choice.

**Multi-head attention (MHA)** — The original form, where every head keeps its own keys and values. Most expressive, and the largest KV cache.

**Multi-query attention (MQA)** — Every query head sharing a single key-value head. The smallest possible cache and the largest quality concession of the three, which is why the grouped compromise is more common.

**Grouped-query attention (GQA)** — Heads sharing key and value projections in groups. The current default, because it cuts the KV cache substantially at little cost in quality.

**Scaled dot-product attention** — The operation's full name. Scores are divided by the square root of the key dimension before the softmax; without that division the scores grow with dimension, the softmax saturates and gradients vanish.

**Softmax (in attention)** — What turns raw scores into weights that are positive and sum to one, so attention distributes a fixed budget rather than adding more of it.

**FlashAttention** — An exact attention algorithm that never materialises the n-by-n score matrix in main memory, working in tiles inside fast on-chip memory and recomputing rather than storing. Same numbers as standard attention; the speed is entirely from moving fewer bytes, which is why it needs no quality re-check when the other variants do.

**Self-attention vs cross-attention** — In self-attention the queries, keys and values come from one sequence. In cross-attention the queries come from one and the keys and values from another, which is how a text model reads an image encoder's output. Identical arithmetic, different sources.

**Linear attention** — Approximating the softmax so the computation reorders into something linear in sequence length. Trades exactness for scaling, unlike FlashAttention which trades nothing.

**State-space model (SSM)** — An alternative to attention carrying a fixed-size recurrent state, designed so training still parallelises — the thing older recurrent architectures could not do. Mamba is the best-known.

**Causal masking** — Preventing a token from attending to tokens after it. Not a variant but a requirement: during generation the future does not exist yet.

**Product quantization** — Compressing the stored vectors themselves rather than the search over them. Often paired with an inverted file index to cut memory dramatically — quantization again, a different object.

**ef_construction** — How much effort an HNSW index spends while being built. You pay it once, so be generous.

**ef_search** — How many candidates the index examines per query. The dial you tune live: raise it for recall and pay in latency, and move it first when recall disappoints.

**Term frequency** — How often a word appears in a document, as a relevance signal. Not linear — ten mentions are not ten times more relevant, which is why BM25 saturates it.

**Inverse document frequency** — Weighting terms by how rare they are across the corpus. A document matching "gearbox" tells you far more than one matching "the".

**Length normalisation** — Discounting matches in long documents, which contain most words by accident. Tuned so that length neither helps nor hurts more than it should.

**Target leakage** — A feature that encodes the answer, such as predicting churn from a cancellation date. The model scores brilliantly in testing and is worthless in production.

**Train-test contamination** — The same rows appearing in both splits: duplicates, near-duplicates, or one customer under two identifiers. Very common in scraped or merged data.

**Preprocessing leakage** — Fitting a scaler or imputer before splitting, so the training set has seen the test set's statistics. The reason a pipeline is fitted inside cross-validation rather than before it.

**Temporal leakage** — Training on the future by splitting time-ordered data at random. The model learns from events that happen after the ones it is predicting.

**Group leakage** — Related rows split across train and test: several readings from one turbine, several notes on one patient. The model recognises the group rather than the pattern.

**Tuning against the test set** — Leakage by repetition. Every time you read the test score and change something, a little of that set moves into your model, and the number stops being an estimate of anything.

---

## Block 1 · Python, Data & EDA

**dtype** — The type pandas inferred for a column. A numeric-looking column typed `object` means something non-numeric is in it. Free diagnostic; read it every time.

**Sentinel value** — A placeholder written instead of a null: 9999, -1, 1900-01-01. Missing data in disguise, and it silently pollutes every statistic.

**MCAR / MAR / MNAR** — The three missingness mechanisms. Completely at random (filling is safe); at random given other columns (fill using them); not at random (filling introduces bias).

**Missingness indicator** — A binary column recording that a value was absent, added before imputing. Preserves signal that imputation would destroy.

**Stratified split** — Splitting while preserving class balance in both halves. Necessary whenever a class is rare.

**Pipeline** — Chained preprocessing plus model, fitted on training data only. Makes leakage structurally difficult, including inside cross-validation.

**Threshold table** — Recall, precision, missed cases and false alarms across candidate cut-offs. More useful than any single score, because it converts a model into a business decision.

**int64 / float64** — Pandas numeric types. A column with any missing value becomes float, because NaN is a float — so an integer column silently turning float is a missingness signal.

**object** — The pandas catch-all, usually strings. It is also what a mixed-type column becomes, which is why an unexpected object column is worth investigating rather than casting away.

**category** — A pandas type for repeated labels. Far cheaper in memory than object for low-cardinality columns, and it makes the intended set of values explicit.

**datetime64** — Real dates, and only if you asked for them. Dates left as strings sort alphabetically, which puts 2026-01 before 2025-12 and produces a wrong answer that looks fine.

**Recorded outcome** — A label that is simply what happened: the turbine failed, the invoice was paid late. Usually the best labels available, and the cheapest.

**Human annotation** — A label somebody judged. Accurate, expensive, and only as consistent as the guidelines — which is where most label-quality problems originate.

**Weak supervision** — Labels generated by rules rather than people. Fast and cheap at volume, and it bakes the rule's blind spots into the training data permanently.

**Implicit label** — A label inferred from behaviour: a click as relevance, a return as dissatisfaction. Abundant, and biased by the interface, because you only observe what the interface let people do.

**Model-generated label** — A label another model assigned. Cheap at scale, and it inherits the teacher's errors confidently rather than visibly.

**Silently wrong logic** — Code that runs and returns the wrong answer: a group-by on the wrong key, a merge that drops rows, an off-by-one on a date window. The dangerous failure mode when using an assistant on data work, because nothing errors.

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

**Class weights** — Making errors on the rare class cost more during training. Without them a model on imbalanced data learns to predict the majority and calls it accuracy.

**Keras** — A high-level neural-network application programming interface for conventional architectures and training loops. Less code and fewer bugs when the training loop is not the interesting part.

**PyTorch** — The lower-level framework for custom losses, unusual training schedules and nearly all published research code. Keras running on the PyTorch backend gives you both, and is a good default.

---

## Block 3 · Retrieval and Agentic RAG

**Knowledge graph** — Entities stored as nodes and their relationships as edges, extracted from a corpus ahead of time. Turns a multi-hop question from a search into a traversal: deterministic, repeatable, and answerable without the model holding intermediate results.

**GraphRAG** — Retrieval that queries a knowledge graph rather than, or alongside, a vector index. It moves the work from query time to build time, which is the entire trade — cheap per question, expensive to build and to keep current.

**Entity extraction** — The pipeline step that reads a corpus and decides what the entities and relationships are, usually with a model. Its quality is the whole system: a wrong edge is reused by every question that walks through it, and is invisible at query time because the traversal works perfectly on bad data.

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

**Read time (prefill)** — How long the model takes to process everything retrieval handed it, before the first output token appears. Usually seconds where retrieval is milliseconds, and it is what the user experiences as the delay.

**Preloading** — Reading a corpus before any query arrives and keeping the result, so requests skip straight to answering. Only valid for knowledge that is stable across queries; anything changing per request is still fetched at request time.

**Naive preload** — Reading the whole corpus once and storing the resulting cache. The simplest preloading approach, also called cache-augmented generation, and bounded by whether the corpus fits the context.

**Modular preload** — Reading each passage separately so it can be assembled in any order. Buys the order-independence a prefix cache cannot offer, and costs either recomputation at request time or a change to the model.

**Compressed preload** — Shrinking the stored cache before saving it. Carries a requirement most compression methods fail: it happens before any query exists, so it cannot be guided by what was asked.

**Trained preload** — A small set of trained vectors taught to behave as though the corpus were present, produced by a training run rather than copied from a read. Requires the corpus to be stable enough to justify the run.

**Attention sink** — The disproportionate attention models place on the first token of a sequence. Concatenating separately-read blocks gives the model several of them instead of one, which is part of why naive concatenation fails.

**Query transformation** — Changing the question before retrieval rather than tuning what retrieves it. The only stage of a retrieval pipeline that touches the request instead of the corpus, and the only one that adds a model call in front of the cheap stage.

**Hypothetical document embedding (HyDE)** — Having the model draft the answer it expects, then retrieving with that draft's vector rather than the question's. It matches answer against answer, which suits the space better than matching a question against answers — and a confidently wrong draft steers retrieval confidently wrong.

**Query rewriting** — Resolving what a question assumed from earlier turns so it stands alone before retrieval. Essential on conversational interfaces, where a follow-up carries almost none of its meaning in its own words.

**Query expansion** — Generating several phrasings of one question, retrieving for each, and fusing the ranked lists. Reciprocal rank fusion applied across queries rather than across retrieval methods.

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

**Prompt caching** — Prefix caching exposed as a billable feature: you mark where the stable part of the prompt ends, entries expire, and writes and reads are priced differently. Reads cost about a tenth of normal input; writes cost 1.25× at the five-minute lifetime and 2× at the one-hour one, so a prefix reused twice roughly breaks even and one reused fifty times is a large win.

**Exact-match response cache** — Returning a stored answer when a request is byte-identical to an earlier one. It saves output tokens as a semantic cache does, and carries none of the false-positive risk because it does no similarity matching — worth measuring your byte-identical repeat rate before reaching for embeddings.

**Hardware caches** — Registers, shared memory, and the L1 and L2 caches: the memory ladder the chip manages for you. Automatic, never addressed by name in your code, and influenced only through access patterns — a different sense of the word from every other cache in this course.

**Semantic caching** — Answering from a store of previous responses when an incoming question embeds close enough to an earlier one, without calling the model at all. Unrelated to the other three caches despite the name: it reuses answers rather than arithmetic, so a near-miss returns a confident answer to a question nobody asked.

**Rubric** — A set of scoring dimensions, each with observable criteria per level and an anchor example, replacing a single score. The test of one is that two careful readers apply it to the same output and agree; if they do not, it describes nothing.

**Anchor example** — A real output kept alongside a rubric to show what each level looks like. What makes a standard transferable to a second reader, a second model, or yourself in three months.

**Blind read** — Judging output without knowing its provenance: which model produced it, and whether it is the treatment or the control. Expectation is a measurable bias pointing toward whatever you hoped for, and it applies to people at least as strongly as to models.

**Blinding the calibration set** — Hand-labelling ground truth without knowing which system produced each answer. Skipped often, and skipping it makes the reported agreement rate a measure of how well the judge reproduces your expectations rather than your judgement.

**Paired data** — Two sets of measurements where each value in one has a natural partner in the other: the same question scored under two systems, the same code before and after a change. An eval on a fixed set is paired by construction; an A/B test on live traffic is not, because no user appears in both arms.

**Paired test** — A comparison that works on the per-item differences rather than on two separate groups. It cancels whatever the pair shares — usually question difficulty, which is often the largest source of variance — and using an unpaired test on paired data can take a real effect from almost always detected to almost never.

**Bessel's correction** — Dividing a sample variance by n − 1 rather than n. The mean was fitted to the same data, so deviations from it are systematically too small; subtracting one accounts for the degree of freedom that fitting spent. Invisible at large samples and worth about a tenth of the variance at eval-sized ones.

**Per-arm distribution** — Reporting the spread and shape of each arm rather than a difference in means. A change that helps most cases and badly harms a few moves the mean upward and hides the tail that should stop the release.

**Peeking** — Repeatedly testing a running experiment and stopping when it crosses the threshold. Every look is another chance for noise to cross, which inflates the false-positive rate far past the nominal one.

**Trajectory evaluation** — Scoring an agent's whole sequence of turns rather than its final answer. A correct ending can follow a wasteful or lucky run, and a wrong one can follow sound reasoning that hit a broken tool; only the sequence distinguishes them.

**Recovery** — Whether an agent notices a failure and adapts. A run that failed a tool call, read the error and tried something sensible is better than one that succeeded by luck, and a final-answer score ranks them the other way round.

**Guardrail metric** — A measure that must not get worse, checked alongside the primary metric but not permitted to declare success. Latency, cost and refusal rate are the usual ones.

**Agreement rate** — How often a judge matches a blind human label on a calibration set. A judge score published without one is an opinion with a decimal point.

**Similarity threshold** — The cut-off a semantic cache uses to decide two questions are the same one. Measured on this course's own encoder, a negation that reverses the answer scores 0.984 while a genuine paraphrase scores 0.940, so no cut-off separates them — see <code>scripts/measure_semantic_threshold.py</code>.

**Cache hit rate** — The fraction of calls that actually reused a cached prefix. Nothing errors on a miss, so a cache that quietly stopped working looks exactly like never having had one, except on the bill.

**Truncate on ingest** — Capping each tool result as it enters the context. One line of code, and it prevents a single large file read from dominating the window for the rest of the run.

**Summarise as you go** — Replacing a read with a short statement of what was learned. Preserves the finding and drops the bulk, but is lossy in a way the agent cannot see.

**Drop after use** — Clearing old tool results once the work derived from them is done. The safest form of compaction, because a read that has already produced an edit is rarely needed verbatim again.

**Retrospective justification** — An architecture decision record written after the fact to legitimise a choice already made. It reads like a decision and records none.

**Consequence amnesia** — An architecture decision record whose consequences section is empty or optimistic. That section is where it states what it is giving up, and without it the record cannot be revisited honestly.

**Status theatre** — Writing a decision record for every change, so none of them are signal. If it does not forbid anything, it is not a decision.

**Outcome honesty** — Whether your fixture can tell success from inaction. At the starting state the check must fail, and with a known-good change it must pass — otherwise every number downstream is noise.

**Process honesty** — Whether the harness recorded what actually happened: the model's reasoning, its tool arguments, and why the run stopped. Without it you cannot tell "never attempted" from "attempted and failed".

**SWE-bench** — A benchmark of 2,294 real GitHub issues across twelve Python repositories, scored by whether the agent's patch makes the project's own tests pass.

**SWE-bench Lite** — A 300-instance subset filtered toward self-contained problems. Cheaper to run and easier, so its scores are not comparable to the full set.

**SWE-bench Verified** — A 500-instance subset human-validated to remove tasks that were underspecified or impossible. The variant most quoted, and the fairest.

**FAIL_TO_PASS** — The tests that must start passing for a fix to count, drawn from the real pull request. They fail at the base commit and pass afterwards.

**PASS_TO_PASS** — The tests that must keep passing. This is what stops "delete the failing test" from scoring as a solution.

**Position bias** — A judge's verdict changing when the same two answers are presented in the opposite order. The reason every pairwise comparison is run both ways.

**Verbosity bias** — A judge rewarding length beyond the point where length helps. Dangerous when the systems being compared differ in how much they say.

**Self-preference** — Models favouring their own generations. The reason a judge should come from a different family than the system under test, and never be the model under test.

**Score compression** — Absolute one-to-ten scoring clustering everything into a seven or an eight. Pairwise comparison discriminates far better.

**Judge calibration** — Hand-labelling thirty to fifty items once and measuring how often the judge agrees. The step nobody does, and without it a judge score is an opinion with a decimal point.

**Acceptance criteria** — Checkable conditions for done, not aspirations. "Fast" is not one; "p95 under 400ms on the existing fixture set" is.

**Non-goals** — What a piece of work explicitly does not do. The highest-value section of any spec and the most often missing, because it is what stops scope creep being invisible.

**Bare (rung)** — The bottom rung of an agent experiment: the task and nothing else, no scaffolding or hints. If it passes here, everything above it is unnecessary.

**Test-first (rung)** — The failing test supplied in context, giving the agent a checkable target. Passing here and not below means it needed the target, not more capability.

**Reloop (rung)** — Failures fed back with a retry allowed. Passing here means it could not get it right first time but could correct itself.

**Guards-off (rung)** — Budgets and limits relaxed. Passing here means capability was never the problem — your harness was stopping it.

**Decomposed (rung)** — The task pre-split into steps. Passing here means the model could do each part and not the planning.

**Oracle (rung)** — The answer, or most of it, supplied. This is the control: failing here means the fixture or the rubric is broken, not the model.

**Branching** — Conditional edges routing by task type, instead of a growing thicket of if-statements inside one function.

**Parallelism** — Independent nodes running together, so two retrievals that do not depend on each other cost one node's worth of wall clock rather than two.

**Inspectability** — Being able to read what the state was at every step of a run that finished yesterday. The trajectory log the telemetry lesson asks for, produced by construction rather than by discipline.

**MCP server** — A connection to a system outside your codebase, spoken in a standard protocol so any client can use it. Installing one grants it your client's privileges, so treat it like adding a dependency.

---

## Block 5 · Evaluation

**Prediction interval** — The range a single new observation is likely to fall in. Always wider than a confidence interval, because it carries the spread of the data as well as the uncertainty in the estimate — and it is the one that answers a per-case question.

**Confidence interval vs prediction interval** — The first is about the mean, the second about the next case. As the sample grows the confidence interval shrinks towards nothing while the prediction interval converges on the real spread and stays wide.

**Learning curve** — Score plotted against the fraction of training data used. Turns "we need more data" from an assumption into a measurement: a flat validation curve means more of the same data will not help.

**Double descent** — Past the capacity where a model can fit the training data exactly, test error peaks and then falls again. Why very large models generalise with far more parameters than data points, in apparent defiance of the classical U-curve.

**Correct by construction** — A gold label you know is right because you planted the fact it depends on, rather than because you trust whoever annotated it. The only kind of label you can debug.

**Derivable** — A label that follows from applying the written rules to the written case, not merely one you believe is right. If a label is not derivable, no amount of model capability will reach it, and scoring against it measures your opinions.

**Under-determined label** — One where two answers are equally defensible under the rules you wrote. The label is encoding a preference you never recorded, so either add the rule that distinguishes them or accept both.

**Self-contradicting rules** — A general clause that quietly forbids what a specific label requires, usually an escalation rule. The system obeys the general clause and is marked wrong for obeying it.

**Output budget** — The cap on tokens a model may generate. On a reasoning model this covers the thinking and the answer together, so it must be sized against the model that needs the most rather than the one you developed against.

**Finish reason** — The model's own statement of why it stopped: it completed, it hit the budget, it was cut off. Record it, and a truncated run can never be misread as a failed one.

**Non-completion** — A run that failed for infrastructure reasons — a timeout, a rate limit, a truncation — rather than because the model was wrong. Classify these out of capability scores, or a provider's bad afternoon becomes a permanent verdict about the model.

---

**Decided behaviour** — Behaviour a person chose for a reason that survives being asked about, and that is recoverable later from a specification, decision record or commit message.

**Invented behaviour** — Behaviour that appeared because it was a plausible continuation rather than because anyone weighed it. It may be sensible; nobody can defend it or say what it traded off, which is what makes it unsafe to change.

**Coupling** — How much one part of a system must know about another. Generation makes adding connections nearly free while removing one costs exactly what it always did.

**Cohesion** — How well the things inside one component belong together. Most design guidance reduces to lowering coupling or raising cohesion.

**Interface as a contract** — What a component guarantees to callers, as distinct from how it currently achieves it. Generated code tends to reach through boundaries rather than across them, because the model can see everything and has no stake in what stays stable.

**Technical debt** — A conscious trade: shipping something suboptimal now with the interest understood. Code that is bad because nobody thought about it is not debt, and calling it debt implies a decision that never happened.

**Refactoring under test** — Changing a system's shape without changing its behaviour, where something can actually verify the behaviour is unchanged. Without that, it is rewriting and hoping.

**Legacy code** — Code whose reasoning nobody holds any more, rather than code that is old. On that definition generated code can be legacy the day it merges.

**Comprehension bottleneck** — The consequence of generation multiplying output without multiplying the capacity to understand it. Reading, verifying and safely changing code cost what they always did, and used to be bounded by how fast people could type.

## Block 6 · Security

**Direct injection** — An attempt to override a system's instructions typed by the user themselves. Bounded by what that user was already allowed to do, which is what makes it the less severe of the two forms.

**Indirect injection** — An instruction that arrives inside content the system reads — a document, a tool result, a record field — rather than from the person using it. It borrows the agent's privileges rather than the attacker's, and the attacker need never touch the system; they only need to control something it will read.

**Instruction hardening** — Telling the model in its system prompt to disregard instructions found in content. Free, worth doing, and defeated by a sufficiently determined payload, because it asks the model to police a boundary the input format never carried.

**Input filtering** — Scanning incoming text for attack patterns. Catches the obvious and misses the quiet, and raises confidence faster than it raises safety — most useful logging rather than blocking, as a signal that you are being probed.

**Output constraints** — Limiting what the model may emit: a closed action set, a schema, an enumerated tool list. Stronger than filtering because it depends on the shape of what you accept rather than on the unbounded input.

**Egress control** — Restricting what a sandboxed agent may reach outbound. The half of containerisation people skip: default networking permits arbitrary outbound connections, which is the direction exfiltration uses.

**Tool chaining** — Two individually harmless capabilities that compose into a harmful one — read plus send, fetch plus interpolate. Invisible to a per-tool review, which is why tool sets are audited as sets.

**Attack battery** — A fixed, privately held set of adversarial cases with decided success criteria, run against a baseline. The security counterpart of the eval battery, and it grows to encode your own incidents rather than the field's.

**Exfiltration channel** — Any path by which data in context reaches somewhere the attacker can see: a fetch tool, a written file read back later, a rendered image address, or a trace written to a lower-trust store.

---

## Block 7 · Training and Fine-Tuning

**Mixed precision** — Holding weights and activations in a sixteen-bit format while keeping a full-precision master copy for the update. Roughly halves memory and is usually faster too, since fewer bytes move.

**Loss scaling** — Multiplying the loss before the backward pass so small gradients stay inside the narrow sixteen-bit range, then dividing it out before the update. Without it gradients underflow to zero and training silently stops learning.

**Gradient accumulation** — Running several small batches, summing their gradients and updating once. Arithmetically identical to the large batch it imitates; costs wall-clock time and no accuracy.

**Gradient checkpointing** — Discarding most forward-pass activations and recomputing them during the backward pass. Trades some tens of per cent more time for a large reduction in activation memory.

**Activations (training memory)** — The intermediate forward-pass values the backward pass needs. Unlike weights, gradients and optimiser state, they scale with batch size and sequence length — which is why they are the part you can trade against.

**Focal loss** — A loss reshaped so easy, already-correct examples contribute progressively less, concentrating training on hard minority cases. Where class weights say some rows matter more, this says some rows matter less once the model has them right.

**LoRA (low-rank adaptation)** — Freezing every base weight and learning a small pair of matrices whose product stands in for the update. The saving is not mainly the parameter count: a frozen weight needs no gradient and no optimiser state, and those are what dominate training memory.

**LoRA rank** — The shared narrow dimension of the two adapter matrices, and the capacity of the adaptation. 8–16 suits most format-and-tone work. It is capacity, not quality: raising it on a small dataset buys faster overfitting, not a better result.

**Alpha** — A scaling factor applied to the low-rank product before it is added to the frozen weight. Conventionally one or two times the rank; worth setting deliberately rather than by folklore.

**Target modules** — Which weight matrices receive an adapter, attention projections by default. Often a bigger lever on quality than the rank.

**Adapter** — The trained artefact of a low-rank run, measured in megabytes. Small enough to version, swap per request, and discard when a better base model arrives — which is why fine-tuning stopped being a commitment.

**QLoRA** — Low-rank adaptation over a base quantised to four bits. Precision matters most for weights being updated and the base is frozen, so storing it coarsely brings larger models within reach of a single machine.

**Catastrophic forgetting** — Capability outside the tuned task degrading as a result of tuning. Invisible in the metric you are watching, because that metric is the task that improved; caught only by evaluating slices against the base model.

**Supervised fine-tuning (SFT)** — Training on input/output pairs so the model imitates the targets. Cheap and stable, and bounded above by the quality of the demonstrations you could write.

**Reinforcement fine-tuning (RFT)** — Training by scoring the model's own attempts rather than showing it answers. Can exceed the demonstrations, because nothing is being copied; needs something that can grade.

**Group Relative Policy Optimisation (GRPO)** — Sampling several answers per prompt, scoring them, and moving towards those beating the group average. Dropping the separate value model earlier methods required is much of why reinforcement tuning became affordable.

**Direct Preference Optimisation (DPO)** — Optimising directly on preferred/rejected response pairs without training a separate reward model. Simpler and cheaper than RLHF, and needs preference pairs rather than a verifier.

**RLHF (reinforcement learning from human feedback)** — Humans rank outputs, a reward model learns to predict those rankings, and the policy is optimised against it. The original recipe for turning a base model into an assistant.

**Reward hacking** — A policy optimising the measure rather than the goal: passing the tests by detecting the fixture, producing length when length was a proxy for thoroughness. The default behaviour of an optimiser, not an edge case — and it is invisible in the reward curve by construction.

**Fine-tuning** — Changing a model's weights so it responds differently: tone, structure, schema adherence, a domain's conventions. Good at installing behaviour and poor at installing facts, which is the distinction that decides whether it is the right tool or whether you needed retrieval.

**Low-rank factorisation** — Approximating a large weight matrix as the product of two smaller ones. The fourth member of the compression family, and the one already familiar from LoRA, where the adapter is a low-rank pair standing in for a full-rank update.

**Depth pruning** — Removing whole layers from a trained network.

**Width pruning** — Removing neurons and attention heads from within layers, leaving the layer count unchanged.

**Distillation as repair** — Using a distillation pass to recover capability a pruning cut removed, training the pruned model against the original as teacher. The one place in the compression family where two techniques compose rather than compete.

**Uneven capability loss** — The fact that compression does not remove capability uniformly. What disappears tends to be what was rare — less-represented languages, minority dialects, uncommon domains — so an aggregate score can barely move while a narrow slice degrades badly, which makes compression a fairness question rather than only an efficiency one.

**Slice evaluation** — Measuring per population or per domain rather than in aggregate. The only instrument that can detect uneven capability loss, and the one routinely skipped when compressing a model.

---

## Block 8 · Deployment and APIs

**Experiment tracking** — Recording each run's parameters, metrics and artefacts in a queryable store rather than in notes. The value is comparability across runs you did not plan to compare — which is the question that arrives months later, and the one notes cannot answer.

**Continuous evaluation** — Running the eval battery automatically rather than when someone remembers, tiered by cost: model-free checks on every push, a sampled set per pull request, the full battery before release. A gate that flakes gets disabled, so thresholds must allow for measured run-to-run spread.

**Model provenance** — What a trained artefact records about its own origin: which base, which dataset version, which tracked run, and the evaluation that justified shipping it. Without it a result cannot be reproduced and a rollback has nowhere to go.

**Model rollback** — Reverting to a previous model, which unlike a code rollback requires the old artefact to still exist and still be servable. If it was overwritten in place or depends on a retired base version, the incident becomes an unplanned training run.

**Retraining trigger** — What decides that a model is retrained: a schedule, a drift threshold, a measured performance drop, or accumulated new data. Each fails differently; a performance drop is the signal you want and it needs labels, which arrive late.

**Retraining as deployment** — The discipline that a retrained model is a new model that can be worse, and earns the same shadow, canary and slice checks as any other change. Teams that would not ship code unreviewed routinely promote retrained models automatically, because the pipeline was unchanged.

**Shadow deployment** — Sending the new version a copy of live traffic and discarding its output. Zero user risk on real inputs, and the only way to see behaviour on the cases a held-out set never contained. It stops being a shadow the moment the path can write.

**Canary release** — Routing a small slice of real traffic to the new version and widening if the metrics hold. The first option that can measure user behaviour, with risk bounded by the slice.

**Interleaved comparison** — Mixing results from both versions into one ranked response so each user acts as their own comparison. Far more sensitive than splitting users — the pairing argument applied to deployment.

**Blue-green deployment** — Two full environments with traffic switched between them. A rollback strategy rather than an evaluation one: fast to revert, and it tells you nothing before the switch.

**Domain classifier (drift detection)** — Labelling training data 0 and recent data 1 and training a classifier to separate them. If it cannot, the distributions match; if it can, its accuracy measures the drift and its feature importances name the cause. Catches joint drift that per-feature tests cannot see.

**Out-of-bag (OOB) estimate** — Scoring each row using only the bagged trees that never saw it. A free held-out estimate, available during training, usually close enough to cross-validation to skip it.

**Spearman correlation** — Correlation computed on ranks, so it detects any monotonic relationship rather than only a linear one, and is far less sensitive to outliers. Where it disagrees with Pearson, the disagreement is the finding.

**Idempotency key** — A caller-generated identifier for a logical operation, sent with every attempt, so a server recognises a repeat and returns the original result instead of doing the work twice. The key belongs to the operation, not the attempt — a fresh key per retry defeats the mechanism.

**Jitter** — Randomisation added to backoff intervals so clients that failed together do not retry together. Without it, a retry storm is a second outage arriving on a schedule.

**Retry-After** — The header a 429 or 503 uses to tell a client when to try again. Honouring it beats backing off on your own schedule, which makes an overload worse.

**Readiness against liveness** — Whether a service can do its job, against whether its process exists. A health check that returns 200 regardless answers the second question, which nobody was asking.

**Startup refusal** — Failing to boot when required configuration is absent, rather than falling back to a permissive default. The failure is then found by the person deploying, in the minute they deploy.

**Image promotion** — Deploying the artefact you tested rather than rebuilding from source at deploy time. Rebuilding discards the guarantee that building an image was for.

---

## Block 9 · Electives

**Image tokens** — What a multimodal encoder turns a picture into: vectors occupying context positions, priced and truncated like text. Resolution is therefore a context-cost dial, not only a quality one.

**Window function** — A SQL construct that keeps every row while adding a group-level aggregate alongside it. What comparing a row against its own group requires, and what GROUP BY cannot do.

**Join cardinality** — Whether a join multiplies rows. A one-to-many join inflates every sum downstream of it and produces a plausible wrong number rather than an error, which makes it the commonest way a confident analysis is wrong.

**Cost per outcome** — Attributing the whole chain — retries, escalations, failed attempts — to the result it produced, rather than pricing individual calls. A cheap model needing three attempts is not cheap.

**Spend attribution** — Recording input, output and cached tokens per request at the time it happens, since an invoice gives a total and cannot be decomposed afterwards.

---

## Closing · The Future of Work

**Compositional effect** — A change in who holds jobs without a change in how many there are. The 2026 labour evidence shows no aggregate employment effect alongside a sharp decline in junior hiring, which is a structurally different situation from a shrinking market.

**Capability frontier** — The boundary of what a model does reliably. Inside it, measured gains are largest for the least experienced; outside it, people using AI were about 19 percentage points less accurate than people without it — so knowing which side you are on is the skill the tool does not supply.

**Tacit knowledge** — Practical, hard-to-codify skill acquired through working alongside someone who has it, rather than from instruction. The thing an apprenticeship transmits, and the reason its transmission does not scale: expertise is embodied in a person, so one expert can only oversee so much at once.

**The apprenticeship problem** — That junior work is simultaneously output and the mechanism by which judgement is built, so automating it removes the second function as an unintended consequence of removing the first. An argument in this course's closing chapter, not a finding.

**Complementary assets** — The skilled staff, organisational processes and data infrastructure that decide whether AI adoption produces a gain. Their importance is why adoption concentrates among firms that were already productive.

