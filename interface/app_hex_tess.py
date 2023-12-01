import pydeck as pdk
import pandas as pd
import random
import geopandas as gpd
import json
import streamlit as st
import tesspy
from matplotlib.colors import ListedColormap
import numpy as np

england = tesspy.Tessellation("England")

england.get_polygon().plot(figsize=(10, 10)).set_axis_off()

# england.get_polygon().crs

england_hex_5 = england.hexagons(5)

england_hex_5["votes"] = england_hex_5.apply(lambda x: np.random.randint(0, 4), axis=1)

england_hex_5 = england.hexagons(5)
cmap = ListedColormap(["#ff3333", "b", "#33ffff", "#999966"])
r = england_hex_5.plot(lw=1, edgecolor="w", cmap=cmap, figsize=(10, 10)).set_axis_off()

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

# # Display the PyDeck chart using st.pydeck_chart
st.pyplot(r)
