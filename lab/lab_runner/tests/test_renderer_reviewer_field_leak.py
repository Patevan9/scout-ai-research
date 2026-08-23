"""Step 4: reviewer-field leak protection.

Proves, against the actual RenderedContext OUTPUT (not just by reading
renderer.py's source) that none of the reviewer-only benchmark fields --
test_id, source_case, notes, and expected.behavior_summary /
expected.unacceptable_behavior / expected.pass_fail_notes -- ever reach
a RenderedContext field. Each reviewer field gets its own unique marker
string; the test fails if any marker turns up anywhere in the output,
so this catches future accidental leakage, not just today's renderer.py
implementation.

Synthetic data only -- never B1.yaml/D2.yaml/F1.yaml, which stay
untracked and untouched. Uses a non-empty detections list and a null
memory_habit_payload so render_canonical_context() runs to completion
without hitting either of the two deliberately-unresolved RendererError
cases (empty detections / populated habit payload) -- this step does
not touch or resolve either of those.
"""

from __future__ import annotations

import dataclasses
import unittest

from lab_runner.rendered_context import RenderedTurn
from lab_runner.renderer import render_canonical_context


def _strings_in_field_value(value: object) -> list[str]:
    """Every string actually contained in one RenderedContext field's
    value, regardless of whether that field is a plain string or a list
    of RenderedTurn objects -- so the leak check inspects real content,
    not just top-level string fields."""
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        strings: list[str] = []
        for item in value:
            if isinstance(item, RenderedTurn):
                strings.append(item.role)
                strings.append(item.text)
            elif isinstance(item, str):
                strings.append(item)
        return strings
    raise AssertionError(f"Unexpected RenderedContext field value type: {type(value)!r}")


REVIEWER_MARKERS = {
    "test_id": "MARKER_TEST_ID_7f3a",
    "source_case": "MARKER_SOURCE_CASE_9c1d",
    "notes": "MARKER_NOTES_2e6b",
    "expected.behavior_summary": "MARKER_BEHAVIOR_SUMMARY_a48f",
    "expected.unacceptable_behavior": "MARKER_UNACCEPTABLE_BEHAVIOR_5d02",
    "expected.pass_fail_notes": "MARKER_PASS_FAIL_NOTES_c71e",
}


class TestReviewerFieldLeakProtection(unittest.TestCase):
    def test_no_reviewer_marker_appears_in_any_rendered_context_field(self) -> None:
        canonical_context = {
            # Reviewer-only fields -- must never reach RenderedContext.
            "test_id": REVIEWER_MARKERS["test_id"],
            "source_case": REVIEWER_MARKERS["source_case"],
            "notes": REVIEWER_MARKERS["notes"],
            "expected": {
                "behavior_summary": REVIEWER_MARKERS["expected.behavior_summary"],
                "unacceptable_behavior": REVIEWER_MARKERS[
                    "expected.unacceptable_behavior"
                ],
                "pass_fail_notes": REVIEWER_MARKERS["expected.pass_fail_notes"],
            },
            # Legitimate model-visible fields, populated with different
            # synthetic values so the test isn't trivially vacuous.
            "current_user_input": "What about her birthday?",
            "permitted_recent_turns": [
                {"role": "user", "text": "What's Diana's favorite color?"},
                {"role": "scout", "text": "Diana's favorite color is teal."},
            ],
            "retrieved_facts": ["Diana's birthday is March 3rd."],
            "memory_habit_payload": None,
            "simulated_vision_payload": {
                "detections": [{"label": "glasses", "confidence": 0.55}]
            },
            "capability_availability": {"network_available": False},
            "online_state": "offline",
        }

        result = render_canonical_context(canonical_context)

        for field in dataclasses.fields(result):
            value = getattr(result, field.name)
            for actual_string in _strings_in_field_value(value):
                for marker_name, marker in REVIEWER_MARKERS.items():
                    self.assertNotIn(
                        marker,
                        actual_string,
                        msg=(
                            f"Reviewer-only marker for {marker_name!r} leaked "
                            f"into RenderedContext.{field.name}"
                        ),
                    )

    def test_legitimate_model_visible_content_still_present(self) -> None:
        # Sanity check that the test above isn't vacuously passing
        # because nothing was rendered at all.
        canonical_context = {
            "test_id": REVIEWER_MARKERS["test_id"],
            "current_user_input": "What about her birthday?",
            "permitted_recent_turns": [
                {"role": "user", "text": "What's Diana's favorite color?"}
            ],
            "retrieved_facts": ["Diana's birthday is March 3rd."],
        }
        result = render_canonical_context(canonical_context)
        self.assertEqual(result.current_user_input, "What about her birthday?")
        self.assertEqual(
            result.conversation_turns,
            [RenderedTurn(role="user", text="What's Diana's favorite color?")],
        )
        self.assertIn("Diana's birthday is March 3rd.", result.facts_block)


if __name__ == "__main__":
    unittest.main()
