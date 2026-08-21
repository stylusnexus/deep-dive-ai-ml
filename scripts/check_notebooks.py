#!/usr/bin/env python3
"""Fail if any notebook is committed without its executed outputs.

A notebook without outputs is a claim nobody has checked. This has been got
wrong twice in this repo, both times by running `git add -A` while a background
execution was still writing.
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
unrun = []
for f in sorted(ROOT.glob("notebooks/**/*.ipynb")):
    nb = json.loads(f.read_text())
    code = [c for c in nb["cells"] if c["cell_type"] == "code"]
    outs = sum(1 for c in code for _ in c.get("outputs", []))
    status = "OK   " if outs else "UNRUN"
    if not outs:
        unrun.append(f)
    print(f"  {status} {outs:>3} outputs  {f.relative_to(ROOT)}")

if unrun:
    print(f"\n{len(unrun)} notebook(s) have no outputs. Execute before committing:")
    for f in unrun:
        print(f"  jupyter nbconvert --to notebook --execute --inplace {f.relative_to(ROOT)}")
    sys.exit(1)
print("\nall notebooks carry executed outputs")
