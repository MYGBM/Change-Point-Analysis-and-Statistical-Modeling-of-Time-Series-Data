import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import arviz as az
import os

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


def plot_price_with_changepoint(df, tau, tau_label="Change Point", 
                                  output_path=None, title="Price Time Series"):
    """
    Plot price time series with a vertical line at the change point.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with 'date' and 'price' columns
    tau : int
        Change point index
    tau_label : str
        Label for the change point line
    output_path : str, optional
        Path to save the figure
    title : str
        Plot title
    """
    fig, ax = plt.subplots(figsize=(14, 6))
    
    ax.plot(df['date'], df['price'], linewidth=1.5, alpha=0.8, label='Price')
    ax.axvline(df.loc[tau, 'date'], color='red', linestyle='--', 
               linewidth=2, label=f'{tau_label} (day {tau})')
    
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Price', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    plt.show()


def plot_price_with_events(df, events_df, tau_true=None, output_path=None):
    """
    Plot price time series with event overlays.
    
    Parameters
    ----------
    df : pd.DataFrame
        Price data
    events_df : pd.DataFrame
        Events data with start_date, end_date, event_name
    tau_true : int, optional
        True change point to overlay
    output_path : str, optional
        Path to save figure
    """
    fig, ax = plt.subplots(figsize=(14, 6))
    
    ax.plot(df['date'], df['price'], linewidth=1.5, alpha=0.8, 
            color='steelblue', label='Price')
    
    colors = ['orange', 'green', 'purple', 'brown']
    for idx, row in events_df.iterrows():
        ax.axvspan(row['start_date'], row['end_date'], 
                   alpha=0.2, color=colors[idx % len(colors)],
                   label=row['event_name'])
    
    if tau_true is not None:
        ax.axvline(df.loc[tau_true, 'date'], color='red', linestyle='--', 
                   linewidth=2, label=f'True Change Point (day {tau_true})')
    
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Price', fontsize=12)
    ax.set_title('Price Time Series with Events Overlay', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10, loc='upper left')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    plt.show()


def plot_posterior_tau(trace, tau_true=None, output_path=None):
    """
    Plot posterior distribution of the change point tau.
    
    Parameters
    ----------
    trace : arviz.InferenceData
        MCMC trace
    tau_true : int, optional
        True change point value
    output_path : str, optional
        Path to save figure
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    tau_samples = trace.posterior['tau'].values.flatten()
    
    ax.hist(tau_samples, bins=50, density=True, alpha=0.7, 
            color='steelblue', edgecolor='black', label='Posterior samples')
    
    tau_mean = tau_samples.mean()
    tau_median = np.median(tau_samples)
    
    ax.axvline(tau_mean, color='blue', linestyle='-', linewidth=2, 
               label=f'Posterior mean = {tau_mean:.1f}')
    ax.axvline(tau_median, color='darkblue', linestyle='--', linewidth=2, 
               label=f'Posterior median = {tau_median:.1f}')
    
    if tau_true is not None:
        ax.axvline(tau_true, color='red', linestyle='--', linewidth=2, 
                   label=f'True τ = {tau_true}')
    
    ax.set_xlabel('Change Point (day index)', fontsize=12)
    ax.set_ylabel('Posterior Density', fontsize=12)
    ax.set_title('Posterior Distribution of Change Point τ', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    plt.show()


def plot_posterior_means(trace, mu1_true=None, mu2_true=None, output_path=None):
    """
    Plot posterior distributions of mu1 and mu2 (before/after means).
    
    Parameters
    ----------
    trace : arviz.InferenceData
        MCMC trace
    mu1_true : float, optional
        True mu1 value
    mu2_true : float, optional
        True mu2 value
    output_path : str, optional
        Path to save figure
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    mu1_samples = trace.posterior['mu1'].values.flatten()
    mu2_samples = trace.posterior['mu2'].values.flatten()
    
    axes[0].hist(mu1_samples, bins=40, density=True, alpha=0.7, 
                 color='coral', edgecolor='black')
    axes[0].axvline(mu1_samples.mean(), color='darkred', linestyle='-', 
                    linewidth=2, label=f'Posterior mean = {mu1_samples.mean():.2f}')
    if mu1_true is not None:
        axes[0].axvline(mu1_true, color='red', linestyle='--', 
                        linewidth=2, label=f'True μ₁ = {mu1_true}')
    axes[0].set_xlabel('μ₁ (mean before change)', fontsize=12)
    axes[0].set_ylabel('Density', fontsize=12)
    axes[0].set_title('Posterior: μ₁ (Before)', fontsize=13, fontweight='bold')
    axes[0].legend(fontsize=10)
    axes[0].grid(True, alpha=0.3)
    
    axes[1].hist(mu2_samples, bins=40, density=True, alpha=0.7, 
                 color='skyblue', edgecolor='black')
    axes[1].axvline(mu2_samples.mean(), color='darkblue', linestyle='-', 
                    linewidth=2, label=f'Posterior mean = {mu2_samples.mean():.2f}')
    if mu2_true is not None:
        axes[1].axvline(mu2_true, color='red', linestyle='--', 
                        linewidth=2, label=f'True μ₂ = {mu2_true}')
    axes[1].set_xlabel('μ₂ (mean after change)', fontsize=12)
    axes[1].set_ylabel('Density', fontsize=12)
    axes[1].set_title('Posterior: μ₂ (After)', fontsize=13, fontweight='bold')
    axes[1].legend(fontsize=10)
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    plt.show()


