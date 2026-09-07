# Project 2 · Grounded Document Assistant

**Block 3 exit criterion.** The finance project.

> Help analysts extract key information from lengthy documents by leveraging
> retrieval-augmented generation, improving efficiency in decision-making.

The corpus here is the operations corpus from `data/corpus/` rather than a real
annual report — because the evaluation labels are then genuinely correct, which
is what makes the measurement worth anything. Swap in your own documents once the
pipeline is proven; `src/rag.py --corpus` takes a directory.

## What "done" looks like

Not "it answers questions". A system whose failures you can locate:

- [ ] Intake sheet completed before building
- [ ] Chunks inspected by eye — twenty printed and read
- [ ] Index recall measured against exact search, not assumed
- [ ] Retrieval quality measured against gold labels at the k you actually send
- [ ] Groundedness measured **separately** from correctness
- [ ] The refusal case tested — a question the corpus cannot answer
- [ ] Every answer carries citations a human can check in one step
- [ ] A statement of which question types the system cannot handle

## Running it

```bash
python src/rag.py                      # build index, run eval, write report
python src/rag.py --k 3                # send fewer chunks
python src/rag.py --no-rerank          # measure what the reranker was worth
python src/rag.py --corpus path/to/docs   # your own documents
```

Requires the embedding model (downloads once) and optionally a local
OpenAI-compatible endpoint for generation. Without one it uses an extractive
stand-in so the measurement still runs.

## The honest framing

The deliverable is not the assistant. It is the sentence *"this system answers
single-hop policy questions with 0.9 groundedness and refuses correctly when the
answer is absent — and it cannot answer questions requiring two documents."*

Knowing what it cannot do is what makes it safe to deploy.
