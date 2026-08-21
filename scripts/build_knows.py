#!/usr/bin/env python3
"""Collect every "worth knowing" line into one revision sheet."""
import html, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
STYLE = (ROOT / "scripts" / "_index_style.html").read_text()

sections, total = [], 0
for topic in ["orientation", "core-vocabulary", "algorithms", "engineering-practice", "block1-data-eda"]:
    d = ROOT / "lessons" / topic
    if not d.exists():
        continue
    meta = json.loads((d / "meta.json").read_text())
    items = []
    for l in meta["lessons"]:
        s = (d / l["file"]).read_text()
        for m in re.findall(r'<blockquote class="know">(.*?)</blockquote>', s, re.S):
            body = m.split("</span>", 1)[1] if "</span>" in m else m
            items.append(f'  <li><a href="lessons/{topic}/{l["file"]}">{html.escape(l["title"])}</a>'
                         f"{body.strip()}</li>")
    if items:
        total += len(items)
        sections.append(f'<h2>{meta["icon"]} {html.escape(meta["title"])}</h2>\n'
                        f'<ul class="knows">\n{chr(10).join(items)}\n</ul>')

doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Things to Know</title>
{STYLE}
<style>
  ul.knows {{ list-style: none; padding: 0; }}
  ul.knows li {{
    margin: 0 0 20px; padding: 16px 18px; background: var(--surface);
    border-left: 3px solid var(--accent2); border-radius: 6px;
  }}
  ul.knows li a {{ display: block; font-size: 0.72em; text-transform: uppercase;
                   letter-spacing: 0.09em; font-weight: 700; text-decoration: none;
                   color: var(--accent2); opacity: 0.95; margin-bottom: 2px; }}
  ul.knows li a:hover {{ text-decoration: underline; }}
  ul.knows li .know-rule {{ margin: 8px 0 8px; font-weight: 600; font-size: 1.02em; }}
  ul.knows li .know-why {{ margin: 0 0 10px; opacity: 0.9; }}
  ul.knows li .know-eg {{ margin: 0; padding: 10px 12px; background: var(--code-bg);
                          border-radius: 5px; font-size: 0.93em; color: var(--muted); }}
  ul.knows li .know-eg-label {{ display: block; font-size: 0.7em; font-weight: 700;
                                letter-spacing: 0.09em; text-transform: uppercase;
                                color: var(--green); margin-bottom: 4px; }}
</style>
</head>
<body>

<p class="eyebrow">📌 Revision sheet</p>
<h1>Things to Know</h1>
<p class="lede">Every compressed, load-bearing line from the course, collected. {total} of them. Each links back to the lesson that earns it — read this before an interview, a vendor call, or a design review.</p>

{chr(10).join(sections)}

</body>
</html>
"""
(ROOT / "things-to-know.html").write_text(doc)
print(f"built things-to-know.html — {total} entries")
