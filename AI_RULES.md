# AI Agent Rules

## Purpose

AI agents are implementation accelerators, not product owners.

Humans decide:
- scope
- architecture
- priorities
- product claims
- accuracy claims
- final UX

## Repository rule

Before changing code:
1. inspect repository
2. identify relevant files
3. read existing conventions
4. understand dependencies
5. make the smallest appropriate change

## Never

- rewrite the entire repository without explicit need
- delete working functionality casually
- create duplicate components
- introduce unnecessary frameworks
- change API contracts silently
- fabricate scientific results
- invent data provenance
- claim model accuracy that was not measured
- expose secrets
- remove tests to make builds pass
- disable validation merely to hide errors

## GIS-specific rule

Never guess:
- CRS
- coordinate order
- unit conversions
- geometry semantics

When uncertain:
- inspect metadata
- use documented conventions
- add a visible limitation if necessary

## AI/ML-specific rule

Prefer:
- pretrained inference
- explainable heuristics
- deterministic geometry processing
- fixture-based development

Avoid:
- training a custom model from scratch under time pressure
- using an LLM for deterministic geometry calculations
- pretending an LLM prediction is cadastral truth

## Agent task format

Every agent task should specify:

```text
Context
Goal
Files allowed
Files forbidden
Acceptance criteria
Tests required
Expected output
```

## Before completion

Agent must report:
- files changed
- behavior added
- tests run
- failures
- known limitations

## Human approval

Require human review before:
- architecture changes
- dependency additions
- database schema breaking changes
- API contract changes
- deleting major code
- changing product claims

## Agent collaboration

Agents must avoid editing the same files simultaneously.

Use small feature branches.

Synchronize shared contracts before implementation.

## Fallback rule

If an external API/model/service fails, fall back to deterministic/fixture behavior where the product can still truthfully demonstrate its workflow.

Never conceal the fallback.
