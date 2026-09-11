"""Topology Validation API router."""
from fastapi import APIRouter, HTTPException
from backend.models.schemas import ValidateTopologyRequest, ValidationResponse, ValidationSummary
from backend.services.project_store import ProjectStore
from backend.geo.topology import TopologyValidator

router = APIRouter(prefix="/api/projects/{project_id}", tags=["validation"])
store = ProjectStore()

@router.post("/validate", response_model=ValidationResponse)
def validate_project_topology(project_id: str, req: ValidateTopologyRequest = None):
    proj = store.get_project(project_id)
    if not proj:
        raise HTTPException(status_code=404, detail={"code": "PROJECT_NOT_FOUND", "message": f"Project {project_id} not found."})

    overlap_tol = (req.overlapToleranceM2 if req and req.overlapToleranceM2 is not None 
                   else proj.parameters.overlapToleranceM2)
    sliver_tol = (req.sliverThresholdM2 if req and req.sliverThresholdM2 is not None 
                  else proj.parameters.sliverThresholdM2)

    validator = TopologyValidator(overlap_tolerance_m2=overlap_tol, sliver_threshold_m2=sliver_tol)
    features = store.get_features(project_id)

    issues = validator.validate_feature_collection(project_id, features)
    store.set_issues(project_id, issues)

    high_count = sum(1 for i in issues if i.severity == "high")
    med_count = sum(1 for i in issues if i.severity == "medium")
    low_count = sum(1 for i in issues if i.severity == "low")

    return {
        "valid": len(issues) == 0,
        "summary": ValidationSummary(
            high=high_count,
            medium=med_count,
            low=low_count,
            total=len(issues)
        ),
        "issues": issues
    }

@router.get("/issues")
def get_validation_issues(project_id: str):
    if not store.get_project(project_id):
        raise HTTPException(status_code=404, detail={"code": "PROJECT_NOT_FOUND", "message": f"Project {project_id} not found."})
    return store.get_issues(project_id)
