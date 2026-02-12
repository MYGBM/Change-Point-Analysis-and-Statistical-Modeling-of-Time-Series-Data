# Task 1: Laying the Foundation for Analysis

**Project:** Bayesian Change Point Analysis of Brent Oil Prices  
**Organization:** Birhan Energies  
**Date:** February 2026

---

## 1. Data Analysis Workflow

This section outlines the complete workflow from data ingestion to actionable insights for stakeholders.

### Phase 1: Foundation & Preparation (Task 1)

#### Step 1.1: Data Loading & Initial Exploration
- **Input:** BrentOilPrices.csv (May 1987 - September 2022)
- **Actions:**
  - Load CSV data using pandas
  - Parse Date column to datetime format
  - Check for missing values and data quality issues
  - Generate summary statistics (mean, std, min, max, quartiles)
  - Verify data integrity and temporal continuity
- **Output:** Clean dataset ready for analysis

#### Step 1.2: Event Database Creation
- **Input:** Historical research from multiple sources
- **Actions:**
  - Research major geopolitical events (wars, conflicts, sanctions)
  - Identify OPEC decisions (production cuts, quota changes)
  - Catalog economic shocks (financial crises, recessions)
  - Document supply disruptions (natural disasters, strikes)
  - Compile policy changes (regulations, trade agreements)
  - Structure data: event_name, start_date, end_date, category, description
- **Output:** events.csv with minimum 10-15 key events
- **Quality criteria:** 
  - Events span entire data range (1987-2022)
  - Dates are validated and accurate
  - Events have clear potential impact on oil markets

#### Step 1.3: Exploratory Time Series Analysis
- **Actions:**
  - Visualize raw price series over time
  - Calculate and plot rolling means (trend identification)
  - Perform stationarity testing (Augmented Dickey-Fuller test)
  - Analyze volatility patterns (rolling standard deviation)
  - Examine price distribution characteristics
  - Overlay events on price chart for visual correlation
  - Document observed patterns and anomalies
- **Output:** 
  - 5-6 visualization plots
  - Statistical test results
  - Written observations and insights

### Phase 2: Data Transformation & Model Preparation (Task 2)

#### Step 2.1: Data Transformation
- **Rationale:** Raw prices are non-stationary (confirmed in Task 1)
- **Transformation:** Convert to log returns
  - Formula: `log_return[t] = log(price[t]) - log(price[t-1])`
  - Interpretation: Approximate percentage change
- **Benefits:**
  - Achieves stationarity (constant mean/variance)
  - Percentage changes are comparable across time
  - More suitable for Normal/Student-t distributions
  - Handles multiplicative effects

#### Step 2.2: Build Bayesian Change Point Model (PyMC)
- **Model Components:**
  1. **Priors** (initial beliefs):
     - τ (tau): DiscreteUniform over all days - "change point could be anywhere"
     - μ_regime: Normal(0, 0.02) for each regime mean
     - σ: HalfNormal(0.05) - volatility must be positive
  2. **Switch Function:**
     - Assigns appropriate mean based on position relative to τ
     - Creates step function in mean parameter
  3. **Likelihood:**
     - Normal or StudentT distribution (StudentT preferred for financial data)
     - Connects model predictions to observed log returns

#### Step 2.3: MCMC Sampling & Convergence
- **Sampling parameters:**
  - draws: 2000-3000 samples per chain
  - tune: 1000-1500 burn-in samples
  - chains: 4 independent chains
  - target_accept: 0.90-0.95 for stability
- **Diagnostics:**
  - R-hat ≈ 1.00 (convergence check)
  - ESS > 400 (effective sample size)
  - Trace plots show good mixing
  - No divergences or warnings

### Phase 3: Interpretation & Communication (Task 2)

#### Step 3.1: Extract Posterior Distributions
- Analyze posteriors for τ, μ_regimes, σ
- Calculate posterior means, medians, credible intervals
- Identify most probable change point dates

