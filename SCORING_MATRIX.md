# Hackathon Scoring Matrix & Requirements Traceability

## Purpose

To maximize competitive scoring, every problem-statement requirement is directly mapped to a software deliverable, an accountable team member, verifiable evidence, and evaluation criteria.

---

## Traceability Matrix

| Requirement | Implementation | Owner | Priority | Status | Verification / Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **High-Resolution Imagery Ingestion** | Support orthophoto/drone GeoTIFF/PNG with spatial metadata and CRS preservation. | Member 1 & 2 | P0 | Planned | Map renders raster layer with correct geographic bounds. |
| **Parcel, Building & Road Extraction** | Multi-layer candidate extraction with modular engine (`cv_baseline` / `demo_fixture`). | Member 2 | P0 | Planned | Features returned as GeoJSON FeatureCollection with `featureType`. |
| **Transparent Confidence Scoring** | Explainable heuristic & inference certainty values [0.0–1.0]. | Member 2 | P0 | Planned | Feature inspector & extraction summary expose confidence scores. |
| **Deterministic Topology Validation** | Shapely engine detecting invalid polygons, self-intersections, overlaps, duplicates, slivers. | Member 3 | P0 | Planned | Unit tests in `backend/tests/test_topology.py` passing; issue objects generated. |
| **Configurable Topology Tolerances** | Prototype parameters for overlap area ($m^2$) and sliver threshold ($m^2$). | Member 3 | P0 | Planned | Configurable via API and settings; documented as prototype limits. |
| **Interactive WebGIS Interface** | MapLibre GL JS workstation with layer toggles, opacity sliders, feature selection. | Member 1 | P0 | Planned | Smooth WebGL rendering; distinct symbology for all layers. |
| **Human-in-the-Loop Boundary Editing** | Interactive vertex drag-and-drop boundary editor for flagged parcels. | Member 1 | P0 | Planned | Surveyor adjusts vertex; PATCH request sent; geometry updated. |
| **Revalidation Workflow** | Instant topology re-check on edited geometry to clear flags. | Member 1 & 3 | P0 | Planned | Issue status transitions from open to resolved; count decreases. |
| **Ground-Truth Comparison** | Reference cadastral layer toggle with opacity comparison slider. | Member 1 & 4 | P1 | Planned | Visual overlay demonstrating AI vs ground truth alignment. |
| **Survey Review Queue** | Prioritized queue sorting features by severity, confidence, and status. | Member 4 | P1 | Planned | One-click zoom-to-issue; filter by status (`review`, `corrected`, `verified`). |
| **Feature & Asset Provenance** | Immutable provenance metadata (`source`, `sourceAssetId`, `processingMode`, `status`). | Member 3 | P0 | Planned | GeoJSON properties contain full audit trail and mode badges. |
| **Asynchronous Job Telemetry** | `ProcessingJob` model with status polling (`queued`, `processing`, `completed`). | Member 3 & 4 | P0 | Planned | Animated progress bar during extraction; no frozen HTTP threads. |
| **GIS-Ready Export** | RFC 7946 GeoJSON export containing geometries and survey attributes. | Member 3 | P0 | Planned | Downloadable `.geojson` verified in QGIS / geojson.io. |
| **SEO & Crawlability** | Semantic HTML5, unique meta tags, OpenGraph preview, `robots.txt`, `sitemap.xml`. | Member 4 | P1 | Planned | Valid `robots.txt` & `sitemap.xml`; Lighthouse SEO score $\ge 90$. |
| **Security & Resiliency** | Safe file parsing, CORS lockdown, error masking without stack traces. | Member 3 | P1 | Planned | Request body validation via Pydantic; sanitized error payloads. |

---

## Evaluation Checklist for Judges

1. **Architecture Coherence**: Frontend and backend are cleanly separated with stable JSON contracts.
2. **GIS Integrity**: Metric calculations are performed in a projected coordinate system; GeoJSON strictly adheres to RFC 7946.
3. **No Hallucinations / Scientific Honesty**: System makes zero claims of 100% legal accuracy; clearly denotes AI candidates vs human verification.
4. **Resilience**: Instantaneous demo fixture fallback ensures zero crashes during live demonstration.
