import React from 'react';

export default function StatsCards({ summary }) {
  if (!summary) return null;

  const { dataset, price_impact, changepoint } = summary;

  const cards = [
    {
      label: 'Time Span',
      value: `${dataset.years_covered} yrs`,
      sub: `${dataset.start_date} → ${dataset.end_date}`,
    },
    {
      label: 'Observations',
      value: dataset.total_observations.toLocaleString(),
      sub: 'Daily price records',
    },
    {
      label: 'Price Range',
      value: `$${dataset.price_min} – $${dataset.price_max}`,
      sub: `Mean: $${dataset.price_mean}`,
    },
    {
      label: 'Change Point',
      value: changepoint.date_mode,
      sub: `CI: ${changepoint.date_5th} to ${changepoint.date_95th}`,
    },
    {
      label: 'Price Shift',
      value: `+$${price_impact.absolute_change}`,
      sub: `+${price_impact.percentage_change}%`,
      positive: true,
    },
    {
      label: 'Events Tracked',
      value: summary.n_events,
      sub: summary.event_categories.join(', '),
    },
  ];

  return (
    <div className="stats-grid">
      {cards.map((c, i) => (
        <div className="stat-card" key={i}>
          <div className="stat-label">{c.label}</div>
          <div className={`stat-value ${c.positive ? 'positive' : ''}`}>
            {c.value}
          </div>
          <div className="stat-sub">{c.sub}</div>
        </div>
      ))}
    </div>
  );
}
