# Changelog

All notable changes to this repository are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). There are no tagged
releases yet, so everything sits under Unreleased.

## [Unreleased]

### Added

- Free-plan Render blueprint (`render.yaml`) for the Project 4 assistant, with a
  note that the free plan has a cold start after about 15 idle minutes.
- A "Do I need Render?" section and a model-endpoint note in the Project 4 README.
- Page metadata on every lesson and on Things to Know: description, canonical URL,
  Open Graph tags and JSON-LD.
- `sitemap.xml`, `robots.txt` and `llms.txt`, generated from the lesson content by
  `scripts/build_seo.py` (also run by `make lessons` and `make seo`).
- Dependabot version updates for the Project 4 Python and Docker files, the lab
  Dockerfiles and the compose file.
- `LICENSE` (MIT), `CONTRIBUTING.md`, `SECURITY.md` and this file.

### Changed

- The quantization notebook prints tool locations relative to the home folder and
  has been re-executed.
- The selection scorecard's worked comparison now refers to "your own services".

### Removed

- Personal names, email addresses and filesystem paths from the repository and its
  history, before the repository was made public.

The history before this point is in `git log`.
