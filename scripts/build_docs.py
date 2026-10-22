#!/usr/bin/env python3
"""Render the repository's markdown worksheets and reference docs as web pages.

Markdown shows as raw text on GitHub Pages, so each document listed in DOCS
becomes docs/<slug>.html:

* worksheets (intake sheets, scorecard, exam, rubric, diagnostic) get tick-boxes
  and fill-in fields that save in the visitor's browser, a "Download my answers"
  button that writes a real .md file, a CSV export for tables, and a print view;
* reference docs (curriculum, glossary, project READMEs and reports) get a clean
  read-only page, with the checkboxes shown as the author left them.

The page embeds the original markdown and a field map, so the downloaded answers
are the source file with the visitor's ticks and text filled in. Stdlib only.
"""
import html, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from seo_meta import SITE, NAME, head_meta, lesson_jsonld, plain

REPO_BLOB = "https://github.com/stylusnexus/deep-dive-ai-ml/blob/main/"
REPO_TREE = "https://github.com/stylusnexus/deep-dive-ai-ml/tree/main/"
STYLE = (ROOT / "scripts" / "_doc_style.html").read_text()
E = html.escape

# (source, slug, mode, options). mode: "worksheet" is interactive, "reference" is read-only.
DOCS = [
    ("artifacts/project-intake.md", "project-intake", "worksheet", {}),
    ("artifacts/selection-scorecard.md", "selection-scorecard", "worksheet", {}),
    ("artifacts/cumulative-exam.md", "cumulative-exam", "worksheet", {"answers": True}),
    ("artifacts/design-interview-rubric.md", "design-interview-rubric", "worksheet", {}),
    ("artifacts/prerequisite-diagnostic.md", "entry-diagnostic", "worksheet", {}),
    ("projects/p1-turbine-failure/intake.md", "p1-intake", "worksheet", {"title": "Project 1 intake sheet: wind turbine failure"}),
    ("projects/p2-financial-rag/intake.md", "p2-intake", "worksheet", {"title": "Project 2 intake sheet: financial retrieval"}),
    ("projects/p3-delivery-agents/intake.md", "p3-intake", "worksheet", {"title": "Project 3 intake sheet: delivery agents"}),
    ("projects/p4-deployed-assistant/intake.md", "p4-intake", "worksheet", {"title": "Project 4 intake sheet: deployed assistant"}),
    ("CURRICULUM.md", "curriculum", "reference", {}),
    ("GLOSSARY.md", "glossary", "reference", {}),
    ("HOW-TO-USE.md", "how-to-use", "reference", {}),
    ("artifacts/engineering-foundations.md", "engineering-foundations", "reference", {}),
    ("projects/README.md", "projects", "reference", {}),
    ("projects/p1-turbine-failure/README.md", "p1-turbine-failure", "reference", {}),
    ("projects/p2-financial-rag/README.md", "p2-financial-rag", "reference", {}),
    ("projects/p3-delivery-agents/README.md", "p3-delivery-agents", "reference", {}),
    ("projects/p4-deployed-assistant/README.md", "p4-deployed-assistant", "reference", {}),
    ("projects/p1-turbine-failure/report.md", "p1-report", "reference", {}),
    ("projects/p2-financial-rag/report.md", "p2-report", "reference", {}),
    ("projects/p3-delivery-agents/report.md", "p3-report", "reference", {}),
    ("projects/p4-deployed-assistant/report.md", "p4-report", "reference", {}),
    ("projects/p4-deployed-assistant/capstone/report.md", "p4-capstone-report", "reference", {}),
    ("docker/README.md", "docker", "reference", {}),
]
BY_SRC = {src: slug for src, slug, _, _ in DOCS}

LABEL_BOLD = re.compile(r"^\*\*([^*]+?):?\*\*:?\s*$")           # **Project:**  alone on a line
LABEL_QUOTE = re.compile(r"^([A-Za-z][A-Za-z0-9 /'’-]{0,48}):\s*$")  # > Baseline:
TABLE_SEP = re.compile(r"^\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")
LIST_ITEM = re.compile(r"^(\s*)([-*]|\d+\.)\s+(.*)$")
TASK = re.compile(r"^\[( |x|X)\]\s+(.*)$", re.S)


def md_plain(text):
    """Markdown to plain text for descriptions: no emphasis marks, no link syntax, no code ticks."""
    t = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    t = re.sub(r"[`*]|(?<!\w)_|_(?!\w)", "", t)
    return t


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"<[^>]+>", "", text).lower()).strip("-") or "section"


