"""QwenAdapter -- the ModelAdapter for Qwen2.5-1.5B-Instruct (candidate
model under investigation against the TinyLlama baseline).

Prompt formatting only. Performs no inference and never calls an
InferenceBackend, per the ModelAdapter interface (adapter.py). Receives
only an already-rendered RenderedContext -- never the raw canonical
fixture dict (Option B, per ADR-0006) -- identical boundary discipline
to TinyLlamaChatMLAdapter.

The chat template, generation-prompt suffix, and authoritative
chat-end/stop token reproduced here were verified directly against the
actual downloaded GGUF artifact
(qwen2.5-1.5b-instruct-q4_k_m.gguf, SHA-256
6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e): its
embedded `tokenizer.chat_template` metadata and
`tokenizer.ggml.eos_token_id` (151645, i.e. `<|im_end|>`), cross-checked
against llama-cpp-python 0.3.35's own independent template parsing at
load time ("Using chat eos_token: <|im_end|>"). Not assumed from general
knowledge of the Qwen model family.

Unlike TinyLlama's `</s>`-terminated Zephyr-style markup, Qwen2.5 uses
true OpenAI-style ChatML (`<|im_start|>`/`<|im_end|>`) -- a different,
incompatible template. TinyLlama's formatting is never reused here.

The Scout system instruction text is imported unchanged from
tinyllama_chatml.py rather than duplicated, so the two adapters can
never silently drift apart in wording -- only the surrounding
model-specific wrapper tokens differ here.
"""

from __future__ import annotations

from typing import Any

from .adapter import ModelAdapter
from .rendered_context import RenderedContext
from .tinyllama_chatml import SYSTEM_INSTRUCTION


class QwenAdapter(ModelAdapter):
    model_id = "qwen2.5-1.5b-instruct-q4km"
    model_version = "2.5"
    quantization = "Q4_K_M"

    def format_prompt(self, rendered_context: RenderedContext) -> str:
        """Formats rendered_context per Qwen2.5's own embedded chat
        template (verified against the real GGUF, see module docstring):

            <|im_start|>system
            {system instruction}

            CANONICAL CONTEXT:
            {non-empty renderer blocks, fixed approved order}<|im_end|>
            <|im_start|>user
            {text}<|im_end|>
            <|im_start|>assistant
            {text}<|im_end|>
            ...
            <|im_start|>user
            {current_user_input}<|im_end|>
            <|im_start|>assistant

        with a trailing bare `<|im_start|>assistant\\n` (no closing tag)
        as the generation prefix -- matching the GGUF's own template's
        `add_generation_prompt` branch exactly.

        Same CANONICAL CONTEXT rule as TinyLlamaChatMLAdapter: the
        section only appears when at least one of the five approved
        blocks is populated, in the same fixed order (state, capability,
        facts, memory/habit, vision evidence) -- this is renderer/
        architecture behavior, not model-specific, so it is reproduced
        identically here rather than reinterpreted.

        Renders every entry in `rendered_context.conversation_turns` as
        given, with no truncation -- same rationale as
        TinyLlamaChatMLAdapter (the fixture's turns are already the
        curated, model-neutral set a RAW case permits the model to see).
        """
        system_text = SYSTEM_INSTRUCTION.strip()

        canonical_context_blocks = [
            block
            for block in (
                rendered_context.state_block,
                rendered_context.capability_block,
                rendered_context.facts_block,
                rendered_context.memory_habit_block,
                rendered_context.vision_evidence_block,
            )
            if block is not None
        ]
        if canonical_context_blocks:
            system_text += "\n\nCANONICAL CONTEXT:\n" + "\n".join(
                canonical_context_blocks
            )

        parts: list[str] = []

        parts.append("<|im_start|>system\n")
        parts.append(system_text)
        parts.append("<|im_end|>\n")

        for turn in rendered_context.conversation_turns or []:
            text = turn.text.strip()
            if not text:
                continue
            if turn.role == "user":
                parts.append("<|im_start|>user\n")
            else:  # "scout" -- schema already restricts role to user/scout
                parts.append("<|im_start|>assistant\n")
            parts.append(text)
            parts.append("<|im_end|>\n")

        current_user_input = rendered_context.current_user_input.strip()
        parts.append("<|im_start|>user\n")
        parts.append(current_user_input)
        parts.append("<|im_end|>\n")

        parts.append("<|im_start|>assistant\n")

        return "".join(parts)

    def default_generation_settings(self) -> dict[str, Any]:
        """Unlike TinyLlamaChatMLAdapter, there is no verified real
        Scout on-device reference setting for Qwen to reproduce here --
        Qwen has never run on a real Scout device under this project.
        Rather than invent a new Qwen-specific default, this returns
        Benchmark Profile v1's own already-approved fixed values
        (temperature 0, max_tokens 150, n_ctx 2048, repeat_penalty 1.0)
        as the only currently-approved generation settings applicable to
        any candidate model under this profile. This method exists only
        as a defined fallback if ever called without an explicit
        sampling_params override -- a real benchmark run always supplies
        Benchmark Profile v1's settings explicitly (see runner.py).
        """
        return {
            "n_ctx": 2048,
            "max_tokens": 150,
            "temperature": 0,
            "repeat_penalty": 1.0,
        }

    def stop_sequences(self) -> list[str]:
        """Qwen2.5's chat turns are terminated by `<|im_end|>` --
        verified directly against the real GGUF's own
        `tokenizer.ggml.eos_token_id` (151645) and its embedded
        `tokenizer.chat_template`, cross-checked against
        llama-cpp-python's own independent template parsing at load
        time (see module docstring). `<|endoftext|>` (the model's
        BOS/pad token, id 151643) is deliberately excluded -- the
        embedded chat template never uses it to terminate a chat turn.
        Structural template knowledge owned here per the
        ModelAdapter/InferenceBackend boundary (ADR-0006) -- no
        InferenceBackend hard-codes or infers this itself.
        """
        return ["<|im_end|>"]
