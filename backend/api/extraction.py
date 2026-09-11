"""Extraction API router."""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from backend.models.schemas import StartExtractionRequest, ExtractionJobResponse
from backend.services.project_store import ProjectStore
from backend.ai.pipeline import ExtractionPipeline

router = APIRouter(prefix="/api/projects/{project_id}", tags=["extraction"])
store = ProjectStore()
pipeline = ExtractionPipeline()

def _run_async_extraction(project_id: str, job_id: str, asset_id: str, feature_types: list, mode: str):
    try:
        store.update_job(job_id, status="processing", progress=0.25)
        features, actual_mode, summary = pipeline.run_extraction(
            project_id=project_id,
            asset_id=asset_id,
            feature_types=feature_types,
            requested_mode=mode
        )
        summary["actualMode"] = actual_mode
        store.update_job(job_id, status="processing", progress=0.75)
        store.set_features(project_id, features)
        store.update_job(job_id, status="completed", progress=1.0, result_summary=summary)
    except Exception as e:
        store.update_job(job_id, status="failed", progress=1.0, error=str(e))

@router.post("/extract", response_model=ExtractionJobResponse, status_code=202)
def start_extraction(project_id: str, req: StartExtractionRequest, background_tasks: BackgroundTasks):
    proj = store.get_project(project_id)
    if not proj:
        raise HTTPException(status_code=404, detail={"code": "PROJECT_NOT_FOUND", "message": f"Project {project_id} not found."})

    job = store.create_job(project_id, job_type="extraction")
    asset_id = req.assetId or "asset-ortho-001"
    mode = req.mode or "cv_baseline"

    background_tasks.add_task(
        _run_async_extraction,
        project_id,
        job.id,
        asset_id,
        req.features,
        mode
    )

    return {
        "jobId": job.id,
        "status": "queued",
        "pollUrl": f"/api/projects/{project_id}/jobs/{job.id}"
    }

# Backward-compatible endpoint matching API_CONTRACT.md /extract/{jobId}
@router.get("/extract/{job_id}")
def get_extraction_status(project_id: str, job_id: str):
    job = store.get_job(job_id)
    if not job or job.projectId != project_id:
        raise HTTPException(status_code=404, detail={"code": "JOB_NOT_FOUND", "message": f"Job {job_id} not found."})

    return {
        "jobId": job.id,
        "status": job.status,
        "progress": job.progress,
        "summary": job.resultSummary
    }
