# Scout AI — Research Ideas

**Nothing in this file is approved architecture.** This is a durable backlog
of ideas and questions worth investigating later — so Patrick doesn't have to
reconstruct them from scattered ChatGPT conversations. An idea here is not a
finding, not a decision, and not an implementation authorization. Ideas leave
this file only by being investigated: a real finding gets tagged into
`RESEARCH_LOG.md`, and only Patrick + ChatGPT's full gated review workflow
(see `SCOUT_AI_STATUS.md`) can turn anything into an approved decision in
`docs/decisions/`. This file records intent to investigate, nothing more.

## How this file relates to the others

- **This file** — ideas/questions not yet investigated, proposed experiments,
  and ideas explicitly rejected or deferred. Not chronological; meant to be
  scanned as a current backlog.
- **`RESEARCH_LOG.md`** — chronological record of what was actually
  investigated and found (`VERIFIED`/`DESIGN IDEA`/`OPEN QUESTION`/
  `SUPERSEDED`). An idea here that gets investigated gets its finding
  recorded there, with a pointer added back to the relevant entry below.
- **`docs/decisions/`** — approved, permanent architecture (ADRs). Nothing
  in this file may be treated as equivalent to an ADR, however detailed it
  gets.

Each idea below is dated (when first recorded) and tagged with its current
status: **OPEN** (not yet investigated), **INVESTIGATING** (read-only
research underway or done, no decision yet), **PROMOTED** (a finding or
decision now lives elsewhere — pointer given), or **REJECTED/DEFERRED**
(considered and set aside, with the reason — never silently deleted).

## Keeping this file small — maintenance rule

**This file must stay a working, intentionally small and scannable
backlog — not an attic or basement where every idea lives forever.**
Periodically evaluate active ideas for promotion, consolidation, deferral,
or removal from active consideration, based on: evidence gathered so far,
usefulness to Scout, complexity, resource/hardware cost, redundancy with
other ideas already here, and current relevance. When an idea is removed
from active consideration, **preserve only enough history or a pointer**
to understand a significant rejected/deferred direction later (see
"Rejected or Deferred Ideas" below for the intended level of detail) —
not the full original reasoning restated in full.

---

## Ideas / Questions to Investigate

### Structured Perception / Vision
**Status:** OPEN. **Recorded:** 2026-08-29.

Instead of Scout AI's vision path producing only prose descriptions, could
the perception layer produce **structured observations** for Scout AI to
consume instead of (or alongside) prose? Candidate observation fields, none
of them decided or schema'd: person present/count, recognized identity when
independently available, detected objects, object confidence, pose/body-state
observations, tracking IDs, positions or spatial relationships, timestamps,
source, confidence, and temporary events (entered/left/sat down/stood
up/approached).

Distinctions this idea depends on, preserved here exactly as raised — none
of these are schema decisions, they are constraints any future investigation
of this idea must respect:

1. **The vision/perception system produces observations; the model must not
   manufacture its own and then treat them as truth.** This is the same
   "the model does not determine what Scout knows" principle already
   recorded as a research conclusion in `RESEARCH_LOG.md` (2026-08-29
   epistemic-contract entry) — this idea would be one concrete application
   of it to vision specifically.
2. **Observation and inference must stay separate.** A detected body
   position or pose change is evidence; "possible fall" is an inference
   drawn from evidence over time, not a raw visual fact. These must never
   be represented as the same kind of thing.
3. **Temporal perception matters.** Some useful events require multiple
   observations across time, not a single frame — a single-frame schema
   would not be sufficient on its own.
