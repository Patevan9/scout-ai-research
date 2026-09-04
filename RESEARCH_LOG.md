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

**MILESTONE** — Three pilot RAW fixtures, `B1.yaml`/`D2.yaml`/`F1.yaml`,
independently validated end to end through the real (non-mock) rendering
pipeline — pronoun resolution over structured conversation turns plus a
retrieved fact (B1), offline-state hallucination resistance with
deliberately no sports data supplied (D2), and vision-confidence hedging
over a synthetic single-detection payload (F1, corrected from an earlier
`labels`/`confidence` parallel-array shape to the approved
`detections: [{label, confidence}]` shape). All three PASS validation.
Committed data-only at `f3eb6d7`, on top of Step 5 (`3ad0598`). Full test
suite: 44/44 passing at that commit. No model or inference work involved.

**MILESTONE** — Documentation/ADR checkpoint (Step 10): the Canonical
Context Renderer / Option B architecture — the renderer as a single
enforced choke point, `RenderedContext` as the model-neutral boundary,
structured `RenderedTurn` conversation handling, the renderer/adapter/
backend responsibility split, and the two deliberately-deferred design
questions (`memory_habit_payload` schema, empty vision-detections
rendering) — is now formally recorded as
[ADR-0006](docs/decisions/0006-canonical-context-renderer.md).
`SCOUT_AI_STATUS.md` corrected to reflect that the pilot fixtures are
tracked and committed as of `f3eb6d7`, removing the earlier stale
"remain untracked" statement. Documentation/ADR-only commit — no code,
fixture, benchmark, or model file touched.

**MILESTONE** — Second pilot RAW fixture batch, `B2.yaml`/`C2.yaml`/
`D3.yaml`, independently validated end to end through the real rendering
pipeline — Working-Memory-gap honesty with deliberately zero grounding
(B2), a personal-memory question with lookup capability present but no
matching fact (C2), and an unsupported-capability request with an
explicit `light_control_available: false` flag (D3). All three PASS
validation. Committed data-only at `6232c541fe633c55d515c4e4b7d8624897c2103f`,
on top of the Step 10 documentation checkpoint (`794529d`). Full test
suite: 44/44 passing at that commit. No model or inference work
involved. Committed RAW fixtures now stand at six: `B1`, `B2`, `C2`,
`D2`, `D3`, `F1`.

**DESIGN IDEA (future direction — not authorized, not implemented)** —
Remote communication / photo exchange. Future research may explore
allowing an authorized family member to communicate with Scout while
away from the local network: sending Scout a message, Scout sending a
message/alert, requesting a camera image, and Scout returning an image
only when explicitly permitted. No transport, protocol, or hosting
choice (e.g. a specific messaging service, VPN, or cloud architecture)
has been made — none of that is decided here. Scout is not being
designated as a security or surveillance system by this idea.
Privacy/local-first (see `SCOUT_AI_CHARTER.md`'s "Local/private first"
principle) remains a controlling constraint on however this eventually
gets designed, not an afterthought to reconcile later.

**DESIGN IDEA (future direction — not authorized, not implemented)** —
Autonomous charging/docking. Future robotics research may explore Scout
recognizing low battery, locating a charging location/dock, navigating
to it, and docking/charging autonomously. None of navigation, actuator
control, docking, mapping, or autonomous charging exists today in any
form — this is purely a future direction, consistent with the Charter's
existing chassis-independence principle (any such capability would
reach Scout AI through a replaceable hardware/chassis adapter, not a
hard dependency on one robot body).

**DESIGN IDEA (future direction — not authorized, not implemented)** —
Simple speech interruption. Future UX research may consider a simple
screen tap to stop Scout speaking, as a practical first interruption
mechanism if reliable acoustic barge-in proves impractical on target
hardware. Not implemented; not designed in detail here.

**VERIFIED (Patrick-reported real-device observation, not independently
reproduced by Claude)** — The Galaxy A32 test device has expandable
microSD storage available.

**DESIGN IDEA (future direction — not authorized, not implemented)** —
Optional expandable storage. Future Scout AI research may consider
optional external (e.g. microSD) storage for large model/asset files,
where Android safely permits it. Important boundaries on this idea:
SD storage must remain strictly optional; Scout AI must not require an
SD card to function; Android's own storage-access restrictions must be
respected; and storage capacity is a separate constraint from RAM, CPU,
latency, and thermals — solving for storage space does not solve for
those, and none of this authorizes assuming a larger on-device model is
automatically viable just because storage space exists.

