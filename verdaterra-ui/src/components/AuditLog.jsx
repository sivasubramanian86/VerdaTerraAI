import React, { useEffect, useState } from 'react';

/**
 * AuditLog - Terminal-style log viewer for agent activities and policy decisions
 * Displays monospace logs with level-based coloring (INFO, WARNING, ERROR, SUCCESS)
 */
export default function AuditLog() {
  const [logs, setLogs] = useState([
    { id: 1, level: 'INFO', timestamp: '14:32:05', message: 'Orchestrator initialized' },
    { id: 2, level: 'INFO', timestamp: '14:32:06', message: 'Loaded jurisdiction config: Mumbai' },
    { id: 3, level: 'SUCCESS', timestamp: '14:32:07', message: 'Hygiene model confidence: 94.2%' },
    { id: 4, level: 'INFO', timestamp: '14:32:08', message: 'Policy check: food handler certification' },
    { id: 5, level: 'WARNING', timestamp: '14:32:09', message: 'Outdated water quality report (12 days)' },
    { id: 6, level: 'INFO', timestamp: '14:32:10', message: 'Routing to local authority' },
  ]);

  const [filter, setFilter] = useState('ALL');

  const logLevels = {
    INFO: 'info',
    SUCCESS: 'success',
    WARNING: 'warning',
    ERROR: 'error',
  };

  const filteredLogs = filter === 'ALL' ? logs : logs.filter(log => log.level === filter);

  return (
    <section className="audit-log glass-card" aria-label="Activity audit log">
      <div className="log-header">
        <h3 className="log-title">Audit Log</h3>
        <div className="log-filters">
          {['ALL', 'INFO', 'SUCCESS', 'WARNING', 'ERROR'].map(level => (
            <button
              key={level}
              className={`log-filter-btn ${filter === level ? 'active' : ''}`}
              onClick={() => setFilter(level)}
              aria-pressed={filter === level}
            >
              {level}
            </button>
          ))}
        </div>
      </div>

      <div className="log-container">
        <div className="log-lines" role="log" aria-live="polite" aria-label="Log output">
          {filteredLogs.map(log => (
            <div
              key={log.id}
              className={`log-line log-${logLevels[log.level]}`}
              role="status"
            >
              <span className="log-timestamp">[{log.timestamp}]</span>
              <span className="log-level">{log.level}</span>
              <span className="log-message">{log.message}</span>
            </div>
          ))}
          {filteredLogs.length === 0 && (
            <div className="log-line log-info">
              <span className="log-message">No logs for {filter} level</span>
            </div>
          )}
        </div>
      </div>

      <div className="log-footer">
        <span className="log-count">{filteredLogs.length} entries</span>
        <button className="log-clear-btn" onClick={() => setLogs([])}>
          Clear
        </button>
      </div>
    </section>
  );
}
