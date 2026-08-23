"""Step 3 fixture schema/loader tests.

Uses only synthetic, plumbing-only fixtures (see fixture_data/) -- never
Patrick's real Scout data. Proves the validator actually rejects
malformed input rather than silently accepting it.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from lab_runner.fixture_schema import FixtureValidationError
from lab_runner.fixtures_loader import load_fixture_dict, load_fixture_file

FIXTURE_DATA_DIR = Path(__file__).parent / "fixture_data"


class TestFixtureLoading(unittest.TestCase):
    def test_valid_fixture_loads_successfully(self) -> None:
        fixture = load_fixture_file(FIXTURE_DATA_DIR / "valid_synthetic.yaml")
        self.assertEqual(fixture["test_id"], "TEST_SYNTHETIC_VALID_01")
        self.assertIn("current_user_input", fixture)

    def test_unknown_field_rejected(self) -> None:
        with self.assertRaises(FixtureValidationError):
            load_fixture_file(FIXTURE_DATA_DIR / "invalid_synthetic.yaml")

    def test_missing_required_field_rejected(self) -> None:
        data = {"test_id": "X"}  # current_user_input missing
        with self.assertRaises(FixtureValidationError):
            load_fixture_dict(data)

    def test_invalid_type_rejected(self) -> None:
        data = {
            "test_id": "X",
            "current_user_input": "hello",
            "retrieved_facts": "should be a list, not a string",
        }
        with self.assertRaises(FixtureValidationError):
            load_fixture_dict(data)

    def test_invalid_conversation_role_rejected(self) -> None:
        data = {
            "test_id": "X",
            "current_user_input": "hello",
            "permitted_recent_turns": [{"role": "robot", "text": "not a valid role"}],
        }
        with self.assertRaises(FixtureValidationError):
            load_fixture_dict(data)

    def test_unknown_nested_turn_field_rejected(self) -> None:
        data = {
            "test_id": "X",
            "current_user_input": "hello",
            "permitted_recent_turns": [
                {"role": "user", "text": "hello", "typo_field": "accidental"}
            ],
        }
        with self.assertRaises(FixtureValidationError):
            load_fixture_dict(data)


if __name__ == "__main__":
    unittest.main()
