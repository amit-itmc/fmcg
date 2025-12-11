import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
from pathlib import Path

# -------------------------------------------------
# BASIC APP SETUP
# -------------------------------------------------
st.set_page_config(
    page_title="AI Demand Forecasting – ITMC FMCG Demo",
    layout="wide",
)

# -------------------------------------------------
# TRY TO LOAD ITMC LOGO (OPTIONAL)
# -------------------------------------------------
logo_path = Path("itmc_logo.png")
has_logo = logo_path.exists()

# HEADER: LOGO + TITLE
header_cols = st.columns([1, 4])
with header_cols[0]:
    if has_logo:
        st.image(str(logo_path), width=80)
with header_cols[1]:
    st.markdown("### AI-Powered Demand Forecasting – FMCG Realtime Demo")
    st.caption(
        "Concept prototype by **ITMC Systems** – Realtime signals, AI-style forecasting, "
        "scenario planning, and a Forecast Copilot chatbot."
    )

st.write("---")

# -------------------------------------------------
# CONSTANTS & SESSION STATE
# -------------------------------------------------
SKU_LIST = [
    "Premium Spice Mix 200g",
    "Breakfast Cereal Choco 500g",
    "Instant Creamer 1kg",
    "Masala Blend 100g",
    "Healthy Oats 1kg",
]

CATEGORIES = ["Cereals", "Spices", "Non-Dairy Creamer"]
REGIONS = ["North", "South", "East", "West"]

# Initialize live data once
if "live_data" not in st.session_state:
    now = dt.datetime.now()
    times = [now - dt.timedelta(minutes=30 - i) for i in range(31)]
    vals = 1000 + np.random.randint(-80, 80, size=len(times))
    st.session_state.live_data = pd.DataFrame(
        {"timestamp": times, "demand_units": vals}
    )

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# -------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------
def add_live_point():
    """Simulate new 'realtime' sales point."""
    df = st.session_state.live_data
    last_time = df["timestamp"].max()
    new_time = last_time + dt.timedelta(minutes=1)
    last_val = df["demand_units"].iloc[-1]
    new_val = max(0, last_val + np.random.randint(-60, 60))
    st.session_state.live_data = pd.concat(
        [df, pd.DataFrame({"timestamp": [new_time], "demand_units": [new_val]})],
        ignore_index=True,
    )


def forecast_sku(sku: str, days: int) -> pd.DataFrame:
    """Simple dummy SKU forecast."""
    base_map = {
        "Premium Spice Mix 200g": 14000,
        "Breakfast Cereal Choco 500g": 16000,
        "Instant Creamer 1kg": 12000,
        "Masala Blend 100g": 9000,
        "Healthy Oats 1kg": 10000,
    }
    base = base_map.get(sku, 12000)

    dates = pd.date_range(
        start=dt.date.today() + dt.timedelta(days=1),
        periods=days,
    )
    values = base + np.random.randint(-1200, 1200, size=len(dates))
    return pd.DataFrame({"date": dates, "forecast_qty": values})


def company_forecast(days: int = 90) -> pd.DataFrame:
    """Dummy company-level actual vs forecast."""
    dates = pd.date_range(
        start=dt.date.today() - dt.timedelta(days=days),
        periods=days,
    )
    actual = 100000 + np.random.randint(-8000, 8000, size=len(dates))
    forecast = 100000 + np.random.randint(-5000, 5000, size=len(dates))
    return pd.DataFrame({"date": dates, "actual": actual, "forecast": forecast})


def category_region_mix() -> pd.DataFrame:
    """Dummy category-region volume for bar chart."""
    data = []
    for cat in CATEGORIES:
        for reg in REGIONS:
            data.append(
                {
                    "category": cat,
                    "region": reg,
                    "forecast_qty": np.random.randint(50_000, 250_000),
                }
            )
    return pd.DataFrame(data)


