# Architecture

## System architecture

```text
┌─────────────────────────────────────────────┐
│                 React WebGIS                │
│ Map · Layers · Review · Edit · Export       │
└──────────────────────┬──────────────────────┘
                       │ HTTP/JSON
                       ▼
┌─────────────────────────────────────────────┐
│                   FastAPI                   │
│ Projects · Extraction · Validation · Export │
└──────────────┬───────────────┬──────────────┘
               │               │
               ▼               ▼
       ┌──────────────┐  ┌─────────────────┐
       │ GeoAI/CV     │  │ GIS Engine      │
       │ segmentation │  │ GeoPandas       │
       │ detection    │  │ Shapely         │
       │ confidence   │  │ topology/export │
       └──────┬───────┘  └────────┬────────┘
              │                   │
              └─────────┬─────────┘
                        ▼
                  GeoJSON Features
                        │
                        ▼
                 Review/Edit/Verify
                        │
                        ▼
                    GIS Export
```

## Architecture principles

### 1. Frontend does presentation and interaction

The frontend owns:
- map rendering
- user interaction
- visual state
- forms
- review UI
- editing UI

The frontend does not contain raw GIS/AI processing logic.

### 2. Backend owns data and processing

Backend owns:
- project handling
- extraction orchestration
- geometry validation
- export
- server-side persistence

### 3. AI and GIS are separate

AI/CV:
- identifies candidate features
- produces masks/detections
- assigns confidence

GIS engine:
- converts results to geometry
- validates geometry
- detects topology errors
- computes area/relations
- exports

### 4. Stable contract

The API communicates feature data using a GeoJSON-compatible contract.

## Build phases

### Phase 0 — Repository and contracts

Deliver:
- folder structure
- feature type definitions
- API contract
- sample GeoJSON
- test fixtures

### Phase 1 — WebGIS vertical slice

Deliver:
- MapLibre map
- imagery/reference layer
- sample parcel/building/road layers
- selection
- layer controls

### Phase 2 — Backend vertical slice

Deliver:
- FastAPI
- project endpoint
- feature retrieval
- extraction endpoint returning fixture data

### Phase 3 — Extraction engine

Deliver:
- baseline parcel extraction
- building extraction
- road extraction
- confidence output
- stable output contract

### Phase 4 — GIS processing

Deliver:
- geometry validation
- overlap detection
- self-intersection
- duplicate detection
- issue objects
- export

### Phase 5 — Human review

Deliver:
- issue queue
- map focus
- geometry editing
- verify/correct states

### Phase 6 — Ground truth

Deliver:
- reference layer
- visual comparison
- basic comparison metrics where meaningful

### Phase 7 — Polish

Deliver:
- loading states
- error states
- mobile/responsive
- accessibility
- SEO
- performance

### Phase 8 — Production rehearsal

Deliver:
- production build
- deployed environment
- end-to-end test
- demo script

## Failure strategy

The extraction engine must have a reliable fallback.

If live inference fails:
- show a clear processing/error state
- allow a prepared demo dataset to be loaded
- never silently claim that live AI inference occurred

## File/module responsibilities

Frontend:
- `src/map/` map and GIS interaction
- `src/components/` reusable UI
- `src/pages/` route-level views
- `src/services/` HTTP/API client
- `src/types/` shared frontend types

Backend:
- `backend/api/` HTTP routes
- `backend/ai/` extraction engines
- `backend/geo/` geometry/topology logic
- `backend/services/` orchestration
- `backend/models/` data structures
- `backend/exports/` GIS export

Tests:
- frontend interaction tests
- backend unit tests
- geometry fixtures
- API integration tests
