# Datasets & Ground Truth Specification

## Purpose

This document catalogs the sample datasets, benchmarks, and reference layers used by GeoParcel AI during development, benchmarking, and hackathon presentation.

---

## 1. Primary Datasets

### Dataset 1: Ward 12 Urban Cadastral Pilot (Primary Demo Dataset)
- **Source**: OpenCities AI / Aerial Urban Survey Pilot (Curated Municipal Drone Survey)
- **License**: Creative Commons Attribution 4.0 International (CC-BY 4.0)
- **Source CRS**: `EPSG:32643` (WGS 84 / UTM Zone 43N - metric projected system)
- **Target WebGIS CRS**: `EPSG:4326` (WGS 84 geographic latitude/longitude for GeoJSON exchange)
- **Resolution**: 0.08 meters Ground Sample Distance (GSD)
- **Format**: GeoTIFF (RGB orthomosaic) + accompanying GeoJSON vector annotations
- **Purpose**:
  - Source raster for live extraction demonstration (`sample_ortho.png` / `.tif`).
  - Contains mixed residential and commercial parcels with dense roof boundaries and access roads.
- **Provenance & Citation**:
  - Derived from open high-resolution aerial mapping initiatives for urban tenure formalization.

### Dataset 2: Ground-Truth Cadastral Reference (Ward 12 Truth Layer)
- **Source**: Municipal Cadastral Survey Office / Digitized Ground Truth
- **License**: CC-BY 4.0
- **Source CRS**: `EPSG:32643`
- **Target WebGIS CRS**: `EPSG:4326`
- **Feature Count**: 48 parcels, 52 buildings, 8 road centerlines
- **Attributes**: `parcel_id`, `survey_number`, `registered_area_m2`, `owner_type` (sanitized/anonymized), `zone`
- **Purpose**:
  - Used in the WebGIS Ground Truth comparison slider to visually evaluate AI-extracted candidate boundaries against official field-verified boundaries.
  - Generates IoU (Intersection-over-Union) and boundary displacement metrics in the review queue.

### Dataset 3: Synthetic Topology Stress Test Collection
- **Source**: GeoParcel AI Internal Test Suite
- **License**: MIT (GeoParcel AI project asset)
- **Source CRS**: `EPSG:4326`
- **Features**:
  - `case_overlap_01`: Two parcels with 8.4 m² intentional overlap.
  - `case_bowtie_02`: Parcel polygon containing an internal self-intersection (twisted boundary).
  - `case_sliver_03`: Tiny micro-polygon with area 0.32 m² (spurious sliver between parcels).
  - `case_duplicate_04`: Two identical polygon geometries with different feature IDs.
  - `case_shared_edge_05`: Two legitimate adjacent parcels sharing an exact border (control test: should NOT flag as overlap).
- **Purpose**:
  - Automated unit and integration testing of `backend/geo/topology.py`.
  - Immediate verification of the reviewer correction workflow.

---

## 2. Dataset Management Rules

1. **Explicit CRS Documentation**:
   - Every dataset registered in the repository or uploaded to `/api/projects/{id}/assets` must explicitly specify its source CRS.
   - If an asset is provided without CRS metadata, it is flagged as `CRS_UNKNOWN` and metric computations are disabled until assigned.
2. **Data Anonymization**:
   - No personally identifiable information (PII) such as personal citizen names, telephone numbers, or tax assessment IDs may appear in sample datasets.
   - All parcel identifiers must follow sanitized codes (e.g. `P-101`, `P-102`).
3. **Storage Location**:
   - Production/sample fixtures reside in `/fixtures/imagery/` and `/fixtures/geojson/`.
   - Temporary uploads reside in a configurable local data directory (e.g. `data/uploads/`), isolated from version control.
