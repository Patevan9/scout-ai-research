# 0005 — Benchmark runner methodology

**Status:** Approved
**Date:** 2026-08-22

## Decision

How Scout Intelligence Test v1's 25 cases are run, and how results are kept
honest and comparable across candidate brains.

### Runner categories

- **RAW** — direct, controlled test of the local brain alone, against a
  canonical test context (below). No Scout AI path-selection or routing runs.
- **SYSTEM** — current Scout + TinyLlama's real integrated behavior, routing
  and all.
- **BOTH** — both runs produce meaningful, different evidence.

### Approved 25-case assignment

| Runner | Cases | Count |
|---|---|---|
| SYSTEM only | A1, A3, A4, C1, E3, G1, G2, G3 | 8 |
| RAW only | C4, C5, F1 | 3 |
| BOTH | A2, B1, B2, B3, B4, C2, C3, D1, D2, D3, E1, E2, F2, F3 | 14 |

8 + 3 + 14 = 25.

**On C4 and F1 specifically:** these are `SIMULATED_FUTURE` in
`benchmarks/scout-intelligence-test-v1.md` because Scout's current
*integrated* system has no path that feeds this information to TinyLlama at
all. That absence applies only to the SYSTEM runner. A RAW run, against the
canonical simulated payload below, remains fully possible and is the correct
way to establish a brain baseline for these two cases — see v1's corrected
wording for the exact clarification.

### Canonical RAW-context principle

Each candidate brain receives **semantically equivalent, model-neutral
information containing only what the specific test case permits it to
know** — expressed as plain structured facts, never as one model's prompt
string. This is deliberate: Scout's current `OfflinePromptBuilder` is
reference evidence for what a real prompt looks like today, not the
permanent definition of a fair test — binding RAW fairness to today's
prompt-builder format would work against the "model-replaceable" principle
in the Charter.

Possible context fields, per case as applicable:

- exact current user input
- permitted recent conversation turns
- relevant retrieved facts
- **memory/habit payloads** (e.g. C4's simulated Truth-vs-habit signal —
  this is Truth/Habit-style structured information, not a sensor reading,
  and must not be grouped with the sensor/vision category below)
- **simulated sensor/vision payloads** (e.g. F1/F2/F3's label/confidence/
  position data — this category is distinct from memory/habit payloads)
- explicit capability availability
- online/offline state, where relevant

Each candidate model may receive surface formatting appropriate to its own
required chat/instruction template, but the semantic information supplied
must remain equivalent across every model tested — TinyLlama today, any
future candidate.

**Left unresolved:** whether canonical contexts eventually live inside
`scout-intelligence-test-v1.md` itself or as separate per-case fixture
files. Not decided by this record.

## Three evaluation axes — kept permanently separate

- **BRAIN QUALITY** — aggregate `brain_verdict` across cases where a model
  was actually invoked.
- **SYSTEM QUALITY** — aggregate `system_verdict` across all cases.
- **RESPONSE SPEED** — latency statistics, reported independently.

Never collapsed into one overall score, under any circumstance.

## Approved result/latency fields

- `total_response_latency_ms`
- `time_to_first_useful_response_ms`
- `model_invoked`
- `model_generation_time_ms`
- `path_taken`: `fast | retrieval | reasoning | not_applicable` —
  `not_applicable` is used for a RAW test, where Scout AI's path selector is
  bypassed entirely. A direct model invocation in a RAW run must never be
  recorded as `reasoning` by default — that would misrepresent a bypassed
  selector as a selector decision.
- `selector_time_ms`
- `heavy_model_avoided`: `true | false` — rolls up cleanly into a future
  summary statistic: the percentage of ordinary interactions resolved
  without invoking the expensive reasoning model.

**No numeric latency target is approved yet.** Today's real hardware
baseline hasn't been measured — setting a millisecond threshold before that
exists would be a guess, not a decision.

## Reason

Fair brain-vs-brain comparison requires controlled, comparable input — but
"controlled" must not silently mean "however Scout's app happens to build a
prompt today." Separating RAW/SYSTEM/BOTH per case, and keeping quality and
speed on independent axes, is what makes it possible to say a future brain
is genuinely better without hiding a routing win or a latency loss inside
one blended number.

## Alternatives considered

- Testing every case only through the full integrated Scout system —
  rejected: several cases (C4, F1) have no such path to test at all, and for
  the rest it would conflate brain quality with routing quality, exactly
  what Brain/System Score separation exists to prevent.
- A single averaged "AI quality" score — rejected per the Charter's own
  intent and explicit instruction; brain quality, system quality, and speed
  must remain visibly separate, especially since they can move in opposite
  directions for the same candidate.

## Consequences

- No harness has been built. This document defines methodology only.
- Any future benchmark harness implementation must be checked against this
  record before being built.
- `benchmarks/scout-intelligence-test-v1.md` is clarified (not rewritten) to
  reference this record where C4/F1's RAW-testability was previously
  understated.