#### Step 3.2: Event Attribution
- Match detected change points to events database
- Calculate temporal proximity (days difference)
- Formulate causal hypotheses
- Quantify impact magnitudes (regime mean shifts)

#### Step 3.3: Generate Insights & Visualizations
- Create publication-quality plots
- Write probabilistic statements
- Document uncertainty quantification
- Prepare stakeholder-specific summaries

---

## 2. Assumptions and Limitations

### Assumptions

1. **Data Quality:**
   - Brent oil prices are accurately recorded
   - No systematic biases in data collection
   - Missing values (if any) are missing at random

2. **Event Database:**
   - Events database is comprehensive for major market-moving events
   - Event dates are approximate (exact timing may vary)
   - Events listed are those with potential causal impact

3. **Model Assumptions:**
   - Price regimes are relatively stable within periods
   - Change points represent sharp transitions (not gradual)
   - Log returns are approximately normally distributed (or Student-t)
   - Volatility is constant within regimes

4. **Market Dynamics:**
   - Oil markets respond to external events
   - Regime shifts have identifiable statistical signatures
   - Past patterns provide insight into future behavior

### Limitations

1. **Correlation vs Causation (Critical Discussion):**
   
   **The Problem:**
   - Detecting a statistical change point coinciding with an event does NOT prove the event caused the price shift
   - Temporal correlation is necessary but not sufficient for causation
   - Multiple confounding factors affect oil prices simultaneously
   
   **Example:**
   - Model detects change point on March 15, 2020
   - COVID-19 pandemic declared on March 11, 2020
   - **Observation:** Strong temporal correlation (4-day gap)
   - **Cannot conclude:** "COVID-19 caused the price drop" without additional evidence
   
   **Why?**
   - Saudi-Russia price war also started in March 2020
   - Global demand was already declining
   - Financial markets were experiencing broad sell-off
   - Supply chain disruptions were beginning
   
   **What We CAN Say:**
   - "A statistically significant change point occurred around March 15, 2020"
   - "This coincides with the COVID-19 pandemic and Saudi-Russia price war"
   - "The posterior probability of a regime shift is 95%"
   - "The mean daily return changed from +0.02% to -0.35%"
   
   **What We CANNOT Say:**
   - "COVID-19 caused the price drop" (too simplistic)
   - "The event alone explains the change" (ignores other factors)
   - "The relationship is causal" (requires controlled experiments or instrumental variables)
   
   **Strengthening Causal Claims:**
   - Triangulate with other data sources (production levels, demand indicators)
   - Use counterfactual analysis ("what would have happened without the event?")
   - Apply causal inference methods (difference-in-differences, synthetic control)
   - Consider dose-response relationships (severity of event → magnitude of impact)

2. **Model Limitations:**
   - **Single vs Multiple Change Points:** 
     - Single change point models may miss complex multi-regime periods
     - Multiple change point models risk overfitting
   - **Sharp vs Gradual Transitions:**
     - Model assumes instantaneous regime changes
     - Reality may involve gradual transitions over weeks/months
   - **Prior Sensitivity:**
     - Results can be influenced by choice of priors
     - Weakly informative priors mitigate but don't eliminate this
   - **Regime Homogeneity:**
     - Assumes constant parameters within regimes
     - Reality may have slow drift or micro-regimes

