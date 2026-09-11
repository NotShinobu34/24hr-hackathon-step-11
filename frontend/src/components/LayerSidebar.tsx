import React from 'react';
import { LayerVisibilityState, LayerOpacityState } from '../types/geoParcel';
import { Eye, EyeOff, Layers, Sliders } from 'lucide-react';
import { LAYER_COLORS } from '../map/layerStyles';

interface LayerSidebarProps {
  visibility: LayerVisibilityState;
  opacity: LayerOpacityState;
  onToggleVisibility: (layer: keyof LayerVisibilityState) => void;
  onChangeOpacity: (layer: keyof LayerOpacityState, value: number) => void;
  counts: {
    parcels: number;
    buildings: number;
    roads: number;
    groundTruth: number;
    issues: number;
  };
}

export const LayerSidebar: React.FC<LayerSidebarProps> = ({
  visibility,
  opacity,
  onToggleVisibility,
  onChangeOpacity,
  counts
}) => {
  return (
    <aside className="gis-sidebar left-sidebar">
      <div className="sidebar-header">
        <Layers size={18} />
        <h2>Map Layers</h2>
      </div>

      <div className="layer-list">
        {/* Drone Imagery */}
        <div className="layer-card">
          <div className="layer-header">
            <button 
              className="layer-toggle-btn"
              onClick={() => onToggleVisibility('imagery')}
              title={visibility.imagery ? 'Hide raster' : 'Show raster'}
            >
              {visibility.imagery ? <Eye size={16} className="text-primary" /> : <EyeOff size={16} className="text-muted" />}
            </button>
            <span className="layer-title">High-Res Orthophoto</span>
            <span className="layer-badge">0.10m GSD</span>
          </div>
          {visibility.imagery && (
            <div className="layer-slider-row">
              <Sliders size={12} />
              <input 
                type="range" 
                min="0.1" 
                max="1" 
                step="0.05"
                value={opacity.imagery}
                onChange={(e) => onChangeOpacity('imagery', parseFloat(e.target.value))}
              />
              <span>{Math.round(opacity.imagery * 100)}%</span>
            </div>
          )}
        </div>

        {/* Parcels */}
        <div className="layer-card">
          <div className="layer-header">
            <button 
              className="layer-toggle-btn"
              onClick={() => onToggleVisibility('parcels')}
            >
              {visibility.parcels ? <Eye size={16} className="text-primary" /> : <EyeOff size={16} className="text-muted" />}
            </button>
            <div className="color-indicator" style={{ backgroundColor: LAYER_COLORS.parcel.fill, borderColor: LAYER_COLORS.parcel.stroke }} />
            <span className="layer-title">Cadastral Parcels</span>
            <span className="count-pill">{counts.parcels}</span>
          </div>
          {visibility.parcels && (
            <div className="layer-slider-row">
              <Sliders size={12} />
              <input 
                type="range" 
                min="0.1" 
                max="1" 
                step="0.05"
                value={opacity.parcels}
                onChange={(e) => onChangeOpacity('parcels', parseFloat(e.target.value))}
              />
              <span>{Math.round(opacity.parcels * 100)}%</span>
            </div>
          )}
        </div>

        {/* Buildings */}
        <div className="layer-card">
          <div className="layer-header">
            <button 
              className="layer-toggle-btn"
              onClick={() => onToggleVisibility('buildings')}
            >
              {visibility.buildings ? <Eye size={16} className="text-primary" /> : <EyeOff size={16} className="text-muted" />}
            </button>
            <div className="color-indicator" style={{ backgroundColor: LAYER_COLORS.building.fill, borderColor: LAYER_COLORS.building.stroke }} />
            <span className="layer-title">Building Footprints</span>
            <span className="count-pill">{counts.buildings}</span>
          </div>
          {visibility.buildings && (
            <div className="layer-slider-row">
              <Sliders size={12} />
              <input 
                type="range" 
                min="0.1" 
                max="1" 
                step="0.05"
                value={opacity.buildings}
                onChange={(e) => onChangeOpacity('buildings', parseFloat(e.target.value))}
              />
              <span>{Math.round(opacity.buildings * 100)}%</span>
            </div>
          )}
        </div>

        {/* Roads */}
        <div className="layer-card">
          <div className="layer-header">
            <button 
              className="layer-toggle-btn"
              onClick={() => onToggleVisibility('roads')}
            >
              {visibility.roads ? <Eye size={16} className="text-primary" /> : <EyeOff size={16} className="text-muted" />}
            </button>
            <div className="color-indicator road-indicator" />
            <span className="layer-title">Access Corridors</span>
            <span className="count-pill">{counts.roads}</span>
          </div>
        </div>

        {/* Ground Truth Reference */}
        <div className="layer-card reference-layer-card">
          <div className="layer-header">
            <button 
              className="layer-toggle-btn"
              onClick={() => onToggleVisibility('groundTruth')}
            >
              {visibility.groundTruth ? <Eye size={16} className="text-success" /> : <EyeOff size={16} className="text-muted" />}
            </button>
            <div className="color-indicator gt-indicator" />
            <span className="layer-title">Official Ground Truth</span>
            <span className="count-pill badge-success">{counts.groundTruth}</span>
          </div>
          {visibility.groundTruth && (
            <div className="layer-slider-row">
              <Sliders size={12} />
              <input 
                type="range" 
                min="0.1" 
                max="1" 
                step="0.05"
                value={opacity.groundTruth}
                onChange={(e) => onChangeOpacity('groundTruth', parseFloat(e.target.value))}
              />
              <span>{Math.round(opacity.groundTruth * 100)}%</span>
            </div>
          )}
        </div>

        {/* Topology Issues Layer */}
        {counts.issues > 0 && (
          <div className="layer-card issue-layer-card">
            <div className="layer-header">
              <button 
                className="layer-toggle-btn"
                onClick={() => onToggleVisibility('issues')}
              >
                {visibility.issues ? <Eye size={16} className="text-danger" /> : <EyeOff size={16} className="text-muted" />}
              </button>
              <div className="color-indicator issue-indicator" />
              <span className="layer-title">Topology Issues</span>
              <span className="count-pill badge-danger">{counts.issues}</span>
            </div>
          </div>
        )}
      </div>

      <div className="sidebar-footer">
        <div className="system-badge">
          <span>Engine: <strong>GeoParcel Shapely v2</strong></span>
          <span>Interchange: <strong>RFC 7946</strong></span>
        </div>
      </div>
    </aside>
  );
};
