# streamlit_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Retail Insights Dashboard", layout="wide")
st.title("📊 Retail Insights Dashboard")

# 1️⃣ File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("Preview of Dataset")
    st.dataframe(df.head())

    st.markdown("---")
    st.subheader("Dataset Summary")
    st.write(df.describe(include='all'))

    # 2️⃣ Filters
    st.subheader("Filters")
    if 'category' in df.columns:
        categories = df['category'].unique()
        selected_category = st.multiselect("Select Category", options=categories, default=categories)
        df = df[df['category'].isin(selected_category)]

    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        min_date, max_date = st.date_input("Select Date Range", [df['date'].min(), df['date'].max()])
        df = df[(df['date'] >= pd.to_datetime(min_date)) & (df['date'] <= pd.to_datetime(max_date))]

    st.markdown("---")
    st.subheader("Key Metrics")
    col1, col2, col3 = st.columns(3)
    if 'revenue' in df.columns:
        col1.metric("Total Revenue", f"${df['revenue'].sum():,.2f}")
    if 'purchase_frequency' in df.columns:
        col2.metric("Total Purchases", df['purchase_frequency'].sum())
    if 'customers' in df.columns:
        col3.metric("Unique Customers", df['customers'].nunique())

    st.markdown("---")
    st.subheader("Charts & Analytics")

    # 3️⃣ Example Charts
    if 'purchase_frequency' in df.columns:
        st.markdown("**Purchase Frequency Distribution**")
        fig, ax = plt.subplots()
        sns.countplot(x='purchase_frequency', data=df, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    if 'revenue' in df.columns and 'category' in df.columns:
        st.markdown("**Revenue by Category**")
        revenue_by_cat = df.groupby('category')['revenue'].sum().sort_values(ascending=False)
        st.bar_chart(revenue_by_cat)

    if 'revenue' in df.columns and 'date' in df.columns:
        st.markdown("**Revenue Over Time**")
        revenue_over_time = df.groupby('date')['revenue'].sum()
        st.line_chart(revenue_over_time)

    st.success("✅ Dashboard ready! Use filters above to explore your data.")
else:
    st.info("Please upload a CSV file to get started.")
