# Benchmarks

Reserved location for the Scout Intelligence Test and future benchmark
results, once approved.

## Current status: empty, on purpose

**Benchmark Draft v1** (the first 25 test cases) exists but is **not yet
here** — it's still under ChatGPT's second independent review round, per the
gated workflow in `SCOUT_AI_STATUS.md` (0002). It is not final and has not
been approved by Patrick. Committing it here happens only after that review
and approval are both complete — see "Next safest step" in
`SCOUT_AI_STATUS.md` for exactly what's pending.

## Intended structure, once populated

- `scout_intelligence_test_v1.md` (or similar) — the approved case
  definitions: categories, per-case input/context, capability tested,
  expected/unacceptable behavior, pass/fail criteria, LM/Infra/Mixed
  attribution, and `test_scope` (CURRENT / SIMULATED_FUTURE / BOTH).
- `results/` — one structured result file per benchmark run (see the result
  schema referenced in `SCOUT_AI_STATUS.md` / `RESEARCH_LOG.md`), enough to
  compare TinyLlama against any future candidate fairly, with Brain Score and
  System Score reported separately rather than collapsed into one number.
