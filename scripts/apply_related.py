#!/usr/bin/env python3
"""Insert ("related", [...]) blocks into the content modules from related_map.

Placement: immediately before the Further-reading block if there is one, else
before the quiz, else at the end — so a lesson reads content, related lessons,
further reading, quiz. Idempotent: an existing related block is replaced.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from lesson_map import content_modules            # noqa: E402
from related_map import RELATED                   # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "scripts" / "content"


def render(slugs, indent="    "):
    inner = ", ".join(f'"{s}"' for s in slugs)
    return f'{indent}("related", [{inner}]),\n'


def main():
    # slug -> module file, so we edit the right source
    where = {}
    for mod in content_modules():
        path = CONTENT / f"{mod.__name__}.py"
        for lsn in mod.LESSONS:
            where[lsn["slug"]] = path

    edited, added = set(), 0
    for slug, targets in RELATED.items():
        path = where.get(slug)
        if path is None:
            print(f"  skip {slug}: no such lesson")
            continue
        s = path.read_text()
        # locate this lesson's dict by its slug line, then its end
        m = re.search(rf'"slug":\s*"{re.escape(slug)}"', s)
        if not m:
            print(f"  skip {slug}: slug line not found")
            continue
        nxt = re.search(r'\n\},\n(?=\{|\]|\Z)', s[m.end():])
        end = m.end() + (nxt.start() if nxt else len(s) - m.end())
        seg = s[m.end():end]

        # drop an existing related block so this is repeatable
        seg = re.sub(r'\n\s*\("related", \[[^\]]*\]\),', '', seg)

        anchor = None
        for pat in (r'\n    \("links", \[', r'\n    \("books", \[', r'\n    \("quiz", \['):
            am = re.search(pat, seg)
            if am:
                anchor = am.start() + 1
                break
        block = render(targets)
        seg = seg[:anchor] + block + seg[anchor:] if anchor is not None else seg + "\n" + block
        s = s[:m.end()] + seg + s[end:]
        path.write_text(s)
        edited.add(path.name)
        added += 1

    print(f"inserted {added} related blocks across {len(edited)} modules")
    return 0


if __name__ == "__main__":
    sys.exit(main())
