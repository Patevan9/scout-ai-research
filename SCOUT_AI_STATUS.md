# Scout AI — Current Status

**This is the handoff document.** Read this first in any new Claude or ChatGPT
session on Scout AI — it should be enough to recover where the project stands
without needing prior conversation history. Keep this concise; update it only
at meaningful milestones or before a long-conversation handoff, not after
every message (see Handoff Rule below).

Last updated: 2026-08-24

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

**Groundwork, with the first approved implementation underway.** No model
chosen, no fine-tuning, no TinyLlama run, no real inference. The approved
Scout AI Lab Runner v0.1 design is being built in small, individually
authorized steps (see `lab/`) — architecture plumbing and the canonical
fixture schema/validator proven so far, with a mock adapter, a mock
backend, and synthetic-only test fixtures, not a real model or real
benchmark data.

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
- **Least Sufficient Intelligence Principle** (Fast Path / Retrieval Path /
  Reasoning Path selection, and its selector safety rules) — approved. See
  [ADR-0004](docs/decisions/0004-least-sufficient-intelligence.md).
- **Benchmark runner methodology** (RAW / SYSTEM / BOTH per-case assignment,
  the canonical model-neutral RAW-context principle, and the three
  permanently-separate evaluation axes — Brain Quality, System Quality,
  Response Speed) — approved. See
  [ADR-0005](docs/decisions/0005-benchmark-runner-methodology.md).
- **Canonical Context Renderer / Option B model-adapter boundary**
  (the renderer as a single enforced choke point between canonical fixture
  data and any `ModelAdapter`) — approved. See
  [ADR-0006](docs/decisions/0006-canonical-context-renderer.md).
- **Scout AI Lab Runner v0.1 design** (standalone PC test harness, the
  ModelAdapter/InferenceBackend boundary, fixture and result schemas, the
  Benchmark Profile process) — reviewed by ChatGPT and approved. Being
  implemented in small, individually authorized steps; not yet complete.
- **Canonical Context Renderer / Option B interface migration** (the
  renderer, `RenderedContext`/`RenderedTurn`, and the `ModelAdapter`
  boundary change) — reviewed by ChatGPT and approved through Step 5,
  commit `3ad0598`, and formally recorded as
  [ADR-0006](docs/decisions/0006-canonical-context-renderer.md). See
  "Last completed step" below.

## Last completed step

The three approved pilot RAW fixtures — `B1.yaml`, `D2.yaml`, `F1.yaml` —
are now tracked and committed at commit `f3eb6d7` (data-only commit, on
top of Step 5). All three validate successfully against the current
fixture schema.

Before that, Step 5 of the Canonical Context Renderer / Option B
interface migration completed at commit `3ad0598`. The pipeline is now
enforced by construction:

    canonical context -> Canonical Context Renderer -> RenderedContext
      -> ModelAdapter -> InferenceBackend

`run_case()` now invokes the renderer before calling the adapter.
`ModelAdapter` — and both concrete adapters, `MockAdapter` and
`TinyLlamaChatMLAdapter` — receive only `RenderedContext`, never the raw
canonical fixture dict. Structured conversation turns (`RenderedTurn`,
introduced in the Step 4A correction) become TinyLlama's ChatML
`<|user|>`/`<|assistant|>` turns directly, with no fragile string
parsing. TinyLlama's verified ChatML format and Scout's system
instruction are unchanged in substance. This architecture is now formally
recorded in
[ADR-0006](docs/decisions/0006-canonical-context-renderer.md). Current
full test suite: **44/44 passing.** See `RESEARCH_LOG.md` for the
milestone entries covering the renderer Steps 1–4A, the Step 5 commit,
and the pilot fixture commit; full detail lives in each commit's own
message, not duplicated here.

**No real inference backend exists. No model has been run. TinyLlama
baseline testing has not begun. No replacement model has been
selected.**

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

## Real-device TinyLlama evidence (new)

Patrick-reported real-device observations — a TinyLlama identity/follow-up/
correction failure transcript (Galaxy A32), and TinyLlama performance
benchmarks on the Galaxy Fold 7 and Galaxy A32 — have been recorded in
`RESEARCH_LOG.md`. Not independently reproduced by Claude. Not yet
incorporated into Scout Intelligence Test v1 or any Lab Runner work —
preserved as evidence for later reviewed incorporation.

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

Step 5 (the Option B interface migration commit, `3ad0598`) and the pilot
fixture commit (`f3eb6d7`) have been independently reviewed and approved
by ChatGPT. This documentation/ADR update (Step 10) is pending that same
review cycle. Nothing else is currently pending review.

## Next safest step

**Not yet authorized.** The Canonical Context Renderer / Option B
migration (Steps 1 through 5, plus this documentation step) is complete
and reviewed. What comes next — the remaining RAW fixtures, TinyLlama
baseline testing, choosing any candidate replacement model, or approving
a Benchmark Profile — is undecided. Waiting for Patrick and ChatGPT to
define the next safe step together.

---

Project Scout / Scout AI Research
Copyright © 2026 Patrick Evan Lippy. All rights reserved.
