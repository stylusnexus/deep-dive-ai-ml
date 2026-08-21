# Generative AI — prompting, RAG, structured output

## Prompting
- [ ] Task actually needs a generative model — not classification wearing a costume
- [ ] Output format specified and constrained, not requested politely
- [ ] Few-shot examples cover the classes, including the awkward ones
- [ ] Examples held back from the ones you evaluate on — tuning against all of them is leakage by hand
- [ ] Temperature 0 for anything parsed by code
- [ ] Stable content at the front of the prompt so caching works
- [ ] Refusal explicitly licensed — "say you don't know" costs little and helps

## Retrieval
- [ ] ☠ Keyword baseline (BM25) tried before reaching for vectors
- [ ] Chunking checked by eye — are chunks whole thoughts?
- [ ] Hybrid retrieval, fused by rank not by score
- [ ] Reranker over the shortlist if precision at the top matters
- [ ] ☠ Index recall measured against exact search — the failure nobody checks
- [ ] Small number of chunks in context; ranked, most relevant first or last, never buried mid-context
- [ ] Empty-retrieval path defined — the model must not answer from memory when nothing came back

## Structured output
- [ ] Highest rung available used: constrained decoding > schema > JSON mode > asking
- [ ] Schema field names and enums written as if explaining them — they're read by the model
- [ ] Validated on values, not just parsed
- [ ] One repair retry, then fail loudly
- [ ] Truncation ruled out as a cause before blaming the model

## Evaluation
- [ ] ☠ Private eval set of ~20 real items exists
- [ ] Groundedness measured separately from correctness
- [ ] Model-as-judge used only as a last resort, never with the judge as the model under test
- [ ] Cost per call and p95 latency measured, not estimated

## Smells
- Answers confident and wrong → ungrounded; retrieval before prompt-tuning
- RAG quality dropped with no prompt change → measure index recall first
- Intermittent malformed JSON → check temperature, then max-tokens
