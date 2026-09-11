"""ProcessingJobs API router."""
from fastapi import APIRouter, HTTPException
from backend.models.domain import ProcessingJob
from backend.services.project_store import ProjectStore

router = APIRouter(prefix="/api/projects/{project_id}/jobs", tags=["jobs"])
store = ProjectStore()

@router.get("/{job_id}", response_model=ProcessingJob)
def get_job(project_id: str, job_id: str):
    job = store.get_job(job_id)
    if not job or job.projectId != project_id:
        raise HTTPException(status_code=404, detail={"code": "JOB_NOT_FOUND", "message": f"Job {job_id} not found."})
    return job
