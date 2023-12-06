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
    add_scotland_ni_data
)
from params import *
from io import BytesIO

####################################################################
############_________Sliders sidebar goes here________##############

col1, col2 = st.columns(2)

# Title for left sidebar
st.sidebar.subheader("2024 UK Elections Predictor")

# Title for the sliders
st.sidebar.text(
    "See how changes in polling \npercentages can affect\nthe outcome of the next election"
)

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
scotni_df = add_scotland_ni_data(extra_cols)
data_source = fetch_data_from_api(api_url, params=params, headers=None)
pred_df = get_election_data(data_source)
df = merge_dataframes(scotni_df, pred_df, map_df)

#############################################################################
#######################__shortcut to full text___############################
party_counts = df["winning_party"].value_counts()
max_winning_party = party_counts.idxmax()
max_winning_party_index = parties.index(max_winning_party)
party_full_name = parties_full[max_winning_party_index]

# Display the current values of the sliders

st.sidebar.text(f"Conservative Party Rating: {conservative_rating}%")
st.sidebar.text(f"Labor Party Rating: {labor_party_rating}%")
st.sidebar.text(f"Lib Dem Party Rating: {libdem_party_rating}%")
st.sidebar.text(f"Other Parties Rating: {other_party_rating}%")


####################################################################
#############_________Map gets displayed here________###############
# brush = alt.selection(type="interval")

map = (
    alt.Chart(df)
    .mark_square()
    .encode(
        x=alt.X("q").scale(zero=False).axis(None),
        y=alt.Y("r").scale(zero=False).axis(None),
        color=colours_obj.legend(title="Legend", orient="bottom"),
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
        title="Constituencies Won",
        width=400,
    )
)

######################################################

with col1:
    st.header("UK, hun?")
    st.altair_chart(map)


with col2:
    st.altair_chart(bar_ch)

st.markdown(
    f"""
    Based on the polling percentages you've chosen, we predict that
    the **{party_full_name}** will win in **{party_counts.max()}** constituencies.
    """
)
