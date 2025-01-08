import streamlit as st
import pandas as pd
import pydeck as pdk
import random

# Dictionary of approximate coordinates for Michigan cities
mi_city_coords = {
    'Marquette': (46.5436, -87.3954),
    'Escanaba': (45.7453, -87.0646),
    'Sault Ste. Marie': (46.4953, -84.3453),
    'Houghton': (47.1215, -88.5694),
    'Iron Mountain': (45.8202, -88.0657),
    'Detroit': (42.3314, -83.0458),
    'Grand Rapids': (42.9634, -85.6681),
    'Lansing': (42.7325, -84.5555),
    'Ann Arbor': (42.2808, -83.7430),
    'Kalamazoo': (42.2917, -85.5872),
    'Flint': (43.0125, -83.6875),
    'Traverse City': (44.7631, -85.6206)
}

@st.cache_data
def load_data():
    # Read the CSV file
    df = pd.read_csv('michigan_synthetic_data.csv')
    
    # Function to extract city from address
    def extract_city(address):
        for city in mi_city_coords.keys():
            if city in address:
                return city
        return None

    # Extract city from address and add coordinates
    df['City'] = df['Address'].apply(extract_city)
    df['lat'], df['lon'] = zip(*df['City'].map(mi_city_coords))

    # Remove rows with unknown cities
    df = df.dropna(subset=['lat', 'lon'])
    
    return df

# Load the data
df = load_data()

# Streamlit app
st.title('Michigan Synthetic Data Visualization')

# Display the map
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=44.3148,
        longitude=-85.6024,
        zoom=6,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=df,
            get_position='[lon, lat]',
            get_color=[255, 0, 0, 160],
            get_radius=1000,
            pickable=True,
            opacity=0.8,
        ),
    ],
    tooltip={
        'html': '<b>Name:</b> {First Name} {Last Name}<br>'
                '<b>Address:</b> {Address}<br>'
                '<b>Group:</b> {Random Letter}',
        'style': {
            'backgroundColor': 'steelblue',
            'color': 'white'
        }
    }
))

# Display data summary
st.subheader('Data Summary')
st.write(f"Total data points: {len(df)}")

# Distribution of Random Letters
st.subheader('Distribution of Random Letters')
letter_counts = df['Random Letter'].value_counts().sort_index()
st.bar_chart(letter_counts)

# Distribution between Peninsulas
st.subheader('Distribution between Peninsulas')
upper_cities = ['Marquette', 'Escanaba', 'Sault Ste. Marie', 'Houghton', 'Iron Mountain']
df['Peninsula'] = df['City'].apply(lambda x: 'Upper' if x in upper_cities else 'Lower')
peninsula_distribution = df['Peninsula'].value_counts()
st.write(peninsula_distribution)
st.write(f"Upper Peninsula: {peninsula_distribution['Upper'] / len(df) * 100:.2f}%")
st.write(f"Lower Peninsula: {peninsula_distribution['Lower'] / len(df) * 100:.2f}%")

# Distribution of data points by city
st.subheader('Distribution by City')
city_distribution = df['City'].value_counts()
st.bar_chart(city_distribution) 