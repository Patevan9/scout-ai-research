# Scout AI Research

A parallel, groundwork-only research and design track for a future Scout-specific
local AI brain — substantially better at *being Scout* than TinyLlama is today.

This is **not** a general-purpose or frontier-AI project. The goal is narrow and
specific: a small local model (plus the deterministic systems around it) that
understands household conversation, context, people, memory, vision information,
habits, and Scout's own tools better than the current baseline — not one that
competes with ChatGPT or Claude.

## Relationship to Project Scout

The real Scout app lives at [Patevan9/Scout](https://github.com/Patevan9/Scout) —
a private, local-first AI companion for Android, currently in its stability-first,
pre-launch phase.

**This repo does not touch that one.** Project Scout builds today's Scout safely;
this repo explores what Scout could eventually become. Current Scout development —
launch priorities, real-device testing, approved PR work — always takes precedence
and is never interrupted or refactored for anything discussed here.

## Status

**Groundwork only.** No implementation, no fine-tuning, no replacement of
TinyLlama, no code. Right now this repo exists to hold the research direction and
the design of the first concrete deliverable: the **Scout Intelligence Test** — a
permanent benchmark of real Scout interactions that any future brain must
demonstrably beat.

## Start here

- **[`SCOUT_AI_STATUS.md`](SCOUT_AI_STATUS.md)** — the current handoff document.
  Read this first in any new session; it's meant to be enough to recover where
  the project stands without prior conversation history.
- **[`SCOUT_AI_CHARTER.md`](SCOUT_AI_CHARTER.md)** — stable long-term vision and
  boundaries.
- **[`docs/decisions/`](docs/decisions/)** — approved architectural/process
  decisions.
- **[`benchmarks/`](benchmarks/)** — the Scout Intelligence Test, once approved.
- **[`RESEARCH_LOG.md`](RESEARCH_LOG.md)** — chronological findings.
- `CLAUDE.md` — earlier working notes, predates the structure above; being
  reconciled with it (see "Unresolved questions" in `SCOUT_AI_STATUS.md`).

---

Project Scout / Scout AI Research
Copyright © 2026 Patrick Evan Lippy. All rights reserved.
