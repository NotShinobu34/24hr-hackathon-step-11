# API Contract

Base path:

```text
/api
```

All JSON responses should use predictable shapes.

## POST /projects

Create a project.

Request:

```json
{
  "name": "Ward 12 Survey",
  "description": "Urban cadastral pilot"
}
```

Response:

```json
{
  "project": {
    "id": "project-001",
    "name": "Ward 12 Survey",
    "status": "draft"
  }
}
```

## GET /projects/{projectId}

Return project metadata and summary.

## POST /projects/{projectId}/assets

Register/upload a project asset.

Request metadata must include:
- asset type
- filename
- optional CRS

## POST /projects/{projectId}/extract

Start extraction.

Request:

```json
{
  "assetId": "asset-001",
  "features": ["parcel", "building", "road"]
}
```

Response:

```json
{
  "jobId": "job-001",
  "status": "queued"
}
```

## GET /projects/{projectId}/extract/{jobId}

Return processing status.

Possible:

```text
queued
processing
completed
failed
```

Completed response:

```json
{
  "jobId": "job-001",
  "status": "completed",
  "summary": {
    "parcels": 127,
    "buildings": 84,
    "roads": 19
  }
}
```

## GET /projects/{projectId}/features

Query features.

Optional filters:
- featureType
- status
- minConfidence
- maxConfidence

Response is a GeoJSON FeatureCollection.

## POST /projects/{projectId}/validate

Run topology validation.

Response:

```json
{
  "valid": false,
  "summary": {
    "high": 2,
    "medium": 5,
    "low": 4
  },
  "issues": []
}
```

## PATCH /projects/{projectId}/features/{featureId}

Update a manually edited feature.

Request:

```json
{
  "geometry": {},
  "properties": {
    "status": "corrected"
  }
}
```

## POST /projects/{projectId}/features/{featureId}/verify

Mark feature as verified/rejected/needs_edit.

## POST /projects/{projectId}/export

Request:

```json
{
  "format": "geojson",
  "include": ["parcel", "building", "road"]
}
```

Response:

```json
{
  "jobId": "export-001",
  "status": "completed",
  "downloadUrl": "..."
}
```

## Error format

Use a consistent structure:

```json
{
  "error": {
    "code": "FEATURE_NOT_FOUND",
    "message": "Feature parcel-104 was not found.",
    "details": {}
  }
}
```

Do not leak stack traces to clients.

## API rules

- Validate input.
- Return useful HTTP status codes.
- Do not trust client ownership/IDs blindly.
- Keep response shapes stable.
- Never expose secrets.
- Add request IDs/log correlation where practical.
