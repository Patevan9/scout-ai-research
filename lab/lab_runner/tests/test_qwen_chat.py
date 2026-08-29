"""Unit tests for QwenAdapter.

Exact-string assertions against Qwen2.5's real embedded GGUF chat
template (verified directly against the downloaded artifact -- see
qwen_chat.py's module docstring). No inference, no model file, no
backend involved. Mirrors test_tinyllama_chatml.py's structure, adjusted
for Qwen's `<|im_start|>`/`<|im_end|>` tokens instead of TinyLlama's
`<|system|>`/`<|user|>`/`<|assistant|>`/`</s>` markup -- the two formats
are intentionally NOT interchangeable, which is exactly what these tests
pin down.
"""

from __future__ import annotations

import unittest

from lab_runner.mock_backend import MockBackend
from lab_runner.renderer import render_canonical_context
from lab_runner.runner import run_case
from lab_runner.qwen_chat import QwenAdapter
from lab_runner.tinyllama_chatml import SYSTEM_INSTRUCTION as TINYLLAMA_SYSTEM_INSTRUCTION


class TestQwenChatFormatting(unittest.TestCase):
    def setUp(self) -> None:
        self.adapter = QwenAdapter()

    def _format(self, canonical_context: dict) -> str:
        rendered_context = render_canonical_context(canonical_context)
        return self.adapter.format_prompt(rendered_context)

    def test_system_wrapping_no_recent_turns(self) -> None:
        canonical_context = {
            "test_id": "TEST_SYNTHETIC_QWEN_ADAPTER_01",
            "current_user_input": "hello scout",
        }

        expected = (
            "<|im_start|>system\n"
            f"{TINYLLAMA_SYSTEM_INSTRUCTION}<|im_end|>\n"
            "<|im_start|>user\n"
            "hello scout<|im_end|>\n"
            "<|im_start|>assistant\n"
        )

        self.assertEqual(self._format(canonical_context), expected)

    def test_user_and_assistant_turn_wrapping_with_multiple_turns_preserves_order(
        self,
    ) -> None:
        canonical_context = {
            "test_id": "TEST_SYNTHETIC_QWEN_ADAPTER_02",
            "permitted_recent_turns": [
                {"role": "user", "text": "Remind me to water the plants on Fridays."},
                {"role": "scout", "text": "Got it -- I'll remember that."},
            ],
            "current_user_input": "What did we say about watering the plants?",
        }

        expected = (
            "<|im_start|>system\n"
            f"{TINYLLAMA_SYSTEM_INSTRUCTION}<|im_end|>\n"
            "<|im_start|>user\n"
            "Remind me to water the plants on Fridays.<|im_end|>\n"
            "<|im_start|>assistant\n"
            "Got it -- I'll remember that.<|im_end|>\n"
            "<|im_start|>user\n"
            "What did we say about watering the plants?<|im_end|>\n"
            "<|im_start|>assistant\n"
        )

        self.assertEqual(self._format(canonical_context), expected)

    def test_scout_role_maps_to_assistant_marker(self) -> None:
        # Direct, isolated check that "scout" (never "assistant") is the
        # fixture-schema role, and it maps to Qwen's "assistant" marker.
        canonical_context = {
            "test_id": "X",
            "permitted_recent_turns": [
                {"role": "user", "text": "u1"},
                {"role": "scout", "text": "a1"},
            ],
            "current_user_input": "u2",
        }
        result = self._format(canonical_context)
        self.assertIn("<|im_start|>assistant\na1<|im_end|>\n", result)
        self.assertIn("<|im_start|>user\nu1<|im_end|>\n", result)

    def test_format_prompt_ends_with_bare_assistant_generation_prompt(self) -> None:
        canonical_context = {"test_id": "X", "current_user_input": "anything"}
        result = self._format(canonical_context)
        self.assertTrue(result.endswith("<|im_start|>assistant\n"))
        # the trailing generation prefix must NOT be closed with <|im_end|>
        self.assertFalse(result.endswith("<|im_end|>\n"))

    def test_default_generation_settings_returns_qwen_documented_defaults(
        self,
    ) -> None:
        # Authoritative Qwen/Qwen2.5-1.5B-Instruct generation_config.json
        # values (transformers_version 4.37.0): temperature 0.7, top_p
        # 0.8, top_k 20, repetition_penalty 1.1 -- the last translated to
        # this project's own interface key `repeat_penalty`. These are
        # Qwen's own model defaults, not Benchmark Profile v1's controls.
        settings = self.adapter.default_generation_settings()
        self.assertEqual(
            settings,
            {
                "temperature": 0.7,
                "top_p": 0.8,
                "top_k": 20,
                "repeat_penalty": 1.1,
            },
        )

    def test_default_generation_settings_does_not_return_benchmark_profile_v1_values(
        self,
    ) -> None:
        # Explicit negative check: Benchmark Profile v1's temperature=0
        # and repeat_penalty=1.0 must never appear as this adapter's own
        # "documented defaults" -- those are benchmark controls, supplied
        # explicitly by the runner during an actual benchmark run, never
        # this method's job to reproduce.
        settings = self.adapter.default_generation_settings()
        self.assertNotEqual(settings.get("temperature"), 0)
        self.assertNotEqual(settings.get("repeat_penalty"), 1.0)
        self.assertNotIn("n_ctx", settings)
        self.assertNotIn("max_tokens", settings)

    def test_stop_sequences_returns_qwen_im_end(self) -> None:
        # "<|im_end|>" is Qwen2.5's real, GGUF-verified chat-end token
        # (tokenizer.ggml.eos_token_id == 151645) -- owned here, never by
        # any InferenceBackend (ADR-0006 boundary).
        self.assertEqual(self.adapter.stop_sequences(), ["<|im_end|>"])

    def test_stop_sequences_does_not_include_endoftext(self) -> None:
        # "<|endoftext|>" (id 151643) is Qwen's BOS/pad token -- the
        # embedded chat template never uses it to terminate a chat turn,
        # so it must not appear here as a stop sequence.
        self.assertNotIn("<|endoftext|>", self.adapter.stop_sequences())

    def test_system_instruction_identical_to_tinyllama_adapter(self) -> None:
        # The Scout system instruction must be identical in substance
        # between adapters -- only the model-specific wrapper tokens
        # differ. Imported directly from tinyllama_chatml.py rather than
        # duplicated, so this can never silently drift.
        from lab_runner.qwen_chat import SYSTEM_INSTRUCTION as qwen_visible_instruction

        self.assertEqual(qwen_visible_instruction, TINYLLAMA_SYSTEM_INSTRUCTION)


