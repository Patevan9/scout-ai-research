# Benchmarks

## Approved: Scout Intelligence Test v1

**[`scout-intelligence-test-v1.md`](scout-intelligence-test-v1.md)** — the
approved benchmark definition. 25 cases across categories A–G, each with
attribution (LM / Infra / Mixed) and `test_scope` (CURRENT / SIMULATED_FUTURE
/ BOTH). Completed the gated review workflow (Claude drafted → ChatGPT
reviewed, two rounds → Patrick approved) — see `SCOUT_AI_STATUS.md` and
`RESEARCH_LOG.md` for the milestone record.

**No testing has been run against it yet.** TinyLlama baseline testing has
not begun; no replacement model has been selected. See "Next safest step" in
`SCOUT_AI_STATUS.md`.

## Approved: Benchmark Profile v1

**[`benchmark-profile-v1.md`](benchmark-profile-v1.md)** — the approved test
conditions (RAW-only, fixed generation settings, result-recording rules) for
the first real benchmark run, scoped to the 9 currently committed RAW
fixtures. **No inference has been run under it yet** — no real inference
backend exists.

## `results/` — not yet created

Reserved for one structured result file per benchmark run, using the schema
defined at the bottom of `scout-intelligence-test-v1.md`. Created once actual
testing begins.
