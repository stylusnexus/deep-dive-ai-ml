# Building and Measuring LLM Systems

A self-built curriculum in applied AI and machine learning: ~13 weeks of lessons, runnable notebooks, and four portfolio projects.

## Why this exists

Most applied AI curricula cover the same standard material and stop short of the parts that decide whether a system survives contact with production. This one covers the standard material and then keeps going, and every checkable claim in it has been checked.

## What this covers that short courses usually skip

| Added | Why |
|---|---|
| **Security** | Curricula routinely teach "Responsible AI" as ethics and governance but never prompt injection, tool abuse, or agent sandboxing — in a program that builds multi-agent systems that take actions |
| **Evaluation** as a module | Usually a bullet point or two. It's the discipline that separates a demo from production |
| **Cost & routing** | Absent entirely. Token cost, caching, model routing, when a small local model is enough |
| **APIs** | Courses consume APIs constantly and rarely teach designing or serving one, despite "deployment" being a module |
| **Training & fine-tuning** | Rarely covered at all |
| **Time series** | Frequently omitted, despite how many real business problems are time-series problems |
| **Retention** | Most courses have no mechanism to make week 3 survive to week 13. This one wires into engram spaced repetition from day one |

## The three outcomes

Everything here is built to deliver three things that aren't modules — they're judgment, practised repeatedly:

1. **What to look for when building projects** → [`artifacts/project-intake.md`](artifacts/project-intake.md), filled in before every project and lab
2. **How to evaluate platforms, tools and models** → [`artifacts/selection-scorecard.md`](artifacts/selection-scorecard.md), used for every model, vendor and framework decision
3. **How to speak the language** → [`GLOSSARY.md`](GLOSSARY.md), built cumulatively and fed into spaced repetition

And when you're actually building: [`artifacts/sop/`](artifacts/sop/) — checklists in the
aviation sense. A master run-through plus focused ones for training, deep learning,
fine-tuning, generative AI, LLM engineering, measurement, and a separate non-normal
checklist for when something is already broken.

## Start here

1. Read [`CURRICULUM.md`](CURRICULUM.md) — the week-by-week map
2. Run `make up` (or see [`docker/README.md`](docker/README.md)) to bring up the environments

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
