"""Unit tests for TinyLlamaBackend.

Exercises only the call-shaping and result-extraction logic. No real
model file is ever loaded here -- `llama_cpp.Llama` is mocked/patched in
every test, matching this repository's standing policy that no .gguf
file is ever committed (see lab/models/.gitignore) and the automated
suite must not depend on one being present on disk.
"""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from lab_runner.backend import RawGenerationResult
from lab_runner.tinyllama_backend import TinyLlamaBackend


class TestTinyLlamaBackendLoad(unittest.TestCase):
    def test_load_passes_model_path_and_default_n_ctx(self) -> None:
        backend = TinyLlamaBackend()
        with patch("lab_runner.tinyllama_backend.Llama") as mock_llama_cls:
            mock_llama_cls.return_value = "fake-handle"
            handle = backend.load("/fake/path/model.gguf")

        mock_llama_cls.assert_called_once_with(
            model_path="/fake/path/model.gguf", n_ctx=2048, verbose=False
        )
        self.assertEqual(handle, "fake-handle")

    def test_load_honors_explicit_n_ctx_setting(self) -> None:
        backend = TinyLlamaBackend()
        with patch("lab_runner.tinyllama_backend.Llama") as mock_llama_cls:
            backend.load("/fake/path/model.gguf", n_ctx=4096)

        mock_llama_cls.assert_called_once_with(
            model_path="/fake/path/model.gguf", n_ctx=4096, verbose=False
        )


