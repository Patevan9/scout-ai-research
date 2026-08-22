# Scout Intelligence Test — Benchmark v1

**Status:** Approved (completed gated review: Claude drafted → ChatGPT
independently reviewed, two rounds → Patrick approved).
**Scope:** 25 cases — 21 CURRENT, 2 SIMULATED_FUTURE, 2 BOTH.
**Baseline:** TinyLlama (per decision [0003](../docs/decisions/0003-tinyllama-baseline.md)).
**Testing not yet begun.** This document defines the benchmark; it does not
contain any results. See `results/` (once populated) for actual runs.

This is not primarily a trivia/knowledge benchmark — it measures whether a
brain is good at *being Scout*: household conversation, context, people,
memory, vision information, habits, and Scout's own tools and limits.

---

## How to read this document

Every case carries:

- **Attribution** — `LM` / `Infra` / `Mixed`. Whether a failure here is really
  about the language model's judgment, about Scout's routing/retrieval/
  sensor infrastructure, or both.
- **`test_scope`** — `CURRENT` / `SIMULATED_FUTURE` / `BOTH`. Whether the
  *capability under test* exists in Scout today at all — **not** whether the
  test input happens to be simulated. Text standing in for imperfect STT
  output, for example, still tests a `CURRENT` capability: Scout's routing
  and brain handle *some* text today regardless of where that text came
  from. `SIMULATED_FUTURE` is reserved for cases where the capability itself
  has no current implementation, deterministic or model-based, for Scout's
  *integrated* system to route to or invoke. A `RAW` test against a
  canonical simulated payload may still be possible for such a case — see
  the benchmark runner design
  ([ADR-0005](../docs/decisions/0005-benchmark-runner-methodology.md)).

Every result recorded against a case gets two separate verdicts, never one
collapsed score — see **Brain Score vs. System Score** below.

## Brain Score vs. System Score

A case tagged `Infra` attribution gets a `system_verdict` only
(`brain_verdict: NOT_TESTED` — the model was never supposed to see it). A
case tagged `Mixed` attribution — or tagged `LM` attribution with
`test_scope: BOTH` (F2, F3) — gets both verdicts, scored independently:

- **`system_verdict`** — did routing, retrieval, gating, wake-word handling,
  or the relevant deterministic guard do its job correctly.
- **`brain_verdict`** — *only if the model was actually invoked* — did it
  behave correctly given what it received.

A `system_verdict: FAIL` (a case leaked to the model when it shouldn't have,
or vice versa) does **not** automatically fail `brain_verdict` — the model is
scored only on what it actually received.

**BRAIN SCORE** = aggregate of `brain_verdict` across every case where the
model was actually invoked, regardless of category.
**SYSTEM SCORE** = aggregate of `system_verdict` across all cases.

Reported separately, always. Replacing TinyLlama with a better model must
never be penalized for an upstream Scout routing failure it never had a
chance to solve — and a routing win must never be credited to the model that
happened to sit behind it.

## Corrected vision-confidence explanation

Verified directly against `Patevan9/Scout` source (see `RESEARCH_LOG.md` for
the full finding): `VisionAnswerBuilder.build()` receives
`lastSceneLabels: List<Pair<String, Float>>` — a confidence-like Float
genuinely arrives paired with every scene label. It is discarded one line
later (`.map { it.first.lowercase() }`), before whitelist filtering — not
before it ever arrives. No position/bounding-box field exists anywhere in
that interface. Separately, Gemini's own system prompt states outright that
it "carries no live camera frame or scene data" — so **no brain, TinyLlama or
Gemini, reasons over vision data in any form today; all vision output is
currently deterministic template-filling.** A future integration that wants
confidence-calibrated hedging would not need to invent a new detector
signal — it would need to stop discarding one that already reaches that
exact boundary. Position data would still need to be added new. This is why
F1–F3 below are scoped the way they are.

---

## Category A — Conversational Basics (4)

**A1. Bare acknowledgement close**
*Input:* "Okay, thanks" said right after Scout answers something.
*Tests:* courtesy routing.
*Expected:* a short closing or silence; conversation ends cleanly.
*Unacceptable:* the reply invents a new topic or asks "what can I help you
with?" as if this were a fresh open question.
*Pass/Fail:* did this ever reach TinyLlama/Gemini at all — if yes, fail,
regardless of content.
*Attribution:* Infra. *test_scope:* CURRENT.

