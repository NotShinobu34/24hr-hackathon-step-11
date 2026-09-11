"""Export API router."""
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
from datetime import datetime
from backend.models.schemas import ExportRequest, ExportResponse
from backend.services.project_store import ProjectStore
from backend.services.export_service import ExportService

router = APIRouter(tags=["export"])
store = ProjectStore()
exporter = ExportService()

@router.post("/api/projects/{project_id}/export", response_model=ExportResponse)
def export_project_data(project_id: str, req: ExportRequest):
    proj = store.get_project(project_id)
    if not proj:
        raise HTTPException(status_code=404, detail={"code": "PROJECT_NOT_FOUND", "message": f"Project {project_id} not found."})

    features = store.get_features(project_id)
    filename, download_url, count = exporter.export_geojson(
        project_id=project_id,
        project_name=proj.name,
        features=features,
        include_types=req.include
    )

    proj.status = "exported"

    return {
        "jobId": f"exp_{filename[:8]}",
        "status": "completed",
        "downloadUrl": download_url,
        "format": "geojson",
        "featureCount": count,
        "exportedAt": datetime.utcnow().isoformat() + "Z"
    }

@router.get("/api/exports/download/{filename}")
def download_export(filename: str):
    # Ensure secure filename without directory traversal
    safe_name = os.path.basename(filename)
    filepath = os.path.join(exporter.export_dir, safe_name)

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail={"code": "FILE_NOT_FOUND", "message": f"Export file {safe_name} not found."})

    return FileResponse(
        filepath,
        media_type="application/geo+json",
        filename=safe_name
    )
