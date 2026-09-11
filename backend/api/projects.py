"""Projects API router."""
from fastapi import APIRouter, HTTPException
from backend.models.schemas import CreateProjectRequest, ProjectResponse
from backend.services.project_store import ProjectStore

router = APIRouter(prefix="/api/projects", tags=["projects"])
store = ProjectStore()

@router.post("", response_model=ProjectResponse)
def create_project(req: CreateProjectRequest):
    proj = store.create_project(
        name=req.name,
        description=req.description,
        source_crs=req.sourceCrs or "EPSG:32643"
    )
    if req.overlapToleranceM2 is not None:
        proj.parameters.overlapToleranceM2 = req.overlapToleranceM2
    if req.sliverThresholdM2 is not None:
        proj.parameters.sliverThresholdM2 = req.sliverThresholdM2
    return {"project": proj}

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: str):
    proj = store.get_project(project_id)
    if not proj:
        raise HTTPException(status_code=404, detail={"code": "PROJECT_NOT_FOUND", "message": f"Project {project_id} not found."})
    return {"project": proj}