class TestQwenCanonicalContextSection(unittest.TestCase):
    """Proves state/capability/facts/vision context becomes visible in
    the system turn under CANONICAL CONTEXT, in the approved fixed
    order -- identical renderer behavior to TinyLlamaChatMLAdapter, only
    the surrounding tokens differ. Confirms the adapter does not
    reinterpret or bypass renderer-decided content."""

    def test_state_capability_facts_appear_in_fixed_order(self) -> None:
        canonical_context = {
            "test_id": "X",
            "current_user_input": "hello",
            "online_state": "offline",
            "capability_availability": {"network_available": False},
            "retrieved_facts": ["Diana's birthday is March 3rd."],
        }
        rendered_context = render_canonical_context(canonical_context)
        result = QwenAdapter().format_prompt(rendered_context)

        expected_system_text = (
            f"{TINYLLAMA_SYSTEM_INSTRUCTION}\n\n"
            "CANONICAL CONTEXT:\n"
            "Connectivity: offline\n"
            "Capabilities available right now:\n"
            "- network_available: false\n"
            "Known facts:\n"
            "- Diana's birthday is March 3rd."
        )
        expected = (
            "<|im_start|>system\n"
            f"{expected_system_text}<|im_end|>\n"
            "<|im_start|>user\n"
            "hello<|im_end|>\n"
            "<|im_start|>assistant\n"
        )
        self.assertEqual(result, expected)

    def test_reviewer_only_fields_never_appear_in_formatted_prompt(self) -> None:
        # Same reviewer-field-leak protection already proven for
        # TinyLlamaChatMLAdapter -- the adapter must not expose or
        # reinterpret any canonical/renderer-internal fixture field the
        # renderer did not itself decide to surface.
        canonical_context = {
            "test_id": "MARKER_TEST_ID_SHOULD_NOT_LEAK",
            "source_case": "MARKER_SOURCE_CASE_SHOULD_NOT_LEAK",
            "notes": "MARKER_NOTES_SHOULD_NOT_LEAK",
            "expected": {
                "behavior_summary": "MARKER_BEHAVIOR_SUMMARY_SHOULD_NOT_LEAK",
                "unacceptable_behavior": "MARKER_UNACCEPTABLE_SHOULD_NOT_LEAK",
                "pass_fail_notes": "MARKER_PASS_FAIL_SHOULD_NOT_LEAK",
            },
            "current_user_input": "hello",
        }
        rendered_context = render_canonical_context(canonical_context)
        result = QwenAdapter().format_prompt(rendered_context)

        for marker in (
            "MARKER_TEST_ID_SHOULD_NOT_LEAK",
            "MARKER_SOURCE_CASE_SHOULD_NOT_LEAK",
            "MARKER_NOTES_SHOULD_NOT_LEAK",
            "MARKER_BEHAVIOR_SUMMARY_SHOULD_NOT_LEAK",
            "MARKER_UNACCEPTABLE_SHOULD_NOT_LEAK",
            "MARKER_PASS_FAIL_SHOULD_NOT_LEAK",
        ):
            self.assertNotIn(marker, result)


