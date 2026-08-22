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
- The permanent handoff documentation structure itself (this file, the
  Charter, the decision records, `benchmarks/`, `RESEARCH_LOG.md`) —
  independently inspected by ChatGPT at commit `436180e` and approved.
- **Scout Intelligence Test v1** — 25 benchmark cases — completed two rounds
  of ChatGPT review and is approved. See `benchmarks/scout-intelligence-test-v1.md`.

## Last completed step

Benchmark v1 was recorded into `benchmarks/scout-intelligence-test-v1.md`
following its approval. **TinyLlama baseline testing has not begun yet.** No
replacement model has been selected. No benchmark harness has been
implemented.

## Current benchmark status

- **Scout Intelligence Test v1 is approved and recorded** — 25 cases,
  categories A–G, in `benchmarks/scout-intelligence-test-v1.md`.
- 21 CURRENT, 2 SIMULATED_FUTURE, 2 BOTH.
- Each case carries attribution (LM / Infra / Mixed) and is scored via
  separate `system_verdict` / `brain_verdict` fields (Brain Score vs. System
  Score kept separate, never collapsed).
- **No results exist yet.** `benchmarks/results/` has not been created.
  Running TinyLlama against this benchmark, choosing any candidate
  replacement model, and building a test harness are all still undecided —
  see "Next safest step."

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

This documentation/recording commit itself — ChatGPT will independently
inspect it before TinyLlama baseline testing or any implementation begins.
Nothing else is currently pending review.

## Next safest step

**Undecided.** Benchmark v1 being approved does not by itself decide what
happens next — that remains for Patrick and ChatGPT to review and agree on
together. Candidates that have been named but not chosen: beginning TinyLlama
baseline testing against v1, designing a minimal test harness, or continuing
research on an unresolved question above. None of these has been approved to
start.

---

Project Scout / Scout AI Research
Copyright © 2026 Patrick Evan Lippy. All rights reserved.
