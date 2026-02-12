"""
Bayesian Modeling Utilities for Change Point Detection

This module provides helper functions for building and analyzing 
Bayesian change point models using PyMC.
"""

import numpy as np
import pandas as pd
import pymc as pm
import arviz as az
import matplotlib.pyplot as plt


def prepare_log_returns(df, price_col='Price', date_col='Date'):
    """
    Convert prices to log returns for stationarity.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with price data
    price_col : str
        Name of price column
    date_col : str
        Name of date column
        
    Returns
    -------
    pd.DataFrame
        Dataframe with log_return column added
    """
    df = df.copy()
    df['log_price'] = np.log(df[price_col])
    df['log_return'] = df['log_price'].diff()
    
    # Remove first NaN value
    df = df.dropna(subset=['log_return']).reset_index(drop=True)
    
    print(f"✓ Calculated log returns")
    print(f"  Original data points: {len(df) + 1}")
    print(f"  Log returns: {len(df)}")
    print(f"  Mean log return: {df['log_return'].mean():.6f}")
    print(f"  Std log return: {df['log_return'].std():.6f}")
    
    return df


def build_single_changepoint_model(data, name="single_cp"):
    """
    Build a single change point model with PyMC.
    
    Uses raw prices with priors appropriate for oil price scale ($10-$150).
    Uses pm.Normal likelihood as specified by the task requirements.
    
    Parameters
    ----------
    data : array-like
        Time series data (raw prices)
    name : str
        Model name for identification
        
    Returns
    -------
    pm.Model
        PyMC model object
    """
    n = len(data)
    
    with pm.Model() as model:
        # Prior for change point location (discrete uniform)
        tau = pm.DiscreteUniform('tau', lower=0, upper=n-1)
        
        # Priors for regime means (price-scale: ~$10-$150)
        mu_1 = pm.Normal('mu_1', mu=50, sigma=30)
        mu_2 = pm.Normal('mu_2', mu=50, sigma=30)
        
        # Prior for noise level (shared across regimes)
        sigma = pm.HalfNormal('sigma', sigma=10)
        
        # Switch function for mean
        idx = np.arange(n)
        mu = pm.math.switch(tau >= idx, mu_1, mu_2)
        
        # Likelihood (Normal distribution)
        obs = pm.Normal('obs', mu=mu, sigma=sigma, observed=data)
    
    print(f"✓ Built single change point model: {name}")
    print(f"  Data points: {n}")
    print(f"  Parameters: tau, mu_1, mu_2, sigma")
    
    return model


def build_multiple_changepoint_model(data, n_changepoints=3, name="multiple_cp"):
    """
    Build a multiple change point model with PyMC.
    
    Uses raw prices with priors appropriate for oil price scale ($10-$150).
    Uses the sorted-uniform approach for ordered change points and
    pm.math.sum + pm.math.stack for efficient regime assignment.
    
    Parameters
    ----------
    data : array-like
        Time series data (raw prices)
    n_changepoints : int
        Number of change points
    name : str
        Model name for identification
        
    Returns
    -------
    pm.Model
        PyMC model object
    """
    import pytensor.tensor as pt
    
    n = len(data)
    n_regimes = n_changepoints + 1
    
    with pm.Model() as model:
        # Priors for change point locations (sorted to enforce ordering)
        tau_raw = pm.DiscreteUniform('tau_raw', lower=0, upper=n-1, shape=n_changepoints)
        tau = pm.Deterministic('tau', pt.sort(tau_raw))
        
        # Priors for regime means (price-scale: ~$10-$150)
        mu = pm.Normal('mu', mu=50, sigma=30, shape=n_regimes)
        
        # Prior for noise level (single shared sigma)
        sigma = pm.HalfNormal('sigma', sigma=10)
        
        # Assign each data point to a regime via counting passed change points
        idx = np.arange(n)
        regime = pm.math.sum(
            pm.math.stack([idx >= tau[i] for i in range(n_changepoints)]),
            axis=0
        )
        
        # Select mean for each data point based on regime
        mu_t = mu[regime]
        
        # Likelihood (Normal distribution)
        obs = pm.Normal('obs', mu=mu_t, sigma=sigma, observed=data)
    
    print(f"✓ Built multiple change point model: {name}")
    print(f"  Data points: {n}")
    print(f"  Change points: {n_changepoints}")
    print(f"  Regimes: {n_regimes}")
    print(f"  Parameters: tau (x{n_changepoints}), mu (x{n_regimes}), sigma")
    
    return model