class TestQwenBenchmarkProfileAuthority(unittest.TestCase):
    """Confirms Benchmark Profile v1's explicitly-supplied settings
    remain authoritative when run through run_case() with QwenAdapter --
    QwenAdapter.default_generation_settings() (now Qwen's own documented
    sampling defaults: temperature 0.7/top_p 0.8/top_k 20/repeat_penalty
    1.1 -- not Benchmark Profile v1's values) must never leak in
    underneath an explicit profile. Same guarantee already proven for
    TinyLlamaChatMLAdapter in test_runner.py's
    TestRunnerStopSequenceMerge; no runner.py change was needed or made
    to support this -- its existing merge logic is already adapter-
    agnostic. MockBackend only -- no real inference."""

    def test_benchmark_profile_v1_settings_override_qwen_defaults(self) -> None:
        profile_settings = {
            "max_tokens": 150,
            "temperature": 0,
            "repeat_penalty": 1.0,
        }
        adapter = QwenAdapter()
        backend = MockBackend()
        handle = backend.load(model_path="not-a-real-file.gguf")
        canonical_context = {"test_id": "T", "current_user_input": "hi"}

        run_case(
            canonical_context, adapter, backend, handle, sampling_params=profile_settings
        )

        # Benchmark Profile v1's explicit values reached the backend...
        self.assertEqual(backend.last_sampling_params["temperature"], 0)
        self.assertEqual(backend.last_sampling_params["repeat_penalty"], 1.0)
        self.assertEqual(backend.last_sampling_params["max_tokens"], 150)
        # ...and QwenAdapter's own documented defaults never leaked in
        # underneath them -- not the differing temperature/repeat_penalty
        # values, and not top_p/top_k, which the profile doesn't specify
        # at all.
        self.assertNotEqual(backend.last_sampling_params["temperature"], 0.7)
        self.assertNotEqual(backend.last_sampling_params["repeat_penalty"], 1.1)
        self.assertNotIn("top_p", backend.last_sampling_params)
        self.assertNotIn("top_k", backend.last_sampling_params)
        # only the adapter-owned stop sequence was folded in additionally
        self.assertEqual(backend.last_sampling_params["stop"], ["<|im_end|>"])

    def test_no_explicit_sampling_params_falls_back_to_qwen_documented_defaults(
        self,
    ) -> None:
        # sampling_params=None -- the pre-existing fallback path -- picks
        # up QwenAdapter's own documented defaults plus its stop sequence,
        # matching the same fallback behavior already proven for
        # TinyLlamaChatMLAdapter.
        adapter = QwenAdapter()
        backend = MockBackend()
        handle = backend.load(model_path="not-a-real-file.gguf")
        canonical_context = {"test_id": "T", "current_user_input": "hi"}

        run_case(canonical_context, adapter, backend, handle, sampling_params=None)

        self.assertEqual(backend.last_sampling_params["temperature"], 0.7)
        self.assertEqual(backend.last_sampling_params["top_p"], 0.8)
        self.assertEqual(backend.last_sampling_params["top_k"], 20)
        self.assertEqual(backend.last_sampling_params["repeat_penalty"], 1.1)
        self.assertEqual(backend.last_sampling_params["stop"], ["<|im_end|>"])


if __name__ == "__main__":
    unittest.main()
