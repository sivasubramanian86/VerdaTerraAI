import React, { useEffect, useState } from 'react';

/**
 * Agent Pipeline Visualizer - Shows the multi-agent workflow with state transitions
 * Implements CSS-only animations with data-state attributes
 */
export default function AgentPipeline() {
  const [states, setStates] = useState({
    orchestrator: 'active',
    perception: 'idle',
    hygiene: 'idle',
    policy: 'idle',
    routing: 'idle',
  });

  // Simulate workflow progression
  useEffect(() => {
    const timeline = [
      { delay: 500, update: { orchestrator: 'done', perception: 'active' } },
      { delay: 1200, update: { perception: 'done', hygiene: 'active' } },
      { delay: 1800, update: { hygiene: 'done', policy: 'active' } },
      { delay: 2400, update: { policy: 'done', routing: 'active' } },
      { delay: 3000, update: { routing: 'done' } },
      { delay: 3500, update: { orchestrator: 'idle', perception: 'idle', hygiene: 'idle', policy: 'idle', routing: 'idle' } },
    ];

    timeline.forEach(({ delay, update }) => {
      const timer = setTimeout(() => setStates(s => ({ ...s, ...update })), delay);
      return () => clearTimeout(timer);
    });

    return () => timeline.forEach(({ delay }) => clearTimeout(delay));
  }, []);

  const agents = [
    { id: 'orchestrator', label: 'Orchestrator', emoji: '🧠' },
    { id: 'perception', label: 'Perception', emoji: '👁' },
    { id: 'hygiene', label: 'Hygiene', emoji: '🏥' },
    { id: 'policy', label: 'Policy', emoji: '📋' },
    { id: 'routing', label: 'Routing', emoji: '🗺' },
  ];

  return (
    <section className="agent-pipeline glass-card" aria-label="Agent pipeline status">
      <h3 className="pipeline-title">Multi-Agent Workflow</h3>
      
      <div className="pipeline" role="list" aria-label="Agent pipeline status">
        {agents.map((agent, idx) => (
          <div
            key={agent.id}
            className="pipeline-step"
            id={`step-${agent.id}`}
            data-state={states[agent.id]}
            role="listitem"
            aria-live="polite"
            aria-label={`${agent.label}: ${states[agent.id]}`}
          >
            <div className="step-icon" aria-hidden="true">
              <div className="step-ring"></div>
              <span className="step-emoji">{agent.emoji}</span>
            </div>
            <span className="step-label">{agent.label}</span>
            {idx < agents.length - 1 && <div className="step-connector" aria-hidden="true"></div>}
          </div>
        ))}
      </div>

      <div className="pipeline-legend" role="doc-glossary">
        <div className="legend-item"><span className="legend-dot" style={{ background: 'var(--accent-primary)' }}></span> Active</div>
        <div className="legend-item"><span className="legend-dot" style={{ background: 'var(--accent-teal)' }}></span> Done</div>
        <div className="legend-item"><span className="legend-dot" style={{ background: 'var(--border-subtle)' }}></span> Idle</div>
      </div>
    </section>
  );
}