def sample_model(model, draws=2000, tune=1500, target_accept=0.95, 
                 chains=4, random_seed=42):
    """
    Run MCMC sampling on a PyMC model.
    
    Parameters
    ----------
    model : pm.Model
        PyMC model to sample
    draws : int
        Number of samples to draw
    tune : int
        Number of tuning samples
    target_accept : float
        Target acceptance rate for NUTS sampler
    chains : int
        Number of MCMC chains
    random_seed : int
        Random seed for reproducibility
        
    Returns
    -------
    az.InferenceData
        Arviz InferenceData object with trace
    """
    print(f"\n{'='*70}")
    print("STARTING MCMC SAMPLING")
    print(f"{'='*70}")
    print(f"Draws: {draws}, Tune: {tune}, Chains: {chains}")
    print(f"Target accept: {target_accept}")
    print(f"Random seed: {random_seed}")
    print(f"{'='*70}\n")
    
    with model:
        trace = pm.sample(
            draws=draws,
            tune=tune,
            target_accept=target_accept,
            chains=chains,
            random_seed=random_seed,
            return_inferencedata=True
        )
    
    print(f"\n{'='*70}")
    print("✓ SAMPLING COMPLETE")
    print(f"{'='*70}\n")
    
    return trace


def check_convergence(trace, var_names=None):
    """
    Check MCMC convergence diagnostics.
    
    Parameters
    ----------
    trace : az.InferenceData
        Trace from MCMC sampling
    var_names : list, optional
        Variables to check (None = all)
        
    Returns
    -------
    pd.DataFrame
        Summary statistics with convergence diagnostics
    """
    print(f"\n{'='*70}")
    print("CONVERGENCE DIAGNOSTICS")
    print(f"{'='*70}\n")
    
    summary = az.summary(trace, var_names=var_names)
    
    # Check r_hat values
    r_hat_ok = (summary['r_hat'] < 1.01).all()
    
    print("R-hat check (should be < 1.01):")
    if r_hat_ok:
        print("  ✓ All variables converged (r_hat < 1.01)")
    else:
        bad_vars = summary[summary['r_hat'] >= 1.01].index.tolist()
        print(f"  ✗ Warning: {len(bad_vars)} variables did not converge")
        print(f"  Problem variables: {bad_vars}")
    
    # Check effective sample size
    ess_low = summary[summary['ess_bulk'] < 400]
    if len(ess_low) > 0:
        print(f"\n  ⚠ Warning: {len(ess_low)} variables have low ESS (< 400)")
    else:
        print("\n  ✓ All variables have adequate ESS")
    
    print(f"\n{'='*70}\n")
    
    return summary


def extract_changepoint_dates(trace, df, date_col='Date', var_name='tau'):
    """
    Extract change point dates from trace.
    
    Parameters
    ----------
    trace : az.InferenceData
        Trace from MCMC sampling
    df : pd.DataFrame
        Original dataframe with dates
    date_col : str
        Name of date column
    var_name : str
        Name of change point variable
        
    Returns
    -------
    dict
        Dictionary with change point statistics
    """
    # Get posterior samples
    tau_samples = trace.posterior[var_name].values.flatten()
    
    # Calculate statistics
    tau_mean = int(np.round(tau_samples.mean()))
    tau_median = int(np.round(np.median(tau_samples)))
    tau_mode = int(np.round(np.argmax(np.bincount(tau_samples.astype(int)))))
    
    # Get dates
    dates = df[date_col].values
    
    result = {
        'tau_mean': tau_mean,
        'tau_median': tau_median,
        'tau_mode': tau_mode,
        'date_mean': pd.Timestamp(dates[tau_mean]),
        'date_median': pd.Timestamp(dates[tau_median]),
        'date_mode': pd.Timestamp(dates[tau_mode]),
        'tau_5th': int(np.percentile(tau_samples, 5)),
        'tau_95th': int(np.percentile(tau_samples, 95)),
        'date_5th': pd.Timestamp(dates[int(np.percentile(tau_samples, 5))]),
        'date_95th': pd.Timestamp(dates[int(np.percentile(tau_samples, 95))])
    }
    
    print(f"Change Point Location:")
    print(f"  Mode (MAP): {result['tau_mode']} -> {result['date_mode'].date()}")
    print(f"  Median: {result['tau_median']} -> {result['date_median'].date()}")
    print(f"  90% CI: [{result['date_5th'].date()}, {result['date_95th'].date()}]")
    
    return result


