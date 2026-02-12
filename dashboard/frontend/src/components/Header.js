import React from 'react';

export default function Header() {
  return (
    <header style={{
      padding: '24px 0 16px',
      borderBottom: '1px solid var(--border)',
      marginBottom: '20px',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '6px' }}>
        <span style={{ fontSize: '28px' }}>📊</span>
        <h1 style={{ fontSize: '22px', fontWeight: 700, color: 'var(--text-primary)' }}>
          Brent Oil Price — Change Point Analysis
        </h1>
      </div>
      <p style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>
        Bayesian structural break detection &amp; event impact analysis &nbsp;|&nbsp; 
        10 Academy &nbsp;|&nbsp; Mariam Gustavo
      </p>
    </header>
  );
}