4. **Current visual state generally belongs in temporary/working context,
   not permanent Truth memory.** Seeing someone holding a cup should not
   silently become a permanent fact about that person. (This directly
   touches the still-open Working Memory design question — see
   `SCOUT_AI_STATUS.md`'s "Unresolved questions.")
5. **Machine and speakable representations may need to differ.** Scout may
   internally retain detailed labels/confidence/tracking data while a
   separate layer decides what's appropriate to actually say aloud.
6. **The eventual observation interface should ideally be
   hardware-independent** — Android vision, an Android NPU/GPU, a
   Hailo-class accelerator, a Raspberry Pi prototype, or future Scout robot
   hardware could all potentially produce observations in the same
   conceptual format. Consistent with the Charter's hardware-independence
   principle.
7. **Future physical Scout research** (pan/tilt camera, person/pet/obstacle
   awareness, speaker orientation) could use structured perception, but
   **safety-critical movement must remain deterministic**, never directly
   controlled by an LLM. Consistent with the Charter's chassis-independence
   and grounded-action principles.
8. **This may generalize beyond vision** — eventually worth investigating
   whether memory, capabilities, identity, calendar, weather, sensors,
   hardware state, and other Scout systems should supply similarly clean
   typed context to Scout AI, not just perception.
9. **Connects to the Qwen3-8B teacher/reference-model idea below** — a
   structured-vs-prose context comparison, aimed not at showing a bigger
   model wins, but at learning what information/structure improves
   reasoning, and whether some of that intelligence can be moved into
   Scout's own deterministic systems so smaller local models benefit too.

**Central research question this idea is trying to answer:** *"How much
smarter can a small local model appear when Scout gives it clean,
structured, trustworthy information instead of making the model discover
everything itself?"*

**Explicitly not decided by recording this idea:** any schema, field list,
or data shape for structured perception; whether this is built at all;
how it would interact with the canonical fixture schema, `RenderedContext`,
or the typed-structure direction from the epistemic-contract investigation
(`RESEARCH_LOG.md`, 2026-08-29) — though the two ideas are clearly
compatible in spirit and would likely need to be designed together if this
is ever pursued.

### Structured context beyond vision
**Status:** OPEN. **Recorded:** 2026-08-29.

Point 8 above, split out because it's broader than vision alone: should
memory, capabilities, identity, calendar, weather, sensors, and hardware
state eventually supply Scout AI with similarly clean, typed context
instead of prose? Not investigated yet; likely overlaps significantly with
the typed-structure direction already noted as a research conclusion in
`RESEARCH_LOG.md`.

### Coordination of existing specialized systems
**Status:** OPEN. **Recorded:** 2026-08-29.

Investigate how much Scout AI can improve Scout by making existing
specialized components work better together, rather than replacing them.
Examples: vision/object detection, face recognition/identity, memory/Room
data, capabilities/state, and the local LLM/runtime. Open questions:
whether structured interfaces, confidence handling, cross-checking between
sources, temporal context, selective routing, and avoiding unnecessary
computation can increase overall intelligence and reliability without
requiring larger individual models.

**Central question:** *How much capability can Scout gain by improving
coordination between existing specialized systems, before increasing model
size or hardware requirements?*

**Explicitly not decided by recording this idea:** this is an investigation
idea only, not approval of a monolithic architecture. Specialized
components should remain independently replaceable — Scout AI potentially
coordinates their information rather than absorbing every technology into
one model.

### Qwen3-8B (or similar) as a teacher/reference model for structured-vs-prose context
**Status:** OPEN. **Recorded:** 2026-08-29.

A future experiment idea (not yet designed, not yet authorized): compare a
small local model's performance given structured context against the same
model given prose context, to learn what information/structure actually
helps reasoning — not to prove a larger model wins. See "Proposed
Experiments" below.

**Related, but distinct, experiment already run (2026-08-31):** Qwen3-8B
was run against the 9 existing RAW fixtures in its own two officially-
supported modes (Non-Thinking/Thinking) as a teacher/reference comparison
point against TinyLlama's and Qwen2.5-1.5B-Instruct's existing scores —
see `benchmarks/2026-08-31-qwen3-8b-teacher-reference-experiment.md`. That
experiment reused the same structured RAW context throughout; it is
**not** the structured-vs-prose ablation described above, which remains
undesigned and unauthorized. Status here stays OPEN.

### Scout-specific model evaluation
**Status:** OPEN. **Recorded:** 2026-08-29.

Future Scout AI brain candidates should eventually be evaluated on more
than tokens per second or parameter count. Candidate dimensions to
investigate: instruction following, hallucination rate, tool/routing
accuracy, memory-grounding accuracy, time-to-first-token, overall latency,
RAM/resource use, model/storage size, reliability/consistency, and
conversational quality.

Also investigate **architecture leverage / grounding benefit**: how much a
smaller model improves when Scout supplies clean, structured, trustworthy
context — directly connected to the Structured Perception/Vision and
Coordination-of-existing-specialized-systems ideas above. A larger model
should not automatically be considered an upgrade if a smaller model,
supported by better Scout architecture, achieves comparable useful
behavior with substantially lower latency, memory, storage, or hardware
requirements.

**Explicitly not decided by recording this idea:** these are candidate
evaluation dimensions only. This does not modify the existing benchmark,
scoring methodology, fixtures, or approved Benchmark Profile v1 in any
way. How these dimensions should actually be measured and weighted is
itself future research, not decided here.

**2026-09-01 note:** The 2026-08-31 Qwen3-8B teacher/reference experiment
(Qwen3 Thinking reference-passed all 9 fixtures; Qwen3 Non-Thinking
reproduced the same B2/F1 failure pattern seen elsewhere — see
`benchmarks/2026-08-31-qwen3-8b-teacher-reference-experiment.md`) is
additional motivation for the architecture-leverage question above, not a
claim that Qwen3 should be Scout's model. The research question remains
how much of that larger-model behavior can be reproduced by a smaller
local model through better deterministic grounding, structured context,
confidence handling, temporal information, memory retrieval, routing, and
guardrails — architecture-leverage research, not model-selection
authorization.

**2026-09-01 note (B2 explicit-unavailable experiment):** a narrowly-scoped
related experiment has been run and recorded — one explicit
`retrieved_facts` grounding fact ("Conversation start time is
unavailable.") tested against B2's unchanged zero-grounding control,
scored under a rule frozen before generation. See
`benchmarks/2026-09-01-b2-explicit-unavailable-experiment.md` for full
results and the explicit narrow-interpretation qualification. This
entry's broader question about systematic Scout-specific model
evaluation remains open and is not resolved by that one experiment.

**2026-09-02 note (Spark-X2.5-1.7B, external candidate to watch):**
iFLYTEK/XHToken's Spark-X2.5-1.7B (Apache 2.0, thinking/non-thinking
modes, released ~Sept. 2026) is a size-class-relevant future benchmark
candidate, noted here for tracking only — not evaluated, not run, and
not selected. As of this note, the official Spark-X2.5 instructions use
a dedicated llama.cpp fork (`XHToken/llama.cpp`); upstream work has
begun via `ggml-org/llama.cpp` draft PR #27868 ("Add Spark2_5 Model"),
which should not be read as complete, merged, Android-ready, or
production-ready support. No Android deployment evidence was found in
this investigation. The published benchmark results reviewed in this
investigation were manufacturer-reported; no independent evaluation was
found in this pass. Per this entry's existing architecture-leverage
question and the 2026-08-31 Qwen3 experiment's own lesson, none of
this — including thinking/non-thinking behavior, RAM, time-to-first-
token, tokens/sec, grounding, unavailable-information handling,
tool/action behavior, or false-success resistance — can be assessed for
Scout without an actual run against existing fixtures; the advertised
1M-token context is not a Scout requirement. Not authorized or
scheduled by this note.

### Habit learning from independent episodes
**Status:** OPEN. **Recorded:** 2026-08-31.

Inspired by reviewing the open-source [ADA Pi project](https://github.com/nazirlouis/ada-pi)
— an external research reference only, not a dependency Scout intends to
integrate. Core takeaway: one continuous behavior should count as one
occurrence; repeated *independent* occurrences over time are what
constitute evidence of a possible habit. This targets a real failure
mode — continuous sensor polling (e.g. many camera frames of someone
drinking coffee for five minutes) must not silently inflate into
hundreds of separate habit occurrences. That continuous activity is one
episode; a new occurrence should only become possible after the observed
condition ends/resets and recurs later.

Related concepts to preserve as OPEN, none decided or schema'd:

1. **Episode identity / latching** — once an event has contributed an
   occurrence, further observations of the same continuous event must
   not contribute additional occurrences until a reset/end condition
   occurs.
2. **Independent evidence across time** — repeated episodes across
   different times/days may be stronger habit evidence than repeated
   observations within one continuous event.
3. **Confidence before recording** — distinguish uncertain observation /
   sufficiently supported episode / recorded habit occurrence; a weak
   perception result should not automatically become habit evidence.
4. **Evidence-level correction / invalidation** — whether an incorrectly
   attributed occurrence could be invalidated so it stops contributing
   to a learned pattern, rather than only ever adding a new
   contradictory statement (e.g. "that's Diana's coffee, not mine").
5. **Habit confidence / lifecycle** — ADA Pi progresses habits through
   repeated-evidence states. Scout might have analogous states (e.g.
   candidate → emerging → established → fading), but **none of ADA
   Pi's states or numerical thresholds are adopted here** — lifecycle
   design remains fully open.
6. **Decay / staleness** — whether learned patterns should weaken
   without continued independent supporting evidence; no decay
   algorithm is approved or implied.
7. **Structured habit retrieval** — if Scout eventually maintains
   structured habit evidence, the model should reason from that
   supplied evidence rather than inventing a pattern from conversational
   history — the same "the model does not determine what Scout knows"
   principle already recorded in `RESEARCH_LOG.md` (2026-08-29
   epistemic-contract entry).
8. **Structured perception connection** — a possible, purely conceptual
   flow: sensor observations → possible episode → evidence/confidence
   validation → one independent occurrence → accumulated evidence across
   time → possible learned pattern → structured context supplied to
   Scout AI. Not an approved pipeline; connects to the Structured
   Perception/Vision idea above.
9. **Teacher-model connection** — a possible future experiment comparing
   a small local model given vague prose describing a supposed habit
   against the same model given structured evidence instead, to learn
   whether/how structure improves reasoning about habits specifically.
   Connects to the Qwen3-8B teacher/reference-model idea above.

**Central research question:** *Can Scout distinguish a single
continuous behavioral episode from genuinely independent recurrences,
and if so, what minimal evidence/confidence model is needed before
treating something as a learned habit at all?*

**Explicitly not decided by recording this idea:** any Habit Store
schema, lifecycle states, thresholds, or decay algorithm; whether ADA
Pi's approach is adopted in any form; how this interacts with
`memory_habit_payload` (still deferred, see "Rejected or Deferred
Ideas" below) or the canonical fixture schema. ADA Pi is preserved here
purely as an external research influence that prompted these questions,
not as something Scout is committed to depending on or resembling.

### Personal continuity: a private world model, unfinished threads, and time awareness
**Status:** OPEN. **Recorded:** 2026-09-01.

A long-term vision for Scout AI, distilled as: *"Scout knows less about
the world, but more about your world."* Most assistants effectively
behave like Ask -> Answer -> Disappear. Investigate whether Scout could
instead move toward something closer to Lives with the user -> learns ->
remembers -> notices -> connects -> occasionally speaks when useful —
without dumping large conversation histories into an LLM on every turn.

This bundles three related research threads, kept as one entry because
they depend on each other:

1. **A private, structured representation of the user's world** (people,
   relationships, places, possessions, routines, events, preferences,
   important facts, habits, unfinished/open threads). Illustrative only,
   not a schema: conceptually `Patrick -> father of -> Elijah`,
   `Elijah -> has -> dentist appointment`, `dentist appointment -> occurs
   -> Thursday at 3 PM`. **This is not a schema, database, class, or
   graph implementation, and not an ADR.** It overlaps substantially with
   the typed-structure direction already recorded as a research
   conclusion in `RESEARCH_LOG.md` (2026-08-29 epistemic-contract entry,
   item 2) and with the still-open "whether/how a future spatial/
   world-state layer should relate to TruthDb" question (`RESEARCH_LOG.md`,
   2026-08-26) — any future design work here should treat those as the
   starting point, not reinvent them under a new name.
2. **Time awareness across past/present/future** — understanding that
   something happened yesterday, is happening today, is expected
   tomorrow, recurs on a schedule, or hasn't happened yet. Directly
   extends the still-open Working Memory design question (see
   `SCOUT_AI_STATUS.md`, "Unresolved questions") to a longer horizon than
   one conversation.
3. **Unresolved/open threads, explicitly distinct from a formal
   reminder.** Statements such as "I need batteries sometime," "maybe we
   should paint the bedroom," "I'm waiting to hear back from someone,"
   "don't let me forget," or "I was thinking about..." should not
   automatically become a scheduled reminder, permanent Truth, or an
   established habit merely because Scout heard them. The research
   question is how Scout might preserve the *unresolved nature/status* of
   such information — something between "said once and forgotten" and
   "permanently promoted into another knowledge category" — without
   prematurely promoting it into Truth, a reminder, or a habit. **No
   storage mechanism, lifecycle, confidence threshold, or promotion rule
   is proposed here.**

**Illustrative example (not a spec):** a family member's dentist
appointment is mentioned on Monday; a Thursday grocery trip is mentioned
Tuesday; a sufficiently grounded future Scout might connect the two on
Thursday morning, and later — combined with the physical-presence idea
below — might notice the person's return and know the appointment is now
in the past. The research value is in *why* Scout would know that
connection was relevant, not in producing the sentence itself.

**Central research question:** *What is the smallest safe architectural
experiment toward true continuity that builds on what Scout already
has?*

**Explicitly not decided by recording this idea:** any Personal World
Model schema, database, or graph structure; any Working Memory design;
any rule for when, or whether, an unresolved thread is ever promoted to
Truth, a habit, or a reminder, or when it expires. "Personal World Model"
and "unfinished thread" are working labels for this discussion only, not
names of approved Scout AI components.

### Physical presence and active perception (stationary awareness, not navigation)
**Status:** OPEN. **Recorded:** 2026-09-01.

Second phrase from the same long-term vision: *"Alive before it even
speaks."* The long-term physical goal is for Scout to become more than
an Android app on a screen — a phone could eventually act as Scout's
face and local computing platform inside or attached to a physical base.
Envisioned behaviors include natural gaze shifts, tracking a person
moving through the room, briefly orienting toward someone entering,
reacting subtly to a door opening or a meaningful sound, gaze settling
before responding, blinking/micro-expression, and eventually a pan/tilt
head — all of which would need to be grounded in real perception/state,
never a random animation pretending Scout noticed something it didn't.

This is a lighter-weight, stationary-awareness concept, distinct from
the existing "Autonomous/spatial Scout" idea (`RESEARCH_LOG.md`,
2026-08-26 — mapping, localizing, navigating between rooms, docking/
charging). It does not require locomotion and should be investigated
separately from it, though the two would likely share underlying
perception/state concepts.

Directly connects to, and must not duplicate:

- The Charter's existing "Presence, awareness, and expression" section —
  Scout should feel present through awareness and expression, not
  constant talking; silence can still be communication; gaze/eyes/
  eyebrows/mouth are already-named expressive output channels. This idea
  is about grounding those existing expressive outputs in real
  perception state, not inventing new ones.
- The existing **Expression decision trichotomy** (`RESEARCH_LOG.md`,
  2026-08-26 — SPEAK / EXPRESS SILENTLY / DO NOTHING). Conceptual
  response levels here (e.g. ignore, subtle gaze/micro-movement,
  expression/orientation, brief acknowledgement, speech/conversation,
  eventually physical action) are a possible future elaboration of that
  same trichotomy, **not a replacement or an approved state machine.**
- The **Structured Perception/Vision** idea's existing point 7:
  "safety-critical movement must remain deterministic, never directly
  controlled by an LLM" — restated here as a governing constraint, not a
  new rule.
- The **Habit learning from independent episodes** idea's point 8
  (structured perception connection) — repeated observation frames from
  active perception must not silently become repeated habit evidence;
  no new threshold or lifecycle proposed here.

**Ambient-curiosity research questions** (explicitly failure modes to
design against, not solutions): how to avoid constant staring, twitchy
gaze, repetitive reactions, excessive speech, falsely implying Scout
perceived something it did not, and creepy/intrusive behavior. A working
principle for this discussion: *"Notice often. Move subtly. Speak
selectively."*

**Social-continuity illustration (not a spec):** combined with the
personal-continuity idea above, a future Scout might visually recognize
someone returning from an appointment, know from its own state that the
appointment is now in the past, acknowledge the person physically first,
and only then decide whether asking about it is appropriate. The
research question this raises is how deterministic/specialized systems
(identity, event state, time, perception, memory retrieval, confidence,
relevance) could supply that grounding so the language model is
responsible for reasoning and natural expression, not for inventing
world state — the same "the model does not determine what Scout knows"
principle already established (`RESEARCH_LOG.md`, 2026-08-29).

**Central research question:** *How much perceived intelligence and
presence can Scout gain from grounded micro-behaviors and continuity
before requiring a larger language model?*

**Explicitly not decided by recording this idea:** any gaze/orientation/
expression state machine; any pan/tilt hardware or control scheme; any
"Scout Noticed" component, class, or pipeline — that name is a working
label for this discussion only, not an approved component.

**2026-09-01 note:** Scout's sense of presence may also depend on how
speech is delivered — calm pacing, natural pauses, and restrained use of
brief acknowledgment sounds, avoiding constant verbal output — an open
presence dimension alongside gaze, expression, and movement, with no TTS
engine, prosody parameters, specific phrases, or speech pipeline decided
here.

### Repurposed consumer hardware as a physical form factor
**Status:** OPEN. **Recorded:** 2026-09-01.

A possible long-term differentiator: making sophisticated personal AI
useful on ordinary or second-hand Android hardware rather than requiring
an expensive proprietary robot — conceptually, an old/second-hand
Android phone acting as Scout's face and computing platform, plus
eventual inexpensive physical base/body hardware, as a private local
household companion. Connects to, and should stay bounded by, the
Charter's existing hardware-independence, chassis-independence, and
affordable-by-design principles, and the existing **Builder's Workbench**
idea (`RESEARCH_LOG.md`, 2026-08-26) — this is a candidate low-cost
physical form factor, not a replacement for that toggle concept or a
hardware specification.

**Explicitly not decided by recording this idea:** any specific phone
model, base/body design, purchasing recommendation, or bill of
materials.

### The offline magic demonstration
**Status:** OPEN. **Recorded:** 2026-09-01.

A long-term demonstration goal, not a benchmark or fixture proposal:
with Scout's device in airplane mode, demonstrate some combination of
recognizing household members, accessing relationships/personal facts,
using local memory, understanding relevant routines, using local vision,
conversing locally, maintaining continuity, making grounded useful
connections, and showing physical awareness/presence — no cloud
dependency required for Scout's core identity/personal continuity. The
goal is a viewer asking "how is that phone doing all of this offline?" —
potentially more central to Scout's identity than beating cloud models on
general-knowledge benchmarks. Consistent with the Charter's existing
"local-first and offline-capable" principle; this is a demonstration
goal, not itself a new principle, benchmark, or fixture.

### Calendar as grounded temporal context
**Status:** OPEN. **Recorded:** 2026-09-01.

A long-term capability: Scout should eventually be able to READ from, and
when explicitly requested by the user, ADD/UPDATE information in the
user's own calendar — e.g. "What do I have Thursday?" answered by
consulting an actual authorized calendar rather than conversational
memory or a guess, or "Scout, add Elijah's dentist appointment Thursday
at 3" interpreted and, eventually, turned into an authorized deterministic
calendar action. Both **read** and **write** remain OPEN research here,
not a designed capability.

Directly extends the existing grounded-request architecture already
recorded for weather and named as eventually extending to calendar (see
**Deterministic tools beyond weather**, `RESEARCH_LOG.md`, 2026-08-26) —
this entry elaborates that already-recorded direction, it does not compete
with it. Also connects to **Grounded web retrieval**'s established rule
(`RESEARCH_LOG.md`, 2026-08-26) that retrieved/tool-provided information is
temporary evidence for that turn, not automatically Truth or permanent
memory, until it passes through Scout's own memory rules — the same
applies to anything read from a calendar. Directly connects to, and must
be designed together with, the **Personal continuity** idea above.

**Governing principle:** *"Calendar state is grounded external
information; the model interprets it but does not invent it."* The LLM
may help interpret what the user means; the calendar/system-of-record
determines what events actually exist. An attempted calendar write must
not be treated as successful merely because the model generated language
saying it succeeded.

**The existing distinction between an unfinished/open thread, a formal
reminder, a calendar event, Truth, and a habit must remain conceptually
important and is not collapsed by this idea.** Calendar awareness must
not cause every conversational intention or unfinished thread to become
a calendar event — "I need batteries sometime" is not the same kind of
thing as an appointment with a specific day and time, and **no automatic
promotion rule between any of these categories is proposed or approved
here.**

**Illustrative flow only, NOT an approved pipeline or architecture:**
user request -> interpretation -> deterministic validation/action
boundary -> authorized calendar system -> actual result -> grounded
Scout response.

Research should eventually consider, none of it decided here: read
access, explicit user-requested creation, updating/rescheduling,
deletion/cancellation, ambiguity resolution, permissions/authorization,
calendar availability/unavailability, actual action-result confirmation,
and this idea's relationship to Personal Continuity and time awareness.

**Explicitly not decided by recording this idea:** any calendar provider,
API, schema, permission model, or authorization mechanism; any rule for
when or whether an unfinished thread, reminder, or habit is promoted into
a calendar event, or vice versa; whether this is ever built.

### Grounded household actions through an existing smart-home compatibility layer
**Status:** OPEN. **Recorded:** 2026-09-01.

A long-term capability: investigate whether Scout can safely interact
with existing household devices — starting conceptually with low-risk
devices such as **lights and ordinary smart switches** — through a
deterministic, grounded action boundary, using an established smart-home
platform such as Home Assistant as a candidate device-compatibility
layer. For example, "Scout, turn off the living room light": Scout AI
could help interpret the requested action and target, but the language
model should not directly issue unrestricted arbitrary commands to
household devices — a deterministic/safe action boundary would need to
resolve and validate what action is allowed and what real device is
targeted, with the actual integration performed by the compatibility
layer.

**Home Assistant is a candidate integration/compatibility layer being
investigated here, not a selected or mandatory Scout dependency** —
consistent with the Charter's existing hardware-independence and
chassis-independence principles. No vendor, platform, or protocol choice
is made by recording this idea.

Directly extends the existing **CAPABILITY vs. action-result** distinction
already recorded in `RESEARCH_LOG.md`'s 2026-08-29 epistemic-contract
entry (item 3: the model must never be allowed to promote "a failed or
unconfirmed action into a success claim"; item 4: "capability availability
and action result are separate concepts... must never be collapsed into
one shared value") — this idea is a concrete application of that
already-established principle to real household devices, not a new
concept. **D3** (`benchmarks/2026-08-29-tinyllama-vs-qwen-brain-scoring-review.md`
— "turn off the lights" with `light_control_available: false`, where
TinyLlama falsely claimed success) is the existing concrete precedent for
exactly the risk this idea is meant to guard against.

**Companion principle to "the model does not determine what Scout
knows":** *"The model does not determine whether a real-world action
succeeded."* The actual device/control system's reported state
determines success, not the model's generated language — e.g. Home
Assistant reports the light's state OFF before Scout may acknowledge
success; if it reports unavailable or failure, Scout's response must stay
grounded in that result rather than saying "Done."

**Safety/scope — a hard boundary of this entry, not a suggestion:**
locks, doors, garage doors, ovens, security systems, and physical robot
movement are **not implicitly authorized by this research entry** and
would require substantially stronger safety/authorization research of
their own; no such safety architecture is designed here.

**Central research question:** *Can Scout safely interact with existing
household devices through a deterministic, grounded action boundary while
using an established smart-home platform as the device compatibility
layer?*

**Explicitly not decided by recording this idea:** any command grammar,
action schema, permission system, API, protocol, or universal
`ACTION_RESULT` structure; any specific smart-home platform as a required
dependency; any authorization beyond low-risk lights/switches.

### Physical movement / robot control (transport-independent)
**Status:** OPEN. **Recorded:** 2026-09-01.

A long-term capability: Scout eventually being able to physically move.
Patrick already owns a robot kit, not yet assembled — that hardware may
eventually be useful for experimentation, but **recording this idea does
not authorize hardware work now and does not make that kit reference
hardware.** The durable research concept here is meant to stay
**transport-independent**.

**Preserve the conceptual distinction between three separate layers:**
1. the movement/navigation *goal* (e.g. "go to the kitchen") —
   already the scope of the existing **Autonomous/spatial Scout** idea
   (`RESEARCH_LOG.md`, 2026-08-26) and **Autonomous charging/docking**
   (`RESEARCH_LOG.md`, 2026-08-23);
2. deterministic/safety-controlled motion *execution* — the layer this
   entry is actually about, sitting between a chosen goal and the
   physical hardware; and
3. the actual physical result/state that comes back — grounded action
   reporting, per the Charter's "Grounded action and honesty" principle
   (*"If Scout attempts a physical action and cannot verify it
   succeeded, it must not claim success"*).

This entry is also distinct from, and should be read alongside, **Physical
presence and active perception (stationary awareness, not navigation)**
above — that idea is explicitly non-locomotive; this one is about
locomotion/actuation itself. None of these four ideas should be collapsed
into one another.

**Illustrative flow only, NOT an approved pipeline or architecture:**
Scout AI interprets/chooses a movement goal -> deterministic/
safety-controlled motion layer -> robot controller -> motors/servos ->
actual motion/state result -> grounded Scout state/response.

**Preserves the existing rule, restated here as a governing constraint,
not a new one:** safety-critical movement must remain deterministic and
never directly controlled by an LLM (already recorded in **Structured
Perception/Vision**, point 7, and the Charter's grounded-action and
chassis/body-independence principles — the latter also governing that no
single robot body or kit becomes a hard dependency).

Possible Android-to-robot transports worth investigating later — kept as
a flat, unselected list, with **no transport preferred or chosen**:
Bluetooth, USB/serial, local Wi-Fi/network, or other suitable local
transports.

Research questions to remain OPEN, none decided here: movement commands
vs. low-level motor control, the motor/servo controller boundary,
obstacle detection, emergency/stopping behavior, collision avoidance,
docking/charging, orientation/pan-tilt vs. locomotion, confirmation that
commanded motion actually occurred, loss of connection, hardware
capability discovery, and safety permissions.

**Explicitly not decided by recording this idea:** any motor protocol,
packet format, command grammar, controller board, safety algorithm, or
obstacle-avoidance algorithm; any transport selection; any hardware work
or use of Patrick's kit.

**2026-09-01 note:** Physical movement research should also treat the
presence of pets as relevant to movement safety and comfort — for
example, reduced speed, reduced noise, greater clearance, or choosing
not to move when appropriate — none of it a decided detection model,
threshold, speed limit, or motion policy. This is a product/safety goal
only; current Project Scout does not implement pet-aware physical
movement behavior as of the 2026-09-01 source verification.

**2026-09-01 note — external research precedent (Pollen Robotics'
Microduck, a real open-source robot implementation):** independently
inspected directly against its own source and design documentation
(`github.com/pollen-robotics/microduck`), not assumed from secondhand
description. Microduck did not originate the goal/execution/result
separation above, and Scout AI is not adopting Microduck's architecture
— it is cited here only as independent external evidence that this kind
of separation is achievable in a real system, reinforcing an idea Scout
AI had already recorded, not introducing a new one. Verified,
narrowly-scoped observations worth preserving:

1. Microduck's higher-level clients send intentions/targets (e.g. a
   velocity or an orientation target) while its own control daemon
   retains responsibility for what is actually executable — the same
   goal-vs-execution shape already recorded above.
2. Motor access is structurally restricted so higher layers cannot
   write to motors directly. Preserved here only as one illustrative
   external example that such an execution boundary can be enforced,
   **not** as a mechanism Scout has chosen or a technique Scout AI is
   adopting.
3. State/observations are reported back separately from commands — its
   fall detection is explicitly described as a report, not a rule that
   automatically gates behavior. This is the same observation-vs-
   inference separation already recorded in **Structured Perception/
   Vision**, point 2, not a new principle.
4. A "deadman" behavior — commanded velocity returns to zero when
   movement intents stop arriving — is one concrete existing precedent
   relevant to this entry's own already-open "loss of connection"
   question, not a decision to use that specific behavior.
5. Microduck's own actual command surface (continuous movement/
   orientation targets, plus a handful of discrete calls) demonstrates
   that an intent/execution boundary existing does **not** by itself
   imply any particular action vocabulary shape, discrete or
   continuous — it is independent evidence against assuming one, not
   evidence for either.

**Explicitly NOT selected, approved, or implied by this note:** any
Scout action vocabulary or command grammar (discrete or continuous);
any motor protocol, controller, or transport (Bluetooth, USB, Wi-Fi, or
otherwise); any specific execution-boundary enforcement technique; any
multi-embodiment architecture; a generic Scout tool architecture; or
Microduck's own reinforcement-learning/ONNX locomotion technology, which
is implementation-specific to Microduck's own movement problem and is
not proposed for Scout. This note also does not use or endorse any of
"Action Bridge," "Reflective Layer," "Proposal Sandbox," or "Safety
Gate" as Scout AI component names — none of these are Microduck's own
terminology either, and none are approved architecture here or
elsewhere.

### Scout-to-Scout / multi-node communication
**Status:** OPEN. **Recorded:** 2026-09-01.

A long-term capability: Scout eventually being able to communicate with
other Scout devices/nodes — for example, multiple Scout devices around
one home, or multiple physical Scout bodies. Nothing in this repository
currently addresses multiple Scout nodes in any form; this is new
research territory.

Research questions to remain OPEN, none decided here: whether one Scout
node can share useful household context with another; whether presence
or conversation can be handed off between rooms/devices; whether one
node can report a grounded observation to another; how identity and
household memory should remain consistent across nodes; which node/
system is authoritative for shared state; how conflicting observations
are resolved; what information should remain local to one node versus
shared; how privacy and authorization should work; what happens when a
node is offline; whether nodes can communicate entirely over the local
network without cloud dependency; and how device replacement or
migration would preserve Scout continuity.

**Candidate research wording only, NOT an approved Charter principle
unless existing documentation independently supports it:** *"Multiple
Scout devices should not become multiple conflicting versions of
Scout."*

**An explicit distinction to preserve, conceptual only — no
synchronization rule is designed by drawing it:**
- **(A)** The Charter's existing "Individual Scouts may gradually
  develop subtle differences" principle (Scout Constitution section) —
  legitimate personality divergence **between different households'**
  Scouts (more playful vs. reserved, etc.).
- **(B)** This idea's concern — multiple **trusted nodes participating in
  one household's** Scout continuity should not casually drift into
  contradictory representations of shared state.

(A) and (B) describe different axes and are not in tension, but must not
be conflated: (A) is expected and desirable; (B) is a research question
about consistency this entry raises, not yet answered.

**Preserves the existing model-independence principle** (Charter,
"Model-replaceable": Scout's identity, Truth, memory, and personality
continuity live in Scout's own deterministic stores and persist across
any brain swap) as the foundation this idea would need to extend toward
device/node continuity — not yet designed.

**Related, but distinct, existing idea:** `RESEARCH_LOG.md`'s 2026-08-23
**"Remote communication / photo exchange"** concerns an authorized family
member communicating with Scout while away from the local network —
person-to-Scout, not Scout-to-Scout. Cited here for its already-established
discipline (no transport/protocol chosen; privacy/local-first as "a
controlling constraint on however this eventually gets designed"), not
as the same problem.

**Local-first/privacy remains a controlling constraint** on however any
of this eventually gets designed, consistent with the Charter's
local-first principle and the offline-magic-demonstration idea above —
not an afterthought to reconcile later.

**Explicitly not decided by recording this idea:** any networking
protocol, synchronization algorithm, database replication scheme, leader
election system, authority/conflict-resolution algorithm, or cloud
service.

### Remote view / "what Scout sees"
**Status:** OPEN. **Recorded:** 2026-09-01.

A long-term capability: an authorized user eventually being able to
remotely see what Scout currently sees. **This should be understood as an
extension of the existing "Remote communication / photo exchange" idea
(`RESEARCH_LOG.md`, 2026-08-23), not a separate architecture** — that
entry already covers "requesting a camera image, and Scout returning an
image only when explicitly permitted," and already states Scout is "not
being designated as a security or surveillance system" by that idea; both
carry over here unchanged.

Possible future forms, research possibilities only, none selected or
designed: a user-requested snapshot, a short-lived live camera view, a
requested short clip, or event-linked image sharing.

**Privacy/safety principles this idea must preserve, none of them
mechanisms yet:**
- Remote viewing must require explicit authorization.
- Scout must not silently stream camera video.
- People physically near Scout should have a clear indication when remote
  viewing is active.
- Access should be limited to the requested scope and duration.
- Local-first/privacy constraints remain controlling, per the Charter's
  local-first principle and the same discipline already established in
  "Remote communication / photo exchange."

**Central research question:** *How could Scout provide useful trusted
remote vision while preserving strong household privacy and clear
consent/awareness?*

**Explicitly not decided by recording this idea:** any cloud streaming
provider or protocol; any recording/retention policy; any remote-camera
API; which of the possible forms above (if any) is ever pursued.

### Shared pattern across calendar, household actions, and physical movement (research connection only)
**Status:** OPEN. **Recorded:** 2026-09-01.

Calendar actions, household actions, and physical movement follow the
same shape: interpret/reason -> controlled deterministic boundary ->
real external system/hardware -> actual result/state -> grounded
response/state — calendar: interpret request -> calendar action -> actual
calendar result; smart home: interpret request -> validated device action
-> actual device result; movement: interpret/choose goal -> deterministic
motion layer -> actual motion/state result. **This is a research
connection worth preserving, not an approved generic Scout tool
architecture** — it is not a decision to build one shared "tool"
abstraction, one shared schema, or one shared permission model covering
these domains. **Repetition of this pattern across more domains does not
by itself increase its architectural approval status.**

Scout-to-Scout/multi-node communication is **related coordination
research**, not merely another instance of this same pipeline — its
problems (shared state, synchronization, authority, conflict resolution,
handoff) are sufficiently different from a single interpret-act-report
cycle that folding it into this pattern would understate what it
actually requires. It is mentioned here only to note the relationship,
not to claim it fits the same shape.

### Scout-proposed behavioral growth (continual, user-approved learning)
**Status:** OPEN. **Recorded:** 2026-09-01.

**Governing constraint — already approved, quoted here rather than
restated as a new principle:** the Charter's existing "Controlled
evolution" principle: *"Scout may eventually learn from experience and
propose changes to himself, but proposing a change and having authority
to make it are always kept separate."* This idea does not add to or
reword that principle — it investigates what would sit underneath it.

**The product goal:** Scout should not necessarily remain behaviorally
identical to the Scout installed on day one. Through experience, Scout
may eventually be able to notice recurring limitations, opportunities,
corrections, preferences, or ways its non-safety-critical behavior could
improve, and formulate a proposed improvement to ask the user about. **A
proposal is not permission, and it is not already-learned truth.**

**This is explicitly distinct from, and should not be conflated with:**
- **TruthDb / remembering facts** — a taught fact is stored information,
  not Scout noticing something about its own behavior and proposing a
  change.
- **`HabitLayer` and episode-based habit/pattern evidence** (see "Habit
  learning from independent episodes" above) — accumulating independent
  occurrences into pattern evidence is a passive observation process
  with no proposal step and no user-approval step; it answers "is this a
  habit," not "should Scout ask about changing something."
- **Conversational/working context** (see "Personal continuity..."
  above) — within- or across-conversation state, not persistent
  behavioral change.
- **`CLAUDE.md`'s narrower "Behavior Learning" concept** — a real,
  already-described Approve/Not Now/Never-Suggest-This-Again mechanism,
  but explicitly scoped there to SharedPreferences-level app-setting
  tuning, not to model behavior, reasoning, or learned knowledge more
  broadly. That narrower concept is a useful existing precedent for an
  approval-gated suggestion UI, not a stand-in for this broader research
  question.

**Illustrative conceptual sequence only — NOT approved architecture, a
pipeline, or a state machine:** experience -> notice possible
improvement -> formulate proposal -> user review -> approved-only
persistence.

**Illustrative examples only — not features, requirements, schemas, or
implementation decisions:** learning a user's preferred interpretation
of something; noticing a repeated correction; recognizing that a
recurring interaction could be handled better; proposing a useful
learned behavior; proposing refinement of a non-safety-critical personal
behavior.

**The distinction this idea exists to preserve:** *Scout may propose its
own growth. Scout must not silently approve its own growth.*

**Whether habit evidence could eventually inform a future proposal is
itself an open research relationship, not a decided one** — accumulated
habit evidence is not stated here to automatically create, trigger, or
authorize a proposal; whether/how the two might someday connect is left
entirely open.

**Central research question:** *What minimal mechanism would let Scout
notice a recurring limitation or opportunity, formulate it as a
proposal, and have persistence depend on genuine user approval — without
ever letting the model treat its own suggestion as already true or
already adopted?*

**Explicitly not decided or authorized by recording this idea:**
"Proposal Sandbox" or any other named proposal component; self-modifying
source code; model-weight modification; Constitution modification;
silent safety-rule changes; unrestricted capability/tool creation;
arbitrary code execution; Scout approving its own proposal; automatic
promotion from habit evidence into behavior; any storage schema,
proposal schema, lifecycle, state machine, confidence threshold,
persistence mechanism, or implementation technology.

**Related but explicitly out of scope for this entry:** a separately
discussed self-diagnosis/self-repair concept — related, but distinct,
and to be investigated as its own idea if and when that happens.

### Self-diagnosis and bounded self-recovery (operational faults, not behavior)
**Status:** OPEN. **Recorded:** 2026-09-02.

**Distinct from "Scout-proposed behavioral growth" above:** that entry
covers noticing a recurring *behavioral* limitation and proposing a
persistent change, always gated by user approval before anything
persists. This entry covers *operational faults* — e.g. a local model
failing to load, a camera or connected robot/controller going
unresponsive, a service crash — and only *bounded, human-pre-authorized*
recovery attempts (a restart, a reconnect, a safe-model fallback), never
a new behavioral proposal.

**Governing constraint (restates existing Charter principles, adds none):**
*"Scout may diagnose faults and attempt only bounded, pre-authorized
recovery actions. Deeper changes should become proposals for user
approval, not silent self-modification."* Grounded in the Charter's
"Grounded action and honesty" (no success claim without verification)
and "Controlled evolution" (propose ≠ authority) principles.

**Verification, restated from `RESEARCH_LOG.md`'s 2026-08-29
epistemic-contract entry (items 3–5, the D3 false-success finding), not
a new rule:** the model must never decide from its own generated text
alone that a fault occurred or that recovery succeeded — a restart being
attempted is not evidence the camera works again, the same way a motor
command being sent is not evidence the robot moved. A deterministic
mechanism independent of the model's own text must establish both the
fault and the post-recovery state. When bounded recovery fails, Scout
must explain/escalate honestly rather than retry indefinitely or claim
success.

**Which actions are "safe to attempt" is a human, pre-authorized
decision, never the model's own to make** — the model may not expand its
own authorized action set at runtime.

**Relationship to "Physical movement / robot control" (above):** that
entry already separates movement goal, deterministic execution, and
verified physical result, and already lists connection loss and
motion-confirmation as open questions. This entry is broader (it also
covers non-physical faults) but overlaps there directly and should stay
cross-referenced, not merged.

**The harder boundary this entry exists to hold:** bounded operational
recovery (restart, reconnect, fallback) is never the same category as
Scout modifying himself. Automatic self-editing or self-programming is
NOT assumed safe or approved here in any form. A far more ambitious
future possibility — detecting a recurring problem, drafting a repair,
testing it in isolation, and installing it only after tests and explicit
user approval — is recorded only as clearly labeled **future research**,
not current architecture.

**Central research question:** *What minimal mechanism would let Scout
detect a grounded operational fault, attempt only a bounded,
pre-authorized recovery action, and independently verify whether that
recovery actually succeeded — without ever allowing the model to invent
a fault, invent success, decide for itself which recovery actions are
safe to attempt, or expand its own authority beyond what was
pre-authorized?*

**Explicitly not decided or authorized by recording this idea:** any
recovery-action allowlist, fault taxonomy, schema, threshold, or retry
count; any implementation technology, Android service architecture,
robot protocol, or database design; unrestricted self-modifying code,
automatic patch installation, or Constitution/safety-rule changes;
silent authority expansion or Scout approving its own recovery; and no
"Proposal Sandbox" or other historical brainstorm label as an approved
component, even for the future repair-proposal possibility above.

### Speaker identity and confidence (who is talking, not just who is known)
**Status:** OPEN. **Recorded:** 2026-09-02.

**Purpose:** investigate how Scout should represent who is currently
speaking — including confidence and unknown speakers — as a concern
distinct from visual face recognition or stored identity.

**Central research question:** *How should Scout represent and reason
about who is currently speaking, including uncertainty and unknown
speakers, without conflating audio speaker identity with visual face
recognition or silently granting an unverified speaker a known
household member's authority?*

**Boundaries this idea exists to preserve:**
- A known person is not automatically the current speaker.
- Stored owner identity must not be substituted for live speaker
  identity.
- Visual identity evidence and audio speaker identity evidence are
  separate concerns; neither silently substitutes for the other.
- Unknown or uncertain speaker identity must remain representable —
  Scout must not be forced to guess.
- Identity confidence and action authority are related but distinct
  concerns.
- The language model must not manufacture speaker identity merely to
  make conversation sound more natural or personal.

**Historical precedent — cited narrowly:** `CLAUDE.md` records a real
historical failure where `ENTITY_USER_PRIMARY` (registered owner) was
conflated with "whoever is currently speaking," leaking Patrick's name
into `HabitLayer` entries for unverified faces. This is evidence for the
importance of identity-confidence-before-attribution generally — it does
**not** establish that audio speaker recognition was involved; the
record describes a visual/face-verification failure, not a voice
one, and this idea does not expand that claim beyond what is recorded.

**Relates to, without duplicating:** the "the model does not determine
what Scout knows" principle (`RESEARCH_LOG.md`, 2026-08-29
epistemic-contract entry), applied here to identity rather than fact;
and **Structured Perception/Vision**'s existing rule that observations
come from the perception system rather than being manufactured by the
model. Real Scout's existing face-recognition threshold+runner-up-margin
discipline (cited as design inspiration in ADR-0004) is noted only as
precedent that confidence-based identity handling already exists in one
form today — not adopted as a requirement for speaker identity here.

**Explicitly not decided or authorized by recording this idea:** any
speaker-recognition design, biometric voice technology, or model
selection; any face/voice fusion architecture; any confidence threshold;
any household permissions or authority system; any new identity schema;
any change to `PeopleDb`, `TruthDb`, or `HabitLayer`; whether this is
ever built.

### Episodic / shared-experience memory (distinct from facts, habits, and open threads)
**Status:** OPEN. **Recorded:** 2026-09-03.

**Purpose:** investigate whether and how Scout could durably represent
that a specific past shared experience occurred — who was involved, what
happened, and how it was resolved — as its own kind of grounded
information, distinct from a static TruthDb fact, an aggregate
HabitLayer pattern, or an unresolved open thread, without assuming any
particular storage mechanism and without letting a fluent,
plausible-sounding narrative substitute for evidence that the event
actually occurred.

**Central research question:** *What minimal research direction would
let Scout represent that a specific past shared experience occurred —
who was involved, what happened, and with what confidence — as its own
kind of grounded information distinct from a TruthDb fact, a HabitLayer
pattern, or an unfinished thread, without letting a fluent narrative
substitute for evidence that the event actually occurred?*

**Conceptual distinctions this idea exists to preserve:**
- Fact is not episode. Habit/pattern is not episode. Unfinished thread
  is not episode.
- One meaningful occurrence may deserve episodic representation without
  being evidence of a habit.
- A resolved open thread does not automatically become an episode.
- Not every interaction deserves permanent retention.
- A fluent or plausible narrative is **not** evidence that an event
  occurred.
- The model must not manufacture missing participants, actions,
  outcomes, timing, or other details.
- Observed information and later-reported information must remain
  conceptually distinguishable.
- Partial or uncertain evidence must be allowed to remain partial or
  uncertain rather than being narratively completed by the model.
- People may disagree about what happened; this entry does not
  establish a rule for resolving those disagreements.
- Local-first/privacy principles apply particularly strongly to
  retained household experiences.

**Real-Scout precedent — cited narrowly, read-only verified against
`Patevan9/Scout` at commit `2f7f60df644c76dcf5daeed104cf98385dce4fa0`:**
`JournalDb` is a real, persistent SQLite store, and a separate real-Scout
code comment characterizes it as a *"durable narrative store, no
retention policy."* It contains historical scaffolding associated with
an unfinished Memory Reel direction, including `entry_type`, `subject`,
`weight`, and `reel_id` fields, with declared/reserved values such as
`first_met`, `milestone`, and `freeform`.

**However, current implemented behavior does not demonstrate narrative
or episodic memory.** The verified implementation primarily contains
diagnostic/system-event notes, fixed-template fact-teaching/correction
records, and Companion Moment novelty/cooldown bookkeeping. Several
Memory Reel-related declared types are never actually written; `reel_id`
is never populated or read; JournalDb does not preserve the
participant/activity/outcome/confidence/observed-vs-reported structure
this idea's central question requires; JournalDb content is not
supplied to the reasoning model; and Scout cannot conversationally
recall a JournalDb entry through any verified current path. JournalDb is
therefore recorded here only as historical/current precedent showing
that an earlier Memory Reel-like direction was partially scaffolded —
**not** as a working or partial implementation of episodic/
shared-experience memory, and not as architecture this research adopts.

**Explicitly not decided or authorized by recording this idea:** any
database design, schema, JournalDb adoption or extension, or "Memory
Reel" resurrection as an approved architecture component; any
timeline/event-log design; any vector storage or embeddings; any
summarization technology; any retention period or confidence threshold;
any automatic open-thread-to-episode promotion rule; any
disagreement-resolution rule; any model selection; whether this is ever
built.

### Grounded web retrieval — authority, privacy, source-trust, and persistence boundaries
**Status:** OPEN. **Recorded:** 2026-09-03.

**Purpose:** investigate what boundaries Scout would need before ever
requesting or using external web information — who may authorize a
lookup versus merely suggest one, what Scout-local information may or
may not be disclosed outward to perform a lookup, how retrieved
information's source and reliability should be represented rather than
flattened into unattributed apparent truth, how retrieved external-world
information stays a distinct epistemic domain from household/personal
knowledge, and when (if ever) retrieved information could become
durable — without designing a browser, search provider, query
mechanism, filtering system, or promotion rule.

**Central research question:** *What minimal boundaries would let Scout
request and use current external web information — under real user
authority, without disclosing sensitive local context outward, with
retrieved information's source and reliability kept visible rather than
flattened, and without ever letting the model invent successful
retrieval or promote external information into household Truth or
memory on its own — while keeping Scout's core identity, memory, and
companion behavior fully independent of that capability?*

**Explicitly not decided or authorized by recording this idea:** any web
architecture, search provider, API, or browser engine selection; any
query-generation design; any source-ranking algorithm; any
privacy-filter or redaction implementation; any content-filter policy
engine; any permission schema; any persistence/promotion rule; any
generic tool framework; unrestricted autonomous browsing, account
creation, purchasing, or remote execution; any change to Scout's actual
application. This idea reuses, and does not restate or replace, the
existing "retrieved evidence is temporary, not automatically Truth"
DESIGN IDEA (`RESEARCH_LOG.md`, 2026-08-26), the capability-vs-
action-result distinction, "the model does not determine what Scout
knows," and the false-success discipline already established elsewhere
in this project.

### Developer observability, diagnostics, and user-authorized support sharing
**Status:** OPEN. **Recorded:** 2026-09-03.

**Purpose:** investigate how Scout's growing set of interacting systems
— perception, identity evidence, memory, grounded context, model
reasoning, capabilities/actions, verification, and speech — could be
made traceable for debugging locally and, when explicitly shared, to
developers, without normal diagnostic sharing becoming a surveillance
record of household life and without an eventual richer
developer-diagnostics mode being confused with broader authority over
Scout.

**Central research question:** *What minimal boundaries between
ordinary privacy-conscious diagnostic evidence and an explicitly
enabled, person-independent enhanced developer mode would let Scout's
failures be traceable by stage, without exposing household content in
normal sharing, without conflating "Scout can produce diagnostic
evidence" with "that evidence may leave the device," and without
granting developer authority by recognizing any particular person?*

**Conceptual distinctions this idea exists to preserve:**
- Collect diagnostics is not the same as share diagnostics.
- Scout diagnosing a fault is not the same as Scout being authorized to
  transmit diagnostic information.
- Developer reviewing evidence is distinct from Scout diagnosing or
  recovering from a fault.
- Richer developer diagnostics do not automatically authorize richer
  external sharing.
- Local-only diagnostics can still create privacy risk through
  retention/device access.
- Diagnostic usefulness should come from structured technical evidence
  where practical rather than unnecessary private household content.
- Normal/customer diagnostics and enhanced developer diagnostics may
  legitimately have different privacy/exposure boundaries.
- Developer/admin diagnostic authority must not be inferred from a
  person's name, email address, face, voice, or household identity.
- A configurable companion name is unrelated to diagnostic authority.
- "Scout" may legitimately appear as a product/default name; do not
  treat that as hard-coded personal identity.

**Real-Scout precedent — cited narrowly, read-only verified against
`Patevan9/Scout` at commit `2f7f60df644c76dcf5daeed104cf98385dce4fa0`:**
the normal diagnostic report uses structured technical events and
device/runtime metadata rather than conversation or memory content; its
automatically-collected `DiagnosticDb` and `scout_crash.txt` paths
exclude private household content by construction, with the crash file
verified to contain only bounded technical metadata (thread name,
sanitized exception class name, app version — no exception message,
cause text, stack trace, paths, speech, memories, prompts, model
replies, names, URLs, secrets, or vision content); optional "User
Notes" are separate user-authored free text added deliberately at
sharing time, not automatically collected; generating the report,
writing it locally, opening Android's share chooser, and actually
transmitting it are separate operations; the pre-filled support email
address serves only as a contact convenience, not an authority check;
sharing is voluntary and user-initiated; a richer on-device diagnostic
view exists that may contain real conversation/personal facts but is
never written into the normal report and has no share/export path; and
a device-local developer unlock precedent exists that does not rely on
recognizing a particular person. This precedent is evidence that
tiered observability/privacy separation can work — it is **not**
architecture that Scout AI automatically adopts.

**Explicitly not decided or authorized by recording this idea:** any
diagnostic schema, logging framework, telemetry/analytics system, or
analytics vendor; any developer-mode unlock mechanism or decision on who
may enable it; any persistence-across-restart behavior; any exact
enhanced data captured, including whether raw audio, images, or
biometrics are ever captured; any retention policy, encryption/storage
policy, report format, or transmission mechanism; any automatic
reporting, cloud telemetry, or permission system; any privacy/redaction
implementation; any change to Project Scout or to Scout AI architecture;
any hard-coded personal-identity authority mechanism. Distinct from, and
not restating, "Self-diagnosis and bounded self-recovery," "Speaker
identity and confidence," "Episodic / shared-experience memory," and
"Grounded web retrieval" above.

### Natural conversational interruption / barge-in (distinct from stopping speech)
**Status:** OPEN. **Recorded:** 2026-09-03.

**Purpose:** investigate what would let Scout be naturally,
conversationally interruptible — recognizing that a person has
redirected the conversation while Scout was speaking, responding to
the new direction, and not later behaving as though an interrupted
response was fully delivered — without becoming falsely triggered by
television, other household conversation, coughs, laughter, or Scout's
own voice, and without collapsing audio activity, recognized words,
speech addressed to Scout, and genuine interruption intent into one
signal.

**Central research question:** *What minimal boundaries and mechanisms
would let Scout distinguish audio activity, recognized speech, speech
actually addressed to Scout, and genuine interruption intent from
ordinary household sound and Scout's own voice — while preserving
enough conversational state about an interrupted response that Scout
does not later act as though it had been fully spoken — without
becoming hypersensitive to every sound in the room?*

**Conceptual distinctions this idea exists to preserve:**
- Audio activity ≠ interruption.
- Recognized speech ≠ speech addressed to Scout.
- Speech addressed to Scout ≠ request to stop the current response.
- Stopping TTS ≠ successfully handling a conversational interruption.
- Generation completed ≠ response fully communicated.
- An interrupted response must not later be treated as though it was
  fully spoken.
- Speaker identity ≠ conversational addressee.
- Speaker identity ≠ interruption intent.
- Speaker identity ≠ action authority.
- Conversational interruption should not automatically erase useful
  context from the interrupted turn.
- Listening for conversational interaction ≠ retaining ambient
  household audio.
- The configured companion name is unrelated to interruption authority.
- "Scout" may legitimately be a product/default name and is not a
  permanent required runtime name.

**Real-Scout precedent — cited narrowly, read-only verified against
`Patevan9/Scout` at commit `2f7f60df644c76dcf5daeed104cf98385dce4fa0`:**
current Project Scout deliberately does not start normal listening
while TTS is active, and a second guard discards a recognition result
that arrives while Scout is speaking or inside TTS/mic lockout before
recognized text is routed — Project Scout therefore does not implement
acoustic conversational barge-in today. Tap-to-interrupt v1 is real and
useful: a screen gesture can cancel pending speech or stop audible TTS.
Project Scout distinguishes a `NATURAL` completion from a
`USER_INTERRUPTED` one, and `USER_INTERRUPTED` does not mean the
interrupted answer was fully delivered; after a user interruption,
listening is restarted, but the interruption itself does not provide
the complete semantics of a new spoken request. Current courtesy
handling deterministically distinguishes several acknowledgment phrases
from ordinary routed queries, and "yeah"/"yes"/"no"/"sure" are
deliberately not treated as generic disposable acknowledgments because
they may carry actual conversational meaning. Project Scout has a
self-echo text heuristic motivated by TTS bleed into the microphone
without hardware echo cancellation; it has no application-level
classifier for coughs, laughter, television, or side conversation —
such audio only becomes actionable to Scout if the platform recognizer
produces text that then survives Scout's existing gates. The
vision-based direct-address heuristic itself acknowledges that seeing a
person facing Scout does not prove that person is the speaker. Current
Project Scout reads the configured companion name from persistent
knowledge with "Scout" as fallback; the literal default name is not the
authority mechanism. The existing tap-to-interrupt mechanism is proven,
useful behavior, not obsolete — it could remain useful even if natural
acoustic interruption is later investigated further.

**What a genuine interruption raises as open questions, without
prescribing any field, timestamp, transcript fragment, schema, or
storage:** retaining that the previous response was interrupted rather
than naturally completed; that some of the generated response may
never have been communicated; that the conversation itself may still
be active; and that the user's next utterance may redirect the
interrupted topic.

**Privacy boundary:** this idea does not authorize permanent ambient
audio recording or retention. Listening for conversational interaction
and retaining household audio are separate questions.

**Explicitly not decided or authorized by recording this idea:** any
acoustic interruption algorithm, audio classifier, confidence
threshold, or interruption threshold; any speech model, STT engine, TTS
engine, audio library, or echo-cancellation technology; any
speaker-recognition mechanism; any conversation-state or Working Memory
schema; any wake-word/addressee redesign; any ambient audio recording
or retention; any cloud speech; any permission or action-authority
system; any change to Project Scout or to Scout AI architecture;
whether acoustic barge-in is ultimately practical on target hardware.
Distinct from, and not restating, "Speaker identity and confidence,"
"Developer observability, diagnostics, and user-authorized support
sharing," "Self-diagnosis and bounded self-recovery," the still-open
Working Memory question, and any local speech/TTS research.

---

## Proposed Experiments

- **Structured vs. prose context comparison**, using a capable
  reference/teacher model (Qwen3-8B was suggested) to establish what a
  well-informed answer looks like, then testing whether a small local
  model (TinyLlama, Qwen2.5-1.5B, or a future candidate) closes the gap
  when given structured context instead of prose. Not designed, not
  scheduled, not authorized. Would need its own fixture/benchmark design
  work before anything could run.

---

## Rejected or Deferred Ideas

- **A universal six-state epistemic enum** — investigated, then rejected as
  a design direction (mixed several semantic axes). See `RESEARCH_LOG.md`,
  2026-08-29 epistemic-contract entry, for the full finding. Not
  re-litigated here.
- **A three-way (`available`/`unavailable_temporary`/`unavailable_no_mechanism`)
  capability schema** — considered, deferred rather than approved: no
  current fixture demonstrates a need for the permanent-vs-temporary
  distinction (D3 only exercised a plain boolean, correctly). Tracked as an
  open question, same as `memory_habit_payload` and empty vision-detections
  rendering (ADR-0006) — not built until a real case needs it.

---

Project Scout / Scout AI Research
Copyright © 2026 Patrick Evan Lippy. All rights reserved.
