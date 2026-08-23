"""Smallest possible orchestration proving the approved architecture:

    canonical_context -> adapter.format_prompt(...) -> backend.run(...) -> result

The RUNNER owns this sequence. Neither ModelAdapter nor InferenceBackend
ever calls the other directly -- run_case() below is the only place the
two are wired together.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .adapter import ModelAdapter
from .backend import InferenceBackend, RawGenerationResult


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
    """Run one canonical context through one adapter + backend pair.

    Step 2 note: this function does not write anything to lab/results/
    and does not assign a brain_verdict -- it only proves the plumbing.
    Real result-record writing and scoring are separate, later,
    explicitly-authorized steps.
    """
    formatted_prompt = adapter.format_prompt(canonical_context)
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
