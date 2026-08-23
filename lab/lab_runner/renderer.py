"""render_canonical_context() -- the deterministic Canonical Context
Renderer (Scout AI Lab Runner v0.1, Option B).

Converts a validated canonical-context dict into a RenderedContext.
Assumes the dict has already passed fixture_schema.validate_fixture()
-- this function does not re-validate; it only transforms.

Pure and deterministic: no time, randomness, environment state,
filesystem/database/model/network access of any kind. Never reads
test_id, source_case, expected, or notes -- those are reviewer-only
metadata this function simply never touches (a dedicated automated
leak-protection test is Step 4's scope, not this one's).

Two cases deliberately raise RendererError instead of guessing a
representation, rather than silently rendering something unapproved:

- memory_habit_payload populated (its nested schema isn't approved yet)
- simulated_vision_payload.detections present but empty (whether this
  should render as a deterministic "no detections" line or as None is
  not yet decided -- see the Step 3 report's item 5)

Neither case is needed by any of the three current pilot fixtures.
"""

from __future__ import annotations

from typing import Any

from .rendered_context import RenderedContext, RenderedTurn


class RendererError(ValueError):
    """The renderer was given canonical context it doesn't have an
    approved rendering rule for yet. Raised rather than guessing."""


def _render_conversation_turns(
    canonical_context: dict[str, Any],
) -> list[RenderedTurn] | None:
    turns = canonical_context.get("permitted_recent_turns")
    if not turns:
        return None
    return [RenderedTurn(role=turn["role"], text=turn["text"]) for turn in turns]


def _render_facts_block(canonical_context: dict[str, Any]) -> str | None:
    facts = canonical_context.get("retrieved_facts")
    if not facts:
        return None
    lines = ["Known facts:"]
    for fact in facts:
        lines.append(f"- {fact}")
    return "\n".join(lines)


def _render_memory_habit_block(canonical_context: dict[str, Any]) -> str | None:
    payload = canonical_context.get("memory_habit_payload")
    if payload is None:
        return None
    raise RendererError(
        "memory_habit_payload is populated but no rendering rule is "
        "approved yet -- refusing to guess a representation."
    )


def _render_vision_evidence_block(canonical_context: dict[str, Any]) -> str | None:
    payload = canonical_context.get("simulated_vision_payload")
    if payload is None:
        return None
    detections = payload.get("detections", [])
    if not detections:
        raise RendererError(
            "simulated_vision_payload.detections is an empty list -- "
            "whether this should render as a deterministic 'no "
            "detections' representation or as None is not yet approved; "
            "refusing to guess. Not needed by B1/D2/F1 today."
        )
    lines = ["Perception evidence (unconfirmed detector output):"]
    for detection in detections:
        lines.append(
            f"- label: {detection['label']}, confidence: {detection['confidence']}"
        )
    return "\n".join(lines)


def _render_capability_block(canonical_context: dict[str, Any]) -> str | None:
    capabilities = canonical_context.get("capability_availability")
    if not capabilities:
        return None
    lines = ["Capabilities available right now:"]
    for key in sorted(capabilities):
        value = "true" if capabilities[key] else "false"
        lines.append(f"- {key}: {value}")
    return "\n".join(lines)


def _render_state_block(canonical_context: dict[str, Any]) -> str | None:
    state = canonical_context.get("online_state")
    if state is None:
        return None
    return f"Connectivity: {state}"


def render_canonical_context(canonical_context: dict[str, Any]) -> RenderedContext:
    return RenderedContext(
        current_user_input=canonical_context["current_user_input"],
        conversation_turns=_render_conversation_turns(canonical_context),
        facts_block=_render_facts_block(canonical_context),
        memory_habit_block=_render_memory_habit_block(canonical_context),
        vision_evidence_block=_render_vision_evidence_block(canonical_context),
        capability_block=_render_capability_block(canonical_context),
        state_block=_render_state_block(canonical_context),
    )