def extract_multiple_changepoint_dates(trace, df, date_col='Date', n_changepoints=3):
    """
    Extract multiple change point dates from trace.
    
    Parameters
    ----------
    trace : az.InferenceData
        Trace from MCMC sampling
    df : pd.DataFrame
        Original dataframe with dates
    date_col : str
        Name of date column
    n_changepoints : int
        Number of change points
        
    Returns
    -------
    list of dict
        List of dictionaries with change point statistics
    """
    results = []
    dates = df[date_col].values
    
    # Get tau samples (already sorted)
    tau_samples = trace.posterior['tau'].values  # shape: (chains, draws, n_changepoints)
    
    print(f"\n{'='*70}")
    print(f"DETECTED CHANGE POINTS (n={n_changepoints})")
    print(f"{'='*70}\n")
    
    for i in range(n_changepoints):
        tau_i = tau_samples[:, :, i].flatten()
        
        tau_mean = int(np.round(tau_i.mean()))
        tau_median = int(np.round(np.median(tau_i)))
        tau_mode = int(np.round(np.argmax(np.bincount(tau_i.astype(int)))))
        
        result = {
            'cp_num': i + 1,
            'tau_mean': tau_mean,
            'tau_median': tau_median,
            'tau_mode': tau_mode,
            'date_mean': pd.Timestamp(dates[tau_mean]),
            'date_median': pd.Timestamp(dates[tau_median]),
            'date_mode': pd.Timestamp(dates[tau_mode]),
            'tau_5th': int(np.percentile(tau_i, 5)),
            'tau_95th': int(np.percentile(tau_i, 95)),
            'date_5th': pd.Timestamp(dates[int(np.percentile(tau_i, 5))]),
            'date_95th': pd.Timestamp(dates[int(np.percentile(tau_i, 95))])
        }
        
        print(f"Change Point {i+1}:")
        print(f"  Mode (MAP): {result['tau_mode']} -> {result['date_mode'].date()}")
        print(f"  Median: {result['tau_median']} -> {result['date_median'].date()}")
        print(f"  90% CI: [{result['date_5th'].date()}, {result['date_95th'].date()}]")
        print()
        
        results.append(result)
    
    print(f"{'='*70}\n")
    
    return results


def match_changepoints_to_events(changepoints, events_df, max_days=90):
    """
    Match detected change points to known events.
    
    Parameters
    ----------
    changepoints : list of dict
        Change point information from extract_multiple_changepoint_dates
    events_df : pd.DataFrame
        Events database
    max_days : int
        Maximum days between change point and event to consider a match
        
    Returns
    -------
    pd.DataFrame
        Dataframe with matched events
    """
    matches = []
    
    print(f"\n{'='*70}")
    print("MATCHING CHANGE POINTS TO EVENTS")
    print(f"{'='*70}\n")
    
    for cp in changepoints:
        cp_date = cp['date_mode']
        
        # Calculate distance to each event
        events_df['days_from_start'] = (events_df['start_date'] - cp_date).dt.days
        events_df['days_from_end'] = (events_df['end_date'] - cp_date).dt.days
        
        # Find closest event
        events_df['min_distance'] = events_df[['days_from_start', 'days_from_end']].abs().min(axis=1)
        closest_event = events_df.loc[events_df['min_distance'].idxmin()]
        
        if closest_event['min_distance'] <= max_days:
            matches.append({
                'cp_num': cp['cp_num'],
                'cp_date': cp_date.date(),
                'event_name': closest_event['event_name'],
                'event_start': closest_event['start_date'].date(),
                'event_end': closest_event['end_date'].date(),
                'days_offset': int(closest_event['min_distance']),
                'category': closest_event['category'],
                'description': closest_event['description']
            })
            
            print(f"Change Point {cp['cp_num']}: {cp_date.date()}")
            print(f"  → Matched to: {closest_event['event_name']}")
            print(f"  → Event period: {closest_event['start_date'].date()} to {closest_event['end_date'].date()}")
            print(f"  → Offset: {int(closest_event['min_distance'])} days")
            print(f"  → Category: {closest_event['category']}")
            print()
        else:
            matches.append({
                'cp_num': cp['cp_num'],
                'cp_date': cp_date.date(),
                'event_name': 'No clear match',
                'event_start': None,
                'event_end': None,
                'days_offset': None,
                'category': None,
                'description': 'Change point does not align with documented events'
            })
            
            print(f"Change Point {cp['cp_num']}: {cp_date.date()}")
            print(f"  → No event match within {max_days} days")
            print()
    
    print(f"{'='*70}\n")
    
    return pd.DataFrame(matches)


