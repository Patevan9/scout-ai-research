"""Approved ModelAdapter interface (Scout AI Lab Runner v0.1 design, section 2).

Responsibility -- and ONLY this responsibility:
    - model-specific prompt/chat formatting
    - the model's own default generation settings and identity metadata

A ModelAdapter must NEVER call an InferenceBackend and must NEVER perform
inference itself. Its only job is turning a canonical context dict into a
formatted prompt string. The runner (see runner.py) owns calling the
backend -- the adapter does not.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ModelAdapter(ABC):
    """Identity metadata (model_id, model_version, quantization) is
    expected as class or instance attributes on concrete adapters -- kept
    as plain attributes rather than abstract properties to keep this
    interface small."""

    model_id: str
    model_version: str
    quantization: str

    @abstractmethod
    def format_prompt(self, canonical_context: dict[str, Any]) -> str:
        """Turn a canonical context dict into this model's formatted
        prompt string. Must not perform inference and must not call a
        backend."""

    @abstractmethod
    def default_generation_settings(self) -> dict[str, Any]:
        """This model's own documented default sampling settings.

        Used only as a fallback until a Benchmark Profile is approved
        (see the Lab Runner design, section 9) -- must never silently
        override an approved profile once one exists.
        """
