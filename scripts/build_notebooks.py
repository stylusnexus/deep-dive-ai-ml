#!/usr/bin/env python3
"""Build .ipynb files from plain Python cell lists. Stdlib only.

Notebooks are painful to write and review as raw JSON, so they're authored
here as (kind, source) pairs and emitted as notebooks.
"""
import hashlib, json, pathlib, sys, importlib.util

ROOT = pathlib.Path(__file__).resolve().parent.parent

def nb(cells, kernel="python3"):
    out = []
    for i, (kind, src) in enumerate(cells):
        cid = hashlib.sha1(f"{i}{src}".encode()).hexdigest()[:8]
        lines = src.strip("\n").split("\n")
        lines = [l + "\n" for l in lines[:-1]] + [lines[-1]]
        if kind == "md":
            out.append({"cell_type": "markdown", "id": cid, "metadata": {}, "source": lines})
        else:
            out.append({"cell_type": "code", "id": cid, "execution_count": None,
                        "metadata": {}, "outputs": [], "source": lines})
    return {
        "cells": out,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": kernel},
            "language_info": {"name": "python", "version": "3.12"},
        },
        "nbformat": 4, "nbformat_minor": 5,
    }

if __name__ == "__main__":
    name = sys.argv[1]
    path = ROOT / "scripts" / "content" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    outdir = ROOT / mod.OUTDIR; outdir.mkdir(parents=True, exist_ok=True)
    for fname, cells in mod.NOTEBOOKS:
        (outdir / fname).write_text(json.dumps(nb(cells), indent=1) + "\n")
        print(f"  {mod.OUTDIR}/{fname}  ({len(cells)} cells)")
