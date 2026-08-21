#!/usr/bin/env python3
"""Build engram-format lessons from a content module. Stdlib only.

Usage: python3 scripts/build_lessons.py <content_module_name>
Emits lessons/<topic>/*.html + meta.json in the same house format as
statistics-for-ai and aigp-exam-prep.
"""
import importlib.util
import html
import json
import pathlib
import sys

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


def render_block(b):
    kind = b[0]
    if kind == "h2":
        return f"  <h2>{E(b[1])}</h2>"
    if kind == "h3":
        return f"  <h3>{E(b[1])}</h3>"
    if kind == "p":
        return f"  <p>{b[1]}</p>"
    if kind == "callout":
        _, variant, label, text = b
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
        return (f'  <figure class="diagram">{svg}'
                f"<figcaption>{caption}</figcaption></figure>")
    if kind == "links":
        items = "".join(
            f'<li><a href="{u}" target="_blank" rel="noopener">{E(t)}</a>'
            f'<span class="link-note">{n}</span></li>' for t, u, n in b[1]
        )
        return f'  <div class="further"><h3>Further reading</h3><ul class="links">{items}</ul></div>'
    if kind == "quiz":
        parts = ['  <div class="quiz">', "    <h3>✅ Check Yourself</h3>"]
        for n, (q, opts, ans) in enumerate(b[1], 1):
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
        body = "\n".join(render_block(b) for b in lsn["body"])
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
