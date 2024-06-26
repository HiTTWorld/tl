import pandas as pd
import streamlit as st
import altair as alt
from datetime import timedelta

# Load data
file_path = 'movie.csv'
data = pd.read_csv(file_path)

# Ensure all date columns are parsed correctly
data['openDt'] = pd.to_datetime(data['openDt'], errors='coerce', format='%Y-%m-%d %H:%M:%S')
data['targetDt'] = pd.to_datetime(data['targetDt'], errors='coerce', format='%Y%m%d')

# Extract year from openDt for coloring
data['year'] = data['openDt'].dt.year

# Aggregate the data to sum showCnt, scrnCnt, and audiCnt for each movie
aggregated_data = data.groupby(['movieNm', 'year'], as_index=False).agg({
    'showCnt': 'sum',
    'scrnCnt': 'sum',
    'audiCnt': 'sum',
    'openDt': 'first'  # Keep the first openDt for reference
})

# Mapping of movie names to be used in the multiselect
movie_names = ['범죄도시', '범죄도시2', '범죄도시3']

# Sidebar navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Main Dashboard", "Demo: Survey", "Demo: User management", "Scatter Plot"])

if page == "Main Dashboard":
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

    # Filter data to get the selected movies
    selected_data = data[data['movieNm'].isin(selected_movies)]

    # Get the release dates of the selected movies
    selected_open_dates = selected_data.drop_duplicates(subset=['movieNm'])[['movieNm', 'openDt']]
    selected_open_dates['openDt'] = pd.to_datetime(selected_open_dates['openDt'], format='%Y-%m-%d %H:%M:%S')

    # Identify the date range for competing movies (2 weeks before and after release date)
    competing_date_ranges = selected_open_dates.apply(lambda row: pd.date_range(start=row['openDt'] - timedelta(days=14), end=row['openDt'] + timedelta(days=14)), axis=1)

    # Filter data to get competing movies
    data['openDt'] = pd.to_datetime(data['openDt'], format='%Y-%m-%d %H:%M:%S')
    is_competing_movie = data.apply(lambda row: any(row['openDt'] in date_range for date_range in competing_date_ranges), axis=1)
    competing_data = data[is_competing_movie]

    # Merge selected movies and competing movies
    plot_data = pd.concat([selected_data, competing_data]).drop_duplicates()

    # Convert targetDt to datetime
    plot_data['targetDt'] = pd.to_datetime(plot_data['targetDt'], format='%Y%m%d')

    # Extract relevant columns for KPI chart
    kpi_data = selected_data[['salesAmt', 'audiCnt', 'scrnCnt', 'showCnt']]

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

    # Plotting the line chart using Altair
    line_chart = alt.Chart(plot_data).mark_line(point=True).encode(
        x='targetDt:T',
        y='audiCnt:Q',
        color='movieNm:N',
        tooltip=['targetDt:T', 'audiCnt:Q', 'movieNm:N']
    ).properties(
        title='Audience Count Over Time'
    ).interactive()

    st.altair_chart(line_chart, use_container_width=True)

elif page == "Demo: Survey":
    st.title("Survey Data")
    st.subheader("Preview of Survey Data")
    st.write(data.head(10))  # Display first 10 rows of the data

elif page == "Demo: User management":
    st.title("User Management Data")
    st.subheader("Preview of User Management Data")
    st.write(data.head(10))  # Display first 10 rows of the data

elif page == "Scatter Plot":
    st.title("Scatter Plot of Show Count vs Screen Count")
    
    # Create the scatter plot
    scatter_chart = alt.Chart(aggregated_data).mark_circle(size=60).encode(
        x=alt.X('scrnCnt:Q', title='Screen Count'),
        y=alt.Y('showCnt:Q', title='Show Count'),
        color=alt.Color('year:N', title='Year'),
        tooltip=['movieNm:N', 'scrnCnt:Q', 'showCnt:Q', 'openDt:T']
    ).properties(
        width=800,
        height=600,
        title='Show Count vs Screen Count with Year Coloring'
    ).interactive()

    st.altair_chart(scatter_chart, use_container_width=True)
    
    # Create the box plot
    box_plot = alt.Chart(aggregated_data).mark_boxplot(extent='min-max').encode(
        x=alt.X('year:O', title='Year'),
        y=alt.Y('audiCnt:Q', title='Audience Count'),
        color=alt.Color('year:N', title='Year'),
        tooltip=['movieNm:N', 'audiCnt:Q', 'year:O']
    ).properties(
        width=800,
        height=600,
        title='Audience Count by Year'
    ).interactive()

    st.altair_chart(box_plot, use_container_width=True)
    
    # Prepare data for dumbbell plot
    dumbbell_data = data.groupby(['movieNm']).agg(
        start_date=pd.NamedAgg(column='openDt', aggfunc='min'),
        end_date=pd.NamedAgg(column='openDt', aggfunc='max'),
        duration=pd.NamedAgg(column='openDt', aggfunc=lambda x: (x.max() - x.min()).days)
    ).reset_index()

    dumbbell_chart = alt.Chart(dumbbell_data).mark_line().encode(
        x=alt.X('duration:Q', title='Duration (Days)'),
        y=alt.Y('movieNm:N', title='Movie Name'),
        color=alt.Color('movieNm:N', legend=None)
    ).properties(
        width=800,
        height=600,
        title='Movie Screening Durations'
    ).interactive()

    points_start = alt.Chart(dumbbell_data).mark_circle(size=100).encode(
        x=alt.X('start_date:T', title='Start Date'),
        y=alt.Y('movieNm:N', title='Movie Name'),
        tooltip=['movieNm:N', 'start_date:T', 'end_date:T', 'duration:Q'],
        color=alt.value('blue')
    )

    points_end = alt.Chart(dumbbell_data).mark_circle(size=100).encode(
        x=alt.X('end_date:T', title='End Date'),
        y=alt.Y('movieNm:N', title='Movie Name'),
        tooltip=['movieNm:N', 'start_date:T', 'end_date:T', 'duration:Q'],
        color=alt.value('red')
    )

    st.altair_chart(dumbbell_chart + points_start + points_end, use_container_width=True)
