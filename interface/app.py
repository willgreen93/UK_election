import altair as alt
import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
from data_to_chart_prep import get_basemap, get_election_data, merge_dataframes
from params import *
from io import BytesIO

#############################################################################
###########################__Data goes here___###############################
######################____BASE___MAP___DATA____##############################

client = storage.Client()

# Get the bucket and file
bucket = client.bucket(bucket_name)
blob = bucket.blob(url)
blob2 = bucket.blob(data_source)

# Download the file's content
hex_json = blob.download_as_text()
preds_csv = blob2.download_as_text()

# Read the data using pandas
hexmap = pd.read_json(BytesIO(hex_json))
preds = pd.read_json(BytesIO(preds_csv))

map_df = get_basemap(hexmap)
preds_df = get_election_data(preds)
df = merge_dataframes(map_df, preds_df)

####################################################################
############_________Sliders sidebar goes here________##############

# Streamlit app layout
st.sidebar.title("UK, hun?")

# Title for left sidebar
st.sidebar.subheader("Pretty Little Sliders")

# Title for the sliders
st.sidebar.text("Move the sliders to change \nthe polling percentages on the map")

conservative_rating = st.sidebar.slider(
    "Conservative Rating", min_value=0, max_value=100, value=50
)
labor_party_rating = st.sidebar.slider(
    "Labor Party Rating", min_value=0, max_value=100, value=50
)
libdem_party_rating = st.sidebar.slider(
    "Lib Dem Rating", min_value=0, max_value=100, value=50
)
other_party_rating = st.sidebar.slider(
    "Other Parties", min_value=0, max_value=100, value=50
)
let_chaos_reign = st.sidebar.slider(
    "Let Chaos Reign", min_value=0, max_value=100, value=50
)

# Display the current values of the sliders
st.sidebar.text(f"Current Conservative Rating: {conservative_rating}%")
st.sidebar.text(f"Current Labor Party Rating: {labor_party_rating}%")
st.sidebar.text(f"Current Lib Dem Rating: {libdem_party_rating}%")
st.sidebar.text(f"Current Other Parties Rating: {other_party_rating}%")
st.sidebar.text(f"Current Chaos Rating: {let_chaos_reign}%")


####################################################################
#############_________Map gets displayed here________###############
st.altair_chart(
    alt.Chart(df)
    .mark_square()
    # .mark_circle()
    .encode(
        x=alt.X("q").scale(zero=False).axis(None),
        y=alt.Y("r").scale(zero=False).axis(None),
        color=colours_obj.legend(
            title="Incumbent Party",
        ),
        size=alt.value(65),
        tooltip=["n:N"],
    )
    .properties(width=700, height=650)
    .configure_axis(grid=False)
    .configure_view(strokeWidth=0)
)
