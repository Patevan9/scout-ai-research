"""TinyLlamaBackend -- the first real (non-mock) InferenceBackend.

Loads and runs TinyLlama 1.1B Chat v1.0 (Q4_K_M GGUF) via
`llama-cpp-python`. Per the InferenceBackend interface (backend.py),
this class does exactly two things -- load a model, run inference
against an already-formatted prompt -- and nothing else:

  - It never formats a prompt or knows a chat template (that is
    TinyLlamaChatMLAdapter's job).
  - It never reads a raw canonical fixture dict.
  - It never reinterprets memory, vision, or habit semantics.
  - It never makes routing/path-selection decisions.
  - It never writes Scout memory and never performs a system action.

This is the minimum implementation needed to prove the Lab Runner's
canonical pipeline (renderer -> RenderedContext -> ModelAdapter ->
InferenceBackend) can execute one real RAW fixture end to end (Scout AI
first-real-inference step). Deliberately narrow:

  - CPU-only, one blocking (non-streaming) completion call per run() --
    no batching.
  - `time_to_first_token_ms` is NOT measured by this backend. Measuring
    it honestly would require streaming generation and per-token timing,
    which this minimal implementation does not do. Left as `None`
    (RawGenerationResult's own declared default) rather than guessed --
    a future step may add streaming if that field is ever required.
  - No seed is passed to the runtime. Benchmark Profile v1 specifies
    temperature 0 (greedy) decoding; this installed llama-cpp-python
    version's sampler takes an explicit `temp == 0.0 -> add_greedy()`
    path (verified by reading llama_cpp/llama.py directly), which is
    deterministic independent of seed.

Model file discipline: the .gguf file itself is never committed to this
repository (see lab/models/.gitignore, lab/models/README.md) -- this
module only loads whatever path it is given at load() time.
"""

from __future__ import annotations

import time
from typing import Any

from llama_cpp import Llama

from .backend import InferenceBackend, RawGenerationResult


class TinyLlamaBackend(InferenceBackend):
    """Real InferenceBackend for TinyLlama 1.1B Chat v1.0 (Q4_K_M),
    via llama-cpp-python. Loading and running inference only."""

    def load(self, model_path: str, **settings: Any) -> Llama:
        """Load the GGUF model file at `model_path` and return the
        llama_cpp.Llama handle.

        `n_ctx` may be passed via settings; defaults to 2048 (Benchmark
        Profile v1's approved model context limit) if not given. No
        other settings are currently read here -- this is the minimum
        load path needed for the proof run.
        """
        n_ctx = settings.get("n_ctx", 2048)
        return Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            verbose=False,
        )

    def run(
        self,
        handle: Llama,
        prompt: str,
        sampling_params: dict[str, Any],
    ) -> RawGenerationResult:
        """Run one blocking (non-streaming) completion against an
        already-formatted prompt string.

        Reads only generation-level settings from `sampling_params`
        (`max_tokens`, `temperature`, `repeat_penalty`). `n_ctx` is a
        load()-time model setting, not a per-run generation setting, and
        is never read here -- consistent with the approved
        renderer/adapter/backend responsibility split (ADR-0006).
        """
        max_tokens = sampling_params.get("max_tokens", 150)
        temperature = sampling_params.get("temperature", 0.0)
        repeat_penalty = sampling_params.get("repeat_penalty", 1.0)

        start = time.monotonic()
        completion = handle.create_completion(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            repeat_penalty=repeat_penalty,
            stop=["</s>"],
        )
        generation_time_ms = (time.monotonic() - start) * 1000.0

        choice = completion["choices"][0]
        usage = completion.get("usage", {})

        return RawGenerationResult(
            text=choice["text"],
            time_to_first_token_ms=None,
            generation_time_ms=generation_time_ms,
            prompt_tokens=usage.get("prompt_tokens"),
            tokens_generated=usage.get("completion_tokens"),
            raw_backend_info={
                "finish_reason": choice.get("finish_reason"),
                "completion_id": completion.get("id"),
            },
        )
