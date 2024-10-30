import streamlit as st
from yahoo.stock_analysis import get_stocks, fetch_periods_intervals, generate_analysis_excel

st.set_page_config(
    page_title="Stocky",
    page_icon="🤟🏼",
)

# Fetch and store config
stocks = get_stocks()
periods = fetch_periods_intervals()

#####Title#####

# Add title to the app
st.markdown("# 📈 **Excel for Stock Analysis** 📈 ")

st.markdown("### **Select stock**")
selected_stocks = st.multiselect("Choose a stock", stocks)

# Add a selector for period
st.markdown("### **Select period**")
period = st.selectbox("Choose a period", periods)

email = st.text_input("Email", "")

key = st.text_input("Validate Key", "")

# Generate the file and automatically provide the download link
if st.button("**Generate**"):
    if email != "" and key != "":
        generate_analysis_excel(stocks, selected_stocks, period, email, key)
    else:
        st.error('Email and key cannot be empty!', icon="🚨")

#####Title End#####