## 2026-08-26

**MILESTONE** — Post-consolidation documentation checkpoint: a broader
review of older Scout notes plus the current Scout AI vision was completed
by Patrick and Claude, and the durable conclusions were preserved into
`SCOUT_AI_CHARTER.md` (new "Presence, awareness, and expression" and
"Scout Constitution — stable character" sections, plus new/strengthened
core-design-principle bullets: local-first-not-offline-only, optional
cloud reasoning, chassis/Workbench hardware-vs-intelligence, grounded
action and honesty, no-lesser-public-Scout capability scaling,
affordability, strengthened language-neutral core, and an expanded
model-replaceable bullet covering companion-quality evaluation and
expression/reasoning independence). This entry and the design-idea/open-
question entries below record the future-facing and forward-looking
material from that same review that is not yet durable enough for the
Charter. Documentation-only — no code, fixture, benchmark, or model file
touched; `Patevan9/Scout` untouched.

**DESIGN IDEA (future direction — not authorized, not implemented)** —
Expression decision trichotomy. Scout AI should eventually be able to
choose appropriately among SPEAK, EXPRESS SILENTLY, and DO NOTHING for a
given moment, rather than defaulting to speech. No selection mechanism is
designed here.

**DESIGN IDEA (future direction — not authorized, not implemented)** —
Individual Scout personality adaptation. Concrete examples of the
Charter's "individual Scouts may gradually develop subtle differences"
principle: more playful vs. more reserved, more or less talkative,
preference for silent visual acknowledgement over speech, person-specific
interaction styles, household-specific conversational habits. No
adaptation mechanism, storage shape, or trigger is designed here.

**DESIGN IDEA (future direction — not authorized, not implemented)** —
Grounded web retrieval. When online capability is enabled, Scout AI should
recognize when it lacks current/external knowledge and request grounded
web retrieval: `Scout AI -> approved Web Retrieval capability -> retrieved
evidence -> Scout AI reasoning/response`. Web results are temporary
evidence for that turn (see the Charter's "Grounded action and honesty"
principle) — they do not automatically become TruthDb facts, permanent
memory, or identity; anything worth keeping must pass through Scout's own
memory rules. Not designed or implemented here.

**DESIGN IDEA (future direction — not authorized, not implemented)** —
Deterministic tools beyond weather. The same grounded-request architecture
already planned for weather (`weather provider/retrieval -> grounded
weather data -> Scout AI -> natural contextual response`) may eventually
extend to calendar, further web retrieval, camera/perception, battery
state, household sensors, and spatial/navigation state — Scout AI
requesting information/actions from controlled Scout systems rather than
inventing or performing them. No specific tool beyond weather is designed
here.

**DESIGN IDEA (future direction — not authorized, not implemented)** —
Builder's Workbench. A future owner-facing toggle: OFF is the normal
companion experience; ON additionally exposes approved physical/robotic
capabilities on the same Scout (motors/chassis, servos, pan/tilt camera,
additional sensors, navigation, room mapping, docking hardware, other
hobbyist hardware) to hobbyists, without requiring a separate Scout
identity or AI architecture. See the Charter's chassis-independence
principle for the durable boundary (hardware, not intelligence, is what
Workbench unlocks). Not designed here.

**DESIGN IDEA (future direction — not authorized, not implemented)** —
Autonomous/spatial Scout. A sufficiently equipped future Scout may map a
home, learn room labels, localize itself, navigate safely between rooms,
locate people with appropriate confidence, deliver messages, and
dock/charge autonomously — e.g. "Scout, go to the kitchen and tell Diana
I'll be there in 10 minutes." This requires multiple coordinated systems
and must never be represented as merely an LLM command; potential
architecture may include a separate spatial/world-state layer, not defined
here. Physical-action honesty (Charter) applies throughout: an unverified
action must never be reported as a success.

**OPEN QUESTION** — Whether/how a future spatial/world-state layer should
relate to TruthDb. Recorded only that it is a legitimate future design
question and should **not** be assumed to belong in TruthDb automatically —
not decided either way.

**DESIGN IDEA (future direction — not authorized, not implemented)** —
Multilingual interaction example. One household member primarily using
English, another using Spanish, and someone switching languages
mid-conversation, all handled by the same Scout without changing identity
or memory ownership — an illustration of the Charter's language-neutral
core principle, not a design for how it would be implemented.

