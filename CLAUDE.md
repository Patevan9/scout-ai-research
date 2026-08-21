# Scout AI Research — Session Notes

Read this at the start of every session on this repo, same as Scout's own
`CLAUDE.md` is read fresh every Scout session. This file is the persistence
mechanism for the Future Scout direction — nothing discussed in a chat survives
into the next session unless it's written here.

## What this repo is

A parallel, groundwork-only research/design track for a future Scout-specific
local AI brain. Not a frontier/general-purpose AI project. The goal:

> Build a local intelligence that is substantially better at *being Scout* than
> TinyLlama is — not one that competes with ChatGPT or Claude.

This could eventually combine: a stronger small local base model, real Working
Memory, Scout's existing Truth/Habit systems, semantic understanding/routing,
vision and environmental context, controlled autonomy, learning from experience,
reflection and proposed improvements, a Scout Constitution governing what the
autonomous AI may do or change, and Scout-specific fine-tuning if it eventually
proves worthwhile.

## Relationship to Project Scout — hard boundary

The real app is [Patevan9/Scout](https://github.com/Patevan9/Scout). Current Scout
development is stability-first (launch, real-device testing, approved PRs) and
**must never be interrupted or refactored for this track.** Rules currently in
force, unless the owner explicitly changes them:

- No implementation here that touches the Scout app repo.
- No branch, no PR against Scout for Future Scout purposes.
- No refactoring current Scout code "in service of" Future Scout.
- No replacing TinyLlama in the shipping app.
- No changes to Scout's current development priorities.

**Flag, don't build.** If something in ongoing Scout development looks like it
would matter to a future Scout brain or to the Intelligence Test (see below),
the right move is to note it here or say so out loud — never to implement a
Future Scout solution inside a Scout session.

Scout's own `CLAUDE.md` and `Scout_Quick_Start.md` are the source of truth for
what's actually built. **Re-verify against them before trusting anything below
as current** — Scout moves fast (60+ merged PRs as of this writing) and this
file will drift, the same way Scout's own docs are explicitly warned to drift.

## Grounding: what's real in Scout today (as of main `021656a`, Aug 21 2026)

Corrections to the marketing site's aspirational framing (`lippyrobotics.github.io`
describes a five-layer memory architecture — Working Memory / Habit Store / Truth
DB / Proposal Sandbox / Reflective Layer — that is not a 1:1 match for the shipped
app):

- **TruthDb** (permanent facts) and **HabitLayer** (behavioral/person data,
  decays, gets cleaned) are real and load-bearing — under those names, not
  "Truth DB"/"Habit Store."
- **Working Memory does not exist yet.** Explicitly flagged as unbuilt in Scout's
  own docs: "How long have we been talking?" / "What were we talking about?" have
  no answer because no conversation-start timestamp exists anywhere in the app.
  This is the most concrete, already-acknowledged gap to design against.
