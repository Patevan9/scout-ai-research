# Temporary Grounded Statements — Design Note (frozen, research concept only)

**Status:** Frozen research design concept. **NOT** an approved
component, schema, database, or production feature. **NOT**
implementation-authorized by this note. "Temporary Grounded Statements"
is a working label for this discussion only, not the name of an
approved Patevan AI component.

**Date frozen:** 2026-09-08.

**Builds on, and does not restate:** the "Personal continuity" OPEN
entry's unresolved/open-thread question and its 2026-09-08 sharpened
refinement (no grounded, timestamped holding mechanism exists today for
an ordinary spoken statement); "Grounded household awareness"'s general
grounding principle that two independently grounded facts do not
establish a third fact connecting them; `PeopleDb`'s unresolved-identity
precedent (`touchSeen()`/`setName()`); the "Speaker identity and
confidence" entry's "unknown or uncertain speaker identity must remain
representable" principle.

## Research question

What is the smallest way to hold a grounded record of *what someone
said*, across turns/time, without ever letting that record become, or
imply, a claim that the described future action occurred?

## Motivating example

Patrick says: *"I'm leaving soon to pick up Elijah."*

Later, Elijah is confidently observed.

**Allowed:** "Patrick previously reported an intention to pick up
Elijah." + "Elijah is now observed." (two independently retained
facts.)

**Not allowed:** "Patrick picked up Elijah." "Patrick brought Elijah
home." "The reported intention was completed." Later observing Elijah
must never complete, confirm, or causally connect the earlier statement
unless a separately designed, separately authorized deterministic
source explicitly establishes that — no such source exists today, and
none is proposed here.

## The shape — four required fields, no more

| Field | Meaning |
|---|---|
| `who` | The reporter. May be unresolved/null. |
| `statement` | Normalized grounded proposition — what was reported, not independently verified world truth. |
| `reported_at` | One timestamp: when the report occurred. |
| `source` | Provenance (today, effectively always `user_speech`). |

Records are **immutable once written**.

## Explicitly excluded from this design

No `resolution_status`. No stored expiration field. No linkage field of
any kind. No supersession inference. No causal inference. No retroactive
speaker reassignment. No LLM adjudication of whether a report became
true. No topic-linking, semantic matching, or conflict resolution. No
event graph, episode engine, or general temporal-reasoning design.

## Three concerns, kept separate

1. **Historical truth that a report occurred** — permanent. "Patrick
   reported X at T" does not become false later.
2. **Active-context staleness/surfacing** — a **retrieval-time-only**
   computation (`now - reported_at` compared against some threshold, not
   fixed here) that gates whether a record is offered as *current*
   context. Never written back onto the record.
3. **Retention/deletion policy** — **undecided.** Records persist for as
   long as they are retained; how long that is (indefinite, a
   time+count-capped rolling store like `AwarenessHistoryDb`, an
   unbounded store like `JournalDb`, or something else) is a separate,
   future, not-yet-authorized decision.

## Corrected retraction example

T1: "I'm leaving soon to pick up Elijah." → one record
(`who=patrick, statement="Patrick reported an intention to leave soon
to pick up Elijah", reported_at=T1, source=user_speech`).

T2: "Never mind, I'm not going to pick up Elijah after all." → a
**second, independent** record (`who=patrick, statement="Patrick
reported that he is no longer planning to pick up Elijah",
reported_at=T2, source=user_speech`), never a mutation of the T1
record.

Both records are retained, unmodified, side by side, for as long as
they are retained. The T1 record is not false, deleted, or marked
contradicted — Patrick really did report that intention at T1.
Retrieval may use `reported_at` only for staleness/surfacing, never to
infer that T2 supersedes T1 as the same topic or plan — that these two
records concern the same intention is not established merely by
matching `who` and differing timestamps, and no mechanism here decides
it.

## Unresolved-speaker rule

An unresolved reporter (`who = <unresolved marker>`) remains unresolved
in that historical record permanently. `who` is never mutated later
based on inference, even if the same speaker is subsequently identified
with confidence elsewhere. Unlike `PeopleDb`'s `face_hash`-keyed
reconciliation, this four-field shape has no equivalent stable identity
key to safely anchor a later reassignment — any future speaker-to-past-
utterance reconciliation would require a separately designed grounded
linkage mechanism, not added here.

## Explicitly not decided or authorized by this note

Any schema, database, or production table; any runtime wiring into
`Patevan9/Scout` or Android; any `TruthDb` change; any model experiment,
fixture, or benchmark run; any event graph, episode engine, or
conflict-resolution mechanism; any supersession or speaker-
reconciliation logic; any retention/deletion policy; whether this is
ever built.

---

Patevan / Patevan AI Research
Copyright © 2026 Patrick Evan Lippy. All rights reserved.
