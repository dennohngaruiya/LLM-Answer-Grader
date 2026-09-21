# Roadmap

Each item is here because it removes a real limitation of the current version, not
because it sounds impressive.

## v0.2 — Configurable rubrics
**Problem:** weights and rules are hard-coded in `scorer.py`. A support team and a legal
team want different rubrics for the same answers.
**Plan:** load a rubric from TOML (stdlib `tomllib`), so weights, required fields and
keyword lists become data instead of code. Ship two example rubrics — `support.toml` and
`safety.toml` — and let `--rubric` select one.

## v0.3 — LLM-as-judge, optional and clearly labelled
**Problem:** some qualities (tone, completeness of an explanation) resist rules.
**Plan:** a `--judge` flag that sends the answer *and the same rubric* to a model and merges
its verdicts with the deterministic ones. Strictly opt-in, always labelled in the report as
*model-judged* so a reader always knows which verdicts are reproducible offline.

## v0.4 — Model comparison view
**Problem:** "which model should we ship?" is the question people actually ask.
**Plan:** accept multiple answer files and render a side-by-side HTML view: same prompt,
two answers, two report cards, one diff. This turns the tool from a grader into a
decision aid.

## v0.5 — Batch and streaming
**Problem:** real evaluation happens over hundreds of transcripts, not four hand-written cases.
**Plan:** read JSONL, write CSV plus a summary HTML, and stream so memory stays flat.

## Backlog / ideas
- Severity thresholds configurable per team (`--strict`)
- Snapshot mode: hash a case's findings so a rubric change is auditable in git
- A tiny GitHub Action so other repos can `uses:` the grader directly
- Optional localisation of finding text (the researcher's audience is multilingual)

## Explicitly not planned
- **A web dashboard.** The report is one self-contained HTML file precisely so it needs no server.
- **A hosted service.** The value here is that it runs offline, in CI, with no account.
- **Any third-party dependency for core scoring.** Determinism and zero-install stay non-negotiable.
