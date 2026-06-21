import React, { useEffect, useState } from 'react';

function Icon({ name }) {
  // simple inline SVG icons by name
  switch (name) {
    case 'dashboard':
      return <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="3" y="3" width="8" height="8" rx="1" stroke="currentColor" strokeWidth="1.2"/><rect x="13" y="3" width="8" height="5" rx="1" stroke="currentColor" strokeWidth="1.2"/><rect x="13" y="10" width="8" height="11" rx="1" stroke="currentColor" strokeWidth="1.2"/><rect x="3" y="13" width="8" height="8" rx="1" stroke="currentColor" strokeWidth="1.2"/></svg>;
    case 'report':
      return <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M4 7h16" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round"/><path d="M4 12h16" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round"/><path d="M4 17h10" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round"/></svg>;
    case 'inspector':
      return <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><circle cx="11" cy="11" r="6" stroke="currentColor" strokeWidth="1.2"/><path d="M21 21l-4.35-4.35" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round"/></svg>;
    case 'settings':
      return <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M12 15.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7z" stroke="currentColor" strokeWidth="1.2"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09a1.65 1.65 0 0 0-1-1.51 1.65 1.65 0 0 0-1.82.33l-.06.06A2 2 0 0 1 2.27 17.9l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09c.68 0 1.28-.39 1.51-1a1.65 1.65 0 0 0-.33-1.82L4.2 3.4A2 2 0 0 1 7 1.57l.06.06c.5.34 1.1.35 1.6.02.5-.33 1.09-.33 1.6-.02L11 2.2c.53.3 1.17.3 1.7 0l.74-.4c.5-.31 1.09-.31 1.6.02l.06.06A2 2 0 0 1 20 4.2l-.4.74c-.34.5-.35 1.1-.02 1.6.33.5.33 1.09.02 1.6l.4.74c.3.53.3 1.17 0 1.7l-.4.74c-.31.5-.31 1.09.02 1.6z" stroke="currentColor" strokeWidth="0.6"/></svg>;
    case 'help':
      return <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M12 17h.01" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round"/><path d="M9.09 9a3 3 0 1 1 5.82 1c0 1.5-2.5 2.5-2.5 2.5" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round"/></svg>;
    case 'about':
      return <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="1.2"/><path d="M12 8v4" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round"/><path d="M12 16h.01" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round"/></svg>;
    default:
      return null;
  }
}

export default function Sidebar({ current, onChange }) {
  const [compact, setCompact] = useState(() => {
    try { return localStorage.getItem('sidebar-compact') === 'true'; } catch { return false; }
  });

  useEffect(() => { try { localStorage.setItem('sidebar-compact', compact); } catch {} }, [compact]);

  const Item = ({ id, icon, label }) => (
    <button className={`side-link ${current === id ? 'active' : ''}`} onClick={() => onChange(id)} title={label}>
      <span className="side-icon"><Icon name={icon} /></span>
      {!compact && <span className="side-label">{label}</span>}
    </button>
  );

  return (
    <aside className={`sidebar glass-card ${compact ? 'compact' : ''}`} aria-label="Main navigation">
      <div className="brand">
        <h2>VerdaTerraAI</h2>
        {!compact && <p className="brand-sub">Civic Operations Copilot</p>}
      </div>

      <nav className="sidebar-nav">
        <Item id="dashboard" icon="dashboard" label="Dashboard" />
        <Item id="report" icon="report" label="Report" />
        <Item id="inspector" icon="inspector" label="Inspector" />
        <hr />
        <Item id="settings" icon="settings" label="Settings" />
        <Item id="help" icon="help" label="Help & FAQ" />
        <Item id="about" icon="about" label="About" />
      </nav>

      <div className="sidebar-footer">
        <button className="side-compact" onClick={() => setCompact(c => !c)} aria-pressed={compact}>{compact ? '→' : '←'}</button>
        {!compact && <small>v0.1 • Local Dev</small>}
      </div>
    </aside>
  );
}