def calculate_regime_statistics(trace, df, changepoints, price_col='Price', return_col='log_return'):
    """
    Calculate statistics for each regime.
    
    Parameters
    ----------
    trace : az.InferenceData
        Trace from MCMC sampling
    df : pd.DataFrame
        Original dataframe
    changepoints : list of dict
        Change point information
    price_col : str
        Name of price column
    return_col : str
        Name of log return column (optional, used if column exists)
        
    Returns
    -------
    pd.DataFrame
        Regime statistics
    """
    n_regimes = len(changepoints) + 1
    regime_stats = []
    
    # Extract posterior means for each regime
    mu_samples = trace.posterior['mu'].values  # shape: (chains, draws, n_regimes)
    
    # Handle sigma - could be scalar or per-regime
    sigma_samples = trace.posterior['sigma'].values
    has_per_regime_sigma = sigma_samples.ndim == 3
    
    # Define regime boundaries
    boundaries = [0] + [cp['tau_mode'] for cp in changepoints] + [len(df)]
    
    print(f"\n{'='*70}")
    print(f"REGIME STATISTICS (n={n_regimes})")
    print(f"{'='*70}\n")
    
    for i in range(n_regimes):
        start_idx = boundaries[i]
        end_idx = boundaries[i + 1]
        
        regime_data = df.iloc[start_idx:end_idx]
        
        # Posterior statistics
        mu_mean = mu_samples[:, :, i].mean()
        mu_std = mu_samples[:, :, i].std()
        
        if has_per_regime_sigma:
            sigma_mean = sigma_samples[:, :, i].mean()
        else:
            sigma_mean = sigma_samples.mean()
        
        # Empirical statistics
        price_mean = regime_data[price_col].mean()
        price_std = regime_data[price_col].std()
        
        stats_dict = {
            'regime': i + 1,
            'start_date': regime_data.iloc[0]['Date'].date(),
            'end_date': regime_data.iloc[-1]['Date'].date(),
            'n_days': len(regime_data),
            'mu_posterior': mu_mean,
            'mu_posterior_std': mu_std,
            'sigma_posterior': sigma_mean,
            'price_mean': price_mean,
            'price_std': price_std,
        }
        
        # Add return stats if column exists
        if return_col in df.columns:
            stats_dict['return_mean'] = regime_data[return_col].mean()
            stats_dict['return_std'] = regime_data[return_col].std()
        
        regime_stats.append(stats_dict)
        
        print(f"Regime {i+1}: {regime_data.iloc[0]['Date'].date()} to {regime_data.iloc[-1]['Date'].date()}")
        print(f"  Duration: {len(regime_data)} days")
        print(f"  Price (empirical): ${price_mean:.2f} ± ${price_std:.2f}")
        print(f"  Price (posterior μ): ${mu_mean:.2f} ± ${mu_std:.2f}")
        print(f"  Noise (posterior σ): ${sigma_mean:.2f}")
        if return_col in df.columns:
            print(f"  Log return: {stats_dict['return_mean']:.6f} ± {stats_dict['return_std']:.6f}")
        print()
    
    print(f"{'='*70}\n")
    
    return pd.DataFrame(regime_stats)
