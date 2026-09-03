#!/usr/bin/env python3
"""Build engram-format lessons from a content module. Stdlib only.

Usage: python3 scripts/build_lessons.py <content_module_name>
Emits lessons/<topic>/*.html + meta.json in the same house format as
statistics-for-ai and aigp-exam-prep.
"""
import html
import importlib.util
import json
import pathlib
import re
import sys
import xml.dom.minidom

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from lesson_map import slug_map

# Cyrillic and CJK never appear intentionally in this course; Greek (Σ, √) does.
STRAY_SCRIPT = re.compile(r"[\u0400-\u04FF\u4E00-\u9FFF\u3040-\u30FF]")

ROOT = pathlib.Path(__file__).resolve().parent.parent
STYLE = (ROOT / "scripts" / "_lesson_style.html").read_text()

QUIZ_JS = """<script>
document.querySelectorAll(".quiz-options").forEach(group => {
  const fb = group.parentElement.querySelector(".quiz-feedback");
  const opts = group.querySelectorAll(".quiz-opt");
  let solved = false;
  opts.forEach((opt, i) => {
    opt.addEventListener("click", () => {
      if (solved) return;
      const ok = i === Number(group.dataset.answer);
      opts.forEach(o => o.classList.remove("wrong"));
      if (ok) {
        solved = true;
        opt.classList.add("correct");
        fb.textContent = "\\u2713 Correct \\u2014 " + opt.textContent.trim() + ".";
        fb.className = "quiz-feedback show correct";
      } else {
        opt.classList.add("wrong");
        fb.textContent = "\\u2717 Not quite \\u2014 think about what problem that choice would actually solve, then try another option.";
        fb.className = "quiz-feedback show wrong";
      }
    });
  });
});

window.addEventListener("message", (e) => {
  if (e.data && e.data.type === "engram-quest-theme") {
    document.body.classList.toggle("light", !e.data.dark);
  }
});
</script>"""

E = html.escape

# variants with a CSS rule in _lesson_style.html; anything else renders unstyled
CALLOUT_VARIANTS = set(re.findall(r"\.callout\.([a-z]+)", STYLE))


def render_block(b, topic=None, self_slug=None):
    kind = b[0]
    stray = STRAY_SCRIPT.findall(" ".join(str(x) for x in b[1:]))
    if stray:
        raise AssertionError(
            f"stray non-Latin characters {sorted(set(stray))} in a {kind} block — "
            f"almost always a slip; Greek maths symbols are allowed, Cyrillic/CJK are not")
    # prose blocks are emitted as raw HTML, so a stray backtick renders literally
    if kind in ("p", "h2", "h3"):
        assert "`" not in b[1], f"backtick in prose (use <code>): {b[1][:60]}"
    if kind == "callout":
        assert "`" not in b[3], f"backtick in callout (use <code>): {b[2]}"
    if kind == "know":
        for part in b[1:]:
            assert "`" not in part, f"backtick in know block (use <code>): {part[:60]}"
    if kind == "h2":
        return f"  <h2>{E(b[1])}</h2>"
    if kind == "h3":
        return f"  <h3>{E(b[1])}</h3>"
    if kind == "p":
        return f"  <p>{b[1]}</p>"
    if kind == "callout":
        _, variant, label, text = b
        assert variant in CALLOUT_VARIANTS, (
            f"undefined callout variant {variant!r} — add CSS or use one of "
            f"{sorted(CALLOUT_VARIANTS)}")
        return (f'  <div class="callout {variant}"><span class="label">{E(label)}</span>'
                f"{text}</div>")
    if kind == "ul":
        items = "".join(f"<li>{i}</li>" for i in b[1])
        return f"  <ul>{items}</ul>"
    if kind == "code":
        return f'  <pre><code>{E(b[1])}</code></pre>'
    if kind == "terms":
        rows = "".join(
            f'<div class="roadmap-item"><div class="roadmap-num">{E(n)}</div>'
            f'<div><div class="roadmap-title">{E(t)}</div>'
            f'<div class="roadmap-desc">{d}</div></div></div>'
            for n, t, d in b[1]
        )
        # numeric labels keep the circle; word labels get the pill variant
        numeric = all(str(n).strip().isdigit() for n, _, _ in b[1])
        cls = "roadmap" if numeric else "roadmap terms"
        return f'  <div class="{cls}">{rows}</div>'
    if kind == "figure":
        _, caption, svg = b
        # SVG is XML: it defines only &amp; &lt; &gt; &quot; &apos;. HTML named
        # entities such as &mdash; parse in prose and blow up inside a diagram.
        stray = set(re.findall(r"&([a-zA-Z][a-zA-Z0-9]*);", svg)) - {
            "amp", "lt", "gt", "quot", "apos"}
        if stray:
            raise AssertionError(
                f"HTML entities in SVG ({', '.join(sorted(stray))}) — "
                f"use the character itself or a numeric entity like &#8212;")
        xml.dom.minidom.parseString(svg)
        return (f'  <figure class="diagram">{svg}'
                f"<figcaption>{caption}</figcaption></figure>")
    if kind == "know":
        _, rule, why, example = b
        return (f'  <blockquote class="know">'
                f'<span class="know-label">Worth knowing</span>'
                f'<p class="know-rule">{rule}</p>'
                f'<p class="know-why">{why}</p>'
                f'<p class="know-eg"><span class="know-eg-label">For example</span>{example}</p>'
                f"</blockquote>")
    if kind == "books":
        items = "".join(
            f'<li><span class="bk-t">{E(t)}</span>'
            f'<span class="bk-a">{E(a)}</span>'
            f'<span class="bk-n">{n}</span></li>' for t, a, n in b[1]
        )
        return (f'  <div class="further shelf"><h3>On your shelf</h3>'
                f'<ul class="books">{items}</ul></div>')
    if kind == "related":
        smap = slug_map()
        items = []
        for slug in b[1]:
            if slug not in smap:
                raise AssertionError(
                    f"related: no lesson with slug {slug!r} — cross-references are "
                    f"checked at build time so a rename cannot leave a dead link")
            if slug == self_slug:
                raise AssertionError(f"related: {slug!r} links to itself")
            t = smap[slug]
            href = t["file"] if t["topic"] == topic else f"../{t['topic']}/{t['file']}"
            same = "" if t["topic"] == topic else f'<span class="rel-set">{E(t["set_title"])}</span>'
            items.append(
                f'<li><a href="{href}">{E(t["title"])}</a>{same}'
                f'<span class="link-note">{t["subtitle"]}</span></li>')
        return ('  <div class="further related"><h3>Related lessons</h3>'
                f'<ul class="links">{"".join(items)}</ul></div>')
    if kind == "links":
        items = "".join(
            f'<li><a href="{u}" target="_blank" rel="noopener">{E(t)}</a>'
            f'<span class="link-note">{n}</span></li>' for t, u, n in b[1]
        )
        return f'  <div class="further"><h3>Further reading</h3><ul class="links">{items}</ul></div>'
    if kind == "quiz":
        parts = ['  <div class="quiz">', "    <h3>✅ Check Yourself</h3>"]
        for n, (q, opts, ans) in enumerate(b[1], 1):
            # quiz text is HTML-escaped, so backticks would render literally
            assert "`" not in q and not any("`" in o for o in opts), \
                f"backtick in escaped quiz text: {q[:50]}"
            parts.append(f'    <p class="quiz-q">{n}. {E(q)}</p>')
            parts.append(f'    <div class="quiz-options" data-answer="{ans}">')
            parts += [f'      <div class="quiz-opt">{E(o)}</div>' for o in opts]
            parts.append("    </div>")
            parts.append('    <div class="quiz-feedback"></div>')
        parts.append("  </div>")
        return "\n".join(parts)
    raise ValueError(f"unknown block: {kind}")


