import altair as alt
import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
from data_to_chart_prep import (
    get_basemap,
    get_election_data,
    merge_dataframes,
    fetch_data_from_api,
)
from params import *
from io import BytesIO

####################################################################
############_________Sliders sidebar goes here________##############


# Title for left sidebar
st.sidebar.subheader("Pretty Little Sliders")

# Title for the sliders
st.sidebar.text("Move the sliders to change \nthe polling percentages on the map")

conservative_rating = st.sidebar.slider(
    "Conservative Rating", min_value=0, max_value=100, value=25
)
labor_party_rating = st.sidebar.slider(
    "Labor Party Rating", min_value=0, max_value=100, value=44
)
libdem_party_rating = st.sidebar.slider(
    "Lib Dem Rating",
    min_value=0,
    max_value=100,
    value=10,
)
other_party_rating = st.sidebar.slider(
    "Other Parties",
    min_value=0,
    max_value=100,
    value=21,
)

params = {
    "con_poll": conservative_rating / 100,
    "lab_poll": labor_party_rating / 100,
    "lib_poll": libdem_party_rating / 100,
    "oth_poll": other_party_rating / 100,
}


#############################################################################
###########################__Data goes here___###############################
######################____BASE___MAP___DATA____##############################


map_df = get_basemap(url)
data_source = fetch_data_from_api(api_url, params=params, headers=None)
preds = get_election_data(data_source)
df = merge_dataframes(map_df, preds)


# Display the current values of the sliders
st.sidebar.text(f"Current Conservative Rating: {conservative_rating}%")
st.sidebar.text(f"Current Labor Party Rating: {labor_party_rating}%")
st.sidebar.text(f"Current Lib Dem Rating: {libdem_party_rating}%")
st.sidebar.text(f"Current Other Parties Rating: {other_party_rating}%")


####################################################################
#############_________Map gets displayed here________###############
brush = alt.selection(type="interval")

map = (
    alt.Chart(df)
    .mark_square()
    .encode(
        x=alt.X("q").scale(zero=False).axis(None),
        y=alt.Y("r").scale(zero=False).axis(None),
        color=colours_obj.legend(title="Winning Party", orient="bottom"),
        size=alt.value(65),
        tooltip=["n:N"],
    )
    .properties(width=450, height=540)
    .configure_axis(grid=False)
    .configure_view(strokeWidth=0)
)


bar_ch = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("count():Q", title="Total Count"),
        y=alt.Y("winning_party:N", title="Winning Party", axis=None),
        tooltip=[alt.Tooltip("count()")],
        color=colours_obj.legend(None),
    )
    .properties(
        title="Total Count of Each Incumbent Party",
        width=400,
    )
)


# st.altair_chart(map)
# st.altair_chart(bar_ch)

######################################################

col1, col2 = st.columns(2)

with col1:
    st.header("UK, hun?")
    st.altair_chart(map)

with col2:
    st.altair_chart(bar_ch)