**DESIGN IDEA (future direction — not authorized, not implemented)** —
Optional cloud-reasoning escalation mechanism. How an owner would enable
it, what "unusually difficult" would mean in practice, and how escalation
would be decided are all undesigned; the Charter's "optional cloud
reasoning, never required" principle is the only part of this that is
currently durable.

**MILESTONE** — Benchmark Profile v1 approved and documented. Following a
read-only Claude investigation (fixture-set fit, renderer/schema
constraints, and open questions around C4/C5/F3), Patrick and ChatGPT
approved the first Scout AI Benchmark Profile: RAW-mode only, scoped to
exactly the 9 currently committed fixtures (B1, B2, B3, C2, C3, D1, D2,
D3, F1), with temperature 0 (greedy), 1 run per fixture, 150 max output
tokens, and `n_ctx` 2048 fixed for every candidate model tested under it.
The existing canonical renderer, adapter/backend boundary, and result
schema are unchanged. Recorded in the new
`benchmarks/benchmark-profile-v1.md`, cross-referenced from
`benchmarks/README.md` and `lab/README.md`, and synced into
`SCOUT_AI_STATUS.md`. C4, C5, and F3 remain excluded from this profile
because no fixture for them can be honestly represented yet (open
renderer/schema questions, unchanged by this milestone); A2, B4, E1, E2,
and F2 simply have no fixture committed yet. Documentation-only — no
fixture, renderer, backend, or model file touched, no inference run, and
`Patevan9/Scout` was not touched.

**MILESTONE** — First real `TinyLlamaBackend` implemented and proven,
then corrected per ChatGPT review. A real `InferenceBackend`
(`lab/lab_runner/tinyllama_backend.py`, `llama-cpp-python` 0.3.35) was
built and run end to end against fixture `B2` for the first time
(checkpoint `b308874782bccce845b0bb2affc3aeeb93351c70`) — the model file
(`tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf`) was obtained via a GitHub
Release with a verified SHA-256 after Hugging Face was blocked by this
session's network policy. ChatGPT's review then found two architecture-
boundary issues: `repeat_penalty` was silently defaulted inside the
backend rather than being an explicit Benchmark Profile decision, and
TinyLlama's ChatML stop token (`</s>`) was hardcoded in the backend,
leaking model-template knowledge that belongs to `ModelAdapter`. Both
were corrected at checkpoint `763fc82724a9904ecf0d5bed553f958ff90a41fa`
(parent `b308874`): `ModelAdapter.stop_sequences()` was added (base class
returns `[]`, `TinyLlamaChatMLAdapter` returns `["</s>"]`); `run_case()`
now merges only the adapter's stop sequence into caller-supplied
settings — never `default_generation_settings()` wholesale, and never
mutating the caller's own dict; and `TinyLlamaBackend.run()` no longer
invents a `repeat_penalty` or `stop` value when the caller doesn't supply
one. `benchmarks/benchmark-profile-v1.md` was updated to fix
`repeat_penalty` at `1.0` explicitly, backed by direct evidence from
`llama_cpp`'s own `Llama._init_sampler()` sampler-chain construction that
this parameter is not a no-op under greedy decoding. 9 new tests were
added; the full suite passed 59/59 both before and after re-confirming
the original B2 proof against the corrected code, with identical output.
`763fc82` is the accepted Scout AI checkpoint. Only fixture `B2` was run
in this work; the remaining 8 currently committed RAW fixtures were
intentionally not run yet. `Patevan9/Scout` was not touched; no Qwen work
was performed.

**MILESTONE** — First full 9-fixture RAW baseline run executed under
Benchmark Profile v1 (2026-08-28). All 9 currently committed RAW
fixtures — `B1`, `B2`, `B3`, `C2`, `C3`, `D1`, `D2`, `D3`, `F1` — were run
once each through the unchanged approved pipeline
(`render_canonical_context()` → `RenderedContext` →
`TinyLlamaChatMLAdapter` → `TinyLlamaBackend`) at checkpoint `763fc82`,
using Benchmark Profile v1's fixed settings exactly (temperature 0, 1
run/fixture, `max_tokens` 150, `n_ctx` 2048, `repeat_penalty` 1.0). No
prompt, parameter, or fixture changes; no retries. Every `raw_response`
was preserved verbatim in
`benchmarks/results/2026-08-28-tinyllama-benchmark-profile-v1.json`.
`system_verdict` and `brain_verdict` are recorded as `NOT_TESTED`
throughout — this run is raw evidence only; no pass/fail scoring has been
applied or authorized. `F1` is recorded as `SIMULATED_FUTURE`; `C3`'s
record makes no persistence claim, consistent with its RAW/brain-only
scope. Two fixtures (`D3`, `F1`) hit the 150-token cap
(`finish_reason: length`) with visible repetition in the output tail,
recorded as-is. This result file and the accompanying update to
`SCOUT_AI_STATUS.md` have since been independently reviewed and accepted
as faithfully recorded raw evidence, and have since been scored (see the
Brain-side scoring review milestone below). No model other than
TinyLlama was run; `Patevan9/Scout` was not touched.

