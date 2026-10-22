#!/usr/bin/env python3
"""Write sitemap.xml, robots.txt, llms.txt and .nojekyll for the Pages site.

Everything is derived from the live lesson content, so a new lesson appears
in all of them on the next build. The set order is the landing page's own
SECTIONS list, read from build_index.py without running it, so the two cannot
drift. Stdlib only.
"""
import ast, html, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from lesson_map import slug_map
from seo_meta import SITE, NAME, plain
from build_docs import DOCS

REPO = "https://github.com/stylusnexus/deep-dive-ai-ml/blob/main/"


def section_order():
    tree = ast.parse((ROOT / "scripts" / "build_index.py").read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                getattr(t, "id", "") == "SECTIONS" for t in node.targets):
            return [(t, h, n) for t, h, n in ast.literal_eval(node.value)]
    raise SystemExit("build_index.py has no literal SECTIONS list to read the order from")


def lastmod(path):
    """Date of the last commit that touched `path`, or None outside a git checkout."""
    out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", path],
                         cwd=ROOT, capture_output=True, text=True).stdout.strip()
    return out or None


def main():
    sections = section_order()
    by_topic = {}
    for info in slug_map().values():
        by_topic.setdefault(info["topic"], []).append(info)
    for items in by_topic.values():
        items.sort(key=lambda i: i["file"])
    missing = set(by_topic) - {t for t, _, _ in sections}
    assert not missing, f"lesson sets missing from the landing page order: {sorted(missing)}"

    pages = [("", "index.html"), ("things-to-know.html", "things-to-know.html"),
             ("docs/", "docs/index.html")]
    pages += [(f"docs/{slug}.html", f"docs/{slug}.html") for _, slug, _, _ in DOCS]
    pages += [("artifacts/sop/index.html", "artifacts/sop/index.html")]
    for topic, _, _ in sections:
        pages += [(f"lessons/{topic}/{i['file']}", f"lessons/{topic}/{i['file']}")
                  for i in by_topic.get(topic, [])]

    urls = []
    for rel, src in pages:
        lm = lastmod(src)
        urls.append(f"  <url><loc>{SITE}{rel}</loc>" + (f"<lastmod>{lm}</lastmod>" if lm else "") + "</url>")
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls) + "\n</urlset>\n")

    # Everything is public teaching material: search and AI crawlers are welcome.
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n")
    (ROOT / ".nojekyll").write_text("")

    total = sum(len(v) for v in by_topic.values())
    lines = [
        f"# {NAME}", "",
        f"> A free, self-built course in applied AI and machine learning: {total} lessons, "
        "runnable notebooks with their executed outputs, and four portfolio projects. "
        "It covers evaluation, retrieval and agentic systems, LLM security, quantization "
        "and fine-tuning, cost, and deployment. Claims that can be checked have been "
        "checked, and numbers in lessons come from runs.", "",
        "Lessons are self-contained HTML pages and can be read in any order; each defines "
        "its terms on first use. The notebooks and projects live in the GitHub repository "
        "and run locally.", "",
    ]
    for topic, heading, note in sections:
        if topic not in by_topic:
            continue
        lines += [f"## {plain(heading, 200)}", "", plain(note, 400), ""]
        for i in by_topic[topic]:
            lines.append(f"- [{i['title']}]({SITE}lessons/{topic}/{i['file']}): {plain(i['subtitle'], 220)}")
        lines.append("")
    lines += [
        "## Course materials", "",
        f"- [Curriculum]({REPO}CURRICULUM.md): all blocks, week by week, each with a runnable exit criterion.",
        f"- [Glossary]({REPO}GLOSSARY.md): every term the course defines.",
        f"- [Things to Know]({SITE}things-to-know.html): every load-bearing rule, linked to the lesson that earns it.",
        f"- [Worksheets and references]({SITE}docs/): fill-in worksheets (project intake, selection scorecard, entry diagnostic, cumulative exam, design interview rubric) and reference pages, each also available as markdown.",
        f"- [SOP checklists]({SITE}artifacts/sop/index.html): operating checklists with killer items and hard gates.",
        f"- [Project intake sheet]({REPO}artifacts/project-intake.md): ten questions to answer before writing code.",
        f"- [Selection scorecard]({REPO}artifacts/selection-scorecard.md): for choosing a model, a vendor or a framework.",
        f"- [Design interview rubric]({REPO}artifacts/design-interview-rubric.md): a scored 45-minute mock interview on nine system-design questions.",
        f"- [Project 4, deployed assistant]({REPO}projects/p4-deployed-assistant/README.md): an authenticated, rate-limited retrieval service with provider failover.",
        f"- [Cumulative exam]({REPO}artifacts/cumulative-exam.md): ten scenarios across Blocks 3 to 8 with a marking key.",
        "", "## Optional", "",
        "- [Source repository](https://github.com/stylusnexus/deep-dive-ai-ml): lesson sources, notebooks, projects and build scripts.",
        "- [Statistical Learning](https://github.com/stylusnexus/statistics-for-ai): the companion statistics course.",
        "- [Math for AI](https://stylusnexus.github.io/statistics-for-ai/math.html): the companion linear algebra and calculus course.",
        "- [Responsible AI and Governance](https://github.com/stylusnexus/aigp-exam-prep): the companion governance course.",
        "",
    ]
    (ROOT / "llms.txt").write_text("\n".join(lines))
    print(f"built sitemap.xml ({len(urls)} urls), robots.txt, llms.txt ({total} lessons), .nojekyll")


if __name__ == "__main__":
    main()
