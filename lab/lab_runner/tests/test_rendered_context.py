"""Step 2 test: RenderedContext is a plain, correctly-shaped data
container -- construction and field read-back only, no rendering logic
exists yet to exercise. Synthetic placeholder strings only.
"""

from __future__ import annotations

import unittest

from lab_runner.rendered_context import RenderedContext


class TestRenderedContext(unittest.TestCase):
    def test_construct_and_read_back_all_fields(self) -> None:
        context = RenderedContext(
            current_user_input="placeholder user input",
            conversation_block="placeholder conversation",
            facts_block="placeholder facts",
            memory_habit_block="placeholder habit evidence",
            vision_evidence_block="placeholder vision evidence",
            capability_block="placeholder capability info",
            state_block="placeholder state",
        )

        self.assertEqual(context.current_user_input, "placeholder user input")
        self.assertEqual(context.conversation_block, "placeholder conversation")
        self.assertEqual(context.facts_block, "placeholder facts")
        self.assertEqual(context.memory_habit_block, "placeholder habit evidence")
        self.assertEqual(context.vision_evidence_block, "placeholder vision evidence")
        self.assertEqual(context.capability_block, "placeholder capability info")
        self.assertEqual(context.state_block, "placeholder state")

    def test_optional_blocks_default_to_none(self) -> None:
        context = RenderedContext(current_user_input="placeholder user input")

        self.assertEqual(context.current_user_input, "placeholder user input")
        self.assertIsNone(context.conversation_block)
        self.assertIsNone(context.facts_block)
        self.assertIsNone(context.memory_habit_block)
        self.assertIsNone(context.vision_evidence_block)
        self.assertIsNone(context.capability_block)
        self.assertIsNone(context.state_block)


if __name__ == "__main__":
    unittest.main()
