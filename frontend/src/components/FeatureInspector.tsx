import React from 'react';
import { GeoJSONFeature, FeatureStatus } from '../types/geoParcel';
import { X, CheckCircle2, Edit3, ShieldAlert, FileText, Info } from 'lucide-react';

interface FeatureInspectorProps {
  feature: GeoJSONFeature | null;
  onClose: () => void;
  isEditing: boolean;
  onToggleEdit: () => void;
  onVerify: (featureId: string, status: FeatureStatus) => void;
  activeIssueMessage?: string;
}

export const FeatureInspector: React.FC<FeatureInspectorProps> = ({
  feature,
  onClose,
  isEditing,
  onToggleEdit,
  onVerify,
  activeIssueMessage
}) => {
  if (!feature) {
    return (
      <div className="inspector-empty-state">
        <Info size={32} className="text-muted" />
        <p>Click any parcel or building on the map to inspect boundary metadata, provenance, and topology status.</p>
      </div>
    );
  }

  const { properties } = feature;
  const confidencePercent = properties.confidence ? Math.round(properties.confidence * 100) : 90;

  return (
    <div className="feature-inspector">
      <div className="inspector-header">
        <div>
          <span className="feature-type-tag">{feature.featureType?.toUpperCase() || 'PARCEL'}</span>
          <h3 className="feature-id">{feature.id}</h3>
        </div>
        <button className="btn-icon" onClick={onClose} title="Close inspector">
          <X size={18} />
        </button>
      </div>

      {/* Active Topology Alert Banner if this feature has an issue */}
      {activeIssueMessage && (
        <div className="inspector-alert">
          <ShieldAlert size={16} />
          <div>
            <strong>Topology Issue Detected</strong>
            <p>{activeIssueMessage}</p>
          </div>
        </div>
      )}

      {/* Primary Metrics Grid */}
      <div className="metric-grid">
        <div className="metric-card">
          <span className="metric-label">Calculated Area</span>
          <span className="metric-value">{properties.area_m2 ? `${properties.area_m2.toLocaleString()} m²` : '—'}</span>
        </div>
        <div className="metric-card">
          <span className="metric-label">Perimeter</span>
          <span className="metric-value">{properties.perimeter_m ? `${properties.perimeter_m.toLocaleString()} m` : '—'}</span>
        </div>
        <div className="metric-card">
          <span className="metric-label">AI Confidence</span>
          <span className="metric-value text-primary">{confidencePercent}%</span>
          <span className="metric-subtext">Method: {properties.confidenceType || 'heuristic'}</span>
        </div>
        <div className="metric-card">
          <span className="metric-label">Review Status</span>
          <span className={`status-pill status-${properties.status}`}>
            {properties.status.toUpperCase()}
          </span>
        </div>
      </div>

      {/* Provenance Details */}
      <div className="provenance-section">
        <h4><FileText size={14} /> Provenance & Audit Trail</h4>
        <dl className="provenance-list">
          <div>
            <dt>Data Source:</dt>
            <dd>{properties.source.toUpperCase()}</dd>
          </div>
          <div>
            <dt>Processing Mode:</dt>
            <dd className="badge badge-secondary">{properties.processingMode}</dd>
          </div>
          <div>
            <dt>Source Asset:</dt>
            <dd className="mono">{properties.sourceAssetId || 'asset-ortho-001'}</dd>
          </div>
          <div>
            <dt>Metric CRS:</dt>
            <dd className="mono">{properties.metricCrs || 'EPSG:32643'}</dd>
          </div>
          <div>
            <dt>Human Edited:</dt>
            <dd>{properties.edited ? 'Yes (Surveyor Adjusted)' : 'No (Raw AI Candidate)'}</dd>
          </div>
        </dl>
      </div>

      {/* Action Buttons */}
      <div className="inspector-actions">
        <button 
          className={`btn ${isEditing ? 'btn-warning' : 'btn-outline'}`}
          onClick={onToggleEdit}
        >
          <Edit3 size={15} />
          {isEditing ? 'Finish Vertex Editing' : 'Edit Boundary Geometry'}
        </button>

        <button 
          className="btn btn-success"
          onClick={() => onVerify(feature.id, 'verified')}
          disabled={properties.status === 'verified'}
        >
          <CheckCircle2 size={15} />
          {properties.status === 'verified' ? 'Verified' : 'Mark as Field Verified'}
        </button>
      </div>
    </div>
  );
};
