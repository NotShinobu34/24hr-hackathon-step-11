# Product Specification

## Product

**GeoParcel AI — AI-Assisted Urban Cadastral Mapping & Field Verification**

## Problem

Urban parcel mapping often requires manual interpretation of drone/orthorectified imagery and field verification. Dense settlements and irregular geometries increase the effort required to extract parcel boundaries, buildings and roads and to validate resulting geometry.

## Product promise

Help a surveyor move from imagery to a **preliminary, reviewable cadastral map** faster.

The system is not a legal cadastral authority and does not replace field verification.

## Primary personas

### Surveyor / GIS operator

Needs:
- fast feature extraction
- map visibility
- confidence information
- issue detection
- geometry editing
- verification
- export

### Project reviewer

Needs:
- project-level statistics
- quality indicators
- review queue
- ground-truth comparison

## Core workflow

1. Create/open survey project.
2. Load imagery.
3. Inspect source data.
4. Run AI-assisted extraction.
5. Render parcel/building/road layers.
6. Review confidence.
7. Run topology validation.
8. Open issues.
9. Edit geometry.
10. Revalidate.
11. Compare with ground truth if available.
12. Mark features verified/corrected.
13. Export GIS-ready data.

## P0 acceptance criteria

### Imagery
- A demo/sample imagery project can be loaded.
- The user can identify the survey area.
- Processing states are visible.

### Extraction
- Parcel candidates are returned.
- Building footprints are returned.
- Roads/access corridors are returned.
- Output includes confidence.
- Output follows the shared feature contract.

### WebGIS
- Layers can be toggled.
- Features are selectable.
- Selected features expose metadata.
- Issues can be located on the map.
- Geometry can be edited at least in a controlled prototype workflow.

### Validation
- Invalid polygons can be identified.
- Overlapping parcels can be identified.
- Self-intersections can be identified.
- Duplicate geometries can be identified.
- Issues are connected to feature IDs.

### Export
- Validated features can be exported as GeoJSON.
- Export contains geometry and essential attributes.

## P1 acceptance criteria

- Ground-truth layer can be toggled and visually compared.
- Review queue prioritizes low-confidence or problematic features.
- Field verification state can be stored.
- Land-use classification is visible where implemented.

## Non-goals

- Legal cadastral certification.
- Guaranteed survey accuracy.
- Fully autonomous official land-record generation.
- Nationwide production deployment.
- Full CORS infrastructure.
- Training a custom deep-learning model during the initial build.

## Demo success criteria

Within a few minutes a judge should see:

**source imagery → extraction → three feature layers → confidence → detected topology issue → human correction → revalidation → ground-truth comparison → GIS export**

## Product language

Preferred:
- AI-assisted
- preliminary cadastral map
- candidate feature
- confidence
- survey review
- ground truth
- validation
- field verification

Avoid:
- 100% accurate
- legally valid cadastral map
- fully autonomous surveying
- guaranteed boundary correctness