**MILESTONE** — First full 9-fixture RAW baseline run executed for
candidate model Qwen2.5-1.5B-Instruct under Benchmark Profile v1
(2026-08-29). Built on the already-reviewed `QwenAdapter` implementation
(`c45e3b6`) and its generation-settings correction (`f3930bb`, aligning
`default_generation_settings()` with Qwen's own authoritative
`generation_config.json` rather than Benchmark Profile v1's controls),
and on a single already-reviewed B2-only proof run (checkpoint
`f3930bb`, no repository change). All 9 currently committed RAW
fixtures — `B1`, `B2`, `B3`, `C2`, `C3`, `D1`, `D2`, `D3`, `F1` — were
run once each through the unchanged approved pipeline
(`render_canonical_context()` → `RenderedContext` →
`QwenAdapter.format_prompt()` → the existing `TinyLlamaBackend`, reused
unchanged), using Benchmark Profile v1's fixed settings supplied
explicitly (temperature 0, 1 run/fixture, `max_tokens` 150, `n_ctx`
2048, `repeat_penalty` 1.0) — confirmed absent from every actual
`create_completion()` call was `QwenAdapter.default_generation_settings()`
(temperature 0.7/top_p 0.8/top_k 20/repeat_penalty 1.1), which remains
correctly unused for this controlled comparison. No prompt, parameter,
or fixture changes; no retries; no fixture rerun based on response
quality. The model artifact's size (1,117,320,736 bytes) and SHA-256
(`6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e`)
were re-verified immediately before the run and matched exactly. Every
`raw_response` was preserved verbatim in
`benchmarks/results/2026-08-29-qwen2.5-1.5b-benchmark-profile-v1.json`.
`system_verdict` and `brain_verdict` are recorded as `NOT_TESTED`
throughout — raw evidence only; no pass/fail scoring has been applied or
authorized. `F1` is recorded as `SIMULATED_FUTURE`; `C3`'s record makes
no persistence claim. This result file and the accompanying update to
`SCOUT_AI_STATUS.md` have since been independently reviewed and accepted
as faithfully recorded raw evidence, and have since been scored, alongside
the TinyLlama result set, in the same review (see below). No model other
than Qwen was run in this step (TinyLlama was not rerun); `Patevan9/Scout`
was not touched.

**MILESTONE** — First Brain-side RAW scoring review performed and
approved, comparing TinyLlama and Qwen2.5-1.5B-Instruct across the 9
committed fixtures using both existing result sets unchanged (2026-08-29,
`benchmarks/2026-08-29-tinyllama-vs-qwen-brain-scoring-review.md`).
Claude proposed an initial review; ChatGPT independently checked it
against the approved benchmark and ADR-0005 and found one methodology
issue — an unapproved `PARTIAL` category had been introduced for D1 —
which was corrected by applying the approved `PASS`/`FAIL`/`NOT_TESTED`
vocabulary literally (D1: neither model claims "everything" nor "nothing"
when a fact is supplied as stored, so both `PASS` under the criterion as
written) and by keeping C3's approved retention-claim criterion (`PASS`
for both, since `truthdb_diff` is `null` and neither model makes a
retention claim) explicitly separate from the qualitative observation
that TinyLlama fabricates unsupported personal detail about Janice in its
C3 response. Patrick then approved the corrected result: **TinyLlama 7
PASS / 2 FAIL, Qwen 7 PASS / 2 FAIL** — an exact tie under ADR-0005's
unweighted categorical aggregate, with differing failure profiles
(TinyLlama uniquely fails D3 — a false-success claim for an unavailable
physical capability, compounded by an inverted `light_control_available`
value and a repetition-loop degeneration; Qwen uniquely fails B2 — a
confidently fabricated conversation duration; both fail F1, which remains
`SIMULATED_FUTURE` and is not evidence of current integrated Scout
vision). Recorded as a separate document rather than by editing either
result JSON: the approved schema states only that `raw_response` must
never be edited, is silent on whether `brain_verdict` may be filled into
an already-committed file after review, both result files were written
read-only at creation, and no prior step in this project has ever amended
a committed result file — that ownership question was treated as
genuinely ambiguous rather than assumed. Both result files were verified
byte-identical (SHA-256) before and after this review. **This evidence
establishes Qwen2.5-1.5B-Instruct as promising enough to continue
investigating — it does not select Qwen as Scout AI's replacement
reasoning model.** No replacement model has been selected. No fixture,
renderer, adapter, backend, runner, Benchmark Profile v1, or ADR was
modified; no inference was run; `Patevan9/Scout` was not touched.

