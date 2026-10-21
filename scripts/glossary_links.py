#!/usr/bin/env python3
"""Turn glossary terms in lesson prose into hover/focus/tap popovers. Stdlib only.

The definitions come from GLOSSARY.md, so the glossary stays the single source.
build_lessons.py calls Linker once per build and Linker.for_lesson() once per
lesson; nothing is marked up by hand in the content modules.

A wrong popover is worse than a missing one, so matching is conservative:

  * Multi-word terms ("context window", "chain-of-thought") link on their own.
  * Acronyms and code-like names ("GPTQ", "FP8", "datetime64") link
    case-sensitively, three characters or more.
  * A single ordinary word links only if it is listed in
    scripts/glossary_link_single.txt. Words with a second everyday meaning in
    this course ("temperature" on the turbine data, "transformer", "precision",
    "alignment") are left off that list on purpose.
  * scripts/glossary_nolink.txt vetoes any form outright.
  * A form that two glossary entries both claim is dropped.
  * Only the first occurrence in a lesson links, and never a term the lesson
    itself defines in a terms block (the popover would repeat the text).
  * Only running prose is touched: not code, headings, labels, links, diagrams,
    quizzes or worked-example blocks (those are copied onto the revision sheet,
    where the popover script does not run).

    python3 scripts/glossary_links.py --report   # every built link, in context
"""
import html
import json
import pathlib
import re
import sys
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
GLOSSARY = ROOT / "GLOSSARY.md"
SINGLE_OK = ROOT / "scripts" / "glossary_link_single.txt"
NOLINK = ROOT / "scripts" / "glossary_nolink.txt"

# Blocks whose rendered HTML is running prose. Everything else is left alone.
LINKED_KINDS = {"p", "ul", "callout", "terms"}

SKIP_TAGS = {"a", "code", "pre", "svg", "h1", "h2", "h3", "dfn", "script", "style",
             "button", "figcaption"}
SKIP_CLASSES = {"label", "know-label", "know-eg-label", "roadmap-num",
                "roadmap-title", "pill", "link-note"}
VOID = {"br", "img", "hr", "meta", "link", "input", "wbr"}


def read_list(path):
    if not path.exists():
        return set()
    return {l.strip().lower() for l in path.read_text().splitlines()
            if l.strip() and not l.startswith("#")}


def read_vetoes(path):
    """(global forms, {lesson slug: forms}) from glossary_nolink.txt.
    "form" vetoes it everywhere; "lesson-slug :: form" only in that lesson."""
    everywhere, scoped = set(), {}
    for line in read_list(path):
        if " :: " in line:
            lesson, form = (x.strip() for x in line.split(" :: ", 1))
            scoped.setdefault(lesson, set()).add(form)
        else:
            everywhere.add(line)
    return everywhere, scoped


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def md_to_html(s):
    """The glossary is plain markdown: **bold**, *italic*, `code`. Nothing else."""
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*([^*\s][^*]*?)\*", r"<em>\1</em>", s)
    return s


def parse_glossary():
    """[(name, definition_html)] in file order."""
    entries = []
    for para in re.split(r"\n\s*\n", GLOSSARY.read_text()):
        m = re.match(r"\*\*(.+?)\*\*\s+—\s+(.*)", para.strip(), re.S)
        if m:
            entries.append((m.group(1).strip(), " ".join(m.group(2).split())))
    return entries


def surface_forms(name):
    """(form, case_sensitive) pairs a glossary entry answers to in prose."""
    if "⊃" in name or re.search(r"\s(vs|versus|against)\s", name):
        return []
    out = []
    base = re.sub(r"\s*\([^)]*\)", "", name).strip()
    for part in (p.strip() for p in base.split(" / ")):
        if part:
            out.append(part)
    forms = [(p, None) for p in out]          # None: decide below
    for alias in re.findall(r"\(([^)]+)\)", name):
        alias = alias.strip()
        if re.fullmatch(r"[A-Za-z0-9+]{3,}", alias) and sum(c.isupper() for c in alias) >= 2:
            forms.append((alias, True))
    return forms


def classify(form, case_sensitive, single_ok):
    """Return the case-sensitivity to match with, or None to not link at all."""
    if re.search(r"[\s\-_./@]", form):               # multi-word or compound
        if len(form) < 6:
            return None
        return bool(case_sensitive)
    # one token
    if len(form) >= 3 and (sum(c.isupper() for c in form) >= 2 or re.search(r"\d", form)):
        return True                                  # GPTQ, FP8, datetime64, BM25
    if form.lower() in single_ok:
        return bool(case_sensitive)
    return None


