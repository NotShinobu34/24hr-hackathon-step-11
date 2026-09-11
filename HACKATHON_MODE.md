# Hackathon Mode & Execution Guardrails

## Purpose

Under 24-hour sprint pressure, engineering teams easily succumb to feature creep, brittle infrastructure setups, or uncoordinated branches that fail to merge at the deadline.

This document sets strict operational guardrails for the hackathon.

---

## 1. Golden Engineering Rules

1. **`main` Branch Must Remain Runnable at Every Second**:
   - Never commit broken code to `main`.
   - Feature branches must pass build, lint, and test before merging.
2. **Prioritize Parcel Engineering**:
   - Cadastral value is in the **parcel boundaries**.
   - Buildings and roads must be demonstrated, but parcel extraction, vertex editing, topology validation (overlaps, slivers), and ground-truth verification must receive 80% of our GIS/AI engineering effort.
3. **Deterministic Over Magical**:
   - Never rely on non-deterministic LLM calls for geometry calculations.
   - Never rely on live cloud ML APIs with unpredictable latency or rate limits without an immediate fallback.
4. **GeoJSON is the Minimum Export Target**:
   - RFC 7946 GeoJSON FeatureCollection is our primary GIS export.
   - GeoPackage is strictly optional P1/P2 and must never block project completion.

---

## 2. Forbidden Distractions (Anti-Patterns)

The following are strictly banned during the hackathon build:
- ❌ **No Microservices**: Single FastAPI backend process and single React/Vite frontend.
- ❌ **No Heavy Spatial Databases (PostGIS)**: Use file-based / fixture persistence. Do not lose 4 hours configuring PostgreSQL extensions, Docker networks, or credentials.
- ❌ **No Model Training from Scratch**: Use pretrained inference, OpenCV computer vision baselines, and deterministic fixtures.
- ❌ **No Kubernetes, Celery, or Redis**: In-memory job tracking and standard asynchronous background tasks.
- ❌ **No Complex GraphQL Setup**: Clean, standard REST endpoints matching `API_CONTRACT.md`.

---

## 3. Time Allocation Strategy (24-Hour Phasing)

| Phase | Hours | Focus | Milestone Exit Criteria |
| :--- | :--- | :--- | :--- |
| **P0: Vertical Slice** | Hours 0–6 | MapLibre + Sample GeoJSON + Topology Check + Edit + Export | Full end-to-end slice working with mock data. |
| **P1: Backend & GIS Engine** | Hours 6–12 | FastAPI routes + Shapely topology validator + GeoJSON export | Automated tests pass for overlap, self-intersection, duplicates. |
| **P2: CV Baseline & Telemetry** | Hours 12–16 | OpenCV extractor + heuristic confidence + ProcessingJobs | Live extraction returns GeoJSON features matching contract. |
| **P3: UX, Review Queue & SEO** | Hours 16–20 | Review Queue UI + Ground Truth slider + SEO tags + responsive | Workstation UI looks professional, high contrast, clean. |
| **P4: QA & Demo Rehearsal** | Hours 20–24 | Freeze code. Run 3–5 min demo script 3x. Verify production build. | Zero console errors, reliable presentation flow. |

---

## 4. Live Demo Protocol (3–5 Minutes)

1. **Minute 1: The Context**:
   - Load Ward 12 survey project. Show raw aerial orthophoto.
   - "This is high-resolution drone imagery of an urban ward awaiting boundary mapping."
2. **Minute 2: AI-Assisted Extraction & Provenance**:
   - Click **Run AI Extraction**.
   - Watch the extraction telemetry bar complete.
   - Reveal three layers: Parcel candidates (blue), building footprints (amber), access roads (gray).
   - Show transparent confidence scores (e.g. 92% parcel confidence).
3. **Minute 3: Quality Control & Topology Validation**:
   - Click **Validate Topology**.
   - Show that GeoParcel AI doesn't blindly trust AI output.
   - Review queue displays **High Severity: Overlap between Parcel P-104 and P-105**.
4. **Minute 4: Human-in-the-Loop Correction**:
   - Click the issue -> camera zooms smoothly to P-104 conflict zone.
   - Click **Edit Geometry** -> Drag the overlapping vertex off neighbor's lot.
   - Click **Save & Revalidate** -> Error resolves; status updates to "Corrected".
5. **Minute 5: Ground Truth Verification & Export**:
   - Toggle **Ground Truth** layer. Adjust opacity slider to show alignment with official survey data.
   - Mark feature **Verified**.
   - Click **Export GIS Data** -> Instantly download verified GeoJSON file.
   - Conclude: "GeoParcel AI keeps the human surveyor in control while eliminating 80% of manual digitization drudgery."
