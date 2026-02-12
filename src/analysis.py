"""
Analysis utilities for Brent oil price time series analysis.
Contains functions for statistical tests, data transformations, and metric calculations.
"""

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller
from scipy import stats


def load_and_prepare_data(file_path, date_column='Date', price_column='Price'):
    """
    Load and prepare price data from CSV file.
    
    Parameters
    ----------
    file_path : str
        Path to CSV file containing price data
    date_column : str
        Name of date column
    price_column : str
        Name of price column
        
    Returns
    -------
    df : pd.DataFrame
        Prepared dataframe with parsed dates and sorted chronologically
    """
    df = pd.read_csv(file_path)
    df[date_column] = pd.to_datetime(df[date_column])
    df = df.sort_values(date_column).reset_index(drop=True)
    
    return df


def calculate_summary_statistics(df, price_column='Price'):
    """
    Calculate comprehensive summary statistics for price series.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe containing price data
    price_column : str
        Name of price column
        
    Returns
    -------
    dict
        Dictionary containing summary statistics
    """
    prices = df[price_column]
    
    stats_dict = {
        'count': len(prices),
        'mean': prices.mean(),
        'median': prices.median(),
        'std': prices.std(),
        'min': prices.min(),
        'max': prices.max(),
        'range': prices.max() - prices.min(),
        'cv': (prices.std() / prices.mean()) * 100,  # Coefficient of variation
        'skewness': prices.skew(),
        'kurtosis': prices.kurtosis()
    }
    
    return stats_dict


def perform_stationarity_test(series, verbose=True):
    """
    Perform Augmented Dickey-Fuller test for stationarity.
    
    Parameters
    ----------
    series : pd.Series or array-like
        Time series data to test
    verbose : bool
        If True, print detailed results
        
    Returns
    -------
    dict
        Dictionary containing test results
    """
    result = adfuller(series.dropna(), autolag='AIC')
    
    test_results = {
        'test_statistic': result[0],
        'p_value': result[1],
        'lags_used': result[2],
        'n_observations': result[3],
        'critical_values': result[4],
        'is_stationary': result[1] < 0.05
    }
    
    if verbose:
        print("="*70)
        print("STATIONARITY TEST: AUGMENTED DICKEY-FULLER")
        print("="*70)
        print(f"\nTest Statistic:     {result[0]:.6f}")
        print(f"P-value:            {result[1]:.6f}")
        print(f"Lags Used:          {result[2]}")
        print(f"Number of Obs:      {result[3]}")
        print(f"\nCritical Values:")
        for key, value in result[4].items():
            print(f"  {key:>5}: {value:.6f}")
        print("\n" + "-"*70)
        if result[1] < 0.05:
            print("✓ CONCLUSION: Series is STATIONARY (reject null hypothesis)")
        else:
            print("✗ CONCLUSION: Series is NON-STATIONARY (fail to reject null hypothesis)")
        print("-"*70 + "\n")
    
    return test_results


def calculate_rolling_statistics(df, price_column='Price', windows=[90, 365]):
    """
    Calculate rolling means and standard deviations for different windows.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe containing price data
    price_column : str
        Name of price column
    windows : list
        List of window sizes for rolling calculations
        
    Returns
    -------
    df : pd.DataFrame
        Dataframe with added rolling statistic columns
    """
    for window in windows:
        df[f'rolling_mean_{window}'] = df[price_column].rolling(window=window, center=True).mean()
        df[f'rolling_std_{window}'] = df[price_column].rolling(window=window, center=True).std()
    
    return df


def calculate_returns(df, price_column='Price'):
    """
    Calculate daily returns (percentage change).
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe containing price data
    price_column : str
        Name of price column
        
    Returns
    -------
    df : pd.DataFrame
        Dataframe with added daily_return column
    """
    df['daily_return'] = df[price_column].pct_change()
    return df


def analyze_distribution(series, sample_size=5000, random_state=42):
    """
    Perform comprehensive distribution analysis including normality test.
    
    Parameters
    ----------
    series : pd.Series
        Data series to analyze
    sample_size : int
        Sample size for Shapiro-Wilk test (max 5000)
    random_state : int
        Random seed for sampling
        
    Returns
    -------
    dict
        Dictionary containing distribution statistics
    """
    clean_series = series.dropna()
    
    # Sample for Shapiro-Wilk test if needed (test has limitations with large samples)
    if len(clean_series) > sample_size:
        test_data = clean_series.sample(sample_size, random_state=random_state)
    else:
        test_data = clean_series
    
    stat, p_value = stats.shapiro(test_data)
    
    dist_stats = {
        'mean': clean_series.mean(),
        'median': clean_series.median(),
        'mode': clean_series.mode().values[0] if len(clean_series.mode()) > 0 else None,
        'std': clean_series.std(),
        'skewness': clean_series.skew(),
        'kurtosis': clean_series.kurtosis(),
        'shapiro_stat': stat,
        'shapiro_pvalue': p_value,
        'is_normal': p_value >= 0.05
    }
    
    return dist_stats