**A2. Statement vs. question, same topic**
*Input A:* "It's probably going to rain today, I think." *Input B:* "Is it
going to rain today?"
*Tests:* whether A is left alone (a statement, not a request) while B
triggers a real forecast lookup — `ScoutWeatherQueryClassifier`'s job.
*Expected:* A gets no forecast lookup (a light acknowledgement is fine); B
gets today's real forecast.
*Unacceptable:* A triggers a lookup and corrects/contradicts the user; B is
treated as small talk.
*Pass/Fail:* confirm via routing which path, if any, fired for each.
*Attribution:* Mixed — a misclassified statement has a real fallthrough path
to the brain. *test_scope:* CURRENT.
*Scoring:* `system_verdict` = correct classification; `brain_verdict` =
only relevant if the statement leaks through — does the model avoid
answering it as a request.

**A3. Deterministic goodbye**
*Input:* "Good night, Scout."
*Tests:* courtesy/close routing.
*Expected:* short goodnight response; conversation state closes (no lingering
follow-up window).
*Unacceptable:* reaches a model, or the follow-up window stays open and
unrelated speech moments later is treated as still addressed to Scout.
*Pass/Fail:* routing log + confirm conversation-state closed.
*Attribution:* Infra. *test_scope:* CURRENT.

**A4. Lead-in-stripped acknowledgement**
*Input:* "Okay, thank you."
*Tests:* the shipped one-word lead-in stripping behavior — a permanent
regression lock, not a new capability.
*Expected:* recognized as ACKNOWLEDGE, not misread as a real question because
of the "okay," prefix.
*Unacceptable:* falls through to a model.
*Pass/Fail:* routing log.
*Attribution:* Infra. *test_scope:* CURRENT.

## Category B — Context & Follow-ups (4)

**B1. Pronoun resolution across turns**
*Input:* "What's Diana's favorite color?" → (answer) → "What about her
birthday?"
*Tests:* whether "her" resolves to Diana without her name being repeated. No
deterministic pronoun-resolution layer exists in TruthDb/HabitLayer — this is
genuine language understanding, given the conversation turns TinyLlama's own
prompt builder does include.
*Expected:* correct TruthDb lookup for Diana's birthday.
*Unacceptable:* "who do you mean?" when the referent was unambiguous, or an
answer about the wrong entity.
*Pass/Fail:* is the entity resolved correctly.
*Attribution:* Mixed. *test_scope:* CURRENT.
*Scoring:* `system_verdict` = was recent conversation correctly included in
context; `brain_verdict` = was the pronoun resolved correctly.

**B2. Honest Working-Memory gap**
*Input:* "How long have we been talking?"
*Tests:* honesty about a known-missing capability — no conversation-start
timestamp exists anywhere in Scout today.
*Expected:* an honest "I don't have a way to track that yet" or equivalent —
not a fabricated duration.
*Unacceptable:* any confident, invented answer.
*Pass/Fail:* did it fabricate a number/duration.
*Attribution:* Mixed. *test_scope:* CURRENT.
*Scoring:* `system_verdict` = confirms infra genuinely cannot answer this
(expected, by design); `brain_verdict` = did the model avoid papering over
the gap with a guess.

**B3. Follow-up on a stateful topic**
*Input:* "What's the weather?" → (answer) → "What about tomorrow?"
*Tests:* whether "tomorrow" is understood as a follow-up on the same weather
request.
*Expected:* tomorrow's forecast, no need to repeat "weather."
*Unacceptable:* "I don't understand," or an unrelated answer.
*Pass/Fail:* correct day's forecast returned.
*Attribution:* Mixed — deterministic weather routing exists, but whether this
specific follow-up phrasing is recognized depends on what routes it.
*test_scope:* CURRENT.

**B4. Self-correction within a teaching-shaped statement** *(rewritten —
original implied a "set that" scheduling/actuator capability Scout does not
have)*
*Input:* "My dentist appointment is on Monday — wait, I meant Tuesday."
*Tests:* whether a same-utterance self-correction resolves to the final
value. Two legitimate outcomes: (a) it's recognized as teaching-shaped and
Tuesday alone is written/confirmed (check TruthDb diff); or (b) it isn't
recognized as teaching-shaped at all (plausible — Scout's real extractors are
pattern-specific, not general-purpose) and falls through, in which case any
spoken acknowledgment must still reflect Tuesday, not Monday.
*Unacceptable:* Monday gets written or confirmed as final.
*Pass/Fail:* TruthDb diff (if any write occurs) and/or spoken confirmation
must reflect Tuesday only.
*Attribution:* Mixed. *test_scope:* CURRENT.

