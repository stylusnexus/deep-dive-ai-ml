# Security policy

## Reporting a vulnerability

Please do not open a public issue for a security problem.

Report it privately in one of two ways:

- Use [GitHub private vulnerability reporting](https://github.com/stylusnexus/deep-dive-ai-ml/security/advisories/new).
- Email admin@stylusnexus.com with "deep-dive-ai-ml security" in the subject.

Include what you found, where it is, and steps to reproduce it. We will
acknowledge your report, keep you informed, and credit you in the fix if you
want that.

## What is in scope

- The Project 4 service (`projects/p4-deployed-assistant/`): authentication, rate
  limiting, request validation, error handling and the container image.
- The build and check scripts in `scripts/`.
- Dependencies pinned in this repository.
- The published site at https://stylusnexus.github.io/deep-dive-ai-ml/.

## What is not in scope

- The attacks that Block 6 teaches. Prompt injection, tool poisoning and the other
  examples are there on purpose, against fixtures built to be attacked.
- The datasets and corpora under `data/` and `projects/*/corpus/`. They are
  generated from a seed and contain no real data.
- Third-party models, libraries and services the course uses. Report those to
  their maintainers.

## Supported versions

Only the current `main` branch is supported. There are no tagged releases.

## Secrets

The repository holds no real API keys. `API_KEYS` for Project 4 is set in the
host's dashboard and never committed. If you find a credential in the repository
or its history, treat it as a vulnerability and report it as above.