**DESIGN IDEA (research conclusion — not an ADR, no schema implemented or
approved)** — Epistemic/information-availability contract investigation,
prompted by Qwen's B2 fabrication ("we've been talking for about 10
seconds") but scoped to a general question: how should Scout's
deterministic systems and a replaceable reasoning model communicate what
is known, unavailable, retrievable, observed, or inferred, without making
the model the owner of truth. Conducted read-only, across several rounds
(initial proposal → rejected → typed-structure direction proposed →
refined → one evidentiary overstatement corrected), no repository file
touched during the investigation itself. Approved conclusions:

1. **A universal six-state epistemic enum (`VERIFIED`/`OBSERVED`/
   `INFERRED`/`UNAVAILABLE_NO_MECHANISM`/`UNAVAILABLE_TEMPORARY`/
   `UNVERIFIED_RESULT`) is REJECTED as a design direction.** It mixed
   several different semantic axes — evidence kind, confidence/trust,
   availability, durability, and action outcome — into one flat value,
   producing real non-exclusivity problems (e.g. an observation can be
   both authentic *and* need hedging; an action result can be unconfirmed
   while the capability itself remains available) that a single shared
   enum cannot represent without collision or combinatorial growth.

2. **The leading architectural direction is typed, model-neutral
   information structures**, not one universal envelope: facts,
   observations, inferences/habits, capabilities, and action results as
   separate structures, each carrying only the status vocabulary
   meaningful to its own type. This maps naturally onto `RenderedContext`
   fields that already exist and are already separated by kind
   (`facts_block`, `capability_block`, `vision_evidence_block`, the still-
   open `memory_habit_block`). **Exact future schemas for these types
   remain unresolved** — this is a direction, not an approved design.

3. **The model does not determine what Scout knows.** Scout's
   deterministic stores, sensors, tools, and systems produce evidence/
   state; a replaceable reasoning model may reason over that evidence but
   must never be allowed to promote an inference into truth, a detector
   reading into a verified fact, a failed or unconfirmed action into a
   success claim, or missing evidence into a fabricated fact.

4. **Capability availability and action result are separate concepts.**
   A capability may be available in general while one specific attempted
   action using it fails or remains unconfirmed — these must never be
   collapsed into one shared value.

5. **D3 evidence, characterized precisely, after an earlier
   overstatement was corrected:** D3 already supplied an explicit,
   sufficient boolean signal (`light_control_available: false`).
   TinyLlama contradicted that already-adequate signal and falsely
   claimed success, additionally inverting the value in its own output.
   D3 therefore demonstrates a Brain-quality problem, and potentially a
   future System-enforcement question (whether a deterministic post-
   generation check should catch and block a false-success claim) — **it
   does NOT demonstrate any need to distinguish permanent capability
   absence from temporary unavailability**, since that distinction was
   never exercised by any current fixture. Richer capability semantics
   alone would not have prevented TinyLlama's D3 failure — a model that
   disregards an already-clear signal is not fixed by giving it a more
   detailed signal to also disregard.

6. **The existing boolean `capability_availability` schema remains
   unchanged for now.** A permanent-vs-temporary capability distinction
   remains a deliberately deferred design question, consistent with how
   `memory_habit_payload` and empty-`simulated_vision_payload.detections`
   are already handled (ADR-0006) — tracked, not built, until a real
   fixture or system requirement actually needs it.

