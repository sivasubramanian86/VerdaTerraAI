import React from 'react';

export default function Dashboard() {
  return (
    <section aria-labelledby="dashboard-title">
      <h2 id="dashboard-title">Area: Bengaluru (loc_bengaluru)</h2>
      <div className="grid grid-cols-3 metrics-grid" aria-label="Current hygiene metrics">
        <article className="glass-card metric-card">
          <h3>Hygiene Score</h3>
          <div className="metric-value metric-success" aria-label="Hygiene score 82 out of 100">82</div>
          <p>Status: Improving</p>
        </article>
        <article className="glass-card metric-card">
          <h3>Open Incidents</h3>
          <div className="metric-value metric-warning" aria-label="Three open incidents">3</div>
          <p>Requires Action</p>
        </article>
        <article className="glass-card metric-card">
          <h3>Odor Index</h3>
          <div className="metric-value metric-info" aria-label="Odor index 4.2">4.2</div>
          <p>Acceptable Range</p>
        </article>
      </div>

      <section className="glass-card map-panel" aria-labelledby="map-title">
        <h3 id="map-title">Hotspot Map</h3>
        <p>Connects to the protected hotspot API for sanitized ward-level risk overlays.</p>
      </section>
    </section>
  );
}