def scenario_forecast(
    sku: str, days: int, promo_uplift: float, price_change: float
) -> pd.DataFrame:
    """Base vs scenario forecast for scenario planner."""
    base_df = forecast_sku(sku, days)
    base_df = base_df.rename(columns={"forecast_qty": "base"})

    scenario_vals = []
    for val in base_df["base"]:
        # price_change: -10 => price drop => demand increase
        scenario = val * (1 + promo_uplift / 100) * (1 - 0.3 * price_change / 100)
        scenario_vals.append(scenario)

    base_df["scenario"] = np.round(scenario_vals)
    return base_df


def chatbot_response(user_text: str) -> str:
    """Very simple rule-based demo chatbot."""
    text = user_text.lower()

    # SKU-specific forecast
    for sku in SKU_LIST:
        if sku.lower() in text:
            df = forecast_sku(sku, 30)
            total = int(df["forecast_qty"].sum())
            avg = int(df["forecast_qty"].mean())
            return (
                f"For **{sku}**, demo forecast for the next 30 days is about "
                f"**{total:,} units** (avg **{avg:,} units/day**)."
            )

    # Portfolio forecast
    if "next month" in text or "next 30 days" in text or "total forecast" in text:
        total = 0
        for sku in SKU_LIST:
            total += forecast_sku(sku, 30)["forecast_qty"].sum()
        return (
            f"For this demo portfolio, total forecast for the next 30 days is "
            f"around **{int(total):,} units** across key SKUs."
        )

    # Stock-out / risk
    if "stockout" in text or "stock-out" in text or "risk" in text:
        return (
            "In this demo, we assume **7 SKUs** are at potential stock-out risk in the next 2 weeks.\n"
            "In a real system, this is calculated from forecast vs inventory, open POs and safety stock."
        )

    # Promotions / discount
    if "promotion" in text or "promo" in text or "discount" in text:
        return (
            "AI learns promo uplift from history. For example, a 10% discount on a top SKU can "
            "generate ~18–22% demand uplift in this demo. The **Scenario Planner** tab lets you "
            "play with these assumptions visually."
        )

    # Generic
    return (
        "I'm the demo **Forecast Copilot**.\n\n"
        "You can ask things like:\n"
        "- \"Next 30 days forecast for Premium Spice Mix 200g\"\n"
        "- \"Total forecast next month\"\n"
        "- \"Any stockout risk?\"\n"
        "- \"How do promotions impact demand?\""
    )


# -------------------------------------------------
# KPI STRIP
# -------------------------------------------------
k1, k2, k3, k4 = st.columns(4)
k1.metric("Forecast Accuracy (Last 3M)", "92.1%", "+3.4% vs LY")
k2.metric("Next 30 Days Demand", "11.2M units")
k3.metric("SKUs at Stock-Out Risk", "7")
k4.metric("Over-Stock Risk SKUs", "12")

st.write("---")

# -------------------------------------------------
# TABS / PAGES
# -------------------------------------------------
tab_live, tab_company, tab_sku, tab_scenario, tab_bot = st.tabs(
    [
        "📡 Live Sales Feed",
        "📊 Company Forecast Dashboard",
        "🔍 SKU-Level Forecast",
        "🧮 Scenario Planner",
        "💬 Forecast Copilot",
    ]
)

# ---------------- TAB 1: LIVE SALES ----------------
with tab_live:
    st.subheader("Live Sales / Offtake Signal (Simulated)")

    st.caption(
        "In real deployment, this connects to DMS / POS / ERP. "
        "Here we simulate minute-by-minute demand to show the concept."
    )

    if st.button("🔄 Refresh Live Data"):
        add_live_point()

    live_df = st.session_state.live_data.sort_values("timestamp")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Latest Minute Demand", f"{int(live_df['demand_units'].iloc[-1]):,} units")
    with c2:
        st.metric(
            "Last 10-Min Avg",
            f"{int(live_df['demand_units'].tail(10).mean()):,} units",
        )
    with c3:
        st.metric(
            "Last 30-Min Avg",
            f"{int(live_df['demand_units'].mean()):,} units",
        )

    st.line_chart(live_df.set_index("timestamp")["demand_units"])

