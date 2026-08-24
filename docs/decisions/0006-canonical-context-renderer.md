# 0006 — Canonical Context Renderer / Option B model-adapter boundary

**Status:** Approved
**Date:** 2026-08-24

## Decision

A single, pure, deterministic function —
`render_canonical_context(canonical_context: dict) -> RenderedContext` —
sits between a RAW test case's canonical fixture data and any
`ModelAdapter`. No `ModelAdapter` implementation ever receives the raw
canonical fixture dict; it receives only the `RenderedContext` the
renderer produces. This is "Option B," chosen explicitly over letting
each adapter read the raw fixture dict itself (Option A).

### Why the renderer exists

ADR-0005 already required that every candidate brain receive
"semantically equivalent, model-neutral information containing only what
the specific test case permits it to know." Without an enforced boundary,
nothing stops an individual `ModelAdapter` from reaching past that
boundary — reading a reviewer-only field (`test_id`, `source_case`,
`expected.*`, `notes`), silently dropping a field it doesn't know how to
render, or improvising its own interpretation of raw data (e.g. turning a
numeric detector confidence into a hedge word itself). The renderer makes
the model-visible surface a single, testable, model-neutral choke point
instead of a convention every future adapter has to remember to honor.

### RenderedContext — the model-neutral boundary

`RenderedContext` (see `lab/lab_runner/rendered_context.py`) is a plain
dataclass carrying only what a model is permitted to see:
`current_user_input`, `conversation_turns`, `facts_block`,
`memory_habit_block`, `vision_evidence_block`, `capability_block`,
`state_block`. It has no field for `test_id`, `source_case`, `expected`,
or `notes` — those fields are structurally unavailable to any adapter, not
merely withheld by convention.

### Structured RenderedTurn conversation handling

Conversation history is carried as `conversation_turns:
list[RenderedTurn] | None`, each `RenderedTurn` holding a plain `role`
and `text`. This was a correction (Step 4A) after an initial flattened
`conversation_block: str` design proved unable to be safely reconstructed
into a specific model's own multi-turn chat format (e.g. TinyLlama's
separate `<|user|>`/`<|assistant|>` ChatML turns) without fragile string
parsing. Carrying turns as structured data lets an adapter emit its own
native per-turn syntax directly, with no parsing step.

### Responsibility boundaries

- **The renderer** owns turning canonical fixture data into a
  deterministic, model-neutral representation — and only that. It never
  knows about any specific model's prompt syntax.
- **A `ModelAdapter`** owns a specific model family's prompt/chat
  template syntax only. It receives `RenderedContext` and formats it into
  that model's expected prompt string. It never reads raw fixture data and
  never calls an inference backend.
- **An `InferenceBackend`** owns loading a model and running inference
  against an already-formatted prompt string. It never formats a prompt
  and never knows a chat template.

This three-way separation is what keeps Scout AI model-replaceable: a new
candidate model needs a new `ModelAdapter` and possibly a new
`InferenceBackend`, never a change to how canonical context is
represented.

### Reviewer-only metadata must never reach the brain

`test_id`, `source_case`, `expected.*`, and `notes` exist only for human/
automated grading of a run's outcome. The renderer never reads them into
`RenderedContext`, and dedicated tests assert no reviewer-only string can
reach any adapter's formatted prompt output.

### Deliberately deferred, not decided by this record

- **`memory_habit_payload`'s nested schema** — the renderer currently
  raises `RendererError` if this field is populated, rather than guessing
  a shape for it. No case has required it yet.
- **Empty `simulated_vision_payload.detections` rendering** — the
  renderer currently raises `RendererError` for an empty detections list,
  rather than guessing whether that should render as text or as `None`.

Both remain open until a specific test case actually requires resolving
them, at which point that resolution goes through the normal
research → report → review → approval workflow — not silently decided
inside implementation.

## Reason

Fair, comparable brain-vs-brain testing (ADR-0005) requires that the
model-visible surface be enforced, not merely documented. Option B makes
that enforcement structural: nothing needs to be remembered or reviewed
line-by-line in every future adapter for the boundary to hold, because
the boundary is the only thing an adapter can see.

## Alternatives considered

- **Option A** — each `ModelAdapter` reads the raw canonical fixture dict
  directly, following documented conventions about what it may use.
  Rejected: this depends on every adapter correctly, consistently
  self-restricting to permitted fields, which is exactly the kind of
  convention-only boundary this record exists to avoid.

## Consequences

- `run_case()` (`lab/lab_runner/runner.py`) always calls
  `render_canonical_context()` before calling `adapter.format_prompt()`;
  the raw canonical dict never reaches an adapter.
- Any future `ModelAdapter` implementation is written against
  `RenderedContext` only, never against the raw fixture schema.
- Model replaceability (a Charter-level goal) is directly served: adding
  a new candidate model touches only its own adapter (and, if needed, a
  new backend), never the renderer or the canonical fixture format.
- `memory_habit_payload` and empty-vision-detections rendering remain
  open questions, tracked here and in `RESEARCH_LOG.md`/
  `SCOUT_AI_STATUS.md`, not resolved by this record.
