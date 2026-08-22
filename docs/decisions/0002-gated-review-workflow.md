# 0002 — Gated research-to-decision workflow

**Status:** Approved
**Date:** 2026-08-22

## Decision

Nothing produced during research or discussion — by Claude, by ChatGPT, or as
an in-conversation idea — automatically becomes a permanent project decision.
The required path is:

Research/discussion → Claude reports → ChatGPT independently reviews →
Patrick approves → **only then** may it enter the permanent record (the
Charter, a decision record, an approved benchmark definition, or
`SCOUT_AI_STATUS.md`).

## Reason

Long-running, multi-session work with two independent AI collaborators needs
a trustworthy permanent record that doesn't silently drift based on whichever
conversation happened most recently or which AI proposed something most
persuasively. This mirrors why the real Scout app's own workflow (see its
`CLAUDE.md`) requires an independent reviewer to inspect an actual diff before
anything merges — the same discipline, applied to Scout AI's documents instead
of Scout's code.

## Alternatives considered

- Trusting a single AI's session report as sufficient to update the permanent
  record — rejected, for the reason above.

## Consequences

- `RESEARCH_LOG.md` can and should record findings and ideas as they happen,
  immediately — but tagged (`VERIFIED` / `DESIGN IDEA` / `OPEN QUESTION` /
  `SUPERSEDED`), and nothing there is authoritative on its own.
- A benchmark, design, or architectural conclusion is not "done" when Claude
  finishes writing it — it's done when this workflow completes.
- Old conversation history never overrides a newer approved decision — see
  the source-of-truth order in `SCOUT_AI_STATUS.md`.
