"""Temporary Grounded Statements -- deterministic surfacing-eligibility
proof (research-only).

Demonstrates, without touching the frozen four-field shape at all, the
distinction the frozen design note
(docs/2026-09-08-temporary-grounded-statements-design.md, committed
aa5a0fcf76b40d7c7239c273338a0537d17ae453) draws between:

  1. historical retention of a record -- permanent, never computed or
     affected by anything in this module
  2. eligibility for active-context surfacing -- a read-time-only
     judgment, computed here and only here

is_eligible_for_surfacing() reads nothing, writes nothing, mutates
nothing, and never touches a record's own fields. Its only inputs are
`reported_at`, a caller-supplied `now`, and a caller-supplied
`threshold` -- it never reads the system clock itself, so every call in
this proof is fully deterministic and reproducible. It embeds no
threshold value of its own: `threshold` has no default, so no value
inside this module could ever be mistaken for production policy.

Deliberately isolated from schema.py in this same directory: this
module does not import it, does not know the four-field shape, and
does not validate anything -- callers pass the already-validated
record's `reported_at` string directly.

Timezone-awareness is an explicit mechanical precondition, not left to
an accidental raw TypeError from datetime subtraction: both the parsed
`reported_at` and the caller-supplied `now` must be timezone-aware, or
is_eligible_for_surfacing() raises a clear ValueError naming which one
was naive. This is required only so the age computation is meaningful
and deterministic -- it is not a production timestamp format decision;
a future real implementation may still choose any representation it
wants.
"""

from __future__ import annotations

from datetime import datetime, timedelta


def _parse_reported_at(reported_at: str) -> datetime:
    """Parse the ISO-8601 `reported_at` string used by the committed
    Temporary Grounded Statements examples into a comparable datetime.
    Mechanical parsing only -- no format validation, no policy. May
    return a naive datetime if `reported_at` itself lacks a UTC offset;
    is_eligible_for_surfacing() is what enforces awareness, not this
    function. A future real implementation may choose a different
    timestamp representation entirely; this proof does not decide
    that."""
    return datetime.fromisoformat(reported_at.replace("Z", "+00:00"))


def is_eligible_for_surfacing(reported_at: str, now: datetime, threshold: timedelta) -> bool:
    """True if a record with this `reported_at` is eligible to be
    offered as active context at `now`, False otherwise.

    Boundary rule, matching the frozen design note's own wording
    verbatim ("now - reported_at > threshold" as the exclusion
    condition): age <= threshold is eligible; only age > threshold is
    not. The boundary itself (age exactly equal to threshold) is
    therefore eligible.

    Requires both `reported_at` (once parsed) and `now` to be
    timezone-aware -- a mechanical precondition for a meaningful,
    deterministic age comparison, not a production timestamp-format
    decision. Raises ValueError, naming which value was naive, rather
    than letting a naive/aware mismatch surface as a raw TypeError from
    datetime subtraction.
    """
    parsed_reported_at = _parse_reported_at(reported_at)
    if parsed_reported_at.tzinfo is None:
        raise ValueError(
            "is_eligible_for_surfacing requires a timezone-aware "
            f"reported_at for deterministic comparison; got naive "
            f"value parsed from {reported_at!r}"
        )
    if now.tzinfo is None:
        raise ValueError(
            "is_eligible_for_surfacing requires a timezone-aware now "
            f"for deterministic comparison; got naive value {now!r}"
        )

    age = now - parsed_reported_at
    return age <= threshold
