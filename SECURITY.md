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
- The build, check and benchmark scripts in `scripts/`, and the lab containers in `docker/`.
- Dependencies pinned in this repository.
- The published site at https://stylusnexus.github.io/deep-dive-ai-ml/.

## What is not in scope

- The attacks that Block 6 teaches. Prompt injection, tool poisoning and the other
  examples are there on purpose, against fixtures built to be attacked.
- The datasets and corpora under `data/` and `projects/*/corpus/`. They are
  generated from a seed and contain no real data.
- Third-party models, libraries and services the course uses. Report those to
  their maintainers.

## The scripts and lab tooling

Everything under `scripts/` runs on your machine with your permissions, so read a
script before you run it, especially one from a fork or a pull request.

- **Build and check scripts** (`build_*.py`, `check_*.py`, `apply_related.py`,
  `lesson_map.py`, `seo_meta.py`) use only the Python standard library. They read
  and write files inside the repository. The one subprocess is `git log`, in
  `build_seo.py`. They use no `eval`, `exec`, `pickle` or `shell=True`, and they
  fetch nothing: `check_links.py` checks internal links only.
- **They delete only what they generate.** The lesson and page builders remove
  stale files under `lessons/` and `docs/`, and nothing else.
- **Two scripts use the network.** `bench_engines.py` sends prompts to the
  endpoint you give it with `--base-url` (default `http://127.0.0.1:8000/v1`),
  using a placeholder bearer token. `measure_quantization.py` downloads model files
  from Hugging Face, limited to `*.safetensors` and `*.json` so that pickled weights
  are never fetched. Neither pins a model revision, so a download is only as
  trustworthy as the upstream repository at that moment.
- **Data and model scripts need extra packages.** `make_dataset.py`,
  `make_timeseries.py`, `eval_finetune.py`, `measure_quantization.py` and
  `measure_semantic_threshold.py` import NumPy, pandas, MLX, `huggingface_hub` or
  `sentence-transformers`. No script installs anything; they print the `pip`
  command and stop.
- **`scripts/check-env.sh` reads, and reports, never prints, secrets.** It says
  whether `ANTHROPIC_API_KEY` and `OPENAI_API_KEY` are set and who you are logged
  in to Hugging Face as. It does not print the keys.
- **Notebooks and projects execute code.** Running a notebook from a pull request
  runs whatever it contains. Review it first, and run untrusted ones in the
  containers rather than on the host.
- **The lab containers** (`docker/compose.yaml`) publish Jupyter, Postgres and
  MLflow on `127.0.0.1` only. Jupyter runs as root with no token and mounts the
  repository read-write at `/work`; Postgres uses the throwaway password `aiml`.
  That is fine on your own machine and unsafe on a shared one. Do not change the
  bindings to `0.0.0.0`, do not expose these ports through a tunnel or firewall
  rule, and never reuse the lab passwords.

## Supported versions

Only the current `main` branch is supported. There are no tagged releases.

## Secrets

The repository holds no real API keys. `API_KEYS` for Project 4 is set in the
host's dashboard and never committed. If you find a credential in the repository
or its history, treat it as a vulnerability and report it as above.
