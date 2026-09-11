"""API request and response schemas matching API_CONTRACT.md."""
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from backend.models.domain import (
    Project, SourceAsset, Feature, TopologyIssue, ProcessingJob,
    FeatureType, FeatureStatus, ProcessingMode
)

# Project Schemas
class CreateProjectRequest(BaseModel):
    name: str = Field(..., example="Ward 12 Survey")
    description: Optional[str] = Field(None, example="Urban cadastral pilot")
    sourceCrs: Optional[str] = "EPSG:32643"
    metricCrs: Optional[str] = "EPSG:32643"
    overlapToleranceM2: Optional[float] = 0.05
    sliverThresholdM2: Optional[float] = 2.0

class ProjectResponse(BaseModel):
    project: Project

# Asset Schemas
class RegisterAssetRequest(BaseModel):
    assetType: str = "ori"
    name: str
    uri: str
    mimeType: str = "image/jpeg"
    sourceCrs: Optional[str] = "EPSG:32643"
    resolutionGsdMeters: Optional[float] = 0.10
    bounds: Optional[Dict[str, float]] = None
    metadata: Optional[Dict[str, Any]] = None

class AssetResponse(BaseModel):
    asset: SourceAsset

# Extraction Schemas
class StartExtractionRequest(BaseModel):
    assetId: Optional[str] = None
    features: List[str] = Field(default_factory=lambda: ["parcel", "building", "road"])
    mode: Optional[ProcessingMode] = "cv_baseline"

class ExtractionJobResponse(BaseModel):
    jobId: str
    status: str
    pollUrl: str

# Features Schemas
class GeoJSONFeatureCollection(BaseModel):
    type: str = "FeatureCollection"
    features: List[Dict[str, Any]]
    totalFeatures: int = 0
    metadata: Optional[Dict[str, Any]] = None

class PatchFeatureRequest(BaseModel):
    geometry: Optional[Dict[str, Any]] = None
    properties: Optional[Dict[str, Any]] = None

class VerifyFeatureRequest(BaseModel):
    status: FeatureStatus = "verified"
    verifierId: Optional[str] = "surveyor-01"
    note: Optional[str] = None

# Validation Schemas
class ValidateTopologyRequest(BaseModel):
    overlapToleranceM2: Optional[float] = None
    sliverThresholdM2: Optional[float] = None

class ValidationSummary(BaseModel):
    high: int = 0
    medium: int = 0
    low: int = 0
    total: int = 0

class ValidationResponse(BaseModel):
    valid: bool
    summary: ValidationSummary
    issues: List[TopologyIssue]

# Export Schemas
class ExportRequest(BaseModel):
    format: str = "geojson"
    include: List[str] = Field(default_factory=lambda: ["parcel", "building", "road"])

class ExportResponse(BaseModel):
    jobId: str
    status: str
    downloadUrl: Optional[str] = None
    format: str
    featureCount: int
    exportedAt: str

# Error Schemas
class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None

class ErrorResponse(BaseModel):
    error: ErrorDetail
