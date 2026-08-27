"""Approved ModelAdapter interface (Scout AI Lab Runner v0.1 design,
section 2; Option B boundary, Step 5).

Responsibility -- and ONLY this responsibility:
    - model-specific prompt/chat formatting
    - the model's own default generation settings and identity metadata

A ModelAdapter receives only an already-rendered RenderedContext --
NEVER the raw canonical fixture/context dict, not even as a nested
mini-dict. All meaning (what a fact, a piece of perception evidence, a
capability, or a connectivity state actually says) was already decided
by render_canonical_context() before the adapter ever sees it; the
adapter's only remaining job is choosing this model's syntax for
presenting that already-decided content.

A ModelAdapter must NEVER call an InferenceBackend and must NEVER
perform inference itself. It must not inspect raw fixture metadata, and
it must not silently omit any information the renderer produced. The
runner (see runner.py) owns calling both the renderer and the backend --
the adapter calls neither.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from .rendered_context import RenderedContext


class ModelAdapter(ABC):
    """Identity metadata (model_id, model_version, quantization) is
    expected as class or instance attributes on concrete adapters -- kept
    as plain attributes rather than abstract properties to keep this
    interface small."""

    model_id: str
    model_version: str
    quantization: str

    @abstractmethod
    def format_prompt(self, rendered_context: RenderedContext) -> str:
        """Turn an already-rendered, model-neutral RenderedContext into
        this model's formatted prompt string. Must not perform inference,
        must not call a backend, and must not interpret what any field
        means -- that interpretation already happened in the renderer."""

    @abstractmethod
    def default_generation_settings(self) -> dict[str, Any]:
        """This model's own documented default sampling settings.

        Used only as a fallback until a Benchmark Profile is approved
        (see the Lab Runner design, section 9) -- must never silently
        override an approved profile once one exists.
        """

    def stop_sequences(self) -> list[str]:
        """This model's own chat/prompt template stop sequence(s) --
        structural information about how this adapter's format_prompt()
        output ends a turn (e.g. TinyLlama ChatML's `</s>`), never a
        tunable benchmark sampling setting.

        Deliberately NOT part of default_generation_settings() -- a
        caller/Benchmark Profile may supply its own explicit sampling
        settings that bypass that method entirely (see run_case()), but
        stop-sequence knowledge must still reach the backend, since only
        the adapter knows its own template's termination syntax. An
        InferenceBackend must never invent this itself (see backend.py).

        Concrete, not abstract, with an empty-list default so an adapter
        with no meaningful stop sequence (e.g. MockAdapter) is never
        forced to invent one.
        """
        return []
