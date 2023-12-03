import altair as alt
import altair_viewer
import streamlit as st

# import pydeck as pdk
# import json
import pandas as pd
import random
import geopandas as gpd
import numpy as np

#######################################
###########Data goes here##############

alt_data = pd.read_json(
    "/home/asia/code/willgreen93/UK_election/interface/data/uk-constituencies-2023.json"
)
alt_df = pd.DataFrame(alt_data)
##Data Setup Here##
alt_df[["n", "r", "q", "region", "colour"]] = alt_df["hexes"].apply(
    lambda x: pd.Series(
        [x.get("n"), x.get("r"), x.get("q"), x.get("region"), x.get("colour")]
    )
)

##this should be replaced when I create the pipeline##
##SAMPLE ONLY randomness, can be deleted when we have the predictions##
alt_df["votes"] = alt_df.apply(lambda x: np.random.randint(0, 4), axis=1)


##Assigning Colors to each party##
parties = ["Conservative", "Labour", "Lib Dem", "Other"]
party_colours = ["#F78DA7", "blue", "orange", "lightgrey"]


alt_df["Party"] = alt_df["votes"].apply(
    lambda x: parties[x] if x < len(parties) else "Other"
)

colours_obj = alt.Color("Party:N", scale=alt.Scale(domain=parties, range=party_colours))
### selector not working SELECTOR SHOULD GO HERE HUHUHUHU##
# selector = alt.selection_point(empty=True, fields=['Party'])

# colours_condition = alt.condition(colours_obj, alt.value("lightgray"))  # selector,


#######################################
####Sliders sidebar goes here##########
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


#######################################
###########Map goes here###############
st.altair_chart(
    alt.Chart(alt_df)
    .mark_square()
    # .mark_circle()
    .encode(
        # x="q", changed this to alt.X
        x=alt.X("q").scale(zero=False).axis(None),
        # y="r",
        y=alt.Y("r").scale(zero=False).axis(None),
        color=colours_obj,
        size=alt.value(90),
        tooltip=["n:N"],
    )
    .properties(width=550, height=650)
    .configure_axis(grid=False)
    .configure_view(strokeWidth=0)
)
