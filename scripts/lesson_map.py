"""Slug -> built-file map, shared by the lesson builder and the link checker.

Lesson filenames are ID_BASE + position, so inserting a lesson renames every
file after it. Cross-references therefore cannot be hardcoded: they are
resolved from the live content modules at build time, which is what this
module exists to do.
"""

import importlib.util
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "scripts" / "content"


def content_modules():
    """Every lesson module, in filename order. Notebook modules are not lessons."""
    for path in sorted(CONTENT.glob("*.py")):
        if path.stem.endswith("_notebooks") or path.stem.startswith("_"):
            continue
        spec = importlib.util.spec_from_file_location(path.stem, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if hasattr(mod, "LESSONS") and hasattr(mod, "TOPIC"):
            yield mod


def slug_map():
    """{slug: {topic, file, title, subtitle, set_title}} across every set.

    Raises on a duplicate slug, because a duplicate makes a cross-reference
    ambiguous and silently points half of them at the wrong lesson.
    """
    out = {}
    for mod in content_modules():
        for idx, lsn in enumerate(mod.LESSONS):
            slug = lsn["slug"]
            if slug in out:
                raise AssertionError(
                    f"duplicate lesson slug {slug!r} in {mod.TOPIC} and "
                    f"{out[slug]['topic']} — slugs are the cross-reference key "
                    f"and must be unique across the whole course")
            out[slug] = {
                "topic": mod.TOPIC,
                "file": f"lsn-{mod.ID_BASE}{idx:03d}-{slug}.html",
                "title": lsn["title"],
                "subtitle": lsn.get("subtitle", ""),
                "set_title": mod.TITLE,
            }
    return out
