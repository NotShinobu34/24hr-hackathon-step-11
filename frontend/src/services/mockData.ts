import { GeoJSONFeatureCollection, Project, TopologyIssue } from '../types/geoParcel';

export const MOCK_PROJECT: Project = {
  id: 'project-001',
  name: 'Ward 12 Survey',
  description: 'Urban cadastral pilot for municipal boundary review',
  status: 'review',
  sourceCrs: 'EPSG:32643',
  metricCrs: 'EPSG:32643',
  parameters: {
    overlapToleranceM2: 0.05,
    sliverThresholdM2: 2.0
  },
  createdAt: '2026-09-11T12:00:00Z',
  updatedAt: '2026-09-11T12:00:00Z'
};

export const MOCK_PARCELS: GeoJSONFeatureCollection = {
  type: 'FeatureCollection',
  features: [
    {
      type: 'Feature',
      id: 'parcel-101',
      featureType: 'parcel',
      geometry: {
        type: 'Polygon',
        coordinates: [[[77.5930, 12.9710], [77.5936, 12.9710], [77.5936, 12.9716], [77.5930, 12.9716], [77.5930, 12.9710]]]
      },
      properties: {
        source: 'ai',
        sourceAssetId: 'asset-ortho-001',
        processingMode: 'cv_baseline',
        confidence: 0.94,
        confidenceType: 'heuristic',
        status: 'review',
        edited: false,
        verified: false,
        area_m2: 441.2,
        perimeter_m: 84.0,
        land_use: 'residential',
        metricCrs: 'EPSG:32643'
      }
    },
    {
      type: 'Feature',
      id: 'parcel-102',
      featureType: 'parcel',
      geometry: {
        type: 'Polygon',
        coordinates: [[[77.5936, 12.9710], [77.5942, 12.9710], [77.5942, 12.9716], [77.5936, 12.9716], [77.5936, 12.9710]]]
      },
      properties: {
        source: 'ai',
        sourceAssetId: 'asset-ortho-001',
        processingMode: 'cv_baseline',
        confidence: 0.92,
        confidenceType: 'heuristic',
        status: 'review',
        edited: false,
        verified: false,
        area_m2: 441.2,
        perimeter_m: 84.0,
        land_use: 'residential',
        metricCrs: 'EPSG:32643'
      }
    },
    {
      type: 'Feature',
      id: 'parcel-103',
      featureType: 'parcel',
      geometry: {
        type: 'Polygon',
        coordinates: [[[77.5942, 12.9710], [77.5949, 12.9710], [77.5949, 12.9716], [77.5942, 12.9716], [77.5942, 12.9710]]]
      },
      properties: {
        source: 'ai',
        sourceAssetId: 'asset-ortho-001',
        processingMode: 'cv_baseline',
        confidence: 0.95,
        confidenceType: 'heuristic',
        status: 'review',
        edited: false,
        verified: false,
        area_m2: 514.8,
        perimeter_m: 91.0,
        land_use: 'commercial',
        metricCrs: 'EPSG:32643'
      }
    },
    // P-104: Intentional overlap with P-105
    {
      type: 'Feature',
      id: 'parcel-104',
      featureType: 'parcel',
      geometry: {
        type: 'Polygon',
        coordinates: [[[77.5949, 12.9710], [77.5956, 12.9710], [77.5956, 12.9716], [77.5949, 12.9716], [77.5949, 12.9710]]]
      },
      properties: {
        source: 'ai',
        sourceAssetId: 'asset-ortho-001',
        processingMode: 'cv_baseline',
        confidence: 0.86,
        confidenceType: 'heuristic',
        status: 'review',
        edited: false,
        verified: false,
        area_m2: 514.8,
        perimeter_m: 91.0,
        land_use: 'residential',
        metricCrs: 'EPSG:32643'
      }
    },
    // P-105: Overlaps P-104 west boundary
    {
      type: 'Feature',
      id: 'parcel-105',
      featureType: 'parcel',
      geometry: {
        type: 'Polygon',
        coordinates: [[[77.59545, 12.9710], [77.5962, 12.9710], [77.5962, 12.9716], [77.59545, 12.9716], [77.59545, 12.9710]]]
      },
      properties: {
        source: 'ai',
        sourceAssetId: 'asset-ortho-001',
        processingMode: 'cv_baseline',
        confidence: 0.88,
        confidenceType: 'heuristic',
        status: 'review',
        edited: false,
        verified: false,
        area_m2: 551.5,
        perimeter_m: 94.0,
        land_use: 'residential',
        metricCrs: 'EPSG:32643'
      }
    },
    {
      type: 'Feature',
      id: 'parcel-106',
      featureType: 'parcel',
      geometry: {
        type: 'Polygon',
        coordinates: [[[77.5930, 12.9718], [77.5937, 12.9718], [77.5937, 12.9725], [77.5930, 12.9725], [77.5930, 12.9718]]]
      },
      properties: {
        source: 'ai',
        sourceAssetId: 'asset-ortho-001',
        processingMode: 'cv_baseline',
        confidence: 0.93,
        confidenceType: 'heuristic',
        status: 'review',
        edited: false,
        verified: false,
        area_m2: 565.0,
        perimeter_m: 95.2,
        land_use: 'residential',
        metricCrs: 'EPSG:32643'
      }
    },
    // P-112: Sliver polygon
    {
      type: 'Feature',
      id: 'parcel-112',
      featureType: 'parcel',
      geometry: {
        type: 'Polygon',
        coordinates: [[[77.59368, 12.97178], [77.59371, 12.97178], [77.59371, 12.97182], [77.59368, 12.97182], [77.59368, 12.97178]]]
      },
      properties: {
        source: 'ai',
        sourceAssetId: 'asset-ortho-001',
        processingMode: 'cv_baseline',
        confidence: 0.65,
        confidenceType: 'heuristic',
        status: 'review',
        edited: false,
        verified: false,
        area_m2: 1.4,
        perimeter_m: 5.8,
        land_use: 'unclassified',
        metricCrs: 'EPSG:32643'
      }
    }
  ]
};

