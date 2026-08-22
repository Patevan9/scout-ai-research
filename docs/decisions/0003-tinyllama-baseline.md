# 0003 — TinyLlama is the required baseline for any future Scout AI brain

**Status:** Approved
**Date:** 2026-08-22

## Decision

Any candidate Scout AI brain must be benchmarked against TinyLlama — Scout's
current shipped local model — and must demonstrably outperform that baseline
on Scout-specific tests (the Scout Intelligence Test, once approved) while
remaining practical on local hardware: comparable or better stability,
factual integrity, privacy, speed, and device resource use, not quality
alone.

## Reason

Avoids adopting a "better" model on the strength of general-purpose
benchmarks that don't reflect what Scout specifically needs to be good at,
and keeps any future brain-replacement decision accountable to real,
comparable, recorded evidence rather than impression.

## Alternatives considered

None recorded yet — open for addition if a real alternative baseline
methodology is proposed and reviewed.

## Consequences

- The Scout Intelligence Test (see `benchmarks/`) is the mechanism this
  decision depends on; no future brain is adopted without passing it.
- Benchmark results must record device and resource use alongside quality
  verdicts (see the result schema under review in the benchmark draft) — a
  brain that wins on quality but fails on-device practicality does not
  satisfy this decision.
- No specific replacement model has been chosen — this decision only fixes
  the standard a candidate must clear, not which candidate to try.
