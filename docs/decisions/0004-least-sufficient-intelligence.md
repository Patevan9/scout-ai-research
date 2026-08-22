# 0004 — Least Sufficient Intelligence Principle

**Status:** Approved
**Date:** 2026-08-22

## Decision

Every Scout interaction is handled by the lightest mechanism sufficient to
handle it correctly. Escalation to a more expensive intelligence path occurs
only when a cheaper path is insufficient.

Three conceptual lanes, in increasing order of cost:

### FAST PATH
- Bounded, deterministic output — no expensive generation required.
- Acknowledgements, courtesy, simple commands, known deterministic responses.
- Scout already has real, working infrastructure in this shape today
  (the courtesy layer, `CourtesyIntent` ACK/GOODBYE, lead-in stripping) —
  this principle generalizes something proven, not something new.

### RETRIEVAL PATH
- Structured, local lookup — facts, memory, calendar, known people,
  sensor/state data.
- Light phrasing assistance may eventually be allowed.
- The answer itself must not depend on expensive generative reasoning — only
  *how* it's phrased may get help, never *what* the answer is.

### REASONING PATH
- Ambiguity resolution, synthesis, multi-step reasoning, deeper
  interpretation, open-ended conversation.
- Latency is justified here — genuine reasoning is happening, not a cost to
  hide.

## Selector safety rule

> When the selector cannot establish that a cheaper path is sufficient, it
> escalates to the next capable path rather than guessing.

Escalation is general, not binary — it may go Fast → Retrieval, or
Fast/Retrieval → Reasoning, depending on what's actually missing. The one
rule that never bends: **never force ambiguous input into Fast Path merely
for speed.** Fast Path must be actively established as sufficient before
it's used — it is never the default under uncertainty, in either direction.

## Additional established points

- Numerical confidence + runner-up margin (inspired by Scout's real
  face-recognition threshold+margin discipline) is a **design option**, not
  a requirement. The actual selector mechanism remains undecided — it may
  end up as deterministic matching, explicit ambiguity rules, confidence/
  margin scoring, or something else not yet considered.
- Selector overhead itself must remain cheaper than the work it's trying to
  avoid — an expensive selector defeats the entire principle by adding
  latency to the case it exists to keep fast.
- Path ownership must prevent duplicated or conflicting answers. Scout has
  already had to fix exactly this class of bug once, for a simpler two-way
  (TinyLlama/Gemini) version of the same problem (PR #55's `pendingAiAnswer`
  lifecycle fix, PR #61's generation-ownership invalidation) — a three-path
  selector must not reintroduce it in a new shape.
- Selector decisions must eventually be auditable/loggable — which path was
  taken and why, not a black-box judgment call.

## Reason

Scout's own philosophy already states "Presence > Intelligence" and reacts
against ordinary interaction feeling slow or over-engineered. A future brain
that's smarter but makes acknowledgements and simple lookups noticeably
slower is not automatically a better Scout — latency needs to be a first-class
design constraint, not an afterthought discovered once a brain is already
chosen.

## Alternatives considered

- Always invoking the full local brain and letting it decide internally
  whether a shortcut applies — rejected. This makes the "fast" case pay the
  cost of loading/considering the heavy model even when it isn't needed, and
  puts a latency-critical decision inside the least auditable component.

## Consequences

- No implementation exists yet — this is a governing design principle, not a
  built selector.
- Any future selector design must be evaluated against this document before
  being adopted.
- The benchmark runner design (see
  [0005](0005-benchmark-runner-methodology.md)) records `path_taken` per
  test result specifically so this principle is checkable against real data
  once testing begins.
