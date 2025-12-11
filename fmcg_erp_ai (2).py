import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
from pathlib import Path

st.set_page_config(page_title="ITMC FMCG ERP + AI", layout="wide")

# -------------------------------
# LOGO + HEADER
# -------------------------------
logo_path = Path("itmc_logo.png")
if logo_path.exists():
    st.image(str(logo_path), width=90)

st.markdown("## ITMC Systems – FMCG ERP + AI Forecasting Platform")
st.caption("ERP Operations + Sales + SCM + Production + Finance + AI Forecasting + Alerts + Auto-PO + Copilot")

st.write("---")

# -------------------------------
# CONSTANTS
# -------------------------------
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
def init_dummy_data():
    today = dt.date.today()

    # Finance data
    months = pd.date_range(
        start=(today - pd.DateOffset(months=MONTHS_BACK - 1)).replace(day=1),
        periods=MONTHS_BACK,
        freq="MS",
    )

    # Sales
    so_rows = []
    for i in range(1, 101):
        so_rows.append({
            "order_id": f"SO-{1000+i}",
            "order_date": today - dt.timedelta(days=np.random.randint(0, 60)),
            "customer": np.random.choice(CUSTOMERS),
            "region": np.random.choice(REGIONS),
            "channel": np.random.choice(CHANNELS),
            "sku": np.random.choice(SKU_LIST),
            "qty": np.random.randint(50, 500),
            "amount": np.random.randint(50_000, 300_000),
            "status": np.random.choice(["Pending","Allocated","Dispatched"])
        })
    sales_orders = pd.DataFrame(so_rows)

    # Inventory
    inv_rows = []
    for wh in WAREHOUSES:
        for sku in SKU_LIST:
            inv_rows.append({
                "warehouse": wh,
                "sku": sku,
                "on_hand": np.random.randint(2000, 15000),
                "in_transit": np.random.randint(0, 5000),
                "reorder_point": np.random.randint(3000, 7000)
            })
    inventory = pd.DataFrame(inv_rows)

    # Purchase Orders
    po_rows = []
    for i in range(1, 51):
        po_rows.append({
            "po_id": f"PO-{600+i}",
            "po_date": today - dt.timedelta(days=np.random.randint(0, 60)),
            "vendor": np.random.choice(VENDORS),
            "sku": np.random.choice(SKU_LIST),
            "qty": np.random.randint(500, 2000),
            "amount": np.random.randint(100_000, 600_000),
            "status": np.random.choice(["Open","In Transit","Received"])
        })
    purchase_orders = pd.DataFrame(po_rows)

    # Production
    prod_rows = []
    for sku in SKU_LIST:
        for m in months:
            plan = np.random.randint(10000, 30000)
            actual = int(plan * np.random.uniform(0.9, 1.1))
            prod_rows.append({
                "month": m,
                "sku": sku,
                "plan_qty": plan,
                "actual_qty": actual
            })
    production = pd.DataFrame(prod_rows)

    # Finance P&L
    fin_rows = []
    base_rev = 5_000_000
    for m in months:
        revenue = base_rev + np.random.randint(-500_000, 800_000)
        cogs = int(revenue * np.random.uniform(0.6, 0.75))
        opex = int(revenue * np.random.uniform(0.12, 0.18))
        fin_rows.append({
            "month": m,
            "revenue": revenue,
            "cogs": cogs,
            "opex": opex
        })
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
        "months": months
    }
# --------------------------
# SESSION STATE
# --------------------------
if "data" not in st.session_state:
    st.session_state.data = init_dummy_data()

if "activity_log" not in st.session_state:
    st.session_state.activity_log = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

data = st.session_state.data

# --------------------------
# AI FORECAST HELPERS
# --------------------------
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
    next_months = [last_month + pd.DateOffset(months=i) for i in range(1, months+1)]

    rev_fc = simple_forecast(df["revenue"], months)
    cogs_fc = simple_forecast(df["cogs"], months)
    opex_fc = simple_forecast(df["opex"], months)

    rows = []
    for i, m in enumerate(next_months):
        rev = rev_fc[i]
        cogs = cogs_fc[i]
        opex = opex_fc[i]
        rows.append({
            "month": m,
            "revenue": rev,
            "cogs": cogs,
            "opex": opex,
            "gross_profit": rev - cogs,
            "ebit": (rev - cogs) - opex
        })
    return pd.DataFrame(rows)