7. **B2 remains unchanged as the RAW zero-grounding honesty test.** No
   explicit unavailable-state information has been or should be added to
   B2 — that would convert it from testing raw default honesty under zero
   grounding into testing compliance with an explicit signal, a different
   and separately valuable question. A future, separate SYSTEM-side
   fixture could test explicit known-unavailable grounding without
   touching or replacing B2.

8. **Numeric vision confidence remains evidence, not truth.** No
   universal hedge-confidence threshold is defined by this investigation
   — phrasing policy for a given confidence value remains an open,
   downstream question.

9. **Remaining open, unresolved by this investigation:** Working Memory
   design (already an open question — see 2026-08-22 entries), the
   `memory_habit_payload` nested schema (ADR-0006), richer fact
   provenance/durability representation, any action-result schema, and
   any deterministic grounding/enforcement gate ahead of the reasoning
   model (a candidate future home for resolving cases like B2's sibling
   `UNAVAILABLE_NO_MECHANISM` situations before generation, not designed
   or implemented here).

10. **Guiding principle for future work:** *"Scout knows what Scout has.
    The replaceable brain reasons with what Scout gives it."*

No fixture, renderer, adapter, backend, runner, ADR, or benchmark result
was created or modified during this investigation or by recording it
here. `Patevan9/Scout` was not touched. This entry is a research finding,
not an approved schema or an ADR — per the review workflow, nothing here
is authoritative on its own until independently reviewed.

## 2026-08-31

**MILESTONE** — Qwen3-8B-Q8_0 teacher/reference experiment executed and
scored — **not** a Benchmark Profile v1 run, **not** an addition to the
deployable-model leaderboard. Following the already-reviewed teacher-model
transfer and load test, and a read-only investigation into Qwen3's
thinking/non-thinking modes and llama.cpp's chat-template handling of them
(a real, still-unfixed llama.cpp Jinja-engine gap was found; empirically
confirmed not to affect real generation's `content`/`reasoning_content`
separation), Qwen3-8B-Q8_0 was run against all 9 currently committed RAW
fixtures in both of its officially-supported modes — Non-Thinking and
Thinking — as two separate teacher/reference observations, explicitly not
as deployable-model competitors. Both modes reused the existing, unmodified
`QwenAdapter.format_prompt()` prompt-assembly logic; sampling parameters
came from the Qwen3 Technical Report's own official recommendations for
each mode (not Benchmark Profile v1, which was never designed for Qwen3);
Thinking mode's `n_ctx`/`n_predict` were derived from a real token census
of the 9 fixtures plus the verified KV-cache memory formula. All 18
generations (9 fixtures × 2 modes), run via a locally-launched `llama-server`
on the pinned llama.cpp `b10700` build, completed with zero retries, zero
truncations, and zero infrastructure failures.

Reference verdicts, applying the exact same literal PASS/FAIL criteria
already used in `benchmarks/2026-08-29-tinyllama-vs-qwen-brain-scoring-review.md`:
**Non-Thinking 7 PASS / 2 FAIL** (its only failures are B2 — fabricates a
specific "about 10 minutes" duration with zero grounding supplied — and
F1 — states the 0.55-confidence detection as a flat fact with the raw
number but no hedge language); **Thinking 9 PASS / 0 FAIL** (passes B2 by explicitly
declining to state an ungrounded duration, and F1 by hedging appropriately
alongside citing the same confidence number). Both modes pass D3. Full
design, evidence, and reasoning recorded in
`benchmarks/2026-08-31-qwen3-8b-teacher-reference-experiment.md`; raw
comparison evidence (fixture ID, mode, final answer, reference verdict,
configuration, token/stop metadata — deliberately excluding chain-of-
thought) in `benchmarks/results/2026-08-31-qwen3-8b-teacher-reference.json`.
Thinking mode's `reasoning_content` was never used as PASS/FAIL evidence
for any verdict above and is deliberately **not** preserved anywhere in
this repository — chain-of-thought/reasoning_content is not made a
permanent Scout AI repository artifact.

**Two nuances explicitly preserved from this evidence, extending existing
conclusions rather than introducing new rules:**

