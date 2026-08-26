# Benchmark Profile v1 — Scout Intelligence Test v1, RAW mode

**Status:** Approved
**Date:** 2026-08-26
**Approved via:** Claude's read-only Benchmark Profile investigation →
independent Patrick + ChatGPT review → approval (see the gated review
workflow in `SCOUT_AI_STATUS.md`).

This document fixes the exact, reproducible test conditions for the first
real RAW benchmark run of Scout Intelligence Test v1
(`scout-intelligence-test-v1.md`) against TinyLlama, and against any future
candidate model tested the same way. **No inference has been run under this
profile yet** — see "Status of actual execution" below.

## Scope

Benchmark Profile v1 covers exactly the 9 RAW fixtures currently committed
under `lab/fixtures/`, and no others:

    B1  B2  B3  C2  C3  D1  D2  D3  F1

This set is deliberately narrower than the full 17 RAW/BOTH cases approved
in [ADR-0005](../docs/decisions/0005-benchmark-runner-methodology.md) (3
RAW-only + 14 BOTH). C4, C5, and F3 are excluded because no fixture for them
can be honestly represented yet — C4 and F3 need renderer rules that
[ADR-0006](../docs/decisions/0006-canonical-context-renderer.md)
explicitly leaves open (`memory_habit_payload`, empty
`simulated_vision_payload.detections`), and C5 needs a fixture-schema field
for a real export-file payload that does not exist yet. A2, B4, E1, E2,
and F2 simply have no fixture committed yet. None of these gaps is resolved by
this document — this Benchmark Profile may be extended later, once a case
can be represented honestly, without needing to be redefined from scratch.

## Runner mode

**RAW only.** Lab Runner has no path to Scout's real routing/app
integration — it cannot produce a `system_verdict` for any case. This
profile governs `brain_verdict` evidence only, per the RAW/SYSTEM/BOTH
split in ADR-0005.

## Context pipeline

Unchanged from the existing, already-tested implementation: canonical
fixture → `render_canonical_context()` → `RenderedContext` →
`ModelAdapter.format_prompt()` → `InferenceBackend.run()` (ADR-0006,
"Option B"). This profile does not modify the renderer, the fixture
schema, or any adapter.

## Fixed generation parameters

| Parameter | Value |
|---|---|
| Temperature | 0 (greedy / deterministic decoding) |
| Runs per fixture | 1 |
| Maximum output tokens | 150 |
| Model context limit (`n_ctx`) | 2048 |

These four values must be identical across every candidate model
benchmarked under this profile — changing any of them produces a different
profile, not a comparable result under this one. (150 and 2048 reuse
TinyLlama's real on-device reference values from `OfflinePromptBuilder`/
`LlamaEngine.kt`, adopted here as this profile's own fixed values, not
inherited implicitly — see `TinyLlamaChatMLAdapter.
default_generation_settings()`'s own note that its defaults are reference
evidence, not an authoritative benchmark setting.)

Sampling parameters not listed above (top-p, top-k, repeat_penalty, random
seed) are intentionally left undecided by this profile — no real
`InferenceBackend` exists yet to make them concrete, and under greedy
decoding most of them have no effect. They remain open for whichever future
step actually implements a backend.

## Result recording

Use the existing approved result schema unchanged — the JSON shape defined
at the bottom of `scout-intelligence-test-v1.md`, plus the latency fields
approved in ADR-0005 (`total_response_latency_ms`,
`time_to_first_useful_response_ms`, `model_invoked`,
`model_generation_time_ms`, `path_taken`, `selector_time_ms`,
`heavy_model_avoided`). `path_taken` for every result under this profile is
`not_applicable` — Scout AI's path selector (ADR-0004) is never invoked in
a RAW run. `raw_response` is preserved verbatim, never summarized or
edited. One structured result file per benchmark run, under
`benchmarks/results/`, per the existing (not yet used) convention.

**No numeric latency threshold is approved.** Latency is recorded, never
scored pass/fail, per ADR-0005.

## Hardware/runtime recording

Each run must record the actual hardware it ran on (device/CPU/RAM/OS as
applicable). A run under this profile executes on a PC, not an Android
device. **PC latency must be labeled as PC latency and must not be
presented as directly comparable** to the existing real-device TinyLlama
measurements already recorded in `RESEARCH_LOG.md` (Galaxy A32, Galaxy
Fold 7) — different hardware, not a substitute for real-device numbers.

## Scope integrity — do not collapse

- **F1** stays labeled `SIMULATED_FUTURE` in every result record and
  report. Running it under this profile establishes a brain baseline for a
  future capability — it must never be presented as evidence about Scout's
  current integrated vision behavior.
- **C3** stays scoped to exactly what its own fixture note says: whether
  the response recognizes teaching-shaped content without falsely claiming
  persistence occurred. A result under this profile must never assert or
  imply that a database write was performed or verified — Lab Runner has
  no persistence layer, and C3's SYSTEM half remains untested by this or
  any RAW run.
- No result under this profile may be blended into an aggregate score that
  hides which cases are `CURRENT` vs. `SIMULATED_FUTURE`, or which cases
  received only partial (RAW-only) scoring — per the Brain Score / System
  Score separation already required by ADR-0005.

## Status of actual execution

**No inference has been run under this profile.** No real
`InferenceBackend` exists yet (only `MockBackend`); no model has been
downloaded; TinyLlama baseline testing has not begun. This document fixes
the test conditions in advance of that work, per the review workflow —
implementing a real backend and running an actual benchmark are separate,
individually authorized future steps.

---

Project Scout / Scout AI Research
Copyright © 2026 Patrick Evan Lippy. All rights reserved.
