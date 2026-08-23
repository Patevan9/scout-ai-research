"""Step 2/4A test: RenderedContext and RenderedTurn are plain,
correctly-shaped data containers -- construction and field read-back
only, no rendering logic exists here to exercise. Synthetic placeholder
strings only.
"""

from __future__ import annotations

import unittest

from lab_runner.rendered_context import RenderedContext, RenderedTurn


class TestRenderedTurn(unittest.TestCase):
    def test_construct_and_read_back(self) -> None:
        turn = RenderedTurn(role="user", text="placeholder turn text")
        self.assertEqual(turn.role, "user")
        self.assertEqual(turn.text, "placeholder turn text")


class TestRenderedContext(unittest.TestCase):
    def test_construct_and_read_back_all_fields(self) -> None:
        turns = [
            RenderedTurn(role="user", text="placeholder user turn"),
            RenderedTurn(role="scout", text="placeholder scout turn"),
        ]
        context = RenderedContext(
            current_user_input="placeholder user input",
            conversation_turns=turns,
            facts_block="placeholder facts",
            memory_habit_block="placeholder habit evidence",
            vision_evidence_block="placeholder vision evidence",
            capability_block="placeholder capability info",
            state_block="placeholder state",
        )

        self.assertEqual(context.current_user_input, "placeholder user input")
        self.assertEqual(context.conversation_turns, turns)
        self.assertEqual(context.facts_block, "placeholder facts")
        self.assertEqual(context.memory_habit_block, "placeholder habit evidence")
        self.assertEqual(context.vision_evidence_block, "placeholder vision evidence")
        self.assertEqual(context.capability_block, "placeholder capability info")
        self.assertEqual(context.state_block, "placeholder state")

    def test_optional_blocks_default_to_none(self) -> None:
        context = RenderedContext(current_user_input="placeholder user input")

        self.assertEqual(context.current_user_input, "placeholder user input")
        self.assertIsNone(context.conversation_turns)
        self.assertIsNone(context.facts_block)
        self.assertIsNone(context.memory_habit_block)
        self.assertIsNone(context.vision_evidence_block)
        self.assertIsNone(context.capability_block)
        self.assertIsNone(context.state_block)


if __name__ == "__main__":
    unittest.main()
