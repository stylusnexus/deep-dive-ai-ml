"""The training-system test the README promises: does the build load the
intended corpus and write a named artefact with its data identity?

Deliberately not a validation test — it does not score an answer, because
this build has no model to score. It proves the pipeline ran and the
identity it wrote is trustworthy, the same way How to Measure's step 0
proves a fixture before trusting anything it reports.
"""
import hashlib
import json
import pathlib
import shutil
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import build_corpus_artifact as build_mod  # noqa: E402


@pytest.fixture
def corpus_copy(tmp_path):
    """A disposable copy of the real corpus, so the test can mutate it without
    touching the artefact the deployed image actually ships."""
    dest = tmp_path / "corpus"
    shutil.copytree(ROOT / "corpus", dest)
    build_mod.CORPUS_DIR = dest
    build_mod.MANIFEST = dest / "manifest.json"
    build_mod.ARTIFACT = dest / "corpus_id.json"
    yield dest


def test_build_writes_the_artifact(corpus_copy):
    result = build_mod.build()
    artifact_path = corpus_copy / "corpus_id.json"
    assert artifact_path.exists(), "the build did not write a named artefact"
    on_disk = json.loads(artifact_path.read_text())
    assert on_disk == result


def test_hash_matches_a_fresh_rehash(corpus_copy):
    """Did nothing and solved it must not score the same — here, built twice
    from the same bytes must not disagree with itself."""
    first = build_mod.build()
    second = build_mod.build()
    assert first["corpus_hash"] == second["corpus_hash"]


def test_hash_changes_when_the_corpus_changes(corpus_copy):
    """Prove the instrument: a hash that cannot detect a changed corpus is not
    recording an identity, it is recording a constant. The manifest and its
    matching .md file are updated together, exactly as a real regeneration
    would, so this exercises a real content change rather than the drift
    guard tested separately above."""
    before = build_mod.build()
    manifest = json.loads((corpus_copy / "manifest.json").read_text())
    # The manifest's embedded text and the on-disk .md file do not share a
    # trailing-newline convention (the build's own drift check only compares
    # them stripped), so the new content is normalised once and assigned to
    # both rather than appended independently to each.
    new_text = manifest[0]["text"].strip() + "\n\nAppended during the test to force drift."
    manifest[0]["text"] = new_text
    (corpus_copy / "manifest.json").write_text(json.dumps(manifest))
    md_path = corpus_copy / f"{manifest[0]['doc_id']}.md"
    md_path.write_text(new_text)
    after = build_mod.build()
    assert before["corpus_hash"] != after["corpus_hash"]


def test_doc_count_matches_the_manifest(corpus_copy):
    manifest = json.loads((corpus_copy / "manifest.json").read_text())
    result = build_mod.build()
    assert result["doc_count"] == len(manifest)
    assert result["doc_ids"] == sorted(d["doc_id"] for d in manifest)


def test_refuses_to_hash_a_manifest_that_disagrees_with_the_files_on_disk(corpus_copy):
    """A hash over a manifest the service does not actually serve is a
    confident wrong answer — see the-artefact-is-code-data-and-config."""
    md_files = list(corpus_copy.glob("*.md"))
    assert md_files, "fixture corpus has no standalone .md files to drift from"
    target = md_files[0]
    target.write_text(target.read_text() + "\n\nThis line exists only on disk.")
    with pytest.raises(ValueError, match="disagrees with the files on disk"):
        build_mod.build()


def test_hash_is_stable_against_the_committed_corpus():
    """The artefact actually committed alongside the real corpus — not a
    fixture copy — must match what the build script produces right now, or
    the corpus changed without anyone re-running the build."""
    committed = json.loads((ROOT / "corpus" / "corpus_id.json").read_text())
    assert committed["corpus_hash"] == hashlib.sha256(
        (ROOT / "corpus" / "manifest.json").read_bytes()).hexdigest()