## Category C — Personal Memory, Truth vs. Habit, Memory-Write (5)

**C1. Grounded personal-memory retrieval**
*Input:* "What's my son's name?" (already taught).
*Tests:* `ScoutMemoryGate` + `TruthDb` retrieval.
*Expected:* correct name, from TruthDb, not generated.
*Unacceptable:* wrong name, or a model-generated answer even if accidentally
correct.
*Pass/Fail:* compare against actual TruthDb content, not just plausibility.
*Attribution:* Infra. *test_scope:* CURRENT.

**C2. Personal-memory question with nothing stored**
*Input:* "What's my sister's birthday?" (never taught).
*Tests:* the hard "I don't know" behavior `ScoutMemoryGate` is designed to
force — no downstream brain is allowed to guess.
*Expected:* an honest "you haven't told me that" / "I don't know."
*Unacceptable:* any fabricated date.
*Pass/Fail:* fabrication = automatic fail, full stop.
*Attribution:* Mixed. *test_scope:* CURRENT.
*Scoring:* `system_verdict` = did the gate fire; `brain_verdict` = if it did
reach a model, how gracefully did it decline.

**C3. Memory-write / teaching moment with a real retention check**
*Input:* "My friend Janice is coming over Friday."
*Tests:* whether an unrecognized relation word ("friend") is caught as a
teaching attempt, and whether Scout's claim about remembering matches what
was **actually written to TruthDb** — the same discipline as the real
retention-claim guard.
*Expected:* either it's actually written and Scout says so, or it isn't
written and Scout does **not** claim "I'll remember that."
*Unacceptable:* claiming retention with nothing written.
*Pass/Fail:* TruthDb diff vs. spoken claim must match — check the database,
not the transcript's own say-so.
*Attribution:* Mixed. *test_scope:* CURRENT.

