"""Features API router."""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, Dict, Any
from backend.models.schemas import (
    GeoJSONFeatureCollection, PatchFeatureRequest, VerifyFeatureRequest
)
from backend.services.project_store import ProjectStore

router = APIRouter(prefix="/api/projects/{project_id}/features", tags=["features"])
store = ProjectStore()

@router.get("", response_model=GeoJSONFeatureCollection)
def get_features(
    project_id: str,
    featureType: Optional[str] = Query(None, description="parcel, building, road"),
    status: Optional[str] = Query(None, description="detected, review, corrected, verified"),
    minConfidence: Optional[float] = Query(None, ge=0.0, le=1.0)
):
    if not store.get_project(project_id):
        raise HTTPException(status_code=404, detail={"code": "PROJECT_NOT_FOUND", "message": f"Project {project_id} not found."})

    feats = store.get_features(
        project_id=project_id,
        feature_type=featureType,
        status=status,
        min_confidence=minConfidence
    )

    return {
        "type": "FeatureCollection",
        "features": feats,
        "totalFeatures": len(feats),
        "metadata": {
            "projectId": project_id,
            "crs": "EPSG:4326"
        }
    }

@router.get("/{feature_id}")
def get_feature(project_id: str, feature_id: str):
    feat = store.get_feature(project_id, feature_id)
    if not feat:
        raise HTTPException(status_code=404, detail={"code": "FEATURE_NOT_FOUND", "message": f"Feature {feature_id} was not found."})
    return feat

@router.patch("/{feature_id}")
def patch_feature(project_id: str, feature_id: str, req: PatchFeatureRequest):
    updated = store.patch_feature(
        project_id=project_id,
        feature_id=feature_id,
        geometry=req.geometry,
        properties=req.properties
    )
    if not updated:
        raise HTTPException(status_code=404, detail={"code": "FEATURE_NOT_FOUND", "message": f"Feature {feature_id} was not found."})
    return updated

@router.post("/{feature_id}/verify")
def verify_feature(project_id: str, feature_id: str, req: VerifyFeatureRequest):
    updated = store.verify_feature(
        project_id=project_id,
        feature_id=feature_id,
        status=req.status,
        verifier_id=req.verifierId or "surveyor-01",
        note=req.note
    )
    if not updated:
        raise HTTPException(status_code=404, detail={"code": "FEATURE_NOT_FOUND", "message": f"Feature {feature_id} was not found."})
    return updated
