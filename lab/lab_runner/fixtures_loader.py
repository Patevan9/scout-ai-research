"""Fixture loader for the canonical RAW benchmark fixture schema.

Loads a YAML fixture file, validates it against `fixture_schema`, and
returns the validated fixture as a plain dict -- the "canonical context"
a ModelAdapter.format_prompt() consumes. A malformed fixture raises
FixtureValidationError; it is never silently accepted or defaulted
around.

Dependency: PyYAML (see lab/requirements.txt) -- the only dependency
this step adds. No inference or model dependency of any kind.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .fixture_schema import FixtureValidationError, validate_fixture


def load_fixture_dict(data: Any) -> dict[str, Any]:
    """Validate an already-parsed fixture dict/object and return it
    unchanged. Kept separate from file loading so tests can validate
    synthetic fixtures without touching disk."""
    validate_fixture(data)
    return data


def load_fixture_file(path: str | Path) -> dict[str, Any]:
    """Load and validate one fixture YAML file from disk."""
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise FixtureValidationError(f"{path}: could not parse YAML: {exc}") from exc
    if data is None:
        raise FixtureValidationError(f"{path}: fixture file is empty")
    return load_fixture_dict(data)
