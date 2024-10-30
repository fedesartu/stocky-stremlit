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

# Generate the file and automatically provide the download link
if st.sidebar.button("**Generate**"):
    file_path = generate_analysis_excel(stocks, selected_stocks, period)
    
    if file_path:  # Check if the file path is not empty
        with open(file_path, 'rb') as file:
            st.sidebar.download_button(
                label="Download File",
                data=file,
                file_name="analysis.xlsx",  # Use the name of the file
                mime='application/octet-stream'  # Change this depending on the file type
            )
    else:
        st.error("No file generated.")

#####Sidebar End#####

#####Title#####

# Add title to the app
st.markdown("# **Excel for Stock Analysis**")

#####Title End#####