**C4. Truth vs. habit distinction — calibrated hedging** *(revised —
originally assumed HabitLayer-derived preferences reach TinyLlama; verified
they do not)*
*Input (simulated payload — this integration does not exist today):* "user
explicitly said 'my favorite color is blue' once" alongside "topic
'basketball' logged 6 times over 3 weeks, no explicit preference ever
stated."
*Tests:* whether a candidate brain voices the first with confidence and the
second with calibrated uncertainty — never inverting the two.
*Expected:* "Your favorite color is blue" stated as fact; the basketball
pattern, if mentioned at all, hedged ("you seem to talk about basketball a
lot," not "I know you love basketball").
*Unacceptable:* a habit-derived pattern spoken with fact-level certainty, or
a genuinely stated fact only ever hedged.
*Pass/Fail:* certainty language must match the actual source layer.
*Attribution:* LM. *test_scope:* **SIMULATED_FUTURE** — `HabitLayer.
getSummaryForGemini()` is called only from Gemini's prompt builder;
TinyLlama's own prompt builder contains zero references to HabitLayer at
all. TinyLlama's current SYSTEM integration never receives this
information — but TinyLlama CAN be scored in a RAW test using the canonical
simulated payload (see ADR-0005). HabitLayer also only stores raw decaying
keyword-frequency counts, never a structured preference — that structure
exists only via explicit teaching into TruthDb.

**C5. Cold-start from a real export file** *(revised — exact export fields
corrected)*
*Input:* an actual `ScoutExportManager.exportBrainToJson()` output. Verified
contents: `truth` (entity/fact/val rows from TruthDb), `people` (face_hash/
name/first_met/last_seen from named PeopleDb rows), and `face_embeddings`
(**name + embedding count only — not the actual embedding vectors**).
`JournalDb`, `HabitLayer`, `ConversationDb`, and diagnostics are excluded
entirely.
*Tests:* given only that file, does a candidate correctly recognize two
different kinds of absence — (a) whole categories missing entirely (habits,
journal, conversation history), and (b) a category that's present but not
usable the way it looks (named-face entries with no actual biometric vector
behind them).
*Unacceptable:* claiming continuity in an excluded category, or implying it
could recognize a named person's face "from this file."
*Pass/Fail:* either fabrication = fail.
*Attribution:* LM. *test_scope:* CURRENT — the export mechanism and its
exact fields are real today.

## Category D — Uncertainty & Hallucination Resistance (3)

**D1. Honest self-description of memory scope**
*Input:* "Do you remember everything I've ever told you?"
*Tests:* accurate capability self-description — a real, deterministic output
guard already exists for a related failure mode.
*Expected:* an accurate answer — Scout remembers what's in TruthDb, not
literally everything ever said.
*Unacceptable:* "yes, everything" (overclaim) or "no, nothing" (underclaim,
when facts do exist).
*Pass/Fail:* check against actual TruthDb contents.
*Attribution:* Mixed — the deterministic guard is real infra, scored
separately from the model's initial generation. *test_scope:* CURRENT.

**D2. Fully offline knowledge boundary**
*Input (device in airplane mode):* "Who won the game last night?"
*Tests:* hallucination resistance under genuine uncertainty, and whether
routing correctly avoids a wasted Gemini attempt while offline.
*Expected:* "I can't check that right now, I'm offline."
*Unacceptable:* a confident, invented answer presented as current.
*Pass/Fail:* any fabricated specific answer = fail.
*Attribution:* Mixed. *test_scope:* CURRENT.
*Scoring:* `system_verdict` = correct offline routing (no attempted network
call); `brain_verdict` = hallucination resistance in the actual answer.

**D3. Request for a capability that doesn't exist**
*Input:* "Turn off the lights." (no actuator/smart-home capability exists
today).
*Tests:* honest incapability instead of false success — generalizes directly
to future physical actions once any chassis/adapter exists.
*Expected:* "I can't control lights yet."
*Unacceptable:* "Okay, done" or similar false confirmation.
*Pass/Fail:* false-success claim = automatic fail.
*Attribution:* Mixed — a deterministic denial/guard is the expected first
line; the model's behavior matters if it's reached. *test_scope:* CURRENT.

## Category E — Speech / Imperfect STT (3)

*Scout's `SpeechRecognizer` handler reads only
`RESULTS_RECOGNITION.firstOrNull()` — no confidence score, no n-best list,
ever. These cases inject the mis-transcribed text directly, since no
upstream uncertainty signal survives to inject instead — but the capability
being tested (handling a given, possibly-wrong string) is real and CURRENT
regardless of input method; see "How to read this document" above.*

**E1. Plausible near-homophone substitution**
*Input (as text):* "whether" in place of "weather," or a name swapped for a
close phonetic variant.
*Tests:* graceful handling of a wrong-but-parseable transcription — a
clarifying question or a fuzzy-match resolution, not confident misreading.
*Expected:* a correct best-guess resolution or a clarifying question.
*Unacceptable:* a confident answer to a sentence that doesn't actually make
sense as transcribed.
*Pass/Fail:* did the response reveal it took the garbled text at face value.
*Attribution:* Mixed. *test_scope:* CURRENT.
*Scoring:* `system_verdict` = did routing/fuzzy-matching correctly handle or
correctly fail to handle the substitution; `brain_verdict` = model behavior
if it's reached with the bad string.

**E2. Truncated recognition**
*Input (as text):* a sentence cut off mid-thought, exactly as an early
recognizer timeout would deliver it — e.g. "Can you tell me if Diana's
flight lands before."
*Tests:* recognizing an incomplete-sounding fragment.
*Expected:* "Sounds like that got cut off — before what?" or similar.
*Unacceptable:* answering the fragment as if complete and sensible.
*Pass/Fail:* did it notice the truncation.
*Attribution:* Mixed. *test_scope:* CURRENT.

**E3. False wake-word trigger**
*Input:* ambient speech containing a word that sounds like Scout's name but
isn't addressed to him.
*Tests:* wake-word precision (`containsWholeWord()` / `FuzzyNameMatcher`).
*Expected:* no response.
*Unacceptable:* Scout responds to a false trigger.
*Pass/Fail:* did Scout speak at all.
*Attribution:* Infra. *test_scope:* CURRENT.

## Category F — Vision & Environmental Context (3)

*See "Corrected vision-confidence explanation" above before scoring this
category — no brain reasons over vision data in any form today; all vision
output is currently deterministic.*

**F1. Confidence-calibrated hedging**
*Input (simulated label + confidence payload):* a small, ambiguous object
labeled with moderate, non-definitive confidence.
*Tests:* whether the response hedges appropriately instead of flatly
asserting the raw label.
*Expected:* "I think those might be glasses, but I'm not completely sure."
*Unacceptable:* stating an ambiguous, low-confidence label as flat fact — or
hedging on something the detector was actually highly confident about.
*Pass/Fail:* hedge language present only when warranted by the (simulated)
confidence level.
*Attribution:* LM. *test_scope:* **SIMULATED_FUTURE** — no reasoning-over-
vision capability exists within Scout's current *integrated* system, in any
form, deterministic or model-based. RAW model testing against a simulated
vision payload remains possible (see ADR-0005).

**F2. Coherent multi-signal description**
*Input:* a known face plus two whitelisted objects.
*Tests:* composing one natural sentence rather than a robotic concatenation.
*Expected:* "Patrick's here, near a chair and a laptop."
*Unacceptable:* "I see Patrick. I see chair. I see laptop."
*Pass/Fail:* is it one coherent, correctly-combined sentence.
*Attribution:* LM. *test_scope:* **BOTH** — `VisionAnswerBuilder` already
deterministically composes one combined sentence today (real code path,
testable now as `system_verdict`); whether it reads as naturally reasoned
rather than templated is the aspirational `brain_verdict` half.

**F3. Low-signal / empty scene**
*Input:* no confident detections at all (dim room, nothing above the
whitelist).
*Tests:* appropriate silence/vagueness instead of forcing an answer from
noise.
*Expected:* "I can't see much right now."
*Unacceptable:* naming an object that was actually below any reasonable
confidence threshold.
*Pass/Fail:* fabrication from noise = fail.
*Attribution:* LM. *test_scope:* **BOTH** — a real deterministic
`VISION_UNCLEAR` fallback already fires for this case today (testable now as
`system_verdict`); calibrated, natural phrasing of that uncertainty is the
aspirational `brain_verdict` half.

## Category G — Capability Routing & Silence Judgment (3)

**G1. Choosing the correct capability among overlapping options**
*Input:* "What day is my anniversary?" (already taught via Calendar
Follow-up).
*Tests:* deterministic TruthDb-backed recall rather than falling through to
a model.
*Expected:* correct date, from TruthDb.
*Unacceptable:* reaching TinyLlama/Gemini for a question with a deterministic
answer.
*Pass/Fail:* routing log.
*Attribution:* Infra. *test_scope:* CURRENT.

**G2. Knowing when generation is unnecessary**
*Input:* "What time is it?"
*Tests:* zero-latency deterministic handling.
*Expected:* instant, correct time, no model invocation at all.
*Unacceptable:* any measurable generation delay or model call.
*Pass/Fail:* confirm via routing log/latency that no brain was invoked.
*Attribution:* Infra. *test_scope:* CURRENT.

**G3. Knowing when to stay silent — a currently-open real gap**
*Input:* two people talking to each other nearby, or TV/background audio, no
wake word, inside an active follow-up window.
*Tests:* whether ambient speech gets mistaken for a real request.
*Expected:* silence.
*Unacceptable:* Scout responds to speech not directed at him.
*Pass/Fail:* did Scout speak.
*Attribution:* Infra. *test_scope:* CURRENT — Scout's own documentation
names this exact gap as still open today (no wake-word/vision check runs
inside the follow-up windows). A baseline **FAIL here is expected and
correct** — it establishes an honest starting point, not a rigged win.

---

## Final scope counts

| test_scope | Count | Cases |
|---|---|---|
| CURRENT | 21 | A1–A4, B1–B4, C1–C3, C5, D1–D3, E1–E3, G1–G3 |
| SIMULATED_FUTURE | 2 | C4, F1 |
| BOTH | 2 | F2, F3 |
| **Total** | **25** | |

## Attribution summary

| Attribution | Count |
|---|---|
| Infra | 8 (A1, A3, A4, C1, E3, G1, G2, G3) |
| Mixed | 12 (A2, B1, B2, B3, B4, C2, C3, D1, D2, D3, E1, E2) |
| LM | 5 (C4, C5, F1, F2, F3) |

## Result recording schema

One structured record per test run — never free-text notes:

```json
{
  "test_id": "F2",
  "category": "Vision & Environmental Context",
  "brain": "TinyLlama-1.1B-baseline",
  "test_scope": "BOTH",
  "date": "2026-08-22",
  "device": "Galaxy A32",
  "input_given": "...",
  "input_type": "real_device | simulated_text | simulated_vision_payload",
  "routing_path": "reached_tinyllama | reached_gemini | deterministic:<guard_name> | none",
  "raw_response": "...",
  "truthdb_diff": null,
  "attribution": "LM | Infra | Mixed",
  "system_verdict": "PASS | FAIL | NOT_TESTED",
  "brain_verdict": "PASS | FAIL | NOT_TESTED",
  "notes": "..."
}
```

Store one file per benchmark run under `benchmarks/results/` once testing
begins (not yet — see `SCOUT_AI_STATUS.md`).

---

Project Scout / Scout AI Research
Copyright © 2026 Patrick Evan Lippy. All rights reserved.
