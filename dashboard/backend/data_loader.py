"""
Data Loader for the Brent Oil Dashboard Backend.

Loads CSV data and hardcoded analysis results from Task 2
(single change point model) and serves them to Flask endpoints.
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta


class DataLoader:
    """Loads and processes all data needed by the dashboard."""
    
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self._load_data()
        self._compute_derived()
    
    # ─── Data Loading ──────────────────────────────────
    
    def _load_data(self):
        """Load CSV files."""
        # Price data
        prices_path = os.path.join(self.data_dir, 'BrentOilPrices_prepared.csv')
        self.df = pd.read_csv(prices_path)
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        self.df = self.df.sort_values('Date').reset_index(drop=True)
        
        # Events data
        events_path = os.path.join(self.data_dir, 'events.csv')
        self.events = pd.read_csv(events_path)
        self.events['start_date'] = pd.to_datetime(self.events['start_date'])
        self.events['end_date'] = pd.to_datetime(self.events['end_date'])
        
        print(f"✓ Loaded {len(self.df):,} price records")
        print(f"✓ Loaded {len(self.events)} events")
    
    def _compute_derived(self):
        """Compute log returns, volatility, and regime assignment."""
        # Log returns
        self.df['log_return'] = np.log(
            self.df['Price'] / self.df['Price'].shift(1)
        )
        self.df['log_return'] = self.df['log_return'].fillna(0)
        
        # Rolling volatility (multiple windows)
        for w in [7, 30, 90]:
            self.df[f'vol_{w}d'] = (
                self.df['log_return'].rolling(window=w).std() * np.sqrt(252)
            )
        
        # Regime assignment based on single change point
        self.cp_index = 4518  # Feb 22, 2005
        self.df['regime'] = np.where(
            self.df.index < self.cp_index, 1, 2
        )
        
        # Pct change for event impact
        self.df['pct_change'] = self.df['Price'].pct_change() * 100
        
        print("✓ Computed derived features")
    
    # ─── Change Point Results (from Task 2) ────────────
    
    # Hardcoded from the converged single change point model
    CHANGEPOINT = {
        'date_mode': '2005-02-22',
        'date_median': '2005-02-23',
        'date_5th': '2005-02-16',
        'date_95th': '2005-03-02',
        'tau_mode': 4518,
        'uncertainty_days': 14,
        'model': {
            'type': 'Bayesian Single Change Point',
            'likelihood': 'Normal',
            'priors': {
                'mu': 'Normal(50, 30)',
                'sigma': 'HalfNormal(10)',
                'tau': 'DiscreteUniform(0, N-1)',
            },
            'mcmc': {
                'draws': 2000,
                'tune': 1000,
                'chains': 4,
                'target_accept': 0.95,
            },
            'convergence': {
                'r_hat': 1.00,
                'ess_min': 400,
                'converged': True,
            },
        },
    }
    
    REGIMES = [
        {
            'regime': 1,
            'label': 'Low-Price Era',
            'start_date': '1987-05-21',
            'end_date': '2005-02-21',
            'n_days': 4518,
            'years': 12.4,
            'price_mean': 21.41,
            'price_std': 7.14,
            'mu_posterior': 21.42,
            'mu_posterior_std': 0.28,
            'sigma_posterior': 18.59,
            'return_mean': 0.000035,
            'return_std': 0.023704,
            'annualized_vol': 0.376,
        },
        {
            'regime': 2,
            'label': 'High-Price Era',
            'start_date': '2005-02-22',
            'end_date': '2022-11-14',
            'n_days': 4492,
            'years': 12.3,
            'price_mean': 75.60,
            'price_std': 25.34,
            'mu_posterior': 75.60,
            'mu_posterior_std': 0.28,
            'sigma_posterior': 18.59,
            'return_mean': 0.000089,
            'return_std': 0.027250,
            'annualized_vol': 0.433,
        },
    ]
    
    PRICE_IMPACT = {
        'absolute_change': 54.19,
        'percentage_change': 253.1,
        'volatility_before': 0.023704,
        'volatility_after': 0.027250,
    }
    
    # ─── API Data Methods ──────────────────────────────
    
    def get_prices(self, start=None, end=None, resample='D'):
        """Return price data, optionally filtered and resampled."""
        df = self.df.copy()
        
        if start:
            df = df[df['Date'] >= pd.to_datetime(start)]
        if end:
            df = df[df['Date'] <= pd.to_datetime(end)]
        
        if resample in ('W', 'M') and len(df) > 0:
            df = df.set_index('Date').resample(resample).agg({
                'Price': 'mean',
                'log_return': 'sum',
                'regime': 'first',
            }).dropna().reset_index()
        
        records = []
        for _, row in df.iterrows():
            records.append({
                'date': row['Date'].strftime('%Y-%m-%d'),
                'price': round(float(row['Price']), 2),
                'log_return': round(float(row['log_return']), 6),
                'regime': int(row['regime']),
            })
        
        return records
    
    def get_changepoint(self):
        """Return the single change point results."""
        return {
            **self.CHANGEPOINT,
            'price_impact': self.PRICE_IMPACT,
        }
    
    def get_regimes(self):
        """Return regime statistics."""
        return self.REGIMES
    
    def get_events(self, category=None):
        """Return events with price context."""
        events = self.events.copy()
        if category:
            events = events[events['category'] == category]
        
        result = []
        for idx, ev in events.iterrows():
            # Find price at event start
            start_mask = self.df['Date'] >= ev['start_date']
            end_mask = self.df['Date'] <= ev['end_date']
            
            if start_mask.any():
                start_idx = self.df[start_mask].index[0]
                price_at_start = float(self.df.loc[start_idx, 'Price'])
            else:
                price_at_start = None
            
            if end_mask.any():
                end_idx = self.df[end_mask].index[-1]
                price_at_end = float(self.df.loc[end_idx, 'Price'])
            else:
                price_at_end = None
            
            # Price change during event
            if price_at_start and price_at_end:
                price_change = round(price_at_end - price_at_start, 2)
                pct_change = round(
                    (price_change / price_at_start) * 100, 1
                )
            else:
                price_change = None
                pct_change = None
            
            # Determine which regime the event falls in
            regime = 1 if ev['start_date'] < pd.Timestamp('2005-02-22') else 2
            
            # Distance to change point
            cp_date = pd.Timestamp('2005-02-22')
            days_to_cp = (ev['start_date'] - cp_date).days
            
            result.append({
                'id': int(idx),
                'name': ev['event_name'],
                'start_date': ev['start_date'].strftime('%Y-%m-%d'),
                'end_date': ev['end_date'].strftime('%Y-%m-%d'),
                'category': ev['category'],
                'description': ev['description'],
                'price_at_start': round(price_at_start, 2) if price_at_start else None,
                'price_at_end': round(price_at_end, 2) if price_at_end else None,
                'price_change': price_change,
                'pct_change': pct_change,
                'regime': regime,
                'days_to_changepoint': days_to_cp,
            })
        
        return result
    
    def get_event_impact(self, event_id, window=60):
        """Return price series around a specific event."""
        if event_id < 0 or event_id >= len(self.events):
            return None
        
        ev = self.events.iloc[event_id]
        start = ev['start_date'] - timedelta(days=window)
        end = ev['end_date'] + timedelta(days=window)
        
        mask = (self.df['Date'] >= start) & (self.df['Date'] <= end)
        subset = self.df[mask]
        
        prices = []
        for _, row in subset.iterrows():
            in_event = (
                row['Date'] >= ev['start_date'] and 
                row['Date'] <= ev['end_date']
            )
            prices.append({
                'date': row['Date'].strftime('%Y-%m-%d'),
                'price': round(float(row['Price']), 2),
                'in_event': in_event,
                'log_return': round(float(row['log_return']), 6),
            })
        
        # Compute impact metrics
        pre_mask = (self.df['Date'] >= start) & (self.df['Date'] < ev['start_date'])
        post_mask = (self.df['Date'] > ev['end_date']) & (self.df['Date'] <= end)
        event_mask = (
            (self.df['Date'] >= ev['start_date']) & 
            (self.df['Date'] <= ev['end_date'])
        )
        
        pre_prices = self.df[pre_mask]['Price']
        post_prices = self.df[post_mask]['Price']
        event_prices = self.df[event_mask]['Price']
        
        return {
            'event': {
                'name': ev['event_name'],
                'start_date': ev['start_date'].strftime('%Y-%m-%d'),
                'end_date': ev['end_date'].strftime('%Y-%m-%d'),
                'category': ev['category'],
                'description': ev['description'],
            },
            'prices': prices,
            'metrics': {
                'pre_mean': round(float(pre_prices.mean()), 2) if len(pre_prices) > 0 else None,
                'post_mean': round(float(post_prices.mean()), 2) if len(post_prices) > 0 else None,
                'event_min': round(float(event_prices.min()), 2) if len(event_prices) > 0 else None,
                'event_max': round(float(event_prices.max()), 2) if len(event_prices) > 0 else None,
                'event_vol': round(float(
                    self.df[event_mask]['log_return'].std() * np.sqrt(252)
                ), 4) if len(event_prices) > 1 else None,
                'pre_vol': round(float(
                    self.df[pre_mask]['log_return'].std() * np.sqrt(252)
                ), 4) if len(pre_prices) > 1 else None,
            },
            'window_days': window,
        }
    
    def get_volatility(self, window=30, start=None, end=None):
        """Return rolling volatility data."""
        df = self.df.copy()
        
        if start:
            df = df[df['Date'] >= pd.to_datetime(start)]
        if end:
            df = df[df['Date'] <= pd.to_datetime(end)]
        
        col = f'vol_{window}d' if f'vol_{window}d' in df.columns else None
        
        if col is None:
            # Compute on the fly
            vol = df['log_return'].rolling(window=window).std() * np.sqrt(252)
        else:
            vol = df[col]
        
        # Downsample for performance (every 5th day for large ranges)
        step = max(1, len(df) // 2000)
        df_sampled = df.iloc[::step]
        vol_sampled = vol.iloc[::step]
        
        records = []
        for i, (_, row) in enumerate(df_sampled.iterrows()):
            v = vol_sampled.iloc[i]
            if pd.notna(v):
                records.append({
                    'date': row['Date'].strftime('%Y-%m-%d'),
                    'volatility': round(float(v), 4),
                    'price': round(float(row['Price']), 2),
                    'regime': int(row['regime']),
                })
        
        return records
    
    def get_summary(self):
        """Return overall analysis summary."""
        return {
            'dataset': {
                'total_observations': len(self.df),
                'start_date': self.df['Date'].min().strftime('%Y-%m-%d'),
                'end_date': self.df['Date'].max().strftime('%Y-%m-%d'),
                'years_covered': round(
                    (self.df['Date'].max() - self.df['Date'].min()).days / 365.25, 1
                ),
                'price_min': round(float(self.df['Price'].min()), 2),
                'price_max': round(float(self.df['Price'].max()), 2),
                'price_mean': round(float(self.df['Price'].mean()), 2),
            },
            'changepoint': self.CHANGEPOINT,
            'regimes': self.REGIMES,
            'price_impact': self.PRICE_IMPACT,
            'n_events': len(self.events),
            'event_categories': sorted(self.events['category'].unique().tolist()),
        }
    
    def get_regime_prices(self):
        """Return prices annotated with regime for charting."""
        step = max(1, len(self.df) // 3000)
        df_sampled = self.df.iloc[::step]
        
        records = []
        for _, row in df_sampled.iterrows():
            records.append({
                'date': row['Date'].strftime('%Y-%m-%d'),
                'price': round(float(row['Price']), 2),
                'regime': int(row['regime']),
            })
        return records
