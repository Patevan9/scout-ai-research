"""Step 4 runner-integration test.

Proves the real TinyLlamaChatMLAdapter composes correctly with the
existing MockBackend through run_case() -- the adapter/backend boundary
holds for a second, real adapter, still with zero real inference.
"""

from __future__ import annotations

import unittest

from lab_runner.mock_backend import CANNED_RESPONSE, MockBackend
from lab_runner.runner import run_case
from lab_runner.tinyllama_chatml import TinyLlamaChatMLAdapter


class TestTinyLlamaAdapterThroughMockBackend(unittest.TestCase):
    def test_adapter_prompt_flows_into_mock_backend(self) -> None:
        adapter = TinyLlamaChatMLAdapter()
        backend = MockBackend()
        handle = backend.load(model_path="not-a-real-file.gguf")

        canonical_context = {
            "test_id": "TEST_SYNTHETIC_ADAPTER_INTEGRATION_01",
            "current_user_input": "hello scout",
        }

        result = run_case(canonical_context, adapter, backend, handle)

        # the backend received the adapter's real ChatML-formatted prompt,
        # not the raw canonical context
        self.assertEqual(backend.last_prompt, result.formatted_prompt)
        self.assertIn("<|system|>", result.formatted_prompt)
        self.assertTrue(result.formatted_prompt.endswith("<|assistant|>\n"))

        # the mock's canned response comes back through the runner
        self.assertEqual(result.raw_result.text, CANNED_RESPONSE)


if __name__ == "__main__":
    unittest.main()
