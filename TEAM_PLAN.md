# Team Plan

## Member 1 — You

Role:
**Tech Lead + WebGIS + Integration**

Own:
- architecture
- shared contracts
- MapLibre
- layer manager
- map interaction
- selection
- geometry editing integration
- merge/review
- final deployment
- demo

Do not:
- spend the entire project doing backend
- redesign every part of the app
- let the main branch become unstable

## Member 2

Role:
**Computer Vision / GeoAI**

Own:
- image preprocessing
- parcel extraction
- building extraction
- road extraction
- confidence
- extraction fixtures/fallback

Do not:
- own React
- build database infrastructure
- train custom models from scratch

## Member 3

Role:
**GIS Backend / Topology**

Own:
- FastAPI
- GeoJSON services
- Shapely
- GeoPandas
- topology validation
- export
- CRS handling

Do not:
- invent complex database architecture
- use AI for deterministic geometry operations

## Member 4

Role:
**UX + QA + SEO**

Own:
- AI panel
- review queue
- project metrics
- accessibility
- responsive behavior
- SEO
- Lighthouse
- automated/manual QA
- final polish

Do not:
- add major features during final QA
- change API contracts without coordination

## Parallel workflow

```text
                 SHARED CONTRACT
                       │
     ┌─────────────────┼─────────────────┐
     ▼                 ▼                 ▼
   YOU              MEMBER 2          MEMBER 3
  WebGIS            GeoAI/CV          GIS/API
     │                 │                 │
     └─────────────────┼─────────────────┘
                       ▼
                  MEMBER 4
                 UX / QA / SEO
                       │
                       ▼
                  INTEGRATION
                       │
                       ▼
               END-TO-END TEST
                       │
                       ▼
                    POLISH
                       │
                       ▼
                   DEPLOY
```

## Rule

Nobody waits for another teammate to finish.

Frontend uses mock data.
Backend uses contracts.
QA tests early.
Integration happens continuously.
