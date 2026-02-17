import streamlit as st
import pandas as pd
import plotly.express as px

# Page settings
st.set_page_config(page_title="Afficionado Coffee Dashboard", layout="wide")

st.title("☕ Afficionado Coffee Roasters")
st.subheader("Revenue Analysis Dashboard")

# Load Excel File
df = pd.read_excel("final_data.xlsx")   # <-- change if your file name is different

# Create Revenue Column
df["Revenue"] = df["transaction_qty"] * df["unit_price"]

# =====================
# KPI Section
# =====================
st.markdown("### Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"₹ {df['Revenue'].sum():,.0f}")
col2.metric("Total Transactions", df["transaction_id"].nunique())
col3.metric("Total Products", df["product_detail"].nunique())

st.markdown("---")

# =====================
# Category Filter
# =====================
category = st.selectbox(
    "Select Product Category",
    df["product_category"].unique()
)

filtered_df = df[df["product_category"] == category]

# =====================
# Top 10 Products
# =====================
st.subheader("Top 10 Products by Revenue")

top_products = (
    filtered_df.groupby("product_detail")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig1 = px.bar(
    top_products,
    x="product_detail",
    y="Revenue",
    title="Top 10 Products"
)

st.plotly_chart(fig1, use_container_width=True)

# =====================
# Category Revenue Share
# =====================
st.subheader("Category Revenue Share")

category_revenue = (
    df.groupby("product_category")["Revenue"]
    .sum()
    .reset_index()
)

fig2 = px.pie(
    category_revenue,
    names="product_category",
    values="Revenue",
    hole=0.5
)

st.plotly_chart(fig2, use_container_width=True)
