# Technology Stack

## Decision

Use a simple two-tier architecture:

### Frontend
- React
- TypeScript
- Vite
- MapLibre GL JS
- GeoJSON
- Turf.js only for frontend geometry utilities where genuinely useful
- CSS or a lightweight utility approach already present in the repository

### Backend
- Python
- FastAPI

### Geospatial processing
- GeoPandas
- Shapely
- Rasterio when raster/CRS handling is required
- OpenCV for baseline computer-vision preprocessing

### AI
- Pretrained/inference-ready models where practical
- Deterministic CV fallbacks for reliability
- LLM/Gemini only for language-oriented tasks or optional image reasoning, not as the authoritative geometry engine

## Why this stack

MapLibre GL JS is a TypeScript/WebGL map library with support for GeoJSON and interactive map layers, making it appropriate for the central WebGIS experience. The current MapLibre documentation also provides examples for GeoJSON polygons, lines, layer interaction and performance optimization. citeturn552394search0turn552394search4

GeoJSON is the team's internal interchange format because it is easy for the React frontend to consume and easy for Python geospatial tooling to generate.

GeoPandas and Shapely are used for deterministic geospatial data manipulation and geometry operations.

FastAPI provides a small HTTP boundary between the React application and processing services.

## Database decision

Start without a heavy database dependency for the vertical-slice prototype.

Preferred order:
1. local/project JSON or GeoJSON fixtures for initial development
2. lightweight persistence if needed
3. PostgreSQL + PostGIS only if the team already has enough time/experience

Do not introduce PostGIS merely because it is a professional GIS technology.

## Map rendering

MapLibre GL JS.

Pin the package version used by the repository rather than relying on an unbounded `latest` version. Current MapLibre v6 is ESM-based and has bundler-specific worker setup considerations. citeturn552394search6

## Performance

Keep GeoJSON compact:
- remove unused properties
- reduce unnecessary coordinate precision
- simplify geometry only where acceptable
- avoid embedding huge datasets directly inside JavaScript

These are recommended MapLibre performance practices for large GeoJSON datasets. citeturn552394search1

## What we deliberately do not use initially

- microservices
- Kubernetes
- GraphQL
- Redis
- custom model training infrastructure
- complex message queues
- unnecessary UI frameworks
- a large GIS server stack

## Node/Python versions

Use the currently supported LTS/runtime versions already compatible with the installed environment at implementation time. Pin versions in lockfiles and avoid assuming an old Node version simply because an old README says so.

## Dependency rule

Every new dependency must answer:

1. What problem does it solve?
2. Could the existing stack solve it?
3. Is it reliable enough for a hackathon?
4. Does it increase build/deployment risk?

If the answer is weak, do not add it.