def calculate_period_statistics(df, periods, date_column='Date', price_column='Price'):
    """
    Calculate statistics for different time periods.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe containing price data
    periods : list of tuples
        List of (name, start_date, end_date) tuples
    date_column : str
        Name of date column
    price_column : str
        Name of price column
        
    Returns
    -------
    list
        List of dictionaries containing period statistics
    """
    period_stats = []
    
    for period_name, start, end in periods:
        mask = (df[date_column] >= start) & (df[date_column] <= end)
        period_data = df[mask]
        
        if len(period_data) > 0:
            price_std = period_data[price_column].std()
            price_mean = period_data[price_column].mean()
            cv = (price_std / price_mean) * 100
            
            period_stats.append({
                'period': period_name,
                'mean': price_mean,
                'std': price_std,
                'cv': cv,
                'n_obs': len(period_data)
            })
    
    return period_stats


def check_extreme_returns(returns, n_std=3):
    """
    Check for extreme returns (outliers beyond n standard deviations).
    
    Parameters
    ----------
    returns : pd.Series
        Series of returns
    n_std : int
        Number of standard deviations to define extreme
        
    Returns
    -------
    dict
        Dictionary with extreme return statistics
    """
    clean_returns = returns.dropna()
    threshold = n_std * clean_returns.std()
    extreme_mask = np.abs(clean_returns) > threshold
    
    return {
        'n_extreme': extreme_mask.sum(),
        'pct_extreme': (extreme_mask.sum() / len(clean_returns)) * 100,
        'threshold': threshold,
        'expected_pct_normal': 0.3  # For normal distribution
    }


def print_summary_report(df, stationarity_result, dist_stats, events_df=None):
    """
    Print comprehensive summary report of analysis findings.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with price data
    stationarity_result : dict
        Stationarity test results
    dist_stats : dict
        Distribution analysis results
    events_df : pd.DataFrame, optional
        Events database
    """
    print("\n" + "="*80)
    print(" " * 20 + "EDA SUMMARY REPORT")
    print("="*80)
    
    print("\n📊 DATA QUALITY:")
    print(f"  ✓ Dataset contains {len(df):,} daily observations")
    print(f"  ✓ Date range: {df['Date'].min().date()} to {df['Date'].max().date()}")
    print(f"  ✓ Duration: {(df['Date'].max() - df['Date'].min()).days:,} days")
    print(f"  ✓ Missing values: {df.isnull().sum().sum()}")
    print(f"  ✓ Price range: ${df['Price'].min():.2f} - ${df['Price'].max():.2f}")
    
    print("\n📉 STATIONARITY:")
    print(f"  • ADF Test P-value: {stationarity_result['p_value']:.6f}")
    if stationarity_result['is_stationary']:
        print("  • Conclusion: STATIONARY")
    else:
        print("  • Conclusion: NON-STATIONARY")
        print("  • ⚡ ACTION REQUIRED: Transform to log returns")
    
    print("\n📊 DISTRIBUTION:")
    print(f"  • Mean: ${dist_stats['mean']:.2f}")
    print(f"  • Skewness: {dist_stats['skewness']:.3f}")
    print(f"  • Kurtosis: {dist_stats['kurtosis']:.3f}")
    print(f"  • Normality (Shapiro-Wilk p-value): {dist_stats['shapiro_pvalue']:.6f}")
    if dist_stats['is_normal']:
        print("  • Distribution: Approximately normal")
    else:
        print("  • Distribution: NOT normal")
        print("  • ⚡ RECOMMENDATION: Use Student's t distribution")
    
    if events_df is not None:
        print("\n🔗 EVENT CORRELATION:")
        print(f"  • Compiled database: {len(events_df)} major events")
        print("  • Event categories:")
        for cat, count in events_df['category'].value_counts().items():
            print(f"    - {cat.replace('_', ' ').title()}: {count}")
    
    print("\n" + "="*80 + "\n")
