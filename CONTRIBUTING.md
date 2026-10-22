# Contributing

This is a self-built course in applied AI and machine learning. The most useful
contributions are corrections: a wrong number, a broken link, a claim the
evidence does not support, a notebook that no longer runs.

## Before you start

Open an issue describing the change. For a typo or a dead link, a pull request
on its own is fine.

## The one rule that trips people up

**Never edit a file in `lessons/`.** The lesson pages, `index.html`,
`things-to-know.html`, `llms.txt`, `sitemap.xml` and the SOP page are generated.
An edit to a generated file is destroyed by the next build.

Edit the source and rebuild:

| To change | Edit | Rebuild |
|---|---|---|
| A lesson | `scripts/content/<module>.py` | `make lessons` |
| The landing page | `scripts/build_index.py`, `scripts/_index_style.html` | `make lessons` |
| A notebook | `scripts/content/*_notebooks.py` | `python3 scripts/build_notebooks.py <module>`, then re-execute it |
| An SOP checklist | the markdown in `artifacts/sop/` | `make sop` |

`make lessons` rebuilds every set, the index, the revision sheet and the search
files. Rebuild everything rather than one set: inserting a lesson renames files
that other sets link to.

## Notebooks ship with their outputs

Rebuilding a notebook strips its executed outputs. Re-execute before you commit:

```bash
jupyter nbconvert --to notebook --execute --inplace <file>.ipynb
```

A notebook without outputs is a claim nobody has checked.

## Evidence standards

- **Numbers come from runs.** A figure in a lesson was either measured in this
  repository or cited from a source you read. Record the verdict for any new
  number in `scripts/numbers_reviewed.txt`.
- **Every link is checked** and resolves before you commit it.
- **Spell out an acronym on its first use** in every lesson. Lessons are read
  standalone.
- **No personal paths or names** in source or in notebook outputs. Print paths
  relative to the home folder (`~`).

## Check your change

```bash
make verify     # glossary, links, numbers and notebook checks
```

For the Project 4 service, run `CORPUS_DIR=corpus pytest tests/` from
`projects/p4-deployed-assistant/` after `python3 scripts/build_corpus_artifact.py`.

## Commits and pull requests

- Commit subject: `type(scope): imperative summary`, lowercase after the colon,
  50 characters or fewer, no trailing period. Types in use: `feat`, `fix`,
  `docs`, `chore`.
- Add a body only when the reason is not obvious from the diff.
- Reference the issue as `Fixes #123` on its own line.
- Open the pull request against `main`. Describe what changed and how you
  checked it.

## Security

Report vulnerabilities privately. See [SECURITY.md](SECURITY.md).

## Licence

By contributing you agree that your contribution is released under the
[MIT License](LICENSE).
