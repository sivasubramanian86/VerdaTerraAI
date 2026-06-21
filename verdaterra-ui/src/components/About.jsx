import React from 'react';

export default function About() {
  return (
    <section className="about-panel glass-card">
      <h2>About VerdaTerraAI</h2>
      <p className="muted">VerdaTerraAI is a multi-sensory civic operations assistant designed for local governments and civic teams.</p>
      <ul>
        <li>Multi-sensory fusion: images, smells, water sensors</li>
        <li>Policy-aware routing and guardrails</li>
        <li>Audit logs and analytics export</li>
      </ul>
      <p className="muted">Version: 0.1 (local dev)</p>
    </section>
  );
}
