import React from 'react';

export default function InspectorView() {
  return (
    <section className="glass-card inspector-card" aria-labelledby="queue-title">
      <h2 id="queue-title">Routing & Governance Queue</h2>

      <article className="queue-item queue-critical" aria-labelledby="restaurant-risk-title">
        <div className="queue-heading">
          <h3 id="restaurant-risk-title">High Risk: Restaurant Kitchen</h3>
          <span className="status-pill status-critical">Escalated: Zonal Commissioner</span>
        </div>
        <p>Violation Detected: Ammonia levels do not meet Swachh Bharat norms.</p>
        <section className="sop-panel" aria-labelledby="restaurant-sop-title">
          <h4 id="restaurant-sop-title">Remediation SOP</h4>
          <ul>
            <li>Clean facility immediately</li>
            <li>Test ammonia levels below 50 ppm</li>
            <li>Log closure only after threshold compliance is verified</li>
          </ul>
        </section>
      </article>

      <article className="queue-item" aria-labelledby="water-risk-title">
        <div className="queue-heading">
          <h3 id="water-risk-title">Water Anomaly: Sector 4</h3>
          <span className="status-pill status-info">Routed: Water Board</span>
        </div>
        <p>Automated complaint routed to Water Board. Immediate action requested.</p>
      </article>
    </section>
  );
}
