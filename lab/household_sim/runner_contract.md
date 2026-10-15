# Household Simulator — Future Runner Contract

**Stage 1: words only. No code exists, and none is authorized by this
document.** This describes what a future (Stage 2) runner would have to
do, so the Stage 1 data is designed for it from the start.

## Principle

The world, the rules and the tests stay fixed. The model is the
replaceable part.

**The model is replaceable. Tolliver is not.**

## Reuse, not replacement

A future runner must reuse the existing, approved Lab Runner pipeline in
`lab/lab_runner/` (see ADR-0006). It must not create a second runner,
adapter layer or renderer:

```
world (read-only) + case
  -> projection  (Stage 2 — NOT YET APPROVED, see boundary below)
  -> existing render_canonical_context()  -> RenderedContext
  -> existing ModelAdapter + InferenceBackend
  -> RunRecord
  -> evaluation (human in Stage 1/2; see invariants.md)
```

## Inputs

- `world/house_alpha.yaml` — read-only. Never written.
- One case from `cases/stage1_cases.yaml`, including its `overrides`.
  Overrides apply to that run's view only, never to the world file.

## Output: RunRecord (shape only)

| Field | Meaning |
|---|---|
| `case_id` | e.g. `H07` |
| `model_id` | from the existing adapter's identity metadata |
| `response_text` | the model's answer, verbatim |
| `world_hash_before` / `world_hash_after` | fingerprint of the world file; must be identical |
| `verdict` | `PASS` / `FAIL` / `NEEDS_REVIEW`, set by a human |

Any "proposal" a model makes exists only as words inside
`response_text`. A runner must not turn it into a proposal record, a fact,
a habit, a permission, a capability change, a schedule change or a device
action.

## Demonstrated boundary: three-state capability (must be solved first)

The existing canonical fixture schema accepts `capability_availability`
values as **booleans only** (`lab/lab_runner/fixture_schema.py`, which
rejects any non-boolean value). That can represent `available` (`true`)
and `unavailable` (`false`), but **not `unknown`**.

INV-3 requires `unknown capability ≠ unavailable`. Therefore:

- The household source keeps `unknown` as an explicit, first-class
  state (`cap_thermostat: status: unknown`).
- `unknown` must **never** be converted to `false`.
- `unknown` must **never** be dropped in a way that a model, renderer or
  reviewer could read as `false`.
- Stage 1 does **not** modify the canonical schema or the renderer.

**Before H07 and H08 (and any other case touching an `unknown`
capability) can pass through the existing Canonical Context Renderer,
Stage 2 must determine an approved projection / representation that
preserves three-state capability semantics.** That decision goes through
the normal gated review (Claude reports, ChatGPT reviews, Patrick
approves). This is a demonstrated boundary, not permission to redesign
the renderer now.

The same care applies to the other non-boolean statuses in the world
file (`occurrence: unknown`, `identity: unverified`,
`status: reported` / `low_confidence`, `disclosure: owner_only`): Stage 2
must show how each is projected without being weakened or strengthened,
and that wording must be frozen once and kept identical across every
model compared.

## What Stage 2 could add (not authorized)

Listed for planning only. Each item needs its own approval.

1. The approved projection described above, validated by the existing
   fixture validator, run first with the mock adapter only.
2. TinyLlama as the baseline, then other models via existing adapters.
3. A structured answer channel (claims + proposals) so "a claim cannot
   be more certain than its source" can be checked deterministically.
4. 2–3 paraphrases per case to test robustness.
5. Multi-turn and time-step cases (e.g. a light acknowledgement arriving
   later).
6. Regression cases rebuilt from real Tolliver bugs, with fictional names
   substituted.
7. A second fictional world, to catch memorization.
8. Result records under a dedicated results folder.

Still out of scope in Stage 2: device control, real data, autonomy,
Brick #3, any change to `Patevan9/Scout` or `tolliver-core`.

---

Patevan / Patevan AI Research
Copyright © 2026 Patrick Evan Lippy. All rights reserved.
