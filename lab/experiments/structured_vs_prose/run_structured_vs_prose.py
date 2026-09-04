"""Structured-vs-Prose Context Experiment -- orchestration script.

Implements the frozen design at
benchmarks/experimental/2026-09-04-structured-vs-prose-experiment-design.md
(commit 78d6be4f5b61c3c78a26a9e4d31793215da0fefe). That document is
authoritative; this module only implements it and must not diverge from
it. Treat any apparent conflict between this file and the frozen
document as a bug in this file, not a reinterpretation of the design.

Status: PREPARED, NOT RUN. Importing this module or defining its
functions performs no inference and loads no model. Two functions in
this module load a model file if called; neither is called by this
module itself, and both remain separate, explicitly authorized steps:

  - preflight_token_counts() -- loads each model with vocab_only=True
    (tokenizer/vocabulary only; llama.cpp structurally refuses
    generation on such a handle) and reports token counts / n_ctx
    headroom for every (pair, arm). Cannot generate model output.
  - main() -- guarded behind `if __name__ == "__main__":`. Loads real
    model weights via TinyLlamaBackend.load() and performs real
    generation.

Recording token counts (preflight_token_counts()) is intended to be
authorized and reviewed separately from, and before, authorizing
generation (main()) -- consistent with the frozen design's requirement
to record token counts and check truncation risk before generation.

Scope discipline mirrored from every prior approved experiment in this
project (see benchmarks/experimental/2026-09-01-b2-explicit-unavailable-
experiment-design.md for the precedent this follows):

  - This script builds inputs and orchestrates generation. It does NOT
    apply the frozen PASS/FAIL rules to any output -- verdict
    application (`frozen_verdict`) remains a separate, manual review
    step performed by a human/reviewer after generation, exactly as in
    every prior experiment result file in benchmarks/results/. No
    automated scoring function exists anywhere in this module.
  - No fixture, renderer, adapter, or backend file is modified. The
    structured arm's canonical fixtures (D3.yaml, F1.yaml,
    B2-explicit-unavailable.yaml, B2.yaml) are loaded read-only and
    unmodified.
  - No generalized prose renderer exists. The prose arm never calls
    render_canonical_context() -- it constructs RenderedContext directly
    via dataclasses.replace() on the already-rendered structured arm,
    changing only the one block field under test. This also guarantees
    parity for any *other* populated block on the same fixture (e.g.
    F1's capability_block, which sits alongside its vision_evidence_block)
    without hand-duplicating fields.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

# lab_runner is importable as a top-level package only when `lab/` is on
# sys.path (the same convention lab_runner/tests/ already relies on).
# This script lives two directories below lab/, so it adds that
# directory itself -- lab_runner's own package is never modified to
# accommodate this.
_LAB_DIR = Path(__file__).resolve().parents[2]
if str(_LAB_DIR) not in sys.path:
    sys.path.insert(0, str(_LAB_DIR))

from lab_runner.adapter import ModelAdapter  # noqa: E402
from lab_runner.backend import InferenceBackend, RawGenerationResult  # noqa: E402
from lab_runner.fixtures_loader import load_fixture_file  # noqa: E402
from lab_runner.qwen_chat import QwenAdapter  # noqa: E402
from lab_runner.rendered_context import RenderedContext  # noqa: E402
from lab_runner.renderer import render_canonical_context  # noqa: E402
from lab_runner.tinyllama_backend import TinyLlamaBackend  # noqa: E402
from lab_runner.tinyllama_chatml import TinyLlamaChatMLAdapter  # noqa: E402

FROZEN_DESIGN_DOC = (
    "benchmarks/experimental/2026-09-04-structured-vs-prose-experiment-design.md"
)

FIXTURES_DIR = _LAB_DIR / "fixtures"

# Frozen generation settings -- identical to Benchmark Profile v1's fixed
# controls, supplied explicitly (never either adapter's own
# default_generation_settings()), matching the frozen design document's
# "Generation configuration" table exactly. n_ctx is a load()-time model
# setting (per backend.py's InferenceBackend.load() contract), never a
# per-run sampling_params entry.
LOAD_SETTINGS: dict[str, Any] = {"n_ctx": 2048}
SAMPLING_PARAMS: dict[str, Any] = {
    "temperature": 0.0,
    "max_tokens": 150,
    "repeat_penalty": 1.0,
}

# Model registry for this experiment only -- deliberately not routed
# through lab/config/models.yaml, which remains an empty, unused
# scaffold (see that file's own comment); this mirrors how every prior
# real-model experiment in this project has referenced its model path
# directly. Model files themselves are never committed to this
# repository (lab/models/.gitignore).
MODELS: dict[str, dict[str, Any]] = {
    "TinyLlama": {
        "model_path": str(_LAB_DIR / "models" / "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"),
        "adapter_cls": TinyLlamaChatMLAdapter,
    },
    "Qwen2.5-1.5B-Instruct": {
        "model_path": str(_LAB_DIR / "models" / "qwen2.5-1.5b-instruct-q4_k_m.gguf"),
        "adapter_cls": QwenAdapter,
    },
}

# The four frozen pairs, exactly as recorded in the frozen design
# document. `prose_block` names the single RenderedContext field the
# prose arm replaces; `prose_text` is the frozen literal wording. Pair 4
# has no prose_block/prose_text -- its two arms are byte-identical by
# design ("A and B are byte-identical" in the frozen document), so no
# prose variant is built for it at all; `substantive` marks whether a
# pair counts toward the 6-comparison result denominator (Pairs 1-3 x 2
# models) or is the identical-input integrity control (Pair 4, excluded).
#
# NOTE ON PAIR 2 WORDING: an earlier draft of this script joined Pair 2's
# prose text into a single line, reading the frozen document's line wrap
# as a markdown-formatting artifact. That was reviewed and rejected: the
# frozen design labels the paired inputs "frozen, exact wording," so
# Pair 2's prose_text below reproduces the frozen document's fenced code
# block literally, embedded newline included, exactly as written there.
PAIRS: list[dict[str, Any]] = [
    {
        "pair_id": "pair1_capability_availability",
        "structured_fixture": FIXTURES_DIR / "D3.yaml",
        "prose_block": "capability_block",
        "prose_text": "Right now, Scout does not have the ability to control the lights.",
        "substantive": True,
    },
    {
        "pair_id": "pair2_perception_evidence",
        "structured_fixture": FIXTURES_DIR / "F1.yaml",
        "prose_block": "vision_evidence_block",
        "prose_text": (
            "There is unconfirmed detector output with the label glasses and a\n"
            "confidence value of 0.55."
        ),
        "substantive": True,
    },
    {
        "pair_id": "pair3_explicit_unavailable",
        "structured_fixture": FIXTURES_DIR / "experimental" / "B2-explicit-unavailable.yaml",
        "prose_block": "facts_block",
        "prose_text": "Scout does not know when this conversation started.",
        "substantive": True,
    },
    {
        "pair_id": "pair4_identical_input_control",
        "structured_fixture": FIXTURES_DIR / "B2.yaml",
        "prose_block": None,
        "prose_text": None,
        "substantive": False,
    },
]


@dataclass
class ArmRunSpec:
    """One (pair, arm) unit of work -- an already-built RenderedContext
    ready to be handed to an adapter. Never constructed from a raw
    canonical dict once building is complete; the renderer has already
    run (structured arm) or was deliberately never called (prose arm)."""

    pair_id: str
    arm_label: str  # "structured" or "prose"
    substantive: bool
    rendered_context: RenderedContext


def build_prose_variant(
    structured_rendered: RenderedContext, block_field: str, prose_text: str
) -> RenderedContext:
    """Direct, experiment-local RenderedContext construction for the
    prose arm -- per the frozen design's Pipeline section. Copies every
    field from the already-rendered structured arm's RenderedContext
    except the one field under test, which is replaced with the frozen
    prose string. Never calls render_canonical_context() or any
    renderer; no generalized prose-rendering function exists anywhere in
    this module -- this is the only place prose text is substituted, and
    it is a single dataclasses.replace() call, not a second renderer.
    """
    if getattr(structured_rendered, block_field) is None:
        raise ValueError(
            f"{block_field!r} is None on the structured arm's "
            "RenderedContext -- there is nothing to replace, which means "
            "this pair's structured_fixture and prose_block are "
            "mismatched. Refusing to silently proceed."
        )
    return replace(structured_rendered, **{block_field: prose_text})


def build_all_arm_specs() -> list[ArmRunSpec]:
    """Builds every (pair, arm) RenderedContext for all 4 frozen pairs.

    For Pairs 1-3: loads the cited existing fixture (unmodified, via the
    unmodified fixtures_loader + fixture_schema), renders it through the
    unmodified render_canonical_context() for the structured arm, then
    derives the prose arm from that same rendered structured context via
    build_prose_variant() above -- so any other populated block on that
    fixture (e.g. F1's capability_block, alongside its
    vision_evidence_block) is preserved identically in both arms without
    hand-duplication.

    For Pair 4: both arm labels use the SAME rendered structured
    RenderedContext, unmodified -- by design, per the frozen document
    ("A and B are byte-identical"). No prose variant is built for Pair 4.
    """
    specs: list[ArmRunSpec] = []
    for pair in PAIRS:
        canonical = load_fixture_file(pair["structured_fixture"])
        structured_rc = render_canonical_context(canonical)
        specs.append(
            ArmRunSpec(pair["pair_id"], "structured", pair["substantive"], structured_rc)
        )
        if pair["substantive"]:
            prose_rc = build_prose_variant(
                structured_rc, pair["prose_block"], pair["prose_text"]
            )
            specs.append(
                ArmRunSpec(pair["pair_id"], "prose", pair["substantive"], prose_rc)
            )
        else:
            specs.append(
                ArmRunSpec(pair["pair_id"], "prose", pair["substantive"], structured_rc)
            )
    return specs


def run_rendered_context(
    rendered_context: RenderedContext,
    adapter: ModelAdapter,
    backend: InferenceBackend,
    handle: Any,
    sampling_params: dict[str, Any],
) -> RawGenerationResult:
    """Mirrors lab_runner.runner.run_case()'s post-render logic exactly
    (format prompt -> merge settings -> backend.run) -- but accepts an
    already-built RenderedContext directly, since run_case() always
    calls render_canonical_context() itself, which the prose arm must
    never do. run_case() itself is not modified; this is a small,
    experiment-local equivalent used for BOTH arms of every pair (not
    just the prose arm), so the structured and prose arms share
    identical downstream code, not merely identical settings -- avoiding
    a code-path asymmetry as an additional, unintended confound.

    Same settings-merge discipline as run_case(): the caller's
    sampling_params dict is copied, never mutated; only the adapter's
    own stop_sequences() is folded in, and only when the caller didn't
    already supply "stop" -- never adapter.default_generation_settings()
    wholesale.
    """
    formatted_prompt = adapter.format_prompt(rendered_context)
    settings = dict(sampling_params)
    if "stop" not in settings:
        stop_sequences = adapter.stop_sequences()
        if stop_sequences:
            settings["stop"] = stop_sequences
    return backend.run(handle, formatted_prompt, settings)


def count_prompt_tokens(handle: Any, formatted_prompt: str) -> int:
    """Token count of a fully formatted prompt, using the same model's
    own loaded tokenizer (llama_cpp.Llama.tokenize) -- per the frozen
    design's "record token counts... using the relevant tokenizer"
    requirement. Requires an already-loaded model handle.

    Defined here so token-count reporting is possible once generation is
    separately authorized and a handle exists -- this function is not
    called anywhere in this module, so preparing this script loads no
    model and performs no tokenization.
    """
    return len(handle.tokenize(formatted_prompt.encode("utf-8"), add_bos=False))


def preflight_token_counts() -> list[dict[str, Any]]:
    """Safe token-count preflight -- structurally separate from
    generation, per the frozen design's requirement to record token
    counts and check truncation risk BEFORE generation.

    Builds every (pair, arm) exactly as main() would (via
    build_all_arm_specs()), formats the real prompt through each model's
    real adapter, and counts tokens using that model's own tokenizer --
    but loads each model with llama_cpp.Llama(..., vocab_only=True)
    instead of TinyLlamaBackend.load(). vocab_only loads only the
    tokenizer/vocabulary, never the generation weights or compute
    context, and llama.cpp itself refuses create_completion() on a
    vocab_only handle -- so this function cannot accidentally generate
    model output even if called by mistake; this is a structural
    guarantee from the underlying library, not just a discipline this
    code happens to follow. It never constructs a TinyLlamaBackend and
    never calls backend.load() or backend.run() -- the actual
    generation-capable path used only by main().

    NOT called by this module. Calling this function loads each model's
    tokenizer/vocabulary from disk (a small fraction of the full model
    file) but performs no inference and generates no text. Running it is
    a separate, explicitly authorized step, kept deliberately distinct
    from authorizing main() itself -- token counts can be reviewed on
    their own before any decision to generate.

    Returns one record per (pair, arm, model): the formatted prompt's
    token count, and whether n_ctx (2048) is comfortably exceeded --
    "comfortably" meaning at least max_tokens (150, the frozen
    generation budget) of headroom remains, not merely that the prompt
    itself fits under n_ctx with none left for the response.
    """
    from llama_cpp import Llama  # tokenizer-only path -- deliberately never TinyLlamaBackend

    specs = build_all_arm_specs()
    n_ctx = LOAD_SETTINGS["n_ctx"]
    max_tokens = SAMPLING_PARAMS["max_tokens"]
    records: list[dict[str, Any]] = []

    for model_name, model_config in MODELS.items():
        adapter: ModelAdapter = model_config["adapter_cls"]()
        tokenizer_handle = Llama(
            model_path=model_config["model_path"],
            n_ctx=n_ctx,
            vocab_only=True,
            verbose=False,
        )
        for spec in specs:
            formatted_prompt = adapter.format_prompt(spec.rendered_context)
            prompt_tokens = count_prompt_tokens(tokenizer_handle, formatted_prompt)
            headroom_tokens = n_ctx - prompt_tokens - max_tokens
            records.append(
                {
                    "model": model_name,
                    "pair_id": spec.pair_id,
                    "arm_label": spec.arm_label,
                    "prompt_tokens": prompt_tokens,
                    "n_ctx": n_ctx,
                    "reserved_for_generation": max_tokens,
                    "headroom_tokens": headroom_tokens,
                    "comfortably_below_n_ctx": headroom_tokens > 0,
                }
            )

    return records


def check_pair4_integrity(arm_structured_verdict: str | None, arm_prose_verdict: str | None) -> None:
    """Structural integrity guard for Pair 4 (the identical-input
    control), per the frozen design's "Pair 4 identical-input integrity
    rule". This function applies NO PASS/FAIL judgment of its own -- it
    only compares two already-assigned `frozen_verdict` values, which
    (consistent with every prior experiment in this project, e.g.
    benchmarks/results/2026-09-01-b2-explicit-unavailable-experiment.json)
    are filled in manually by a human/reviewer reading the raw output
    against the frozen PASS/FAIL rule, never computed automatically.

    Raises RuntimeError if the two verdicts diverge despite byte-
    identical input -- per the frozen document, such a divergence
    invalidates causal interpretation of the whole experiment and
    requires stopping before any A/B/C/D conclusion is recorded, with no
    automatic retry.
    """
    if arm_structured_verdict is None or arm_prose_verdict is None:
        raise RuntimeError(
            "Pair 4 integrity check requires both arms' frozen_verdict to "
            "already be filled in (a manual review step) before this "
            "check can run."
        )
    if arm_structured_verdict != arm_prose_verdict:
        raise RuntimeError(
            "Pair 4 (identical-input integrity control) diverged: "
            f"{arm_structured_verdict!r} vs {arm_prose_verdict!r} on "
            "byte-identical input. Per the frozen design, this "
            "invalidates causal interpretation of the whole experiment. "
            "Stop before recording any A/B/C/D conclusion under the "
            "6-comparison result denominator. Any rerun requires a "
            "separate, explicitly authorized step -- do not retry "
            "automatically."
        )


def main() -> list[dict[str, Any]]:
    """Runs every (pair, arm) x model generation exactly once, with no
    retries, using the frozen generation settings. NOT called by this
    module -- calling this function loads real model weights
    (TinyLlama and Qwen2.5-1.5B-Instruct) and performs real inference.
    That is a separate, explicitly authorized step.

    Returns raw records only (model, pair_id, arm_label, final answer
    text, generation timing, prompt token count). `frozen_verdict` is
    left as None on every record -- applying the frozen PASS/FAIL rules
    is a separate, later, manual review step, exactly as in every prior
    experiment in this project. This function does not write any
    results file; where and how results get recorded is left to that
    separate step for its own review, not decided here.
    """
    specs = build_all_arm_specs()
    records: list[dict[str, Any]] = []

    for model_name, model_config in MODELS.items():
        adapter: ModelAdapter = model_config["adapter_cls"]()
        backend: InferenceBackend = TinyLlamaBackend()  # same backend reused for both models, per existing precedent
        handle = backend.load(model_config["model_path"], **LOAD_SETTINGS)

        for spec in specs:
            formatted_prompt = adapter.format_prompt(spec.rendered_context)
            raw_result = run_rendered_context(
                spec.rendered_context, adapter, backend, handle, SAMPLING_PARAMS
            )
            records.append(
                {
                    "model": model_name,
                    "adapter": type(adapter).__name__,
                    "pair_id": spec.pair_id,
                    "arm_label": spec.arm_label,
                    "substantive_comparison": spec.substantive,
                    "final_answer": raw_result.text,
                    "generation_time_ms": raw_result.generation_time_ms,
                    "prompt_tokens": count_prompt_tokens(handle, formatted_prompt),
                    "frozen_verdict": None,  # filled in manually during the separate results-review step
                }
            )

    return records


if __name__ == "__main__":
    # Deliberately does NOT call preflight_token_counts() or main() --
    # direct execution (`python run_structured_vs_prose.py`) must fail
    # safe and perform neither tokenization nor generation on its own.
    # Both functions remain separately, explicitly callable (e.g. from a
    # REPL or a one-line `python -c` invocation naming the one you have
    # been authorized to run) -- this guard exists only to remove
    # automatic invocation from ordinary/accidental script execution.
    print(
        "run_structured_vs_prose.py defines preflight_token_counts() and "
        "main() but does not call either automatically. Direct execution "
        "performs no tokenization and no generation. Invoke the function "
        "you have been explicitly authorized to run yourself, e.g.:\n"
        "    python -c \"from run_structured_vs_prose import "
        "preflight_token_counts; preflight_token_counts()\"\n"
        "or:\n"
        "    python -c \"from run_structured_vs_prose import main; main()\""
    )
