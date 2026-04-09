import streamlit as st
import pandas as pd

st.title("Retail Insights Dashboard")

# Upload CSV
uploaded_file = st.file_uploader("Choose CSV", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write(df.head())

    # Example chart
    if 'purchase_frequency' in df.columns:
        st.bar_chart(df['purchase_frequency'].value_counts())
