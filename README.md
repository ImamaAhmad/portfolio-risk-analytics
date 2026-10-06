# Portfolio Risk Lab

## Can Portfolio Optimization Actually Survive Unseen Data?

Portfolio Risk Lab is a quantitative finance project investigating the relationship between **portfolio return, volatility, diversification, optimization, and robustness**.

Rather than assuming that the portfolio with the best historical Sharpe ratio is automatically the best portfolio, this project tests whether optimization results remain convincing when evaluated on data that the model has never seen.

## Research Question

> **Does maximizing historical risk-adjusted return produce a portfolio that generalizes to unseen market conditions?**

## Assets

The analysis uses six diversified ETF-based asset proxies:

* SPY — U.S. equities
* VXUS — International equities
* EEM — Emerging-market equities
* TLT — Long-duration U.S. Treasuries
* GLD — Gold
* VNQ — U.S. real estate

Historical market data is retrieved programmatically using `yfinance`.

## Methodology

The project follows a reproducible quantitative workflow:

1. Download historical market prices.
2. Calculate daily returns.
3. Estimate annualized return and volatility.
4. Calculate Sharpe ratios.
5. Analyze correlations between assets.
6. Construct an equal-weight benchmark portfolio.
7. Optimize portfolio weights subject to long-only constraints.
8. Measure Value at Risk (VaR), Conditional Value at Risk (CVaR), and maximum drawdown.
9. Split the dataset into training and testing periods.
10. Evaluate the optimized strategy on unseen data.
11. Visualize results through an interactive Streamlit dashboard.
12. Perform hypothetical stress testing.

## Key Results

### Equal-Weight Portfolio

* Annualized return: **8.48%**
* Annualized volatility: **12.19%**
* Sharpe ratio: **0.70**
* 95% historical VaR: **−1.14%**
* 95% historical CVaR: **−1.78%**
* Maximum drawdown: **−25.74%**

### Optimized Portfolio — In Sample

The historical optimizer allocated approximately:

* **52.6% SPY**
* **47.4% GLD**
* **0% EEM**
* **0% TLT**
* **0% VNQ**
* **0% VXUS**

This produced:

* Annualized return: **13.11%**
* Annualized volatility: **12.44%**
* Sharpe ratio: **1.05**

### Out-of-Sample Test

When the optimization was trained using data before January 2022 and evaluated on unseen data after that date:

* Annualized return: **5.49%**
* Annualized volatility: **11.69%**
* Sharpe ratio: **0.47**

## Main Finding

The optimized portfolio appeared substantially stronger than the equal-weight portfolio when evaluated across the historical sample used for optimization.

However, its performance deteriorated when tested on unseen observations.

This demonstrates an important principle in quantitative finance:

> **Strong historical optimization results do not necessarily imply strong future generalization.**

The project therefore treats optimization as a model that must be **validated**, rather than as a mechanism for discovering a universally optimal portfolio.

## Risk Analysis

The project examines risk from multiple perspectives rather than relying solely on volatility.

### Volatility

Measures the dispersion of daily returns and provides a standard measure of portfolio uncertainty.

### Value at Risk

Historical 95% VaR estimates a daily loss threshold associated with the lower 5% of observed portfolio returns.

### Conditional Value at Risk

CVaR examines the average loss among observations that fall beyond the VaR threshold, providing additional information about tail risk.

### Maximum Drawdown

Measures the largest peak-to-trough decline experienced by the portfolio.

### Stress Testing

Hypothetical scenarios examine how portfolios might respond to:

* Equity crashes
* Inflation shocks
* Gold declines

These scenarios are illustrative rather than forecasts.

## Technology

* Python
* Pandas
* NumPy
* SciPy
* Matplotlib
* Seaborn
* Plotly
* Streamlit
* yfinance
* Jupyter

## Project Structure

```text
portfolio-risk-analytics/
│
├── app/
│   └── dashboard.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── images/
│
├── notebooks/
│   └── 01_data_collection.ipynb
│
├── README.md
└── requirements.txt
```

## Limitations

This project is an educational quantitative analysis rather than investment advice.

Historical returns are not guaranteed to persist. Portfolio optimization can be sensitive to estimation error, and the chosen historical period, assets, constraints, and risk assumptions can materially affect the results.

The stress tests are hypothetical scenarios and should not be interpreted as predictions.

## Conclusion

The central lesson of this project is not that an optimizer can find a portfolio with an attractive historical Sharpe ratio.

It is that **the apparent quality of an investment strategy depends on how well it survives information it has not already seen**.

This makes out-of-sample validation a central component of the analysis rather than an afterthought.
