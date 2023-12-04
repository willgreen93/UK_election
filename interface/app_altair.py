import altair as alt
import altair_viewer
import streamlit as st

# import pydeck as pdk
# import json
import pandas as pd
import random
import geopandas as gpd
import numpy as np

####################################################################
########################__Data goes here___#########################
###################____BASE___MAP___DATA____########################

alt_data = pd.read_json(
    "/home/asia/code/willgreen93/UK_election/interface/data/uk-constituencies-2019-BBC.hexjson"
)
alt_df = pd.DataFrame(alt_data)

alt_df[["n", "r", "q", "region"]] = alt_df["hexes"].apply(
    lambda x: pd.Series([x.get("n"), x.get("r"), x.get("q"), x.get("region")])
)

new_df = alt_df.rename_axis("constituency_id").reset_index().drop(columns=["hexes"])

####################################################################
########################__Data goes here___#########################
###################____ELECTION_____DATA____########################

results_2019 = pd.read_csv(
    "/home/asia/code/willgreen93/UK_election/interface/data/elec_data_2019.csv"
)


basic_df = results_2019[
    ["constituency_id", "constituency", "country", "incumbent_party"]
]

df = pd.merge(basic_df, new_df, on="constituency_id", how="left")

##############_________Assigning Colors to each party________#############
parties = ["conservative", "labour", "liberal_democrats", "other_parties"]
party_colours = ["#F78DA7", "blue", "orange", "lightgrey"]
colours_obj = alt.Color(
    "incumbent_party:N", scale=alt.Scale(domain=parties, range=party_colours)
)


#############################################
####___Sliders sidebar goes here___##########

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


##########################################
###########__Map goes here__###############
st.altair_chart(
    alt.Chart(df)
    .mark_square()
    # .mark_circle()
    .encode(
        x=alt.X("q").scale(zero=False).axis(None),
        y=alt.Y("r").scale(zero=False).axis(None),
        color=colours_obj,
        size=alt.value(70),
        tooltip=["n:N"],
    )
    .properties(width=550, height=650)
    .configure_axis(grid=False)
    .configure_view(strokeWidth=0)
)
