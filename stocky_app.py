import streamlit as st

from yahoo.stock_analysis import get_stocks, fetch_periods_intervals, generate_analysis_excel

st.set_page_config(
    page_title="Stocky",
    page_icon="🤟🏼",
)

#####Sidebar Start#####

# Fetch and store config
stocks = get_stocks()
periods = fetch_periods_intervals()

# Add a dropdown for selecting the stock
st.sidebar.markdown("### **Select stock**")
selected_stocks = st.sidebar.multiselect("Choose a stock", stocks)

# Add a selector for period
st.sidebar.markdown("### **Select period**")
period = st.sidebar.selectbox("Choose a period", list(periods.keys()))

if st.sidebar.button("**Generate**"):
    download = generate_analysis_excel(stocks, selected_stocks, period)

if st.sidebar.button("**Download**"):
    

#####Sidebar End#####

#####Title#####

# Add title to the app
st.markdown("# **Excel for Stock Analysis**")

#####Title End#####