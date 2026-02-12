import React from 'react';

export default function RegimePanel({ regimes, summary }) {
  if (!regimes || regimes.length < 2) return null;

  const r1 = regimes[0];
  const r2 = regimes[1];
  const impact = summary?.price_impact;

  return (
    <div>
      <div className="regime-grid">
        {/* Regime 1 */}
        <div className="regime-card regime-1">
          <div className="regime-header">
            <div>
              <div className="regime-name">{r1.label}</div>
              <div style={{ fontSize: 12, color: 'var(--text-muted)', marginTop: 2 }}>
                {r1.start_date} → {r1.end_date}
              </div>
            </div>
            <span className="regime-badge">Regime 1</span>
          </div>

          <div className="regime-stats">
            <div className="regime-stat">
              <div className="regime-stat-label">Mean Price</div>
              <div className="regime-stat-value">${r1.price_mean}</div>
            </div>
            <div className="regime-stat">
              <div className="regime-stat-label">Std Dev</div>
              <div className="regime-stat-value">${r1.price_std}</div>
            </div>
            <div className="regime-stat">
              <div className="regime-stat-label">Posterior μ</div>
              <div className="regime-stat-value">${r1.mu_posterior} <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>±{r1.mu_posterior_std}</span></div>
            </div>
            <div className="regime-stat">
              <div className="regime-stat-label">Posterior σ</div>
              <div className="regime-stat-value">${r1.sigma_posterior}</div>
            </div>
            <div className="regime-stat">
              <div className="regime-stat-label">Duration</div>
              <div className="regime-stat-value">{r1.years} yrs</div>
            </div>
            <div className="regime-stat">
              <div className="regime-stat-label">Ann. Volatility</div>
              <div className="regime-stat-value">{(r1.annualized_vol * 100).toFixed(1)}%</div>
            </div>
          </div>
        </div>

        {/* Regime 2 */}
        <div className="regime-card regime-2">
          <div className="regime-header">
            <div>
              <div className="regime-name">{r2.label}</div>
              <div style={{ fontSize: 12, color: 'var(--text-muted)', marginTop: 2 }}>
                {r2.start_date} → {r2.end_date}
              </div>
            </div>
            <span className="regime-badge">Regime 2</span>
          </div>

          <div className="regime-stats">
            <div className="regime-stat">
              <div className="regime-stat-label">Mean Price</div>
              <div className="regime-stat-value">${r2.price_mean}</div>
            </div>
            <div className="regime-stat">
              <div className="regime-stat-label">Std Dev</div>
              <div className="regime-stat-value">${r2.price_std}</div>
            </div>
            <div className="regime-stat">
              <div className="regime-stat-label">Posterior μ</div>
              <div className="regime-stat-value">${r2.mu_posterior} <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>±{r2.mu_posterior_std}</span></div>
            </div>
            <div className="regime-stat">
              <div className="regime-stat-label">Posterior σ</div>
              <div className="regime-stat-value">${r2.sigma_posterior}</div>
            </div>
            <div className="regime-stat">
              <div className="regime-stat-label">Duration</div>
              <div className="regime-stat-value">{r2.years} yrs</div>
            </div>
            <div className="regime-stat">
              <div className="regime-stat-label">Ann. Volatility</div>
              <div className="regime-stat-value">{(r2.annualized_vol * 100).toFixed(1)}%</div>
            </div>
          </div>
        </div>
      </div>

      {/* Price Impact Banner */}
      {impact && (
        <div className="impact-banner">
          <div className="impact-title">Price Impact at Change Point</div>
          <div className="impact-value">+${impact.absolute_change} / barrel</div>
          <div className="impact-sub">
            +{impact.percentage_change}% increase &nbsp;|&nbsp; 
            From ${r1.price_mean} → ${r2.price_mean} mean price
          </div>
        </div>
      )}

      {/* Model Info */}
      {summary?.changepoint?.model && (
        <div className="card" style={{ marginTop: 16 }}>
          <div className="card-title">🔬 Model Specification</div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: 10 }}>
            {[
              ['Type', summary.changepoint.model.type],
              ['Likelihood', summary.changepoint.model.likelihood],
              ['μ Prior', summary.changepoint.model.priors.mu],
              ['σ Prior', summary.changepoint.model.priors.sigma],
              ['τ Prior', summary.changepoint.model.priors.tau],
              ['Draws', summary.changepoint.model.mcmc.draws],
              ['Tune', summary.changepoint.model.mcmc.tune],
              ['Chains', summary.changepoint.model.mcmc.chains],
              ['R-hat', summary.changepoint.model.convergence.r_hat],
              ['Converged', summary.changepoint.model.convergence.converged ? '✅ Yes' : '❌ No'],
            ].map(([label, val], i) => (
              <div key={i} style={{ padding: '8px 12px', background: 'var(--bg-primary)', borderRadius: 6 }}>
                <div style={{ fontSize: 11, color: 'var(--text-muted)', textTransform: 'uppercase' }}>{label}</div>
                <div style={{ fontSize: 14, fontWeight: 600, marginTop: 2 }}>{val}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
