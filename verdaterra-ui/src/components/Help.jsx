import React from 'react';

export default function Help() {
  return (
    <section className="help-panel glass-card">
      <h2>Help & FAQ</h2>
      <h3>How do I submit a report?</h3>
      <p className="muted">Use the Report Issue screen or the API endpoint `/api/v1/incidents/submit` with `X-API-Key`.</p>
      <h3>How do I run locally?</h3>
      <p className="muted">Use the `scripts/run-backend.*` and `scripts/run-frontend.*` helpers included in the repo.</p>
      <h3>Privacy & Guardrails</h3>
      <p className="muted">PII is sanitized by default. See the guardrails documentation in the repo.</p>
    </section>
  );
}
