import React, { useState } from 'react';
import ReportForm from './components/ReportForm';
import Dashboard from './components/Dashboard';
import InspectorView from './components/InspectorView';
import AgentPipeline from './components/AgentPipeline';
import Sidebar from './components/Sidebar';
import TopNav from './components/TopNav';
import SettingsPanel from './components/SettingsPanel';
import About from './components/About';
import Help from './components/Help';
import ThemeProvider from './ThemeProvider';
import './design-tokens.css';
import './index.css';
import ThemeProvider from './ThemeProvider';

function App() {
  const [currentView, setCurrentView] = useState('dashboard');

  const [sidebarOpen, setSidebarOpen] = React.useState(true);

  return (
    <ThemeProvider>
    <div className="app-shell">
      <a className="skip-link" href="#main-content">Skip to dashboard content</a>
      <TopNav onToggle={() => setSidebarOpen(s => !s)} />
      <div className="app-layout">
        {sidebarOpen && <Sidebar current={currentView} onChange={setCurrentView} />}

        <main id="main-content" className="main-panel" tabIndex="-1">
          <header className="page-header">
            <h1>{currentView === 'dashboard' ? 'Hygiene Dashboard' : currentView === 'report' ? 'Report Issue' : currentView === 'inspector' ? 'Inspector View' : currentView}</h1>
          </header>

          <div className="content-area">
            {currentView === 'dashboard' && (
              <>
                <AgentPipeline />
                <Dashboard />
              </>
            )}
            {currentView === 'report' && <ReportForm />}
            {currentView === 'inspector' && <InspectorView />}
            {currentView === 'settings' && <SettingsPanel />}
            {currentView === 'about' && <About />}
            {currentView === 'help' && <Help />}
          </div>
        </main>
      </div>
    </div>
    </ThemeProvider>
  );
}

export default App;
