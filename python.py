import pandas as pd
import streamlit as st

# Load data
file_path = 'Moive_Boxoffice.csv'
data = pd.read_csv(file_path)

# Set the title of the main page
st.title("Movie Project")

# Add items to the sidebar
with st.sidebar:
    st.header("Getting started")
    st.write('Demo: Survey')
    st.write('Demo: User management')

# Ensure the default movie codes are present in the data
default_movie_codes = ['20226411', '20204548', '20172742']
available_movie_codes = data['movieCd'].unique()

# Only use default movie codes that are present in the available options
valid_default_movie_codes = [code for code in default_movie_codes if code in available_movie_codes]

# Filter data based on MovieCd
selected_movies = st.sidebar.multiselect(
    'Select Movie Codes',
    options=available_movie_codes,
    default=valid_default_movie_codes
)

filtered_data = data[data['movieCd'].isin(selected_movies)]

# Extract relevant columns for KPI chart
kpi_data = filtered_data[['salesAmt', 'audiCnt', 'scrnCnt', 'showCnt']]

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