def build(mod):
    topic_dir = ROOT / "lessons" / mod.TOPIC
    topic_dir.mkdir(parents=True, exist_ok=True)
    total = len(mod.LESSONS)
    entries, completion = [], {}

    for idx, lsn in enumerate(mod.LESSONS):
        lid = f"lsn-{mod.ID_BASE}{idx:03d}"
        fname = f"{lid}-{lsn['slug']}.html"
        body = "\n".join(render_block(b, mod.TOPIC, lsn["slug"]) for b in lsn["body"])
        doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{E(lsn['title'])}</title>
{STYLE}
</head>
<body>

  <span class="pill">Lesson {idx + 1} of {total}</span>
  <h1>{E(lsn['title'])}</h1>
  <p class="subtitle">{lsn['subtitle']}</p>

{body}

{QUIZ_JS}
</body>
</html>
"""
        (topic_dir / fname).write_text(doc)
        entries.append({"id": lid, "title": lsn["title"], "file": fname, "source": "skill"})
        completion[lid] = {"viewed": False, "completed": False, "starred": False}

    # Lesson ids are index-based and filenames carry the slug, so inserting or
    # renaming a lesson leaves the old file on disk — present to anyone browsing
    # the directory, absent from meta.json. Drop what this build did not write.
    written = {e["file"] for e in entries}
    for stale in topic_dir.glob("lsn-*.html"):
        if stale.name not in written:
            print(f"  removed stale {mod.TOPIC}/{stale.name}")
            stale.unlink()

    meta = {
        "title": mod.TITLE,
        "topic": mod.TOPIC,
        "icon": mod.ICON,
        "description": mod.DESCRIPTION,
        "tags": mod.TAGS,
        "colorScheme": mod.COLOR,
        "starred": False,
        "archived": False,
        "createdAt": mod.CREATED,
        "lessons": entries,
        "completion": completion,
    }
    (topic_dir / "meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    return topic_dir, total


if __name__ == "__main__":
    name = sys.argv[1]
    path = ROOT / "scripts" / "content" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    out, n = build(module)
    print(f"built {n} lessons -> {out.relative_to(ROOT)}")
