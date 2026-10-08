import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Executive Business Dashboard", page_icon="📊", layout="wide")

df = pd.read_csv("dashboard_dataset.csv")
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

st.title("📊 Executive Business Dashboard")
st.caption("Interactive KPI & Business Performance Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
categories = st.sidebar.multiselect("Category", sorted(df["Category"].unique()), default=sorted(df["Category"].unique()))
regions = st.sidebar.multiselect("Region", sorted(df["Region"].unique()), default=sorted(df["Region"].unique()))
date_min, date_max = df["Order_Date"].min().date(), df["Order_Date"].max().date()
date_range = st.sidebar.date_input("Date range", (date_min, date_max), min_value=date_min, max_value=date_max)

filtered = df[
    df["Category"].isin(categories) &
    df["Region"].isin(regions) &
    (df["Order_Date"].dt.date >= date_range[0]) &
    (df["Order_Date"].dt.date <= date_range[1])
].copy()

# KPIs
revenue = filtered["Sales"].sum()
profit = filtered["Profit"].sum()
customers = filtered["Customer_ID"].nunique()
orders = len(filtered)
aov = revenue / orders if orders else 0
profit_margin = (profit/revenue*100) if revenue else 0

c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Revenue", f"₹{revenue:,.0f}")
c2.metric("Profit", f"₹{profit:,.0f}")
c3.metric("Customers", f"{customers:,}")
c4.metric("Average Order Value", f"₹{aov:,.0f}")
c5.metric("Profit Margin", f"{profit_margin:.1f}%")

st.divider()

# Trend
monthly = filtered.groupby("Month", as_index=False)["Sales"].sum()
fig = px.area(monthly, x="Month", y="Sales", title="Monthly Revenue Trend")
fig.update_layout(xaxis_title="", yaxis_title="Revenue")
st.plotly_chart(fig, use_container_width=True)

left,right = st.columns(2)

with left:
    cat_sales = filtered.groupby("Category", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    fig2 = px.bar(cat_sales, x="Category", y="Sales", title="Revenue by Category")
    st.plotly_chart(fig2, use_container_width=True)

with right:
    region_sales = filtered.groupby("Region", as_index=False)["Sales"].sum()
    fig3 = px.bar(region_sales, x="Region", y="Sales", title="Revenue by Region")
    st.plotly_chart(fig3, use_container_width=True)

st.subheader("Profitability")
profit_cat = filtered.groupby("Category", as_index=False).agg(
    Profit=("Profit","sum"),
    Profit_Margin=("Profit_Margin","mean")
)
fig4 = px.bar(profit_cat, x="Category", y="Profit", title="Profit by Category")
st.plotly_chart(fig4, use_container_width=True)

st.subheader("Executive Insights")
if len(filtered):
    best_cat = filtered.groupby("Category")["Sales"].sum().idxmax()
    best_region = filtered.groupby("Region")["Sales"].sum().idxmax()
    st.write(f"• **Top revenue category:** {best_cat}")
    st.write(f"• **Top revenue region:** {best_region}")
    st.write(f"• **Average Order Value:** ₹{aov:,.0f}")
    st.write(f"• **Overall profit margin:** {profit_margin:.1f}%")
    st.write("• Use the sidebar filters to drill down by category, region, and time period.")
else:
    st.warning("No records match the selected filters.")
