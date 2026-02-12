import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import './App.css';
import Header from './components/Header';
import StatsCards from './components/StatsCards';
import PriceChart from './components/PriceChart';
import VolatilityChart from './components/VolatilityChart';
import RegimePanel from './components/RegimePanel';
import EventsTimeline from './components/EventsTimeline';
import EventImpactModal from './components/EventImpactModal';

const API = 'http://localhost:5000/api';

function App() {
  // Data state
  const [prices, setPrices] = useState([]);
  const [summary, setSummary] = useState(null);
  const [regimes, setRegimes] = useState([]);
  const [events, setEvents] = useState([]);
  const [volatility, setVolatility] = useState([]);
  const [loading, setLoading] = useState(true);

  // UI state
  const [dateRange, setDateRange] = useState({ start: '', end: '' });
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [eventImpact, setEventImpact] = useState(null);
  const [highlightedEvents, setHighlightedEvents] = useState([]);
  const [volWindow, setVolWindow] = useState(30);
  const [activeTab, setActiveTab] = useState('overview');

  // Initial data load
  useEffect(() => {
    const load = async () => {
      try {
        const [sumRes, regRes, evRes] = await Promise.all([
          axios.get(`${API}/summary`),
          axios.get(`${API}/regimes`),
          axios.get(`${API}/events`),
        ]);
        setSummary(sumRes.data);
        setRegimes(regRes.data);
        setEvents(evRes.data);
      } catch (e) {
        console.error('Failed to load initial data:', e);
      }
    };
    load();
  }, []);

  // Load prices when date range changes
  const loadPrices = useCallback(async () => {
    setLoading(true);
    try {
      const params = {};
      if (dateRange.start) params.start = dateRange.start;
      if (dateRange.end) params.end = dateRange.end;

      const [priceRes, volRes] = await Promise.all([
        axios.get(`${API}/prices`, { params }),
        axios.get(`${API}/volatility`, { params: { ...params, window: volWindow } }),
      ]);
      setPrices(priceRes.data);
      setVolatility(volRes.data);
    } catch (e) {
      console.error('Failed to load prices:', e);
    }
    setLoading(false);
  }, [dateRange, volWindow]);

  useEffect(() => {
    loadPrices();
  }, [loadPrices]);

  // Event impact drill-down
  const handleEventClick = async (event) => {
    setSelectedEvent(event);
    try {
      const res = await axios.get(`${API}/events/${event.id}/impact`, {
        params: { window: 60 },
      });
      setEventImpact(res.data);
    } catch (e) {
      console.error('Failed to load event impact:', e);
    }
  };

  const toggleEventHighlight = (eventId) => {
    setHighlightedEvents((prev) =>
      prev.includes(eventId)
        ? prev.filter((id) => id !== eventId)
        : [...prev, eventId]
    );
  };

  const handleDateRangeChange = (field, value) => {
    setDateRange((prev) => ({ ...prev, [field]: value }));
  };

  const resetDateRange = () => {
    setDateRange({ start: '', end: '' });
  };

  return (
    <div className="app">
      <Header />

      {/* Tab Navigation */}
      <nav className="tabs">
        <button
          className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button
          className={`tab ${activeTab === 'changepoint' ? 'active' : ''}`}
          onClick={() => setActiveTab('changepoint')}
        >
          Change Point Analysis
        </button>
        <button
          className={`tab ${activeTab === 'events' ? 'active' : ''}`}
          onClick={() => setActiveTab('events')}
        >
          Event Impact
        </button>
        <button
          className={`tab ${activeTab === 'volatility' ? 'active' : ''}`}
          onClick={() => setActiveTab('volatility')}
        >
          Volatility
        </button>
      </nav>

      {/* Summary Cards - always visible */}
      {summary && <StatsCards summary={summary} />}

      {/* Date Range Filter */}
      <div className="controls-bar">
        <div className="date-controls">
          <label>From:</label>
          <input
            type="date"
            value={dateRange.start}
            min="1987-05-20"
            max="2022-11-14"
            onChange={(e) => handleDateRangeChange('start', e.target.value)}
          />
          <label>To:</label>
          <input
            type="date"
            value={dateRange.end}
            min="1987-05-20"
            max="2022-11-14"
            onChange={(e) => handleDateRangeChange('end', e.target.value)}
          />
          <button className="btn btn-secondary" onClick={resetDateRange}>
            Reset
          </button>
        </div>

        {activeTab === 'volatility' && (
          <div className="vol-controls">
            <label>Rolling Window:</label>
            <select
              value={volWindow}
              onChange={(e) => setVolWindow(Number(e.target.value))}
            >
              <option value={7}>7 days</option>
              <option value={30}>30 days</option>
              <option value={90}>90 days</option>
            </select>
          </div>
        )}
      </div>

      {/* Main Content */}
      <main className="main-content">
        {loading && <div className="loading">Loading data...</div>}

        {/* OVERVIEW TAB */}
        {activeTab === 'overview' && !loading && (
          <div className="tab-content">
            <PriceChart
              data={prices}
              events={events}
              highlightedEvents={highlightedEvents}
              showChangePoint={true}
              title="Brent Oil Prices — Full History"
            />
          </div>
        )}

        {/* CHANGE POINT TAB */}
        {activeTab === 'changepoint' && !loading && (
          <div className="tab-content">
            <PriceChart
              data={prices}
              events={events}
              highlightedEvents={highlightedEvents}
              showChangePoint={true}
              showRegimeShading={true}
              title="Change Point Detection — Regime Analysis"
            />
            <RegimePanel regimes={regimes} summary={summary} />
          </div>
        )}

        {/* EVENTS TAB */}
        {activeTab === 'events' && !loading && (
          <div className="tab-content">
            <PriceChart
              data={prices}
              events={events}
              highlightedEvents={highlightedEvents}
              showChangePoint={true}
              title="Price Series with Event Markers"
            />
            <EventsTimeline
              events={events}
              highlightedEvents={highlightedEvents}
              onEventClick={handleEventClick}
              onToggleHighlight={toggleEventHighlight}
            />
          </div>
        )}

        {/* VOLATILITY TAB */}
        {activeTab === 'volatility' && !loading && (
          <div className="tab-content">
            <VolatilityChart data={volatility} window={volWindow} />
            <PriceChart
              data={prices}
              events={events}
              highlightedEvents={highlightedEvents}
              showChangePoint={true}
              title="Price Reference"
              compact={true}
            />
          </div>
        )}
      </main>

      {/* Event Impact Modal */}
      {selectedEvent && eventImpact && (
        <EventImpactModal
          event={selectedEvent}
          impact={eventImpact}
          onClose={() => {
            setSelectedEvent(null);
            setEventImpact(null);
          }}
        />
      )}
    </div>
  );
}

export default App;
