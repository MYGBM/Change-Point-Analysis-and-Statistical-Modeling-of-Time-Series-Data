"""
Flask Backend for Brent Oil Price Change Point Analysis Dashboard

Serves analysis results from Task 1 & 2 via REST API endpoints.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from data_loader import DataLoader
import os

app = Flask(__name__)
CORS(app)

# Initialize data loader (loads data once at startup)
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
loader = DataLoader(DATA_DIR)


# ─────────────────────────────────────────────
# API Endpoints
# ─────────────────────────────────────────────

@app.route('/api/prices', methods=['GET'])
def get_prices():
    """
    Historical price data with optional date range filtering.
    
    Query params:
        start (str): Start date YYYY-MM-DD (optional)
        end (str):   End date YYYY-MM-DD (optional)
        resample (str): 'D','W','M' for daily/weekly/monthly (optional, default 'D')
    
    Returns:
        JSON array of {date, price, log_return} objects
    """
    start = request.args.get('start')
    end = request.args.get('end')
    resample = request.args.get('resample', 'D')
    
    data = loader.get_prices(start=start, end=end, resample=resample)
    return jsonify(data)


@app.route('/api/changepoint', methods=['GET'])
def get_changepoint():
    """
    Single change point detection results.
    
    Returns:
        JSON object with change point date, credible interval,
        regime parameters, and model diagnostics.
    """
    return jsonify(loader.get_changepoint())


@app.route('/api/regimes', methods=['GET'])
def get_regimes():
    """
    Regime statistics for the single change point model.
    
    Returns:
        JSON array of regime objects with price stats,
        posterior parameters, and duration info.
    """
    return jsonify(loader.get_regimes())


@app.route('/api/events', methods=['GET'])
def get_events():
    """
    Historical events with price context around each event.
    
    Query params:
        category (str): Filter by category (optional)
    
    Returns:
        JSON array of event objects with price impact metrics.
    """
    category = request.args.get('category')
    return jsonify(loader.get_events(category=category))


@app.route('/api/events/<int:event_id>/impact', methods=['GET'])
def get_event_impact(event_id):
    """
    Detailed price impact analysis for a specific event.
    
    Path params:
        event_id (int): Event index (0-based)
    
    Query params:
        window (int): Days before/after event to include (default 60)
    
    Returns:
        JSON with price series around event + impact metrics.
    """
    window = int(request.args.get('window', 60))
    data = loader.get_event_impact(event_id, window=window)
    if data is None:
        return jsonify({'error': 'Event not found'}), 404
    return jsonify(data)


@app.route('/api/volatility', methods=['GET'])
def get_volatility():
    """
    Rolling volatility data.
    
    Query params:
        window (int): Rolling window size in days (default 30)
        start (str):  Start date YYYY-MM-DD (optional)
        end (str):    End date YYYY-MM-DD (optional)
    
    Returns:
        JSON array of {date, volatility, price} objects.
    """
    window = int(request.args.get('window', 30))
    start = request.args.get('start')
    end = request.args.get('end')
    
    data = loader.get_volatility(window=window, start=start, end=end)
    return jsonify(data)


@app.route('/api/summary', methods=['GET'])
def get_summary():
    """
    Overall analysis summary with key metrics.
    
    Returns:
        JSON object with dataset info, model results,
        and key statistics.
    """
    return jsonify(loader.get_summary())


@app.route('/api/regime-prices', methods=['GET'])
def get_regime_prices():
    """
    Price data annotated with regime assignment.
    
    Returns:
        JSON array of {date, price, regime} objects.
    """
    return jsonify(loader.get_regime_prices())


# ─────────────────────────────────────────────
# Run
# ─────────────────────────────────────────────

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("  Brent Oil Change Point Analysis - API Server")
    print("=" * 60)
    print("\nEndpoints:")
    print("  GET /api/prices          - Historical prices")
    print("  GET /api/changepoint     - Change point results")
    print("  GET /api/regimes         - Regime statistics")
    print("  GET /api/events          - Historical events")
    print("  GET /api/events/<id>/impact - Event price impact")
    print("  GET /api/volatility      - Rolling volatility")
    print("  GET /api/summary         - Analysis summary")
    print("  GET /api/regime-prices   - Prices with regime labels")
    print("=" * 60 + "\n")
    
    app.run(debug=True, port=5000)
