"""Step 4 tests: TinyLlamaChatMLAdapter.

Exact-string assertions against the ChatML format verified directly from
Scout's real source (OfflinePromptBuilder.kt, LlamaEngine.kt). No
inference, no model file, no backend involved.
"""

from __future__ import annotations

import unittest

from lab_runner.tinyllama_chatml import SYSTEM_INSTRUCTION, TinyLlamaChatMLAdapter


class TestTinyLlamaChatMLFormatting(unittest.TestCase):
    def setUp(self) -> None:
        self.adapter = TinyLlamaChatMLAdapter()

    def test_format_prompt_no_recent_turns(self) -> None:
        canonical_context = {
            "test_id": "TEST_SYNTHETIC_ADAPTER_01",
            "current_user_input": "hello scout",
        }

        expected = (
            "<|system|>\n"
            f"{SYSTEM_INSTRUCTION}</s>\n"
            "<|user|>\n"
            "hello scout</s>\n"
            "<|assistant|>\n"
        )

        self.assertEqual(self.adapter.format_prompt(canonical_context), expected)

    def test_format_prompt_with_recent_turns(self) -> None:
        canonical_context = {
            "test_id": "TEST_SYNTHETIC_ADAPTER_02",
            "permitted_recent_turns": [
                {"role": "user", "text": "Remind me to water the plants on Fridays."},
                {"role": "scout", "text": "Got it -- I'll remember that."},
            ],
            "current_user_input": "What did we say about watering the plants?",
        }

        expected = (
            "<|system|>\n"
            f"{SYSTEM_INSTRUCTION}</s>\n"
            "<|user|>\n"
            "Remind me to water the plants on Fridays.</s>\n"
            "<|assistant|>\n"
            "Got it -- I'll remember that.</s>\n"
            "<|user|>\n"
            "What did we say about watering the plants?</s>\n"
            "<|assistant|>\n"
        )

        self.assertEqual(self.adapter.format_prompt(canonical_context), expected)

    def test_format_prompt_ends_with_bare_assistant_prefix(self) -> None:
        canonical_context = {"test_id": "X", "current_user_input": "anything"}
        result = self.adapter.format_prompt(canonical_context)
        self.assertTrue(result.endswith("<|assistant|>\n"))
        # the trailing generation prefix must NOT be closed with </s>
        self.assertFalse(result.endswith("</s>\n"))

    def test_default_generation_settings_matches_scout_reference(self) -> None:
        settings = self.adapter.default_generation_settings()
        self.assertEqual(
            settings,
            {
                "n_ctx": 2048,
                "max_tokens": 150,
                "temperature": 0.6,
                "repeat_penalty": 1.12,
            },
        )


if __name__ == "__main__":
    unittest.main()
