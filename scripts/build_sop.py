#!/usr/bin/env python3
"""Build one self-contained HTML SOP from the markdown checklists.

Markdown stays the source of truth — it is what gets edited and diffed. This
emits a single file that works from file://, remembers which boxes are ticked,
and lets you jump into a sub-checklist and return to the exact item you left.

Deliberately not a general markdown parser. It handles the forms these files
actually use and raises on anything else, because silently dropping a checklist
item is precisely the failure this repo is arranged around preventing.
"""
import html, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "artifacts" / "sop"

ORDER = ["README", "training", "deep-learning", "fine-tuning", "generative-ai",
         "llm-engineering", "tuning", "measurement", "judging", "security",
         "mcp", "hardware", "incident"]

E = html.escape


SECTION_IDS = set(ORDER)


def inline(t: str) -> str:
    """Bold, code, and links. Links to other SOPs become in-page jumps."""
    t = E(t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", t)

    def link(m):
        label, target = m.group(1), m.group(2)
        stem = pathlib.Path(target).stem
        if target.endswith(".md") and stem in SECTION_IDS:
            return f'<a class="jump" data-to="{stem}">{label} &rarr;</a>'
        if target.endswith(".md"):
            # a markdown file that is not a section: open it where it lives
            href = target if target.startswith(("http", "../")) else f"../{target}"
            return f'<a href="{href}">{label}</a>'
        return f'<a href="{target}" target="_blank" rel="noopener">{label}</a>'

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, t)


def parse(path: pathlib.Path) -> dict:
    doc = {"id": path.stem, "title": "", "blocks": []}
    lines = path.read_text().split("\n")
    i, n = 0, len(lines)
    item_no = 0

    while i < n:
        raw = lines[i]
        s = raw.strip()

        if not s or s == "---":
            i += 1
        elif s.startswith("# "):
            doc["title"] = s[2:].strip()
            i += 1
        elif s.startswith("### "):
            doc["blocks"].append({"t": "h3", "text": s[4:].strip()})
            i += 1
        elif s.startswith("## "):
            doc["blocks"].append({"t": "h2", "text": s[3:].strip()})
            i += 1
        elif s.startswith("- [ ]"):
            body = s[5:].strip()
            killer = body.startswith("☠")
            if killer:
                body = body[1:].strip()
            item_no += 1
            doc["blocks"].append({"t": "item", "killer": killer,
                                  "id": f"{doc['id']}-{item_no}", "text": body})
            i += 1
        elif s.startswith("- "):
            doc["blocks"].append({"t": "bullet", "text": s[2:].strip()})
            i += 1
        elif s.startswith(">"):
            quote = []
            while i < n and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip(">").strip())
                i += 1
            doc["blocks"].append({"t": "quote", "text": " ".join(q for q in quote if q)})
        elif s.startswith("|"):
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(set(c) <= set("-: ") for c in cells):
                    rows.append(cells)
                i += 1
            doc["blocks"].append({"t": "table", "rows": rows})
        elif s.startswith("```"):
            code = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                code.append(lines[i]); i += 1
            i += 1
            doc["blocks"].append({"t": "code", "text": "\n".join(code)})
        elif s.startswith("**GATE"):
            doc["blocks"].append({"t": "gate", "text": s.strip("*")})
            i += 1
        else:
            para = []
            while i < n:
                cur = lines[i].strip()
                if (not cur or cur == "---" or cur.startswith(("#", "- ", ">", "|", "```", "**GATE"))):
                    break
                para.append(cur)
                i += 1
            doc["blocks"].append({"t": "p", "text": " ".join(para)})

    return doc


