# GeoParcel AI — AI-Assisted Urban Cadastral Mapping

This directory is the project specification pack for the GeoParcel AI practice project.

## Product goal

Build a credible prototype of an AI-assisted cadastral workflow:

**Imagery → AI/CV extraction → vectorization → topology validation → human review/edit → GIS-ready export**

The product is deliberately designed as a hackathon-scale prototype rather than a production cadastral system.

## Primary user

Surveyor / GIS operator / urban land-record technician.

## Core P0 capabilities

1. Load or upload high-resolution urban imagery.
2. Visualize imagery in a WebGIS interface.
3. Extract preliminary:
   - parcel candidates
   - building footprints
   - roads/access corridors
4. Represent results as editable GeoJSON-compatible vector features.
5. Show confidence scores.
6. Detect geometry/topology issues:
   - overlaps
   - self-intersections
   - duplicate geometries
   - invalid polygons
   - suspicious slivers/gaps where practical
7. Let a human review and edit features.
8. Compare AI output with ground-truth/reference layers.
9. Export GIS-ready results.

## P1 capabilities

- AI review queue
- field-verification workflow
- land-use classification
- project analytics
- AI-generated survey summary
- imagery/reference comparison

## P2 capabilities

- real GNSS/CORS integration
- advanced 3D/terrain
- multi-user collaboration
- custom model training
- advanced temporal change detection

## Repository rules

- `main` must remain runnable.
- Use feature branches.
- Keep services and UI separated.
- Define shared data contracts before parallel development.
- Prefer simple, testable architecture.
- Do not invent accuracy claims.
- The application must use phrases such as "preliminary", "AI-assisted", "candidate", and "survey review" where appropriate.

## Specification reading order

1. `PRODUCT_SPEC.md`
2. `TECH_STACK.md`
3. `ARCHITECTURE.md`
4. `DATABASE_SCHEMA.md`
5. `API_CONTRACT.md`
6. `USER_FLOWS.md`
7. `UI_SPEC.md`
8. `AI_PIPELINE.md`
9. `GIS_SPEC.md`
10. `TOPOLOGY_RULES.md`
11. `SECURITY.md`
12. `SEO.md`
13. `TESTING.md`
14. `AI_RULES.md`
15. `GIT_WORKFLOW.md`
16. `DECISIONS.md`
17. `ROADMAP.md`
18. Role prompt files

## Important

These documents are the source of truth for the practice project. If implementation conflicts with them, stop and reconcile the conflict instead of silently inventing a different architecture.
