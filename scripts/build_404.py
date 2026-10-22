#!/usr/bin/env python3
"""404.html for GitHub Pages, in the landing page's look.

Pages serves this file for any missing address, at any depth, so nothing here
may be relative: every link is absolute. It is kept out of search results.
The design inspector's motion-budget rule (still-page) is meant for full pages and
is allowed here: this is one screen with one entrance animation. Stdlib only.
"""
import html, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from seo_meta import SITE, NAME

STYLE = (ROOT / "scripts" / "_index_style.html").read_text()
E = html.escape
WORDMARK = "Stylus Nexus"

first = json.loads((ROOT / "lessons" / "orientation" / "meta.json").read_text())["lessons"][0]["file"]
START = f"{SITE}lessons/orientation/{first}"

doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Page not found | {E(NAME)}</title>
<meta name="robots" content="noindex">
<meta name="description" content="This page does not exist. Browse the lessons, worksheets and references of the free {E(NAME)} course.">
<meta name="color-scheme" content="dark light">
{STYLE}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<header class="bar">
  <a class="mark" href="{SITE}">{WORDMARK}</a>
  <nav aria-label="Primary">
    <ul>
      <li><a href="{SITE}#lessons">Lessons</a></li>
      <li><a href="{SITE}docs/">Worksheets</a></li>
      <li><a href="https://github.com/stylusnexus/deep-dive-ai-ml">Source</a></li>
    </ul>
  </nav>
</header>

<main id="main">
<section class="hero" aria-label="Page not found">
  <div class="up"></div>
  <h1 class="hero-title"><span class="ln"><span>That page</span></span><span class="ln"><span>is not here</span></span></h1>
  <div class="down">
    <div class="hero-copy">
      <p>It moved, or it never existed. Lesson addresses include the lesson's position in its set, so a link saved before a lesson was added can point at an old name. The lesson list always has the current ones.</p>
      <a class="btn" href="{SITE}#lessons">See all lessons</a>
      <small><a href="{START}">Start with the map</a> &middot; <a href="{SITE}docs/">Worksheets and references</a> &middot; <a href="{SITE}things-to-know.html">Things to Know</a></small>
    </div>
  </div>
</section>
</main>

<footer>
  <nav aria-label="Project">
    <ul class="places">
      <li><a href="https://github.com/stylusnexus/deep-dive-ai-ml">Source on GitHub</a></li>
      <li><a href="{SITE}docs/curriculum.html">Curriculum</a></li>
      <li><a href="{SITE}docs/glossary.html">Glossary</a></li>
      <li><a href="{SITE}docs/">Worksheets</a></li>
    </ul>
  </nav>
  <p class="name" aria-hidden="true">{WORDMARK}</p>
  <p class="legal">Published by Stylus Nexus. {E(NAME)}.</p>
</footer>
</body>
</html>
"""
(ROOT / "404.html").write_text(doc)
print("built 404.html")
