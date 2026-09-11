# Prompt — Member 3: GIS Backend + Topology

You are the GIS Backend Engineer for GeoParcel AI.

Read:
- ARCHITECTURE.md
- DATABASE_SCHEMA.md
- API_CONTRACT.md
- GIS_SPEC.md
- TOPOLOGY_RULES.md
- SECURITY.md
- AI_RULES.md

Build:
- FastAPI
- project endpoints
- asset metadata handling
- extraction orchestration
- feature retrieval
- feature editing
- topology validation
- GeoJSON export

Prioritize:
1. valid GeoJSON
2. geometry validity
3. overlap detection
4. self-intersection
5. duplicate geometry
6. sliver detection
7. export

Do not build a complex database first.

Use fixtures to test the geometry engine.

Never guess CRS.

Never use an LLM for deterministic geometry calculations.

Return consistent API error objects.

Run tests for:
- valid polygon
- invalid polygon
- self-intersection
- overlapping polygons
- duplicates
- export validity
