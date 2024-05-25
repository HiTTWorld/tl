import pandas as pd
import streamlit as st
# pip install openpyxl

# Set the title of the main page
st.title("Movie Project")

# Add items to the sidebar
with st.sidebar:
    st.header("Getting started")
    st.write("Demo: Survey")
    st.write("Demo: User management")
   
data = pd.read_csv('Moive_Boxoffice.csv')  

kpi_data = data[['salesAmt', 'audiCnt', 'scrnCnt', 'showCnt']]

# Summarize the data to create meaningful KPIs
kpi_summary = kpi_data.sum().reset_index()
kpi_summary.columns = ['Metric', 'Value']

# Function to format large numbers with commas
def format_number(number):
    return f"{number:,}"

# Streamlit App
st.title("KPI Dashboard")

# Display KPI metrics in card format
st.subheader("KPI Summary")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Sales Amount", value=format_number(kpi_summary[kpi_summary['Metric'] == 'salesAmt']['Value'].values[0]))
with col2:
    st.metric(label="Total Audience Count", value=format_number(kpi_summary[kpi_summary['Metric'] == 'audiCnt']['Value'].values[0]))
with col3:
    st.metric(label="Total Screen Count", value=format_number(kpi_summary[kpi_summary['Metric'] == 'scrnCnt']['Value'].values[0]))
with col4:
    st.metric(label="Total Show Count", value=format_number(kpi_summary[kpi_summary['Metric'] == 'showCnt']['Value'].values[0]))

# You can add more styling or features as needed
