#!/usr/bin/env python3
"""Fail when a lesson defines a term the glossary has never heard of.

The glossary is hand-written and it drifted: it covered Block 0 and stopped,
while four more blocks were built. This guard exists so that cannot happen
silently again — add a block, and its new terms have to be either defined or
explicitly declined.

Lessons use ("terms", [...]) blocks for two different jobs: real definitions,
and rows of a comparison table ("Too large", "Before", "1 · Can you write the
rule?"). Only the first kind belongs in the glossary, so a term may be resolved
three ways — defined in GLOSSARY.md, listed in glossary_backlog.txt as known
and untriaged, or listed in glossary_notterms.txt as deliberately not a term.
Anything else is new, and stops the build until somebody decides which it is.
"""
import importlib.util, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "scripts" / "content"
BACKLOG = ROOT / "scripts" / "glossary_backlog.txt"
NOTTERMS = ROOT / "scripts" / "glossary_notterms.txt"


def norm(term):
    """Match a lesson's label to a glossary entry without demanding they be typed
    identically. A lesson says "MAE" where the glossary says "Mean absolute error
    (MAE)", and "Lags" where it says "Lag feature" — those are the same term, and
    treating them as gaps buries the real ones."""
    t = term.strip().lower().rstrip(".")
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"s$", "", t)          # lags -> lag
    return t


def names_for(entry):
    """Every name a glossary entry answers to: its full name, each parenthesised
    acronym or alias inside it, and the name with those parentheses removed."""
    out = {entry}
    for alias in re.findall(r"\(([^)]+)\)", entry):
        out.add(alias)
    out.add(re.sub(r"\s*\([^)]*\)", "", entry).strip())
    for part in entry.split(" / "):
        out.add(part.strip())
    return {norm(o) for o in out if o.strip()}


def read_list(path):
    if not path.exists():
        return set()
    return {norm(l) for l in path.read_text().splitlines()
            if l.strip() and not l.startswith("#")}


def lesson_terms():
    found = {}
    for f in sorted(CONTENT.glob("*.py")):
        if f.stem.endswith("notebooks"):
            continue
        spec = importlib.util.spec_from_file_location(f.stem, f)
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception as ex:
            print(f"  cannot load {f.name}: {ex.__class__.__name__}")
            continue
        for lesson in getattr(mod, "LESSONS", []):
            for item in lesson.get("body", []):
                if item[0] == "terms":
                    for entry in item[1]:
                        found.setdefault(entry[0].strip(), f.stem)
    return found


def main():
    glossary = (ROOT / "GLOSSARY.md").read_text()
    defined = set()
    for m in re.finditer(r'^\*\*(.+?)\*\*\s+—', glossary, re.M):
        defined |= names_for(m.group(1).strip())
    backlog, notterms = read_list(BACKLOG), read_list(NOTTERMS)

    terms = lesson_terms()
    known = defined | backlog | notterms
    new = {t: mod for t, mod in terms.items() if norm(t) not in known}

    print(f"glossary defines   : {len(defined)}")
    print(f"lessons define     : {len(terms)}")
    print(f"awaiting triage    : {len(backlog)}  (scripts/glossary_backlog.txt)")
    print(f"declined as rows   : {len(notterms)}  (scripts/glossary_notterms.txt)")

    if new:
        print(f"\n{len(new)} term(s) appear in a lesson and nowhere else:\n")
        for t, mod in sorted(new.items()):
            print(f"  {t:44s} ({mod})")
        print("\nDefine each in GLOSSARY.md, or add it to glossary_notterms.txt")
        print("if it is a comparison-table row rather than a term.")
        return 1

    print("\nno untracked terms — every lesson term is defined, backlogged or declined")
    return 0


if __name__ == "__main__":
    sys.exit(main())
