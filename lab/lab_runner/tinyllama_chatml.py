"""TinyLlamaChatMLAdapter -- the real (non-mock) ModelAdapter for
TinyLlama 1.1B Chat v1.0.

Prompt formatting only. Performs no inference and never calls an
InferenceBackend, per the ModelAdapter interface (adapter.py). Receives
only an already-rendered RenderedContext -- never the raw canonical
fixture dict (Option B, Step 5).

The ChatML structure and default system instruction reproduced here were
verified directly against Scout's real source, read-only, at
`Patevan9/Scout` commit `1850531`:
  - app/src/main/cpp/OfflinePromptBuilder.kt (chat template, system
    instruction)
  - app/src/main/java/com/example/scoutface/LlamaEngine.kt (generation
    defaults)

That verified structure -- the ChatML tokens, the no-name system
instruction, the trailing bare `<|assistant|>` generation prefix, and
the Scout reference generation settings -- is unchanged by the Step 5
migration; only the input boundary (RenderedContext instead of a raw
dict) and the new CANONICAL CONTEXT section are new.

No name/identity context is used -- per explicit instruction, this
adapter uses Scout's verified NO-NAME default system instruction only.
The canonical fixture schema has no user-identity field, and none is
added here.
"""

from __future__ import annotations

from typing import Any

from .adapter import ModelAdapter
from .rendered_context import RenderedContext

# Verified verbatim from OfflinePromptBuilder.buildSystemInstruction()
# with userName == null (the no-name branch).
SYSTEM_INSTRUCTION = (
    "You are Scout, a calm and helpful family companion. Give short, "
    "friendly answers. Be honest when you do not know something."
)


class TinyLlamaChatMLAdapter(ModelAdapter):
    model_id = "tinyllama-1.1b-chat-v1.0-q4km"
    model_version = "v1.0"
    quantization = "Q4_K_M"

    def format_prompt(self, rendered_context: RenderedContext) -> str:
        """Reproduces OfflinePromptBuilder.build()'s ChatML structure
        exactly, with the approved model-neutral context folded into the
        system turn:

            <|system|>
            {system instruction}

            CANONICAL CONTEXT:
            {non-empty renderer blocks, fixed approved order}</s>
            <|user|>
            {text}</s>
            <|assistant|>
            {text}</s>
            ...
            <|user|>
            {current_user_input}</s>
            <|assistant|>

        with a trailing bare `<|assistant|>` (no closing tag) as the
        generation prefix.

        The CANONICAL CONTEXT section only appears when at least one of
        the five approved blocks is populated -- if all five are None,
        the system turn is exactly the plain system instruction, byte-
        identical to Step 4's output. The fixed approved block order is:
        state, capability, facts, memory/habit, vision evidence.

        Renders every entry in `rendered_context.conversation_turns` as
        given -- it does NOT apply OfflinePromptBuilder's own `maxTurns`
        truncation. That truncation is a Scout-system-level convenience;
        the canonical fixture's turns are already the curated,
        model-neutral set of turns a RAW test case permits the model to
        see (per ADR-0005), so silently dropping any of it here would
        misrepresent what the case actually supplies.
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

        parts.append("<|system|>\n")
        parts.append(system_text)
        parts.append("</s>\n")

        for turn in rendered_context.conversation_turns or []:
            text = turn.text.strip()
            if not text:
                continue
            if turn.role == "user":
                parts.append("<|user|>\n")
            else:  # "scout" -- schema already restricts role to user/scout
                parts.append("<|assistant|>\n")
            parts.append(text)
            parts.append("</s>\n")

        current_user_input = rendered_context.current_user_input.strip()
        parts.append("<|user|>\n")
        parts.append(current_user_input)
        parts.append("</s>\n")

        parts.append("<|assistant|>\n")

        return "".join(parts)

    def default_generation_settings(self) -> dict[str, Any]:
        """SCOUT REFERENCE SETTINGS -- NOT THE APPROVED BENCHMARK PROFILE.

        These are Scout's real on-device defaults for TinyLlama
        (LlamaEngine.kt), reproduced here only as this adapter's own
        documented fallback. They are reference evidence, not an
        authoritative benchmark setting -- once a Benchmark Profile
        (Lab Runner design section 9) is approved, that profile is
        authoritative for actual benchmark runs, not this method.
        """
        return {
            "n_ctx": 2048,
            "max_tokens": 150,
            "temperature": 0.6,
            "repeat_penalty": 1.12,
        }

    def stop_sequences(self) -> list[str]:
        """TinyLlama's ChatML turns are terminated by the literal
        `</s>` token -- verified against the same real
        OfflinePromptBuilder.kt source as this adapter's ChatML
        structure (see module docstring). Structural template knowledge
        owned here per the ModelAdapter/InferenceBackend boundary
        (ADR-0006) -- TinyLlamaBackend never hard-codes or infers this
        itself.
        """
        return ["</s>"]
