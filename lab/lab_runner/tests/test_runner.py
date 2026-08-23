"""Step 2 plumbing test.

Proves, with no real model and no llama-cpp-python dependency:
    - adapter.format_prompt() is actually called by the runner
    - the backend receives exactly that formatted prompt (not the raw
      canonical context)
    - the backend's canned response comes back through the runner
"""

from __future__ import annotations

import unittest

from lab_runner.mock_adapter import MockAdapter
from lab_runner.mock_backend import CANNED_RESPONSE, MockBackend
from lab_runner.runner import run_case


class TestRunnerPlumbing(unittest.TestCase):
    def test_context_flows_through_adapter_then_backend(self) -> None:
        adapter = MockAdapter()
        backend = MockBackend()
        handle = backend.load(model_path="not-a-real-file.gguf")

        canonical_context = {
            "test_id": "STEP2_SMOKE",
            "current_user_input": "hello scout",
        }

        result = run_case(canonical_context, adapter, backend, handle)

        expected_prompt = "MOCK_PROMPT[hello scout]"

        # adapter.format_prompt() was actually called and its output used
        self.assertEqual(result.formatted_prompt, expected_prompt)

        # the backend received the ADAPTER's formatted prompt, never the
        # raw canonical context dict
        self.assertEqual(backend.last_prompt, expected_prompt)

        # the backend's canned response comes back through the runner
        self.assertEqual(result.raw_result.text, CANNED_RESPONSE)


if __name__ == "__main__":
    unittest.main()
