"""RenderedContext -- the model-neutral output container for the
Canonical Context Renderer (Scout AI Lab Runner v0.1, Option B).

Data shape only. This step defines the container that a future
render_canonical_context() will populate, and that ModelAdapter will
eventually receive instead of the raw canonical fixture dict. It
contains no logic for facts, habits, vision, capabilities, connectivity,
conversation formatting, or prompt formatting -- each field is simply a
place to hold already-rendered text (or None, when a fixture doesn't
populate that concept).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RenderedContext:
    current_user_input: str
    conversation_block: str | None = None
    facts_block: str | None = None
    memory_habit_block: str | None = None
    vision_evidence_block: str | None = None
    capability_block: str | None = None
    state_block: str | None = None