class TestTinyLlamaBackendRun(unittest.TestCase):
    def _fake_handle(
        self,
        text: str = "hello",
        finish_reason: str = "stop",
        completion_id: str = "cmpl-1",
        prompt_tokens: int = 10,
        completion_tokens: int = 3,
    ) -> MagicMock:
        handle = MagicMock()
        handle.create_completion.return_value = {
            "id": completion_id,
            "choices": [{"text": text, "finish_reason": finish_reason}],
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
            },
        }
        return handle

    def test_run_passes_benchmark_profile_v1_generation_settings(self) -> None:
        # Benchmark Profile v1 now fixes repeat_penalty=1.0 explicitly,
        # and the adapter/runner supply "stop" -- both flow through
        # unchanged when present in sampling_params.
        backend = TinyLlamaBackend()
        handle = self._fake_handle()

        backend.run(
            handle,
            "<|system|>\n...\n<|assistant|>\n",
            {
                "max_tokens": 150,
                "temperature": 0,
                "repeat_penalty": 1.0,
                "stop": ["</s>"],
            },
        )

        handle.create_completion.assert_called_once_with(
            prompt="<|system|>\n...\n<|assistant|>\n",
            max_tokens=150,
            temperature=0,
            repeat_penalty=1.0,
            stop=["</s>"],
        )

    def test_run_does_not_invent_repeat_penalty_when_absent(self) -> None:
        # repeat_penalty is a Benchmark Profile decision, never a backend
        # fallback (ChatGPT review finding) -- if sampling_params doesn't
        # supply one, this backend must not pass any value at all, so
        # llama-cpp-python's own library default applies rather than a
        # Scout-AI-chosen number.
        backend = TinyLlamaBackend()
        handle = self._fake_handle()

        backend.run(handle, "prompt", {"max_tokens": 150, "temperature": 0})

        _, kwargs = handle.create_completion.call_args
        self.assertNotIn("repeat_penalty", kwargs)

    def test_run_forwards_top_p_when_supplied(self) -> None:
        # Needed to faithfully represent QwenAdapter's own documented
        # sampling defaults (top_p 0.8) -- passed through unchanged, same
        # discipline as repeat_penalty.
        backend = TinyLlamaBackend()
        handle = self._fake_handle()

        backend.run(handle, "prompt", {"max_tokens": 150, "temperature": 0.7, "top_p": 0.8})

        handle.create_completion.assert_called_once_with(
            prompt="prompt", max_tokens=150, temperature=0.7, top_p=0.8
        )

    def test_run_forwards_top_k_when_supplied(self) -> None:
        # Needed to faithfully represent QwenAdapter's own documented
        # sampling defaults (top_k 20) -- passed through unchanged, same
        # discipline as repeat_penalty.
        backend = TinyLlamaBackend()
        handle = self._fake_handle()

        backend.run(handle, "prompt", {"max_tokens": 150, "temperature": 0.7, "top_k": 20})

        handle.create_completion.assert_called_once_with(
            prompt="prompt", max_tokens=150, temperature=0.7, top_k=20
        )

    def test_run_does_not_invent_top_p_or_top_k_when_absent(self) -> None:
        # TinyLlamaChatMLAdapter's own settings never specify either --
        # this backend must not substitute a value of its own for either.
        backend = TinyLlamaBackend()
        handle = self._fake_handle()

        backend.run(handle, "prompt", {"max_tokens": 150, "temperature": 0})

        _, kwargs = handle.create_completion.call_args
        self.assertNotIn("top_p", kwargs)
        self.assertNotIn("top_k", kwargs)

    def test_run_does_not_invent_stop_sequence_when_absent(self) -> None:
        # "</s>" is TinyLlama ChatML template knowledge, owned by
        # TinyLlamaChatMLAdapter -- this backend must never hard-code or
        # substitute a stop sequence itself (ChatGPT review finding).
        backend = TinyLlamaBackend()
        handle = self._fake_handle()

        backend.run(handle, "prompt", {"max_tokens": 150, "temperature": 0})

        _, kwargs = handle.create_completion.call_args
        self.assertNotIn("stop", kwargs)

    def test_run_passes_qwen_documented_generation_settings(self) -> None:
        # QwenAdapter.default_generation_settings() -- temperature 0.7,
        # top_p 0.8, top_k 20, repeat_penalty 1.1, plus its own stop
        # sequence -- all flow through this same generic backend
        # unchanged, confirming it is reusable across adapters without
        # any Qwen-specific code here.
        backend = TinyLlamaBackend()
        handle = self._fake_handle()

        backend.run(
            handle,
            "<|im_start|>system\n...\n<|im_start|>assistant\n",
            {
                "temperature": 0.7,
                "top_p": 0.8,
                "top_k": 20,
                "repeat_penalty": 1.1,
                "stop": ["<|im_end|>"],
            },
        )

        handle.create_completion.assert_called_once_with(
            prompt="<|im_start|>system\n...\n<|im_start|>assistant\n",
            max_tokens=150,
            temperature=0.7,
            repeat_penalty=1.1,
            top_p=0.8,
            top_k=20,
            stop=["<|im_end|>"],
        )

    def test_run_uses_documented_defaults_when_sampling_params_sparse(self) -> None:
        backend = TinyLlamaBackend()
        handle = self._fake_handle()

        backend.run(handle, "prompt", {})

        handle.create_completion.assert_called_once_with(
            prompt="prompt",
            max_tokens=150,
            temperature=0.0,
        )

    def test_run_returns_raw_generation_result_with_extracted_fields(self) -> None:
        backend = TinyLlamaBackend()
        handle = self._fake_handle(
            text="hi there",
            finish_reason="stop",
            completion_id="cmpl-42",
            prompt_tokens=7,
            completion_tokens=2,
        )

        result = backend.run(handle, "prompt", {"max_tokens": 150, "temperature": 0})

        self.assertIsInstance(result, RawGenerationResult)
        self.assertEqual(result.text, "hi there")
        self.assertEqual(result.prompt_tokens, 7)
        self.assertEqual(result.tokens_generated, 2)
        # Not measured by this minimal backend -- see module docstring.
        self.assertIsNone(result.time_to_first_token_ms)
        self.assertIsNotNone(result.generation_time_ms)
        self.assertGreaterEqual(result.generation_time_ms, 0.0)
        self.assertEqual(result.raw_backend_info["finish_reason"], "stop")
        self.assertEqual(result.raw_backend_info["completion_id"], "cmpl-42")

    def test_run_never_forwards_n_ctx_to_create_completion(self) -> None:
        # n_ctx is a load()-time model setting, never a per-run generation
        # setting -- confirms the boundary documented in the module
        # docstring and in ADR-0006's responsibility split.
        backend = TinyLlamaBackend()
        handle = self._fake_handle()

        backend.run(handle, "prompt", {"n_ctx": 4096, "max_tokens": 150, "temperature": 0})

        _, kwargs = handle.create_completion.call_args
        self.assertNotIn("n_ctx", kwargs)


if __name__ == "__main__":
    unittest.main()
