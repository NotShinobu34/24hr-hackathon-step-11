"""Assets API router."""
from fastapi import APIRouter, HTTPException
from typing import List
from backend.models.schemas import RegisterAssetRequest, AssetResponse
from backend.models.domain import SourceAsset
from backend.services.project_store import ProjectStore

router = APIRouter(prefix="/api/projects/{project_id}/assets", tags=["assets"])
store = ProjectStore()

@router.get("", response_model=List[SourceAsset])
def list_assets(project_id: str):
    if not store.get_project(project_id):
        raise HTTPException(status_code=404, detail={"code": "PROJECT_NOT_FOUND", "message": f"Project {project_id} not found."})
    return store.get_assets(project_id)

@router.post("", response_model=AssetResponse)
def register_asset(project_id: str, req: RegisterAssetRequest):
    if not store.get_project(project_id):
        raise HTTPException(status_code=404, detail={"code": "PROJECT_NOT_FOUND", "message": f"Project {project_id} not found."})

    asset = SourceAsset(
        projectId=project_id,
        assetType=req.assetType,
        name=req.name,
        uri=req.uri,
        mimeType=req.mimeType,
        sourceCrs=req.sourceCrs,
        resolutionGsdMeters=req.resolutionGsdMeters,
        bounds=req.bounds,
        metadata=req.metadata or {}
    )
    store.add_asset(asset)
    return {"asset": asset}
