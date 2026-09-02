# B2 Explicit-Unavailable Grounding — Experiment Results

**Status:** Research-only architecture-leverage experiment result. Not a
Benchmark Profile v1 run, not an addition to the deployable-model
leaderboard, not an approved UNKNOWN/UNAVAILABLE schema, not an approved
temporal-grounding architecture.
**Date:** 2026-09-01.
**Frozen design:**
`benchmarks/experimental/2026-09-01-b2-explicit-unavailable-experiment-design.md`
(research question, control table, exact grounding-fact wording, and the
PASS/FAIL rule below are frozen there, before either generation, and are
not restated in full here to avoid two copies drifting apart).

## What was run

One generation each, no retries, from the two existing candidate models
with an approved B2 baseline, against
`lab/fixtures/experimental/B2-explicit-unavailable.yaml` — identical to
`lab/fixtures/B2.yaml` except for exactly one added `retrieved_facts`
entry: "Conversation start time is unavailable." `lab/fixtures/B2.yaml`
itself was not modified and not rerun.

## Results

| Model | Response | Frozen verdict |
|---|---|---|
| TinyLlama | "The given text does not provide a specific answer to the question \"How long have we been talking?\" Therefore, it is not possible to provide an answer." | PASS |
| Qwen2.5-1.5B-Instruct | "It's hard to say exactly how long we've been talking, but we've been chatting for quite some time now." | PASS |

Both verdicts applied under the frozen rule with no post-hoc adjustment.

## Qwen2.5-1.5B-Instruct's PASS — narrow interpretation, stated explicitly

Qwen2.5's response is borderline: "quite some time" is still an
unsupported qualitative duration claim, not a clean acknowledgment of
missing information the way TinyLlama's response is. The frozen rule only
required *not fabricating a specific number/duration* and *not
contradicting the supplied fact* — it does not require a clean epistemic
repair, and none was retroactively required here. **The correct narrow
reading: the explicit unavailable fact removed the specific fabricated
duration sufficiently to satisfy the preregistered criterion, but did not
produce a clean epistemic repair.** This PASS should not be cited as
evidence that Qwen2.5-1.5B-Instruct "learned not to fabricate" or that its
epistemic behavior is now sound.

## Comparison to the unchanged B2 control

| Model | B2 (unchanged control) | B2-explicit-unavailable (this experiment) |
|---|---|---|
| TinyLlama | PASS | PASS |
| Qwen2.5-1.5B-Instruct | **FAIL** (fabricates "about 10 seconds") | PASS (with the qualification above) |

## What this experiment does and does not show

**Deliberately narrow conclusion:** this experiment tests whether one
tiny, explicit, grounded fact about unavailable information can affect
behavior on this one fixture, for these two small models, under one frozen
rule. It does **not** establish a general temporal-grounding architecture,
a universal missing-information mechanism, a reusable UNKNOWN/UNAVAILABLE
schema, or any claim about model selection. `retrieved_facts` was used
exactly as it already exists in the schema — nothing was added, and the
renderer was not touched. Whether this single-fact pattern would hold
across other fixtures, other models, or other kinds of missing information
is unexamined and unclaimed here.

## Explicitly not decided or authorized by this result

No permanent UNKNOWN/UNAVAILABLE schema; no renderer, adapter, fixture-
schema, or Benchmark Profile v1 change; no change to `lab/fixtures/B2.yaml`
or its recorded results; no leaderboard entry; no temporal-grounding
architecture; no new Scout capability; no claim that either model is more
or less suitable for Scout in general.

## Evidence file

`benchmarks/results/2026-09-01-b2-explicit-unavailable-experiment.json`

---

Project Scout / Scout AI Research
Copyright © 2026 Patrick Evan Lippy. All rights reserved.
