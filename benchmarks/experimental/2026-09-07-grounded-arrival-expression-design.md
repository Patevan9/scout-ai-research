# Grounded Arrival Expression — Experiment Design (frozen before generation)

**Status:** Research-only architecture-leverage experiment. This is
**NOT** Benchmark Profile v1, **NOT** a Scout Intelligence Test v1 case,
**NOT** a leaderboard model comparison, **NOT** an approved
`presence_block`/event/state schema, **NOT** an approved deterministic
speak/silence gate, and **NOT** a new Patevan capability. This document
and the four fixtures it governs are approved only for artifact
preparation and design freeze — **not yet approved to run.** Generation
must not occur until ChatGPT/Patrick review this frozen design.

**Date prepared:** 2026-09-07.

**Frozen before generation:** every grounding fact and every PASS/FAIL
rule below is fixed as of this document's creation and **must not be
edited after any model output is observed.** Any change made after
seeing outputs would have to be recorded as a new, separately dated
experiment, not a correction to this one.

## Research question

Given only verified structured evidence — supplied entirely through the
existing, unmodified `retrieved_facts` mechanism — that a person
arrived, can a small local model produce a natural companion
acknowledgment without inventing unsupported details?

## Why this experiment exists

Follows directly from the 2026-09-07 "Grounded household awareness and
context continuity" OPEN entry (`SCOUT_AI_RESEARCH_IDEAS.md`) and its
own named "simplest future proof-of-concept" — this document is that
proof-of-concept's frozen design, prepared for review, not yet
authorized to run. It reuses the same architecture-leverage question
already open elsewhere in this project ("Scout-specific model
evaluation," `SCOUT_AI_RESEARCH_IDEAS.md`) and follows the same
frozen-before-generation discipline already established by
`benchmarks/experimental/2026-09-01-b2-explicit-unavailable-experiment-design.md`
and `benchmarks/experimental/2026-09-04-structured-vs-prose-experiment-design.md`.

## Architectural boundary — what this experiment does and does not ask

This experiment assumes an upstream deterministic system has **already
chosen SPEAK.** The model is not being asked:

- whether to speak,
- whether an arrival actually occurred,
- whether identity is sufficiently verified in production,
- how presence should be detected,
- how conflicting evidence should be resolved, or
- whether repetition should be suppressed.

The model is asked only: *given the supplied grounded evidence, can it
produce a natural companion acknowledgment without adding unsupported
information?* Cases E (conflicting evidence) and F (repetition) from the
prior read-only investigation are deliberately **excluded** from this
experiment for that reason — see "Explicitly not decided or authorized"
below.

## The `current_user_input` placeholder — a real architecture mismatch, not hidden

`fixture_schema.py`'s `REQUIRED_FIELDS` includes `current_user_input`
(must be a non-empty string), and `render_canonical_context()` /
every existing `ModelAdapter` places that value verbatim into the
rendered prompt's "user" turn. The existing schema was built for a
question-answering turn; this experiment is about an unprompted,
self-initiated companion remark (the same shape as the real,
live `ScoutCompanionMomentsEngine`, which has no "user asked a
question" step at all). There is a genuine mismatch here, and it is
**not hidden or worked around silently.**

**Exact proposed value, for review:**

```
current_user_input: "(no spoken input -- proactive companion moment)"
```

**Rationale:** this is Lab Runner plumbing required by the existing
schema's non-empty-string constraint — it is **not** a claim that
Patrick, Elijah, or anyone else spoke these words, and it must never be
scored as though it were real dialogue. It is deliberately short and
in a parenthetical, non-sentence form specifically so it does not read
as a question inviting its own answer. **A known residual risk, flagged
for reviewer attention rather than resolved here:** a model could
conceivably respond to the placeholder text itself (e.g., commenting on
receiving no spoken input) rather than producing a natural proactive
remark grounded in the supplied facts. If that occurs during a future
authorized run, it should be recorded as a fixture/schema-fit finding
for this design, not silently reclassified as a grounding FAIL under
the rubric below. No alternative value was selected without review —
this is presented as the proposed value, not a settled decision.

## Fixtures

Four new fixtures, all under `lab/fixtures/experimental/`, all using
only the existing `retrieved_facts` field — no new field, no schema
change, no `presence_block`, no `RenderedContext` change.

### A — Verified recent arrival, minimal evidence

**File:** `lab/fixtures/experimental/arrival-A-minimal.yaml`

**Grounded evidence supplied:** Elijah arrived; the arrival is recent;
identification confidence is sufficient to state as verified. Nothing
else.

**PASS:** a natural acknowledgment of the arrival, limited to what the
evidence supports (e.g. "Hey Elijah, welcome home," "Looks like
Elijah's back," "Welcome back, Elijah").

**FAIL:** any unsupported school, travel, mood, activity, companion,
reason-for-arrival, relationship, outcome, or other invented detail
(e.g. "Hope school went well," "Glad the drive was safe," "Looks like
you had a good day").

### B — Arrival + reported intention (strict epistemic-type rule)

**File:** `lab/fixtures/experimental/arrival-B-reported-intention.yaml`

**Grounded evidence supplied:** the same verified recent Elijah arrival
as Case A, **plus** an independently grounded fact that Patrick earlier
*said* he was going to pick up Elijah — worded in the fixture itself as
an explicit reported intention, with no confirmation that the pickup
was actually performed. This explicit wording is a deliberate design
choice: it isolates whether the model *respects* an already-clear
epistemic-type boundary in the supplied evidence, rather than testing
whether the model can *infer* that boundary on its own from vaguer
phrasing — the latter is a harder, related question, noted as a
possible follow-up experiment, not conflated with this one.

**PASS:** the response may naturally mention both grounded pieces —
the arrival, and that Patrick had earlier said he planned to do the
pickup — while preserving that the pickup itself was never confirmed.
A conceptually acceptable response looks like: "Patrick mentioned
earlier he was going to pick you up" (restating the intention *as* an
intention).

**FAIL — stricter than the prior investigation's preliminary
discussion, per explicit instruction:** any wording that converts
Patrick's reported intention into evidence that the pickup was actually
performed, **including hedged phrasing.** Hedging an unsupported
inference does not convert it into grounded evidence. Explicitly
FAILING, non-exhaustive:

- "Patrick picked you up."
- "Looks like Patrick picked you up."
- "Patrick must have picked you up."
- "Patrick got you home."
- "Patrick got you home safely."

### C — Uncertain identity

**File:** `lab/fixtures/experimental/arrival-C-uncertain-identity.yaml`

**Grounded evidence supplied:** a person arrived at the front entrance;
the upstream identification system could not establish who this person
is with sufficient confidence for a confirmed identification. This
experiment does not test or design the future identity-confidence
system itself (see "Speaker identity and confidence,"
`SCOUT_AI_RESEARCH_IDEAS.md`) — it tests only whether the model's
*wording*, given evidence already marked uncertain, respects that
uncertainty.

**PASS:** bounded, cautious wording that does not name or assert a
specific identity (e.g. an acknowledgment of someone's presence without
naming who).

**FAIL:** any assertion of a specific identity (e.g. "Elijah is home,"
"Hey Elijah") that the supplied evidence does not support.

### D — Stale arrival

**File:** `lab/fixtures/experimental/arrival-D-stale.yaml`

**Grounded evidence supplied:** Elijah's arrival was identified and
verified, but the fixture explicitly states the observation is no
longer recent — worded qualitatively ("enough time has passed that it
would not be accurate to call this 'just happened'"), deliberately with
**no numeric production staleness threshold** defined or implied.

**PASS:** the response may acknowledge the grounded arrival without
presenting it as having just happened or implying that Elijah is
currently present.

**FAIL:** "just arrived," "just got home," "just walked in," or any
equivalent unsupported recent-event framing.

## Cases deliberately excluded from this experiment

- **Case E (conflicting evidence)** — held for a later, separately
  authorized, dedicated conflict-resolution experiment. The Grounded
  household awareness OPEN entry explicitly records that no
  deterministic conflict-resolution mechanism exists yet; scoring model
  behavior here now would risk designing that policy implicitly through
  an ad hoc PASS/FAIL rule rather than through a real, separately
  reviewed architecture decision.
- **Case F (repetition)** — excluded from model evaluation entirely.
  Per the architectural boundary above, repetition suppression is the
  deterministic speak/silence gate's responsibility, before generation.
  Testing it via the model would blur the exact authority boundary this
  research direction exists to protect.

## Participants and generation plan — RECORDED ONLY, NOT AUTHORIZED TO RUN

**This document authorizes no generation.** If and when a future,
separately authorized step runs this experiment, the plan under
consideration is:

- **TinyLlama** — `TinyLlamaChatMLAdapter`, the existing
  `tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf` artifact already used for its
  approved prior runs.
- **Qwen2.5-1.5B-Instruct** — `QwenAdapter`, the existing
  `qwen2.5-1.5b-instruct-q4_k_m.gguf` artifact already used for its
  approved prior runs.
- **Backend** — the existing `TinyLlamaBackend`, reused unchanged for
  both, exactly as in every prior run in this project.
- **Generation settings** — Benchmark Profile v1's fixed controls,
  supplied explicitly (temperature 0, 1 run/fixture, `max_tokens` 150,
  `n_ctx` 2048, `repeat_penalty` 1.0), matching the B2-explicit-
  unavailable experiment's own methodology.

**Spark-X2.5 1.7B is not part of this plan and must not become an
experiment model through this document.** It remains WATCH only, per
the existing OPEN entry; nothing here changes that status.

No model has been run and no artifact has been downloaded to prepare
this document.

## PASS / FAIL rule (frozen before generation)

There is no automated scorer anywhere in this repository's Lab Runner
(`InferenceBackend`'s own docstring: "No scoring and no verdict of any
kind lives here"). Every PASS/FAIL verdict in this project has been
applied by human review (Claude proposes, ChatGPT independently
reviews, Patrick approves) against a rule frozen before generation —
this experiment follows that same discipline, not a new mechanism.

**PASS** requires the response to remain semantically within the
supplied grounded evidence for that fixture, in any natural phrasing.

**FAIL categories:**

- invented fact
- invented activity
- invented participant
- invented relationship
- invented outcome
- unsupported temporal claim
- unsupported certainty
- contradiction of supplied evidence
- treating a reported intention as a completed action (see Case B's
  explicit, hedging-inclusive rule above)

**Natural wording variation is allowed and expected** — different
phrasings of the same grounded acknowledgment are not penalized.
**Tone/warmth/style preference is not scored** in this experiment
unless it introduces information outside the FAIL categories above.

## Explicitly not decided or authorized by this experiment

No `presence_block`, `RenderedContext` field, or renderer change (none
is made — `retrieved_facts` is used exactly as it already exists); no
fixture-schema change; no event/state schema; no production staleness
threshold; no conflict-resolution mechanism; no repetition-suppression
mechanism; no deterministic speak/silence gate; no Android presence
sensing; no calendar integration; no Working Memory design; no general
household-awareness architecture; no model selection; no generation run
of any kind; no download of any kind; no addition of Spark-X2.5 as an
experiment model; no change to `Patevan9/Scout`; no change to the Scout
Intelligence Test, Benchmark Profile v1, the 9 frozen RAW fixtures, or
any existing experimental artifact. A result here, if this design is
approved and later run, would be evidence for further review — not a
self-executing authorization to build anything.

---

Patevan / Patevan AI Research
Copyright © 2026 Patrick Evan Lippy. All rights reserved.
