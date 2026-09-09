"""Temporary Grounded Statements -- minimal shape validator (research-only).

Implements exactly the frozen four-field shape from
docs/2026-09-08-temporary-grounded-statements-design.md (committed
aa5a0fcf76b40d7c7239c273338a0537d17ae453). That document is
authoritative; this module only validates the shape it describes.

Deliberately isolated from lab_runner/ (fixture_schema.py, renderer.py,
rendered_context.py, fixtures_loader.py): a Temporary Grounded
Statement is not a RAW benchmark fixture, is never rendered into a
model prompt, and is never consumed by any ModelAdapter or
InferenceBackend. No file under lab_runner/ is imported or modified
here.

Validates REPRESENTATION AND VALIDATION ONLY -- no model generation, no
scoring, no persistence, no linkage between records. ALLOWED_FIELDS is
an exact whitelist, not a blacklist of specific forbidden names: any
field beyond the frozen four is rejected on sight, so no
resolution/expiration/linkage field (or any other future field) can be
added to a record without this validator being deliberately changed
first.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ALLOWED_FIELDS = frozenset({"who", "statement", "reported_at", "source"})


class TemporaryStatementValidationError(ValueError):
    """A record failed validation against the frozen four-field shape.
    Never caught and defaulted around -- a malformed record must never
    be silently accepted."""


def validate_temporary_statement(data: Any) -> None:
    """Validate one record against the frozen shape only -- exactly
    these four fields, nothing more and nothing less. `who` may be
    `None`, representing an explicitly unresolved reporter per the
    frozen design's unresolved-speaker rule, but the key itself must
    still be present, never silently omitted.
    """
    if not isinstance(data, dict):
        raise TemporaryStatementValidationError("record must be a dict")

    missing = ALLOWED_FIELDS - data.keys()
    if missing:
        raise TemporaryStatementValidationError(
            f"missing required field(s): {sorted(missing)}"
        )

    extra = data.keys() - ALLOWED_FIELDS
    if extra:
        # repr() first, then sort -- malformed YAML can produce
        # unexpected mapping keys of mixed, non-comparable types (e.g. a
        # bool alongside a str), and sorting those directly would raise
        # a raw TypeError instead of this validator's own error type.
        raise TemporaryStatementValidationError(
            f"unexpected field(s), not part of the frozen four-field "
            f"shape: {sorted(repr(key) for key in extra)}"
        )

    who = data["who"]
    if who is not None and (not isinstance(who, str) or who.strip() == ""):
        raise TemporaryStatementValidationError("who must be null or a non-empty string")

    for field in ("statement", "reported_at", "source"):
        value = data[field]
        if not isinstance(value, str) or value.strip() == "":
            raise TemporaryStatementValidationError(f"{field} must be a non-empty string")


def load_temporary_statement_file(path: str | Path) -> dict[str, Any]:
    """Load and validate one record YAML file from disk. Mirrors
    lab_runner.fixtures_loader.load_fixture_file's own load/validate
    split -- kept separate here rather than imported from there, since
    this shape is not a RAW fixture and must not be validated by
    fixture_schema's rules."""
    path = Path(path)
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise TemporaryStatementValidationError(
            f"{path}: could not parse YAML: {exc}"
        ) from exc
    if data is None:
        raise TemporaryStatementValidationError(f"{path}: record file is empty")
    validate_temporary_statement(data)
    return data
