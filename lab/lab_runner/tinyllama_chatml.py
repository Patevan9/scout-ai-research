"""TinyLlamaChatMLAdapter -- the real (non-mock) ModelAdapter for
TinyLlama 1.1B Chat v1.0.

Prompt formatting only. Performs no inference and never calls an
InferenceBackend, per the ModelAdapter interface (adapter.py).

The ChatML structure and default system instruction reproduced here were
verified directly against Scout's real source, read-only, at
`Patevan9/Scout` commit `1850531`:
  - app/src/main/cpp/OfflinePromptBuilder.kt (chat template, system
    instruction)
  - app/src/main/java/com/example/scoutface/LlamaEngine.kt (generation
    defaults)

No name/identity context is used -- per explicit instruction, this step
uses Scout's verified NO-NAME default system instruction only. The
canonical fixture schema has no user-identity field, and none is added
here.
"""

from __future__ import annotations

from typing import Any

from .adapter import ModelAdapter

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

    def format_prompt(self, canonical_context: dict[str, Any]) -> str:
        """Reproduces OfflinePromptBuilder.build() exactly:

            <|system|>
            {system}</s>
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

        Renders every entry in `permitted_recent_turns` as given -- it
        does NOT apply OfflinePromptBuilder's own `maxTurns` truncation.
        That truncation is a Scout-system-level convenience; the
        canonical fixture's `permitted_recent_turns` is already the
        curated, model-neutral set of turns a RAW test case permits the
        model to see (per ADR-0005), so silently dropping any of it here
        would misrepresent what the case actually supplies.
        """
        parts: list[str] = []

        parts.append("<|system|>\n")
        parts.append(SYSTEM_INSTRUCTION.strip())
        parts.append("</s>\n")

        for turn in canonical_context.get("permitted_recent_turns") or []:
            text = (turn.get("text") or "").strip()
            if not text:
                continue
            role = turn.get("role")
            if role == "user":
                parts.append("<|user|>\n")
            else:  # "scout" -- schema already restricts role to user/scout
                parts.append("<|assistant|>\n")
            parts.append(text)
            parts.append("</s>\n")

        current_user_input = (canonical_context.get("current_user_input") or "").strip()
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
