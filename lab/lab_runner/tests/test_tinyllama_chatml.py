"""Step 4/5 tests: TinyLlamaChatMLAdapter.

Exact-string assertions against the ChatML format verified directly from
Scout's real source (OfflinePromptBuilder.kt, LlamaEngine.kt). No
inference, no model file, no backend involved. Since Step 5, the
adapter only accepts a RenderedContext -- every test here goes through
the real render_canonical_context() first, exactly as the runner does.
"""

from __future__ import annotations

import unittest

from lab_runner.renderer import render_canonical_context
from lab_runner.tinyllama_chatml import SYSTEM_INSTRUCTION, TinyLlamaChatMLAdapter


class TestTinyLlamaChatMLFormatting(unittest.TestCase):
    def setUp(self) -> None:
        self.adapter = TinyLlamaChatMLAdapter()

    def _format(self, canonical_context: dict) -> str:
        rendered_context = render_canonical_context(canonical_context)
        return self.adapter.format_prompt(rendered_context)

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

        self.assertEqual(self._format(canonical_context), expected)

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

        self.assertEqual(self._format(canonical_context), expected)

    def test_format_prompt_ends_with_bare_assistant_prefix(self) -> None:
        canonical_context = {"test_id": "X", "current_user_input": "anything"}
        result = self._format(canonical_context)
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

    def test_stop_sequences_returns_chatml_terminator(self) -> None:
        # "</s>" is TinyLlama ChatML template knowledge -- owned here,
        # never by TinyLlamaBackend (ChatGPT review finding).
        self.assertEqual(self.adapter.stop_sequences(), ["</s>"])


class TestStep5RegressionAgainstStep4(unittest.TestCase):
    """Regression proof required by the Step 5 assignment: for a context
    with no facts/state/capabilities/vision/habits, the Step 5 output
    must match Step 4's exact output byte-for-byte. This is exactly
    TestTinyLlamaChatMLFormatting.test_format_prompt_with_recent_turns'
    canonical context, checked independently here as an explicit
    no-CANONICAL-CONTEXT-section proof."""

    def test_no_new_context_fields_means_no_canonical_context_section(self) -> None:
        canonical_context = {
            "test_id": "TEST_SYNTHETIC_REGRESSION_01",
            "permitted_recent_turns": [
                {"role": "user", "text": "Remind me to water the plants on Fridays."},
                {"role": "scout", "text": "Got it -- I'll remember that."},
            ],
            "current_user_input": "What did we say about watering the plants?",
        }
        rendered_context = render_canonical_context(canonical_context)
        result = TinyLlamaChatMLAdapter().format_prompt(rendered_context)

        self.assertNotIn("CANONICAL CONTEXT", result)
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
        self.assertEqual(result, expected)


class TestCanonicalContextSection(unittest.TestCase):
    """Proves state/capability/facts/vision context becomes visible in
    the system turn under CANONICAL CONTEXT, in the approved fixed
    order, once populated."""

    def test_state_capability_facts_appear_in_fixed_order(self) -> None:
        canonical_context = {
            "test_id": "X",
            "current_user_input": "hello",
            "online_state": "offline",
            "capability_availability": {"network_available": False},
            "retrieved_facts": ["Diana's birthday is March 3rd."],
        }
        rendered_context = render_canonical_context(canonical_context)
        result = TinyLlamaChatMLAdapter().format_prompt(rendered_context)

        expected_system_text = (
            f"{SYSTEM_INSTRUCTION}\n\n"
            "CANONICAL CONTEXT:\n"
            "Connectivity: offline\n"
            "Capabilities available right now:\n"
            "- network_available: false\n"
            "Known facts:\n"
            "- Diana's birthday is March 3rd."
        )
        expected = (
            "<|system|>\n"
            f"{expected_system_text}</s>\n"
            "<|user|>\n"
            "hello</s>\n"
            "<|assistant|>\n"
        )
        self.assertEqual(result, expected)

    def test_vision_evidence_appears_under_canonical_context(self) -> None:
        canonical_context = {
            "test_id": "X",
            "current_user_input": "What do you see?",
            "simulated_vision_payload": {
                "detections": [{"label": "glasses", "confidence": 0.55}]
            },
        }
        rendered_context = render_canonical_context(canonical_context)
        result = TinyLlamaChatMLAdapter().format_prompt(rendered_context)

        self.assertIn(
            "CANONICAL CONTEXT:\n"
            "Perception evidence (unconfirmed detector output):\n"
            "- label: glasses, confidence: 0.55",
            result,
        )

    def test_reviewer_only_fields_never_appear_in_formatted_prompt(self) -> None:
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
        result = TinyLlamaChatMLAdapter().format_prompt(rendered_context)

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
