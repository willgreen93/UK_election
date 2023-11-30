# find a place to insert the Y as a clean dataframe
# connect the two sliders with the column we want
# add the map >> use an API map or something from google
# label each hexagon with the colors blue or red for each constituency

# requirements
# - static map with all the divisions
# - SVG maybe from the


import streamlit as st
import pydeck as pdk
import json
import pandas as pd
import random
import geopandas as gpd
import numpy as np

##geo_data is a dataframe with the centroids of the polygons and overlapping
# downloaded from https://martinjc.github.io/UK-GeoJSON/ *ENGLAND > National > \
# Local Authority Districts and converted to GEOJson

# Open the JSON file and load it into a variable
with open("interface/data/England.geojson", "r") as file:
    geo_data = json.load(file)

# Changing the centroid lons and lats as a DataFrame
gdf = gpd.GeoDataFrame.from_features(geo_data["features"])
coordinates = gdf.get_coordinates()
coordinates.columns = ["lng", "lat"]
centroids = gdf.centroid.to_frame()
geo_data = pd.DataFrame()
geo_data["lng"] = gdf.centroid.x
geo_data["lat"] = gdf.centroid.y

# setting results as random integers between 0 to 3
geo_data["fake_results"] = np.random.randint(0, 4, geo_data.shape[0])

# map colors
color_scale = {
    0: [255, 0, 0, 1],  # Red
    1: [0, 0, 255, 1],  # Blue
    2: [128, 128, 128, 1],  # Grey
    3: [0, 255, 0, 1],  # Green
}

# Map "fake_results" values to RGB colors
geo_data["color"] = geo_data["fake_results"].map(color_scale)


# styling the map f hexes
layer = pdk.Layer(
    "HexagonLayer",
    geo_data,
    get_position=["lng", "lat"],
    elevation_scale=0,
    pickable=True,
    elevation_range=[0, 3000],
    filled=True,
    coverage=10,
    get_fill_color="color",  # Use the new "color" column
)

view_state = pdk.ViewState(
    longitude=-1.415,
    latitude=52.2323,
    zoom=5,
    min_zoom=5,
    max_zoom=15,
    pitch=0,
    bearing=0,
)

# Render without the map
r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style="",
    map_provider="",
    api_keys=None,
)

# Streamlit app layout
st.title("UK, hun?")

# Create a placeholder for the map on the left side
st.sidebar.header("Interactive Hex Map")

# Create sliders for conservative and labor party approval ratings on the right side
st.sidebar.header("Sliders for Polling/Approval Ratings")
conservative_rating = st.sidebar.slider(
    "Conservative Rating", min_value=0, max_value=100, value=50
)
labor_party_rating = st.sidebar.slider(
    "Labor Party Rating", min_value=0, max_value=100, value=50
)

# Display the current values of the sliders
st.sidebar.text(f"Current Conservative Rating: {conservative_rating}%")
st.sidebar.text(f"Current Labor Party Rating: {labor_party_rating}%")

# Display the PyDeck chart using st.pydeck_chart
st.pydeck_chart(r)
