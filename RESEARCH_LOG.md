# Research Log

A chronological record of meaningful research findings — **not a transcript.**
Conversations are not copied here; only the discoveries that came out of them.
Tag every entry:

- **VERIFIED** — checked directly against real Scout source or another
  primary source, not inferred or assumed.
- **DESIGN IDEA** — a proposed approach, not yet decided or approved.
- **OPEN QUESTION** — genuinely unresolved, needs more research or a decision.
- **SUPERSEDED** — an earlier entry that turned out to be wrong or incomplete;
  left in place with a pointer to the correction, never silently deleted.

Nothing in this log is authoritative on its own — see the review workflow and
source-of-truth order in `SCOUT_AI_STATUS.md`.

---

## 2026-08-22

**VERIFIED** — Scout has no Working Memory today. No conversation-start
timestamp exists anywhere in the app; Scout's own docs name this as a known,
explicit, unimplemented gap ("How long have we been talking?" / "What were we
talking about?"), not a bug.

**VERIFIED** — "Memory Import" is not a working feature. As of Scout PR #65
(merged 2026-08-21), both Settings → My Household rows toast "coming in a
future release." Only export exists, via a voice command through
`ScoutExportManager`.

**VERIFIED** — `ScoutExportManager.exportBrainToJson()`'s actual output
contains exactly three arrays: `truth` (TruthDb `entity_memory` rows —
entity/fact/val), `people` (named `PeopleDb` identity rows — face_hash, name,
first_met, last_seen), and `face_embeddings` (**name + embedding count only**,
via `COUNT(*) GROUP BY name` — not the real embedding vectors). `JournalDb`,
`HabitLayer`, `ConversationDb`, and diagnostics are excluded entirely.

**VERIFIED** — `HabitLayer.getSummaryForGemini()` is called only from
`ScoutPromptBuilder.kt` (Gemini's prompt path). `OfflinePromptBuilder.kt`
(TinyLlama's actual prompt builder) contains zero references to `habitLayer`.
TinyLlama never receives habit/pattern data in any form. HabitLayer itself
stores raw decaying keyword-frequency counts (14-day half-life), not
structured preferences — a "favorite_X" fact only ever comes from explicit
teaching into TruthDb, never inferred by HabitLayer.

**VERIFIED** — Vision output is 100% deterministic in Scout today.
`VisionAnswerBuilder.build()`'s `lastSceneLabels: List<Pair<String, Float>>`
does carry a confidence-like Float per label, but it's discarded one line
later (`.map { it.first.lowercase() }`) before whitelist filtering. No
position/bounding-box field exists anywhere in that interface. Separately,
`ScoutPromptBuilder.kt`'s Gemini system prompt states outright that Gemini
"carries no live camera frame or scene data." No brain — TinyLlama or Gemini —
reasons over vision data in any form today; a real `VISION_UNCLEAR`
deterministic fallback exists for the no-detection case.

**VERIFIED** — Scout's speech pipeline reads only
`SpeechRecognizer.RESULTS_RECOGNITION.firstOrNull()` — the single top
hypothesis. No confidence score, no n-best alternate list, is ever read or
used downstream.

**VERIFIED** — A Constitution-shaped pattern already exists in Scout, real
and merged, just scattered and unnamed: `ScoutIntentRouter`, `ScoutMemoryGate`,
`ScoutVisionGate`, `TeachExtractor`, and a retention-claim output guard
(`applyRetentionClaimGuard`, PR #39) all intercept a decision before, or check
an output after, a model's turn — without the model's cooperation being
required. Real evidence that a Constitution enforced outside the model is
achievable, not just a design aspiration.

**DESIGN IDEA** — Generalize the above scattered guards into one named,
unified policy engine that new Scout AI capabilities register with by
default, instead of each new capability inventing its own bespoke guard after
a bug report (this is a Scout AI research proposal, not something proposed
for the Scout app itself).

**DESIGN IDEA** — Separate benchmark scoring into a Brain Score (cases that
actually exercise the language/reasoning model) and a System Score (cases
primarily testing routing, retrieval, wake-word, STT handling, or other
infrastructure) rather than one collapsed "AI intelligence" number, so a
replacement brain is never penalized for an upstream Scout routing failure it
never had a chance to solve.

**DESIGN IDEA** — Tag every benchmark case with `test_scope`
(CURRENT / SIMULATED_FUTURE / BOTH) — distinguishing whether the *capability
under test* exists in Scout today at all, separately from whether the *test
input* happens to be simulated (e.g., injected text standing in for STT
output tests a capability that's still CURRENT, since routing+brain handling
of arbitrary text is real today regardless of input source).

**OPEN QUESTION** — What specific stronger small open-weight model, if any,
is worth evaluating against TinyLlama. Deliberately not decided — out of
scope until the benchmark itself is approved.

**OPEN QUESTION** — What a real Working Memory design for Scout should look
like. Not yet designed.

**OPEN QUESTION** — How a future brain would ever receive real-time vision
confidence/position data given today's architecture discards it before
whitelist filtering — this would require a change on the Scout app side,
which Scout AI cannot make directly (reference-only boundary) and hasn't been
scoped as a request to Patrick yet.

**SUPERSEDED** — An earlier draft of the benchmark stated vision confidence
"does not exist downstream at all." Corrected: a confidence Float does reach
`VisionAnswerBuilder`, it's discarded there, not earlier — see the VERIFIED
vision entry above for the accurate version.

**SUPERSEDED** — An earlier benchmark case (C4) assumed a repeated casual
topic could become a voiced, hedged HabitLayer-derived preference reachable
by the TinyLlama baseline. Corrected: TinyLlama never receives HabitLayer
data at all (see VERIFIED entry above) — the case now targets a future,
unbuilt integration and is marked `SIMULATED_FUTURE`.

**SUPERSEDED** — An earlier benchmark case (B4) implied Scout has a generic
"set that" scheduling/actuator capability. Corrected: no such capability
exists; the case was rewritten to test self-correction within a
teaching-shaped statement instead, which is real and testable today.

**MILESTONE** — Scout Intelligence Test v1 (25 cases) completed the full
gated review workflow — Claude drafted, ChatGPT independently reviewed across
two rounds, Patrick approved — and was recorded to
`benchmarks/scout-intelligence-test-v1.md`. Final scope: 21 CURRENT, 2
SIMULATED_FUTURE, 2 BOTH. No results exist yet; TinyLlama baseline testing has
not begun.

**MILESTONE** — The Least Sufficient Intelligence Principle (Fast Path /
Retrieval Path / Reasoning Path, with a general escalation-safety rule) and
the benchmark runner methodology (RAW / SYSTEM / BOTH per-case assignment,
canonical model-neutral RAW context, three permanently-separate evaluation
axes) each completed the gated review workflow and were recorded as
ADR-0004 and ADR-0005. See those records for full content — not duplicated
here.

**SUPERSEDED** — Benchmark v1's C4/F1 notes originally read as though
TinyLlama could not be scored on those cases at all. Corrected: the
limitation only applies to Scout's *current integrated* system — a RAW test
against a canonical simulated payload can still score TinyLlama (and any
future candidate) on both. Benchmark v1's wording was clarified accordingly,
not rewritten in substance.

**SUPERSEDED** — Benchmark v1's "Brain Score vs. System Score" section
previously read "a case tagged `Mixed` or `BOTH` gets both" — comparing an
`attribution` value (`Mixed`) against a `test_scope` value (`BOTH`) as if
they were the same field. Corrected to name both fields explicitly.

## 2026-08-23

**MILESTONE** — Scout AI Lab Runner v0.1 design (standalone PC test
harness, ModelAdapter/InferenceBackend boundary, fixture/result schemas,
Benchmark Profile process) completed two rounds of ChatGPT review and was
approved. Implementation authorized in small, individually gated steps —
see `lab/README.md` and `SCOUT_AI_STATUS.md` for current status, not
duplicated here.

**MILESTONE** — Lab Runner Step 1 (directory structure only) and Step 2
(the approved `ModelAdapter`/`InferenceBackend` interfaces, proven end to
end with a mock adapter and mock backend, plus one automated test) are
committed to `lab/`. No real model, no llama-cpp-python, and no TinyLlama
run exist yet.
