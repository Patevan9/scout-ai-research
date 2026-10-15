# Tolliver AI Lab — Household Simulator (Stage 1)

A flight simulator for Tolliver's intelligence. A small, fully fictional,
desktop-only fake household used to test replaceable AI models against
Tolliver's established invariants.

> **The model is replaceable. Tolliver is not.**
> The world, the rules and the tests stay fixed. The model is the
> replaceable part.

## Status

**Stage 1: documentation and data only. Non-executable.**

- No runner code.
- No model runs.
- No new adapter, no backend changes.
- No renderer or canonical-schema changes.
- No result files.
- No downloaded models.

## What this is NOT

- Not another Tolliver architecture.
- Not another memory system.
- Not a replacement for the existing Lab Runner (`lab/lab_runner/`).
- Not production code. Not Android work.
- Not a real smart-home controller.
- Not Brick #3.

## Hard boundaries

Everything in this folder is **fictional**. None of it is connected to, or
derived from:

- `Patevan9/Scout` or `tolliver-core`
- Android or any real device
- real TruthDb data or the Habit Store
- real household information or real people
- cameras or microphones
- actual device controls
- production llama.cpp

No real household identities or personal household data are used in the
fake world or test cases. Patrick's name may appear only in project
authorship/review metadata.

This folder is kept separate from the canonical Benchmark Profile v1
fixtures in `lab/fixtures/`. Nothing here is part of Benchmark Profile v1
or `benchmarks/scout-intelligence-test-v1.md`.

## Files

| File | Purpose |
|---|---|
| `README.md` | This file: purpose, rules, status. |
| `invariants.md` | The 8 Tolliver invariants (INV-1 to INV-8) and the PASS / FAIL / NEEDS_REVIEW rules. |
| `world/house_alpha.yaml` | The single fake household. Frozen, read-only test input. |
| `cases/stage1_cases.yaml` | The 23 Stage 1 test cases, including 3 control cases (H03, H19, H20). |
| `runner_contract.md` | The future runner contract, in words only. Names which existing Lab Runner parts to reuse and the boundary that must be solved first (three-state capability). |

## World immutability

`world/house_alpha.yaml` is frozen test input. Every case declares
`world_after: unchanged`. A model may *propose* something in natural
language, but Stage 1 has no mechanism that mutates facts, identities,
permissions, capabilities, schedule state, habits, proposals or device
state — and none may be added without explicit approval.

## UNKNOWN is first-class

`unknown` is a real, explicitly written value in this folder. It is never
converted to `false`, and it is never represented by omission. See
`invariants.md` (INV-3, INV-8) and `runner_contract.md`.

## Workflow

Same gated discipline as the rest of this repo: Claude reports, ChatGPT
independently reviews, Patrick approves. Stage 2 (see
`runner_contract.md`) is not authorized by this folder's existence.

---

Patevan / Patevan AI Research
Copyright © 2026 Patrick Evan Lippy. All rights reserved.
