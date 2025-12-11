import streamlit as st
import pandas as pd

st.set_page_config(page_title="ITMC – Upload & View Data", layout="wide")

st.markdown("## ITMC – Upload & Explore FMCG Data")
st.caption("Upload your own Excel/CSV files – sales, inventory, finance, etc. – and view them instantly.")

# 1) File uploader
uploaded_file = st.file_uploader(
    "Choose a file (.csv or .xlsx)",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    # 2) Read file
    try:
        if uploaded_file.name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success(f"File loaded: {uploaded_file.name}")

        # 3) Show basic info
        st.markdown("### Preview of Data (first 200 rows)")
        st.dataframe(df.head(200))

        st.markdown("### Quick Summary")
        st.write(df.describe(include="all"))

        # 4) Optional simple charts
        st.markdown("### Quick Chart (pick a numeric column)")
        numeric_cols = df.select_dtypes(include="number").columns.tolist()

        if len(numeric_cols) == 0:
            st.warning("No numeric columns found for charting.")
        else:
            col_to_plot = st.selectbox("Select column for chart", numeric_cols)
            st.line_chart(df[col_to_plot])

    except Exception as e:
        st.error(f"Could not read file: {e}")

else:
    st.info("Upload a CSV or Excel file to see the data here.")
