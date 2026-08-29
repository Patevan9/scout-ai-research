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
  - Corrected after ChatGPT review of the first version of this file:
    this backend does not hard-code a ChatML stop sequence (that was a
    template-knowledge leak across the adapter/backend boundary -- see
    run()'s docstring) and does not default `repeat_penalty` itself
    (that was an uncontrolled Benchmark Profile decision made silently
    inside backend code -- llama_cpp's own sampler applies the repeat
    penalty to logits *before* greedy selection, so it is not a no-op
    parameter under temperature 0). Both are now supplied only via
    `sampling_params`, never invented here.
  - Extended (still model-neutral) to also pass through `top_p`/`top_k`
    when a caller's `sampling_params` supplies them -- needed to
    faithfully represent QwenAdapter's own documented sampling defaults,
    which use both. Same pass-through discipline as `repeat_penalty`:
    forwarded unchanged when present, never invented when absent.
    `do_sample` is deliberately NOT handled anywhere in this backend --
    `llama_cpp.Llama.create_completion()` has no such parameter (verified
    directly against its signature); sampling behavior here is expressed
    entirely through temperature/top_p/top_k/repeat_penalty, so there is
    no code path a `do_sample` flag could affect.

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
        (`max_tokens`, `temperature`, `repeat_penalty`, `top_p`, `top_k`,
        `stop`). `n_ctx` is a load()-time model setting, not a per-run
        generation setting, and is never read here -- consistent with
        the approved renderer/adapter/backend responsibility split
        (ADR-0006).

        This backend invents neither a `repeat_penalty`, `top_p`,
        `top_k`, nor a `stop` value:

        - `repeat_penalty` is a tunable Benchmark Profile decision (see
          benchmarks/benchmark-profile-v1.md), never a backend fallback
          -- confirmed by direct inspection of llama_cpp's own sampler
          chain that repeat_penalty rescales logits *before* greedy
          selection, so a silently-chosen value here would silently
          change output. If `sampling_params` doesn't supply one, this
          backend passes nothing and llama-cpp-python's own library
          default applies -- never a Scout-AI-chosen number.
        - `top_p`/`top_k` are likewise passed through unchanged only
          when present -- e.g. QwenAdapter's own documented sampling
          defaults use both; TinyLlamaChatMLAdapter's do not. This
          backend has no opinion on either and never substitutes a
          value of its own.
        - `stop` is model-specific chat-template knowledge, owned by
          each adapter's own `stop_sequences()` (e.g. TinyLlama's `</s>`,
          Qwen's `<|im_end|>`) and supplied here only via
          `sampling_params` (run_case() folds it in). If absent, this
          backend does not substitute any value itself.
        """
        max_tokens = sampling_params.get("max_tokens", 150)
        temperature = sampling_params.get("temperature", 0.0)

        completion_kwargs: dict[str, Any] = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if "repeat_penalty" in sampling_params:
            completion_kwargs["repeat_penalty"] = sampling_params["repeat_penalty"]
        if "top_p" in sampling_params:
            completion_kwargs["top_p"] = sampling_params["top_p"]
        if "top_k" in sampling_params:
            completion_kwargs["top_k"] = sampling_params["top_k"]
        stop = sampling_params.get("stop")
        if stop:
            completion_kwargs["stop"] = stop

        start = time.monotonic()
        completion = handle.create_completion(**completion_kwargs)
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
