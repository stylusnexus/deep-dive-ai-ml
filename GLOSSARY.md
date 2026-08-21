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

---

## Block 1 · Python, Data & EDA
*to come*

## Block 2 · Classical ML
*to come*
