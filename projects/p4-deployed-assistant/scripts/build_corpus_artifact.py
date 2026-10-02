#!/usr/bin/env python3
"""Write the data-identity artefact this service's model file does not have.

This project has no trained weights — the deployable unit is the retrieval
corpus. Without a recorded identity for it, "which corpus answered this
question" and "did the corpus change under me" are both unanswerable after
the fact, which is exactly the gap the-artefact-is-code-data-and-config
lesson describes. The fix here is deliberately small: a manifest hash, a doc
count and a build timestamp, not a registry platform.

Run from the project root:
    python3 scripts/build_corpus_artifact.py
"""
from __future__ import annotations

import datetime
import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CORPUS_DIR = ROOT / "corpus"
MANIFEST = CORPUS_DIR / "manifest.json"
ARTIFACT = CORPUS_DIR / "corpus_id.json"


def corpus_hash(manifest_bytes: bytes) -> str:
    return hashlib.sha256(manifest_bytes).hexdigest()


def check_manifest_matches_files(docs: list[dict]) -> list[str]:
    """The manifest embeds each document's full text. If an .md file on disk
    disagrees with what the manifest says it contains, the hash below is
    certifying content nobody is actually serving. Returns the doc_ids that
    disagree, empty when the manifest and the files on disk agree."""
    mismatched = []
    for doc in docs:
        md_path = CORPUS_DIR / f"{doc['doc_id']}.md"
        if not md_path.exists():
            continue  # some corpora are manifest-only; that is not a mismatch
        if md_path.read_text().strip() != doc["text"].strip():
            mismatched.append(doc["doc_id"])
    return mismatched


def build() -> dict:
    if not MANIFEST.exists():
        raise FileNotFoundError(f"no manifest at {MANIFEST} — nothing to hash")
    manifest_bytes = MANIFEST.read_bytes()
    docs = json.loads(manifest_bytes)

    drift = check_manifest_matches_files(docs)
    if drift:
        raise ValueError(
            f"manifest disagrees with the files on disk for: {', '.join(drift)} — "
            "regenerate the manifest before hashing; a hash over a manifest that "
            "does not match what is served is a confident wrong answer")

    artifact = {
        "corpus_hash": corpus_hash(manifest_bytes),
        "hash_algorithm": "sha256",
        "hashed_file": "manifest.json",
        "doc_count": len(docs),
        "doc_ids": sorted(d["doc_id"] for d in docs),
        "built_at": datetime.datetime.now(datetime.timezone.utc)
            .isoformat(timespec="seconds"),
    }
    ARTIFACT.write_text(json.dumps(artifact, indent=2) + "\n")
    return artifact


if __name__ == "__main__":
    result = build()
    print(f"wrote {ARTIFACT.relative_to(ROOT)}")
    print(json.dumps(result, indent=2))
    sys.exit(0)
