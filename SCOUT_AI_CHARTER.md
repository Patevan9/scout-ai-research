# Scout AI Charter

Permanent vision and boundaries for Scout AI. This document should stay stable —
changes require Patrick's explicit approval, following the review workflow in
`SCOUT_AI_STATUS.md`. This is not a place for in-progress ideas; see
`RESEARCH_LOG.md` for those.

## What Scout AI is

A separate, long-term research and design project to eventually create the best
practical local intelligence for Patrick's Scouts — substantially better at
*being Scout* than TinyLlama is today. Not a frontier or general-purpose AI
project; it does not need to, and is not trying to, compete with cloud systems
like ChatGPT or Claude.

## Relationship to the Scout app

- Scout AI is separate from the current Scout application.
- The [`Patevan9/Scout`](https://github.com/Patevan9/Scout) repository is
  **reference-only** for Scout AI work — read to understand real architecture
  and real problems, never modified, branched, or committed to from this
  project.
- Current Scout app development (launch priorities, real-device testing,
  approved PR work) always takes precedence and is never interrupted or
  refactored for Scout AI purposes.

## Core design principles

- **Local/private first.** Scout AI runs on-device, offline-capable, by design.
- **Model-replaceable.** The brain is a swappable component, not a fixed
  identity — Scout is not defined by which model happens to power him at a
  given time.
- **Hardware-independent.** Android is the first target, not the permanent
  hardware definition. A Raspberry Pi, mini-PC, or other host must remain
  possible later.
- **Robot-body/chassis-independent.** The KEYESTUDIO Mini Tank Kit V2 is one
  planned physical-body target — it must remain possible, but Scout AI must
  never become permanently tied to that or any single chassis. Different
  robot bodies should eventually be reachable through adapters.
- **Memory stays separate from model weights.** Truth, habits, and identity
  live in Scout's own deterministic stores, never inside the model itself —
  upgrading or replacing the brain must not mean Scout loses who he knows or
  what he's learned.
- **Upgradeable without losing identity.** A brain swap is a component
  replacement, not a rebirth.
- **Increasing autonomy is a long-term goal**, introduced deliberately and
  bounded — never assumed as a default.
- **Controlled evolution is a long-term goal** — Scout may eventually learn
  from experience and propose changes to himself, but proposing a change and
  having authority to make it are always kept separate.
- **A future Scout Constitution** — a set of supreme, model-external rules
  governing what an increasingly autonomous Scout AI may do or change —
  is a standing long-term concept for this project.
- **Scout AI may eventually be useful independently of the Scout app/robot** —
  the intelligence itself is not assumed to be permanently bound to one
  product.

## What this charter is not

Not a design spec, not a benchmark definition, not a status report. Those live
in `docs/decisions/`, `benchmarks/`, and `SCOUT_AI_STATUS.md` respectively —
see the source-of-truth order in `SCOUT_AI_STATUS.md`.

---

Project Scout / Scout AI Research
Copyright © 2026 Patrick Evan Lippy. All rights reserved.
