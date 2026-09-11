# GeoParcel AI — Documentation Index

Welcome to the comprehensive documentation suite for **GeoParcel AI**. All specifications are preserved both at the repository root and indexed here under logical categories.

---

## 1. Product & Domain Specifications
- [PRODUCT_SPEC.md](../PRODUCT_SPEC.md) — Product vision, personas, core workflows, P0/P1/P2 criteria.
- [USER_FLOWS.md](../USER_FLOWS.md) — Detailed step-by-step user journeys and failure handling.
- [UI_SPEC.md](../UI_SPEC.md) — Desktop GIS workstation layout, layer styling, review queue design.
- [SEO.md](../SEO.md) — Public landing metadata, semantic HTML hierarchy, crawlability specs.
- [DEMO_SCRIPT.md](../DEMO_SCRIPT.md) — 3–5 minute live presentation script and judging flow.

---

## 2. Technical Architecture & Data Models
- [TECH_STACK.md](../TECH_STACK.md) — Decision rationale for React, Vite, MapLibre, FastAPI, Shapely, OpenCV.
- [ARCHITECTURE.md](../ARCHITECTURE.md) — System flow diagram, component separation, phase roadmap.
- [DECISIONS.md](../DECISIONS.md) — Architecture Decision Records (ADR-001 through ADR-009).
- [DATABASE_SCHEMA.md](../DATABASE_SCHEMA.md) — Project, SourceAsset, Feature, TopologyIssue, Verification entities.
- [API_CONTRACT.md](../API_CONTRACT.md) — REST endpoints, request/response JSON schemas, error shapes.
- [PROCESSING_JOBS.md](../PROCESSING_JOBS.md) — Asynchronous job model, status polling, and execution lifecycle.

---

## 3. GIS & Computer Vision Engineering
- [GIS_SPEC.md](../GIS_SPEC.md) — CRS rules, geometry lifecycle, metric projections, export standards.
- [TOPOLOGY_RULES.md](../TOPOLOGY_RULES.md) — Deterministic topology validation rules (overlaps, bowties, slivers).
- [AI_PIPELINE.md](../AI_PIPELINE.md) — Extraction stages, OpenCV baseline, modular inference adapters.
- [PROVENANCE.md](../PROVENANCE.md) — Feature-level audit trails, extraction modes (`model_inference`, `cv_baseline`, `demo_fixture`).
- [DATASETS.md](../DATASETS.md) — Catalog of demo orthophotos, ground-truth layers, and synthetic test cases.
- [DEMO_DATA_RULES.md](../DEMO_DATA_RULES.md) — Transparent presentation standards and guaranteed fallback protocols.

---

## 4. Engineering Operations, Quality & Team
- [TEAM_PLAN.md](../TEAM_PLAN.md) — Member 1 through 4 role assignments, parallel workstreams, contract-first boundaries.
- [HACKATHON_MODE.md](../HACKATHON_MODE.md) — Operational sprint guardrails, anti-patterns, time allocation.
- [SCORING_MATRIX.md](../SCORING_MATRIX.md) — Traceability matrix mapping problem statements to code and evidence.
- [TESTING.md](../TESTING.md) — Testing pyramid, unit test cases, integration gates, Lighthouse criteria.
- [SECURITY.md](../SECURITY.md) — Input validation, file upload sanitization, secret management.
- [ENVIRONMENT.md](../ENVIRONMENT.md) — Runtime versions, backend/frontend environment variables.
- [DEPLOYMENT.md](../DEPLOYMENT.md) — Static frontend + ASGI container deployment guide.
- [OBSERVABILITY.md](../OBSERVABILITY.md) — Health check endpoint, structured JSON logs, frontend error boundaries.
- [GIT_WORKFLOW.md](../GIT_WORKFLOW.md) — Branch naming, pull request gates, commit style.
- [AI_RULES.md](../AI_RULES.md) — Behavioral constraints for AI coding agents.
- [AGENT_HANDOFF.md](../AGENT_HANDOFF.md) — Handoff protocol between agent sessions and team members.
- [ROADMAP.md](../ROADMAP.md) — Phase 0 to Phase 10 execution timeline.

---

## 5. Agent Role Prompts
- [PROMPT_MEM1.md](../PROMPT_MEM1.md) — Member 1: Tech Lead + WebGIS + Integration.
- [PROMPT_MEM2.md](../PROMPT_MEM2.md) — Member 2: Computer Vision / GeoAI.
- [PROMPT_MEM3.md](../PROMPT_MEM3.md) — Member 3: GIS Backend + Topology + Export.
- [PROMPT_MEM4.md](../PROMPT_MEM4.md) — Member 4: UX + QA + SEO.
- [PROMPT_INTEGRATION.md](../PROMPT_INTEGRATION.md) — Senior Integration Reviewer.
- [PROMPT_FINAL_AUDIT.md](../PROMPT_FINAL_AUDIT.md) — Final Hackathon Audit Agent.
