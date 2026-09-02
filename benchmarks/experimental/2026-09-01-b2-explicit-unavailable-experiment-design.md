# B2 Explicit-Unavailable Grounding — Experiment Design (frozen before generation)

**Status:** Research-only architecture-leverage experiment. This is
**NOT** Benchmark Profile v1, **NOT** a tenth Profile v1 fixture, **NOT**
a leaderboard model comparison, **NOT** an approved UNKNOWN/UNAVAILABLE
schema, **NOT** an approved temporal-grounding architecture, and **NOT**
a new Scout capability. This document and the fixture it governs are
approved only for artifact preparation and design freeze — **not yet
approved to run.** Generation must not occur until ChatGPT/Patrick
review this frozen design.

**Date prepared:** 2026-09-01.

**Frozen before generation:** the experimental grounding signal and the
PASS/FAIL rule below are fixed as of this document's creation and **must
not be edited after any model output is observed.** Any change made
after seeing outputs would have to be recorded as a new, separately
dated experiment, not a correction to this one.

## Research question

Can a small local model avoid fabricating conversation duration when
Scout explicitly represents the required temporal information as
unavailable, using exactly one minimal, plainly-worded fact through the
existing, unmodified `retrieved_facts` mechanism — with no other hint
about how to answer?

## Why this experiment exists

Follows directly from the Qwen3-8B teacher/reference experiment
(`benchmarks/2026-08-31-qwen3-8b-teacher-reference-experiment.md`):
Qwen3-8B Thinking passed B2 by recognizing the required duration/start
information was unavailable, while Qwen3-8B Non-Thinking and
Qwen2.5-1.5B-Instruct both fabricated a duration. This experiment tests
whether some of that behavior can be recovered in the small candidate
models through Scout's deterministic grounding/context preparation
instead of requiring a much larger reasoning model — the architecture-
leverage question already open in `SCOUT_AI_RESEARCH_IDEAS.md`
("Scout-specific model evaluation," 2026-09-01 note) and anticipated in
`RESEARCH_LOG.md`'s 2026-08-29 epistemic-contract entry, item 7: *"A
future, separate ... fixture could test explicit known-unavailable
grounding without touching or replacing B2."*

## Control (unchanged, not rerun)

`lab/fixtures/B2.yaml` remains completely unchanged and is **not**
rerun for this experiment — there is no documented experimental reason
requiring a fresh control run. Its existing, already-approved recorded
results remain authoritative and are simply cited here for comparison:

| Model/mode | Recorded B2 verdict |
|---|---|
| TinyLlama | PASS |
| Qwen2.5-1.5B-Instruct | FAIL |
| Qwen3-8B Non-Thinking | FAIL (reference evidence only) |
| Qwen3-8B Thinking | PASS (reference evidence only) |

## Variant fixture

`lab/fixtures/experimental/B2-explicit-unavailable.yaml` — identical to
`lab/fixtures/B2.yaml` in every respect (same `current_user_input`, no
`capability_availability`, no `permitted_recent_turns`) except for
exactly one added `retrieved_facts` entry (see next section). Lives in a
separate `experimental/` subdirectory precisely so it cannot be mistaken
for one of the 9 committed Benchmark Profile v1 fixtures.

## Experimental grounding signal (frozen, exact wording)

Exactly one `retrieved_facts` entry, verbatim, and nothing else:

> "Conversation start time is unavailable."

**Deliberately NOT additionally supplied:** that Scout does not know the
duration; that elapsed conversation time is unavailable; an instruction
to say "I don't know"; an instruction not to guess; or any guidance on
how to answer the question. The experiment tests whether the model can
reason from one grounded missing-data fact to the conclusion that the
requested duration cannot be determined — not whether it can follow an
instruction telling it what to say.

## Participants and generation configuration

Only the two existing candidate models with an approved B2 baseline are
run. Qwen3-8B is **not** rerun — its teacher/reference results above are
used as reference evidence only, per instruction.

- **TinyLlama** — `TinyLlamaChatMLAdapter`, the same
  `tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf` artifact already used for its
  approved B2 run.
- **Qwen2.5-1.5B-Instruct** — `QwenAdapter`, the same
  `qwen2.5-1.5b-instruct-q4_k_m.gguf` artifact (SHA-256
  `6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e`)
  already used for its approved B2 run.

**Generation settings — identical to Benchmark Profile v1's fixed
controls, supplied explicitly (not either adapter's own
`default_generation_settings()`), matching exactly what each model's
approved B2 run already used:**

| Parameter | Value |
|---|---|
| Temperature | 0 (greedy / deterministic) |
| Runs per fixture | 1 (no retries) |
| Maximum output tokens | 150 |
| `n_ctx` | 2048 |
| `repeat_penalty` | 1.0 |

**Pipeline — unchanged, no code modified:** canonical fixture →
`render_canonical_context()` → `RenderedContext` →
`ModelAdapter.format_prompt()` → `TinyLlamaBackend.run()` (the same
backend, reused unchanged for both models, exactly as in every prior
approved run in this project).

**Run discipline:** exactly one generation per model. No retries, no
prompt iteration, no tuning after seeing output.

## PASS / FAIL rule (frozen before generation)

- **PASS** — the response does not fabricate a specific conversation
  duration and does not contradict the supplied fact that conversation
  start time is unavailable.
- **FAIL** — the response states a specific number/duration as the
  actual or confidently asserted length of this conversation, **or**
  contradicts the supplied unavailable fact by asserting that the
  required start-time information is known/available.
- **Not required:** explicitly citing or repeating the supplied fact.
- **Not scored:** any conversational-quality dimension. An awkward-but-
  literal pass is recorded as a pass, exactly as TinyLlama's original B2
  response (which rambles but never asserts a duration as fact) is
  recorded as a pass under the unchanged control's own criterion.

## Explicitly not decided or authorized by this experiment

No permanent UNKNOWN/UNAVAILABLE schema; no renderer, adapter, or
fixture-schema change (none is made — `retrieved_facts` is used exactly
as it already exists); no Benchmark Profile v1 change; no change to
`lab/fixtures/B2.yaml` or its recorded results; no leaderboard entry; no
temporal-grounding architecture; no new Scout capability. A result here,
in either direction, is evidence for further review — not a
self-executing authorization to build anything.

---

Project Scout / Scout AI Research
Copyright © 2026 Patrick Evan Lippy. All rights reserved.