def plot_trace_summary(trace, output_path=None):
    """
    Plot trace plots for all parameters.
    
    Parameters
    ----------
    trace : arviz.InferenceData
        MCMC trace
    output_path : str, optional
        Path to save figure
    """
    fig = az.plot_trace(trace, var_names=['tau', 'mu1', 'mu2', 'sigma'],
                        figsize=(14, 10))
    
    plt.suptitle('MCMC Trace Plots', fontsize=16, fontweight='bold', y=1.001)
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    plt.show()


def plot_price_with_multiple_changepoints(df, tau_list, tau_labels=None, 
                                          output_path=None, title="Price Time Series"):
    """
    Plot price time series with MULTIPLE vertical lines at change points.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with 'date' and 'price' columns
    tau_list : list of int
        List of change point indices
    tau_labels : list of str, optional
        Labels for each change point
    output_path : str, optional
        Path to save the figure
    title : str
        Plot title
    """
    fig, ax = plt.subplots(figsize=(14, 6))
    
    ax.plot(df['date'], df['price'], linewidth=1.5, alpha=0.8, label='Price', color='steelblue')
    
    colors = ['red', 'orange', 'purple', 'brown', 'green']
    
    for i, tau in enumerate(tau_list):
        if tau_labels:
            label = f'{tau_labels[i]} (day {tau})'
        else:
            label = f'Change Point {i+1} (day {tau})'
        
        ax.axvline(df.loc[tau, 'date'], color=colors[i % len(colors)], 
                   linestyle='--', linewidth=2, label=label)
    
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Price', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    plt.show()


def plot_price_with_events_multiple(df, events_df, tau_true_list=None, output_path=None):
    """
    Plot price time series with event overlays and MULTIPLE change points.
    
    Parameters
    ----------
    df : pd.DataFrame
        Price data
    events_df : pd.DataFrame
        Events data with start_date, end_date, event_name
    tau_true_list : list of int, optional
        List of true change points to overlay
    output_path : str, optional
        Path to save figure
    """
    fig, ax = plt.subplots(figsize=(14, 6))
    
    ax.plot(df['date'], df['price'], linewidth=1.5, alpha=0.8, 
            color='steelblue', label='Price')
    
    event_colors = ['orange', 'green', 'purple', 'brown', 'pink', 'cyan']
    for idx, row in events_df.iterrows():
        ax.axvspan(row['start_date'], row['end_date'], 
                   alpha=0.2, color=event_colors[idx % len(event_colors)],
                   label=row['event_name'])
    
    if tau_true_list is not None:
        cp_colors = ['red', 'darkred', 'crimson']
        for i, tau in enumerate(tau_true_list):
            ax.axvline(df.loc[tau, 'date'], color=cp_colors[i % len(cp_colors)], 
                       linestyle='--', linewidth=2, 
                       label=f'True Change Point {i+1} (day {tau})')
    
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Price', fontsize=12)
    ax.set_title('Price Time Series with Events & Multiple Change Points', 
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=9, loc='upper left', ncol=2)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    plt.show()