export const MOCK_BUILDINGS: GeoJSONFeatureCollection = {
  type: 'FeatureCollection',
  features: [
    {
      type: 'Feature',
      id: 'bldg-201',
      featureType: 'building',
      geometry: {
        type: 'Polygon',
        coordinates: [[[77.5931, 12.9711], [77.5935, 12.9711], [77.5935, 12.9715], [77.5931, 12.9715], [77.5931, 12.9711]]]
      },
      properties: {
        source: 'ai',
        sourceAssetId: 'asset-ortho-001',
        processingMode: 'cv_baseline',
        confidence: 0.93,
        status: 'detected',
        edited: false,
        verified: false,
        area_m2: 196.0,
        metricCrs: 'EPSG:32643'
      }
    },
    {
      type: 'Feature',
      id: 'bldg-202',
      featureType: 'building',
      geometry: {
        type: 'Polygon',
        coordinates: [[[77.5937, 12.9711], [77.5941, 12.9711], [77.5941, 12.9715], [77.5937, 12.9715], [77.5937, 12.9711]]]
      },
      properties: {
        source: 'ai',
        sourceAssetId: 'asset-ortho-001',
        processingMode: 'cv_baseline',
        confidence: 0.91,
        status: 'detected',
        edited: false,
        verified: false,
        area_m2: 196.0,
        metricCrs: 'EPSG:32643'
      }
    },
    {
      type: 'Feature',
      id: 'bldg-203',
      featureType: 'building',
      geometry: {
        type: 'Polygon',
        coordinates: [[[77.5943, 12.9711], [77.5948, 12.9711], [77.5948, 12.9715], [77.5943, 12.9715], [77.5943, 12.9711]]]
      },
      properties: {
        source: 'ai',
        sourceAssetId: 'asset-ortho-001',
        processingMode: 'cv_baseline',
        confidence: 0.95,
        status: 'detected',
        edited: false,
        verified: false,
        area_m2: 245.0,
        metricCrs: 'EPSG:32643'
      }
    },
    {
      type: 'Feature',
      id: 'bldg-204',
      featureType: 'building',
      geometry: {
        type: 'Polygon',
        coordinates: [[[77.5950, 12.9711], [77.5954, 12.9711], [77.5954, 12.9715], [77.5950, 12.9715], [77.5950, 12.9711]]]
      },
      properties: {
        source: 'ai',
        sourceAssetId: 'asset-ortho-001',
        processingMode: 'cv_baseline',
        confidence: 0.89,
        status: 'detected',
        edited: false,
        verified: false,
        area_m2: 196.0,
        metricCrs: 'EPSG:32643'
      }
    }
  ]
};

