import pandas as pd
import numpy as np
import datetime as dt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ------------ CONFIG ------------
MONTHS_BACK = 12
ALERT_EMAIL_TO = ["youremail@yourcompany.com"]  # change this
ALERT_EMAIL_FROM = "no-reply@itmc-demo.com"     # change this if using real SMTP
ALERT_EMAIL_SUBJECT = "ITMC FMCG – Daily ERP & Forecast Alerts (Demo)"

# ------------ DUMMY DATA GENERATORS (similar to app) ------------

def generate_finance_data():
    today = dt.date.today()
    months = pd.date_range(
        start=(today - pd.DateOffset(months=MONTHS_BACK - 1)).replace(day=1),
        periods=MONTHS_BACK,
        freq="MS",
    )
    rows = []
    base_revenue = 5_000_000
    for m in months:
        revenue = base_revenue + np.random.randint(-500_000, 800_000)
        cogs = int(revenue * np.random.uniform(0.6, 0.75))
        opex = int(revenue * np.random.uniform(0.12, 0.18))
        rows.append(
            {"month": m, "revenue": revenue, "cogs": cogs, "opex": opex}
        )
        base_revenue *= np.random.uniform(0.97, 1.05)
    df = pd.DataFrame(rows)
    df["gross_profit"] = df["revenue"] - df["cogs"]
    df["ebit"] = df["gross_profit"] - df["opex"]
    return df

def generate_inventory_data():
    SKU_LIST = [
        "Premium Spice Mix 200g",
        "Breakfast Cereal Choco 500g",
        "Instant Creamer 1kg",
        "Masala Blend 100g",
        "Healthy Oats 1kg",
    ]
    WAREHOUSES = ["WH–North", "WH–South", "WH–East", "WH–West"]
    rows = []
    for wh in WAREHOUSES:
        for sku in SKU_LIST:
            rows.append(
                {
                    "warehouse": wh,
                    "sku": sku,
                    "on_hand": np.random.randint(2000, 15000),
                    "reorder_point": np.random.randint(3000, 7000),
                }
            )
    return pd.DataFrame(rows)

def finance_forecast(finance_df, months_forward=3):
    last_month = finance_df["month"].max()
    future_months = [last_month + pd.DateOffset(months=i) for i in range(1, months_forward+1)]

    def simple_fc(series, growth):
        base = series.tail(3).mean()
        vals = []
        val = base
        for _ in range(months_forward):
            val *= growth * np.random.uniform(0.97, 1.05)
            vals.append(int(val))
        return vals

    rev_fc = simple_fc(finance_df["revenue"], 1.04)
    cogs_fc = simple_fc(finance_df["cogs"], 1.03)
    opex_fc = simple_fc(finance_df["opex"], 1.02)

    rows = []
    for i, m in enumerate(future_months):
        rows.append(
            {
                "month": m,
                "revenue": rev_fc[i],
                "cogs": cogs_fc[i],
                "opex": opex_fc[i],
            }
        )
    df = pd.DataFrame(rows)
    df["gross_profit"] = df["revenue"] - df["cogs"]
    df["ebit"] = df["gross_profit"] - df["opex"]
    return df

# ------------ ALERT LOGIC ------------

def build_alert_message():
    finance = generate_finance_data()
    inventory = generate_inventory_data()
    finance_fc = finance_forecast(finance, months_forward=3)

    last = finance.iloc[-1]
    low_stock = inventory[inventory["on_hand"] < inventory["reorder_point"]]

    lines = []
    lines.append("ITMC FMCG – Daily ERP & Forecast Alerts (DEMO)")
    lines.append("=================================================\n")

    # P&L summary
    lines.append("1. P&L – Last Month Snapshot")
    lines.append(f"- Revenue: ₹ {last['revenue']:,}")
    lines.append(f"- EBIT   : ₹ {last['ebit']:,}\n")

    # Finance forecast
    lines.append("2. Finance Forecast – Next 3 Months (Demo AI)")
    for _, row in finance_fc.iterrows():
        month_str = row["month"].strftime("%b %Y")
        lines.append(
            f"- {month_str}: Revenue ~₹ {row['revenue']:,}, EBIT ~₹ {row['ebit']:,}"
        )
    lines.append("")

    # Stock alerts
    lines.append("3. Stock Alerts – SKUs Below Reorder Point")
    if low_stock.empty:
        lines.append("- No SKUs below reorder point in this demo run.\n")
    else:
        for _, r in low_stock.iterrows():
            lines.append(
                f"- {r['warehouse']} – {r['sku']}: On-hand {r['on_hand']}, ROP {r['reorder_point']}"
            )
        lines.append("")

    return "\n".join(lines)

# ------------ EMAIL SENDER (OPTIONAL) ------------

def send_email_alert(body_text: str):
    """
    Simple email sender – your IT team must configure real SMTP here.
    For demo, this function is not called by default.
    """
    msg = MIMEMultipart()
    msg["From"] = ALERT_EMAIL_FROM
    msg["To"] = ", ".join(ALERT_EMAIL_TO)
    msg["Subject"] = ALERT_EMAIL_SUBJECT

    msg.attach(MIMEText(body_text, "plain"))

    # EXAMPLE ONLY – replace with your SMTP details
    smtp_server = "smtp.yourserver.com"
    smtp_port = 587
    smtp_user = "your_username"
    smtp_pass = "your_password"

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)

# ------------ MAIN ------------

if __name__ == "__main__":
    alert_text = build_alert_message()

    # For now, just print – so you see it works
    print(alert_text)

    # When IT configures SMTP, uncomment this to email:
    # send_email_alert(alert_text)