3. **Data Limitations:**
   - Historical data analysis (backward-looking, not predictive)
   - Data ends in September 2022 (doesn't capture recent events)
   - Daily prices may mask intraday volatility
   - Brent is one benchmark (doesn't represent all crude types)

4. **Event Database Limitations:**
   - Subjective selection of "important" events
   - Event dates are approximations (start/end may be ambiguous)
   - Attribution of event categories is qualitative
   - Omission of unreported or classified events
   - No weighting of event severity or expected impact

5. **Computational Limitations:**
   - MCMC sampling is computationally intensive
   - Convergence not guaranteed for complex models
   - Requires careful tuning and diagnostics
   - Results may vary slightly across runs (stochastic)

---

## 3. Communication Channels and Formats

### Target Stakeholders

#### 1. **Investors & Portfolio Managers**
- **Information Needs:**
  - When did major regime shifts occur?
  - What is the magnitude of price changes?
  - How confident are we in these estimates?
  - Which events had the largest impact?
  - What are the implications for diversification?

- **Preferred Formats:**
  - Executive summary (1-page, visual)
  - Interactive dashboard with filters
  - Quarterly briefing presentations
  - Risk assessment reports

- **Key Metrics to Communicate:**
  - Dates of regime changes (with credible intervals)
  - Percentage change in mean price levels
  - Volatility shifts (standard deviation changes)
  - Probability of future regime changes

#### 2. **Policymakers & Regulators**
- **Information Needs:**
  - How do geopolitical events affect oil markets?
  - Are price movements consistent with supply/demand fundamentals?
  - What is the effectiveness of policy interventions?
  - How quickly do markets respond to events?

- **Preferred Formats:**
  - Technical reports with methodology details
  - Policy briefs (2-3 pages, non-technical summary)
  - Testimony to legislative committees
  - White papers with recommendations

- **Key Metrics to Communicate:**
  - Event-to-impact lag times
  - Magnitude and duration of policy effects
  - Comparison of different event types
  - Uncertainty quantification (credible intervals)

#### 3. **Energy Companies & Traders**
- **Information Needs:**
  - What are the current and historical price regimes?
  - How can we forecast near-term price movements?
  - Which events are most predictive of change points?
  - What is the volatility regime for hedging strategies?

- **Preferred Formats:**
  - Real-time data feeds and alerts
  - Weekly/monthly market reports
  - Trading strategy recommendations
  - Scenario analysis and stress testing

- **Key Metrics to Communicate:**
  - Current regime characteristics (mean, volatility)
  - Probability of imminent regime change
  - Historical analogues for current conditions
  - Hedging recommendations based on regime

### Communication Media

1. **Written Reports:**
   - Full technical report (20-30 pages) with appendices
   - Executive summary (1 page)
   - Policy brief (2-3 pages)

2. **Visualizations:**
   - Price time series with detected change points
   - Posterior distribution plots
   - Event overlay charts
   - Before/after comparison plots
   - Regime summary tables


3. **Interactive Dashboards:**
   - Web-based interface
   - Filters: date range, event type, confidence level
   - Drill-down capabilities
   - Exportable charts and data tables

## 4. Understanding Change Point Models

### What Is a Change Point?

A **change point** is a specific moment in time when the statistical properties of a time series undergo a structural break. In the context of oil prices, this means:

- The **mean** price level shifts (e.g., $50/barrel → $80/barrel)
- The **volatility** changes (e.g., stable → highly volatile)
- The **trend** direction reverses (e.g., upward → downward)
- The underlying **market regime** transitions (e.g., supply surplus → shortage)

### Purpose in Oil Price Analysis

1. **Detect Regime Shifts:**
   - Identify when markets transition between different states
   - Example: From 2010-2013 high-price regime to 2014-2016 low-price regime

2. **Associate with Causal Events:**
   - Test if geopolitical events, OPEC decisions, or economic shocks coincide with detected change points
   - Quantify the timing and magnitude of event impacts

3. **Improve Forecasting:**
   - Different regimes may require different forecasting models
   - Understanding regime duration informs probabilistic forecasts

4. **Risk Management:**
   - Regime shifts represent major risk events for investors
   - Early detection enables hedging and portfolio rebalancing

### Why Bayesian Approach?

Traditional change point methods (e.g., CUSUM, binary segmentation) provide point estimates. **Bayesian methods offer:**

1. **Full Posterior Distributions:**
   - Not just "change point is at day 5,234"
   - But "there's an 85% probability the change point is between days 5,220-5,250"

2. **Uncertainty Quantification:**
   - Credible intervals for all parameters
   - Probabilistic statements about regime characteristics

3. **Incorporation of Prior Knowledge:**
   - Can use expert knowledge about typical oil price ranges
   - Priors reflect realistic constraints (e.g., volatility > 0)

4. **Flexible Modeling:**
   - Easy to extend to multiple change points
   - Can add hierarchical structure or covariates
   - Natural framework for model comparison (Bayes factors)

5. **Event-Driven Inference:**
   - Can test hypotheses like "Did Event X cause a regime shift?"
   - Probability-based conclusions rather than binary tests

### How Change Point Models Work

**Conceptual Framework:**

1. **Divide time series into segments:**
   - Before change point: Days 0 to τ-1
   - After change point: Days τ to N

2. **Different parameters per segment:**
   - Segment 1: Mean = μ₁, Volatility = σ₁
   - Segment 2: Mean = μ₂, Volatility = σ₂

3. **Unknown change point location:**
   - τ is a parameter to be estimated
   - Model explores all possible values of τ
   - Selects value(s) that best explain the data

4. **Bayesian framework:**
   - Assign prior distributions to τ, μ₁, μ₂, σ
   - Combine with likelihood (how well parameters fit data)
   - Obtain posterior distributions (updated beliefs)

**Mathematical Intuition (Simple Case):**

For each day `t`:
- If `t < τ`: price[t] ~ Normal(μ₁, σ)
- If `t ≥ τ`: price[t] ~ Normal(μ₂, σ)

The model finds τ that maximizes the likelihood while respecting priors.

---

## 5. Expected Outputs from Change Point Analysis

### Primary Outputs

1. **Change Point Dates:**
   - **Format:** Posterior distribution over possible dates
   - **Example:** "Change point most likely occurred around July 14, 2008 (95% credible interval: July 10-18, 2008)"
   - **Interpretation:** Peak of posterior distribution indicates most probable date

2. **Regime Parameters:**
   - **Before Change Point:**
     - Mean: μ₁ = $45.30/barrel (95% CI: $43.50 - $47.10)
     - Volatility: σ₁ = $3.20/barrel (95% CI: $2.90 - $3.50)
   - **After Change Point:**
     - Mean: μ₂ = $72.80/barrel (95% CI: $70.20 - $75.40)
     - Volatility: σ₂ = $8.50/barrel (95% CI: $7.80 - $9.20)

3. **Magnitude of Change:**
   - **Absolute Change:** +$27.50/barrel
   - **Percentage Change:** +60.8%
   - **Volatility Change:** +$5.30/barrel (+165%)

4. **Uncertainty Quantification:**
   - **Credible Intervals:** 95% probability ranges for all parameters
   - **Posterior Distributions:** Full probability densities (not just point estimates)
   - **R-hat Values:** Convergence diagnostics (~ 1.00 = good)

5. **Event Attribution:**
   - **Detected Change Point:** July 14, 2008
   - **Associated Event:** Global Financial Crisis (officially September 2008, but oil peaked in July)
   - **Temporal Correlation:** Change point precedes official crisis date
   - **Hypothesis:** Oil markets were forward-looking, pricing in expected recession

### Visualizations

1. **Price Series with Change Points:**
   - Line plot of prices
   - Vertical lines at detected change points
   - Color-coded regimes

2. **Posterior Distributions:**
   - Histogram/density plot of τ samples
   - Shows which dates are most probable
   - Highlights uncertainty

3. **Before/After Comparison:**
   - Side-by-side histograms of μ₁ and μ₂ posteriors
   - Demonstrates separation between regimes

4. **Trace Plots:**
   - MCMC chain behavior over iterations
   - Diagnostic tool for convergence

5. **Event Overlay Chart:**
   - Price series with event spans shaded
   - Change points marked
   - Visual correlation assessment

### Tabular Outputs

1. **Summary Statistics Table:**
   ```
   Parameter | Mean  | SD   | 2.5% | 97.5% | R-hat | ESS
   -------------------------------------------------------
   τ         | 5234  | 12.3 | 5210 | 5258  | 1.00  | 4523
   μ₁        | 45.30 | 0.90 | 43.50| 47.10 | 1.00  | 6789
   μ₂        | 72.80 | 1.30 | 70.20| 75.40 | 1.00  | 6234
   σ         | 5.80  | 0.15 | 5.50 | 6.10  | 1.00  | 5890
   ```

2. **Event-Change Point Mapping:**
   ```
   Change Point Date | Associated Event        | Days Offset | Category
   --------------------------------------------------------------------
   2008-07-14        | Financial Crisis Peak   | -60         | Economic
   2014-11-27        | OPEC No-Cut Decision    | 0           | Policy
   2020-03-15        | COVID-19 + Price War    | +4          | Health/Geopolitical
   ```

### Limitations to Communicate

1. **Not Predictive (Descriptive Only):**
   - Model identifies past change points
   - Cannot predict future change points without additional modeling
   - Historical patterns don't guarantee future behavior

2. **Sensitivity to Model Specification:**
   - Number of change points affects results
   - Prior distributions influence posteriors (though weakly with sufficient data)
   - Choice of likelihood (Normal vs Student-t) matters

3. **Correlation ≠ Causation:**
   - Temporal alignment doesn't prove causality
   - Multiple events may contribute to single change point
   - Some change points may have no clear external cause (market dynamics)

4. **Discrete vs Continuous Change:**
   - Model assumes sharp transitions
   - Real regime changes may be gradual
   - Detected date is an approximation

5. **Data-Dependent:**
   - Results are only as good as the input data
   - Data quality issues propagate to outputs
   - Limited by historical period covered

---

## 6. References & Resources

### Key Literature

1. **Bayesian Statistics & MCMC:**
   - Gelman et al. (2013): *Bayesian Data Analysis*, 3rd Edition
   - McElreath (2020): *Statistical Rethinking*, 2nd Edition
   - Kruschke (2014): *Doing Bayesian Data Analysis*

2. **Change Point Detection:**
   - Barry & Hartigan (1993): "A Bayesian Analysis for Change Point Problems"
   - Chernoff & Zacks (1964): "Estimating the Current Mean of a Normal Distribution which is Subjected to Changes in Time"
   - Killick et al. (2012): "Optimal Detection of Changepoints With a Linear Computational Cost"

3. **Oil Market Analysis:**
   - Hamilton (2009): "Causes and Consequences of the Oil Shock of 2007-08"
   - Kilian (2009): "Not All Oil Price Shocks Are Alike"
   - Baumeister & Kilian (2016): "Understanding the Decline in the Price of Oil since June 2014"

### Technical Resources

1. **PyMC Documentation:** https://www.pymc.io/
2. **ArviZ (Bayesian Visualization):** https://arviz-devs.github.io/arviz/
3. **Bayesian Methods for Hackers:** https://github.com/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers

### Data Sources

1. **Brent Oil Prices:** BrentOilPrices.csv (provided dataset)
2. **Event Database:** Compiled from news archives, OPEC reports, academic papers

---

## 7. Timeline & Milestones

### Task 1 (Foundation) - Current Phase
- [x] Define workflow
- [x] Create event database
- [x] Perform exploratory analysis
- [x] Document assumptions and limitations

### Task 2 (Modeling & Insights) - Next Phase
- [ ] Transform data to log returns
- [ ] Build Bayesian change point model
- [ ] Run MCMC sampling and diagnostics
- [ ] Interpret results and attribute to events
- [ ] Generate visualizations and reports

### Task 3 (Communication) - Final Phase
- [ ] Prepare stakeholder communications via an interactive dashboard

---

**Document Version:** 1.0  
**Last Updated:** February 12, 2026  
**Author:** Mariam Gustavo, 10 Academy