def render(doc: dict) -> str:
    out = [f'<section class="sop" id="sop-{doc["id"]}" hidden>']
    out.append(f'<div class="sop-head"><button class="back" hidden>&larr; Return</button>'
               f'<h1>{E(doc["title"])}</h1>'
               f'<div class="progress"><span class="bar"><i></i></span>'
               f'<span class="count"></span>'
               f'<button class="reset" title="Clear ticks on this checklist">reset</button></div></div>')
    for b in doc["blocks"]:
        t = b["t"]
        if t == "h2":
            out.append(f'<h2>{inline(b["text"])}</h2>')
        elif t == "h3":
            out.append(f'<h3>{inline(b["text"])}</h3>')
        elif t == "p":
            out.append(f'<p>{inline(b["text"])}</p>')
        elif t == "bullet":
            out.append(f'<p class="bullet">{inline(b["text"])}</p>')
        elif t == "quote":
            out.append(f'<blockquote>{inline(b["text"])}</blockquote>')
        elif t == "gate":
            out.append(f'<div class="gate">{inline(b["text"])}</div>')
        elif t == "code":
            out.append(f'<pre><code>{E(b["text"])}</code></pre>')
        elif t == "table":
            head, *body = b["rows"]
            th = "".join(f"<th>{inline(c)}</th>" for c in head)
            tr = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body)
            out.append(f"<table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>")
        elif t == "item":
            k = " killer" if b["killer"] else ""
            out.append(f'<label class="item{k}" id="{b["id"]}">'
                       f'<input type="checkbox" data-id="{b["id"]}">'
                       f'<span class="tick"></span>'
                       f'<span class="body">{"<b class=skull>☠</b> " if b["killer"] else ""}'
                       f'{inline(b["text"])}</span></label>')
        else:
            sys.exit(f"unhandled block type {t!r} in {doc['id']}")
    out.append("</section>")
    return "\n".join(out)


docs = []
for name in ORDER:
    p = SRC / f"{name}.md"
    if not p.exists():
        sys.exit(f"missing {p}")
    docs.append(parse(p))

# every checklist item in the markdown must survive into the HTML
md_items = sum(len(re.findall(r"^- \[ \]", (SRC / f"{d['id']}.md").read_text(), re.M)) for d in docs)
html_items = sum(sum(1 for b in d["blocks"] if b["t"] == "item") for d in docs)
assert md_items == html_items, f"lost items: {md_items} in markdown, {html_items} in HTML"

nav = "".join(
    f'<button class="navbtn{" master" if d["id"] == "README" else ""}" data-to="{d["id"]}">'
    f'{E("Master" if d["id"] == "README" else d["title"].split("—")[0].strip())}'
    f'<span class="navcount" data-for="{d["id"]}"></span></button>'
    for d in docs)

page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Master SOP — Building LLM Systems</title>
<style>
:root {{
  --bg:#0f1117; --surface:#1a1d27; --surface2:#242736; --border:#2e3248;
  --accent:#6c8fff; --accent2:#a78bfa; --green:#34d399; --yellow:#fbbf24; --red:#f87171;
  --text:#e2e8f0; --muted:#94a3b8; --code-bg:#0d1117;
}}
* {{ box-sizing:border-box; }}
[hidden] {{ display:none !important; }}
body {{ margin:0; background:var(--bg); color:var(--text); line-height:1.6;
       font:16px/1.6 -apple-system,'Segoe UI',sans-serif; }}
nav {{ position:sticky; top:0; z-index:10; background:var(--surface);
      border-bottom:1px solid var(--border); padding:8px 12px;
      display:flex; gap:6px; flex-wrap:wrap; }}
.brand {{ align-self:center; margin-right:6px; padding:5px 11px; border-radius:999px;
         background:var(--accent2); color:#0f1117; font-size:.7em; font-weight:800;
         letter-spacing:.09em; }}
.navbtn {{ background:var(--surface2); color:var(--muted); border:1px solid var(--border);
          border-radius:999px; padding:5px 12px; font-size:.8em; cursor:pointer; }}
