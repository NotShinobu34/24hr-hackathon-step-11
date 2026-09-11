import React from 'react';
import { Project, ProjectStatus } from '../types/geoParcel';
import { Layers, ShieldCheck, Download, CheckCircle2, AlertTriangle } from 'lucide-react';

interface TopBarProps {
  project: Project;
  onValidate: () => void;
  onOpenExport: () => void;
  isValidating: boolean;
  issueCount: number;
}

export const TopBar: React.FC<TopBarProps> = ({
  project,
  onValidate,
  onOpenExport,
  isValidating,
  issueCount
}) => {
  const getStatusBadge = (status: ProjectStatus) => {
    switch (status) {
      case 'verified':
        return <span className="badge badge-success"><CheckCircle2 size={13} /> Verified</span>;
      case 'review':
        return <span className="badge badge-warning"><AlertTriangle size={13} /> Review Required</span>;
      case 'processing':
        return <span className="badge badge-info">Processing</span>;
      default:
        return <span className="badge badge-secondary">Draft</span>;
    }
  };

  return (
    <header className="gis-topbar">
      <div className="topbar-left">
        <div className="brand">
          <Layers className="brand-icon" size={22} />
          <div>
            <span className="brand-title">GeoParcel AI</span>
            <span className="brand-subtitle">Cadastral Field Verification Workstation</span>
          </div>
        </div>

        <div className="project-metadata">
          <span className="project-name">{project.name}</span>
          {getStatusBadge(project.status)}
          <span className="crs-pill">CRS: {project.metricCrs || 'EPSG:32643'}</span>
        </div>
      </div>

      <div className="topbar-right">
        <button 
          className={`btn btn-outline ${issueCount > 0 ? 'btn-issue-alert' : ''}`}
          onClick={onValidate}
          disabled={isValidating}
          title="Run deterministic topology checks"
        >
          <ShieldCheck size={16} />
          {isValidating ? 'Validating...' : `Validate Topology ${issueCount > 0 ? `(${issueCount})` : ''}`}
        </button>

        <button 
          className="btn btn-primary"
          onClick={onOpenExport}
          title="Export validated GeoJSON"
        >
          <Download size={16} />
          Export GIS Data
        </button>
      </div>
    </header>
  );
};
