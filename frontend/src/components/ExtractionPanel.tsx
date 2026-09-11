import React, { useState } from 'react';
import { ProcessingMode } from '../types/geoParcel';
import { Cpu, Play, CheckSquare, Sparkles } from 'lucide-react';

interface ExtractionPanelProps {
  onExtract: (features: string[], mode: ProcessingMode) => void;
  isProcessing: boolean;
  progress: number;
  activeMode: ProcessingMode;
}

export const ExtractionPanel: React.FC<ExtractionPanelProps> = ({
  onExtract,
  isProcessing,
  progress,
  activeMode
}) => {
  const [selectedTypes, setSelectedTypes] = useState<string[]>(['parcel', 'building', 'road']);
  const [mode, setMode] = useState<ProcessingMode>(activeMode || 'cv_baseline');

  const toggleType = (type: string) => {
    if (selectedTypes.includes(type)) {
      if (selectedTypes.length > 1) {
        setSelectedTypes(selectedTypes.filter(t => t !== type));
      }
    } else {
      setSelectedTypes([...selectedTypes, type]);
    }
  };

  const handleRun = () => {
    onExtract(selectedTypes, mode);
  };

  return (
    <div className="extraction-panel">
      <div className="panel-title-row">
        <div className="panel-title">
          <Cpu size={18} />
          <h3>AI-Assisted Extraction</h3>
        </div>
        <span className="mode-badge">
          {mode === 'demo_fixture' ? 'Demo Fixture' : mode === 'cv_baseline' ? 'OpenCV Baseline' : 'Live Inference'}
        </span>
      </div>

      <div className="extraction-source-info">
        <span className="source-label">Active Imagery:</span>
        <span className="source-value">sample_ortho.jpg (Ward 12 UAV)</span>
      </div>

      <div className="feature-selection-row">
        <label className="checkbox-label">
          <input 
            type="checkbox" 
            checked={selectedTypes.includes('parcel')} 
            onChange={() => toggleType('parcel')}
            disabled={isProcessing}
          />
          <span>Parcels</span>
        </label>
        <label className="checkbox-label">
          <input 
            type="checkbox" 
            checked={selectedTypes.includes('building')} 
            onChange={() => toggleType('building')}
            disabled={isProcessing}
          />
          <span>Buildings</span>
        </label>
        <label className="checkbox-label">
          <input 
            type="checkbox" 
            checked={selectedTypes.includes('road')} 
            onChange={() => toggleType('road')}
            disabled={isProcessing}
          />
          <span>Roads</span>
        </label>
      </div>

      <div className="mode-selector-group">
        <label>Extraction Engine Mode:</label>
        <select 
          value={mode} 
          onChange={(e) => setMode(e.target.value as ProcessingMode)}
          disabled={isProcessing}
        >
          <option value="cv_baseline">Deterministic CV Baseline (OpenCV)</option>
          <option value="demo_fixture">Curated Demo Fixture (High Resilience)</option>
          <option value="model_inference">Pretrained Neural Model Adapter</option>
        </select>
      </div>

      {isProcessing && (
        <div className="progress-section">
          <div className="progress-info">
            <span>Extracting boundary candidates...</span>
            <span>{Math.round(progress * 100)}%</span>
          </div>
          <div className="progress-bar-track">
            <div className="progress-bar-fill" style={{ width: `${Math.round(progress * 100)}%` }} />
          </div>
        </div>
      )}

      <button 
        className="btn btn-primary btn-block"
        onClick={handleRun}
        disabled={isProcessing}
      >
        {isProcessing ? (
          <>
            <span className="spinner"></span>
            Processing Imagery...
          </>
        ) : (
          <>
            <Play size={15} />
            Run Extraction Pipeline
          </>
        )}
      </button>
    </div>
  );
};
