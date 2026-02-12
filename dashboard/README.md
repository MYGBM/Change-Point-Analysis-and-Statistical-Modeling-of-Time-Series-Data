# Task 3: Interactive Dashboard — Brent Oil Change Point Analysis

An interactive web dashboard built with **Flask** (backend) and **React** (frontend) to explore the Bayesian change point analysis results for Brent oil prices.

## Features

| Feature | Description |
|---------|-------------|
| **Overview Tab** | Full price history with change point overlay |
| **Change Point Tab** | Regime comparison, posterior stats, model diagnostics |
| **Event Impact Tab** | 15 historical events with category filters, highlight-on-chart, and drill-down modal |
| **Volatility Tab** | Rolling volatility (7/30/90-day windows) with regime context |
| **Date Range Filter** | Filter all charts to a custom date range |
| **Event Highlighting** | Pin events onto the price chart to visualize correlation |
| **Drill-Down Modal** | Click any event to see ±60 day price impact, pre/post comparison, volatility |
| **Responsive Design** | Desktop, tablet, and mobile layouts |

## Architecture

```
dashboard/
├── backend/
│   ├── app.py              # Flask API server (8 endpoints)
│   └── data_loader.py      # Data processing & result serving
└── frontend/
    ├── public/index.html
    ├── package.json
    └── src/
        ├── App.js           # Main app with tab navigation
        ├── App.css          # All styles (dark theme)
        ├── index.js
        ├── index.css        # CSS variables
        └── components/
            ├── Header.js           # Title bar
            ├── StatsCards.js       # Summary metric cards
            ├── PriceChart.js       # Main price chart (Recharts)
            ├── VolatilityChart.js   # Rolling volatility chart
            ├── RegimePanel.js      # Regime comparison + model info
            ├── EventsTimeline.js   # Event list with filters
            └── EventImpactModal.js # Event drill-down modal
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/prices?start=&end=&resample=` | Historical prices (filterable) |
| GET | `/api/changepoint` | Change point results + model diagnostics |
| GET | `/api/regimes` | Regime statistics (pre/post change point) |
| GET | `/api/events?category=` | Events with price impact metrics |
| GET | `/api/events/<id>/impact?window=60` | Detailed event impact analysis |
| GET | `/api/volatility?window=30&start=&end=` | Rolling volatility data |
| GET | `/api/summary` | Overall analysis summary |
| GET | `/api/regime-prices` | Prices annotated with regime labels |

## Setup & Running

### Prerequisites
- Python 3.9+
- Node.js 18+ and npm

### 1. Install Python dependencies

From the **project root**:

```bash
pip install -r requirements.txt
```

### 2. Start the Flask backend

```bash
cd dashboard/backend
python app.py
```

The API server starts at **http://localhost:5000**.

### 3. Install and start the React frontend

In a **new terminal**:

```bash
cd dashboard/frontend
npm install
npm start
```

The dashboard opens at **http://localhost:3000**.

### Quick Start (both together)

**Terminal 1** (backend):
```bash
cd dashboard/backend && python app.py
```

**Terminal 2** (frontend):
```bash
cd dashboard/frontend && npm install && npm start
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Flask 3.0, Flask-CORS |
| Frontend | React 18, Recharts 2 |
| Data | Pandas, NumPy |
| Styling | CSS (custom dark theme, responsive) |

## Key Analysis Results Displayed

- **Single Change Point**: February 22, 2005 (90% CI: Feb 16 – Mar 2)
- **Regime 1** (1987–2005): Mean $21.41, Volatility $7.14
- **Regime 2** (2005–2022): Mean $75.60, Volatility $25.34
- **Price Impact**: +$54.19 (+253.1%)
- **15 Historical Events** across 4 categories with correlation analysis

---

*10 Academy — Mariam Gustavo*
