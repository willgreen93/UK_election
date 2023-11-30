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


with open("interface/data/England.geojson", "r") as file:
    data = json.load(file)

gdf = gpd.GeoDataFrame.from_features(data["features"])
coordinates = gdf.get_coordinates()
coordinates.columns = ["lng", "lat"]
centroids = gdf.centroid.to_frame()
df = pd.DataFrame()
df["lng"] = gdf.centroid.x
df["lat"] = gdf.centroid.y

layer = pdk.Layer(
    "HexagonLayer",
    df,
    get_position=["lng", "lat"],
    elevation_scale=0,
    pickable=True,
    elevation_range=[0, 1000],
    filled=True,
    coverage=20,
    radius=500,
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
