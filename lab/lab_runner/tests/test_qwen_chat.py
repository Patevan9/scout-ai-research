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

from lab_runner.renderer import render_canonical_context
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

    def test_default_generation_settings_reuses_benchmark_profile_v1_values(
        self,
    ) -> None:
        # No real Scout on-device reference exists for Qwen (unlike
        # TinyLlama) -- this must reuse Benchmark Profile v1's own
        # already-approved values, not invent a new Qwen-specific default.
        settings = self.adapter.default_generation_settings()
        self.assertEqual(
            settings,
            {
                "n_ctx": 2048,
                "max_tokens": 150,
                "temperature": 0,
                "repeat_penalty": 1.0,
            },
        )

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


if __name__ == "__main__":
    unittest.main()
