# Fine-tuning — adapting an existing model

## ☠ Before you fine-tune at all
- [ ] ☠ Prompt engineering exhausted and measured
- [ ] ☠ Retrieval tried — if the gap is *knowledge*, RAG is the answer, not fine-tuning
- [ ] ☠ The gap is format, tone, domain idiom or consistency — things weights can fix
- [ ] Few-shot economics calculated: example tokens × call volume vs training cost
- [ ] Eval set built **before** training, so before/after is comparable

If the first three aren't all yes, stop. Most fine-tuning projects should end here.

## Data
- [ ] Enough examples for the method — hundreds for LoRA on a narrow task, not tens
- [ ] Examples consistent in format; contradictions in the data become contradictions in the model
- [ ] Held-out split the training never sees
- [ ] Licensing checked if the data came from another model's outputs
- [ ] Deduplicated — near-duplicates inflate your eval

## Method
- [ ] LoRA / QLoRA before full fine-tune; rank chosen deliberately
- [ ] Base model licence permits your use
- [ ] Chat template matches the base model exactly
- [ ] Hardware plan real (M4 Max, 128GB: LoRA on 7B–13B is comfortable locally)
- [ ] If it does not fit: mixed precision, then gradient accumulation, then gradient
      checkpointing — in that order — *before* reaching for a smaller model. The first two cost
      no accuracy at all and the third costs only time; a smaller model costs capability
- [ ] Loss flat immediately after enabling mixed precision treated as a numerics problem
      (gradient underflow, loss scaling) rather than a learning-rate one

## After
- [ ] ☠ Evaluated against the **base model** on the same held-out set — not just "it looks better"
- [ ] Checked for capability loss outside the fine-tuned task
- [ ] Overfitting checked — does it parrot training examples verbatim?
- [ ] Adapter versioned and stored somewhere real, not a local folder
- [ ] Quantized for serving if it's going local; re-evaluated after quantizing

## Smells
- Brilliant on training examples, worse everywhere else → trained too long on too little
- No improvement at all → the gap was knowledge, not format; go back to retrieval
