# How to use this

Three things live here: **lessons** you read, **notebooks** you run, and **projects**
you build. This page says how they fit together and in what order.

## The short version

```bash
open index.html      # the landing page - every lesson, by block
make up              # the environments, if you're going to run notebooks
```

Then, per block: read the lessons, run the notebook, build the project if the block
has one, and stop when you hit the block's exit criterion. [`CURRICULUM.md`](CURRICULUM.md)
is the map and tells you what each exit criterion is.

Before Block 1, run the [entry diagnostic](artifacts/prerequisite-diagnostic.md).
It routes repair work; it is not an admissions test.

That's the whole loop. The rest of this page is detail you can come back for.

## What each part is for

| Part | What it is | How you use it |
|---|---|---|
| [`index.html`](index.html) | Landing page, 106 lessons by block | Open it in a browser. No server, no build |
| `lessons/` | Self-contained HTML - prose, diagrams, quizzes | Read in block order, or jump to one; each is written to stand alone |
| `notebooks/` | Runnable labs, one folder per block | See [`notebooks/README.md`](notebooks/README.md) |
| `projects/` | Four portfolio builds | At block boundaries 2, 3, 4 and 8 |
| [`artifacts/sop/`](artifacts/sop/) | Checklists, aviation-style | Open before you build, tick as you go |
| [`artifacts/engineering-foundations.md`](artifacts/engineering-foundations.md) | Optional systems-engineering reading map | Experienced developers can skip it; otherwise use it when a project exposes a representation, time, distributed-failure or maintenance assumption |
| [`GLOSSARY.md`](GLOSSARY.md) | Every term, cumulative | Add to it as you go; feed into spaced repetition |
| [`things-to-know.html`](things-to-know.html) | 158 rules harvested from the lessons | The revision sheet. Read it when you've forgotten a block |

## A block, start to finish

1. **Fill in the intake sheet** - [`artifacts/project-intake.md`](artifacts/project-intake.md),
   before any code. It asks what you're building and how you'll know it worked.
2. **Read the block's lessons.** They assume the previous blocks' vocabulary but not
   your memory of it - every acronym re-expands.
3. **Run the block's notebook.** It arrives already executed so you can read the
   results first, then re-run it yourself. After the guided run, close the notebook
   and rebuild one small example from memory before looking back at the answer.
4. **Open the matching SOP** when you start building. There's one for training,
   deep learning, fine-tuning, generative AI, LLM engineering, measurement and
   security, plus a non-normal checklist for when something is already broken.
5. **Hit the exit criterion.** Every block has one, and it's a thing that runs
   rather than a box you tick.
6. **Commit.** Block boundaries are the save points.

## The three that thread through

These aren't modules - they're the judgment the course exists to build, practised
in every block rather than taught once:

- **[The intake sheet](artifacts/project-intake.md)** - what to look for before building
- **[The selection scorecard](artifacts/selection-scorecard.md)** - how to evaluate a model, vendor or framework
- **[The glossary](GLOSSARY.md)** - how to say it out loud

Re-read the intake sheet *after* the build, against what actually happened. That
comparison is most of the value.

## Making it stick

Thirteen weeks is long enough to forget week 3 by week 13, so there's a mechanism:

- Every glossary term goes into spaced repetition
- Every lesson's `know` blocks are harvested into [`things-to-know.html`](things-to-know.html)
- Each is a rule, a reason and a worked example - a rule on its own is a slogan

If you can't explain a term out loud without looking, you haven't got it yet.

## If you have less than 13 weeks

The shortest path that still leaves you able to build something real:

**Block 0** (vocabulary) → **Block 3** (retrieval) → **Block 5** (evaluation) → **Block 6** (security)

That's the spine of an LLM system: know the words, get grounded answers, prove
they're right, and don't get owned. Blocks 1 and 2 are classical ML and matter if
you're doing tabular work. Block 7 is training, which most projects should skip -
its first lesson argues exactly that.

## When you find a mistake

Two fabricated statistics reached these lessons before anyone checked them. Both
came from search summaries rather than papers, and both looked entirely reasonable.

So: if a number looks wrong, it might be. Check it, and if it *is* wrong, fix it at
source and record the verdict. `make numbers` fails on any figure nobody has
reviewed, which is what forces the judgement to happen once rather than never.

Lessons and notebooks are **generated**. Never edit `lessons/*.html` directly - edit
the module in `scripts/content/` and run `make lessons`. [`CLAUDE.md`](CLAUDE.md) has
the full authoring rules.

## What you need

To **read** the lessons: a browser. That's all - they're self-contained HTML.

To **run** the notebooks, three things beyond a laptop that can run Docker:

- **Blocks 1 to 3** need the containers, and Block 3 needs pgvector running. `make up`.
- **Blocks 3, 4 and 6** call a real model on a local OpenAI-compatible endpoint
  (`localhost:11434` or `11455` - Ollama or LM Studio). Any chat model will do; it
  takes whichever the endpoint offers first.
- **Block 7's training run** uses MLX on Apple Silicon. The notebook analyses a
  recorded run, so you can read the result without reproducing it.

Blocks 5, 8 and 9 run on any Python 3 with nothing installed.

Nothing here requires renting a GPU.
