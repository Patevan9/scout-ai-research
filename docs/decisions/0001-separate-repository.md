# 0001 — Separate repository for Scout AI research

**Status:** Approved
**Date:** 2026-08-22

## Decision

Scout AI research and design work happens in its own repository
(`Patevan9/scout-ai-research`), never inside `Patevan9/Scout`. The Scout app
repository is reference-only for this project — read from, never written to.

## Reason

Current Scout app development is explicitly stability-first (launch,
real-device testing, approved PR work) and must never be interrupted or
refactored for exploratory Future Scout work. That separation needs to be
structural, not just a discipline maintained by hand in every session.

## Alternatives considered

- A `future-scout/` directory inside the Scout app repository — rejected.
  Sharing a repository creates gravitational pull toward cross-contamination
  over time (a PR "just touching future-scout docs" is one small step from
  also touching app code), and CI/review process for the Scout repo isn't
  built to distinguish the two cleanly on an ongoing basis.

## Consequences

- Scout AI gets its own persistence mechanism (this documentation structure),
  independent of Scout's own `CLAUDE.md`/`Scout_Quick_Start.md` system.
- Any reference to real Scout architecture in Scout AI documents must be
  re-verified against the actual `Patevan9/Scout` source before being trusted
  — this repo's own notes can drift, same as any documentation can.
- No GitHub write access from Scout AI work ever touches the Scout app repo.
