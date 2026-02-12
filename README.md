# Bayesian Change Point Analysis of Brent Oil Prices

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyMC](https://img.shields.io/badge/PyMC-5.27.1-orange.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![React](https://img.shields.io/badge/React-18.2.0-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

> **Detecting structural breaks and associating causes in 35 years of Brent Oil price data using Bayesian statistical methods and interactive visualization.**

A comprehensive data science project combining exploratory data analysis, Bayesian change point detection with MCMC inference, and full-stack web dashboard development for oil market analysis.

**Organization:** 10 Academy — Birhan Energies  
**Author:** Mariam Gustavo  
**Date:** February 2026

---

## 📊 Project Overview

This project applies **Bayesian change point detection** to identify structural breaks in Brent crude oil prices from 1987-2022. The analysis reveals a dominant regime shift on **February 22, 2005**, marking a **253% price increase** from $21.41/barrel (pre-2005) to $75.60/barrel (post-2005)—the transition from the "Cheap Oil Era" to the "Commodity Super-Cycle."

### Key Results

- ✅ **Single Change Point Detected**: February 22, 2005 (90% CI: ±7 days)
- ✅ **Regime 1 (1987-2005)**: Mean $21.41, Volatility 0.024, Duration 12.4 years
- ✅ **Regime 2 (2005-2022)**: Mean $75.60, Volatility 0.027, Duration 12.3 years
- ✅ **15 Historical Events Catalogued**: Wars, crises, policy decisions
- ✅ **Interactive Dashboard**: Flask backend + React frontend

---

## 🎯 Project Objectives

### Task 1: Exploratory Data Analysis
- Load and clean 9,010 daily Brent oil prices (May 1987 - November 2022)
- Create comprehensive historical event database (15 events)
- Analyze time series properties: trend, stationarity, volatility, distribution
- Visualize event correlations with price movements

### Task 2: Bayesian Change Point Detection
- Build single and multiple change point models using PyMC
- Perform MCMC inference with Hamiltonian Monte Carlo (NUTS)
- Validate convergence with R-hat and ESS diagnostics
- Quantify regime characteristics and price impacts
- Match detected change points to historical events

### Task 3: Interactive Dashboard
- Develop Flask REST API (8 endpoints)
- Build React frontend with 4 interactive tabs
- Enable date filtering, event highlighting, drill-down analysis
- Deploy responsive web application for stakeholder exploration

---

## 🏗️ Project Structure

```
.
├── data/
│   ├── BrentOilPrices.csv              # Raw price data (9,010 observations)
│   ├── BrentOilPrices_prepared.csv     # Processed data with log returns
│   ├── events.csv                      # 15 curated historical events
│   ├── demo_prices.csv                 # Demo datasets
│   └── demo_events.csv
│
├── notebooks/
│   ├── eda.ipynb                       # Task 1: Exploratory Data Analysis
│   ├── task2_bayesian_changepoint.ipynb # Task 2: Bayesian Modeling
│   ├── 01_demo_bayes_changepoint.ipynb  # Demo: Single change point
│   └── 02_demo_multiple_changepoints.ipynb # Demo: Multiple change points
│
├── src/
│   ├── __init__.py
│   ├── analysis.py                     # EDA utility functions (9 functions)
│   ├── plots.py                        # Plotting utilities (9 functions)
│   ├── bayesian_models.py              # PyMC model builders (8 functions)
│   └── demo_data.py                    # Demo data generators
│
├── outputs/                            # Generated plots (15 PNG files)
│   ├── task1_*.png                     # EDA visualizations
│   └── task2_*.png                     # Bayesian analysis plots
│
├── dashboard/
│   ├── backend/
│   │   ├── app.py                      # Flask API server (8 endpoints)
│   │   └── data_loader.py              # Data processing logic
│   └── frontend/
│       ├── public/
│       │   └── index.html
│       ├── src/
│       │   ├── App.js                  # Main React app
│       │   ├── App.css                 # Styling (dark theme)
│       │   └── components/             # UI components (7 components)
│       └── package.json
│
├── PLAN.md                             # Task 1 detailed workflow
├── REPORT.md                           # Final project report (10 pages)
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
└── quick_start.py                      # Quick demo script
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Node.js 14+** (for dashboard)
- **Git**

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/MYGBM/Change-Point-Analysis-and-Statistical-Modeling-of-Time-Series-Data.git
cd Change-Point-Analysis-and-Statistical-Modeling-of-Time-Series-Data
```

#### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Key Packages:**
- `pymc==5.27.1` — Bayesian modeling
- `arviz==0.23.4` — MCMC diagnostics
- `pandas==2.0.0` — Data manipulation
- `matplotlib==3.7.0` — Visualization
- `flask==3.0.0` — Backend API
- `flask-cors==4.0.0` — CORS handling

#### 3. Run Notebooks

```bash
jupyter notebook
```

Open and run:
1. `notebooks/eda.ipynb` — Task 1
2. `notebooks/task2_bayesian_changepoint.ipynb` — Task 2

#### 4. Launch Dashboard (Optional)

**Backend:**
```bash
cd dashboard/backend
python app.py
# Server starts on http://localhost:5000
```

**Frontend:**
```bash
cd dashboard/frontend
npm install
npm start
# React app opens at http://localhost:3000
```

---

## 📈 Usage Examples

### Example 1: Load Data and Perform EDA

```python
from src import analysis, plots
import pandas as pd

# Load data
df = analysis.load_and_prepare_data(
    file_path='data/BrentOilPrices.csv',
    date_column='Date',
    price_column='Price'
)

# Test stationarity
adf_result = analysis.perform_stationarity_test(df['Price'])
print(f"ADF p-value: {adf_result['p_value']:.4f}")

# Plot price series
plots.plot_raw_price_series(df, price_col='Price', date_col='Date')
```

### Example 2: Build and Sample Bayesian Model

```python
from src import bayesian_models
import numpy as np

# Load data
prices = df['Price'].values

# Build model
model = bayesian_models.build_single_changepoint_model(prices)

# Sample with MCMC
trace = bayesian_models.sample_model(
    model,
    draws=2000,
    tune=1000,
    chains=4
)

# Check convergence
summary = bayesian_models.check_convergence(trace)
print(summary)

# Extract change point
cp = bayesian_models.extract_changepoint_dates(
    trace, df, date_col='Date', var_name='tau'
)
print(f"Detected change point: {cp['date_mode'].date()}")
```

### Example 3: API Request to Dashboard Backend

```bash
# Get historical data
curl http://localhost:5000/api/historical-data

# Get change point results
curl http://localhost:5000/api/change-point

# Get event impact for Gulf War (event ID 0)
curl http://localhost:5000/api/event-impact/0
```

---

## 🔬 Methodology

### Bayesian Change Point Model

**Single Change Point:**
```
τ ~ DiscreteUniform(0, n-1)          # Change point location
μ₁ ~ Normal(50, 30)                  # Pre-change mean
μ₂ ~ Normal(50, 30)                  # Post-change mean
σ ~ HalfNormal(10)                   # Noise level
yₜ ~ Normal(μ(τ), σ)                 # Likelihood
```

**Inference:**
- **Algorithm**: Hamiltonian Monte Carlo (No-U-Turn Sampler)
- **Chains**: 4 parallel chains
- **Samples**: 2,000 draws per chain (after 1,000 tuning steps)
- **Convergence**: R-hat < 1.01, ESS > 400
- **Credible Intervals**: 90% highest density intervals

### Why This Approach?

1. **Bayesian Framework**: Quantifies uncertainty via posterior distributions
2. **No Assumptions on Break Count**: Model discovers change points from data
3. **MCMC Robustness**: Explores complex posterior landscapes
4. **Interpretable Results**: Credible intervals, regime statistics, event attribution

---

## 📊 Key Findings

### Detected Change Point: February 22, 2005

| Statistic | Value |
|-----------|-------|
| **Mode (MAP)** | February 22, 2005 |
| **Median** | February 23, 2005 |
| **90% Credible Interval** | [Feb 16, 2005 — Mar 2, 2005] |
| **Uncertainty** | ±7 days |
| **Model Convergence** | R-hat = 1.00 ✅ |

### Regime Characteristics

| Regime | Period | Duration | Mean Price | Std Dev | Volatility |
|--------|--------|----------|------------|---------|------------|
| **1** | May 1987 - Feb 2005 | 12.4 years | $21.41 | $7.14 | 0.0237 |
| **2** | Feb 2005 - Nov 2022 | 12.3 years | $75.60 | $25.34 | 0.0273 |
| **Change** | — | — | **+$54.19** | **+$18.20** | **+15.1%** |
| **% Change** | — | — | **+253%** | **+255%** | — |

### Event Correlation

| Event | Date | Category | Proximity to Change Point |
|-------|------|----------|---------------------------|
| Iraq War | 2003-03-20 | Geopolitical | -2 years (buildup phase) |
| **Change Point** | **2005-02-22** | — | — |
| Hurricane Katrina | 2005-08-29 | Supply Shock | +6 months (reinforcement) |
| Global Financial Crisis | 2008-07-01 | Economic | +3.4 years (within regime) |
| COVID-19 Pandemic | 2020-03-11 | Economic | +15 years (within regime) |

**Interpretation:** The change point represents a **fundamental market transition** driven by cumulative factors (Asian demand, geopolitical risk, declining spare capacity) rather than a single event.

---

## 🎨 Dashboard Features

### Overview Tab
- Full price history chart (1987-2022)
- Change point overlay with credible interval
- Event markers (toggle on/off)
- Date range filter

### Change Point Tab
- Posterior distribution histogram
- Regime comparison table
- Model diagnostics (R-hat, ESS)
- Key findings summary

### Event Impact Tab
- 15 historical events with category filters
- Click-to-highlight on price chart
- Drill-down modal with ±60 day analysis
- Pre/post price comparison

### Volatility Tab
- Rolling volatility (7/30/90-day windows)
- Regime shading (pre/post 2005)
- High-volatility event annotations

**Tech Stack:** Flask + React + Recharts + Axios + CSS3

---

## 📚 Documentation

- **[PLAN.md](PLAN.md)**: Task 1 detailed workflow and methodology
- **[REPORT.md](REPORT.md)**: Complete 10-page project report with findings
- **[dashboard/README.md](dashboard/README.md)**: Dashboard setup guide
- **[Notebooks](notebooks/)**: Executable analysis with markdown explanations

---

## 🧪 Testing

### Run Quick Demo

```bash
python quick_start.py
```

This script demonstrates:
- Data loading
- Single change point detection
- Regime statistics calculation
- Event matching

### Validate Convergence

```python
from src import bayesian_models

# Check R-hat and ESS
summary = bayesian_models.check_convergence(trace)
assert all(summary['r_hat'] < 1.01), "Convergence failed!"
print("✓ All parameters converged successfully")
```

---

## 🛠️ Troubleshooting

### Issue: PyMC import error

**Solution:** Ensure you have PyTensor backend installed:
```bash
pip install pytensor
```

### Issue: Dashboard CORS error

**Solution:** Check Flask CORS configuration in `backend/app.py`:
```python
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
```

### Issue: Multiple change point model won't converge

**Solution:** This is expected. The model has weak signal for secondary change points. Use single change point model results (R-hat = 1.00).

### Issue: Frontend won't start

**Solution:** Delete `node_modules` and reinstall:
```bash
cd dashboard/frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

---

## 🤝 Contributing

This is a course project for 10 Academy. Contributions are welcome for:
- Additional event databases (natural gas, WTI crude)
- Alternative models (BSTS, Dirichlet process)
- Dashboard enhancements (export features, real-time data)

**Contact:** Mariam Gustavo (GitHub: [@MYGBM](https://github.com/MYGBM))

---

## 📜 License

MIT License — See [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **10 Academy** for project guidance and training
- **Birhan Energies** for domain context
- **PyMC Development Team** for excellent probabilistic programming framework
- **U.S. EIA** for public oil price data

---

## 📞 Contact

**Mariam Gustavo**  
10 Academy — Week 5 Capstone Project  
Email: [contact via GitHub]  
GitHub: [@MYGBM](https://github.com/MYGBM)  
Repository: [Change-Point-Analysis-and-Statistical-Modeling-of-Time-Series-Data](https://github.com/MYGBM/Change-Point-Analysis-and-Statistical-Modeling-of-Time-Series-Data)

---

## 📖 Citation

If you use this work, please cite:

```bibtex
@misc{gustavo2026brentcp,
  author = {Gustavo, Mariam},
  title = {Bayesian Change Point Analysis of Brent Oil Prices},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/MYGBM/Change-Point-Analysis-and-Statistical-Modeling-of-Time-Series-Data}
}
```

---

**Last Updated:** February 12, 2026  
**Status:** ✅ Complete (Tasks 1, 2, 3)  
**Version:** 1.0.0