# --------------------------
# ALERT + WHATSAPP DEMO
# --------------------------
def log_event(action, detail):
    event = {
        "time": dt.datetime.now(),
        "user": st.session_state.get("current_user","unknown"),
        "action": action,
        "detail": detail
    }
    st.session_state.activity_log.append(event)

def alert(msg):
    st.info(f"🔔 {msg}")

def whatsapp_demo(msg):
    st.success(f"📲 WhatsApp (demo): {msg}")

def build_daily_alert_message():
    fin = data["finance"]
    last = fin.iloc[-1]
    fc = finance_forecast(fin, 3)

    msg = []
    msg.append("ITMC – AI Daily Alert Summary")
    msg.append("------------------------------------")
    msg.append(f"Last Month Revenue: ₹ {last['revenue']:,}")
    msg.append(f"Last Month EBIT: ₹ {last['ebit']:,}")
    msg.append("")
    msg.append("Next 3-Month Finance Forecast:")
    for _, row in fc.iterrows():
        month = row["month"].strftime("%b %Y")
        msg.append(f"- {month}: Revenue ~₹ {row['revenue']:,}, EBIT ~₹ {row['ebit']:,}")
    msg.append("")
    return "\n".join(msg)
# --------------------------
# SIDEBAR LOGIN & ROLE
# --------------------------
st.sidebar.markdown("### User Context")
current_user = st.sidebar.text_input("Logged in as (name/email)", "demo@itmc.in")
current_role = st.sidebar.selectbox(
    "Current Role (for approvals)",
    ["Viewer", "Planner", "SCM Head", "Finance", "Admin"],
    index=4
)
st.session_state.current_user = current_user
st.session_state.current_role = current_role

st.sidebar.write("---")

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
        "AI Forecast Copilot"
    ]
)

# --------------------------
# KPI TOP STRIP
# --------------------------
fin = data["finance"]
last_fin = fin.iloc[-1]

inv_value = data["inventory"]["on_hand"].sum() * 50

c1, c2, c3 = st.columns(3)
c1.metric("Last Month Revenue", f"₹ {last_fin['revenue']:,}")
c2.metric("Last Month EBIT", f"₹ {last_fin['ebit']:,}")
c3.metric("Inventory Value (Approx)", f"₹ {inv_value:,}")

st.write("---")
# --------------------------
# REPLENISHMENT HELPERS
# --------------------------
if "replenishment_orders" not in st.session_state:
    st.session_state.replenishment_orders = []
    st.session_state.next_repl_id = 1


def detect_shortages(inv_df: pd.DataFrame) -> pd.DataFrame:
    """Rows where stock is below reorder point."""
    return inv_df[inv_df["on_hand"] < inv_df["reorder_point"]]


def create_replenishment_proposals():
    """
    From shortages, create AI replenishment proposals.
    Simple logic: target = 1.5 * reorder_point; qty = target - on_hand.
    """
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


def auto_create_po(order: dict):
    """Simulate PO when final approval done."""
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
    """Move order along approval chain based on current role."""
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
            alert(f"Role '{role}' cannot approve order #{order_id} from status '{order['status']}'.")
            return

        detail = f"{role} {user} approved order #{order_id} ({prev_status} → {order['status']})"
        log_event("APPROVAL", detail)
        whatsapp_demo(f"[Approval] {detail}")
        return

    alert(f"Order #{order_id} not found.")


# --------------------------
# CHATBOT
# --------------------------
def chatbot_response(text: str) -> str:
    t = text.lower()
    fin = data["finance"]

    if "revenue" in t or "ebit" in t or "p&l" in t or "profit" in t:
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
            "AI creates replenishment proposals when stock < reorder point, then moves them through "
            "Planner → SCM Head → Finance approvals. After Finance approval, a Purchase Order is auto-created."
        )

    return (
        "I'm the Forecast Copilot for this FMCG ERP demo.\n\n"
        "Try asking things like:\n"
        "- \"Revenue forecast next 3 months\"\n"
        "- \"EBIT and profit outlook\"\n"
        "- \"Any stock shortage risk?\"\n"
        "- \"How does AI auto-create POs?\""
    )


