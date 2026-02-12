import React, { useMemo } from 'react';
import {
  ResponsiveContainer,
  ComposedChart,
  Area,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ReferenceLine,
  ReferenceArea,
  CartesianGrid,
} from 'recharts';

const CP_DATE = '2005-02-22';
const CP_DATE_5 = '2005-02-16';
const CP_DATE_95 = '2005-03-02';

const CATEGORY_COLORS = {
  geopolitical: '#f85149',
  economic: '#d29922',
  supply_shock: '#bc8cff',
  policy: '#3fb950',
};

function CustomTooltip({ active, payload }) {
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
      <div>Price: <span style={{ color: '#58a6ff', fontWeight: 600 }}>${d.price}</span></div>
      {d.log_return !== undefined && (
        <div style={{ color: '#8b949e' }}>Return: {(d.log_return * 100).toFixed(3)}%</div>
      )}
      <div style={{ color: '#8b949e' }}>Regime: {d.regime === 1 ? 'Low-Price Era' : 'High-Price Era'}</div>
    </div>
  );
}

export default function PriceChart({
  data,
  events = [],
  highlightedEvents = [],
  showChangePoint = false,
  showRegimeShading = false,
  title = 'Brent Oil Prices',
  compact = false,
}) {
  // Downsample for perf if needed
  const chartData = useMemo(() => {
    if (data.length <= 2000) return data;
    const step = Math.ceil(data.length / 2000);
    return data.filter((_, i) => i % step === 0);
  }, [data]);

  const height = compact ? 250 : 400;

  // Find highlighted event dates for reference lines
  const eventLines = useMemo(() => {
    return events
      .filter((e) => highlightedEvents.includes(e.id))
      .map((e) => ({
        date: e.start_date,
        name: e.name,
        color: CATEGORY_COLORS[e.category] || '#8b949e',
      }));
  }, [events, highlightedEvents]);

  return (
    <div className={`chart-container ${compact ? 'compact' : ''}`}>
      <div className="chart-title">{title}</div>
      <ResponsiveContainer width="100%" height={height}>
        <ComposedChart data={chartData} margin={{ top: 5, right: 20, bottom: 5, left: 10 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#21262d" />
          <XAxis
            dataKey="date"
            tick={{ fill: '#8b949e', fontSize: 11 }}
            tickLine={false}
            axisLine={{ stroke: '#30363d' }}
            minTickGap={80}
          />
          <YAxis
            tick={{ fill: '#8b949e', fontSize: 11 }}
            tickLine={false}
            axisLine={{ stroke: '#30363d' }}
            tickFormatter={(v) => `$${v}`}
            domain={['auto', 'auto']}
          />
          <Tooltip content={<CustomTooltip />} />

          {/* Regime shading */}
          {showRegimeShading && chartData.length > 0 && (
            <>
              <ReferenceArea
                x1={chartData[0]?.date}
                x2={CP_DATE}
                fill="#58a6ff"
                fillOpacity={0.04}
              />
              <ReferenceArea
                x1={CP_DATE}
                x2={chartData[chartData.length - 1]?.date}
                fill="#f0883e"
                fillOpacity={0.04}
              />
            </>
          )}

          {/* Price area + line */}
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
            strokeWidth={compact ? 1 : 1.5}
            dot={false}
            activeDot={{ r: 4, fill: '#58a6ff' }}
          />

          {/* Change point line + credible interval */}
          {showChangePoint && (
            <>
              <ReferenceArea
                x1={CP_DATE_5}
                x2={CP_DATE_95}
                fill="#f85149"
                fillOpacity={0.08}
                label=""
              />
              <ReferenceLine
                x={CP_DATE}
                stroke="#f85149"
                strokeDasharray="6 3"
                strokeWidth={2}
                label={compact ? undefined : {
                  value: 'Change Point: Feb 22, 2005',
                  position: 'insideTopRight',
                  fill: '#f85149',
                  fontSize: 12,
                  fontWeight: 600,
                }}
              />
            </>
          )}

          {/* Highlighted event lines */}
          {eventLines.map((ev, i) => (
            <ReferenceLine
              key={i}
              x={ev.date}
              stroke={ev.color}
              strokeDasharray="4 3"
              strokeWidth={1.5}
              label={{
                value: ev.name,
                position: i % 2 === 0 ? 'insideTopLeft' : 'insideBottomLeft',
                fill: ev.color,
                fontSize: 10,
                fontWeight: 500,
              }}
            />
          ))}
        </ComposedChart>
      </ResponsiveContainer>

      {!compact && (
        <div className="chart-legend">
          <div className="legend-item">
            <div className="legend-line" style={{ background: '#58a6ff' }} />
            Price
          </div>
          {showChangePoint && (
            <>
              <div className="legend-item">
                <div className="legend-line" style={{ background: '#f85149', borderStyle: 'dashed' }} />
                Change Point
              </div>
              <div className="legend-item">
                <div className="legend-dot" style={{ background: 'rgba(248,81,73,0.2)' }} />
                90% Credible Interval
              </div>
            </>
          )}
          {showRegimeShading && (
            <>
              <div className="legend-item">
                <div className="legend-dot" style={{ background: 'rgba(88,166,255,0.2)' }} />
                Regime 1 (Low-Price)
              </div>
              <div className="legend-item">
                <div className="legend-dot" style={{ background: 'rgba(240,136,62,0.2)' }} />
                Regime 2 (High-Price)
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
}
