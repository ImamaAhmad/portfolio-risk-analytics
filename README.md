# Portfolio Risk Lab

## Can Portfolio Optimization Actually Survive Unseen Data?

**Portfolio Risk Lab** is an interactive quantitative-finance project investigating whether historical portfolio optimization results remain convincing when tested against **unseen market data**.

**[Launch the Portfolio Risk Lab Dashboard](https://portfolio-risk-analytics-project.streamlit.app/)**

The project combines portfolio optimization, statistical risk analysis, diversification analysis, out-of-sample validation, and hypothetical stress testing into an interactive Streamlit application.

---

## Research Question

> Does maximizing historical risk-adjusted return produce a portfolio that performs robustly on unseen market data?

Instead of treating the portfolio with the highest historical Sharpe ratio as automatically superior, this project asks a more important question:

**Does the strategy generalize?**

---

## What This Project Does

The project follows a complete quantitative research workflow:

1. Collect historical market data
2. Clean and prepare price data
3. Calculate daily asset returns
4. Analyze annualized return and volatility
5. Compare asset-level Sharpe ratios
6. Examine correlations and diversification
7. Construct an equal-weight benchmark portfolio
8. Optimize portfolio weights
9. Measure portfolio risk using VaR, CVaR, and maximum drawdown
10. Perform out-of-sample validation
11. Simulate an efficient frontier
12. Stress-test portfolios under hypothetical market shocks
13. Present the results through an interactive dashboard

---

## Asset Universe

The analysis uses six diversified ETF-based asset proxies:

| Ticker   | Asset Exposure                | Role                              |
| -------- | ----------------------------- | --------------------------------- |
| **SPY**  | U.S. equities                 | Core equity exposure              |
| **VXUS** | International equities        | Geographic diversification        |
| **EEM**  | Emerging-market equities      | Higher-risk growth exposure       |
| **TLT**  | Long-duration U.S. Treasuries | Defensive / fixed-income exposure |
| **GLD**  | Gold                          | Alternative / defensive exposure  |
| **VNQ**  | U.S. real estate              | Real-estate exposure              |

These instruments are used as **research proxies**, not investment recommendations.

---

# Methodology

## 1. Historical Data

Daily historical market prices are collected programmatically using `yfinance`.

The dataset begins in **2015** and contains multiple years of market observations across the six asset classes.

Prices are adjusted before calculating returns to better represent the economic return series.

---

## 2. Asset-Level Analysis

For each asset, the project calculates:

* Annualized return
* Annualized volatility
* Sharpe ratio

The annualization assumes approximately **252 trading days per year**.

### Historical Sharpe Results

| Asset | Sharpe Ratio |
| ----- | -----------: |
| SPY   |     **0.83** |
| GLD   |     **0.71** |
| VXUS  |     **0.54** |
| EEM   |     **0.44** |
| VNQ   |     **0.33** |
| TLT   |    **−0.03** |

These results provide a starting point for understanding the risk-return characteristics of the individual assets.

---

# Portfolio Construction

Two main portfolios are compared.

### Equal-Weight Portfolio

Each asset receives an equal allocation.

This serves as a simple benchmark that does not attempt to forecast which asset will perform best.

### Optimized Portfolio

Portfolio weights are optimized using historical return and covariance information with a focus on maximizing risk-adjusted performance.

The optimization is constrained to long-only positions.

---

# In-Sample Results

The equal-weight portfolio produced:

| Metric            | Equal Weight |
| ----------------- | -----------: |
| Annual Return     |    **8.48%** |
| Annual Volatility |   **12.19%** |
| Sharpe Ratio      |     **0.70** |

The optimized portfolio produced:

| Metric            |  Optimized |
| ----------------- | ---------: |
| Annual Return     | **13.11%** |
| Annual Volatility | **12.44%** |
| Sharpe Ratio      |   **1.05** |

The optimizer produced a substantially higher historical Sharpe ratio while maintaining a similar level of volatility.

However, this is **not treated as proof that the optimized portfolio is superior**.

That distinction motivates the out-of-sample analysis.

---

# The Optimization Result

The historical optimization allocated approximately:

| Asset | Optimized Weight |
| ----- | ---------------: |
| SPY   |       **52.60%** |
| GLD   |       **47.40%** |
| EEM   |        **0.00%** |
| TLT   |        **0.00%** |
| VNQ   |        **0.00%** |
| VXUS  |        **0.00%** |

This result is itself informative.

Rather than producing a broadly diversified portfolio, the optimizer concentrated almost entirely in **SPY and GLD**.

This highlights an important limitation of optimization:

> A mathematically optimal solution can become highly concentrated when historical estimates strongly favor a small number of assets.

---

# Portfolio Risk Analysis

The project evaluates risk using several complementary measures.

### Value at Risk

The historical **95% daily VaR** was:

**−1.14%**

This represents a historical threshold for losses in the lower 5% of the observed daily-return distribution.

### Conditional Value at Risk

The historical **95% CVaR** was:

**−1.78%**

CVaR examines the average loss among observations beyond the VaR threshold, providing additional information about tail losses.

### Maximum Drawdown

The maximum historical drawdown was:

**−25.74%**

This measures the largest peak-to-trough decline experienced by the portfolio during the sample.

---

# Out-of-Sample Validation

One of the central features of this project is the separation between **training data and unseen test data**.

The portfolio optimization is performed using historical information before the test period.

The resulting portfolio is then evaluated on observations that were **not used during optimization**.

### Out-of-Sample Results

| Metric            | Out-of-Sample |
| ----------------- | ------------: |
| Annual Return     |     **5.49%** |
| Annual Volatility |    **11.69%** |
| Sharpe Ratio      |      **0.47** |

The optimized strategy's Sharpe ratio fell from approximately:

**1.05 → 0.47**

when moving from the historical optimization environment to unseen data.

---

# Main Finding

The most important result of the project is **not** that optimization produced a Sharpe ratio above 1.

It is that the apparent improvement **did not fully survive out-of-sample testing**.

The optimized portfolio looked considerably stronger using the historical data used for estimation, but its risk-adjusted performance weakened when evaluated on unseen observations.

This demonstrates a fundamental issue in quantitative finance:

> **A portfolio that looks optimal on historical data is not necessarily optimal in a different market environment.**

The result highlights the importance of:

* Out-of-sample validation
* Model robustness
* Estimation uncertainty
* Diversification
* Avoiding over-reliance on historical optimization

---

# Interactive Dashboard

The entire analysis is presented through an interactive Streamlit dashboard.

### Live Application

**[Portfolio Risk Lab — Streamlit](https://portfolio-risk-analytics-project.streamlit.app/)**

The dashboard includes:

* Portfolio performance
* Risk metrics
* Asset correlation analysis
* Portfolio optimization
* Efficient-frontier simulations
* Out-of-sample validation
* Portfolio stress testing

---

# Stress Testing

The dashboard includes hypothetical scenario analysis to explore how different portfolio structures could react to extreme conditions.

Current scenarios include:

### Equity Crash

Simulates a severe decline across equity markets while assigning different responses to defensive assets.

### Inflation Shock

Simulates a period in which traditional bonds and risk assets experience pressure while gold performs relatively better.

### Gold Shock

Tests the sensitivity of portfolios to a sharp decline in gold.

These scenarios are **hypothetical stress tests, not forecasts**.

Their purpose is to examine portfolio sensitivity under alternative market conditions.

---

# Efficient Frontier

The dashboard generates thousands of randomly weighted portfolios and plots their estimated risk-return characteristics.

This creates an interactive visualization of the portfolio opportunity set.

The equal-weight and optimized portfolios are highlighted to show where they sit relative to alternative combinations of the six assets.

---

# Technology Stack

The project was built using:

* **Python**
* **Pandas**
* **NumPy**
* **SciPy**
* **Matplotlib**
* **Seaborn**
* **Plotly**
* **Streamlit**
* **yfinance**
* **Jupyter**

---

# Project Structure

```text
portfolio-risk-analytics/
│
├── app/
│   └── dashboard.py
│
├── data/
│   ├── raw/
│   └── processed/
│       ├── asset_prices.csv
│       ├── optimal_weights.csv
│       ├── out_of_sample_results.csv
│       ├── portfolio_comparison.csv
│       └── risk_metrics.csv
│
├── images/
│
├── notebooks/
│   └── 01_data_collection.ipynb
│
├── src/
│
├── README.md
└── requirements.txt
```

---

# Running the Project Locally

Clone the repository and enter the project directory:

```bash
git clone https://github.com/ImamaAhmad/portfolio-risk-analytics.git
cd portfolio-risk-analytics
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Launch the dashboard:

```bash
streamlit run app/dashboard.py
```

The application should then open in your browser.

---

# Limitations

This project is an educational quantitative-finance analysis and **not investment advice**.

Several limitations should be considered:

* Historical returns do not guarantee future performance.
* Optimization is sensitive to the historical sample period.
* Expected returns and covariance estimates contain estimation error.
* The selected assets represent only a small portion of investable markets.
* Transaction costs and taxes are not modeled.
* Portfolio rebalancing costs are not modeled.
* Stress scenarios are hypothetical.
* The optimization framework may produce concentrated allocations.

These limitations are important because they prevent the results from being interpreted as a guaranteed investment strategy.

---

# Conclusion

Portfolio optimization can produce an attractive historical risk-return profile.

However, this project shows why **historical performance alone is not enough**.

The optimized portfolio achieved a historical Sharpe ratio of approximately **1.05**, compared with **0.70** for the equal-weight portfolio.

When evaluated on unseen data, however, the optimized strategy's Sharpe ratio declined to approximately **0.47**.

The result suggests that optimization can capture relationships that are specific to the historical period used for estimation.

Therefore, the central lesson of Portfolio Risk Lab is:

> **The real test of an investment model is not how well it explains the past, but how robustly it performs when confronted with data it has never seen.**

---

# Project Status

**Completed**

The project includes:

* [x] Historical data collection
* [x] Return analysis
* [x] Risk analysis
* [x] Correlation analysis
* [x] Equal-weight portfolio
* [x] Portfolio optimization
* [x] VaR / CVaR
* [x] Maximum drawdown
* [x] Out-of-sample validation
* [x] Efficient frontier
* [x] Stress testing
* [x] Interactive Streamlit dashboard
* [x] Reproducible environment
* [x] Project documentation