def plot_posterior_tau_multiple(trace, n_changepoints, tau_true_list=None, output_path=None):
    """
    Plot posterior distributions of MULTIPLE change points.
    
    Parameters
    ----------
    trace : arviz.InferenceData
        MCMC trace
    n_changepoints : int
        Number of change points
    tau_true_list : list of int, optional
        List of true change point values
    output_path : str, optional
        Path to save figure
    """
    fig, axes = plt.subplots(1, n_changepoints, figsize=(7*n_changepoints, 5))
    
    if n_changepoints == 1:
        axes = [axes]
    
    colors = ['steelblue', 'coral', 'mediumseagreen']
    
    for i in range(n_changepoints):
        tau_samples = trace.posterior['tau'].values[:, :, i].flatten()
        
        axes[i].hist(tau_samples, bins=50, density=True, alpha=0.7, 
                    color=colors[i % len(colors)], edgecolor='black', 
                    label='Posterior samples')
        
        tau_mean = tau_samples.mean()
        tau_median = np.median(tau_samples)
        
        axes[i].axvline(tau_mean, color='blue', linestyle='-', linewidth=2, 
                       label=f'Mean = {tau_mean:.1f}')
        axes[i].axvline(tau_median, color='darkblue', linestyle='--', linewidth=2, 
                       label=f'Median = {tau_median:.1f}')
        
        if tau_true_list is not None and i < len(tau_true_list):
            axes[i].axvline(tau_true_list[i], color='red', linestyle='--', linewidth=2, 
                           label=f'True τ{i+1} = {tau_true_list[i]}')
        
        axes[i].set_xlabel(f'Change Point {i+1} (day index)', fontsize=12)
        axes[i].set_ylabel('Posterior Density', fontsize=12)
        axes[i].set_title(f'Posterior: τ{i+1}', fontsize=13, fontweight='bold')
        axes[i].legend(fontsize=10)
        axes[i].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    plt.show()


def plot_posterior_means_multiple(trace, n_regimes, mu_true_list=None, output_path=None):
    """
    Plot posterior distributions of MULTIPLE regime means.
    
    Parameters
    ----------
    trace : arviz.InferenceData
        MCMC trace
    n_regimes : int
        Number of regimes (n_changepoints + 1)
    mu_true_list : list of float, optional
        List of true mean values
    output_path : str, optional
        Path to save figure
    """
    fig, axes = plt.subplots(1, n_regimes, figsize=(5*n_regimes, 5))
    
    if n_regimes == 1:
        axes = [axes]
    
    colors = ['coral', 'skyblue', 'lightgreen', 'plum']
    
    for i in range(n_regimes):
        mu_samples = trace.posterior['mu'].values[:, :, i].flatten()
        
        axes[i].hist(mu_samples, bins=40, density=True, alpha=0.7, 
                    color=colors[i % len(colors)], edgecolor='black')
        axes[i].axvline(mu_samples.mean(), color='darkred', linestyle='-', 
                       linewidth=2, label=f'Mean = {mu_samples.mean():.2f}')
        
        if mu_true_list is not None and i < len(mu_true_list):
            axes[i].axvline(mu_true_list[i], color='red', linestyle='--', 
                           linewidth=2, label=f'True μ{i+1} = {mu_true_list[i]}')
        
        axes[i].set_xlabel(f'μ{i+1} (Regime {i+1} mean)', fontsize=12)
        axes[i].set_ylabel('Density', fontsize=12)
        axes[i].set_title(f'Posterior: μ{i+1}', fontsize=13, fontweight='bold')
        axes[i].legend(fontsize=10)
        axes[i].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    plt.show()


# ============================================================================
# EDA-Specific Plotting Functions
# ============================================================================