def split_row(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    cells, cur, i = [], "", 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s) and s[i + 1] == "|":
            cur += "\\|"; i += 2; continue
        if s[i] == "|":
            cells.append(cur.strip()); cur = ""
        else:
            cur += s[i]
        i += 1
    cells.append(cur.strip())
    return cells


class Doc:
    def __init__(self, src, slug, mode, opts):
        self.src, self.slug, self.mode, self.opts = src, slug, mode, opts
        self.lines = (ROOT / src).read_text().split("\n")
        self.fields, self.ids, self.warnings = [], {}, []
        self.fill = mode == "worksheet"
        self.tables = 0

    # ---- links -------------------------------------------------------------
    def href(self, target):
        if re.match(r"^(https?:|mailto:|#)", target):
            return target
        path, _, frag = target.partition("#")
        frag = "#" + frag if frag else ""
        resolved = (pathlib.PurePosixPath(self.src).parent / path)
        parts = []
        for p in resolved.parts:
            if p == "..":
                if not parts:
                    self.warnings.append(f"link leaves the repo: {target}")
                    return target
                parts.pop()
            elif p != ".":
                parts.append(p)
        rel = "/".join(parts)
        full = ROOT / rel
        if rel in BY_SRC:
            return f"{BY_SRC[rel]}.html{frag}"
        if not full.exists():
            self.warnings.append(f"{self.src}: link to missing path {target}")
            return target
        if full.is_dir():
            if (full / "index.html").exists():
                return f"../{rel}/index.html{frag}"
            meta = full / "meta.json"
            if rel.startswith("lessons/") and meta.exists():
                first = json.loads(meta.read_text())["lessons"][0]["file"]
                return f"../{rel}/{first}{frag}"
            return REPO_TREE + rel + frag
        if rel.endswith(".html"):
            return f"../{rel}{frag}"
        return REPO_BLOB + rel + frag

    # ---- inline ------------------------------------------------------------
    def inline(self, s):
        stash = []

        def keep(m):
            stash.append(f"<code>{E(m.group(1))}</code>")
            return f"\x00{len(stash) - 1}\x00"
        s = re.sub(r"`([^`]+)`", keep, s)
        s = E(s, quote=False)

        def link(m):
            h = self.href(html.unescape(m.group(2)))
            ext = ' rel="noopener"' if h.startswith("http") else ""
            return f'<a href="{E(h)}"{ext}>{m.group(1)}</a>'
        s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, s)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"(?<![\*\w])\*(?!\s)(.+?)(?<!\s)\*(?![\*\w])", r"<em>\1</em>", s)
        s = re.sub(r"(?<!\w)_(?!\s)(.+?)(?<!\s)_(?!\w)", r"<em>\1</em>", s)
        return re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], s)

    # ---- fields ------------------------------------------------------------
    def field(self, kind, ln, c=None):
        base = f"f{ln}" + (f"-{c}" if c is not None else "")
        fid = base if kind != "insert" else f"a{ln}"
        self.fields.append({"id": fid, "kind": kind, "ln": ln, **({"c": c} if c is not None else {})})
        return fid

    def input_html(self, kind, ln, label, c=None, multiline=False):
        fid = self.field(kind, ln, c)
        if multiline:
            return (f'<textarea data-fid="{fid}" rows="4" aria-label="{E(label)}"></textarea>')
        return f'<input type="text" data-fid="{fid}" aria-label="{E(label)}">'

    # ---- blocks ------------------------------------------------------------
    def render(self):
        L, n, i, out = self.lines, len(self.lines), 0, []
        self.h2 = []
        while i < n:
            line = L[i]
            if not line.strip():
                i += 1; continue
            if line.startswith("```"):
                lang = line[3:].strip(); j = i + 1; code = []
                while j < n and not L[j].startswith("```"):
                    code.append(L[j]); j += 1
                out.append(f'<pre><code{" class=lang-" + E(lang) if lang else ""}>{E(chr(10).join(code))}</code></pre>')
                i = j + 1; continue
            m = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
            if m:
                lvl, text = len(m.group(1)), m.group(2)
                hid = self.unique_id(slugify(text))
                if lvl == 2:
                    self.h2.append((hid, re.sub(r"<[^>]+>", "", self.inline(text))))
                if lvl == 1:
                    text = self.opts.get("title", text)
                    if not hasattr(self, "title"):
                        self.title = re.sub(r"<[^>]+>", "", self.inline(text))
                out.append(f'<h{lvl} id="{hid}">{self.inline(text)}</h{lvl}>')
                i += 1; continue
            if re.match(r"^\s*(-{3,}|\*{3,}|_{3,})\s*$", line):
                out.append("<hr>"); i += 1; continue
            if line.lstrip().startswith(">"):
                i = self.quote(i, out); continue
            if line.lstrip().startswith("|") and i + 1 < n and TABLE_SEP.match(L[i + 1].strip()):
                i = self.table(i, out); continue
            if LIST_ITEM.match(line):
                i = self.list(i, out); continue
            i = self.paragraph(i, out)
        return "\n".join(out)

    def unique_id(self, base):
        k = self.ids.get(base, 0); self.ids[base] = k + 1
        return base if k == 0 else f"{base}-{k + 1}"

    def starts_block(self, line, nxt):
        s = line.lstrip()
        return (not line.strip() or line.startswith(("```", "#")) or s.startswith(">")
                or bool(LIST_ITEM.match(line)) or bool(re.match(r"^-{3,}\s*$", line))
                or (s.startswith("|") and nxt is not None and bool(TABLE_SEP.match(nxt.strip()))))

    def paragraph(self, i, out):
        L, n = self.lines, len(self.lines)
        j = i; rows = []
        while j < n and (j == i or not self.starts_block(L[j], L[j + 1] if j + 1 < n else None)):
            rows.append((j, L[j])); j += 1
        text_rows = []
        key = rows[0][1].startswith("**Key.**")
        if key and self.opts.get("answers") and self.fill:
            fid = self.field("insert", i)
            out.append('<div class="answer"><label>Your answer'
                       f'<textarea data-fid="{fid}" rows="5"></textarea></label></div>')
        for ln, text in rows:
            m = LABEL_BOLD.match(text.strip())
            if m and self.fill:
                if text_rows:
                    out.append(f"<p>{self.inline(' '.join(text_rows))}</p>"); text_rows = []
                label = m.group(1).rstrip(":")
                out.append(f'<div class="fill"><span>{E(label)}:</span>{self.input_html("label", ln, label)}</div>')
            else:
                text_rows.append(text.strip())
        if text_rows:
            body = self.inline(" ".join(text_rows))
            out.append(f"<p>{body}</p>" if not key else
                       f'<details class="key"><summary>Show marking key</summary><p>{body}</p></details>')
        return j

    def quote(self, i, out):
        L, n = self.lines, len(self.lines)
        j = i; rows = []
        while j < n and L[j].lstrip().startswith(">"):
            rows.append((j, re.sub(r"^\s*>\s?", "", L[j]))); j += 1
        parts, text_rows = [], []

        def flush():
            if text_rows:
                parts.append(f"<p>{self.inline(' '.join(text_rows))}</p>"); text_rows.clear()
        blank_only = all(not t.strip() for _, t in rows)
        if blank_only and self.fill:
            parts.append(self.input_html("quote", rows[0][0], "Your notes", multiline=True))
        else:
            for ln, t in rows:
                s = t.strip()
                m = LABEL_BOLD.match(s) or LABEL_QUOTE.match(s)
                if m and self.fill:
                    flush()
                    label = m.group(1).rstrip(":")
                    parts.append(f'<div class="fill"><span>{E(label)}:</span>{self.input_html("label", ln, label)}</div>')
                elif not s:
                    flush()
                else:
                    text_rows.append(s)
            flush()
        out.append(f'<blockquote class="{"fillbox" if blank_only or any("fill" in p for p in parts) else "note"}">' + "".join(parts) + "</blockquote>")
        return j

    def table(self, i, out):
        L, n = self.lines, len(self.lines)
        head = split_row(L[i]); j = i + 2; body = []
        while j < n and L[j].lstrip().startswith("|"):
            body.append((j, split_row(L[j]))); j += 1
        fillable = self.fill and any(c == "" for _, r in body for c in r)
        self.tables += 1
        cls = ' class="fillable" data-csv="%s"' % self.tables if fillable else ""
        h = "".join(f'<th scope="col">{self.inline(c)}</th>' for c in head)
        rows = []
        for ln, r in body:
            r = (r + [""] * len(head))[:len(head)] if len(r) < len(head) else r
            tds = []
            for c, cell in enumerate(r):
                if fillable and cell == "":
                    tds.append("<td>" + self.input_html("cell", ln, f"{head[c] if c < len(head) else ''} for {re.sub(r'<[^>]+>', '', self.inline(r[0])) or 'row'}", c=c) + "</td>")
                else:
                    tds.append(f"<td>{self.inline(cell)}</td>")
            rows.append("<tr>" + "".join(tds) + "</tr>")
        out.append(f'<div class="table-scroll"><table{cls}><thead><tr>{h}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>')
        if fillable:
            out.append(f'<p class="table-actions"><button type="button" class="btn small" data-csv-btn="{self.tables}">Download this table as CSV</button></p>')
        return j

    def list(self, i, out):
        L, n = self.lines, len(self.lines)
        ordered = bool(re.match(r"^\s*\d+\.", L[i]))
        items, j = [], i
        while j < n:
            m = LIST_ITEM.match(L[j])
            if not m or bool(re.match(r"^\s*\d+\.", L[j])) != ordered:
                break
            ln, text = j, m.group(3); j += 1
            while j < n and L[j].strip() and L[j].startswith("  ") and not LIST_ITEM.match(L[j]):
                text += " " + L[j].strip(); j += 1
            items.append((ln, text))
            k = j
            while k < n and not L[k].strip():
                k += 1
            if k < n and k > j and LIST_ITEM.match(L[k]) and bool(re.match(r"^\s*\d+\.", L[k])) == ordered:
                j = k
        tag = "ol" if ordered else "ul"
        lis, tasks = [], False
        for ln, text in items:
            t = TASK.match(text)
            if t:
                tasks = True
                checked = t.group(1) != " "
                body = self.inline(t.group(2))
                if self.fill:
                    if checked:
                        self.warnings.append(f"{self.src}:{ln + 1} worksheet starts with a ticked box")
                    fid = self.field("check", ln)
                    lis.append(f'<li class="task"><label><input type="checkbox" data-fid="{fid}"> <span>{body}</span></label></li>')
                else:
                    lis.append(f'<li class="task"><label><input type="checkbox" disabled{" checked" if checked else ""}> <span>{body}</span></label></li>')
            else:
                lis.append(f"<li>{self.inline(text)}</li>")
        start = ""
        if ordered:
            num = re.match(r"^\s*(\d+)\.", L[i]).group(1)
            start = f' start="{num}"' if num != "1" else ""
        out.append(f'<{tag}{start}{" class=tasks" if tasks else ""}>{"".join(lis)}</{tag}>')
        return j


