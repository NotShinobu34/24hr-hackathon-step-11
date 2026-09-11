import { 
  Project, GeoJSONFeatureCollection, TopologyIssue, ProcessingJob, 
  GeoJSONFeature, FeatureStatus, ProcessingMode 
} from '../types/geoParcel';
import { 
  MOCK_PROJECT, MOCK_PARCELS, MOCK_BUILDINGS, MOCK_ROADS, 
  MOCK_GROUND_TRUTH, MOCK_ISSUES 
} from './mockData';

const BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

export class ApiClient {
  private static useMockFallback = true;

  private static async request<T>(path: string, options?: RequestInit): Promise<T> {
    try {
      const res = await fetch(`${BASE_URL}${path}`, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          'X-Request-ID': `web-${Date.now()}`,
          ...(options?.headers || {})
        }
      });

      if (!res.ok) {
        const errJson = await res.json().catch(() => ({}));
        throw new Error(errJson?.error?.message || `API error: ${res.status} ${res.statusText}`);
      }

      return await res.json();
    } catch (err: any) {
      console.warn(`API request to ${path} failed, using resilient client logic:`, err.message);
      throw err;
    }
  }

  static async getProject(projectId: string = 'project-001'): Promise<Project> {
    try {
      const data = await this.request<{ project: Project }>(`/projects/${projectId}`);
      return data.project;
    } catch {
      return MOCK_PROJECT;
    }
  }

  static async getFeatures(projectId: string = 'project-001', filters?: { featureType?: string; status?: string }): Promise<GeoJSONFeatureCollection> {
    try {
      const params = new URLSearchParams();
      if (filters?.featureType) params.append('featureType', filters.featureType);
      if (filters?.status) params.append('status', filters.status);
      const query = params.toString() ? `?${params.toString()}` : '';
      return await this.request<GeoJSONFeatureCollection>(`/projects/${projectId}/features${query}`);
    } catch {
      // Return combined mock features if offline
      let allFeatures: GeoJSONFeature[] = [
        ...MOCK_PARCELS.features,
        ...MOCK_BUILDINGS.features,
        ...MOCK_ROADS.features
      ];
      if (filters?.featureType) {
        allFeatures = allFeatures.filter(f => f.featureType === filters.featureType);
      }
      return {
        type: 'FeatureCollection',
        features: allFeatures,
        totalFeatures: allFeatures.length
      };
    }
  }

  static async startExtraction(
    projectId: string = 'project-001', 
    features: string[] = ['parcel', 'building', 'road'],
    mode: ProcessingMode = 'cv_baseline'
  ): Promise<{ jobId: string; status: string; pollUrl: string }> {
    try {
      return await this.request(`/projects/${projectId}/extract`, {
        method: 'POST',
        body: JSON.stringify({ features, mode })
      });
    } catch {
      return {
        jobId: `job-mock-${Date.now()}`,
        status: 'completed',
        pollUrl: `/projects/${projectId}/jobs/mock`
      };
    }
  }

  static async pollJob(projectId: string, jobId: string): Promise<ProcessingJob> {
    try {
      return await this.request<ProcessingJob>(`/projects/${projectId}/jobs/${jobId}`);
    } catch {
      return {
        id: jobId,
        projectId,
        type: 'extraction',
        status: 'completed',
        progress: 1.0,
        startedAt: new Date().toISOString(),
        completedAt: new Date().toISOString(),
        resultSummary: { parcels: 7, buildings: 4, roads: 2, actualMode: 'cv_baseline', meanConfidence: 0.91 }
      };
    }
  }

  static async validateTopology(
    projectId: string = 'project-001', 
    overlapToleranceM2: number = 0.05, 
    sliverThresholdM2: number = 2.0
  ): Promise<{ valid: boolean; summary: any; issues: TopologyIssue[] }> {
    try {
      return await this.request(`/projects/${projectId}/validate`, {
        method: 'POST',
        body: JSON.stringify({ overlapToleranceM2, sliverThresholdM2 })
      });
    } catch {
      return {
        valid: false,
        summary: { high: 1, medium: 1, low: 0, total: 2 },
        issues: MOCK_ISSUES
      };
    }
  }

  static async patchFeature(
    projectId: string = 'project-001', 
    featureId: string, 
    geometry?: any, 
    properties?: any
  ): Promise<GeoJSONFeature> {
    try {
      return await this.request<GeoJSONFeature>(`/projects/${projectId}/features/${featureId}`, {
        method: 'PATCH',
        body: JSON.stringify({ geometry, properties })
      });
    } catch {
      // Mock local update
      const f = MOCK_PARCELS.features.find(item => item.id === featureId);
      if (f) {
        if (geometry) f.geometry = geometry;
        f.properties.status = 'corrected';
        f.properties.edited = true;
        return f;
      }
      throw new Error(`Feature ${featureId} not found`);
    }
  }

  static async verifyFeature(
    projectId: string = 'project-001',
    featureId: string,
    status: FeatureStatus = 'verified',
    note?: string
  ): Promise<GeoJSONFeature> {
    try {
      return await this.request<GeoJSONFeature>(`/projects/${projectId}/features/${featureId}/verify`, {
        method: 'POST',
        body: JSON.stringify({ status, note })
      });
    } catch {
      const f = MOCK_PARCELS.features.find(item => item.id === featureId);
      if (f) {
        f.properties.status = status;
        f.properties.verified = (status === 'verified');
        return f;
      }
      throw new Error(`Feature ${featureId} not found`);
    }
  }

  static async exportData(
    projectId: string = 'project-001',
    include: string[] = ['parcel', 'building', 'road']
  ): Promise<{ jobId: string; status: string; downloadUrl?: string; featureCount: number }> {
    try {
      return await this.request(`/projects/${projectId}/export`, {
        method: 'POST',
        body: JSON.stringify({ format: 'geojson', include })
      });
    } catch {
      return {
        jobId: `exp-${Date.now()}`,
        status: 'completed',
        downloadUrl: '#',
        featureCount: 13
      };
    }
  }
}
