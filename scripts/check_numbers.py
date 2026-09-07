#!/usr/bin/env python3
"""Fail when a lesson gains a numeric claim nobody has vetted.

Two fabricated figures reached this course before anyone checked them, both from
search summaries rather than papers, and both looked entirely reasonable. A number
is the one thing in a lesson a reader cannot sanity-check from context, so it is
the thing most worth gating.

This cannot decide whether a number is *true* — that is a human judgement, and the
audit that seeded this file was done by reading sources. What it can do is notice
when a new one appears, so the judgement happens once per claim rather than never.

    python3 scripts/check_numbers.py          # fail on unreviewed claims
    python3 scripts/check_numbers.py --list   # print every claim it can see
    python3 scripts/check_numbers.py --seed   # write the current set as reviewed

Reviewed claims live in scripts/numbers_reviewed.txt, one per line, as
    <lesson-slug>|<sha1 of the normalised sentence>|<short note on why it is sound>
"""
import argparse
import hashlib
import importlib.util
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "scripts" / "content"
REVIEWED = ROOT / "scripts" / "numbers_reviewed.txt"

# A bare integer under three digits is nearly always structural ("the three
# techniques", "step 2"). Anything with a unit, or any longer number, is a claim.
NUM = re.compile(
    r"(?<![\w.])(\d[\d,]*\.?\d*)\s*"
    r"(%|per cent|percentage points?|x\b|×|GB|MB|KB|TB|tokens?|ms|GHz|"
    r"seconds?|minutes?|hours?|points?)?",
    re.I,
)
SENTENCE = re.compile(r"(?<=[.!?])\s+")


def strip_html(text):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", str(text))).strip()


def key(sentence):
    norm = re.sub(r"\s+", " ", sentence.strip().lower())
    return hashlib.sha1(norm.encode("utf-8")).hexdigest()[:12]


def claims():
    """Every sentence in the lesson prose that carries a numeric claim."""
    out = []
    for path in sorted(CONTENT.glob("*.py")):
        if path.stem.endswith("_notebooks") or path.stem.startswith("_"):
            continue
        spec = importlib.util.spec_from_file_location(path.stem, path)
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception:
            continue
        for lesson in getattr(mod, "LESSONS", []):
            for block in lesson["body"]:
                kind = block[0]
                if kind in ("p", "h2", "h3"):
                    texts = [block[1]]
                elif kind == "ul":
                    texts = list(block[1])
                elif kind == "terms":
                    texts = [f"{a}: {b}. {c}" for a, b, c in block[1]]
                elif kind == "know":
                    texts = list(block[1:])
                elif kind == "callout":
                    texts = [block[3]]
                else:
                    continue
                for text in texts:
                    for sentence in SENTENCE.split(strip_html(text)):
                        hits = [
                            m.group(0).strip()
                            for m in NUM.finditer(sentence)
                            if m.group(2) or len(m.group(1)) > 2
                        ]
                        if hits:
                            out.append((lesson["slug"], key(sentence), sentence, hits))
    return out


def load_reviewed():
    if not REVIEWED.exists():
        return {}
    reviewed = {}
    for line in REVIEWED.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("|", 2)
        if len(parts) >= 2:
            reviewed[parts[1]] = parts[0]
    return reviewed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--seed", action="store_true")
    args = ap.parse_args()

    found = claims()
    if args.list:
        for slug, k, sentence, hits in found:
            print(f"{slug:38s} {k}  {','.join(hits[:3]):<18} {sentence[:96]}")
        return 0

    if args.seed:
        lines = ["# Numeric claims reviewed for a source. See scripts/check_numbers.py.",
                 "# <lesson>|<hash>|<why it is sound>", ""]
        for slug, k, sentence, _ in found:
            lines.append(f"{slug}|{k}|seeded by the audit of 2026-09-07")
        REVIEWED.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"seeded {len(found)} reviewed claims -> {REVIEWED.relative_to(ROOT)}")
        return 0

    reviewed = load_reviewed()
    new = [(s, k, sent, h) for s, k, sent, h in found if k not in reviewed]
    print(f"numeric claims in lessons : {len(found)}")
    print(f"reviewed                  : {len(found) - len(new)}")
    if new:
        print(f"\n{len(new)} claim(s) not yet reviewed:\n")
        for slug, k, sentence, hits in new:
            print(f"  [{slug}] {','.join(hits[:3])}")
            print(f"    {sentence[:150]}")
            print(f"    -> add to numbers_reviewed.txt as: {slug}|{k}|<why it is sound>\n")
        print("Each one needs a source, a measurement in this repo, or to be recognisably")
        print("hypothetical. Record which, then add the line.")
        return 1
    print("\nevery numeric claim in the lessons has been reviewed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
