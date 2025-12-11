import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
from pathlib import Path
import altair as alt

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="ITMC FMCG ERP + AI",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# GLOBAL THEME (LIGHT, NEUTRAL, NO BLUE) – CSS
# --------------------------------------------------
st.markdown(
    """
<style>
/* ===== GLOBAL PAGE ===== */
.main {
    background: #f3f4f6;
    color: #111827;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
.block-container {
    padding-top: 0.6rem;
    padding-bottom: 2rem;
}

/* Default text sizes */
h1, h2, h3, h4, h5, h6 {
    color: #0f172a !important;
    font-weight: 700 !important;
}
p, div, label, span {
    font-size: 15px !important;
    color: #111827 !important;
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background: #ffffff;
    color: #111827;
    border-right: 1px solid #e5e7eb;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-size: 16px !important;
    font-weight: 700 !important;
    color: #111827 !important;
}
[data-testid="stSidebar"] label {
    font-size: 14px !important;
}

/* Sidebar radio labels (modules) */
[data-testid="stSidebar"] .stRadio label {
    color: #111827 !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    padding: 8px 12px;
    border-radius: 8px;
    margin-bottom: 4px;
    transition: background 0.15s ease-out;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: #e5e7eb;
}
[data-testid="stSidebar"] .stRadio div[role='radiogroup'] > label[data-checked="true"] {
    background: #4b5563;
    color: #f9fafb !important;
}

/* ===== KPI CARDS ===== */
[data-testid="stMetric"] {
    background: #ffffff;
    padding: 1.1rem;
    border-radius: 16px;
    box-shadow: 0 6px 18px rgba(15,23,42,0.10);
    border: 1px solid #e5e7eb;
}
[data-testid="stMetricLabel"] {
    font-size: 15px !important;
    color: #374151 !important;   /* neutral dark grey */
}
[data-testid="stMetricValue"] {
    font-size: 20px !important;
    font-weight: 700 !important;
}

/* ===== SECTION CARDS ===== */
.card {
    background: #ffffff;
    padding: 1.2rem 1.3rem;
    border-radius: 18px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 10px 25px rgba(15,23,42,0.08);
    margin-bottom: 1rem;
}

/* ===== TOP HEADER BAR ===== */
.header-bar {
    background: linear-gradient(90deg, #111827, #374151); /* dark greys */
    padding: 0.8rem 1.1rem;
    border-radius: 0 0 20px 20px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    color:#f9fafb;
    margin-bottom:0.9rem;
}
.header-title {
    font-size: 1.1rem;
    font-weight: 700;
}
.header-sub {
    font-size: 1rem !important;
    font-weight: 600 !important;
    color: #f9fafb !important;
    opacity: 1 !important;
}


/* ===== TOP PILL BELOW HEADER ===== */
.top-pill {
    background: #e5e7eb;      /* light neutral grey */
    color: #1f2937;
    padding: 0.6rem 1.1rem;
    border-radius: 999px;
    font-size: 13px;
    display:flex;
    justify-content:space-between;
    align-items:center;
    border: 1px solid #d1d5db;
    margin-bottom: 0.8rem;
}

/* small feature chips */
.badge-chip {
    display:inline-block;
    padding:3px 10px;
    border-radius:999px;
    background:#ffffff;
    border:1px solid #d1d5db;
    font-size: 12px;
    color:#374151;
    margin-right:6px;
}

/* module-specific banner */
.module-banner {
    background:#f3f4f6;
    border-radius:14px;
    padding:0.5rem 0.75rem;
    font-size:13px;
    color:#111827;
    border:1px solid #e5e7eb;
    margin-bottom:0.7rem;
}

/* muted labels / hints */
.muted-label {
    font-size:12px !important;
    color:#6b7280 !important;
}

/* ===== TABLES ===== */
table, th, td {
    font-size: 14px !important;
}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar {
    width: 7px;
    height: 7px;
}
::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 999px;
}
::-webkit-scrollbar-track {
    background: transparent;
}
</style>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# CONSTANTS / MASTER DATA
# --------------------------------------------------
SKU_LIST = [
    "Premium Spice Mix 200g",
    "Breakfast Cereal Choco 500g",
    "Instant Creamer 1kg",
    "Masala Blend 100g",
    "Healthy Oats 1kg",
]
REGIONS = ["North", "South", "East", "West"]
CHANNELS = ["General Trade", "Modern Trade", "E-Commerce"]
WAREHOUSES = ["WH–North", "WH–South", "WH–East", "WH–West"]
CUSTOMERS = ["Retailer A", "Retailer B", "Modern Trade X", "Distributor Y", "E-Com Z"]
VENDORS = ["Vendor 1", "Vendor 2", "Vendor 3"]
MONTHS_BACK = 12


# --------------------------------------------------
# DUMMY DATA GENERATION
# --------------------------------------------------
def init_dummy_data():
    today = dt.date.today()
    months = pd.date_range(
        start=(today - pd.DateOffset(months=MONTHS_BACK - 1)).replace(day=1),
        periods=MONTHS_BACK,
        freq="MS",
    )

    # Sales orders
    so_rows = []
    for i in range(1, 101):
        so_rows.append(
            {
                "order_id": f"SO-{1000 + i}",
                "order_date": today - dt.timedelta(days=np.random.randint(0, 60)),
                "customer": np.random.choice(CUSTOMERS),
                "region": np.random.choice(REGIONS),
                "channel": np.random.choice(CHANNELS),
                "sku": np.random.choice(SKU_LIST),
                "qty": np.random.randint(50, 500),
                "amount": np.random.randint(50_000, 300_000),
                "status": np.random.choice(["Pending", "Allocated", "Dispatched"]),
            }
        )
    sales_orders = pd.DataFrame(so_rows)

    # Inventory
    inv_rows = []
    for wh in WAREHOUSES:
        for sku in SKU_LIST:
            inv_rows.append(
                {
                    "warehouse": wh,
                    "sku": sku,
                    "on_hand": np.random.randint(2000, 15000),
                    "in_transit": np.random.randint(0, 5000),
                    "reorder_point": np.random.randint(3000, 7000),
                }
            )
    inventory = pd.DataFrame(inv_rows)

    # Purchase orders
    po_rows = []
    for i in range(1, 51):
        po_rows.append(
            {
                "po_id": f"PO-{600 + i}",
                "po_date": today - dt.timedelta(days=np.random.randint(0, 60)),
                "vendor": np.random.choice(VENDORS),
                "sku": np.random.choice(SKU_LIST),
                "qty": np.random.randint(500, 2000),
                "amount": np.random.randint(100_000, 600_000),
                "status": np.random.choice(["Open", "In Transit", "Received"]),
            }
        )
    purchase_orders = pd.DataFrame(po_rows)

    # Production
    prod_rows = []
    for sku in SKU_LIST:
        for m in months:
            plan = np.random.randint(10000, 30000)
            actual = int(plan * np.random.uniform(0.9, 1.1))
            prod_rows.append(
                {
                    "month": m,
                    "sku": sku,
                    "plan_qty": plan,
                    "actual_qty": actual,
                }
            )
    production = pd.DataFrame(prod_rows)

    # Finance P&L
    fin_rows = []
    base_rev = 5_000_000
    for m in months:
        revenue = base_rev + np.random.randint(-500_000, 800_000)
        cogs = int(revenue * np.random.uniform(0.6, 0.75))
        opex = int(revenue * np.random.uniform(0.12, 0.18))
        fin_rows.append(
            {
                "month": m,
                "revenue": revenue,
                "cogs": cogs,
                "opex": opex,
            }
        )
        base_rev *= np.random.uniform(0.97, 1.05)
    finance = pd.DataFrame(fin_rows)
    finance["gross_profit"] = finance["revenue"] - finance["cogs"]
    finance["ebit"] = finance["gross_profit"] - finance["opex"]

    return {
        "sales_orders": sales_orders,
        "inventory": inventory,
        "purchase_orders": purchase_orders,
        "production": production,
        "finance": finance,
        "months": months,
    }


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "data" not in st.session_state:
    st.session_state.data = init_dummy_data()
if "activity_log" not in st.session_state:
    st.session_state.activity_log = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "replenishment_orders" not in st.session_state:
    st.session_state.replenishment_orders = []
if "next_repl_id" not in st.session_state:
    st.session_state.next_repl_id = 1

data = st.session_state.data

# --------------------------------------------------
# FORECAST HELPERS
# --------------------------------------------------
def simple_forecast(series, months=3, growth=1.04):
    base = series.tail(3).mean()
    vals = []
    val = base
    for _ in range(months):
        val *= growth * np.random.uniform(0.97, 1.05)
        vals.append(int(val))
    return vals


def finance_forecast(df, months=3):
    last_month = df["month"].max()
    next_months = [last_month + pd.DateOffset(months=i) for i in range(1, months + 1)]

    rev_fc = simple_forecast(df["revenue"], months)
    cogs_fc = simple_forecast(df["cogs"], months)
    opex_fc = simple_forecast(df["opex"], months)

    rows = []
    for i, m in enumerate(next_months):
        rev = rev_fc[i]
        cogs = cogs_fc[i]
        opex = opex_fc[i]
        rows.append(
            {
                "month": m,
                "revenue": rev,
                "cogs": cogs,
                "opex": opex,
                "gross_profit": rev - cogs,
                "ebit": (rev - cogs) - opex,
            }
        )
    return pd.DataFrame(rows)


# --------------------------------------------------
# ALERTS + LOGGING
# --------------------------------------------------
def log_event(action, detail):
    st.session_state.activity_log.append(
        {
            "time": dt.datetime.now(),
            "user": st.session_state.get("current_user", "unknown"),
            "action": action,
            "detail": detail,
        }
    )


def alert(msg):
    st.info(f"🔔 {msg}")


def whatsapp_demo(msg):
    st.success(f"📲 WhatsApp (demo): {msg}")


def build_daily_alert_message():
    fin = data["finance"]
    last = fin.iloc[-1]
    fc = finance_forecast(fin, 3)
    lines = [
        "ITMC – AI Daily Alert Summary",
        "------------------------------------",
        f"Last Month Revenue: ₹ {last['revenue']:,}",
        f"Last Month EBIT: ₹ {last['ebit']:,}",
        "",
        "Next 3-Month Finance Forecast:",
    ]
    for _, row in fc.iterrows():
        month = row["month"].strftime("%b %Y")
        lines.append(
            f"- {month}: Revenue ~₹ {row['revenue']:,}, EBIT ~₹ {row['ebit']:,}"
        )
    return "\n".join(lines)


# --------------------------------------------------
# REPLENISHMENT / APPROVALS
# --------------------------------------------------
def detect_shortages(inv_df):
    return inv_df[inv_df["on_hand"] < inv_df["reorder_point"]]


def create_replenishment_proposals():
    inv = data["inventory"]
    shortages = detect_shortages(inv)
    created = 0
    existing_keys = {
        (r["warehouse"], r["sku"])
        for r in st.session_state.replenishment_orders
        if r["status"] != "PO Created"
    }

    for _, row in shortages.iterrows():
        key = (row["warehouse"], row["sku"])
        if key in existing_keys:
            continue
        target = int(row["reorder_point"] * 1.5)
        qty = max(0, target - int(row["on_hand"]))
        if qty <= 0:
            continue

        rid = st.session_state.next_repl_id
        st.session_state.next_repl_id += 1

        proposal = {
            "id": rid,
            "warehouse": row["warehouse"],
            "sku": row["sku"],
            "on_hand": int(row["on_hand"]),
            "reorder_point": int(row["reorder_point"]),
            "suggested_qty": int(qty),
            "status": "Proposed",
            "planner_approved_by": None,
            "scm_approved_by": None,
            "finance_approved_by": None,
            "po_id": None,
        }
        st.session_state.replenishment_orders.append(proposal)
        created += 1

        detail = (
            f"AI created replenishment #{rid} for {row['sku']} in {row['warehouse']} "
            f"(on-hand {row['on_hand']}, ROP {row['reorder_point']}, qty {qty})"
        )
        log_event("REPLENISHMENT_PROPOSAL", detail)
        alert(detail)
        whatsapp_demo(f"[AI Replenishment] {detail}")

    return created


def auto_create_po(order):
    po_df = data["purchase_orders"]
    new_po_id = f"PO-AI-{1000 + order['id']}"
    new_row = {
        "po_id": new_po_id,
        "po_date": dt.date.today(),
        "vendor": np.random.choice(VENDORS),
        "sku": order["sku"],
        "qty": order["suggested_qty"],
        "amount": np.random.randint(100_000, 600_000),
        "status": "Open",
    }
    po_df = pd.concat([po_df, pd.DataFrame([new_row])], ignore_index=True)
    data["purchase_orders"] = po_df

    order["po_id"] = new_po_id
    order["status"] = "PO Created"

    detail = f"Auto PO {new_po_id} created for {order['sku']} qty {order['suggested_qty']}."
    log_event("PO_CREATED", detail)
    alert(detail)
    whatsapp_demo(f"[AI Auto PO] {detail}")


def approve_replenishment(order_id: int):
    role = st.session_state.current_role
    user = st.session_state.current_user

    for order in st.session_state.replenishment_orders:
        if order["id"] != order_id:
            continue

        prev_status = order["status"]

        if role == "Planner" and order["status"] == "Proposed":
            order["status"] = "Planner Approved"
            order["planner_approved_by"] = user
        elif role == "SCM Head" and order["status"] == "Planner Approved":
            order["status"] = "SCM Approved"
            order["scm_approved_by"] = user
        elif role == "Finance" and order["status"] == "SCM Approved":
            order["status"] = "Finance Approved"
            order["finance_approved_by"] = user
            auto_create_po(order)
        else:
            alert(
                f"Role '{role}' cannot approve order #{order_id} from status '{order['status']}'."
            )
            return

        detail = f"{role} {user} approved order #{order_id} ({prev_status} → {order['status']})"
        log_event("APPROVAL", detail)
        whatsapp_demo(f"[Approval] {detail}")
        return

    alert(f"Order #{order_id} not found.")


# --------------------------------------------------
# CHATBOT
# --------------------------------------------------
def chatbot_response(text: str) -> str:
    t = text.lower()
    fin = data["finance"]

    if any(k in t for k in ["revenue", "ebit", "p&l", "profit"]):
        last = fin.iloc[-1]
        fc = finance_forecast(fin, 3)
        msg = [
            f"Last month revenue: ₹ {last['revenue']:,}",
            f"Last month EBIT: ₹ {last['ebit']:,}",
            "",
            "AI forecast for next 3 months:",
        ]
        for _, row in fc.iterrows():
            msg.append(
                f"- {row['month'].strftime('%b %Y')}: Revenue ~₹ {row['revenue']:,}, EBIT ~₹ {row['ebit']:,}"
            )
        return "\n".join(msg)

    if "stock" in t or "shortage" in t or "reorder" in t:
        inv = data["inventory"]
        short = detect_shortages(inv)
        if short.empty:
            return "AI check: no SKUs below reorder point right now in this demo."
        lines = ["AI check: below-reorder SKUs (demo):"]
        for _, r in short.iterrows():
            lines.append(
                f"- {r['warehouse']} – {r['sku']}: on-hand {r['on_hand']}, ROP {r['reorder_point']}"
            )
        return "\n".join(lines)

    if "po" in t or "purchase order" in t or "auto" in t:
        return (
            "AI creates replenishment proposals when stock is below reorder point, "
            "routes them through Planner → SCM Head → Finance approvals, and after Finance approval, "
            "automatically creates a Purchase Order."
        )

    return (
        "I'm the Forecast Copilot for this FMCG ERP demo.\n\n"
        "Try asking things like:\n"
        "- \"Revenue forecast next 3 months\"\n"
        "- \"Any stock shortage risk?\"\n"
        "- \"How does AI auto-create POs?\""
    )


# --------------------------------------------------
# SIDEBAR – USER CONTEXT & MODULE
# --------------------------------------------------
st.sidebar.markdown("### User Context")
current_user = st.sidebar.text_input("Logged in as (name/email)", "demo@itmc.in")
current_role = st.sidebar.selectbox(
    "Current Role (for approvals)",
    ["Viewer", "Planner", "SCM Head", "Finance", "Admin"],
    index=0,
)
st.session_state.current_user = current_user
st.session_state.current_role = current_role

st.sidebar.markdown("---")

module = st.sidebar.radio(
    "Choose Module",
    [
        "ERP Operations Dashboard",
        "Sales & Orders",
        "Inventory & Supply Chain",
        "Production",
        "Finance & AI Forecasting",
        "Upload & Explore Data",
        "AI Generated Alerts & Activity Log",
        "AI Forecast Copilot",
    ],
)

st.sidebar.markdown("---")
st.sidebar.caption("ITMC FMCG ERP + AI Control Tower")

# --------------------------------------------------
# HEADER BAR
# --------------------------------------------------
logo_path = Path("itmc_logo.png")
logo_html = ""
if logo_path.exists():
    logo_html = (
        '<img src="itmc_logo.png" style="height:42px;margin-right:12px;border-radius:10px;" />'
    )

st.markdown(
    f"""
<div class="header-bar">
    <div style="display:flex; align-items:center;">
        {logo_html}
        <div>
            <div class="header-title">ITMC FMCG ERP + AI Forecasting Platform</div>
            <div class="header-sub">Unified control tower across Sales • Inventory • Production • Finance • Forecast Copilot</div>
        </div>
    </div>
    <div style="text-align:right; font-size:0.85rem;">
        <div><b>{current_user}</b></div>
        <div style="color:#e5e7eb;">Role: {current_role}</div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# TOP PILL
# --------------------------------------------------
st.markdown(
    """
<div class="top-pill">
    <div>
        <span class="badge-chip">AI Forecasting</span>
        <span class="badge-chip">Replenishment Engine</span>
        <span class="badge-chip">Multi-level Approvals</span>
        <span class="badge-chip">Alerts + WhatsApp (demo)</span>
    </div>
    <div style="font-size:12px;">Environment: Demo • Sector: FMCG • Powered by ITMC Systems</div>
</div>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# KPI STRIP
# --------------------------------------------------
fin = data["finance"]
last_fin = fin.iloc[-1]
inv_value = int(data["inventory"]["on_hand"].sum() * 50)

k1, k2, k3 = st.columns(3)
k1.metric("Last Month Revenue", f"₹ {last_fin['revenue']:,}")
k2.metric("Last Month EBIT", f"₹ {last_fin['ebit']:,}")
k3.metric("Inventory Value (Approx)", f"₹ {inv_value:,}")

st.write("")

# --------------------------------------------------
# MODULES
# --------------------------------------------------
if module == "ERP Operations Dashboard":
    st.markdown(
        '<div class="module-banner">📊 <b>Operations Snapshot:</b> Single view of revenue, EBIT, sales mix and inventory health for leadership.</div>',
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("ERP Operations Dashboard – End-to-End View")

        st.markdown("##### Revenue & EBIT – Last 12 Months")

        fin_long = fin[["month", "revenue", "ebit"]].melt(
            "month", var_name="metric", value_name="value"
        )
        rev_chart = (
            alt.Chart(fin_long)
            .mark_line(point=False, strokeWidth=2)
            .encode(
                x=alt.X("month:T", title="Month"),
                y=alt.Y("value:Q", title="Amount (₹)"),
                color=alt.Color(
                    "metric:N",
                    title="",
                    scale=alt.Scale(range=["#16a34a", "#f97316"]),  # green + orange
                ),
                tooltip=["month:T", "metric:N", "value:Q"],
            )
            .properties(height=280)
        )
        st.altair_chart(rev_chart, use_container_width=True)

        so = data["sales_orders"]
        inv = data["inventory"]

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("##### Sales Mix by Region")
            region_df = so.groupby("region")["amount"].sum().reset_index()
            region_chart = (
                alt.Chart(region_df)
                .mark_bar(color="#6b7280")
                .encode(
                    x=alt.X("region:N", title="Region"),
                    y=alt.Y("amount:Q", title="Sales Amount (₹)"),
                    tooltip=["region:N", "amount:Q"],
                )
                .properties(height=260)
            )
            st.altair_chart(region_chart, use_container_width=True)
        with c2:
            st.markdown("##### Sales Mix by Channel")
            channel_df = so.groupby("channel")["amount"].sum().reset_index()
            channel_chart = (
                alt.Chart(channel_df)
                .mark_bar(color="#6b7280")
                .encode(
                    x=alt.X("channel:N", title="Channel"),
                    y=alt.Y("amount:Q", title="Sales Amount (₹)"),
                    tooltip=["channel:N", "amount:Q"],
                )
                .properties(height=260)
            )
            st.altair_chart(channel_chart, use_container_width=True)

        st.markdown("##### Inventory by Warehouse")
        wh_df = inv.groupby("warehouse")["on_hand"].sum().reset_index()
        wh_chart = (
            alt.Chart(wh_df)
            .mark_bar(color="#9ca3af")
            .encode(
                x=alt.X("warehouse:N", title="Warehouse"),
                y=alt.Y("on_hand:Q", title="On-hand Qty"),
                tooltip=["warehouse:N", "on_hand:Q"],
            )
            .properties(height=260)
        )
        st.altair_chart(wh_chart, use_container_width=True)

        st.markdown(
            '<div class="muted-label">Client value: leadership sees how demand, margin and inventory are moving together.</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

elif module == "Sales & Orders":
    st.markdown(
        '<div class="module-banner">🛒 <b>Sales Control:</b> Filter orders by region, channel and status to support trade & promotion decisions.</div>',
        unsafe_allow_html=True,
    )
    st.subheader("Sales & Orders")

    so = data["sales_orders"]
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            rf = st.selectbox("Region", ["All"] + REGIONS)
        with c2:
            cf = st.selectbox("Channel", ["All"] + CHANNELS)
        with c3:
            sf = st.selectbox("Status", ["All", "Pending", "Allocated", "Dispatched"])
        st.markdown("</div>", unsafe_allow_html=True)

    df = so.copy()
    if rf != "All":
        df = df[df["region"] == rf]
    if cf != "All":
        df = df[df["channel"] == cf]
    if sf != "All":
        df = df[df["status"] == sf]

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("##### Order Book")
        st.dataframe(df, use_container_width=True, height=350)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("##### Daily Sales Trend")
        daily = df.groupby("order_date")["amount"].sum().sort_index()
        if not daily.empty:
            daily_df = daily.reset_index().rename(columns={"order_date": "date", "amount": "amount"})
            sales_chart = (
                alt.Chart(daily_df)
                .mark_line(strokeWidth=2, color="#16a34a")
                .encode(
                    x=alt.X("date:T", title="Date"),
                    y=alt.Y("amount:Q", title="Sales Amount (₹)"),
                    tooltip=["date:T", "amount:Q"],
                )
                .properties(height=240)
            )
            st.altair_chart(sales_chart, use_container_width=True)
        else:
            st.info("No data for selected filters.")
        st.markdown(
            '<div class="muted-label">Client value: great for trade review meetings, promotion tracking and key account discussions.</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

elif module == "Inventory & Supply Chain":
    st.markdown(
        '<div class="module-banner">📦 <b>Inventory & Replenishment:</b> AI keeps stock balanced between stock-outs and overstock.</div>',
        unsafe_allow_html=True,
    )
    st.subheader("Inventory & Supply Chain")

    inv = data["inventory"]
    po = data["purchase_orders"]

    tab1, tab2 = st.tabs(["📊 Inventory Overview", "🤖 AI Replenishment & Auto-PO"])

    with tab1:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("##### Inventory by Warehouse")
            wh_df = inv.groupby("warehouse")["on_hand"].sum().reset_index()
            wh_chart = (
                alt.Chart(wh_df)
                .mark_bar(color="#9ca3af")
                .encode(
                    x=alt.X("warehouse:N", title="Warehouse"),
                    y=alt.Y("on_hand:Q", title="On-hand Qty"),
                    tooltip=["warehouse:N", "on_hand:Q"],
                )
                .properties(height=260)
            )
            st.altair_chart(wh_chart, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("##### Inventory Details")
            st.dataframe(inv, use_container_width=True, height=320)
            st.markdown("</div>", unsafe_allow_html=True)

        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("##### Purchase Orders")
            st.dataframe(po, use_container_width=True, height=260)
            st.markdown("</div>", unsafe_allow_html=True)

        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("##### Below Reorder (Risk View)")
            short = detect_shortages(inv)
            if short.empty:
                st.success("No shortages (below reorder point) in this demo run.")
            else:
                st.warning(
                    "Some items are below reorder point – AI can propose replenishment."
                )
                st.dataframe(short, use_container_width=True, height=260)
            st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.caption(
                "AI monitors stock vs reorder point, creates replenishment proposals and routes them through "
                "Planner → SCM Head → Finance approvals. After Finance approval, a PO is auto-created."
            )

            if st.button("🔍 Run AI Shortage Scan & Create Proposals"):
                n = create_replenishment_proposals()
                if n == 0:
                    st.info("No new proposals (either no shortage or already proposed).")
                else:
                    st.success(f"AI created {n} replenishment proposal(s).")

            orders = st.session_state.replenishment_orders
            if not orders:
                st.info("No AI replenishment proposals yet. Click the scan button above.")
            else:
                st.markdown("##### Replenishment Queue")
                st.dataframe(pd.DataFrame(orders), use_container_width=True, height=260)

                st.markdown("##### Approvals (Role-based Demo)")
                eligible = []
                for o in orders:
                    if current_role == "Planner" and o["status"] == "Proposed":
                        eligible.append(o["id"])
                    if current_role == "SCM Head" and o["status"] == "Planner Approved":
                        eligible.append(o["id"])
                    if current_role == "Finance" and o["status"] == "SCM Approved":
                        eligible.append(o["id"])

                if current_role in ["Planner", "SCM Head", "Finance"]:
                    if not eligible:
                        st.info(f"No orders awaiting {current_role} approval.")
                    else:
                        sel = st.selectbox("Select order to approve", eligible)
                        if st.button("✅ Approve Selected Order"):
                            approve_replenishment(sel)
                else:
                    st.info(
                        "Change role in sidebar to Planner / SCM Head / Finance to demo approvals."
                    )
            st.markdown(
                '<div class="muted-label">Client value: this is where \"no more stock-out\" becomes real – AI + workflow + auto-PO.</div>',
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

elif module == "Production":
    st.markdown(
        '<div class="module-banner">🏭 <b>Production View:</b> Compare plan vs actual to know which SKUs are underperforming.</div>',
        unsafe_allow_html=True,
    )
    st.subheader("Production – Plan vs Actual")

    prod = data["production"]
    sku = st.selectbox("Select SKU", SKU_LIST)
    df = prod[prod["sku"] == sku]

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        if df.empty:
            st.info("No production data for this SKU in demo.")
        else:
            st.markdown("##### Plan vs Actual Output")
            prod_long = df[["month", "plan_qty", "actual_qty"]].melt(
                "month", var_name="metric", value_name="qty"
            )
            prod_chart = (
                alt.Chart(prod_long)
                .mark_line(strokeWidth=2)
                .encode(
                    x=alt.X("month:T", title="Month"),
                    y=alt.Y("qty:Q", title="Quantity"),
                    color=alt.Color(
                        "metric:N",
                        title="",
                        scale=alt.Scale(range=["#6b7280", "#f97316"]),  # grey + orange
                    ),
                    tooltip=["month:T", "metric:N", "qty:Q"],
                )
                .properties(height=260)
            )
            st.altair_chart(prod_chart, use_container_width=True)

            total_plan = int(df["plan_qty"].sum())
            total_act = int(df["actual_qty"].sum())
            var = total_act - total_plan
            var_pct = (var / total_plan * 100) if total_plan else 0

            c1, c2, c3 = st.columns(3)
            c1.metric("Total Plan", f"{total_plan:,}")
            c2.metric("Total Actual", f"{total_act:,}")
            c3.metric("Variance", f"{var:,}", f"{var_pct:.1f}%")
        st.markdown(
            '<div class="muted-label">Client value: great for S&OP discussions and capacity planning review.</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

elif module == "Finance & AI Forecasting":
    st.markdown(
        '<div class="module-banner">💹 <b>Finance & Forecast:</b> P&L view plus AI forecast for revenue and EBIT.</div>',
        unsafe_allow_html=True,
    )
    st.subheader("Finance & AI Forecasting")

    fin = data["finance"]

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("##### P&L Table")
        st.dataframe(fin, use_container_width=True, height=260)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("##### Revenue & EBIT Trend (Actual)")
        fin_long = fin[["month", "revenue", "ebit"]].melt(
            "month", var_name="metric", value_name="value"
        )
        fin_chart = (
            alt.Chart(fin_long)
            .mark_line(strokeWidth=2)
            .encode(
                x=alt.X("month:T", title="Month"),
                y=alt.Y("value:Q", title="Amount (₹)"),
                color=alt.Color(
                    "metric:N",
                    title="",
                    scale=alt.Scale(range=["#16a34a", "#f97316"]),  # green + orange
                ),
                tooltip=["month:T", "metric:N", "value:Q"],
            )
            .properties(height=260)
        )
        st.altair_chart(fin_chart, use_container_width=True)

        months = st.slider("Forecast Horizon (months)", 1, 6, 3)
        fc = finance_forecast(fin, months)
        st.markdown("##### AI Finance Forecast")
        st.dataframe(fc, use_container_width=True, height=220)

        combo = pd.concat(
            [
                fin[["month", "revenue", "ebit"]].assign(kind="Actual"),
                fc[["month", "revenue", "ebit"]].assign(kind="Forecast"),
            ]
        ).set_index("month")

        combo_rev = combo.reset_index()[["month", "revenue", "kind"]]
        combo_ebit = combo.reset_index()[["month", "ebit", "kind"]]

        st.markdown("##### Revenue – Actual vs Forecast")
        rev_combo_chart = (
            alt.Chart(combo_rev)
            .mark_line(strokeWidth=2)
            .encode(
                x="month:T",
                y="revenue:Q",
                color=alt.Color(
                    "kind:N",
                    title="",
                    scale=alt.Scale(range=["#374151", "#16a34a"]),  # grey actual, green forecast
                ),
                tooltip=["month:T", "kind:N", "revenue:Q"],
            )
            .properties(height=230)
        )
        st.altair_chart(rev_combo_chart, use_container_width=True)

        st.markdown("##### EBIT – Actual vs Forecast")
        ebit_combo_chart = (
            alt.Chart(combo_ebit)
            .mark_line(strokeWidth=2)
            .encode(
                x="month:T",
                y="ebit:Q",
                color=alt.Color(
                    "kind:N",
                    title="",
                    scale=alt.Scale(range=["#374151", "#16a34a"]),
                ),
                tooltip=["month:T", "kind:N", "ebit:Q"],
            )
            .properties(height=230)
        )
        st.altair_chart(ebit_combo_chart, use_container_width=True)

        st.markdown(
            '<div class="muted-label">Client value: this is a live talking point for CFO reviews – what AI expects next 3–6 months.</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

elif module == "Upload & Explore Data":
    st.markdown(
        '<div class="module-banner">📁 <b>Upload & Explore:</b> Any file upload triggers audit logging and AI-style notifications.</div>',
        unsafe_allow_html=True,
    )
    st.subheader("Upload & Explore Data")
    st.caption(
        "Any upload/download here is logged and can trigger AI alerts + WhatsApp (demo)."
    )

    up = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])
    if up is not None:
        try:
            if up.name.lower().endswith(".csv"):
                df = pd.read_csv(up)
            else:
                df = pd.read_excel(up)

            log_event("UPLOAD", f"{current_user} uploaded {up.name}")
            alert(f"{current_user} uploaded {up.name}")
            whatsapp_demo(f"[File Upload] {current_user} uploaded {up.name}")

            with st.container():
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.success(f"Loaded: {up.name}")
                st.dataframe(df.head(200), use_container_width=True, height=260)

                num_cols = df.select_dtypes(include="number").columns.tolist()
                if num_cols:
                    col = st.selectbox("Numeric column to chart", num_cols)
                    chart_df = df[[col]].reset_index().rename(columns={"index": "row"})
                    num_chart = (
                        alt.Chart(chart_df)
                        .mark_line(strokeWidth=2, color="#6b7280")
                        .encode(
                            x=alt.X("row:Q", title="Row"),
                            y=alt.Y(f"{col}:Q", title=col),
                        )
                        .properties(height=230)
                    )
                    st.altair_chart(num_chart, use_container_width=True)
                else:
                    st.info("No numeric columns to chart.")

                csv = df.to_csv(index=False).encode("utf-8")
                if st.download_button(
                    "Download as CSV", csv, file_name=f"download_{up.name}.csv"
                ):
                    log_event("DOWNLOAD", f"{current_user} downloaded {up.name}")
                    alert(f"{current_user} downloaded {up.name}")
                    whatsapp_demo(f"[File Download] {current_user} downloaded {up.name}")
                st.markdown("</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error reading file: {e}")
    else:
        st.info("Upload a file to view and analyse.")

elif module == "AI Generated Alerts & Activity Log":
    st.markdown(
        '<div class="module-banner">🔔 <b>AI Alerts & Log:</b> View AI-generated summaries plus who did what in the system.</div>',
        unsafe_allow_html=True,
    )
    st.subheader("AI Generated Alerts & Activity Log")

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        if st.button("⚡ Generate AI Alerts Preview"):
            msg = build_daily_alert_message()
            log_event("AI_ALERT_PREVIEW", "User generated AI alert preview")
            alert("AI daily alert generated.")
            whatsapp_demo("[AI Alert] Daily alert preview generated in app.")
            st.text_area("AI Alert Preview (email / WhatsApp body)", msg, height=260)
        else:
            st.markdown(
                '<div class="muted-label">Click the button to show how a daily AI alert summary for management would look.</div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("##### Activity Log")
        if not st.session_state.activity_log:
            st.info("No activity logged yet.")
        else:
            log_df = pd.DataFrame(st.session_state.activity_log)
            log_df = log_df.sort_values("time", ascending=False)
            st.dataframe(log_df, use_container_width=True, height=300)
        st.markdown("</div>", unsafe_allow_html=True)

elif module == "AI Forecast Copilot":
    st.markdown(
        '<div class="module-banner">🤖 <b>Forecast Copilot:</b> Ask questions in plain English, get AI-style answers on this dataset.</div>',
        unsafe_allow_html=True,
    )
    st.subheader("AI Forecast Copilot")
    st.caption(
        "Ask natural language questions about revenue, profit, stock risks and AI replenishment. "
        "This is a demo chatbot running simple rules on top of the same dataset."
    )

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["text"])

    user_msg = st.chat_input("Ask me something...")
    if user_msg:
        st.session_state.chat_history.append({"role": "user", "text": user_msg})
        reply = chatbot_response(user_msg)
        st.session_state.chat_history.append({"role": "assistant", "text": reply})

        with st.chat_message("user"):
            st.write(user_msg)
        with st.chat_message("assistant"):
            st.write(reply)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.write("---")
st.markdown(
    "<div style='font-size:0.85rem;color:#6b7280;text-align:center;'>Powered by <b>ITMC Systems</b> – Empowering Innovation, Delivering Excellence.</div>",
    unsafe_allow_html=True,
)