def page(doc, body):
    title = doc.title
    first_p = next((l for l in doc.lines if l.strip() and not l.startswith(("#", ">", "|", "-", "*", "`", "!")) and not LABEL_BOLD.match(l.strip())), title)
    desc = plain(md_plain(first_p), 158)
    if "title" in doc.opts:
        desc = plain(f"{title}. {md_plain(first_p)}", 158)
    if len(desc) < 110:
        kind = "A fill-in worksheet" if doc.fill else "A reference page"
        desc = plain(f"{desc} {kind} from the free {NAME} course.", 158)
    path = f"docs/{doc.slug}.html"
    ld = lesson_jsonld(title, desc, path, NAME)
    ld["learningResourceType"] = "worksheet" if doc.fill else "reference"
    toc = ""
    if len(doc.h2) >= 4:
        toc = ('<nav class="toc" aria-label="On this page"><h2>On this page</h2><ol>'
               + "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in doc.h2) + "</ol></nav>")
    # The title leads the page; the toolbar and contents come after it.
    head_html = ""
    if body.startswith("<h1"):
        head_html, _, body = body.partition("</h1>")
        head_html += "</h1>"
        body = body.lstrip("\n")
    data = json.dumps({"slug": doc.slug, "lines": doc.lines, "fields": doc.fields}, ensure_ascii=False).replace("</", "<\\/")
    md_link = f"../{doc.src}"
    gh = REPO_BLOB + doc.src
    if doc.fill:
        note = ("What you tick or type stays in this browser. To keep it, download your answers as a "
                "markdown file, or print this page or save it as a PDF.")
        actions = (f'<a class="btn" href="{md_link}" download>Download blank (.md)</a>'
                   '<button type="button" class="btn primary" id="dl-answers">Download my answers (.md)</button>'
                   '<button type="button" class="btn" onclick="window.print()">Print or save as PDF</button>'
                   '<button type="button" class="btn quiet" id="clear-answers">Clear my answers</button>')
    else:
        note = "A reference page. The source is a markdown file in the repository."
        actions = (f'<a class="btn" href="{md_link}" download>Download (.md)</a>'
                   '<button type="button" class="btn" onclick="window.print()">Print or save as PDF</button>')
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{E(title)} | {E(NAME)}</title>
{head_meta(title, desc, path, ld)}
{STYLE}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><nav aria-label="Site"><a href="../index.html">{E(NAME)}</a> <span aria-hidden="true">/</span> <a href="index.html">Worksheets and references</a></nav></header>
<main id="main">
{head_html}
<div class="toolbar" role="group" aria-label="Page actions">{actions}<a class="btn quiet" href="{E(gh)}" rel="noopener">View on GitHub</a></div>
<p class="note" id="save-note">{note}</p>
{toc}
{body}
</main>
<footer class="foot"><p>Source: <a href="{E(gh)}" rel="noopener"><code>{E(doc.src)}</code></a>. This page is generated; edit the markdown file.</p></footer>
<script type="application/json" id="doc-data">{data}</script>
{SCRIPT if doc.fill else ""}
</body>
</html>
"""


SCRIPT = (ROOT / "scripts" / "_doc_script.html").read_text()


def index_page(built):
    def card(d):
        return (f'<li><a class="card" href="{d.slug}.html"><h3>{E(d.title)}</h3><p>{E(d.blurb)}</p></a>'
                f'<a class="mdlink" href="../{d.src}" download>Download .md</a></li>')
    groups = [("Worksheets you can fill in", [d for d in built if d.fill],
               "Tick boxes and type answers. They save in your browser, and you can download your answers as a markdown file or print them."),
              ("Reference", [d for d in built if not d.fill],
               "The curriculum, glossary and project write-ups, as readable pages.")]
    body = "".join(f'<h2>{t}</h2><p>{n}</p><ul class="cards">{"".join(card(d) for d in ds)}</ul>' for t, ds, n in groups)
    sop = ('<h2>Checklists</h2><p>Operating checklists with killer items and hard gates.</p>'
           '<ul class="cards"><li><a class="card" href="../artifacts/sop/index.html"><h3>SOP checklists</h3>'
           '<p>Aviation-style checklists for LLM work, with a separate non-normal checklist for when something is already wrong.</p></a></li></ul>')
    desc = ("Fill-in worksheets and reference pages for the free LLM systems course: intake sheets, "
            "a scorecard, an exam, a rubric, the curriculum and glossary.")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Worksheets and references | {E(NAME)}</title>
{head_meta("Worksheets and references", desc, "docs/", {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Worksheets and references", "description": desc, "url": SITE + "docs/", "isPartOf": {"@type": "Course", "name": NAME, "url": SITE}}, og_type="website")}
{STYLE}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><nav aria-label="Site"><a href="../index.html">{E(NAME)}</a></nav></header>
<main id="main">
<h1>Worksheets and references</h1>
<p class="lead">Everything that used to be a raw markdown file, as a page you can use.</p>
{body}{sop}
</main>
<footer class="foot"><p>These pages are generated from the markdown files in the repository.</p></footer>
</body>
</html>
"""


def main():
    out_dir = ROOT / "docs"
    out_dir.mkdir(exist_ok=True)
    built, problems = [], []
    for src, slug, mode, opts in DOCS:
        d = Doc(src, slug, mode, opts)
        body = d.render()
        d.title = getattr(d, "title", slug)
        d.blurb = plain(md_plain(next((l for l in d.lines if l.strip() and not l.startswith(("#", ">", "|", "-", "*", "`")) and not LABEL_BOLD.match(l.strip())), d.title)), 150)
        (out_dir / f"{slug}.html").write_text(page(d, body))
        problems += d.warnings
        built.append(d)
    (out_dir / "index.html").write_text(index_page(built))
    for stale in out_dir.glob("*.html"):
        if stale.stem not in {s for _, s, _, _ in DOCS} | {"index"}:
            stale.unlink()
    if problems:
        print("\n".join(sorted(set(problems))))
        raise SystemExit(f"{len(set(problems))} problem(s) in the markdown pages")
    nf = sum(len(d.fields) for d in built)
    print(f"built docs/ — {len(built)} pages ({sum(d.fill for d in built)} worksheets, {nf} fields)")


if __name__ == "__main__":
    main()
