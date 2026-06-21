import React, { useState } from 'react';
import ReportForm from './components/ReportForm';
import Dashboard from './components/Dashboard';
import InspectorView from './components/InspectorView';
import './index.css';

function App() {
  const [currentView, setCurrentView] = useState('dashboard');

  return (
    <div className="app-container">
      <a className="skip-link" href="#main-content">Skip to dashboard content</a>
      <header className="site-header">
        <h1>VerdaTerraAI</h1>
        <p>Multi-Sensory Environmental Copilot</p>
      </header>

      <nav className="nav-bar" aria-label="Primary dashboard views">
        <button
          type="button"
          className={`nav-link ${currentView === 'dashboard' ? 'active' : ''}`}
          aria-pressed={currentView === 'dashboard'}
          onClick={() => setCurrentView('dashboard')}
        >
          Hygiene Dashboard
        </button>
        <button
          type="button"
          className={`nav-link ${currentView === 'report' ? 'active' : ''}`}
          aria-pressed={currentView === 'report'}
          onClick={() => setCurrentView('report')}
        >
          Report Issue
        </button>
        <button
          type="button"
          className={`nav-link ${currentView === 'inspector' ? 'active' : ''}`}
          aria-pressed={currentView === 'inspector'}
          onClick={() => setCurrentView('inspector')}
        >
          Inspector View
        </button>
      </nav>

      <main id="main-content" tabIndex="-1">
        {currentView === 'dashboard' && <Dashboard />}
        {currentView === 'report' && <ReportForm />}
        {currentView === 'inspector' && <InspectorView />}
      </main>
    </div>
  );
}

export default App;
