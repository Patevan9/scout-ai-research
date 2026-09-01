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
