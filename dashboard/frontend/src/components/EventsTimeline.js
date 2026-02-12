import React, { useState, useMemo } from 'react';

const CATEGORIES = ['all', 'geopolitical', 'economic', 'supply_shock', 'policy'];

const CATEGORY_LABELS = {
  all: 'All',
  geopolitical: 'Geopolitical',
  economic: 'Economic',
  supply_shock: 'Supply Shock',
  policy: 'Policy',
};

export default function EventsTimeline({
  events,
  highlightedEvents,
  onEventClick,
  onToggleHighlight,
}) {
  const [filter, setFilter] = useState('all');

  const filtered = useMemo(() => {
    if (filter === 'all') return events;
    return events.filter((e) => e.category === filter);
  }, [events, filter]);

  return (
    <div className="events-container">
      <div className="events-header">
        <div className="card-title">📅 Historical Events</div>
        <div className="events-filters">
          {CATEGORIES.map((cat) => (
            <button
              key={cat}
              className={`filter-btn ${filter === cat ? 'active' : ''}`}
              onClick={() => setFilter(cat)}
            >
              {CATEGORY_LABELS[cat]}
            </button>
          ))}
        </div>
      </div>

      <div className="event-list">
        {filtered.map((ev) => (
          <div
            key={ev.id}
            className={`event-item ${highlightedEvents.includes(ev.id) ? 'highlighted' : ''}`}
          >
            <div className={`event-dot ${ev.category}`} />

            <div className="event-info" onClick={() => onEventClick(ev)}>
              <div className="event-name">{ev.name}</div>
              <div className="event-date">
                {ev.start_date}
                {ev.start_date !== ev.end_date && ` → ${ev.end_date}`}
                &nbsp;·&nbsp;
                <span style={{
                  color: ev.regime === 1 ? 'var(--regime1)' : 'var(--regime2)',
                  fontWeight: 500,
                }}>
                  Regime {ev.regime}
                </span>
              </div>
            </div>

            <div className="event-impact" onClick={() => onEventClick(ev)}>
              {ev.pct_change !== null && (
                <>
                  <div className={`event-impact-value ${ev.pct_change >= 0 ? 'positive' : 'negative'}`}
                    style={{ color: ev.pct_change >= 0 ? 'var(--accent-green)' : 'var(--accent-red)' }}>
                    {ev.pct_change >= 0 ? '+' : ''}{ev.pct_change}%
                  </div>
                  <div className="event-impact-label">during event</div>
                </>
              )}
            </div>

            <div className="event-actions">
              <button
                className={`icon-btn ${highlightedEvents.includes(ev.id) ? 'active' : ''}`}
                onClick={(e) => { e.stopPropagation(); onToggleHighlight(ev.id); }}
                title={highlightedEvents.includes(ev.id) ? 'Hide on chart' : 'Show on chart'}
              >
                📍
              </button>
              <button
                className="icon-btn"
                onClick={(e) => { e.stopPropagation(); onEventClick(ev); }}
                title="View details"
              >
                🔍
              </button>
            </div>
          </div>
        ))}
      </div>

      <div style={{ marginTop: 12, display: 'flex', gap: 16, flexWrap: 'wrap' }}>
        {Object.entries(CATEGORY_LABELS).filter(([k]) => k !== 'all').map(([cat, label]) => (
          <div key={cat} className="legend-item">
            <div className={`event-dot ${cat}`} />
            {label}
          </div>
        ))}
      </div>
    </div>
  );
}
