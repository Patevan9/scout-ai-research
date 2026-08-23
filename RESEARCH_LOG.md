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

**MILESTONE** — Lab Runner Step 3: the canonical RAW fixture schema and a
loader/validator are committed to `lab/`, proven against one valid and
one intentionally invalid synthetic fixture plus one runner-integration
test — see `lab/README.md` and `SCOUT_AI_STATUS.md` for current status,
not duplicated here. PyYAML added as the first dependency. Still no real
model, no llama-cpp-python, no real benchmark fixtures, and no Benchmark
Profile.

**VERIFIED (Patrick-reported real-device observation, not independently
reproduced by Claude)** — TinyLlama identity/follow-up/correction failure,
observed on a Samsung Galaxy A32 running current production Scout. In one
conversation: Scout correctly answered "What are the names in my family?"
using its existing deterministic family/memory systems; the user then said
"Scout is also part of the family," and Scout replied as though "Scout"
were a dog's name ("My dog's name is Scout"); corrected with "No, your
name is Scout," Scout then denied having a personal name and offered a
generic dictionary-style definition of "scout" (a common dog name / a
military-scouting abbreviation) instead of recognizing its own stable,
already-known identity. Research significance: follow-up-context weakness,
self-identity weakness, correction-handling weakness, a hallucinated
relationship/fact ("my dog"), failure to respect Scout's own stable,
deterministically-owned identity, and unnecessary generic generation in a
case where a stable deterministic fact should have dominated. The exact
transcript was not independently reproduced by Claude this session —
recorded exactly as reported. This does not change Scout Intelligence
Test v1 or authorize adding a new case (e.g. a "B5") — any such change
requires its own separately reviewed step.

**VERIFIED (Patrick-reported real-device observation, not independently
reproduced by Claude)** — TinyLlama performance benchmarks on two real
devices, using current production Scout's hidden TinyLlama Performance
Benchmark: 4 synthetic prompt classes (short_factual, personal_memory,
conversational, long_history) across 6 thread configurations (2/2, 2/4,
3/3, 4/4, 5/5, 6/6), test order rotated to reduce thermal/order bias.
These are controlled benchmark prompts modeled on Scout's production
prompt shape, **not** exact live-conversation latency measurements.

*Galaxy Fold 7* — all 24 runs recovered. Approximate average total
generation time by thread configuration: 2/2 ~4.81s, 2/4 ~3.35s, 3/3
~3.42s, 4/4 ~2.99s, 5/5 ~2.48s, 6/6 ~2.60s. Best overall configuration in
this run: 5/5 (~2.48s) — maximum thread count (6/6) was slightly slower
overall than 5/5; possible causes (scheduling, heterogeneous cores,
thermals) remain hypotheses only, not established. Per-class examples:
short_factual 2/2 ~1.91s, 5/5 ~1.44s, 6/6 ~1.24s; long_history 2/2 ~8.83s,
5/5 ~3.68s.

*Galaxy A32* — benchmark captured via screen recording; not all 24 values
were recovered with enough confidence to calculate complete
per-configuration averages, so **no A32 winning thread configuration
should be declared from this partial dataset.** Clearly readable recovered
values (seconds, total generation time): 2/2 short_factual ~6.09, 2/4
personal_memory ~7.39, 3/3 conversational ~10.95, 4/4 long_history ~17.17,
2/4 short_factual ~4.45, 3/3 personal_memory ~8.39, 4/4 conversational
~9.32, 5/5 long_history ~9.32, 3/3 short_factual ~4.69, 4/4
personal_memory ~8.60, 5/5 conversational ~9.14. One same-class comparison
stands out even in this partial dataset: short_factual 2/2 (~6.09s) vs.
short_factual 2/4 (~4.45s) — meaningful thread-configuration sensitivity
on this slower device.

*Instrumentation warning* — displayed fields including `prefill=0ms`,
`gen=.../0ms`, and `0.0 tok/s` appear unreliable in this run and must
**not** be treated as valid performance evidence until the instrumentation
is investigated; rely primarily on `total_ms` and TTFT.

*Current Scout runtime context* (Patrick-reported, not independently
verified by Claude): production Scout generation currently uses
`n_ctx=2048`, `n_batch=512`, `n_threads=2`; the native path destroys and
recreates the llama context on every generation call — no KV-cache/context
reuse occurs across calls.

Potential future research leads (none assumed beneficial until actually
measured): device-appropriate thread configuration, prompt-length
reduction, context/KV-cache reuse, generation-length reduction,
quantization/model choice, and specialized Scout-oriented local models.
This evidence does not change Scout Intelligence Test v1, the approved
25-case benchmark, any Lab Runner code, or any fixture, and does not
authorize modifying current production Scout — recorded as research
evidence only, for later reviewed incorporation.

**MILESTONE** — Canonical Context Renderer, Steps 1–4A, all reviewed and
approved: fixture validator hardening for `capability_availability` and
`simulated_vision_payload.detections` (`a03577e`); the `RenderedContext`
dataclass (`6ca6757`); `render_canonical_context()` implementing the five
deterministic rendering rules — facts, vision evidence, capabilities,
connectivity, plus the two deliberately-deferred cases (`memory_habit_payload`
populated, empty vision detections) that raise rather than guess (`af5bbcd`);
reviewer-field leak protection tests (`77d5b62`); and the Step 4A correction
replacing flattened `conversation_block` text with structured `RenderedTurn`
objects, resolving a real architectural blocker (TinyLlama's separate ChatML
turns can't be reconstructed from flattened text without fragile parsing)
without ever writing that parser (`8495909`). Full detail lives in each
commit's own message and this session's reports, not duplicated here.

**MILESTONE** — Step 5, Option B `ModelAdapter` interface migration,
reviewed and approved at commit `3ad0598`. The pipeline is now enforced by
construction: canonical context → `render_canonical_context()` →
`RenderedContext` → `ModelAdapter` → `InferenceBackend`. `run_case()`
invokes the renderer before calling the adapter; `MockAdapter` and
`TinyLlamaChatMLAdapter` receive only `RenderedContext`, never the raw
canonical dict — reviewer-only fields (`test_id`, `source_case`, `expected`,
`notes`) are structurally unavailable to either. Structured conversation
turns become TinyLlama's `<|user|>`/`<|assistant|>` ChatML turns directly,
with no string parsing. TinyLlama's verified ChatML format and Scout's
system instruction are unchanged in substance; a new `CANONICAL CONTEXT`
section (fixed order: state, capability, facts, memory/habit, vision
evidence) is folded into the system turn only when populated. Full test
suite: 44/44 passing. `B1.yaml`/`D2.yaml`/`F1.yaml` remain untracked pilot
fixtures, not part of the permanent benchmark record. No real model, no
real inference backend. Next implementation step not yet authorized.
