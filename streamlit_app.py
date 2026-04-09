# streamlit_app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Retail Insights Dashboard", layout="wide")
st.title("📊 Retail Insights Dashboard")

# ---------------------------
# Sidebar Filters
# ---------------------------
st.sidebar.header("Filters")
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Convert date column to datetime if exists
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Category filter
    if 'category' in df.columns:
        categories = df['category'].unique()
        selected_category = st.sidebar.multiselect("Select Categories", options=categories, default=categories)
        df = df[df['category'].isin(selected_category)]

    # Date filter
    if 'date' in df.columns:
        min_date, max_date = st.sidebar.date_input(
            "Select Date Range", [df['date'].min(), df['date'].max()]
        )
        df = df[(df['date'] >= pd.to_datetime(min_date)) & (df['date'] <= pd.to_datetime(max_date))]

    # ---------------------------
    # Metrics
    # ---------------------------
    st.subheader("Key Metrics")
    col1, col2, col3 = st.columns(3)
    if 'revenue' in df.columns:
        col1.metric("💰 Total Revenue", f"${df['revenue'].sum():,.2f}")
    if 'purchase_frequency' in df.columns:
        col2.metric("🛒 Total Purchases", df['purchase_frequency'].sum())
    if 'customers' in df.columns:
        col3.metric("👥 Unique Customers", df['customers'].nunique())

    st.markdown("---")
    st.subheader("Charts & Analytics")

    # ---------------------------
    # Purchase Frequency Chart
    # ---------------------------
    if 'purchase_frequency' in df.columns:
        st.markdown("**Purchase Frequency Distribution**")
        st.bar_chart(df['purchase_frequency'].value_counts())

    # ---------------------------
    # Revenue by Category Chart
    # ---------------------------
    if 'revenue' in df.columns and 'category' in df.columns:
        st.markdown("**Revenue by Category**")
        revenue_by_cat = df.groupby('category')['revenue'].sum()
        st.bar_chart(revenue_by_cat)

    # ---------------------------
    # Revenue Over Time Chart
    # ---------------------------
    if 'revenue' in df.columns and 'date' in df.columns:
        st.markdown("**Revenue Over Time**")
        revenue_over_time = df.groupby('date')['revenue'].sum()
        st.line_chart(revenue_over_time)

    st.success("✅ Dashboard ready! Use the sidebar filters to explore your data.")

else:
    st.info("Please upload a CSV file from the sidebar to get started.")
