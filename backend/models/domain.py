"""Domain entities for GeoParcel AI."""
from typing import Dict, Any, List, Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field
import uuid

FeatureType = Literal["parcel", "building", "road", "land_use"]
FeatureSource = Literal["ai", "ground_truth", "manual"]
FeatureStatus = Literal["detected", "review", "corrected", "verified", "rejected"]
ProcessingMode = Literal["model_inference", "cv_baseline", "demo_fixture", "manual_edit", "reference"]
ConfidenceType = Literal["model_probability", "heuristic", "ground_truth", "n/a"]
IssueType = Literal["overlap", "self_intersection", "duplicate", "invalid_geometry", "sliver", "gap"]
IssueSeverity = Literal["high", "medium", "low"]
JobType = Literal["extraction", "validation", "export", "transformation"]
JobStatus = Literal["queued", "processing", "completed", "failed", "cancelled"]
ProjectStatus = Literal["draft", "processing", "review", "verified", "exported"]

class ProjectParameters(BaseModel):
    """Configurable prototype validation parameters."""
    overlapToleranceM2: float = Field(0.05, description="Prototype threshold in m² above which parcel intersection is flagged as overlap")
    sliverThresholdM2: float = Field(2.0, description="Prototype threshold in m² below which parcel is flagged as suspicious sliver")

class Project(BaseModel):
    id: str = Field(default_factory=lambda: f"proj_{uuid.uuid4().hex[:8]}")
    name: str
    description: Optional[str] = None
    status: ProjectStatus = "draft"
    sourceCrs: Optional[str] = "EPSG:32643"
    metricCrs: str = "EPSG:32643"
    parameters: ProjectParameters = Field(default_factory=ProjectParameters)
    createdAt: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    updatedAt: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

class SourceAsset(BaseModel):
    id: str = Field(default_factory=lambda: f"asset_{uuid.uuid4().hex[:8]}")
    projectId: str
    assetType: Literal["ori", "drone", "dsm", "dtm", "gis_parcel", "ground_truth"]
    name: str
    uri: str
    mimeType: str = "image/jpeg"
    sourceCrs: Optional[str] = "EPSG:32643"
    resolutionGsdMeters: Optional[float] = 0.10
    width: Optional[int] = None
    height: Optional[int] = None
    bounds: Optional[Dict[str, float]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    createdAt: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

class EditHistoryEntry(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    editorId: Optional[str] = "surveyor-01"
    operation: str
    previousArea_m2: Optional[float] = None

class FeatureProperties(BaseModel):
    source: FeatureSource = "ai"
    sourceAssetId: Optional[str] = None
    processingMode: ProcessingMode = "cv_baseline"
    confidence: Optional[float] = None
    confidenceType: ConfidenceType = "heuristic"
    status: FeatureStatus = "detected"
    edited: bool = False
    verified: bool = False
    verifierId: Optional[str] = None
    verifiedAt: Optional[str] = None
    editHistory: List[EditHistoryEntry] = Field(default_factory=list)
    area_m2: Optional[float] = None
    perimeter_m: Optional[float] = None
    metricCrs: Optional[str] = "EPSG:32643"
    land_use: Optional[str] = None
    name: Optional[str] = None
    surveyNumber: Optional[str] = None

class GeoJSONGeometry(BaseModel):
    type: str
    coordinates: Any

class Feature(BaseModel):
    id: str
    type: str = "Feature"
    featureType: FeatureType
    geometry: GeoJSONGeometry
    properties: FeatureProperties

class TopologyIssue(BaseModel):
    id: str = Field(default_factory=lambda: f"issue_{uuid.uuid4().hex[:8]}")
    projectId: str
    featureId: str
    relatedFeatureId: Optional[str] = None
    issueType: IssueType
    severity: IssueSeverity
    message: str
    toleranceUsed: float
    resolved: bool = False
    createdAt: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    resolvedAt: Optional[str] = None

class ProcessingJob(BaseModel):
    id: str = Field(default_factory=lambda: f"job_{uuid.uuid4().hex[:8]}")
    projectId: str
    type: JobType
    status: JobStatus = "queued"
    progress: float = 0.0
    startedAt: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    completedAt: Optional[str] = None
    error: Optional[str] = None
    resultSummary: Dict[str, Any] = Field(default_factory=dict)
