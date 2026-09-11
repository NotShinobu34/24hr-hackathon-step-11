import React from 'react';
import { Eye, Sliders, CheckCheck } from 'lucide-react';

interface GroundTruthSliderProps {
  isVisible: boolean;
  opacity: number;
  onToggle: () => void;
  onChangeOpacity: (val: number) => void;
}

export const GroundTruthSlider: React.FC<GroundTruthSliderProps> = ({
  isVisible,
  opacity,
  onToggle,
  onChangeOpacity
}) => {
  return (
    <div className="ground-truth-slider-card">
      <div className="gt-header">
        <div className="gt-title">
          <CheckCheck size={16} className="text-success" />
          <span>Ground Truth Comparison</span>
        </div>
        <button 
          className={`btn-sm ${isVisible ? 'btn-success' : 'btn-outline'}`}
          onClick={onToggle}
        >
          <Eye size={13} />
          {isVisible ? 'Enabled' : 'Disabled'}
        </button>
      </div>

      {isVisible && (
        <div className="gt-controls">
          <div className="gt-slider-row">
            <Sliders size={13} />
            <span className="slider-label">Reference Opacity:</span>
            <input 
              type="range"
              min="0.05"
              max="1"
              step="0.05"
              value={opacity}
              onChange={(e) => onChangeOpacity(parseFloat(e.target.value))}
            />
            <span className="slider-val">{Math.round(opacity * 100)}%</span>
          </div>
          <span className="gt-help-text">
            Comparing preliminary AI parcels against registered municipal survey records (Ward 12 Truth Layer).
          </span>
        </div>
      )}
    </div>
  );
};
