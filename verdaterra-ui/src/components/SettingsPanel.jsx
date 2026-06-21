import React, { useEffect, useState } from 'react';

export default function SettingsPanel() {
  const [endpoint, setEndpoint] = useState('');
  const [apiKey, setApiKey] = useState('');

  useEffect(() => {
    try {
      setEndpoint(localStorage.getItem('api-endpoint') || 'http://localhost:8081');
      setApiKey(localStorage.getItem('api-key') || '');
    } catch {}
  }, []);

  const save = () => {
    try {
      localStorage.setItem('api-endpoint', endpoint);
      localStorage.setItem('api-key', apiKey);
      alert('Settings saved to localStorage (local dev)');
    } catch { alert('Unable to save settings'); }
  };

  return (
    <section className="settings-panel glass-card">
      <h2>Settings</h2>
      <div className="field-group">
        <label>API Endpoint</label>
        <input value={endpoint} onChange={e => setEndpoint(e.target.value)} />
      </div>
      <div className="field-group">
        <label>API Key</label>
        <input value={apiKey} onChange={e => setApiKey(e.target.value)} placeholder="set via .env for local dev" />
      </div>
      <div style={{marginTop: '1rem'}}>
        <button className="btn" onClick={save}>Save</button>
      </div>
    </section>
  );
}