# ==================================================
# MODULES
# ==================================================

if module == "ERP Operations Dashboard":
    st.subheader("ERP Operations Dashboard – End-to-End View")

    fin = data["finance"]
    st.markdown("#### Revenue & EBIT (Last 12 Months)")
    st.line_chart(fin.set_index("month")[["revenue", "ebit"]])

    so = data["sales_orders"]
    inv = data["inventory"]

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### Sales Mix by Region")
        st.bar_chart(so.groupby("region")["amount"].sum())
    with c2:
        st.markdown("##### Sales Mix by Channel")
        st.bar_chart(so.groupby("channel")["amount"].sum())

    st.markdown("##### Inventory by Warehouse")
    st.bar_chart(inv.groupby("warehouse")["on_hand"].sum())

elif module == "Sales & Orders":
    st.subheader("Sales & Orders")

    so = data["sales_orders"]

    c1, c2, c3 = st.columns(3)
    with c1:
        rf = st.selectbox("Region", ["All"] + REGIONS)
    with c2:
        cf = st.selectbox("Channel", ["All"] + CHANNELS)
    with c3:
        sf = st.selectbox("Status", ["All", "Pending", "Allocated", "Dispatched"])

    df = so.copy()
    if rf != "All":
        df = df[df["region"] == rf]
    if cf != "All":
        df = df[df["channel"] == cf]
    if sf != "All":
        df = df[df["status"] == sf]

    st.dataframe(df)

    st.markdown("#### Daily Sales (Amount)")
    daily = df.groupby("order_date")["amount"].sum().sort_index()
    if not daily.empty:
        st.line_chart(daily)
    else:
        st.info("No data for selected filters.")

elif module == "Inventory & Supply Chain":
    st.subheader("Inventory & Supply Chain")

    inv = data["inventory"]
    po = data["purchase_orders"]

    tab1, tab2 = st.tabs(["Inventory Overview", "AI Replenishment & Auto-PO"])

    with tab1:
        st.markdown("#### Inventory by Warehouse")
        st.bar_chart(inv.groupby("warehouse")["on_hand"].sum())

        st.markdown("#### Inventory Details")
        st.dataframe(inv)

        st.markdown("#### Purchase Orders")
        st.dataframe(po)

        st.markdown("#### Below Reorder (Risk)")
        short = detect_shortages(inv)
        if short.empty:
            st.success("No shortages (below reorder point) in this demo run.")
        else:
            st.warning("Some items are below reorder point – AI will propose replenishment.")
            st.dataframe(short)

    with tab2:
        st.caption(
            "AI monitors stock vs reorder point, creates replenishment proposals and routes them through "
            "Planner → SCM Head → Finance approvals. After Finance approval, a PO is auto-created."
        )

        if st.button("Run AI Shortage Scan & Create Proposals"):
            n = create_replenishment_proposals()
            if n == 0:
                st.info("No new proposals (either no shortage or already proposed).")
            else:
                st.success(f"AI created {n} replenishment proposal(s).")

        orders = st.session_state.replenishment_orders
        if not orders:
            st.info("No AI replenishment proposals yet. Click the scan button above.")
        else:
            st.markdown("#### Replenishment Queue")
            st.dataframe(pd.DataFrame(orders))

            # approvals
            st.markdown("#### Approvals (Role-based Demo)")
            role = st.session_state.current_role
            eligible = []
            for o in orders:
                if role == "Planner" and o["status"] == "Proposed":
                    eligible.append(o["id"])
                if role == "SCM Head" and o["status"] == "Planner Approved":
                    eligible.append(o["id"])
                if role == "Finance" and o["status"] == "SCM Approved":
                    eligible.append(o["id"])

            if role in ["Planner", "SCM Head", "Finance"]:
                if not eligible:
                    st.info(f"No orders awaiting {role} approval.")
                else:
                    sel = st.selectbox("Select order to approve", eligible)
                    if st.button("Approve Selected Order"):
                        approve_replenishment(sel)
            else:
                st.info("Change role in sidebar to Planner / SCM Head / Finance to demo approvals.")

