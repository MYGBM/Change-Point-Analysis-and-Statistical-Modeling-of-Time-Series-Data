import React, { useMemo } from 'react';
import {
  ResponsiveContainer,
  ComposedChart,
  Area,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ReferenceArea,
} from 'recharts';

function ImpactTooltip({ active, payload }) {
  if (!active || !payload || !payload.length) return null;
  const d = payload[0].payload;
  return (
    <div style={{
      background: '#1c2129',
      border: '1px solid #30363d',
      borderRadius: 8,
      padding: '10px 14px',
      fontSize: 13,
    }}>
      <div style={{ fontWeight: 600, marginBottom: 4 }}>{d.date}</div>
      <div>
        Price: <span style={{
          color: d.in_event ? '#f85149' : '#58a6ff',
          fontWeight: 600,
        }}>${d.price}</span>
      </div>
      {d.in_event && (
        <div style={{ color: '#f85149', fontSize: 11, marginTop: 2 }}>⚠ During event</div>
      )}
    </div>
  );
}

export default function EventImpactModal({ event, impact, onClose }) {
  const prices = impact?.prices || [];
  const metrics = impact?.metrics || {};

  // Add color field for area
  const chartData = useMemo(() => {
    return prices.map((p) => ({
      ...p,
      eventPrice: p.in_event ? p.price : null,
      normalPrice: !p.in_event ? p.price : null,
    }));
  }, [prices]);

  // Find event date range for shading
  const eventStart = prices.find((p) => p.in_event)?.date;
  const eventEnd = [...prices].reverse().find((p) => p.in_event)?.date;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div>
            <div className="modal-title">{event.name}</div>
          </div>
          <button className="modal-close" onClick={onClose}>✕</button>
        </div>

        <div className="modal-meta">
          <div className="modal-meta-item">
            <span className="modal-meta-label">Period: </span>
            {event.start_date} → {event.end_date}
          </div>
          <div className="modal-meta-item">
            <span className="modal-meta-label">Category: </span>
            {event.category}
          </div>
          <div className="modal-meta-item">
            <span className="modal-meta-label">Regime: </span>
            {event.regime === 1 ? 'Low-Price Era' : 'High-Price Era'}
          </div>
          <div className="modal-meta-item">
            <span className="modal-meta-label">Distance to CP: </span>
            {Math.abs(event.days_to_changepoint)} days {event.days_to_changepoint < 0 ? 'before' : 'after'}
          </div>
        </div>

        <div className="modal-description">{event.description}</div>

        {/* Impact Metrics */}
        <div className="impact-metrics">
          <div className="impact-metric">
            <div className="impact-metric-label">Price at Start</div>
            <div className="impact-metric-value" style={{ color: 'var(--accent-blue)' }}>
              ${event.price_at_start}
            </div>
          </div>
          <div className="impact-metric">
            <div className="impact-metric-label">Price at End</div>
            <div className="impact-metric-value" style={{ color: 'var(--accent-blue)' }}>
              ${event.price_at_end}
            </div>
          </div>
          <div className="impact-metric">
            <div className="impact-metric-label">Change</div>
            <div className="impact-metric-value" style={{
              color: event.pct_change >= 0 ? 'var(--accent-green)' : 'var(--accent-red)',
            }}>
              {event.pct_change >= 0 ? '+' : ''}{event.pct_change}%
            </div>
          </div>
          {metrics.event_min != null && (
            <div className="impact-metric">
              <div className="impact-metric-label">Event Low</div>
              <div className="impact-metric-value">${metrics.event_min}</div>
            </div>
          )}
          {metrics.event_max != null && (
            <div className="impact-metric">
              <div className="impact-metric-label">Event High</div>
              <div className="impact-metric-value">${metrics.event_max}</div>
            </div>
          )}
          {metrics.event_vol != null && (
            <div className="impact-metric">
              <div className="impact-metric-label">Event Volatility</div>
              <div className="impact-metric-value" style={{ color: 'var(--accent-purple)' }}>
                {(metrics.event_vol * 100).toFixed(1)}%
              </div>
            </div>
          )}
        </div>

        {/* Price Chart Around Event */}
        <div style={{ marginTop: 8 }}>
          <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 8 }}>
            Price ±{impact.window_days} Days Around Event
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <ComposedChart data={chartData} margin={{ top: 5, right: 20, bottom: 5, left: 10 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#21262d" />
              <XAxis
                dataKey="date"
                tick={{ fill: '#8b949e', fontSize: 10 }}
                tickLine={false}
                axisLine={{ stroke: '#30363d' }}
                minTickGap={60}
              />
              <YAxis
                tick={{ fill: '#8b949e', fontSize: 11 }}
                tickLine={false}
                axisLine={{ stroke: '#30363d' }}
                tickFormatter={(v) => `$${v}`}
                domain={['auto', 'auto']}
              />
              <Tooltip content={<ImpactTooltip />} />

              {/* Shade event period */}
              {eventStart && eventEnd && (
                <ReferenceArea
                  x1={eventStart}
                  x2={eventEnd}
                  fill="#f85149"
                  fillOpacity={0.1}
                  label={{
                    value: 'Event Period',
                    position: 'insideTop',
                    fill: '#f85149',
                    fontSize: 11,
                  }}
                />
              )}

              <Area
                type="monotone"
                dataKey="price"
                stroke="none"
                fill="#58a6ff"
                fillOpacity={0.08}
              />
              <Line
                type="monotone"
                dataKey="price"
                stroke="#58a6ff"
                strokeWidth={2}
                dot={false}
                activeDot={{ r: 4, fill: '#58a6ff' }}
              />
            </ComposedChart>
          </ResponsiveContainer>
        </div>

        {/* Pre/Post Comparison */}
        {metrics.pre_mean != null && metrics.post_mean != null && (
          <div style={{
            display: 'grid',
            gridTemplateColumns: '1fr auto 1fr',
            gap: 12,
            marginTop: 16,
            alignItems: 'center',
          }}>
            <div style={{ textAlign: 'center', padding: 14, background: 'var(--bg-primary)', borderRadius: 8 }}>
              <div style={{ fontSize: 11, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
                Pre-Event Mean
              </div>
              <div style={{ fontSize: 22, fontWeight: 700, marginTop: 4 }}>${metrics.pre_mean}</div>
              {metrics.pre_vol != null && (
                <div style={{ fontSize: 12, color: 'var(--text-muted)', marginTop: 2 }}>
                  Vol: {(metrics.pre_vol * 100).toFixed(1)}%
                </div>
              )}
            </div>
            <div style={{ fontSize: 24, color: 'var(--text-muted)' }}>→</div>
            <div style={{ textAlign: 'center', padding: 14, background: 'var(--bg-primary)', borderRadius: 8 }}>
              <div style={{ fontSize: 11, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
                Post-Event Mean
              </div>
              <div style={{ fontSize: 22, fontWeight: 700, marginTop: 4 }}>${metrics.post_mean}</div>
              <div style={{
                fontSize: 12,
                marginTop: 2,
                color: metrics.post_mean >= metrics.pre_mean ? 'var(--accent-green)' : 'var(--accent-red)',
              }}>
                {metrics.post_mean >= metrics.pre_mean ? '▲' : '▼'} $
                {Math.abs(metrics.post_mean - metrics.pre_mean).toFixed(2)}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