class _Rewriter(HTMLParser):
    """Re-emit HTML verbatim, wrapping glossary terms found in prose text nodes."""

    def __init__(self, linker):
        super().__init__(convert_charrefs=False)
        self.lk = linker
        self.out = []
        self.stack = []                              # (tag, skipping)

    def _skipping(self):
        return any(s for _, s in self.stack)

    def handle_starttag(self, tag, attrs):
        self.out.append(self.get_starttag_text())
        if tag in VOID:
            return
        cls = set(dict(attrs).get("class", "").split())
        self.stack.append((tag, tag in SKIP_TAGS or bool(cls & SKIP_CLASSES)))

    def handle_startendtag(self, tag, attrs):
        self.out.append(self.get_starttag_text())

    def handle_endtag(self, tag):
        self.out.append(f"</{tag}>")
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        self.out.append(data if self._skipping() else self.lk._link_text(data))

    def handle_entityref(self, name):
        self.out.append(f"&{name};")

    def handle_charref(self, name):
        self.out.append(f"&#{name};")

    def handle_comment(self, data):
        self.out.append(f"<!--{data}-->")

    def handle_decl(self, decl):
        self.out.append(f"<!{decl}>")


class Linker:
    def __init__(self):
        single_ok = read_list(SINGLE_OK)
        nolink, self.scoped_vetoes = read_vetoes(NOLINK)
        self.entries = {}                            # id -> (name, def_html)
        claims = {}                                  # lowered form -> {ids}
        cands = []                                   # (form, cs, id)
        for name, definition in parse_glossary():
            eid = slug(name)
            if not eid or eid in self.entries:
                continue
            self.entries[eid] = (name, md_to_html(definition))
            for form, cs in surface_forms(name):
                if form.lower() in nolink:
                    continue
                mode = classify(form, cs, single_ok)
                if mode is None:
                    continue
                claims.setdefault(form.lower(), set()).add(eid)
                cands.append((form, mode, eid))
        # a form two entries both answer to is ambiguous: link neither
        self.forms = {}                              # form -> (cs, id)
        for form, mode, eid in cands:
            if len(claims[form.lower()]) == 1:
                self.forms[form] = (mode, eid)
        self.form_names = {eid: set() for eid in self.entries}
        for form, (_, eid) in self.forms.items():
            self.form_names[eid].add(form.lower())
        for eid, (name, _) in self.entries.items():     # for "defined in this lesson"
            self.form_names[eid] |= {f.lower() for f, _ in surface_forms(name)}
        self.rx_cs, self.rx_ci = self._compile()

    def _compile(self):
        def build(cs):
            fs = sorted((f for f, (m, _) in self.forms.items() if m is cs),
                        key=len, reverse=True)
            if not fs:
                return None
            body = "|".join(re.escape(f) + (r"(?:s|es)?" if f[-1].isalpha() and cs is False else "")
                            for f in fs)
            return re.compile(rf"(?<![\w\-/.@_])({body})(?![\w@_]|-\w|\.\w)",
                              0 if cs else re.I)
        return build(True), build(False)

    # ---- per-lesson ----
    def for_lesson(self, defined_labels=(), lesson_slug=None):
        lk = object.__new__(Linker)
        lk.__dict__.update(self.__dict__)
        lk.used = {}
        lk.skip = set()
        labels = {re.sub(r"s$", "", l.strip().lower()) for l in defined_labels}
        labels |= {re.sub(r"s$", "", f) for f in self.scoped_vetoes.get(lesson_slug, ())}
        for eid, names in self.form_names.items():
            if any(re.sub(r"s$", "", n) in labels for n in names):
                lk.skip.add(eid)
        return lk

    def link(self, kind, rendered):
        if kind not in LINKED_KINDS:
            return rendered
        rw = _Rewriter(self)
        rw.feed(rendered)
        rw.close()
        return "".join(rw.out)

    def _link_text(self, text):
        hits = []
        for rx, cs in ((self.rx_cs, True), (self.rx_ci, False)):
            if rx is None:
                continue
            for m in rx.finditer(text):
                matched = m.group(1)
                key = matched if cs else self._ci_key(matched)
                if key is None:
                    continue
                hits.append((m.start(1), m.end(1), self.forms[key][1]))
        hits.sort(key=lambda h: (h[0], -(h[1] - h[0])))
        out, pos = [], 0
        for s, e, eid in hits:
            if s < pos or eid in self.used or eid in self.skip:
                continue
            out.append(text[pos:s])
            out.append(f'<dfn class="gl" tabindex="0" data-gl="{eid}">{text[s:e]}</dfn>')
            self.used[eid] = self.entries[eid]
            pos = e
        out.append(text[pos:])
        return "".join(out)

    def _ci_key(self, matched):
        low = matched.lower()
        for cand in (low, re.sub(r"(es|s)$", "", low)):
            for form, (cs, _) in self.forms.items():
                if cs is False and form.lower() == cand:
                    return form
        return None

    def assets(self):
        """The definitions this lesson uses, plus the script that shows them."""
        if not self.used:
            return ""
        data = {eid: {"t": n, "d": d} for eid, (n, d) in self.used.items()}
        blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
        return (f'<script type="application/json" id="gl-defs">{blob}</script>\n'
                f"{POPOVER_JS}\n")


