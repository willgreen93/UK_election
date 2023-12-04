import altair as alt
import altair_viewer
import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
from data_to_chart_prep import get_basemap, get_election_data

####################################################################
########################__Data goes here___#########################
###################____BASE___MAP___DATA____########################

url = "data/uk-constituencies-2019-BBC.hexjson"
new_df = get_basemap(url)

####################################################################
########################__Data goes here___#########################
###################____ELECTION_____DATA____########################

data_source = "data/elec_data_2019.csv"
preds_df = get_election_data(data_source)

df = pd.merge(preds_df, new_df, on="constituency_id", how="left")

####################################################################
###########_________Assigning Colors to each party________##########
parties = ["conservative", "labour", "liberal_democrats", "other_parties"]
party_colours = ["#F78DA7", "blue", "orange", "lightgrey"]
colours_obj = alt.Color(
    "incumbent_party:N", scale=alt.Scale(domain=parties, range=party_colours)
)


####################################################################
############_________Sliders sidebar goes here________##############

# Streamlit app layout
st.title("UK, hun?")

# Title for left sidebar
st.sidebar.header("Pretty Little Sliders")

# Title for the sliders
st.sidebar.subheader("Sliders for Polling/Approval Ratings")
st.sidebar.text("Move the sliders to change the map")
conservative_rating = st.sidebar.slider(
    "Conservative Rating", min_value=0, max_value=100, value=50
)
labor_party_rating = st.sidebar.slider(
    "Labor Party Rating", min_value=0, max_value=100, value=50
)
let_chaos_reign = st.sidebar.slider(
    "Let Chaos Reign", min_value=0, max_value=100, value=50
)

# Display the current values of the sliders
st.sidebar.text(f"Current Conservative Rating: {conservative_rating}%")
st.sidebar.text(f"Current Labor Party Rating: {labor_party_rating}%")
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
        color=colours_obj,
        size=alt.value(65),
        tooltip=["n:N"],
    )
    .properties(width=555, height=650)
    .configure_axis(grid=False)
    .configure_view(strokeWidth=0)
)
