# Portfolio projects

Four projects across four domains, each ending as a published Hugging Face
Space with a live URL.

| # | Project | Block | Exit |
|---|---|---|---|
| 1 | Wind turbine failure prediction | 2 | Neural net beats the baseline on held-out data |
| 2 | Financial report RAG assistant | 3 | Cited answers over a real 10-K |
| 3 | Multi-agent delivery exceptions | 4 | Runs with human-in-the-loop, traced in LangSmith |
| 4 | Deployed energy intelligence assistant | 8 | Authenticated, rate-limited, public URL |

Every one starts with [the intake sheet](../artifacts/project-intake.md) filled
in **before** any code, and a re-read of it afterwards against what actually happened.

## Optional open-ended challenge after Block 2

Choose a small public dataset or a question from your own work and run the same
decision loop as Project 1, without copying its domain:

- define the decision and the cost of each error;
- build and score a dumb baseline;
- make a time- or group-aware split if the data requires one;
- compare one simple model with one stronger candidate;
- record per-item failures, not only the headline score; and
- write a one-page stop/ship decision.

This is practice, not a fifth portfolio project. Keep it small enough to finish in
one or two sessions. If the dataset cannot support a defensible split or outcome,
stop and choose another one.

## Optional portfolio extensions

After the core projects, choose at most one:

- reproduce one result from a paper or official technical report and record where
  your setup differs;
- write a short technical note explaining a measured failure and its fix;
- make a small upstream contribution to a tool used here; or
- use the existing projects as interview prompts and explain the trade-offs,
  failure paths and evidence rather than memorising definitions.

These are extensions of the work already done, not new required blocks.
