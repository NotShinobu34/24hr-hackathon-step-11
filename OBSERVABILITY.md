# Observability, Health & Telemetry Specification

## Purpose

To ensure system stability and diagnose issues rapidly during development and live demonstration, GeoParcel AI implements a lightweight, structured observability architecture.

---

## 1. Health Check Endpoint

### `GET /api/health`
Returns operational health of all system components.

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-09-11T14:45:00.000Z",
  "services": {
    "api": "up",
    "gis_engine": "available",
    "cv_pipeline": "available",
    "fixture_store": "ready"
  },
  "metrics": {
    "activeJobs": 0,
    "uptimeSeconds": 1420
  }
}
```

---

## 2. Structured JSON Logging

All backend log messages follow structured JSON formatting with request tracing:

```json
{
  "timestamp": "2026-09-11T14:45:02.124Z",
  "level": "INFO",
  "requestId": "req-98f3-a12b",
  "module": "geo.topology",
  "message": "Topology validation completed",
  "projectId": "project-001",
  "durationMs": 42.8,
  "issuesDetected": 2
}
```

### Request ID Middleware
FastAPI attaches an `X-Request-ID` header to all incoming requests and includes it in all related logs and error responses for easy correlation.

---

## 3. Frontend Telemetry & Error Handling

1. **Global React Error Boundary**:
   - Catches unhandled rendering crashes and renders a clean, professional recovery screen:
     `"A rendering issue occurred. Your survey edits have been preserved locally. [Reload Workspace]"`
2. **Zero Silent Failures**:
   - Every asynchronous API call must handle network errors and render an alert banner or toast with a retry button.
   - Zero unhandled promise rejections allowed in browser console.
3. **Execution Telemetry in UI**:
   - Extraction jobs display real-time elapsed time and stage description (`"Detecting parcel edges..."`, `"Vectorizing polygons..."`, `"Validating geometry..."`).
