export type FeatureType = 'parcel' | 'building' | 'road' | 'land_use';
export type FeatureSource = 'ai' | 'ground_truth' | 'manual';
export type FeatureStatus = 'detected' | 'review' | 'corrected' | 'verified' | 'rejected';
export type ProcessingMode = 'model_inference' | 'cv_baseline' | 'demo_fixture' | 'manual_edit' | 'reference';
export type IssueType = 'overlap' | 'self_intersection' | 'duplicate' | 'invalid_geometry' | 'sliver' | 'gap';
export type IssueSeverity = 'high' | 'medium' | 'low';
export type JobStatus = 'queued' | 'processing' | 'completed' | 'failed' | 'cancelled';
export type ProjectStatus = 'draft' | 'processing' | 'review' | 'verified' | 'exported';

export interface EditHistoryEntry {
  timestamp: string;
  editorId?: string;
  operation: string;
  previousArea_m2?: number;
}

export interface FeatureProperties {
  source: FeatureSource;
  sourceAssetId?: string;
  processingMode: ProcessingMode;
  confidence?: number;
  confidenceType?: string;
  status: FeatureStatus;
  edited: boolean;
  verified: boolean;
  verifierId?: string | null;
  verifiedAt?: string | null;
  editHistory?: EditHistoryEntry[];
  area_m2?: number;
  perimeter_m?: number;
  metricCrs?: string;
  land_use?: string;
  name?: string;
  surveyNumber?: string;
  verificationNote?: string;
}

export interface GeoJSONFeature {
  type: 'Feature';
  id: string;
  featureType?: FeatureType;
  geometry: {
    type: 'Polygon' | 'MultiPolygon' | 'LineString' | 'Point';
    coordinates: any;
  };
  properties: FeatureProperties;
}

export interface GeoJSONFeatureCollection {
  type: 'FeatureCollection';
  features: GeoJSONFeature[];
  totalFeatures?: number;
  metadata?: Record<string, any>;
}

export interface TopologyIssue {
  id: string;
  projectId: string;
  featureId: string;
  relatedFeatureId?: string | null;
  issueType: IssueType;
  severity: IssueSeverity;
  message: string;
  toleranceUsed: number;
  resolved: boolean;
  createdAt: string;
  resolvedAt?: string | null;
}

export interface ProcessingJob {
  id: string;
  projectId: string;
  type: string;
  status: JobStatus;
  progress: number;
  startedAt: string;
  completedAt?: string | null;
  error?: string | null;
  resultSummary?: Record<string, any>;
}

export interface ProjectParameters {
  overlapToleranceM2: number;
  sliverThresholdM2: number;
}

export interface Project {
  id: string;
  name: string;
  description?: string | null;
  status: ProjectStatus;
  sourceCrs?: string | null;
  metricCrs: string;
  parameters: ProjectParameters;
  createdAt: string;
  updatedAt: string;
}

export interface LayerVisibilityState {
  imagery: boolean;
  parcels: boolean;
  buildings: boolean;
  roads: boolean;
  groundTruth: boolean;
  issues: boolean;
}

export interface LayerOpacityState {
  imagery: number;
  parcels: number;
  buildings: number;
  roads: number;
  groundTruth: number;
}
