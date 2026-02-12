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
  ReferenceLine,
} from 'recharts';

const CP_DATE = '2005-02-22';

function VolTooltip({ active, payload }) {
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
      <div>Volatility: <span style={{ color: '#bc8cff', fontWeight: 600 }}>
        {(d.volatility * 100).toFixed(1)}%
      </span></div>
      <div style={{ color: '#8b949e' }}>Price: ${d.price}</div>
    </div>
  );
}

export default function VolatilityChart({ data, window: win }) {
  const chartData = useMemo(() => {
    if (data.length <= 1500) return data;
    const step = Math.ceil(data.length / 1500);
    return data.filter((_, i) => i % step === 0);
  }, [data]);

  return (
    <div className="chart-container">
      <div className="chart-title">
        Annualized Volatility ({win}-Day Rolling Window)
      </div>
      <ResponsiveContainer width="100%" height={350}>
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
            tickFormatter={(v) => `${(v * 100).toFixed(0)}%`}
            domain={['auto', 'auto']}
          />
          <Tooltip content={<VolTooltip />} />

          <Area
            type="monotone"
            dataKey="volatility"
            stroke="none"
            fill="#bc8cff"
            fillOpacity={0.12}
          />
          <Line
            type="monotone"
            dataKey="volatility"
            stroke="#bc8cff"
            strokeWidth={1.5}
            dot={false}
            activeDot={{ r: 4, fill: '#bc8cff' }}
          />

          <ReferenceLine
            x={CP_DATE}
            stroke="#f85149"
            strokeDasharray="6 3"
            strokeWidth={1.5}
            label={{
              value: 'Change Point',
              position: 'insideTopRight',
              fill: '#f85149',
              fontSize: 11,
            }}
          />
        </ComposedChart>
      </ResponsiveContainer>

      <div className="chart-legend">
        <div className="legend-item">
          <div className="legend-line" style={{ background: '#bc8cff' }} />
          Annualized Volatility
        </div>
        <div className="legend-item">
          <div className="legend-line" style={{ background: '#f85149' }} />
          Change Point
        </div>
      </div>
    </div>
  );
}