- **"Proposal Sandbox" ≈ "Behavior Learning"** — CLAUDE.md already states the
  philosophy almost verbatim ("Scout never surprises the user... every meaningful
  change requires explicit user approval — Approve / Not Now / Never Suggest This
  Again") but it's explicitly **post-launch, not yet built**, and scoped to
  SharedPreferences-level behavior tuning, not model weight changes.
- **No Scout-internal Reflective Layer exists.** The "second AI reviews the
  first AI's work" pattern is real today but lives entirely in the human dev
  process (Claude implements, ChatGPT independently reviews the actual diff
  before merge) — nothing like it runs inside Scout's own runtime.
- **A Constitution-shaped pattern already exists, just unnamed and scattered.**
  `ScoutIntentRouter`, `ScoutMemoryGate`, `ScoutVisionGate`, `TeachExtractor`,
  and a retention-claim output guard (`applyRetentionClaimGuard`, PR #39) are
  all real, merged examples of deterministic code intercepting a decision before
  — or checking an output after — the model gets a turn. This is the strongest
  existing evidence that a Constitution enforced *outside* the model is
  achievable: the pattern is proven, it just needs to be generalized into one
  policy engine instead of re-invented per bug report.
- **Semantic/paraphrase routing was already considered and deliberately
  deferred** during the TinyLlama misroute investigation — not a new idea, a
  shelved one worth revisiting here.
- **Companion Moments** (`ScoutCompanionMomentsEngine`) is a real, live example
  of a bounded "Decisions layer" — Scout choosing to speak unprompted, gated by
  hard cooldowns, a persisted daily budget, and a confidence threshold, with
  silence as the explicit default outcome. Good template for how autonomy should
  be introduced: small, explicit, widened slowly after real-device observation.
- **Awareness Layer Phase 1** (`AwarenessState`/`AwarenessHistoryDb`) ships with
  *zero consumers by design* — signals collected, nothing acts on them yet.
  Template for "build the sensing substrate before granting autonomy on top of
  it."
- **Public Scout vs. Scout Dev build variants** is a working precedent for
  tiered autonomy/telemetry — the public release stays conservative and
  mechanism-hidden; Patrick's own dev build gets full telemetry, but even there
  "Scout Dev reports observations. Patrick and Claude decide the fixes" — pattern
  noticing stays separate from authority to act.
- A real historical failure worth remembering as a cautionary precedent: PR
  #32/#33 found `ENTITY_USER_PRIMARY` (registered owner) getting conflated with
  "whoever is currently speaking," leaking Patrick's name into `HabitLayer`
  entries for unverified faces — an ordinary bug, not malice or autonomy, that
  violated the Truth/Habit boundary and needed a traced fix plus a guarded
  one-time cleanup. Any future "evolve" pipeline needs at least this level of
  discipline, formalized.
- **TinyLlama 1.1B via llama.cpp, fully offline, is the current primary brain**
  (Gemini is opt-in/online enhancement). Runs on a Samsung Galaxy A32 (primary
  test device) and a Fold 7 (12GB RAM, secondary). Model delivery already goes
  through a real in-app download + unified startup gate — reusable
  infrastructure for shipping a future brain, too.

## First groundwork project: the Scout Intelligence Test

A permanent benchmark of real Scout interactions. TinyLlama is the baseline.
**Any future Scout brain must demonstrably outperform that baseline while
preserving stability, factual integrity, privacy, acceptable speed, and
acceptable device resource use** — not quality alone.

Coverage areas (eventual, not all at once):

- statements vs. questions
- acknowledgements and courtesy
- conversational context
- follow-ups
- pronoun/reference resolution
- personal-memory questions
- correct TruthDb use
- appropriate HabitLayer use
- memory-write requests
- uncertainty / knowing when Scout doesn't know
- hallucination resistance
- vision-context understanding
- environmental context
- choosing the appropriate Scout capability
- deciding when reasoning is unnecessary
- deciding when silence is appropriate
- natural household conversation
- multi-step reasoning
- future autonomous decisions

Real Scout failures and real-device observations (A32/Fold 7 findings, `DiagLog`
traces) should eventually become regression cases here — this benchmark is meant
to grow from Scout's actual bug history, not synthetic examples invented in the
abstract.

## Working direction — sequencing (not yet started, no approval to build any of this)

Roughly ordered, each stage meant to be individually valuable and de-risk the
next. Nothing below is authorized to start without explicit go-ahead, and it
should follow the same gated-phase discipline Scout's own `CLAUDE.md` uses
(Investigation → Design → Design revision → Implementation → Merge → Post-merge
verification, each phase waiting for explicit sign-off):

1. Name and unify the Constitution — generalize the existing deterministic-guard
   pattern into one policy engine.
2. Design real Working Memory (Scout's own acknowledged gap).
3. Build the Scout Intelligence Test / eval suite, seeded from real A32/Fold 7
   findings.
4. Evaluate upgrading the base local model (TinyLlama → a stronger small
   open-weight model) against that suite, using Scout's existing model-delivery
   infrastructure — no personalization yet, isolate "better small brain" from
   "self-evolving brain."
5. Build the semantic/paraphrase routing layer already scoped and deferred in
   Scout's own history.
6. Build "Behavior Learning" as Scout's `CLAUDE.md` already describes it —
   SharedPreferences-level suggestions, Approve/Not Now/Never Suggest This Again.
7. Only after 1–6: an off-device, eval-gated fine-tuning pipeline for real
   personalization, and only then any widening of the Decisions layer beyond
   what Companion Moments already does.

Treat capability and autonomy as independent dials — a better local model does
not by itself justify more autonomy. Autonomy expands only after the policy
engine, eval suite, and audit log have proven themselves at the current
capability level.

## Working rules

- Groundwork only until the owner explicitly authorizes moving past it.
- No repo other than this one is ever modified from this track.
- Every claim about "what Scout currently does" gets re-verified against the
  real `Patevan9/Scout` repo before being trusted — this file is a snapshot,
  not a live source.
- Full paste-ready files, clear screenshot-level explanations — same
  communication style Patrick's Scout sessions use (not a professional
  programmer; explain plainly).

---

Project Scout / Scout AI Research
Copyright © 2026 Patrick Evan Lippy. All rights reserved.
