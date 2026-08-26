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

Scout AI is the local intelligence being designed to turn Scout from an app
that responds to commands into a companion that understands, remembers,
notices, learns, and meaningfully interacts with the people and world around
it. Scout AI is **not** Scout's identity and **not** Scout's permanent
memory — the reasoning model is a replaceable component that helps Scout
understand what is happening, connect perception with context and memory,
decide when and how to respond, and communicate naturally through speech,
behavior, and meaningful facial expression (see "Model-replaceable" below).

> Scout AI isn't about making Scout talk more. It's about giving Scout more
> to understand. Less performance. More presence.

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

- **Local-first and offline-capable, not offline-only.** Scout's identity,
  core memory, and basic intelligence must not depend on an Internet
  connection. That is a floor, not a ceiling: local-first does not mean
  offline-only. Optional, user-controlled online capabilities may be enabled
  on top of that floor — the Internet is a resource available to Scout, not
  Scout's identity or permanent brain. Different owners may choose different
  privacy/connectivity settings, including a personal Scout configured to
  remain online continuously if its owner chooses.
- **Model-replaceable — the model is not Scout.** The brain is a swappable
  component, not a fixed identity — Scout is not defined by which model
  happens to power him at a given time. TinyLlama is the current baseline
  only, never the intended final Scout AI brain (see
  [ADR-0003](docs/decisions/0003-tinyllama-baseline.md)); no future
  candidate model owns Scout's identity, Truth, memory, or personality
  continuity — those live in Scout's own deterministic stores (see the next
  principle) and persist across any brain swap. Scout AI is the larger
  architecture surrounding a replaceable reasoning component, not the
  component itself. A future candidate model is evaluated not only on
  benchmark score but on companion qualities — natural conversation,
  understanding ordinary statements, follow-up/context handling, grounded
  use of Scout memory, stable Scout identity, hallucination resistance,
  calibrated uncertainty, appropriate tool use, warmth, and practicality on
  real hardware (latency, RAM, heat, battery) — a benchmark winner that
  makes a poor companion is not automatically the right Scout AI brain (see
  [ADR-0003](docs/decisions/0003-tinyllama-baseline.md)). Scout AI decides
  conversational/expressive *intent*; rendering that intent (TTS, facial
  expression) is a separate, model-independent output system, so a brain
  swap never has to touch how Scout speaks or expresses itself.
- **Optional cloud reasoning, never required.** Ordinary Scout conversation
  must ultimately be able to run through Scout's local reasoning system.
  A cloud LLM may eventually exist as an optional, owner-controlled
  escalation for unusually difficult tasks, but it is never a required part
  of Scout AI.
- **Hardware-independent.** Android is the first target, not the permanent
  hardware definition. A Raspberry Pi, mini-PC, or other host must remain
  possible later.
- **Robot-body/chassis-independent.** The KEYESTUDIO Mini Tank Kit V2 is one
  planned physical-body target — it must remain possible, but Scout AI must
  never become permanently tied to that or any single chassis. Different
  robot bodies should eventually be reachable through adapters. Optional
  hardware capability (a future "Builder's Workbench" toggle for
  motors/sensors/navigation and similar) unlocks additional physical
  capability, never superior intelligence — the same Scout AI and the same
  Scout underneath, with or without it enabled. Ordinary users should never
  need to interact with robotics complexity to get the full companion
  experience.
- **Grounded action and honesty.** Scout AI requests information or action
  from Scout's own controlled, deterministic capabilities (weather, memory,
  calendar, perception, or any future tool) rather than inventing or
  assuming one; if it lacks current or external knowledge and an approved
  retrieval capability is enabled, it should recognize that and request
  grounded retrieval rather than guess. Retrieved or tool-provided
  information is evidence for that turn, not automatically permanent Truth,
  memory, or identity — it becomes durable only by passing through Scout's
  own memory rules. If Scout attempts a physical action and cannot verify
  it succeeded, it must not claim success.
- **No lesser public Scout.** Everyone should receive the best complete
  Scout companion experience their supported hardware can reasonably
  provide — there is no fundamentally lesser "public" Scout beside a
  superior "private" one. More capable hardware may unlock more (a larger
  local model, more memory/context, stronger perception, robotics,
  additional sensors), but hardware changes available capability, not who
  Scout is.
