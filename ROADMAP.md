# Roadmap

## Phase 0 — Setup

- repository
- Python environment
- React/Vite frontend
- FastAPI
- MapLibre
- fixtures
- shared types
- API contract
- Git workflow

## Phase 1 — One vertical slice

Goal:

**sample imagery → sample GeoJSON → MapLibre → select feature → feature panel**

Do not continue until this works.

## Phase 2 — Backend boundary

Implement:
- projects
- assets
- extraction job
- features

Use fixture data.

## Phase 3 — Three feature types

Implement output for:
- parcels
- buildings
- roads

Start with deterministic/fixture processing if necessary.

## Phase 4 — Topology

Implement:
- invalid geometry
- self-intersection
- overlaps
- duplicates
- slivers

## Phase 5 — Review/edit

Implement:
- issue queue
- zoom-to-issue
- feature edit
- revalidation
- verification state

## Phase 6 — Ground truth

Implement:
- reference layer
- comparison
- basic meaningful metrics

## Phase 7 — AI enhancement

Replace selected fixture extractors with reliable pretrained/model/CV pipelines where available.

## Phase 8 — Export

Minimum:
- GeoJSON

Optional:
- GeoPackage

## Phase 9 — Polish

- UI polish
- responsive
- accessibility
- SEO
- performance
- errors
- loading
- empty states

## Phase 10 — Competition rehearsal

Run the entire project under a simulated 24-hour constraint.

## Definition of progress

A phase is complete only when:
- implementation works
- tests pass
- integration is stable
- no known P0 issue remains
