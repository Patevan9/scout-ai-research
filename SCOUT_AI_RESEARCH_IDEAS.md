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