# ---------------- TAB 2: COMPANY FORECAST ----------------
with tab_company:
    st.subheader("Company-Level Forecast vs Actual")

    comp_df = company_forecast(90)
    st.line_chart(comp_df.set_index("date")[["actual", "forecast"]])

    st.markdown("#### Category–Region Mix (Forecast Volume)")
    mix_df = category_region_mix()
    # Pivot for bar chart: region on x-axis, stacked by category
    mix_pivot = mix_df.pivot(index="region", columns="category", values="forecast_qty")
    st.bar_chart(mix_pivot)

# ---------------- TAB 3: SKU FORECAST ----------------
with tab_sku:
    st.subheader("SKU-Level Forecast")

    col_sku1, col_sku2 = st.columns([2, 1])
    with col_sku1:
        sku_selected = st.selectbox("Select SKU", SKU_LIST)
    with col_sku2:
        horizon = st.slider("Forecast Horizon (days)", min_value=7, max_value=90, value=30)

    sku_df = forecast_sku(sku_selected, horizon)

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Avg Daily Forecast", f"{int(sku_df['forecast_qty'].mean()):,} units")
    with m2:
        st.metric("Total Forecast", f"{int(sku_df['forecast_qty'].sum()):,} units")
    with m3:
        st.metric("Peak Day", f"{int(sku_df['forecast_qty'].max()):,} units")

    st.line_chart(sku_df.set_index("date")["forecast_qty"])

    with st.expander("Show forecast table"):
        st.dataframe(
            sku_df.rename(columns={"date": "Date", "forecast_qty": "Forecast Qty (Units)"})
        )

# ---------------- TAB 4: SCENARIO PLANNER ----------------
with tab_scenario:
    st.subheader("Scenario Planner – Promotions & Price")

    col1, col2, col3 = st.columns(3)
    with col1:
        s_sku = st.selectbox("Select SKU", SKU_LIST, key="scenario_sku")
    with col2:
        promo = st.slider("Promotion Uplift (%)", 0, 50, 20)
    with col3:
        price_change = st.slider("Price Change (%)", -20, 20, -5)

    days = 30
    sc_df = scenario_forecast(s_sku, days, promo, price_change)

    st.line_chart(sc_df.set_index("date")[["base", "scenario"]])

    base_total = sc_df["base"].sum()
    scen_total = sc_df["scenario"].sum()
    uplift_units = scen_total - base_total
    uplift_pct = (uplift_units / base_total) * 100 if base_total > 0 else 0

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Base Volume", f"{int(base_total):,} units")
    with m2:
        st.metric("Scenario Volume", f"{int(scen_total):,} units")
    with m3:
        st.metric("Uplift", f"{int(uplift_units):,} units", f"{uplift_pct:.1f}%")

    st.caption(
        "Use this to explain: ‘Before finalising a promotion or price move, we simulate the impact on demand and supply.’"
    )

# ---------------- TAB 5: CHATBOT ----------------
with tab_bot:
    st.subheader("Forecast Copilot – Chatbot Demo")

    st.caption(
        "Ask in simple English. Examples: "
        "`Next 30 days forecast for Premium Spice Mix 200g`, "
        "`Total forecast next month`, `Any stockout risk?`"
    )

    # Show chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["text"])

    # New user message
    user_msg = st.chat_input("Type your question here...")
    if user_msg:
        st.session_state.chat_history.append({"role": "user", "text": user_msg})
        reply = chatbot_response(user_msg)
        st.session_state.chat_history.append({"role": "assistant", "text": reply})

        with st.chat_message("user"):
            st.write(user_msg)
        with st.chat_message("assistant"):
            st.write(reply)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.write("---")
st.markdown(
    "🟦 **Powered by ITMC Systems** – Empowering Innovation, Delivering Excellence.",
)
