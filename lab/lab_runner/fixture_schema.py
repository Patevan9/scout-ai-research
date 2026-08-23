"""Canonical RAW benchmark fixture schema (Scout AI Lab Runner v0.1
design, section 4).

A fixture describes INFORMATION only -- the exact facts a case permits a
model to know. It must never contain model-specific prompt syntax (no
ChatML tokens, no `<|system|>`/`<|user|>` markers, nothing tied to
TinyLlama or any other specific model's chat template). Turning a
fixture into an actual prompt string is a ModelAdapter's job, not a
fixture's.

Not every fixture uses every field -- a field a case doesn't need is
simply omitted or set to null, never guessed or defaulted to a
fabricated value.

A malformed fixture must never be silently accepted. `validate_fixture`
raises FixtureValidationError naming exactly what was wrong; callers must
let that propagate rather than catching it and defaulting around it.
"""

from __future__ import annotations

from typing import Any

VALID_TURN_ROLES = frozenset({"user", "scout"})
VALID_ONLINE_STATES = frozenset({"online", "offline"})

REQUIRED_FIELDS = frozenset({"test_id", "current_user_input"})

OPTIONAL_FIELDS = frozenset(
    {
        "source_case",
        "permitted_recent_turns",
        "retrieved_facts",
        "memory_habit_payload",
        "simulated_vision_payload",
        "capability_availability",
        "online_state",
        "expected",
        "notes",
    }
)

ALL_FIELDS = REQUIRED_FIELDS | OPTIONAL_FIELDS


class FixtureValidationError(ValueError):
    """A fixture failed validation. Never caught and defaulted around --
    a malformed fixture must never be silently accepted."""


def _require_type(data: dict[str, Any], field: str, expected: type, label: str) -> None:
    if field in data and data[field] is not None and not isinstance(data[field], expected):
        raise FixtureValidationError(f"{field} must be {label}")


def validate_fixture(data: Any) -> None:
    """Validate a fixture dict against the canonical schema.

    Raises FixtureValidationError on the first problem found.
    """
    if not isinstance(data, dict):
        raise FixtureValidationError(
            f"Fixture must be a mapping/object, got {type(data).__name__}"
        )

    unknown = set(data.keys()) - ALL_FIELDS
    if unknown:
        raise FixtureValidationError(f"Unknown fixture field(s): {sorted(unknown)}")

    missing = REQUIRED_FIELDS - set(data.keys())
    if missing:
        raise FixtureValidationError(f"Missing required fixture field(s): {sorted(missing)}")

    if not isinstance(data["test_id"], str) or not data["test_id"].strip():
        raise FixtureValidationError("test_id must be a non-empty string")

    if not isinstance(data["current_user_input"], str) or not data["current_user_input"].strip():
        raise FixtureValidationError("current_user_input must be a non-empty string")

    _require_type(data, "source_case", str, "a string")
    _require_type(data, "capability_availability", dict, "a mapping/object")
    _require_type(data, "memory_habit_payload", dict, "a mapping/object or null")
    _require_type(data, "simulated_vision_payload", dict, "a mapping/object or null")
    _require_type(data, "expected", dict, "a mapping/object")
    _require_type(data, "notes", str, "a string")

    if "retrieved_facts" in data and data["retrieved_facts"] is not None:
        if not isinstance(data["retrieved_facts"], list):
            raise FixtureValidationError("retrieved_facts must be a list")

    if "permitted_recent_turns" in data and data["permitted_recent_turns"] is not None:
        turns = data["permitted_recent_turns"]
        if not isinstance(turns, list):
            raise FixtureValidationError("permitted_recent_turns must be a list")
        for i, turn in enumerate(turns):
            if not isinstance(turn, dict):
                raise FixtureValidationError(
                    f"permitted_recent_turns[{i}] must be a mapping/object"
                )
            role = turn.get("role")
            if role not in VALID_TURN_ROLES:
                raise FixtureValidationError(
                    f"permitted_recent_turns[{i}].role must be one of "
                    f"{sorted(VALID_TURN_ROLES)}, got {role!r}"
                )
            text = turn.get("text")
            if not isinstance(text, str):
                raise FixtureValidationError(
                    f"permitted_recent_turns[{i}].text must be a string"
                )

    if "online_state" in data and data["online_state"] is not None:
        if data["online_state"] not in VALID_ONLINE_STATES:
            raise FixtureValidationError(
                f"online_state must be one of {sorted(VALID_ONLINE_STATES)}, "
                f"got {data['online_state']!r}"
            )
