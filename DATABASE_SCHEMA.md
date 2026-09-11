# Database / Data Schema

## Important architecture note

The practice project should not begin with a complex production database.

The canonical domain model must be defined first. Persistence can begin with fixtures/files and later move to PostgreSQL/PostGIS if justified.

## Entities

### Project

```text
id: string
name: string
description: string | null
createdAt: timestamp
updatedAt: timestamp
status: draft | processing | review | verified | exported
crs: string | null
```

### SourceAsset

```text
id: string
projectId: string
assetType: ori | drone | dsm | dtm | gis_parcel | ground_truth
name: string
uri: string
mimeType: string
crs: string | null
width: number | null
height: number | null
metadata: object
createdAt: timestamp
```

### Feature

```text
id: string
projectId: string
featureType: parcel | building | road | land_use
geometry: GeoJSON Geometry
confidence: number | null
source: ai | ground_truth | manual
status: detected | review | corrected | verified
properties: object
createdAt: timestamp
updatedAt: timestamp
```

### TopologyIssue

```text
id: string
projectId: string
featureId: string
relatedFeatureId: string | null
issueType: overlap | self_intersection | duplicate | invalid_geometry | sliver | gap
severity: low | medium | high
message: string
resolved: boolean
createdAt: timestamp
resolvedAt: timestamp | null
```

### Verification

```text
id: string
featureId: string
verifierId: string | null
status: pending | verified | rejected | needs_edit
note: string | null
referenceSourceId: string | null
createdAt: timestamp
updatedAt: timestamp
```

### ExportJob

```text
id: string
projectId: string
format: geojson | geopackage
status: queued | processing | completed | failed
uri: string | null
createdAt: timestamp
completedAt: timestamp | null
```

## Relationships

```text
Project
 ├── SourceAssets
 ├── Features
 │     ├── TopologyIssues
 │     └── Verifications
 └── ExportJobs
```

## Geometry rules

- Store geometry as GeoJSON-compatible geometry at the API boundary.
- Store CRS metadata explicitly.
- Never silently assume CRS.
- Geometry validation must happen before export.
- Preserve source/provenance metadata.

## Data ownership

The source of truth for extracted feature state is the backend/service layer.

UI state may temporarily contain unsaved edits, but it must clearly distinguish:
- saved
- unsaved
- verified
- invalid
