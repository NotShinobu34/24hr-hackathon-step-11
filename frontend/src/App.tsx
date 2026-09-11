import React, { useState, useEffect } from 'react';
import { 
  Project, GeoJSONFeature, GeoJSONFeatureCollection, TopologyIssue, 
  LayerVisibilityState, LayerOpacityState, ProcessingMode, FeatureStatus 
} from './types/geoParcel';
import { ApiClient } from './services/api';
import { 
  MOCK_PROJECT, MOCK_PARCELS, MOCK_BUILDINGS, MOCK_ROADS, 
  MOCK_GROUND_TRUTH, MOCK_ISSUES 
} from './services/mockData';
import { TopBar } from './components/TopBar';
import { LayerSidebar } from './components/LayerSidebar';
import { MapLibreCanvas } from './map/MapLibreCanvas';
import { FeatureInspector } from './components/FeatureInspector';
import { ExtractionPanel } from './components/ExtractionPanel';
import { ValidationQueue } from './components/ValidationQueue';
import { GroundTruthSlider } from './components/GroundTruthSlider';
import { ExportModal } from './components/ExportModal';

export const App: React.FC = () => {
  // Application State
  const [project, setProject] = useState<Project>(MOCK_PROJECT);
  const [parcels, setParcels] = useState<GeoJSONFeatureCollection>(MOCK_PARCELS);
  const [buildings, setBuildings] = useState<GeoJSONFeatureCollection>(MOCK_BUILDINGS);
  const [roads, setRoads] = useState<GeoJSONFeatureCollection>(MOCK_ROADS);
  const [groundTruth, setGroundTruth] = useState<GeoJSONFeatureCollection>(MOCK_GROUND_TRUTH);
  const [issues, setIssues] = useState<TopologyIssue[]>(MOCK_ISSUES);

  // Selection & Active Panel
  const [selectedFeature, setSelectedFeature] = useState<GeoJSONFeature | null>(null);
  const [selectedIssueId, setSelectedIssueId] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'review' | 'inspect' | 'extract'>('review');

  // Editing State
  const [isEditing, setIsEditing] = useState<boolean>(false);
  const [focusTarget, setFocusTarget] = useState<{ center: [number, number]; zoom?: number } | null>(null);

  // Progress & Modal State
  const [isValidating, setIsValidating] = useState<boolean>(false);
  const [isExtracting, setIsExtracting] = useState<boolean>(false);
  const [extractionProgress, setExtractionProgress] = useState<number>(0);
  const [activeMode, setActiveMode] = useState<ProcessingMode>('cv_baseline');
  const [isExportModalOpen, setIsExportModalOpen] = useState<boolean>(false);

  // Layer Controls
  const [visibility, setVisibility] = useState<LayerVisibilityState>({
    imagery: true,
    parcels: true,
    buildings: true,
    roads: true,
    groundTruth: false,
    issues: true
  });

  const [opacity, setOpacity] = useState<LayerOpacityState>({
    imagery: 0.90,
    parcels: 0.85,
    buildings: 0.90,
    roads: 1.0,
    groundTruth: 0.60
  });

  // Initial Data Fetch
  useEffect(() => {
    const initData = async () => {
      try {
        const proj = await ApiClient.getProject('project-001');
        setProject(proj);

        const feats = await ApiClient.getFeatures('project-001');
        if (feats.features.length > 0) {
          setParcels({
            type: 'FeatureCollection',
            features: feats.features.filter(f => f.featureType === 'parcel')
          });
          setBuildings({
            type: 'FeatureCollection',
            features: feats.features.filter(f => f.featureType === 'building')
          });
          setRoads({
            type: 'FeatureCollection',
            features: feats.features.filter(f => f.featureType === 'road')
          });
        }
      } catch (err) {
        console.log('Using pre-seeded offline fixtures');
      }
    };
    initData();
  }, []);

  // Layer Handlers
  const handleToggleVisibility = (layer: keyof LayerVisibilityState) => {
    setVisibility(prev => ({ ...prev, [layer]: !prev[layer] }));
  };

  const handleChangeOpacity = (layer: keyof LayerOpacityState, value: number) => {
    setOpacity(prev => ({ ...prev, [layer]: value }));
  };

  // Run Extraction
  const handleExtract = async (types: string[], mode: ProcessingMode) => {
    setIsExtracting(true);
    setExtractionProgress(0.15);
    setActiveMode(mode);

    try {
      const res = await ApiClient.startExtraction(project.id, types, mode);
      setExtractionProgress(0.5);

      // Poll progress simulation or live API
      setTimeout(async () => {
        setExtractionProgress(0.85);
        const job = await ApiClient.pollJob(project.id, res.jobId);
        setExtractionProgress(1.0);

        // Fetch fresh features
        const fresh = await ApiClient.getFeatures(project.id);
        if (fresh.features.length > 0) {
          setParcels({
            type: 'FeatureCollection',
            features: fresh.features.filter(f => f.featureType === 'parcel')
          });
          setBuildings({
            type: 'FeatureCollection',
            features: fresh.features.filter(f => f.featureType === 'building')
          });
          setRoads({
            type: 'FeatureCollection',
            features: fresh.features.filter(f => f.featureType === 'road')
          });
        }

        setIsExtracting(false);
        // Automatically run validation to find any candidate issues
        handleValidate();
      }, 1000);
    } catch (err) {
      console.error(err);
      setIsExtracting(false);
    }
  };

  // Run Topology Validation
  const handleValidate = async () => {
    setIsValidating(true);
    try {
      const res = await ApiClient.validateTopology(
        project.id,
        project.parameters.overlapToleranceM2,
        project.parameters.sliverThresholdM2
      );
      setIssues(res.issues);
      if (res.issues.length > 0) {
        setActiveTab('review');
      }
    } catch (err) {
      console.error(err);
    } finally {
      setIsValidating(false);
    }
  };

  // Zoom to Topology Issue
  const handleSelectIssue = (issue: TopologyIssue) => {
    setSelectedIssueId(issue.id);
    const targetFeat = parcels.features.find(f => f.id === issue.featureId);
    if (targetFeat && targetFeat.geometry.type === 'Polygon') {
      setSelectedFeature(targetFeat);
      setActiveTab('inspect');

      // Focus camera on first coordinate
      const coords = targetFeat.geometry.coordinates[0];
      const center: [number, number] = [coords[0][0], coords[0][1]];
      setFocusTarget({ center, zoom: 18.5 });
    }
  };

  // Save Geometry Edit (Surveyor drags vertex to correct overlap)
  const handleSaveGeometry = async (featureId: string, updatedCoordinates: any) => {
    const updatedGeom = {
      type: 'Polygon',
      coordinates: updatedCoordinates
    };

    // Update in-memory parcels immediately for instant UI feedback
    setParcels(prev => ({
      ...prev,
      features: prev.features.map(f => {
        if (f.id === featureId) {
          return {
            ...f,
            geometry: updatedGeom as any,
            properties: {
              ...f.properties,
              edited: true,
              status: 'corrected'
            }
          };
        }
        return f;
      })
    }));

    if (selectedFeature && selectedFeature.id === featureId) {
      setSelectedFeature(prev => prev ? {
        ...prev,
        geometry: updatedGeom as any,
        properties: { ...prev.properties, edited: true, status: 'corrected' }
      } : null);
    }

    try {
      await ApiClient.patchFeature(project.id, featureId, updatedGeom);
      // Automatically re-run validation to verify if the issue was resolved!
      const valRes = await ApiClient.validateTopology(
        project.id,
        project.parameters.overlapToleranceM2,
        project.parameters.sliverThresholdM2
      );
      setIssues(valRes.issues);
    } catch (err) {
      console.error(err);
    }
  };

  // Verify Feature
  const handleVerify = async (featureId: string, status: FeatureStatus) => {
    try {
      await ApiClient.verifyFeature(project.id, featureId, status);
      setParcels(prev => ({
        ...prev,
        features: prev.features.map(f => {
          if (f.id === featureId) {
            return {
              ...f,
              properties: { ...f.properties, status, verified: status === 'verified' }
            };
          }
          return f;
        })
      }));

      if (selectedFeature && selectedFeature.id === featureId) {
        setSelectedFeature(prev => prev ? {
          ...prev,
          properties: { ...prev.properties, status, verified: status === 'verified' }
        } : null);
      }
    } catch (err) {
      console.error(err);
    }
  };

  // Export Data
  const handleExport = async (include: string[]) => {
    return await ApiClient.exportData(project.id, include);
  };

  // Active Issue message for selected feature
  const activeIssue = issues.find(i => !i.resolved && (i.featureId === selectedFeature?.id || i.relatedFeatureId === selectedFeature?.id));

  return (
    <div className="app-container" style={{ width: '100vw', height: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* TopBar */}
      <TopBar 
        project={project}
        onValidate={handleValidate}
        onOpenExport={() => setIsExportModalOpen(true)}
        isValidating={isValidating}
        issueCount={issues.filter(i => !i.resolved).length}
      />

      {/* Workspace Grid */}
      <div className="gis-workspace">
        {/* Left Sidebar: Layers & Opacities */}
        <LayerSidebar 
          visibility={visibility}
          opacity={opacity}
          onToggleVisibility={handleToggleVisibility}
          onChangeOpacity={handleChangeOpacity}
          counts={{
            parcels: parcels.features.length,
            buildings: buildings.features.length,
            roads: roads.features.length,
            groundTruth: groundTruth.features.length,
            issues: issues.filter(i => !i.resolved).length
          }}
        />

        {/* Center: WebGIS Map Canvas */}
        <main className="map-canvas-container">
          <MapLibreCanvas 
            parcels={parcels}
            buildings={buildings}
            roads={roads}
            groundTruth={groundTruth}
            issues={issues}
            visibility={visibility}
            opacity={opacity}
            selectedFeature={selectedFeature}
            onSelectFeature={(feat) => {
              setSelectedFeature(feat);
              if (feat) setActiveTab('inspect');
            }}
            isEditing={isEditing}
            onSaveGeometry={handleSaveGeometry}
            focusTarget={focusTarget}
          />
        </main>

        {/* Right Sidebar: AI Extraction, Review Queue & Feature Inspector */}
        <aside className="gis-sidebar right-sidebar">
          {/* Tabs */}
          <div className="right-panel-tabs">
            <button 
              className={`tab-btn ${activeTab === 'review' ? 'active' : ''}`}
              onClick={() => setActiveTab('review')}
            >
              Review Queue ({issues.filter(i => !i.resolved).length})
            </button>
            <button 
              className={`tab-btn ${activeTab === 'inspect' ? 'active' : ''}`}
              onClick={() => setActiveTab('inspect')}
            >
              Feature Inspector
            </button>
            <button 
              className={`tab-btn ${activeTab === 'extract' ? 'active' : ''}`}
              onClick={() => setActiveTab('extract')}
            >
              AI Extraction
            </button>
          </div>

          <div className="panel-content-scroll">
            {/* Ground Truth Comparison Widget */}
            <GroundTruthSlider 
              isVisible={visibility.groundTruth}
              opacity={opacity.groundTruth}
              onToggle={() => handleToggleVisibility('groundTruth')}
              onChangeOpacity={(val) => handleChangeOpacity('groundTruth', val)}
            />

            {/* Tab: Review Queue */}
            {activeTab === 'review' && (
              <ValidationQueue 
                issues={issues}
                onSelectIssue={handleSelectIssue}
                selectedIssueId={selectedIssueId}
              />
            )}

            {/* Tab: Feature Inspector */}
            {activeTab === 'inspect' && (
              <FeatureInspector 
                feature={selectedFeature}
                onClose={() => setSelectedFeature(null)}
                isEditing={isEditing}
                onToggleEdit={() => setIsEditing(!isEditing)}
                onVerify={handleVerify}
                activeIssueMessage={activeIssue?.message}
              />
            )}

            {/* Tab: AI Extraction */}
            {activeTab === 'extract' && (
              <ExtractionPanel 
                onExtract={handleExtract}
                isProcessing={isExtracting}
                progress={extractionProgress}
                activeMode={activeMode}
              />
            )}
          </div>
        </aside>
      </div>

      {/* Export Modal */}
      <ExportModal 
        isOpen={isExportModalOpen}
        onClose={() => setIsExportModalOpen(false)}
        onExport={handleExport}
        totalParcels={parcels.features.length}
        totalBuildings={buildings.features.length}
        totalRoads={roads.features.length}
      />
    </div>
  );
};
