# import plotly.figure_factory as ff

# import plotly.express as px
# import matplotlib.pyplot as plt
# import pandas as pd
# import json

# with open("interface/uk-constituencies-2023.json", "r") as file:
#     data = json.load(file)
# df = pd.DataFrame(data["hexes"]).T
# df.columns = ["const", "centroid_lat", "centroid_lon", "region", "colour"]
# df = df.astype({"centroid_lat": "float", "centroid_lon": "float"})


# token = "pk.eyJ1IjoibGV3YWdvbnBvbG9uaWtpIiwiYSI6ImNscGlmbmRhczBhNHEya3Q3b250YjAxbGIifQ.MO88QvgzYmYbxwujAWkHxQ"
# px.set_mapbox_access_token(token)
# df_old = px.data.carshare()

# fig = ff.create_hexbin_mapbox(
#     center={"lon": -3.2766, "lat": 54.7024},
#     data_frame=df,
#     lat="centroid_lat",
#     lon="centroid_lon",
#     nx_hexagon=15,
#     opacity=0.5,
#     labels={"color": "Point Count"},
#     min_count=1,
# )

# fig.update_geos(visible=False, showrivers=False, showcountries=False)
# st.plotly_chart(fig)


import pydeck as pdk
import pandas as pd
import random
import geopandas as gpd
import json
import streamlit as st

with open("json_files/England.geojson", "r") as file:
    data = json.load(file)

gdf = gpd.GeoDataFrame.from_features(data["features"])
coordinates = gdf.get_coordinates()
coordinates.columns = ["lng", "lat"]
centroids = gdf.centroid.to_frame()
df = pd.DataFrame()
df["lng"] = gdf.centroid.x
df["lat"] = gdf.centroid.y


fig = ff.create_hexbin_mapbox(
    data_frame=df,
    lat="lat",
    lon="lng",  # color="randNumCol", #color_discrete_map =["red", "blue", "grey"],
    nx_hexagon=20,
    opacity=0.5,
    labels={"color": "color label"},
    min_count=1,
)
fig.show()
# layer = pdk.Layer(
#     "HexagonLayer",
#     df,
#     get_position=["lng", "lat"],
#     elevation_scale=0,
#     pickable=True,
#     elevation_range=[0, 3000],
#     filled=True,
#     coverage=10,
# )
# view_state = pdk.ViewState(
#     longitude=-1.415,
#     latitude=52.2323,
#     zoom=5,
#     min_zoom=5,
#     max_zoom=15,
#     pitch=0,
#     bearing=0,
# )

# Render without the map
# r = pdk.Deck(layers=[layer], initial_view_state=view_state, map_style="")
# st.pydeck_chart(r)