POPOVER_JS = """<script>
(function () {
  const holder = document.getElementById("gl-defs");
  if (!holder) return;
  const defs = JSON.parse(holder.textContent);
  const tip = document.createElement("div");
  tip.className = "gl-tip"; tip.id = "gl-tip"; tip.setAttribute("role", "tooltip"); tip.hidden = true;
  document.body.appendChild(tip);
  let cur = null;
  function place(el) {
    const r = el.getBoundingClientRect(), w = tip.offsetWidth, h = tip.offsetHeight;
    const left = Math.max(12, Math.min(r.left + window.scrollX, window.scrollX + document.documentElement.clientWidth - w - 12));
    const below = r.bottom + h + 12 < window.innerHeight || r.top < h + 12;
    tip.style.left = left + "px";
    tip.style.top = (below ? r.bottom + window.scrollY + 6 : r.top + window.scrollY - h - 6) + "px";
  }
  function show(el) {
    const d = defs[el.dataset.gl]; if (!d) return;
    hide();
    tip.innerHTML = '<strong class="gl-t"></strong>' + d.d;
    tip.firstChild.textContent = d.t;
    tip.hidden = false; cur = el; el.setAttribute("aria-describedby", "gl-tip");
    place(el);
  }
  function hide() {
    if (cur) cur.removeAttribute("aria-describedby");
    tip.hidden = true; cur = null;
  }
  const term = t => t.closest && t.closest("dfn.gl");
  document.addEventListener("mouseover", e => { const el = term(e.target); if (el && el !== cur) show(el); });
  document.addEventListener("mouseout", e => { if (term(e.target) && !(e.relatedTarget && tip.contains(e.relatedTarget))) hide(); });
  document.addEventListener("focusin", e => { const el = term(e.target); if (el) show(el); });
  document.addEventListener("focusout", e => { if (term(e.target)) hide(); });
  document.addEventListener("click", e => {
    const el = term(e.target);
    if (el) { cur === el ? hide() : show(el); } else if (!tip.contains(e.target)) hide();
  });
  document.addEventListener("keydown", e => { if (e.key === "Escape") hide(); });
  window.addEventListener("scroll", () => { if (cur) place(cur); }, { passive: true });
})();
</script>"""


def report():
    pat = re.compile(r'(.{0,45})<dfn class="gl"[^>]*data-gl="([^"]+)">(.*?)</dfn>(.{0,35})', re.S)
    total = 0
    for f in sorted((ROOT / "lessons").glob("*/lsn-*.html")):
        hits = pat.findall(f.read_text())
        if not hits:
            continue
        print(f"\n{f.parent.name}/{f.name}  ({len(hits)})")
        for before, eid, shown, after in hits:
            ctx = re.sub(r"<[^>]+>", "", before) + "[[" + shown + "]]" + re.sub(r"<[^>]+>", "", after)
            print(f"   {eid:<34} {ctx!r}")
        total += len(hits)
    print(f"\n{total} popovers")


if __name__ == "__main__":
    if "--report" in sys.argv:
        report()
    else:
        lk = Linker()
        print(f"{len(lk.entries)} glossary entries, {len(lk.forms)} linkable forms")
