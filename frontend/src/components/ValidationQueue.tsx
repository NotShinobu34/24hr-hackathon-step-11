import React from 'react';
import { TopologyIssue } from '../types/geoParcel';
import { AlertCircle, ShieldAlert, CheckCircle, Crosshair, ArrowRight } from 'lucide-react';

interface ValidationQueueProps {
  issues: TopologyIssue[];
  onSelectIssue: (issue: TopologyIssue) => void;
  selectedIssueId?: string | null;
}

export const ValidationQueue: React.FC<ValidationQueueProps> = ({
  issues,
  onSelectIssue,
  selectedIssueId
}) => {
  const unresolvedIssues = issues.filter(i => !i.resolved);

  if (unresolvedIssues.length === 0) {
    return (
      <div className="validation-queue-clean">
        <CheckCircle size={28} className="text-success" />
        <div>
          <h4>Topology Clean</h4>
          <p>No overlaps, self-intersections, or slivers detected with current prototype tolerances.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="validation-queue">
      <div className="queue-header">
        <div className="queue-title">
          <ShieldAlert size={18} className="text-danger" />
          <h3>Topology Review Queue</h3>
        </div>
        <span className="badge badge-danger">{unresolvedIssues.length} issues</span>
      </div>

      <p className="queue-description">
        Cadastral parcels requiring human surveyor verification or boundary adjustment before export:
      </p>

      <div className="issue-cards-list">
        {unresolvedIssues.map(issue => (
          <div 
            key={issue.id} 
            className={`issue-card severity-${issue.severity} ${selectedIssueId === issue.id ? 'issue-selected' : ''}`}
            onClick={() => onSelectIssue(issue)}
          >
            <div className="issue-card-top">
              <span className={`severity-tag severity-${issue.severity}`}>
                {issue.severity.toUpperCase()}
              </span>
              <span className="issue-type-tag">{issue.issueType.replace('_', ' ').toUpperCase()}</span>
            </div>

            <p className="issue-message">{issue.message}</p>

            <div className="issue-card-footer">
              <span className="issue-target">Target: <strong>{issue.featureId}</strong></span>
              <button className="btn-zoom-issue" title="Zoom to issue on map">
                <Crosshair size={13} />
                Zoom to Conflict
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
