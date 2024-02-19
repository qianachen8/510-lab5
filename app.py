import streamlit as st
import pandas as pd
import pandas.io.sql as sqlio
import altair as alt
import folium
from streamlit_folium import st_folium

from db import conn_str

st.title("Seattle Events")

df = sqlio.read_sql_query("SELECT * FROM events", conn_str)

#Feature1: Data Visualization
#1 What type of events is most common in Seattle?(Bar chart)
st.subheader("What type of events is most common in Seattle?")

st.altair_chart(
    alt.Chart(df).mark_bar().encode(x="count()", y=alt.Y("category").sort('-x')).interactive(),
    use_container_width=True,
)


#2 In which locations are events most frequently held?
st.subheader("Where are events most frequently held?")

chart1 = alt.Chart(df).mark_bar().encode(
    x=alt.X('count()', title='Number of Events'),
    y=alt.Y('location', sort='-x', title='Location')
).properties(
    width=700,
    height=400
)
st.altair_chart(chart1, use_container_width=True)



#3. What month has the most number of events in 2024?
df['month'] = df['date'].dt.month
chart2 = alt.Chart(df).mark_bar().encode(
    x=alt.X('month', title='Month'),
    y=alt.Y('count()', title='Number of Events')
).properties(
    width=700,
    height=400
)
st.altair_chart(chart2, use_container_width=True)


# Feature 2: Data control and filtering
filtered_df = df.copy()

# Dropdown to filter by category
categories = df['category'].unique()
selected_category = st.selectbox("Select a category", options=categories)
filtered_df = filtered_df[filtered_df['category'] == selected_category]

# Date range selector for event date
min_date = df['date'].min().date()
max_date = df['date'].max().date()
selected_date_range = st.date_input("Select date range", value=[min_date, max_date], min_value=min_date, max_value=max_date)

# Apply date range filter
filtered_df = filtered_df[(filtered_df['date'].dt.date >= selected_date_range[0]) & (filtered_df['date'].dt.date <= selected_date_range[1])]

# Dropdown to filter by location
locations = ['All'] + list(df['location'].unique())
selected_location = st.selectbox("Select a location", options=locations)

if selected_location != 'All':
    filtered_df = filtered_df[filtered_df['location'] == selected_location]
    
# Display the filtered dataframe
st.write(filtered_df)

m = folium.Map(location=[47.6062, -122.3321], zoom_start=12)
folium.Marker([47.6062, -122.3321], popup='Seattle').add_to(m)
st_folium(m, width=1200, height=600)