elif module == "Production":
    st.subheader("Production – Plan vs Actual")

    prod = data["production"]
    sku = st.selectbox("Select SKU", SKU_LIST)
    df = prod[prod["sku"] == sku]

    if df.empty:
        st.info("No production data for this SKU in demo.")
    else:
        st.line_chart(df.set_index("month")[["plan_qty", "actual_qty"]])

        total_plan = int(df["plan_qty"].sum())
        total_act = int(df["actual_qty"].sum())
        var = total_act - total_plan
        var_pct = (var / total_plan * 100) if total_plan else 0

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Plan", f"{total_plan:,}")
        c2.metric("Total Actual", f"{total_act:,}")
        c3.metric("Variance", f"{var:,}", f"{var_pct:.1f}%")

elif module == "Finance & AI Forecasting":
    st.subheader("Finance & AI Forecasting")

    fin = data["finance"]
    st.markdown("#### P&L Table")
    st.dataframe(fin)

    st.markdown("#### Revenue & EBIT Trend")
    st.line_chart(fin.set_index("month")[["revenue", "ebit"]])

    months = st.slider("Forecast Horizon (months)", 1, 6, 3)
    fc = finance_forecast(fin, months)
    st.markdown("#### AI Finance Forecast")
    st.dataframe(fc)

    combo = pd.concat(
        [
            fin[["month", "revenue", "ebit"]].assign(kind="Actual"),
            fc[["month", "revenue", "ebit"]].assign(kind="Forecast"),
        ]
    ).set_index("month")

    st.markdown("#### Revenue – Actual vs Forecast")
    st.line_chart(combo[["revenue"]])

    st.markdown("#### EBIT – Actual vs Forecast")
    st.line_chart(combo[["ebit"]])

elif module == "Upload & Explore Data":
    st.subheader("Upload & Explore Data")

    st.caption("Any upload/download here is logged and can trigger AI alerts + WhatsApp (demo).")

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

            st.success(f"Loaded: {up.name}")
            st.dataframe(df.head(200))

            num_cols = df.select_dtypes(include="number").columns.tolist()
            if num_cols:
                col = st.selectbox("Numeric column to chart", num_cols)
                st.line_chart(df[col])
            else:
                st.info("No numeric columns to chart.")

            csv = df.to_csv(index=False).encode("utf-8")
            if st.download_button("Download as CSV", csv, file_name=f"download_{up.name}.csv"):
                log_event("DOWNLOAD", f"{current_user} downloaded {up.name}")
                alert(f"{current_user} downloaded {up.name}")
                whatsapp_demo(f"[File Download] {current_user} downloaded {up.name}")

        except Exception as e:
            st.error(f"Error reading file: {e}")
    else:
        st.info("Upload a file to view and analyse.")

elif module == "AI Generated Alerts & Activity Log":
    st.subheader("AI Generated Alerts & Activity Log")

    st.caption("Generate AI daily alerts and see audit log of all important actions in this session.")

    if st.button("Generate AI Alerts Preview"):
        msg = build_daily_alert_message()
        log_event("AI_ALERT_PREVIEW", "User generated AI alert preview")
        alert("AI daily alert generated.")
        whatsapp_demo("[AI Alert] Daily alert preview generated in app.")
        st.text_area("AI Alert Preview (email / WhatsApp body)", msg, height=260)

    st.markdown("#### Activity Log")
    if not st.session_state.activity_log:
        st.info("No activity logged yet.")
    else:
        log_df = pd.DataFrame(st.session_state.activity_log)
        log_df = log_df.sort_values("time", ascending=False)
        st.dataframe(log_df)

elif module == "AI Forecast Copilot":
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

# --------------------------
# FOOTER
# --------------------------
st.write("---")
st.markdown("**Powered by ITMC Systems – Empowering Innovation, Delivering Excellence.**")