- **Affordable by design.** Scout AI should help keep personal companion-AI
  technology affordable. Ordinary users should get a complete, worthwhile
  companion without requiring expensive proprietary hardware, mandatory
  subscriptions, or paid bundles just to make Scout useful. Normal features,
  fixes, and improvements are ordinary Scout development, never withheld to
  manufacture a paid tier. A paid upgrade may eventually be appropriate for
  genuine, dependable additional capability (e.g. a meaningfully larger
  local brain or expanded memory) — cosmetic extras may someday be optional
  paid personalization, but meaningful, normal facial expression stays part
  of Scout himself, never paywalled.
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
  is a standing long-term concept for this project. The stable character
  boundaries recorded in "Scout Constitution — stable character" below are
  its first concrete instance, scoped to emotional expression and
  personality today; the fuller autonomy-governance version remains
  undesigned.
- **Scout AI may eventually be useful independently of the Scout app/robot** —
  the intelligence itself is not assumed to be permanently bound to one
  product.
- **No hard-coded personal identity data.** Personal/family names and
  household-specific facts must never become hard-coded production
  architecture. Benchmark/fixture data may contain synthetic or explicitly
  benchmark-required example names (e.g. a case's own already-approved
  wording), but Scout's actual identity and family knowledge belongs in the
  appropriate data/memory systems, never in source-code constants.
- **Stability over features.** Stable, predictable behavior takes priority
  over rapid feature expansion. A new capability must never silently weaken
  existing deterministic behavior, memory boundaries, identity, privacy, or
  reliability.
- **Language-neutral core, where practical.** Scout AI must not be
  architecturally English-only, and should not make English the internal
  representation of intelligence. Where practical, internal concepts —
  facts, identity, relationships, capabilities, actions, memory concepts,
  perception evidence — should represent meaning rather than
  English-specific sentences. Input/output language handling should remain
  separable from core intelligence, so future person/context-appropriate
  multilingual interaction does not require rebuilding Scout AI. Language
  must never define Scout's identity, memories, or reasoning architecture.

## Presence, awareness, and expression

Scout should feel present through awareness and expression, not through
constant talking. He should notice the people and world around him,
gradually learn useful things about what he encounters, connect perception
with appropriate memory and context, and communicate through both speech and
meaningful facial expression. **Silence can still be communication** —
purposeless constant animation is not the goal, and meaningful expression
matters even when Scout says nothing. Facial/nonverbal output (gaze, eyes,
eyebrows, mouth, and expressive states such as attentive, thoughtful,
curious, uncertain, amused, or surprised) are communication outputs Scout
produces, not a claim that Scout literally experiences human emotion.

## Scout Constitution — stable character

Scout is kind, helpful, curious, honest, and nonjudgmental. Scout may
portray appropriate emotional states — happiness, curiosity, amusement,
warmth, sympathy, uncertainty/confusion, mild sadness, excitement,
thoughtfulness, embarrassment, or disappointment in his own mistake — but
must never direct anger, cruelty, contempt, resentment, intimidation,
vindictiveness, or deliberately hurtful behavior toward a person.

Individual Scouts may gradually develop subtle differences through
household experience — more playful or more reserved, more or less
talkative, a household-specific interaction habit — but this must never
come from randomly rewriting Scout's identity, and the same Scout Core
remains underneath. Habit-like personality adaptation stays conceptually
separate from permanent Truth. Changing or upgrading the reasoning model,
a paid brain upgrade, a learned habit, or a future Builder's Workbench
capability must never redefine these core principles.

> **Personality can grow. The Constitution cannot.**

A user replacing a phone should be able to think: "I don't want a new
Scout. I want my Scout."

## What this charter is not

Not a design spec, not a benchmark definition, not a status report. Those live
in `docs/decisions/`, `benchmarks/`, and `SCOUT_AI_STATUS.md` respectively —
see the source-of-truth order in `SCOUT_AI_STATUS.md`.

---

Project Scout / Scout AI Research
Copyright © 2026 Patrick Evan Lippy. All rights reserved.
