"""A minimal mock ModelAdapter -- Step 2 plumbing verification only.

Turns a small canonical-context dict into one predictable formatted
string. This is NOT TinyLlama's ChatML format -- a real
`tinyllama_chatml` adapter is a separate, later, explicitly-authorized
step. This adapter exists only to prove the adapter boundary works.
"""

from __future__ import annotations

from typing import Any

from .adapter import ModelAdapter


class MockAdapter(ModelAdapter):
    model_id = "mock-adapter-v0"
    model_version = "0"
    quantization = "n/a"

    def format_prompt(self, canonical_context: dict[str, Any]) -> str:
        user_input = canonical_context.get("current_user_input", "")
        return f"MOCK_PROMPT[{user_input}]"

    def default_generation_settings(self) -> dict[str, Any]:
        return {"max_tokens": 16}
