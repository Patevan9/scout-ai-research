"""A minimal mock ModelAdapter -- Step 2 plumbing verification only.

Turns a RenderedContext into one predictable formatted string. This is
NOT TinyLlama's ChatML format -- the real `TinyLlamaChatMLAdapter` is a
separate adapter. This one exists only to prove the adapter boundary
works, reading only from the already-rendered RenderedContext, never a
raw canonical dict (Option B).
"""

from __future__ import annotations

from typing import Any

from .adapter import ModelAdapter
from .rendered_context import RenderedContext


class MockAdapter(ModelAdapter):
    model_id = "mock-adapter-v0"
    model_version = "0"
    quantization = "n/a"

    def format_prompt(self, rendered_context: RenderedContext) -> str:
        return f"MOCK_PROMPT[{rendered_context.current_user_input}]"

    def default_generation_settings(self) -> dict[str, Any]:
        return {"max_tokens": 16}
