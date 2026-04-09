# streamlit_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Retail Insights Pro", layout="wide")
st.title("📊 Retail Insights Pro Dashboard")

# Sidebar Filters
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
    
    # Metrics
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

    # Top-Selling Products
    if 'product' in df.columns and 'purchase_frequency' in df.columns:
        st.markdown("**Top-Selling Products**")
        top_products = df.groupby('product')['purchase_frequency'].sum().sort_values(ascending=False).head(10)
        st.bar_chart(top_products)
    
    # Revenue by Category Pie Chart
    if 'revenue' in df.columns and 'category' in df.columns:
        st.markdown("**Revenue by Category**")
        revenue_cat = df.groupby('category')['revenue'].sum()
        fig1, ax1 = plt.subplots()
        ax1.pie(revenue_cat, labels=revenue_cat.index, autopct='%1.1f%%', startangle=140)
        ax1.axis('equal')
        st.pyplot(fig1)
    
    # Revenue Heatmap over time
    if 'date' in df.columns and 'revenue' in df.columns:
        st.markdown("**Revenue Heatmap (Month vs Day)**")
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        heatmap_data = df.pivot_table(values='revenue', index='month', columns='day', aggfunc='sum', fill_value=0)
        fig2, ax2 = plt.subplots(figsize=(12,4))
        sns.heatmap(heatmap_data, cmap="YlGnBu", ax=ax2)
        st.pyplot(fig2)

    st.success("✅ Pro Dashboard ready! Explore your data using the sidebar filters.")
else:
    st.info("Please upload a CSV file from the sidebar to get started.")
