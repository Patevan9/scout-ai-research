"""Smallest possible orchestration proving the approved architecture:

    canonical_context
      -> render_canonical_context(...) -> RenderedContext
      -> adapter.format_prompt(...) -> backend.run(...)
      -> result

The RUNNER owns this whole sequence -- it is the only place the
renderer, ModelAdapter, and InferenceBackend are ever wired together.
Neither the renderer, the adapter, nor the backend ever calls another of
them directly. Per the approved Option B boundary, the adapter receives
only the already-rendered RenderedContext -- it never sees the raw
canonical_context dict.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .adapter import ModelAdapter
from .backend import InferenceBackend, RawGenerationResult
from .renderer import render_canonical_context


@dataclass
class RunnerResult:
    canonical_context: dict[str, Any]
    formatted_prompt: str
    raw_result: RawGenerationResult

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def run_case(
    canonical_context: dict[str, Any],
    adapter: ModelAdapter,
    backend: InferenceBackend,
    handle: Any,
    sampling_params: dict[str, Any] | None = None,
) -> RunnerResult:
    """Run one canonical context through the renderer, then one adapter +
    backend pair.

    canonical_context here is the raw, already-validated fixture dict --
    it is kept on RunnerResult for later result-record traceability, but
    it is never passed to the adapter. Only the renderer ever reads it.

    Step 2 note, still true: this function does not write anything to
    lab/results/ and does not assign a brain_verdict -- it only proves
    the plumbing. Real result-record writing and scoring are separate,
    later, explicitly-authorized steps.
    """
    rendered_context = render_canonical_context(canonical_context)
    formatted_prompt = adapter.format_prompt(rendered_context)
    settings = (
        sampling_params
        if sampling_params is not None
        else adapter.default_generation_settings()
    )
    raw_result = backend.run(handle, formatted_prompt, settings)
    return RunnerResult(
        canonical_context=canonical_context,
        formatted_prompt=formatted_prompt,
        raw_result=raw_result,
    )
