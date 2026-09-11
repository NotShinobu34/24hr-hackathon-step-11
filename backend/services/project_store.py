"""In-memory and JSON storage service for projects, assets, jobs, and features."""
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import os
from backend.models.domain import (
    Project, SourceAsset, ProcessingJob, TopologyIssue,
    ProjectParameters
)
from backend.geo.geometry import GeometryEngine

class ProjectStore:
    """Singleton store managing survey projects and feature layers."""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ProjectStore, cls).__new__(cls)
            cls._instance._init_store()
        return cls._instance

    def _init_store(self):
        self.projects: Dict[str, Project] = {}
        self.assets: Dict[str, List[SourceAsset]] = {}
        self.features: Dict[str, List[Dict[str, Any]]] = {}
        self.jobs: Dict[str, ProcessingJob] = {}
        self.issues: Dict[str, List[TopologyIssue]] = {}
        self._seed_default_project()

    def _seed_default_project(self):
        proj_id = "project-001"
        self.projects[proj_id] = Project(
            id=proj_id,
            name="Ward 12 Survey",
            description="Urban cadastral pilot for municipal boundary review",
            status="draft",
            sourceCrs="EPSG:32643",
            metricCrs="EPSG:32643",
            parameters=ProjectParameters(overlapToleranceM2=0.05, sliverThresholdM2=2.0)
        )

        asset = SourceAsset(
            id="asset-ortho-001",
            projectId=proj_id,
            assetType="ori",
            name="sample_ortho.jpg",
            uri="/fixtures/imagery/sample_ortho.jpg",
            mimeType="image/jpeg",
            sourceCrs="EPSG:32643",
            resolutionGsdMeters=0.10,
            bounds={"west": 77.5910, "south": 12.9685, "east": 77.5982, "north": 12.9747}
        )
        self.assets[proj_id] = [asset]
        self.features[proj_id] = []
        self.issues[proj_id] = []

        # Load default fixture features into project
        fixture_path = "fixtures/geojson/parcels_detected.geojson"
        if not os.path.exists(fixture_path):
            fixture_path = "../fixtures/geojson/parcels_detected.geojson"
        
        if os.path.exists(fixture_path):
            try:
                with open(fixture_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.features[proj_id].extend(data.get("features", []))
            except Exception:
                pass

        # Also load buildings and roads
        for fname in ["buildings_detected.geojson", "roads_detected.geojson"]:
            p = os.path.join(os.path.dirname(fixture_path), fname)
            if os.path.exists(p):
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        d = json.load(f)
                        self.features[proj_id].extend(d.get("features", []))
                except Exception:
                    pass

    # Project Operations
    def get_project(self, project_id: str) -> Optional[Project]:
        return self.projects.get(project_id)

    def create_project(self, name: str, description: Optional[str] = None, source_crs: str = "EPSG:32643") -> Project:
        proj = Project(
            name=name,
            description=description,
            sourceCrs=source_crs,
            metricCrs=source_crs,
            status="draft"
        )
        self.projects[proj.id] = proj
        self.assets[proj.id] = []
        self.features[proj.id] = []
        self.issues[proj.id] = []
        return proj

    # Asset Operations
    def get_assets(self, project_id: str) -> List[SourceAsset]:
        return self.assets.get(project_id, [])

    def add_asset(self, asset: SourceAsset) -> SourceAsset:
        if asset.projectId not in self.assets:
            self.assets[asset.projectId] = []
        self.assets[asset.projectId].append(asset)
        return asset

    # Feature Operations
    def get_features(
        self,
        project_id: str,
        feature_type: Optional[str] = None,
        status: Optional[str] = None,
        min_confidence: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        feats = self.features.get(project_id, [])
        filtered = []
        for f in feats:
            f_type = f.get("featureType") or f.get("properties", {}).get("featureType")
            f_status = f.get("properties", {}).get("status")
            f_conf = f.get("properties", {}).get("confidence", 1.0)

            if feature_type and f_type != feature_type:
                continue
            if status and f_status != status:
                continue
            if min_confidence is not None and f_conf < min_confidence:
                continue
            filtered.append(f)
        return filtered

    def get_feature(self, project_id: str, feature_id: str) -> Optional[Dict[str, Any]]:
        for f in self.features.get(project_id, []):
            if f.get("id") == feature_id:
                return f
        return None

    def patch_feature(self, project_id: str, feature_id: str, geometry: Optional[Dict[str, Any]], properties: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        feats = self.features.get(project_id, [])
        for f in feats:
            if f.get("id") == feature_id:
                old_area = f.get("properties", {}).get("area_m2")
                if geometry:
                    f["geometry"] = geometry
                    # Recalculate area and perimeter
                    try:
                        area_m2, perim_m, _ = GeometryEngine.calculate_metric_measurements(geometry)
                        f["properties"]["area_m2"] = area_m2
                        f["properties"]["perimeter_m"] = perim_m
                    except Exception:
                        pass

                f["properties"]["edited"] = True
                f["properties"]["status"] = "corrected"

                if "editHistory" not in f["properties"]:
                    f["properties"]["editHistory"] = []

                f["properties"]["editHistory"].append({
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "editorId": "surveyor-01",
                    "operation": "boundary_vertex_edit",
                    "previousArea_m2": old_area
                })

                if properties:
                    for k, v in properties.items():
                        if k not in ("editHistory", "edited"):
                            f["properties"][k] = v

                return f
        return None

    def verify_feature(self, project_id: str, feature_id: str, status: str, verifier_id: str, note: Optional[str] = None) -> Optional[Dict[str, Any]]:
        f = self.get_feature(project_id, feature_id)
        if f:
            f["properties"]["status"] = status
            f["properties"]["verified"] = (status == "verified")
            f["properties"]["verifierId"] = verifier_id
            f["properties"]["verifiedAt"] = datetime.utcnow().isoformat() + "Z"
            if note:
                f["properties"]["verificationNote"] = note
            return f
        return None

    def set_features(self, project_id: str, features: List[Dict[str, Any]]):
        self.features[project_id] = features

    # Job Operations
    def create_job(self, project_id: str, job_type: str) -> ProcessingJob:
        job = ProcessingJob(projectId=project_id, type=job_type, status="queued")
        self.jobs[job.id] = job
        return job

    def get_job(self, job_id: str) -> Optional[ProcessingJob]:
        return self.jobs.get(job_id)

    def update_job(self, job_id: str, status: str, progress: float = 1.0, error: Optional[str] = None, result_summary: Optional[Dict[str, Any]] = None):
        job = self.jobs.get(job_id)
        if job:
            job.status = status
            job.progress = progress
            if status in ("completed", "failed"):
                job.completedAt = datetime.utcnow().isoformat() + "Z"
            if error:
                job.error = error
            if result_summary:
                job.resultSummary = result_summary

    # Topology Issue Operations
    def set_issues(self, project_id: str, issues: List[TopologyIssue]):
        self.issues[project_id] = issues

    def get_issues(self, project_id: str) -> List[TopologyIssue]:
        return self.issues.get(project_id, [])
