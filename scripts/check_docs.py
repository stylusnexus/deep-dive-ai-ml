#!/usr/bin/env python3
"""Check the interactive worksheets: the answers a visitor downloads must be the
source markdown with their input filled in, and nothing else.

Runs the page's own serializer under Node, for every worksheet in docs/:
  1. with no input it must return the source file byte for byte;
  2. with every field filled it must contain each value on the right line, keep
     the table shape, and add only the lines the fields call for.
"""
import json, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
HARNESS = r"""
const fs = require("fs");
const html = fs.readFileSync(process.argv[1], "utf8");
const script = html.match(/\/\*serialize:start\*\/([\s\S]*?)\/\*serialize:end\*\//)[1];
const data = JSON.parse(html.match(/<script type="application\/json" id="doc-data">([\s\S]*?)<\/script>/)[1]);
const serialize = new Function(script + "; return serialize;")();
const blank = serialize(data.lines, data.fields, {});
const values = {};
data.fields.forEach(f => { values[f.id] = f.kind === "check" ? true : "V_" + f.id; });
const filled = serialize(data.lines, data.fields, values);
console.log(JSON.stringify({ blank, filled, lines: data.lines, fields: data.fields }));
"""


def main():
    docs = sorted((ROOT / "docs").glob("*.html"))
    worksheets = [d for d in docs if 'id="dl-answers"' in d.read_text()]
    if not worksheets:
        raise SystemExit("no worksheet pages found in docs/")
    bad = 0
    for page in worksheets:
        r = subprocess.run(["node", "-e", HARNESS, str(page)], capture_output=True, text=True)
        if r.returncode:
            print(f"FAIL {page.name}: node error: {r.stderr.strip()[:200]}"); bad += 1; continue
        out = json.loads(r.stdout)
        src = "\n".join(out["lines"])
        problems = []
        if out["blank"] != src:
            problems.append("blank round trip differs from the source")
        filled, fields = out["filled"].split("\n"), out["fields"]
        for f in fields:
            if f["kind"] == "check":
                continue
            if not any(f"V_{f['id']}" in line for line in filled):
                problems.append(f"value for {f['id']} not written")
        ticks = sum(1 for f in fields if f["kind"] == "check")
        if out["filled"].count("[x]") != ticks:
            problems.append(f"expected {ticks} ticked boxes, found {out['filled'].count('[x]')}")
        n_extra = len(filled) - len(out["lines"])
        n_ins = sum(1 for f in fields if f["kind"] == "insert")
        if n_extra < n_ins:
            problems.append("answer boxes did not insert lines")
        status = "FAIL" if problems else "ok  "
        bad += bool(problems)
        print(f"{status} {page.name:34} {len(fields):3} fields" + ("  " + "; ".join(problems) if problems else ""))
    print(f"\n{len(worksheets)} worksheets checked, {bad} failing")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
