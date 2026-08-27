"""Step 2 plumbing test, plus the adapter-owned-stop-sequence merge
behavior added after ChatGPT's review of the first TinyLlamaBackend.

Proves, with no real model and no llama-cpp-python dependency:
    - adapter.format_prompt() is actually called by the runner
    - the backend receives exactly that formatted prompt (not the raw
      canonical context)
    - the backend's canned response comes back through the runner
    - a base ModelAdapter with no meaningful stop sequence contributes
      nothing to the settings the backend receives
    - an adapter's stop_sequences() survives into the backend-facing
      settings even when the caller supplies its own explicit Benchmark
      Profile sampling_params -- without run_case() wholesale-merging in
      adapter.default_generation_settings() (which would silently
      reintroduce TinyLlama's reference temperature/repeat_penalty
      underneath an explicit profile)
    - the caller's own sampling_params dict is never mutated
    - an explicit caller-supplied "stop" is left alone, not overwritten
      by the adapter's own stop_sequences()
"""

from __future__ import annotations

import unittest

from lab_runner.mock_adapter import MockAdapter
from lab_runner.mock_backend import CANNED_RESPONSE, MockBackend
from lab_runner.runner import run_case
from lab_runner.tinyllama_chatml import TinyLlamaChatMLAdapter


class TestRunnerPlumbing(unittest.TestCase):
    def test_context_flows_through_adapter_then_backend(self) -> None:
        adapter = MockAdapter()
        backend = MockBackend()
        handle = backend.load(model_path="not-a-real-file.gguf")

        canonical_context = {
            "test_id": "STEP2_SMOKE",
            "current_user_input": "hello scout",
        }

        result = run_case(canonical_context, adapter, backend, handle)

        expected_prompt = "MOCK_PROMPT[hello scout]"

        # adapter.format_prompt() was actually called and its output used
        self.assertEqual(result.formatted_prompt, expected_prompt)

        # the backend received the ADAPTER's formatted prompt, never the
        # raw canonical context dict
        self.assertEqual(backend.last_prompt, expected_prompt)

        # the backend's canned response comes back through the runner
        self.assertEqual(result.raw_result.text, CANNED_RESPONSE)

    def test_base_adapter_default_stop_sequence_contributes_nothing(self) -> None:
        # MockAdapter never overrides stop_sequences(), so it uses
        # ModelAdapter's own concrete default: an empty list. run_case()
        # must not add a "stop" key at all in that case.
        adapter = MockAdapter()
        backend = MockBackend()
        handle = backend.load(model_path="not-a-real-file.gguf")

        canonical_context = {"test_id": "T", "current_user_input": "hi"}
        run_case(canonical_context, adapter, backend, handle)

        self.assertNotIn("stop", backend.last_sampling_params)


class TestRunnerStopSequenceMerge(unittest.TestCase):
    """TinyLlamaChatMLAdapter has a real, non-empty stop_sequences() --
    used here (with MockBackend, still zero real inference) to prove the
    merge behavior the empty-default MockAdapter case above can't
    exercise."""

    def _run(self, sampling_params: dict | None):
        adapter = TinyLlamaChatMLAdapter()
        backend = MockBackend()
        handle = backend.load(model_path="not-a-real-file.gguf")
        canonical_context = {"test_id": "T", "current_user_input": "hi"}
        run_case(canonical_context, adapter, backend, handle, sampling_params=sampling_params)
        return backend

    def test_adapter_stop_sequence_survives_explicit_profile_settings(self) -> None:
        profile_settings = {
            "max_tokens": 150,
            "temperature": 0,
            "repeat_penalty": 1.0,
        }

        backend = self._run(profile_settings)

        # the adapter's stop sequence was folded in...
        self.assertEqual(backend.last_sampling_params["stop"], ["</s>"])
        # ...without disturbing the caller's explicit tunable values
        self.assertEqual(backend.last_sampling_params["temperature"], 0)
        self.assertEqual(backend.last_sampling_params["repeat_penalty"], 1.0)
        self.assertEqual(backend.last_sampling_params["max_tokens"], 150)

    def test_default_generation_settings_not_wholesale_merged_underneath_profile(self) -> None:
        # TinyLlamaChatMLAdapter.default_generation_settings() carries
        # Scout's reference temperature (0.6) and repeat_penalty (1.12) --
        # neither must leak into a run where the caller supplied its own
        # explicit Benchmark Profile settings.
        profile_settings = {"max_tokens": 150, "temperature": 0, "repeat_penalty": 1.0}

        backend = self._run(profile_settings)

        self.assertNotEqual(backend.last_sampling_params["temperature"], 0.6)
        self.assertNotEqual(backend.last_sampling_params["repeat_penalty"], 1.12)
        # exactly the caller's four keys plus the merged-in stop -- nothing
        # else from default_generation_settings() (e.g. "n_ctx") leaked in
        self.assertEqual(
            set(backend.last_sampling_params.keys()),
            {"max_tokens", "temperature", "repeat_penalty", "stop"},
        )

    def test_caller_supplied_stop_is_not_overridden_by_adapter(self) -> None:
        backend = self._run({"max_tokens": 150, "temperature": 0, "stop": ["CUSTOM"]})

        self.assertEqual(backend.last_sampling_params["stop"], ["CUSTOM"])

    def test_caller_sampling_params_dict_is_not_mutated(self) -> None:
        original = {"max_tokens": 150, "temperature": 0, "repeat_penalty": 1.0}
        original_copy = dict(original)

        self._run(original)

        self.assertEqual(original, original_copy)
        self.assertNotIn("stop", original)

    def test_no_sampling_params_falls_back_to_adapter_defaults_plus_stop(self) -> None:
        # sampling_params=None -- the pre-existing fallback path -- still
        # gets the adapter's stop sequence folded in too.
        backend = self._run(None)

        self.assertEqual(backend.last_sampling_params["stop"], ["</s>"])
        self.assertEqual(backend.last_sampling_params["temperature"], 0.6)


if __name__ == "__main__":
    unittest.main()
