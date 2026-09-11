import React, { useState } from 'react';
import { X, Download, FileCheck, Check } from 'lucide-react';

interface ExportModalProps {
  isOpen: boolean;
  onClose: () => void;
  onExport: (include: string[]) => Promise<{ downloadUrl?: string; featureCount: number }>;
  totalParcels: number;
  totalBuildings: number;
  totalRoads: number;
}

export const ExportModal: React.FC<ExportModalProps> = ({
  isOpen,
  onClose,
  onExport,
  totalParcels,
  totalBuildings,
  totalRoads
}) => {
  const [include, setInclude] = useState<string[]>(['parcel', 'building', 'road']);
  const [isExporting, setIsExporting] = useState(false);
  const [downloadUrl, setDownloadUrl] = useState<string | null>(null);
  const [exportedCount, setExportedCount] = useState<number>(0);

  if (!isOpen) return null;

  const toggleLayer = (layer: string) => {
    if (include.includes(layer)) {
      if (include.length > 1) {
        setInclude(include.filter(l => l !== layer));
      }
    } else {
      setInclude([...include, layer]);
    }
  };

  const handleExport = async () => {
    setIsExporting(true);
    try {
      const res = await onExport(include);
      setDownloadUrl(res.downloadUrl || '#');
      setExportedCount(res.featureCount);
    } catch (err) {
      console.error(err);
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <div className="modal-backdrop">
      <div className="modal-card">
        <div className="modal-header">
          <div className="modal-title">
            <Download size={20} className="text-primary" />
            <h3>Export GIS-Ready Dataset</h3>
          </div>
          <button className="btn-icon" onClick={onClose} title="Close modal">
            <X size={18} />
          </button>
        </div>

        <div className="modal-body">
          <p className="modal-desc">
            Generate an RFC 7946-compliant GeoJSON FeatureCollection containing all validated geometry, area measurements, and surveyor audit trails.
          </p>

          <div className="form-group">
            <label className="form-label">Export Format:</label>
            <div className="radio-pill active">
              <FileCheck size={16} />
              <div>
                <strong>GeoJSON (RFC 7946)</strong>
                <span>Universal GIS standard, WGS84 coordinates</span>
              </div>
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Select Layers to Include:</label>
            <div className="checkbox-list">
              <label className="checkbox-item">
                <input 
                  type="checkbox" 
                  checked={include.includes('parcel')} 
                  onChange={() => toggleLayer('parcel')}
                />
                <span>Cadastral Parcels ({totalParcels} features)</span>
              </label>
              <label className="checkbox-item">
                <input 
                  type="checkbox" 
                  checked={include.includes('building')} 
                  onChange={() => toggleLayer('building')}
                />
                <span>Building Footprints ({totalBuildings} features)</span>
              </label>
              <label className="checkbox-item">
                <input 
                  type="checkbox" 
                  checked={include.includes('road')} 
                  onChange={() => toggleLayer('road')}
                />
                <span>Access Corridors ({totalRoads} features)</span>
              </label>
            </div>
          </div>

          {downloadUrl && (
            <div className="export-success-banner">
              <Check size={18} className="text-success" />
              <div>
                <strong>Export Package Ready</strong>
                <p>{exportedCount} features packaged successfully.</p>
                <a 
                  href={downloadUrl} 
                  download="ward12_cadastral_export.geojson" 
                  className="btn btn-success btn-sm mt-2"
                >
                  <Download size={14} /> Download File Now
                </a>
              </div>
            </div>
          )}
        </div>

        <div className="modal-footer">
          <button className="btn btn-outline" onClick={onClose}>Cancel</button>
          {!downloadUrl ? (
            <button 
              className="btn btn-primary" 
              onClick={handleExport}
              disabled={isExporting}
            >
              {isExporting ? 'Packaging...' : 'Generate GeoJSON Package'}
            </button>
          ) : (
            <button className="btn btn-primary" onClick={onClose}>Done</button>
          )}
        </div>
      </div>
    </div>
  );
};
