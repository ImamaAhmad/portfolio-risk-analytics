import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="Portfolio Risk Lab",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# CUSTOM STYLE
# -----------------------------

st.markdown("""
<style>

.main {
    background-color: #0b1120;
}

[data-testid="stMetric"] {
    background-color: #111827;
    border: 1px solid #263244;
    padding: 18px;
    border-radius: 12px;
}

h1 {
    color: #f8fafc;
}

h2, h3 {
    color: #cbd5e1;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD DATA
# -----------------------------

prices = pd.read_csv(
    "data/processed/asset_prices.csv",
    index_col=0,
    parse_dates=True
)

prices = prices.apply(pd.to_numeric, errors="coerce")

returns = prices.pct_change().dropna()

# -----------------------------
# PORTFOLIO WEIGHTS
# -----------------------------

assets = ["EEM", "GLD", "SPY", "TLT", "VNQ", "VXUS"]

equal_weights = pd.Series(
    1 / len(assets),
    index=assets
)

optimized_weights = pd.Series({
    "EEM": 0.0,
    "GLD": 0.4740054,
    "SPY": 0.5259946,
    "TLT": 0.0,
    "VNQ": 0.0,
    "VXUS": 0.0
})

# -----------------------------
# PORTFOLIO RETURNS
# -----------------------------

equal_returns = returns[assets].dot(equal_weights)

optimized_returns = returns[assets].dot(optimized_weights)

# -----------------------------
# METRICS
# -----------------------------

def portfolio_metrics(portfolio_returns):

    annual_return = portfolio_returns.mean() * 252

    annual_volatility = (
        portfolio_returns.std() * np.sqrt(252)
    )

    sharpe = annual_return / annual_volatility

    cumulative = (1 + portfolio_returns).cumprod()

    running_max = cumulative.cummax()

    drawdown = cumulative / running_max - 1

    max_drawdown = drawdown.min()

    var_95 = portfolio_returns.quantile(0.05)

    cvar_95 = portfolio_returns[
        portfolio_returns <= var_95
    ].mean()

    return {
        "return": annual_return,
        "volatility": annual_volatility,
        "sharpe": sharpe,
        "drawdown": max_drawdown,
        "var": var_95,
        "cvar": cvar_95
    }


equal_metrics = portfolio_metrics(equal_returns)

optimized_metrics = portfolio_metrics(
    optimized_returns
)

# -----------------------------
# HEADER
# -----------------------------

st.title("📊 Portfolio Risk Lab")

st.markdown(
    """
    ### Can portfolio optimization actually survive unseen data?

    This project investigates the trade-off between **return, risk,
    diversification, and optimization robustness** using historical
    market data.
    """
)

st.divider()

# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.title("Portfolio Lab")

portfolio_choice = st.sidebar.radio(
    "Select Portfolio",
    ["Equal Weight", "Optimized"]
)

if portfolio_choice == "Equal Weight":

    selected_returns = equal_returns
    selected_metrics = equal_metrics
    selected_weights = equal_weights

else:

    selected_returns = optimized_returns
    selected_metrics = optimized_metrics
    selected_weights = optimized_weights

# -----------------------------
# KPI ROW
# -----------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Annual Return",
        f"{selected_metrics['return']:.2%}"
    )

with col2:
    st.metric(
        "Annual Volatility",
        f"{selected_metrics['volatility']:.2%}"
    )

with col3:
    st.metric(
        "Sharpe Ratio",
        f"{selected_metrics['sharpe']:.2f}"
    )

with col4:
    st.metric(
        "Maximum Drawdown",
        f"{selected_metrics['drawdown']:.2%}"
    )

# -----------------------------
# PERFORMANCE CHART
# -----------------------------

st.subheader("Portfolio Growth")

cumulative = (
    1 + selected_returns
).cumprod()

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=cumulative.index,
        y=cumulative,
        mode="lines",
        name=portfolio_choice,
        line=dict(width=3)
    )
)

fig.update_layout(
    template="plotly_dark",
    yaxis_title="Growth of $1",
    xaxis_title="Date",
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------
# RISK SECTION
# -----------------------------

st.subheader("Risk Profile")

risk_col1, risk_col2 = st.columns(2)

with risk_col1:

    st.write("### Drawdown")

    running_max = cumulative.cummax()

    drawdown = (
        cumulative / running_max - 1
    )

    fig_dd = go.Figure()

    fig_dd.add_trace(
        go.Scatter(
            x=drawdown.index,
            y=drawdown,
            fill="tozeroy",
            name="Drawdown"
        )
    )

    fig_dd.update_layout(
        template="plotly_dark",
        yaxis_title="Drawdown",
        xaxis_title="Date"
    )

    st.plotly_chart(
        fig_dd,
        use_container_width=True
    )

with risk_col2:

    st.write("### Tail Risk")

    tail_data = pd.DataFrame({
        "Metric": [
            "95% VaR",
            "95% CVaR"
        ],
        "Loss": [
            selected_metrics["var"],
            selected_metrics["cvar"]
        ]
    })

    fig_tail = px.bar(
        tail_data,
        x="Metric",
        y="Loss",
        color="Metric",
        template="plotly_dark"
    )

    fig_tail.update_layout(
        yaxis_title="Daily Loss",
        showlegend=False
    )

    st.plotly_chart(
        fig_tail,
        use_container_width=True
    )

# -----------------------------
# ALLOCATION
# -----------------------------

st.subheader("Portfolio Allocation")

allocation = pd.DataFrame({
    "Asset": selected_weights.index,
    "Weight": selected_weights.values
})

fig_alloc = px.pie(
    allocation,
    names="Asset",
    values="Weight",
    hole=0.45,
    template="plotly_dark"
)

fig_alloc.update_traces(
    textinfo="label+percent"
)

st.plotly_chart(
    fig_alloc,
    use_container_width=True
)

# -----------------------------
# OPTIMIZATION VS BASELINE
# -----------------------------

st.subheader("Optimization vs. Equal Weight")

comparison = pd.DataFrame({
    "Portfolio": [
        "Equal Weight",
        "Optimized"
    ],
    "Return": [
        equal_metrics["return"],
        optimized_metrics["return"]
    ],
    "Volatility": [
        equal_metrics["volatility"],
        optimized_metrics["volatility"]
    ],
    "Sharpe": [
        equal_metrics["sharpe"],
        optimized_metrics["sharpe"]
    ]
})

fig_compare = px.bar(
    comparison,
    x="Portfolio",
    y="Sharpe",
    color="Portfolio",
    template="plotly_dark",
    title="Risk-Adjusted Performance"
)

st.plotly_chart(
    fig_compare,
    use_container_width=True
)
# -----------------------------
# EFFICIENT FRONTIER
# -----------------------------

st.subheader("Efficient Frontier")

st.write(
    "Each point represents a randomly generated portfolio. "
    "The chart shows the relationship between portfolio risk and return."
)

np.random.seed(42)

n_simulations = 5000

simulation_returns = []
simulation_volatility = []
simulation_sharpe = []

mean_returns = returns[assets].mean() * 252
cov_matrix = returns[assets].cov() * 252

for _ in range(n_simulations):

    weights = np.random.random(len(assets))
    weights = weights / weights.sum()

    portfolio_return = np.dot(weights, mean_returns)

    portfolio_volatility = np.sqrt(
        weights.T @ cov_matrix @ weights
    )

    portfolio_sharpe = portfolio_return / portfolio_volatility

    simulation_returns.append(portfolio_return)
    simulation_volatility.append(portfolio_volatility)
    simulation_sharpe.append(portfolio_sharpe)

frontier = pd.DataFrame({
    "Return": simulation_returns,
    "Volatility": simulation_volatility,
    "Sharpe": simulation_sharpe
})

fig_frontier = px.scatter(
    frontier,
    x="Volatility",
    y="Return",
    color="Sharpe",
    color_continuous_scale="Viridis",
    opacity=0.55,
    title="Portfolio Risk-Return Opportunity Set"
)

fig_frontier.add_trace(
    go.Scatter(
        x=[equal_metrics["volatility"]],
        y=[equal_metrics["return"]],
        mode="markers",
        name="Equal Weight",
        marker=dict(size=14, color="red", symbol="diamond")
    )
)

fig_frontier.add_trace(
    go.Scatter(
        x=[optimized_metrics["volatility"]],
        y=[optimized_metrics["return"]],
        mode="markers",
        name="Optimized",
        marker=dict(size=16, color="white", symbol="star")
    )
)

fig_frontier.update_layout(
    template="plotly_dark",
    xaxis_title="Annualized Volatility",
    yaxis_title="Annualized Return"
)

st.plotly_chart(
    fig_frontier,
    use_container_width=True
)

# -----------------------------
# OUT-OF-SAMPLE RESULT
# -----------------------------

st.subheader("⚠️ Out-of-Sample Reality Check")

st.markdown(
    """
    The optimizer produced a **1.05 historical Sharpe ratio**,
    but when evaluated on unseen data after January 2022,
    the portfolio achieved a Sharpe ratio of approximately **0.47**.

    This gap highlights a central problem in quantitative finance:

    **A strategy that looks excellent on historical data may not
    generalize to future market conditions.**
    """
)

oos_col1, oos_col2, oos_col3 = st.columns(3)

with oos_col1:
    st.metric(
        "In-Sample Sharpe",
        "1.05"
    )

with oos_col2:
    st.metric(
        "Out-of-Sample Sharpe",
        "0.47"
    )

with oos_col3:
    st.metric(
        "Sharpe Difference",
        "-0.58"
    )
# -----------------------------
# STRESS TESTING
# -----------------------------

st.subheader("⚡ Portfolio Stress Test")

st.write(
    "Estimate how each portfolio could react to hypothetical market shocks."
)

stress_scenarios = {
    "Equity Crash": {
        "SPY": -0.30,
        "VXUS": -0.25,
        "EEM": -0.30,
        "VNQ": -0.25,
        "TLT": 0.05,
        "GLD": 0.10
    },

    "Inflation Shock": {
        "SPY": -0.10,
        "VXUS": -0.10,
        "EEM": -0.15,
        "VNQ": -0.15,
        "TLT": -0.20,
        "GLD": 0.15
    },

    "Gold Shock": {
        "SPY": 0.00,
        "VXUS": 0.00,
        "EEM": 0.00,
        "VNQ": 0.00,
        "TLT": 0.00,
        "GLD": -0.25
    }
}

stress_results = []

for scenario, shocks in stress_scenarios.items():

    equal_loss = sum(
        equal_weights[asset] * shocks[asset]
        for asset in assets
    )

    optimized_loss = sum(
        optimized_weights[asset] * shocks[asset]
        for asset in assets
    )

    stress_results.append({
        "Scenario": scenario,
        "Equal Weight": equal_loss,
        "Optimized": optimized_loss
    })

stress_df = pd.DataFrame(stress_results)

fig_stress = px.bar(
    stress_df,
    x="Scenario",
    y=["Equal Weight", "Optimized"],
    barmode="group",
    template="plotly_dark",
    title="Hypothetical Portfolio Stress Scenarios"
)

fig_stress.update_layout(
    yaxis_title="Estimated Portfolio Return",
    xaxis_title="Scenario"
)

st.plotly_chart(
    fig_stress,
    use_container_width=True
)

# -----------------------------
# FOOTER
# -----------------------------

st.divider()

st.caption(
    "Portfolio Risk Lab • Historical analysis for educational and research purposes."
)