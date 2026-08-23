"""Step 3 runner-integration test.

Proves a validated fixture can flow through the existing MockAdapter and
MockBackend via run_case() exactly like any other canonical context --
no real model, no new runner behavior added.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from lab_runner.fixtures_loader import load_fixture_file
from lab_runner.mock_adapter import MockAdapter
from lab_runner.mock_backend import CANNED_RESPONSE, MockBackend
from lab_runner.runner import run_case

FIXTURE_DATA_DIR = Path(__file__).parent / "fixture_data"


class TestFixtureThroughRunner(unittest.TestCase):
    def test_validated_fixture_flows_through_mock_pipeline(self) -> None:
        fixture = load_fixture_file(FIXTURE_DATA_DIR / "valid_synthetic.yaml")

        adapter = MockAdapter()
        backend = MockBackend()
        handle = backend.load(model_path="not-a-real-file.gguf")

        result = run_case(fixture, adapter, backend, handle)

        self.assertIn(fixture["current_user_input"], result.formatted_prompt)
        self.assertEqual(result.raw_result.text, CANNED_RESPONSE)


if __name__ == "__main__":
    unittest.main()
