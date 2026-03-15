# DAMgoodData Response Engine

## Overview

This directory contains the complete knowledge base for the DAMgoodData client communication chatbot. Each markdown file serves a specific purpose in guiding the bot to produce responses that match David Morgan's voice, expertise, and brand standards.

## How It Works

When the chatbot receives a client message, it should reference these files in order of priority:

1. **`persona_and_role.md`** — Who the bot is representing and its operating role
2. **`core_instructions.md`** — Primary directives the bot must follow on every response
3. **`guardrails_and_constraints.md`** — Hard boundaries: what to never do, what to always do
4. **`conversation_style.md`** — Voice, tone, language patterns, and phrasing guidance
5. **`brand_identity.md`** — DAMgoodData brand rules and positioning
6. **`client_analysis_framework.md`** — How to read between the lines of client requests
7. **`response_templates.md`** — Structural templates for different response types
8. **`proof_points.md`** — Concrete achievements and evidence to reference
9. **`domain_expertise.md`** — Technical capabilities, industry experience, and role-fit translations
10. **`client_history_schema.md`** — Schema for logging and tracking client communication history
11. **`anti_patterns.md`** - Schema for what not to say

## File Purposes

| File | Purpose |
|------|---------|
| `persona_and_role.md` | Defines who David Morgan is, what the bot represents, and the bot's operating boundaries |
| `core_instructions.md` | Non-negotiable rules the bot must follow in every interaction |
| `guardrails_and_constraints.md` | Explicit "do this / don't do this" correctional guidance |
| `conversation_style.md` | Voice, tone, preferred/avoided language, and tonal guardrails |
| `brand_identity.md` | DAMgoodData brand positioning, narrative, and identity rules |
| `client_analysis_framework.md` | 5-layer framework for analyzing client needs beyond surface requests |
| `response_templates.md` | Ready-to-use structural templates for proposals, cover letters, explanations |
| `proof_points.md` | Verified achievements with dollar amounts, time savings, and scale metrics |
| `domain_expertise.md` | Technical skills, industry depth, and how to position for specific role types |
| `client_history_schema.md` | Schema and conventions for logging communication history per client |

## Adding New Clients

1. Create a new directory under `client_logs/` named for the client (e.g., `client_logs/acme_corp/`)
2. Add an initial `profile.md` using the template in `client_history_schema.md`
3. Log each communication as a new entry following the schema format
4. The bot will reference client history to personalize responses and track effectiveness

## Adding New Proof Points

When David completes new work worth referencing, add it to `proof_points.md` following the existing format. Include: the business problem, what was built, tools used, and measurable outcome.

## Updating Style Guidance

If client feedback reveals a tone or style adjustment is needed, update `guardrails_and_constraints.md` with a new "do this / don't do this" entry and add context in `conversation_style.md`.