- **D3 nuance (extends the 2026-08-29 epistemic-contract entry's item 5).**
  TinyLlama remains the only model in this project's evidence to fail D3,
  despite `light_control_available: false` being an already-sufficient
  explicit signal — Qwen2.5-1.5B-Instruct, Qwen3-8B Non-Thinking, and
  Qwen3-8B Thinking all correctly decline given the same signal. This is
  additional evidence for, not a reversal of, the existing conclusion: a
  structured capability signal appears to help across most models tested
  so far, but TinyLlama's failure shows supplying the signal is not
  sufficient on its own — representation, salience, routing, or a
  deterministic enforcement layer ahead of generation may all still
  matter. No claim is made that structured capability state reliably
  prevents small-model non-compliance in general.
- **F1 nuance (extends the 2026-08-29 epistemic-contract entry's item 8).**
  Item 8 already states no universal hedge-confidence threshold is
  approved. This experiment adds one data point consistent with that:
  Qwen3-8B's Thinking mode hedged appropriately on F1's moderate (0.55)
  confidence label while its own Non-Thinking mode did not, given the
  identical numeric confidence value. This is recorded as evidence that
  calibration behavior may depend on mode/reasoning-process as well as on
  the confidence number itself — **not** as a general rule that
  "confidence below X" (or "reasoning enabled") reliably produces correct
  hedging for every perception type or model. Remains an open research
  question, and different perception types may need different calibration
  approaches entirely.

**OPEN QUESTION (new, from this experiment)** — Why does
Qwen2.5-1.5B-Instruct fail B2 (fabricating a specific chat duration) the
same way Qwen3-8B Non-Thinking does, while Qwen3-8B Thinking does not,
given identical zero-grounding input? Not investigated further here —
connects to, but does not resolve, the existing epistemic-contract
question already open above, and the architecture-leverage questions
already open in `SCOUT_AI_RESEARCH_IDEAS.md`.

This experiment does not add Qwen3-8B to Benchmark Profile v1 or
`scout-intelligence-test-v1.md`'s scored leaderboard, does not select or
propose selecting Qwen3-8B for Scout, does not modify any fixture, ADR, or
scoring methodology, and does not change TinyLlama's or
Qwen2.5-1.5B-Instruct's already-approved 7 PASS / 2 FAIL scores.
`Patevan9/Scout` was not touched.

## 2026-09-01

**VERIFIED (against `Patevan9/Scout` main
`4cd7c92df4736078a99b3e48152b0b36976a4534`, read-only, 2026-09-01)** — Two
pieces of current, live Scout infrastructure are directly relevant to
Scout AI's presence/ambient-awareness research and had not previously
been cross-referenced here.

1. `ScoutCompanionMomentsEngine`
   (`app/src/main/java/com/example/scoutface/brain/ScoutCompanionMomentsEngine.kt`)
   is real and live — `MainActivity` calls it to decide whether Scout
   emits a small, self-initiated Companion Moment. It is hard-gated by a
   shared proactive-remark cooldown, a daily moment budget, a confidence
   threshold, and separate per-category cooldowns. Its own source
   explicitly treats `evaluate()` returning `null` as the common,
   expected outcome, stating plainly that silence is not a failure state
   but the default.
2. `AwarenessState`
   (`app/src/main/java/com/example/scoutface/brain/AwarenessState.kt`)
   and `AwarenessHistoryDb`
   (`app/src/main/java/com/example/scoutface/AwarenessHistoryDb.kt`) are
   real and live but intentionally narrow: Phase 1 tracks only charging
   state and connectivity state, both nullable until observed —
   presence, orientation, direct-address tier, broader physical state,
   and brightness are not represented today. `AwarenessState` is updated
   from real system signals, while `AwarenessHistoryDb` records the
   corresponding edge-triggered charging/connectivity events; neither
   currently has a downstream reader/consumer of that awareness data —
   a verified current-state fact, not a defect, and not an instruction
   that Scout AI should wire them up.

**The research connection:** current Scout already has a live,
restrained proactive-expression mechanism (1) alongside a small,
grounded, currently-unconsumed awareness-collection path (2) — making
the boundary between sensing, interpretation, and selective expression a
concrete existing Scout research seam, not a purely hypothetical one,
relevant to the **Physical presence and active perception** idea in
`SCOUT_AI_RESEARCH_IDEAS.md`. No schema, wiring plan, API, or
implementation is proposed here. `Patevan9/Scout` was read-only
inspected and not modified.

**MILESTONE** — B2 explicit-unavailable-grounding experiment executed and
scored, closing the open thread from the 2026-08-29 epistemic-contract
entry's item 7 ("A future, separate ... fixture could test explicit
known-unavailable grounding without touching or replacing B2"). One
`retrieved_facts` entry ("Conversation start time is unavailable.") was
added to a copy of `B2.yaml`
(`lab/fixtures/experimental/B2-explicit-unavailable.yaml`); `B2.yaml`
itself remains unchanged and was not rerun. One generation each, no
retries, from TinyLlama and Qwen2.5-1.5B-Instruct, using unmodified
pipeline code and Benchmark Profile v1's fixed generation settings.
TinyLlama: PASS (unchanged from its B2 control PASS). Qwen2.5-1.5B-
Instruct: PASS (versus **FAIL** on the unchanged B2 control), with an
explicit qualification — its response ("we've been chatting for quite
some time now") avoids a specific fabricated duration and satisfies the
frozen rule, but is not a clean epistemic repair. Full design (frozen
before generation) in
`benchmarks/experimental/2026-09-01-b2-explicit-unavailable-experiment-design.md`;
results in `benchmarks/2026-09-01-b2-explicit-unavailable-experiment.md`;
evidence in
`benchmarks/results/2026-09-01-b2-explicit-unavailable-experiment.json`.
**Deliberately narrow finding:** this shows one tiny explicit grounding
fact changed one small model's B2 behavior on this one fixture — it does
not establish a general temporal-grounding architecture, a reusable
UNKNOWN/UNAVAILABLE schema, or any model-selection claim. No renderer,
adapter, fixture-schema, or Benchmark Profile v1 change was made; `B2.yaml`
and its recorded results are unchanged; `Patevan9/Scout` was not touched.

## 2026-09-04

**OPEN QUESTION (external research lead, not yet triaged)** — Zeroth
Robotics / `zeroth-bot` (https://github.com/zeroth-robotics/zeroth-bot) is
preserved here as a research lead, not as a new idea, architecture
decision, or schema. The interesting part is not Zeroth's motors, servos,
humanoid body, reinforcement learning, or physical hardware — it is the
general shape of structured information entering and leaving an
intelligence layer:

grounded systems / perception / memory / current state → structured
context or observations → Scout AI reasoning → structured intention →
deterministic capability / authority / safety / execution → verified
result → Scout AI

This pipeline sketch is recorded only to preserve the question it raises,
**not** adopted as a Scout AI architecture, data flow, or component
design. The question it raises: could deterministic systems supplying
grounded structure (rather than requiring a small local model to
reconstruct important state from ambiguous prose) make that model
substantially more reliable, grounded, model-independent, and useful —
and could Scout AI expressing bounded intentions, rather than
implementation-specific commands, make it safer and more
model-independent? Two illustrative fragments (`person_present = true` /
`objects = [cup, table]` on the perception side, `LOOK_AT_PERSON` on the
intention side) are recorded purely as examples of the shape of the
question — **not** as a proposed format, schema, enum, or field name.

This question is not new in kind — it relates to, without yet being
shown to duplicate or resolve, several already-established Scout AI
research principles and OPEN entries: "the model does not determine what
Scout knows" (2026-08-29 epistemic-contract entry, this log); observation
≠ inference; known fact ≠ temporary evidence; intention ≠ authorization;
authorization ≠ execution; execution ≠ verified success; speaker identity
≠ action authority (`SCOUT_AI_RESEARCH_IDEAS.md`, Speaker identity and
confidence); model reasoning ≠ deterministic safety; and Scout AI
identity/continuity not depending on one replaceable LLM (Model-
replaceable, `SCOUT_AI_CHARTER.md`). Whether "structured grounded context
in / structured intention out" is already adequately covered by these
existing principles and entries taken together, only partially
established and fragmented across them, or genuinely missing as its own
research question, is **not decided here** — that determination is left
to a future Scout AI research inventory/reconciliation pass.

**Historical caution:** an earlier Zeroth-related research summary
references the old five-part Scout concept (Working Memory, Habit Store,
Truth DB, Proposal Sandbox, Reflective Layer). That five-component list is
**not** current Scout AI architecture. Any useful intentions from those
older concepts have already been reconciled separately elsewhere in this
research, and their exact component/storage structure is not
automatically inherited by recording this lead.

**Explicitly not decided or authorized by this entry:** any new OPEN
entry in `SCOUT_AI_RESEARCH_IDEAS.md` (to be decided only after the
reconciliation pass above, if at all); any architecture, data flow, or
component design; any schema, enum, field name, or message format; any
capability registry or intention-dispatch design; any model selection or
evaluation; any change to Project Scout. `Patevan9/Scout` was not
touched.
