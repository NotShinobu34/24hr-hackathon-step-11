# GIS Specification

## GIS responsibilities

The geospatial layer owns:
- geometry representation
- CRS metadata
- geometry validity
- spatial relationships
- measurements
- vector export

## Data format

Internal API format:

**GeoJSON FeatureCollection**

## Geometry types

### Parcel
Polygon or MultiPolygon

### Building
Polygon or MultiPolygon

### Road/access
LineString or MultiLineString, or polygon where the extraction representation requires it

## CRS

Every dataset must carry CRS metadata when known.

Rules:
- never silently assume CRS
- do not mix coordinate systems without explicit transformation
- document input/output CRS
- validate transformed geometry

## Geometry lifecycle

```text
AI mask/detection
 ↓
vectorization
 ↓
simplification
 ↓
validation
 ↓
editable geometry
 ↓
verification
 ↓
export
```

## Measurements

Where projected CRS is available, use it for metric area/length calculations.

Do not report physically meaningful area/length values from raw degree coordinates without an appropriate projection.

## Ground truth

Ground truth is a reference dataset.

It must be visually distinguishable from AI output.

## Provenance

Every feature should maintain:

```text
source = ai | ground_truth | manual
```

## Export

Minimum:
- GeoJSON

Optional:
- GeoPackage

Do not add additional export formats unless they can be generated reliably and tested.

## Performance

For large datasets:
- simplify geometry appropriately
- avoid unnecessary feature properties
- load GeoJSON as external data when practical
- consider tiling only if dataset size genuinely requires it

MapLibre's current documentation recommends reducing GeoJSON size and considering simplification, chunking, streaming or vector tiles for larger datasets. citeturn552394search1
