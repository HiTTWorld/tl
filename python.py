import pandas as pd
import streamlit as st
import altair as alt

# Load data
file_path = 'Moive_Boxoffice.csv'
data = pd.read_csv(file_path)

# Mapping of movie names to be used in the multiselect
movie_names = ['범죄도시', '범죄도시2', '범죄도시3']

# Set the title of the main page
st.title("Movie Project")

# Add items to the sidebar
with st.sidebar:
    st.header("Getting started")
    st.write('Demo: Survey')
    st.write('Demo: User management')

# Create a multiselect dropdown with specific movie names
selected_movies = st.sidebar.multiselect(
    'Select Movie Names',
    options=movie_names,
    default=movie_names
)

filtered_data = data[data['movieNm'].isin(selected_movies)]

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

# Define CSS for reducing font size
st.markdown(
    """
    <style>
    .metric-container .metric-value {
        font-size: 1.5em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Sales Amount", value=format_number(kpi_summary[kpi_summary['Metric'] == 'salesAmt']['Value'].values[0]))
with col2:
    st.metric(label="Total Audience Count", value=format_number(kpi_summary[kpi_summary['Metric'] == 'audiCnt']['Value'].values[0]))
with col3:
    st.metric(label="Total Screen Count", value=format_number(kpi_summary[kpi_summary['Metric'] == 'scrnCnt']['Value'].values[0]))
with col4:
    st.metric(label="Total Show Count", value=format_number(kpi_summary[kpi_summary['Metric'] == 'showCnt']['Value'].values[0]))

# Convert targetDt to datetime
filtered_data['targetDt'] = pd.to_datetime(filtered_data['targetDt'], format='%Y%m%d')

# Plotting the line chart using Altair
line_chart = alt.Chart(filtered_data).mark_line(point=True).encode(
    x='targetDt:T',
    y='audiCnt:Q',
    color='movieNm:N',
    tooltip=['targetDt:T', 'audiCnt:Q', 'movieNm:N']
).properties(
    title='Audience Count Over Time'
).interactive()

st.altair_chart(line_chart, use_container_width=True)
