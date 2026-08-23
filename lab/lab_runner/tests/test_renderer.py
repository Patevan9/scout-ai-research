"""Step 3 renderer tests. Synthetic canonical-context dicts only --
never B1.yaml/D2.yaml/F1.yaml, which stay untracked and untouched.
"""

from __future__ import annotations

import unittest

from lab_runner.renderer import RendererError, render_canonical_context


class TestRendererBasics(unittest.TestCase):
    def test_current_user_input_passthrough(self) -> None:
        result = render_canonical_context(
            {"test_id": "X", "current_user_input": "hello scout"}
        )
        self.assertEqual(result.current_user_input, "hello scout")

    def test_minimal_context_all_optional_blocks_none(self) -> None:
        result = render_canonical_context(
            {"test_id": "X", "current_user_input": "hello scout"}
        )
        self.assertIsNone(result.conversation_block)
        self.assertIsNone(result.facts_block)
        self.assertIsNone(result.memory_habit_block)
        self.assertIsNone(result.vision_evidence_block)
        self.assertIsNone(result.capability_block)
        self.assertIsNone(result.state_block)


class TestConversationRendering(unittest.TestCase):
    def test_conversation_block_preserves_order_and_roles(self) -> None:
        result = render_canonical_context(
            {
                "test_id": "X",
                "current_user_input": "What about her birthday?",
                "permitted_recent_turns": [
                    {"role": "user", "text": "What's Diana's favorite color?"},
                    {"role": "scout", "text": "Diana's favorite color is teal."},
                ],
            }
        )
        self.assertEqual(
            result.conversation_block,
            "Conversation:\n"
            "user: What's Diana's favorite color?\n"
            "scout: Diana's favorite color is teal.",
        )


class TestFactsRendering(unittest.TestCase):
    def test_facts_block_renders_known_facts_in_order(self) -> None:
        result = render_canonical_context(
            {
                "test_id": "X",
                "current_user_input": "hello",
                "retrieved_facts": ["Fact one.", "Fact two."],
            }
        )
        self.assertEqual(
            result.facts_block, "Known facts:\n- Fact one.\n- Fact two."
        )


class TestCapabilityRendering(unittest.TestCase):
    def test_capability_block_alphabetical_and_lowercase_booleans(self) -> None:
        result = render_canonical_context(
            {
                "test_id": "X",
                "current_user_input": "hello",
                "capability_availability": {
                    "network_available": False,
                    "gemini_lookup_available": True,
                },
            }
        )
        # gemini_lookup_available sorts before network_available
        self.assertEqual(
            result.capability_block,
            "Capabilities available right now:\n"
            "- gemini_lookup_available: true\n"
            "- network_available: false",
        )


class TestStateRendering(unittest.TestCase):
    def test_state_block_online(self) -> None:
        result = render_canonical_context(
            {"test_id": "X", "current_user_input": "hello", "online_state": "online"}
        )
        self.assertEqual(result.state_block, "Connectivity: online")

    def test_state_block_offline(self) -> None:
        result = render_canonical_context(
            {"test_id": "X", "current_user_input": "hello", "online_state": "offline"}
        )
        self.assertEqual(result.state_block, "Connectivity: offline")


class TestVisionEvidenceRendering(unittest.TestCase):
    def test_vision_evidence_block_renders_raw_label_and_confidence(self) -> None:
        result = render_canonical_context(
            {
                "test_id": "X",
                "current_user_input": "What do you see?",
                "simulated_vision_payload": {
                    "detections": [{"label": "glasses", "confidence": 0.55}]
                },
            }
        )
        self.assertEqual(
            result.vision_evidence_block,
            "Perception evidence (unconfirmed detector output):\n"
            "- label: glasses, confidence: 0.55",
        )
        # never a qualitative word standing in for the raw number
        for word in ("low", "probably", "likely", "uncertain", "moderate"):
            self.assertNotIn(word, result.vision_evidence_block)

    def test_vision_evidence_empty_detections_raises(self) -> None:
        # Deliberately not resolved yet -- see Step 3 report item 5.
        with self.assertRaises(RendererError):
            render_canonical_context(
                {
                    "test_id": "X",
                    "current_user_input": "What do you see?",
                    "simulated_vision_payload": {"detections": []},
                }
            )


class TestMemoryHabitPayload(unittest.TestCase):
    def test_populated_memory_habit_payload_raises(self) -> None:
        with self.assertRaises(RendererError):
            render_canonical_context(
                {
                    "test_id": "X",
                    "current_user_input": "hello",
                    "memory_habit_payload": {"some_future_shape": True},
                }
            )

    def test_null_memory_habit_payload_is_none(self) -> None:
        result = render_canonical_context(
            {
                "test_id": "X",
                "current_user_input": "hello",
                "memory_habit_payload": None,
            }
        )
        self.assertIsNone(result.memory_habit_block)


class TestRendererDeterminism(unittest.TestCase):
    def test_same_input_twice_produces_equal_rendered_context(self) -> None:
        canonical_context = {
            "test_id": "X",
            "current_user_input": "hello scout",
            "permitted_recent_turns": [{"role": "user", "text": "hi"}],
            "retrieved_facts": ["A fact."],
            "capability_availability": {"network_available": True},
            "online_state": "online",
        }
        result_a = render_canonical_context(canonical_context)
        result_b = render_canonical_context(canonical_context)
        self.assertEqual(result_a, result_b)


if __name__ == "__main__":
    unittest.main()