.navbtn:hover {{ color:var(--text); }}
.navbtn.master {{ border-color:var(--accent2); color:var(--accent2); }}
.navbtn.on {{ background:var(--accent); color:#0f1117; border-color:var(--accent); font-weight:600; }}
.navcount {{ margin-left:6px; opacity:.75; font-variant-numeric:tabular-nums; }}
main {{ max-width:880px; margin:0 auto; padding:28px 20px 100px; }}
.sop-head {{ margin-bottom:20px; }}
h1 {{ font-size:1.7em; margin:6px 0 10px; }}
h2 {{ color:var(--accent); font-size:1.2em; margin:34px 0 10px;
     border-bottom:1px solid var(--border); padding-bottom:6px; }}
h3 {{ color:var(--accent2); font-size:1.02em; margin:24px 0 8px; }}
p {{ margin:10px 0; }} p.bullet {{ padding-left:16px; position:relative; }}
p.bullet::before {{ content:"·"; position:absolute; left:4px; color:var(--muted); }}
a {{ color:var(--accent); }}
a.jump {{ cursor:pointer; text-decoration:underline; text-underline-offset:3px; }}
code {{ background:var(--code-bg); padding:1px 5px; border-radius:4px; font-size:.9em; }}
pre {{ background:var(--code-bg); padding:12px 14px; border-radius:8px; overflow-x:auto; }}
pre code {{ background:none; padding:0; }}
blockquote {{ margin:16px 0; padding:14px 18px; background:var(--surface);
             border-left:4px solid var(--accent2); border-radius:6px; }}
.gate {{ margin:16px 0; padding:12px 16px; background:rgba(248,113,113,.09);
        border:1px solid var(--red); border-radius:8px; color:var(--red); font-weight:600; }}
table {{ width:100%; border-collapse:collapse; margin:16px 0; font-size:.94em; }}
th,td {{ text-align:left; padding:8px 10px; border-bottom:1px solid var(--border); vertical-align:top; }}
th {{ color:var(--muted); font-size:.85em; text-transform:uppercase; letter-spacing:.05em; }}
.item {{ display:flex; gap:10px; align-items:flex-start; padding:9px 12px; margin:5px 0;
        background:var(--surface); border:1px solid var(--border); border-radius:7px;
        cursor:pointer; transition:background .12s; }}
.item:hover {{ background:var(--surface2); }}
.item input {{ display:none; }}
.tick {{ flex:0 0 18px; height:18px; margin-top:2px; border:2px solid var(--muted);
        border-radius:4px; position:relative; }}
.item.killer .tick {{ border-color:var(--red); }}
.item input:checked ~ .tick {{ background:var(--green); border-color:var(--green); }}
.item input:checked ~ .tick::after {{ content:"✓"; position:absolute; inset:-3px 0 0 2px;
        color:#0f1117; font-size:14px; font-weight:800; }}
.item input:checked ~ .body {{ opacity:.5; text-decoration:line-through; }}
.skull {{ color:var(--red); }}
.item.flash {{ animation:flash 1.6s ease-out; }}
@keyframes flash {{ 0%,40% {{ background:rgba(108,143,255,.28); border-color:var(--accent); }}
                   100% {{ background:var(--surface); }} }}
.progress {{ display:flex; align-items:center; gap:10px; font-size:.85em; color:var(--muted); }}
.bar {{ flex:1; height:6px; background:var(--surface2); border-radius:3px; overflow:hidden; }}
.bar i {{ display:block; height:100%; width:0; background:var(--green); transition:width .2s; }}
.count {{ font-variant-numeric:tabular-nums; white-space:nowrap; }}
.reset, .back {{ background:var(--surface2); color:var(--muted); border:1px solid var(--border);
        border-radius:6px; padding:4px 10px; font-size:.85em; cursor:pointer; }}
.reset:hover, .back:hover {{ color:var(--text); }}
.back {{ display:inline-block; margin-bottom:10px; border-color:var(--accent); color:var(--accent); }}
</style></head><body>
<nav><span class="brand">MASTER SOP</span>{nav}</nav>
<main>{"".join(render(d) for d in docs)}</main>
<script>
const KEY = "pgp-sop-v1";
const load = () => {{ try {{ return JSON.parse(localStorage.getItem(KEY)) || {{}}; }} catch {{ return {{}}; }} }};
const save = s => {{ try {{ localStorage.setItem(KEY, JSON.stringify(s)); }} catch {{}} }};
let state = load();
let stack = [];                                    // return positions

const sections = [...document.querySelectorAll(".sop")];
const navbtns  = [...document.querySelectorAll(".navbtn")];

function counts(id) {{
  const sec = document.getElementById("sop-" + id);
  const boxes = [...sec.querySelectorAll("input")];
  const done = boxes.filter(b => state[b.dataset.id]).length;
  const killers = [...sec.querySelectorAll(".item.killer input")];
  const killersLeft = killers.filter(b => !state[b.dataset.id]).length;
  return {{ done, total: boxes.length, killersLeft }};
}}

function paint() {{
  for (const sec of sections) {{
    const id = sec.id.replace("sop-", "");
    const {{ done, total, killersLeft }} = counts(id);
    sec.querySelector(".bar i").style.width = total ? (done / total * 100) + "%" : "0%";
    sec.querySelector(".count").textContent =
      `${{done}}/${{total}}` + (killersLeft ? `  ·  ${{killersLeft}} ☠ open` : (total ? "  ·  clear" : ""));
    const nc = document.querySelector(`.navcount[data-for="${{id}}"]`);
    if (nc) nc.textContent = total ? `${{done}}/${{total}}` : "";
  }}
}}

function show(id, returnTo, keepScroll) {{
  sections.forEach(s => s.hidden = s.id !== "sop-" + id);
  navbtns.forEach(b => b.classList.toggle("on", b.dataset.to === id));
  const sec = document.getElementById("sop-" + id);
  const back = sec.querySelector(".back");
  if (returnTo) {{
    stack.push(returnTo);
    back.hidden = false;
    back.textContent = "← Return to " + returnTo.label;
  }} else if (!keepScroll) {{
    stack = [];
    back.hidden = true;
  }}
  if (!keepScroll) window.scrollTo({{ top: 0 }});
  paint();
}}

document.addEventListener("click", e => {{
  const nb = e.target.closest(".navbtn");
  if (nb) return show(nb.dataset.to);

  const jump = e.target.closest("a.jump");
  if (jump) {{
    e.preventDefault();
    const from = document.querySelector(".sop:not([hidden])");
    // remember the exact element the jump was made from
    const anchor = jump.closest(".item, p, td, li") || jump;
    if (!anchor.id) anchor.id = "ret-" + Math.random().toString(36).slice(2, 9);
    const heading = [...from.querySelectorAll("h2,h3")]
      .filter(h => h.compareDocumentPosition(anchor) & Node.DOCUMENT_POSITION_FOLLOWING).pop();
    return show(jump.dataset.to, {{
      section: from.id.replace("sop-", ""),
      anchor: anchor.id,
      label: heading ? heading.textContent.trim() : from.querySelector("h1").textContent.trim(),
    }});
  }}

  const back = e.target.closest(".back");
  if (back) {{
    const r = stack.pop();
    if (!r) return;
    show(r.section, null, true);              // do not jump to the top
    back.hidden = stack.length === 0;
    // the section was hidden a moment ago, so wait for layout before scrolling
    requestAnimationFrame(() => requestAnimationFrame(() => {{
      const el = document.getElementById(r.anchor);
      if (!el) return;
      el.scrollIntoView({{ block: "center", behavior: "smooth" }});
      el.classList.remove("flash"); void el.offsetWidth; el.classList.add("flash");
    }}));
    return;
  }}

  const reset = e.target.closest(".reset");
  if (reset) {{
    const sec = reset.closest(".sop");
    sec.querySelectorAll("input").forEach(b => {{ delete state[b.dataset.id]; b.checked = false; }});
    save(state); paint();
  }}
}});

document.addEventListener("change", e => {{
  const box = e.target.closest("input[type=checkbox]");
  if (!box) return;
  if (box.checked) state[box.dataset.id] = 1; else delete state[box.dataset.id];
  save(state); paint();
}});

document.querySelectorAll("input[type=checkbox]").forEach(b => {{ b.checked = !!state[b.dataset.id]; }});
show("README");
</script></body></html>
"""

out = SRC / "index.html"
out.write_text(page)
print(f"built {out.relative_to(ROOT)} — {len(docs)} checklists, {html_items} items")
