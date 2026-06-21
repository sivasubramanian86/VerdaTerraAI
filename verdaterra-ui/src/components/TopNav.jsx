import React from 'react';
import { useTheme } from '../ThemeProvider';

export default function TopNav({ onToggle }) {
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="topnav glass-card">
      <div className="topnav-left">
        <button className="icon-btn" aria-label="toggle-sidebar" onClick={onToggle}>☰</button>
        <div className="top-title">
          <strong>VerdaTerraAI</strong>
          <span className="top-sub">Operations Dashboard</span>
        </div>
      </div>
      <div className="topnav-right">
        <input className="top-search" placeholder="Search locations, incidents..." />
        <button className="icon-btn" title="Notifications">🔔</button>
        <button className="icon-btn" title="Toggle theme" onClick={toggleTheme}>{theme === 'dark' ? '🌙' : '☀️'}</button>
        <div className="avatar">S</div>
      </div>
    </div>
  );
}
