"""Approved InferenceBackend interface (Scout AI Lab Runner v0.1 design, section 2).

Responsibility -- and ONLY this responsibility:
    - loading a model
    - running inference against an already-formatted prompt
    - returning raw generation result information (text, timing, token
      counts)

A backend never formats a prompt and never knows a specific model
family's chat template -- that belongs entirely to ModelAdapter.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class RawGenerationResult:
    """Raw output of one backend.run() call.

    No scoring and no verdict of any kind lives here -- just what the
    backend actually produced and how long it took, matching the Lab
    Runner design's timing definitions (section 8).
    """

    text: str
    time_to_first_token_ms: float | None = None
    generation_time_ms: float | None = None
    prompt_tokens: int | None = None
    tokens_generated: int | None = None
    raw_backend_info: dict[str, Any] = field(default_factory=dict)


class InferenceBackend(ABC):
    """A backend loads a model and runs inference against an already
    formatted prompt string. It never formats a prompt itself."""

    @abstractmethod
    def load(self, model_path: str, **settings: Any) -> Any:
        """Load a model and return an opaque handle to it."""

    @abstractmethod
    def run(
        self,
        handle: Any,
        prompt: str,
        sampling_params: dict[str, Any],
    ) -> RawGenerationResult:
        """Run inference on an already-formatted prompt and return the raw result."""
