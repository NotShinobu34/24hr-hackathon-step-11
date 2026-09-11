# Processing Jobs Architecture & Specification

## Purpose

Long-running geospatial and computer vision tasks (feature extraction, batch topology validation, large-file vector export) must not block HTTP request/response loops.

This document defines the formal `ProcessingJob` model, lifecycle states, and polling contract.

---

## 1. Data Model: ProcessingJob

```text
ProcessingJob:
  id: string              (e.g., "job-ext-001" or UUID)
  projectId: string       (e.g., "proj-ward12")
  type: string            ("extraction" | "validation" | "export" | "transformation")
  status: string          ("queued" | "processing" | "completed" | "failed" | "cancelled")
  progress: float         (0.0 to 1.0 or 0 to 100 percentage)
  startedAt: timestamp    (ISO 8601 string)
  completedAt: timestamp  (ISO 8601 string | null)
  error: string | null    (Human-readable error description, no raw stack traces)
  resultSummary: object   (Structured outcome metadata)
```

### Example JSON Schema

```json
{
  "id": "job-ext-7849",
  "projectId": "project-001",
  "type": "extraction",
  "status": "completed",
  "progress": 1.0,
  "startedAt": "2026-09-11T14:30:00.000Z",
  "completedAt": "2026-09-11T14:30:04.250Z",
  "error": null,
  "resultSummary": {
    "mode": "cv_baseline",
    "parcelsExtracted": 34,
    "buildingsExtracted": 48,
    "roadsExtracted": 12,
    "meanConfidence": 0.89,
    "durationMs": 4250
  }
}
```

---

## 2. Job Lifecycle State Machine

```text
       [Triggered]
            │
            ▼
        ┌────────┐
        │ queued │
        └───┬────┘
            │ Worker picked up job
            ▼
      ┌────────────┐
      │ processing │◄───── Progress updates (0.1, 0.4, 0.8...)
      └─────┬──────┘
            │
     ┌──────┴──────────────────────┐
     │                             │
     ▼                             ▼
┌───────────┐                ┌──────────┐
│ completed │                │  failed  │
└───────────┘                └──────────┘
```

---

## 3. Job Endpoints

### 1. Trigger Job
- `POST /api/projects/{projectId}/extract`
- `POST /api/projects/{projectId}/validate`
- `POST /api/projects/{projectId}/export`
- **Response**: `202 Accepted` with initial job record:
  ```json
  {
    "jobId": "job-ext-7849",
    "status": "queued",
    "pollUrl": "/api/projects/project-001/jobs/job-ext-7849"
  }
  ```

### 2. Poll Job Status
- `GET /api/projects/{projectId}/jobs/{jobId}`
- **Response**: Full `ProcessingJob` object.
- If status is `completed`, the client triggers a refresh of the target resource (e.g. `GET /features` or downloads the export artifact).

### 3. Cancel Job
- `POST /api/projects/{projectId}/jobs/{jobId}/cancel`
- Marks job status as `cancelled` and terminates running sub-tasks gracefully.

---

## 4. Error Handling & Guardrails

1. **No Stack Traces**:
   - The `error` field must contain actionable messages (e.g., `"Invalid raster format: missing CRS metadata."` or `"Image dimension 12000x12000 exceeds prototype limit of 4096x4096"`), never internal Python traceback dumps.
2. **Timeout Protection**:
   - Extraction jobs timeout after 15 seconds in prototype mode, cleanly failing over to fallback extraction.
3. **In-Memory / File Store**:
   - For the hackathon vertical slice, jobs are held in an asynchronous in-memory dictionary with disk persistence in `data/jobs/`.
