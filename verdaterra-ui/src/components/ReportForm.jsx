import React from 'react';

export default function ReportForm() {
  const [submitted, setSubmitted] = React.useState(false);

  const handleSubmit = (event) => {
    event.preventDefault();
    setSubmitted(true);
  };

  return (
    <section className="glass-card report-card" aria-labelledby="report-title">
      <h2 id="report-title">Report an Issue</h2>
      {!submitted ? (
        <form onSubmit={handleSubmit} className="report-form">
          <div className="field-group">
            <label htmlFor="issue-image">Upload Image</label>
            <input id="issue-image" name="issueImage" type="file" accept="image/*" />
          </div>
          <div className="field-group">
            <label htmlFor="ammonia-ppm">Gas Sensor (Ammonia ppm)</label>
            <input id="ammonia-ppm" name="ammoniaPpm" type="range" min="0" max="100" defaultValue="45" />
          </div>
          <div className="field-group">
            <label htmlFor="locale">Locale</label>
            <select id="locale" name="locale">
              <option value="en-IN">English (India)</option>
              <option value="hi-IN">Hindi</option>
            </select>
          </div>
          <button type="submit" className="btn">Generate Civic Campaign</button>
        </form>
      ) : (
        <section className="campaign-result" aria-live="polite" aria-labelledby="campaign-title">
          <h3 id="campaign-title">Campaign Generated</h3>
          <div className="grid campaign-grid">
            <article className="glass-card campaign-panel">
              <h4>Panel 1</h4>
              <p>Visual: Dirty Area</p>
              <p>"Today's neglect..."</p>
            </article>
            <article className="glass-card campaign-panel">
              <h4>Panel 2</h4>
              <p>Visual: Clean Business</p>
              <p>"Tomorrow's health."</p>
            </article>
          </div>
          <button type="button" className="btn" onClick={() => setSubmitted(false)}>Report Another</button>
        </section>
      )}
    </section>
  );
}
