# pgp-aiml

A self-built recreation of the UT Austin / McCombs **Post Graduate Program in AI & Machine Learning: Business Applications**, rebuilt as ~13 weeks of lessons, runnable notebooks, and four portfolio projects.

## Why this exists

The original is 23 weeks and sells four things: content, live mentorship, a credential, and graded assessment. Only the content is reproducible — and it's standard material. This repo reproduces the content, adds the parts the original leaves out, and drops the scheduling padding.

## What's different from the original

The syllabus we're copying has real gaps. This version fixes them:

| Added | Why |
|---|---|
| **Security** | The original teaches "Responsible AI" (ethics/governance) but never prompt injection, tool abuse, or agent sandboxing — in a program that builds multi-agent systems that take actions |
| **Evaluation** as a module | Two bullet points in the original. It's the discipline that separates a demo from production |
| **Cost & routing** | Absent entirely. Token cost, caching, model routing, when a small local model is enough |
| **APIs** | The original consumes APIs constantly and never teaches designing or serving one, despite "deployment" being a module |
| **Training & fine-tuning** | Zero coverage in the original |
| **Time series** | Omitted by the original, despite three of its own case studies being time-series problems |
| **Retention** | The original has no mechanism to make week 3 survive to week 23. This one wires into engram spaced repetition from day one |

## The three outcomes

Everything here is built to deliver three things that aren't modules — they're judgment, practised repeatedly:

1. **What to look for when building projects** → [`artifacts/project-intake.md`](artifacts/project-intake.md), filled in before every project and lab
2. **How to evaluate platforms, tools and models** → [`artifacts/selection-scorecard.md`](artifacts/selection-scorecard.md), used for every model, vendor and framework decision
3. **How to speak the language** → [`GLOSSARY.md`](GLOSSARY.md), built cumulatively and fed into spaced repetition

## Start here

1. Read [`CURRICULUM.md`](CURRICULUM.md) — the week-by-week map
2. Run `make up` (or see [`docker/README.md`](docker/README.md)) to bring up the environments
3. Begin with `lessons/bullpen-vocabulary/` — the vocabulary spine

## Layout

```
lessons/     Self-contained HTML lessons (engram format, open straight from disk)
notebooks/   Runnable labs, one folder per block
projects/    Four portfolio projects
artifacts/   The intake sheet, selection scorecard, and other recurring tools
docker/      Reproducible environments — torch, keras, pgvector, mlflow
scripts/     Setup and helper scripts
```

## Already complete

Two blocks were built previously and are wired in rather than rebuilt:

- **Statistical Learning** → [`statistics-for-ai`](https://github.com/stylusnexus/statistics-for-ai) (10 lessons)
- **Responsible AI / Governance** → `aigp-exam-prep` (12 lessons, private)

## Hardware and accounts this assumes

Apple M4 Max / 128GB unified memory · Docker · Hugging Face Pro (org `stylusnexus`) · Anthropic and OpenAI API keys.

Local fine-tuning of 7B–13B models with LoRA runs on this machine. Nothing here requires renting a GPU.
