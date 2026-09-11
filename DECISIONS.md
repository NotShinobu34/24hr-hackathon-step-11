# Architecture Decision Record

## ADR-001 — React + Vite

### Decision
Use React + Vite + TypeScript for the frontend.

### Why
- familiar component model
- fast development loop
- good fit for map-heavy SPA behavior
- easy integration with MapLibre

### Rejected
Next.js by default for this practice prototype because server rendering is not central to the GIS workspace.

---

## ADR-002 — MapLibre for WebGIS

### Decision
Use MapLibre GL JS.

### Why
- WebGL rendering
- TypeScript
- GeoJSON support
- rich interactive map/layer API

MapLibre's current documentation confirms GeoJSON sources/layers and interactive map APIs, along with performance guidance. citeturn552394search0turn552394search1

---

## ADR-003 — GeoJSON as API interchange

### Decision
Use GeoJSON FeatureCollection at the frontend/backend boundary.

### Why
- simple
- human-readable
- directly consumable by WebGIS
- compatible with Python geospatial tooling

---

## ADR-004 — Separate AI from GIS

### Decision
AI produces candidate features; deterministic GIS code validates and exports them.

### Why
This makes the system more reliable and explainable.

---

## ADR-005 — No custom model training initially

### Decision
Do not train a new deep-learning model during the initial implementation.

### Why
Team experience and time constraints make model training a poor 24-hour risk.

---

## ADR-006 — Fallback extraction

### Decision
Maintain a deterministic/demo fallback.

### Why
The product must remain demonstrable when model/API inference fails.

The UI must clearly represent fallback/demo behavior.

---

## ADR-007 — No database-first architecture

### Decision
Start with fixture/file persistence and introduce PostGIS only if justified.

### Why
The first objective is to establish a reliable vertical slice.

---

## ADR-008 — Topology is deterministic

### Decision
Use geometry libraries for topology rather than an LLM.

### Why
Geometry validity and spatial relationships are algorithmic problems.

---

## ADR-009 — Human review is part of the product

### Decision
AI results are preliminary and must support human review/edit/verification.

### Why
This aligns with the problem's ground-truthing and field-verification requirements and avoids overclaiming autonomous cadastral accuracy.
