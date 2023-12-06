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
    add_scotland_ni_data,
)
from params import *
from io import BytesIO

####################################################################
############_________Sliders sidebar goes here________##############

col1, col2 = st.columns([2, 1], gap="small")

# Title for left sidebar
st.sidebar.subheader("2024 UK Elections Predictor")

# Title for the sliders
st.sidebar.markdown(
    """See how changes in polling \npercentages can affect\nthe outcome of the next election"""
)

conservative_rating = st.sidebar.slider(
    "Conservative Rating", min_value=0, max_value=100, value=25, format="%d%%"
)
labor_party_rating = st.sidebar.slider(
    "Labour Party Rating", min_value=0, max_value=100, value=44, format="%d%%"
)
libdem_party_rating = st.sidebar.slider(
    "Lib Dem Rating", min_value=0, max_value=100, value=10, format="%d%%"
)
other_party_rating = st.sidebar.slider(
    "Other Parties", min_value=0, max_value=100, value=21, format="%d%%"
)

params = {
    "con_poll": conservative_rating / 100,
    "lab_poll": labor_party_rating / 100,
    "lib_poll": libdem_party_rating / 100,
    "oth_poll": other_party_rating / 100,
}

total = sum(params.values())
if total > 1:
    st.sidebar.error("Polling percentages sum must be lower than 100%")
    st.stop()

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
# st.sidebar.markdown(f"""Conservative Party Rating: {conservative_rating}%""")
# st.sidebar.markdown(f"""Labour Party Rating: {labor_party_rating}%""")
# st.sidebar.markdown(f"""Lib Dem Party Rating: {libdem_party_rating}%""")
# st.sidebar.markdown(f"""Other Parties Rating: {other_party_rating}%""")


####################################################################
#############_________Map gets displayed here________###############
# brush = alt.selection(type="interval")

map = (
    alt.Chart(df)
    .mark_square()
    .encode(
        x=alt.X("q").scale(zero=False).axis(None),
        y=alt.Y("r").scale(zero=False).axis(None),
        color=colours_obj.legend(None),
        size=alt.value(65),
        tooltip=["n:N"],
    )
    .properties(width=440, height=540)
    .configure_axis(grid=False)
    .configure_view(strokeWidth=0)
)

bar_ch = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("count():Q", title="Total Count"),
        y=alt.Y("winning_party:N", title="Winning Party", axis=None, sort="-x"),
        tooltip=[
            alt.Tooltip("winning_party:N"),
        ],
        color=colours_obj.legend(title="Legend", orient="bottom"),
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


##### Constituency Selector #####

st.markdown("## Constituency Selector")


# Select the constituency
option = st.selectbox(
    label="Pick the constituency you want to investigate",
    options=df["n"],
)


# Transfor the DF (this can be packed in a function)
# Pick the value we need
selection_df = df[df["n"] == option][
    ["n", "con_votes", "lab_votes", "lib_votes", "oth_votes"]
].set_index("n")
# Rename columns
selection_df.columns = ["Conservative", "Labour", "Lib Dem", "Other"]
# Transpose to make colum,ns as rows
selection_df = selection_df.T.reset_index()
# Set column name to Votes
selection_df.columns = ["Party", "Predicted Votes"]
# Add percentage column
# Add a new column 'Percentage' with the share of votes
selection_df["Predicted Percentage"] = (
    selection_df["Predicted Votes"] / selection_df["Predicted Votes"].sum()
) * 100
# Format votes with commas (1,000)
selection_df["Predicted Votes"] = selection_df["Predicted Votes"].apply(
    "{:,.0f}".format
)
# Format % as percentage (43.2%)
selection_df["Predicted Percentage"] = selection_df["Predicted Percentage"].apply(
    "{:.1f}%".format
)


# Define color party function
def color_party(data):
    if data.Party == "Conservative":
        color = "#0087DC"
    elif data.Party == "Labour":
        color = "#dc143c"
    elif data.Party == "Lib Dem":
        color = "#FAA61A"
    elif data.Party == "Other":
        color = "#005B54"
    else:
        color = "black"
    return [f"background-color: {color}"] * len(data)


# Apply colors to the DF
colored_df = selection_df.style.apply(color_party, axis=1)
colored_contrast_df = colored_df.applymap(
    lambda x: "color:black" if x else "color:black;"
)


st.dataframe(colored_contrast_df, hide_index=True)


# st.table(data=selection_df)
# st.data_editor(data=selection_df)
