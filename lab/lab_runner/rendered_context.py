"""RenderedContext -- the model-neutral output container for the
Canonical Context Renderer (Scout AI Lab Runner v0.1, Option B).

Data shape only. This module defines the container that
render_canonical_context() populates, and that ModelAdapter receives
instead of the raw canonical fixture dict. It contains no logic for
facts, habits, vision, capabilities, connectivity, conversation
formatting, or prompt formatting.

Conversation turns are held as a typed list of RenderedTurn objects, not
a flattened string and not a raw dict -- RenderedContext is meant to be
a clean, typed, model-neutral boundary; ModelAdapters should never
receive raw canonical dictionaries, not even as nested mini-dicts. No
ChatML or other model-specific syntax belongs in RenderedTurn -- turning
turns into a model's actual chat/prompt syntax is each ModelAdapter's
job.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RenderedTurn:
    role: str
    text: str


@dataclass
class RenderedContext:
    current_user_input: str
    conversation_turns: list[RenderedTurn] | None = None
    facts_block: str | None = None
    memory_habit_block: str | None = None
    vision_evidence_block: str | None = None
    capability_block: str | None = None
    state_block: str | None = None
