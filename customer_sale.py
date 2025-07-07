import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_page_config(layout="wide")
st.title("📊 Customer Sales Dashboard")

# Load dataset
data = pd.read_csv("customer_sales.csv")

# Preprocessing
data['Purchase Date'] = pd.to_datetime(data['Purchase Date'], errors='coerce')
data.drop_duplicates(inplace=True)

# KPI Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Sales", f"${data['Sale'].sum():,.2f}")
with col2:
    st.metric("Total Quantity", int(data['Quantity'].sum()))
with col3:
    st.metric("Unique Customers", data['Customer Name'].nunique())

st.markdown("---")

# Total Sales per Month
st.subheader("📅 Total Sales per Month")
monthly_sales = data.groupby('Purchase Month')['Sale'].sum()

fig1, ax1 = plt.subplots()
monthly_sales.plot(kind='bar', color='skyblue', ax=ax1)
ax1.set_title("Monthly Sales")
ax1.set_xlabel("Month")
ax1.set_ylabel("Sales")
st.pyplot(fig1)

# Sales by Product Category
st.subheader("📦 Sales by Product Category")
product_sales = data.groupby('Product Category')['Sale'].sum().sort_values(ascending=False)
st.bar_chart(product_sales)

# Customer Segmentation
st.subheader("👥 Top Customers by Total Spending")
customer_spending = data.groupby('Customer Name')['Sale'].sum().sort_values(ascending=False).head(10)
st.bar_chart(customer_spending)

# Customer Lifetime Value (CLV) Calculation
st.subheader("💰 Top Customers by CLV (Customer Lifetime Value)")
customer_frequency = data.groupby('Customer Name').size()
customer_avg_sale = data.groupby('Customer Name')['Sale'].mean()
lifespan = data.groupby('Customer Name')['Purchase Date'].agg(['min', 'max'])
lifespan['days'] = (lifespan['max'] - lifespan['min']).dt.days.replace(0, 1)
clv = (customer_frequency * customer_avg_sale * lifespan['days']).sort_values(ascending=False).head(10)
st.bar_chart(clv)

st.markdown("---")
st.caption("Built with 💡 Streamlit | Data Analyst Portfolio Demo")
