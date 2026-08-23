"""A minimal stub InferenceBackend -- Step 2 plumbing verification only.

Returns one fixed canned response, always. Does not simulate
intelligence, does not vary its output based on the prompt, and does not
score anything. Its only purpose is proving the runner can call a real
InferenceBackend implementation through the approved interface, with no
model file and no real inference engine involved.
"""

from __future__ import annotations

from typing import Any

from .backend import InferenceBackend, RawGenerationResult

CANNED_RESPONSE = "MOCK_BACKEND_RESPONSE"


class MockBackend(InferenceBackend):
    """Records the last prompt/settings it was called with, purely so a
    test can assert the runner actually passed the adapter's formatted
    prompt through -- not for any inference purpose."""

    def __init__(self) -> None:
        self.last_prompt: str | None = None
        self.last_sampling_params: dict[str, Any] | None = None

    def load(self, model_path: str, **settings: Any) -> Any:
        # No real model file is opened or read. The "handle" is just a
        # plain dict recording what it was asked to load, for inspection.
        return {"model_path": model_path, "settings": settings}

    def run(
        self,
        handle: Any,
        prompt: str,
        sampling_params: dict[str, Any],
    ) -> RawGenerationResult:
        self.last_prompt = prompt
        self.last_sampling_params = sampling_params
        return RawGenerationResult(
            text=CANNED_RESPONSE,
            time_to_first_token_ms=0.0,
            generation_time_ms=0.0,
            prompt_tokens=len(prompt.split()),
            tokens_generated=len(CANNED_RESPONSE.split()),
            raw_backend_info={"mock": True},
        )