def plot_raw_price_series(df, date_col='Date', price_col='Price', events=None,
                          output_path=None, title='Brent Crude Oil Prices'):
    """
    Plot raw price time series with optional event overlays.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with price data
    date_col : str
        Name of date column
    price_col : str
        Name of price column
    events : list of tuples, optional
        List of (name, start_date, end_date, color) for event overlays
    output_path : str, optional
        Path to save figure
    title : str
        Plot title
    """
    fig, ax = plt.subplots(figsize=(16, 6))
    
    ax.plot(df[date_col], df[price_col], linewidth=1, alpha=0.8, color='steelblue')
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Brent Oil Price (USD/barrel)', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Add event overlays if provided
    if events is not None:
        for event in events:
            name, start, end, color = event
            ax.axvspan(pd.Timestamp(start), pd.Timestamp(end), 
                      alpha=0.1, color=color, label=name)
        ax.legend(fontsize=10, loc='upper left')
    
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    plt.show()


def plot_trend_analysis(df, date_col='Date', price_col='Price', 
                        rolling_cols=['rolling_mean_90', 'rolling_mean_365'],
                        output_path=None):
    """
    Plot price with rolling means to show trends.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with price and rolling mean columns
    date_col : str
        Name of date column
    price_col : str
        Name of price column
    rolling_cols : list
        List of rolling mean column names
    output_path : str, optional
        Path to save figure
    """
    fig, ax = plt.subplots(figsize=(16, 6))
    
    ax.plot(df[date_col], df[price_col], linewidth=0.8, alpha=0.4, 
            color='gray', label='Daily Price')
    
    colors = ['orange', 'darkred', 'purple']
    for idx, col in enumerate(rolling_cols):
        if col in df.columns:
            window = col.split('_')[-1]
            linewidth = 1.5 if idx == 0 else 2.5
            ax.plot(df[date_col], df[col], linewidth=linewidth, 
                   color=colors[idx % len(colors)], 
                   label=f'{window}-day Rolling Mean')
    
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Price (USD/barrel)', fontsize=12)
    ax.set_title('Brent Oil Prices with Trend Analysis', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    plt.show()


def plot_volatility_analysis(df, date_col='Date', price_col='Price',
                             volatility_col='rolling_std_365',
                             output_path=None):
    """
    Plot price and volatility in dual axis plot.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with price and volatility columns
    date_col : str
        Name of date column
    price_col : str
        Name of price column
    volatility_col : str
        Name of volatility column
    output_path : str, optional
        Path to save figure
    """
    fig, axes = plt.subplots(2, 1, figsize=(16, 10), sharex=True)
    
    # Top plot: Price
    axes[0].plot(df[date_col], df[price_col], linewidth=1, alpha=0.7, color='steelblue')
    axes[0].set_ylabel('Price (USD/barrel)', fontsize=12)
    axes[0].set_title('Brent Oil Prices', fontsize=13, fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    
    # Bottom plot: Volatility
    axes[1].plot(df[date_col], df[volatility_col], linewidth=2, color='darkred')
    axes[1].set_xlabel('Date', fontsize=12)
    axes[1].set_ylabel('Rolling Std Dev (365 days)', fontsize=12)
    axes[1].set_title('Price Volatility Over Time', fontsize=13, fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    axes[1].fill_between(df[date_col], 0, df[volatility_col], alpha=0.3, color='red')
    
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    plt.show()


def plot_distribution_analysis(df, price_col='Price', return_col='daily_return',
                               output_path=None):
    """
    Create 4-panel distribution analysis plot.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with price and return columns
    price_col : str
        Name of price column
    return_col : str
        Name of daily return column
    output_path : str, optional
        Path to save figure
    """
    from scipy import stats
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Histogram of prices
    axes[0, 0].hist(df[price_col], bins=60, edgecolor='black', alpha=0.7, color='steelblue')
    axes[0, 0].axvline(df[price_col].mean(), color='red', linestyle='--', 
                       linewidth=2, label=f'Mean = ${df[price_col].mean():.2f}')
    axes[0, 0].axvline(df[price_col].median(), color='orange', linestyle='--', 
                       linewidth=2, label=f'Median = ${df[price_col].median():.2f}')
    axes[0, 0].set_xlabel('Price (USD/barrel)', fontsize=11)
    axes[0, 0].set_ylabel('Frequency', fontsize=11)
    axes[0, 0].set_title('Distribution of Brent Oil Prices', fontsize=12, fontweight='bold')
    axes[0, 0].legend(fontsize=10)
    axes[0, 0].grid(True, alpha=0.3, axis='y')
    
    # 2. Q-Q plot
    stats.probplot(df[price_col], dist="norm", plot=axes[0, 1])
    axes[0, 1].set_title('Q-Q Plot (Normality Test)', fontsize=12, fontweight='bold')
    axes[0, 1].grid(True, alpha=0.3)
    
    # 3. Box plot by decade
    df_copy = df.copy()
    df_copy['Decade'] = (pd.to_datetime(df_copy['Date']).dt.year // 10) * 10 if 'Date' in df.columns else (df_copy.index.year // 10) * 10
    decade_labels = [f"{d}s" for d in sorted(df_copy['Decade'].unique())]
    axes[1, 0].boxplot([df_copy[df_copy['Decade'] == d][price_col].values 
                        for d in sorted(df_copy['Decade'].unique())],
                       labels=decade_labels)
    axes[1, 0].set_xlabel('Decade', fontsize=11)
    axes[1, 0].set_ylabel('Price (USD/barrel)', fontsize=11)
    axes[1, 0].set_title('Price Distribution by Decade', fontsize=12, fontweight='bold')
    axes[1, 0].grid(True, alpha=0.3, axis='y')
    
    # 4. Histogram of daily returns
    axes[1, 1].hist(df[return_col].dropna(), bins=100, edgecolor='black', alpha=0.7, color='coral')
    axes[1, 1].axvline(0, color='red', linestyle='--', linewidth=2)
    axes[1, 1].set_xlabel('Daily Return', fontsize=11)
    axes[1, 1].set_ylabel('Frequency', fontsize=11)
    axes[1, 1].set_title('Distribution of Daily Returns', fontsize=12, fontweight='bold')
    axes[1, 1].grid(True, alpha=0.3, axis='y')
    axes[1, 1].set_xlim(-0.15, 0.15)
    
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    plt.show()


def plot_events_overlay(df, events_df, date_col='Date', price_col='Price',
                        output_path=None):
    """
    Plot price series with detailed event overlays.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with price data
    events_df : pd.DataFrame
        Dataframe with events (event_name, start_date, end_date, category)
    date_col : str
        Name of date column in df
    price_col : str
        Name of price column in df
    output_path : str, optional
        Path to save figure
    """
    from matplotlib.patches import Patch
    
    fig, ax = plt.subplots(figsize=(18, 8))
    
    # Plot price series
    ax.plot(df[date_col], df[price_col], linewidth=1.5, alpha=0.8, 
            color='steelblue', label='Brent Price', zorder=1)
    
    # Define colors for event categories
    category_colors = {
        'geopolitical': 'red',
        'economic': 'orange',
        'supply_shock': 'purple',
        'policy': 'green'
    }
    
    # Overlay events
    for idx, row in events_df.iterrows():
        color = category_colors.get(row['category'], 'gray')
        
        ax.axvspan(row['start_date'], row['end_date'], 
                   alpha=0.15, color=color, zorder=0)
        
        # Add label for first 5 events
        if idx < 5:
            mid_date = row['start_date'] + (row['end_date'] - row['start_date']) / 2
            price_at_event = df[df[date_col] >= row['start_date']][price_col].iloc[0] if len(df[df[date_col] >= row['start_date']]) > 0 else df[price_col].max()
            
            ax.annotate(row['event_name'], 
                       xy=(mid_date, price_at_event),
                       xytext=(0, 20), textcoords='offset points',
                       fontsize=8, ha='center', rotation=45,
                       bbox=dict(boxstyle='round,pad=0.3', facecolor=color, alpha=0.3),
                       arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', 
                                     color=color, alpha=0.5))
    
    # Create legend
    legend_elements = [Patch(facecolor=color, alpha=0.3, 
                            label=cat.replace('_', ' ').title()) 
                      for cat, color in category_colors.items()]
    legend_elements.insert(0, plt.Line2D([0], [0], color='steelblue', 
                                         linewidth=2, label='Brent Price'))
    
    ax.set_xlabel('Date', fontsize=13)
    ax.set_ylabel('Price (USD/barrel)', fontsize=13)
    ax.set_title('Brent Oil Prices with Major Events Overlay', 
                 fontsize=15, fontweight='bold')
    ax.legend(handles=legend_elements, fontsize=11, loc='upper left')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    plt.show()
