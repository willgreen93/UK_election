import plotly.figure_factory as ff
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
import json

with open("interface/uk-constituencies-2023.json", "r") as file:
    data = json.load(file)
df = pd.DataFrame(data["hexes"]).T
df.columns = ["const", "centroid_lat", "centroid_lon", "region", "colour"]
df = df.astype({"centroid_lat": "float", "centroid_lon": "float"})


token = "pk.eyJ1IjoibGV3YWdvbnBvbG9uaWtpIiwiYSI6ImNscGlmbmRhczBhNHEya3Q3b250YjAxbGIifQ.MO88QvgzYmYbxwujAWkHxQ"
px.set_mapbox_access_token(token)
df_old = px.data.carshare()

fig = ff.create_hexbin_mapbox(
    center={"lon": -3.2766, "lat": 54.7024},
    data_frame=df,
    lat="centroid_lat",
    lon="centroid_lon",
    nx_hexagon=15,
    opacity=0.5,
    labels={"color": "Point Count"},
    min_count=1,
)

fig.update_geos(visible=False, showrivers=False, showcountries=False)
st.plotly_chart(fig)
