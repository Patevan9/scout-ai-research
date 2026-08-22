# Scout AI — Current Status

**This is the handoff document.** Read this first in any new Claude or ChatGPT
session on Scout AI — it should be enough to recover where the project stands
without needing prior conversation history. Keep this concise; update it only
at meaningful milestones or before a long-conversation handoff, not after
every message (see Handoff Rule below).

Last updated: 2026-08-22

---

## Repository boundary — always in force

- **`Patevan9/scout-ai-research`** (this repo) — where all Scout AI research,
  design, and documentation lives.
- **`Patevan9/Scout`** (the real app) — **reference-only.** Read to verify
  claims about real architecture and real problems. Never modify, branch,
  commit, or open a PR against it from Scout AI work. Current Scout app
  development always takes precedence and is never interrupted for this.

## Source-of-truth priority

When information conflicts, resolve in this order — highest first:

1. `SCOUT_AI_CHARTER.md`
2. Approved records in `docs/decisions/`
3. Approved benchmark definitions in `benchmarks/`
4. This file (`SCOUT_AI_STATUS.md`)
5. `RESEARCH_LOG.md`
6. Old conversation history

**Old conversations must never silently override a newer approved project
decision.** If something from a past conversation contradicts what's written
here, this file wins — flag the conflict rather than trusting the older
source.

## Review workflow — always in force

Research/discussion → Claude reports → ChatGPT independently reviews → Patrick
approves → **only then** does something enter the permanent record (the
Charter, a decision record, an approved benchmark definition, or this status
file). Claude's conclusions, ChatGPT's conclusions, and in-conversation ideas
are never auto-promoted. `RESEARCH_LOG.md` may capture findings and ideas
immediately, but nothing there is authoritative on its own — see that file's
own tagging system.

---

## Current project phase

**Groundwork.** No implementation, no model chosen, no fine-tuning, no code.
Current focus: defining the Scout Intelligence Test (a permanent benchmark of
real Scout interactions) as the first concrete deliverable, before any brain
work begins.

## Current approved work

- Separate repository established for this track (ADR-0001).
- Gated research → review → approval workflow adopted (ADR-0002).
- TinyLlama adopted as the required baseline for any future brain comparison
  (ADR-0003).

## Last completed step

Claude produced **Benchmark Draft v1** of the Scout Intelligence Test's first
25 cases, incorporating ChatGPT's first review round (vision-confidence
correction, Brain Score / System Score separation, `test_scope` tagging,
rewritten B4/C4/C5). **Not yet committed anywhere** — still awaiting ChatGPT's
second independent review before Patrick decides whether it's approved.

## Current benchmark status

- 25 cases defined, categorized A–G.
- Each case tagged: attribution (LM / Infra / Mixed), `test_scope` (CURRENT /
  SIMULATED_FUTURE / BOTH), and scored via separate `system_verdict` /
  `brain_verdict` fields.
- **Status: DRAFT, under second review — not approved, not final, not in
  `benchmarks/` yet.** `benchmarks/README.md` explains why the directory is
  currently empty.

## Important verified findings

(Full detail with sourcing lives in `RESEARCH_LOG.md`; headlines only here.)

- Scout has no Working Memory today — no conversation-start timestamp exists
  anywhere in the app; this is an acknowledged gap in Scout's own docs, not a
  bug.
- "Memory Import" does not exist as a working feature — as of Scout PR #65,
  both Settings rows are placeholders ("coming in a future release"). Only
  Memory Export is real, and it's narrower than it sounds (see next point).
- `ScoutExportManager`'s real export contains exactly: TruthDb `entity_memory`
  rows, named `PeopleDb` identity rows, and per-name face-embedding **counts**
  (not the actual embedding vectors). It excludes `JournalDb`, `HabitLayer`,
  and `ConversationDb` entirely.
- `HabitLayer` data reaches Gemini's prompt only — TinyLlama's own prompt
  builder never references it. HabitLayer itself stores raw decaying
  keyword-frequency counts, not structured preferences.
- Vision output is 100% deterministic today. A confidence `Float` does arrive
  at `VisionAnswerBuilder`, paired with each scene label, but is discarded
  before whitelist filtering; no position/bounding-box data exists anywhere in
  that interface; Gemini's own prompt explicitly states it receives no live
  camera/scene data at all. No brain — TinyLlama or Gemini — reasons over
  vision data in any form today.
- Scout's speech pipeline reads only the single top STT hypothesis
  (`RESULTS_RECOGNITION.firstOrNull()`) — no confidence score, no n-best list,
  ever used downstream.
- A Constitution-shaped pattern already exists in Scout, just scattered and
  unnamed: multiple deterministic guards (`ScoutIntentRouter`,
  `ScoutMemoryGate`, `ScoutVisionGate`, `TeachExtractor`, a retention-claim
  output guard) intercept decisions before or check outputs after a model's
  turn. Real evidence a Constitution enforced outside the model is achievable.

## Unresolved questions

- What specific stronger small open-weight model (if any) is worth evaluating
  against TinyLlama — deliberately not decided yet, per explicit instruction.
- What a real Working Memory design should look like for Scout.
- How a future brain would ever receive real-time vision confidence/position
  data — would require a Scout-side architecture change, which is out of
  scope for Scout AI to touch directly; needs eventual coordination, not a
  Scout AI-side workaround.
- Where `CLAUDE.md` (this repo's pre-existing session-notes file) ranks
  relative to this new structure — it predates the Charter/Status/Decisions
  system and hasn't been reconciled with it yet. Flagged, not resolved.

## Awaiting ChatGPT review

Benchmark Draft v1 (25 cases) — full content currently lives in conversation
history only, not yet committed to `benchmarks/`. Will be committed once
ChatGPT's second review and Patrick's approval are both in.

## Next safest step

1. ChatGPT independently reviews Benchmark Draft v1.
2. Patrick approves (or requests further revision).
3. Only then: commit the approved benchmark into `benchmarks/`, and record an
   ADR in `docs/decisions/` if the benchmark's methodology (Brain/System
   split, `test_scope` tagging) should be treated as an established decision
   rather than just an approved document.

---

Project Scout / Scout AI Research
Copyright © 2026 Patrick Evan Lippy. All rights reserved.
