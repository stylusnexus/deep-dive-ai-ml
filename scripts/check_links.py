#!/usr/bin/env python3
"""Verify every internal link in the built lessons resolves to a file on disk.

Lesson filenames carry their position, so inserting a lesson in one set renames
files that another set links to. Build-time slug validation cannot see that:
it checks the source, and the stale href lives in already-built HTML. This
checks the output instead, which catches it however it happened.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
HREF = re.compile(r'href="([^"]+)"')

def main():
    bad, checked = [], 0
    for page in sorted(ROOT.glob("lessons/**/*.html")) + [ROOT / "index.html"]:
        if not page.exists():
            continue
        for href in HREF.findall(page.read_text()):
            if href.startswith(("http://", "https://", "#", "mailto:")):
                continue
            checked += 1
            target = (page.parent / href.split("#")[0]).resolve()
            if not target.exists():
                bad.append(f"{page.relative_to(ROOT)} -> {href}")
    print(f"internal links checked : {checked}")
    if bad:
        print(f"\n{len(bad)} dead link(s):")
        for b in bad:
            print("  " + b)
        return 1
    print("no dead internal links")
    return 0

if __name__ == "__main__":
    sys.exit(main())