export const MOCK_ROADS: GeoJSONFeatureCollection = {
  type: 'FeatureCollection',
  features: [
    {
      type: 'Feature',
      id: 'road-301',
      featureType: 'road',
      geometry: {
        type: 'LineString',
        coordinates: [[77.5925, 12.9708], [77.5965, 12.9708]]
      },
      properties: {
        source: 'ai',
        sourceAssetId: 'asset-ortho-001',
        processingMode: 'cv_baseline',
        confidence: 0.91,
        status: 'detected',
        edited: false,
        verified: false,
        name: 'Main Access Corridor 1'
      }
    },
    {
      type: 'Feature',
      id: 'road-302',
      featureType: 'road',
      geometry: {
        type: 'LineString',
        coordinates: [[77.5925, 12.9717], [77.5965, 12.9717]]
      },
      properties: {
        source: 'ai',
        sourceAssetId: 'asset-ortho-001',
        processingMode: 'cv_baseline',
        confidence: 0.89,
        status: 'detected',
        edited: false,
        verified: false,
        name: 'Residential Access Lane 2'
      }
    }
  ]
};

export const MOCK_GROUND_TRUTH: GeoJSONFeatureCollection = {
  type: 'FeatureCollection',
  features: [
    {
      type: 'Feature',
      id: 'gt-parcel-104',
      featureType: 'parcel',
      geometry: {
        type: 'Polygon',
        coordinates: [[[77.5949, 12.9710], [77.5955, 12.9710], [77.5955, 12.9716], [77.5949, 12.9716], [77.5949, 12.9710]]]
      },
      properties: {
        source: 'ground_truth',
        sourceAssetId: 'asset-gt-001',
        processingMode: 'reference',
        status: 'verified',
        edited: false,
        verified: true,
        surveyNumber: '104/A',
        area_m2: 441.2,
        metricCrs: 'EPSG:32643'
      }
    },
    {
      type: 'Feature',
      id: 'gt-parcel-105',
      featureType: 'parcel',
      geometry: {
        type: 'Polygon',
        coordinates: [[[77.5955, 12.9710], [77.5962, 12.9710], [77.5962, 12.9716], [77.5955, 12.9716], [77.5955, 12.9710]]]
      },
      properties: {
        source: 'ground_truth',
        sourceAssetId: 'asset-gt-001',
        processingMode: 'reference',
        status: 'verified',
        edited: false,
        verified: true,
        surveyNumber: '105/B',
        area_m2: 514.8,
        metricCrs: 'EPSG:32643'
      }
    }
  ]
};

export const MOCK_ISSUES: TopologyIssue[] = [
  {
    id: 'issue-001',
    projectId: 'project-001',
    featureId: 'parcel-104',
    relatedFeatureId: 'parcel-105',
    issueType: 'overlap',
    severity: 'high',
    message: 'Overlapping parcel boundaries detected between parcel-104 and parcel-105. Overlap area: 8.42 m² (tolerance: 0.05 m²).',
    toleranceUsed: 0.05,
    resolved: false,
    createdAt: '2026-09-11T12:05:00Z'
  },
  {
    id: 'issue-002',
    projectId: 'project-001',
    featureId: 'parcel-112',
    relatedFeatureId: null,
    issueType: 'sliver',
    severity: 'medium',
    message: 'Parcel parcel-112 has area 1.40 m², which is below the prototype sliver threshold of 2.0 m².',
    toleranceUsed: 2.0,
    resolved: false,
    createdAt: '2026-09-11T12:05:00Z'
  }
];
