#!/usr/bin/env python3
"""Landing page for the program, in the same house style as the other courses."""
import html, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
STYLE = (ROOT / "scripts" / "_index_style.html").read_text()
E = html.escape

BLURBS = {
 "agent-loop-and-harness": "The two words your own docs use most — and why almost every agent failure is a harness failure, not a model failure.",
 "tokens-context-and-kv-cache": "Why a model 'forgets', why long conversations get expensive quadratically, and what prompt caching is actually caching.",
 "weights-gguf-quantization": "What Q4_K_M means character by character, and why a heavily quantized big model beats a small precise one.",
 "serving-locally": "Ollama, llama.cpp and the metal underneath — plus how to read a tokens-per-second number without being misled.",
 "embeddings-and-retrieval": "How a machine decides two things mean the same, the routing it enables, and the three places it quietly fails.",
 "tool-calls-and-mcp": "How a text model comes to run your code, what MCP standardises, and where prompt injection gets its leverage.",
 "routing-and-escalation": "The idea Bullpen is built on — try cheap, verify, escalate — plus temperature and top-k.",
 "eval-battery": "How you know any of it works, and why the only number worth trusting is one you built yourself.",
 "overfitting-and-underfitting": "The most important pair of words in machine learning, and the habit that catches the dangerous one.",
}

meta = json.loads((ROOT / "lessons" / "bullpen-vocabulary" / "meta.json").read_text())
cards = []
for l in meta["lessons"]:
    slug = l["file"].split("-", 2)[2].rsplit(".", 1)[0]
    cards.append(
        f'  <li><a class="card" href="lessons/bullpen-vocabulary/{l["file"]}">\n'
        f'    <h2>{E(l["title"])}</h2>\n'
        f'    <p>{E(BLURBS.get(slug, ""))}</p>\n'
        f"  </a></li>"
    )

doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PGP AI/ML — Program Home</title>
{STYLE}
</head>
<body>

<p class="eyebrow">🎯 Self-built program</p>
<h1>Post Graduate Program in AI &amp; Machine Learning</h1>
<p class="lede">A rebuild of the UT Austin / McCombs PGP curriculum as ~13 weeks of lessons, runnable notebooks and four portfolio projects — with the security, evaluation, cost and fine-tuning material the original leaves out.</p>

<div class="meta">
  <span class="chip">10 blocks</span>
  <span class="chip">4 portfolio projects</span>
  <span class="chip">Docker environments</span>
  <span class="chip">Spaced repetition built in</span>
</div>

<h2 style="margin-top:44px">Block 0 · Vocabulary</h2>
<p class="lede" style="font-size:1em">The terms the rest of the program assumes, taught against Bullpen — a system you built — rather than someone else's toy example.</p>

<ol class="lessons">
{chr(10).join(cards)}
</ol>

<h2 style="margin-top:44px">Everything else</h2>
<ol class="lessons">
  <li><a class="card" href="CURRICULUM.md"><h2>The curriculum</h2>
    <p>All ten blocks, week by week, each with an exit criterion that runs rather than a box that ticks.</p></a></li>
  <li><a class="card" href="artifacts/project-intake.md"><h2>Project intake sheet</h2>
    <p>Ten questions to answer before writing code. Filled in before every project, reviewed after.</p></a></li>
  <li><a class="card" href="artifacts/selection-scorecard.md"><h2>Selection scorecard</h2>
    <p>For choosing a model, a vendor, or a framework — three decisions with three different failure modes.</p></a></li>
  <li><a class="card" href="GLOSSARY.md"><h2>Glossary</h2>
    <p>Every term the program defines, accumulating block by block and feeding spaced repetition.</p></a></li>
</ol>

</body>
</html>
"""
(ROOT / "index.html").write_text(doc)
print(f"built index.html ({len(meta['lessons'])} lesson cards)")
