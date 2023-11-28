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

# Load your HexJSON data (replace 'your_hexjson_file.json' with your actual file)
with open("interface/uk-constituencies-2023.json", "r") as file:
    hexjson_data = json.load(file)
st.write(hexjson_data)  # debugging tool

# Load HexJSON layer
hex_layer = pdk.Layer(
    "HexagonLayer",
    data=hexjson_data,
    get_position="[r, q]",
    auto_highlight=True,
    elevation_scale=50,
    pickable=True,
    extruded=True,
)

# Set the initial view location (adjust as needed)
view_state = pdk.ViewState(
    longitude=-3.2766,
    latitude=54.7024,
    zoom=4.5,  # You may need to adjust the zoom level based on your preference
    min_zoom=0,
    max_zoom=15,
    pitch=0,
    bearing=-27.36,
)

# Create the PyDeck deck
deck = pdk.Deck(layers=[hex_layer], initial_view_state=view_state)

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
st.pydeck_chart(deck)
