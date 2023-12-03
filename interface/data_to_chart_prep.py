from eqcart import Cartogram
from chorogrid import Chorogrid
import geopandas as gpd
import json
import numpy as np
import seaborn as sns
import streamlit as st
import pandas as pd
import pydeck as pdk
import random
from cartutils import is_valid, delete_old_point, update_new_point, shunt_point

##Process the HexMap file##
##replace with URL when possible##
alt_data = pd.read_json('/home/asia/code/willgreen93/UK_election/interface/data/uk-constituencies-2023.json')

#Change to DF to add the voting results(new y)
alt_df = pd.DataFrame(alt_data)
alt_df[['n', 'r', 'q','region','colour']] = alt_df['hexes'].apply(lambda x: pd.Series([x.get('n'), x.get('r'), x.get('q'),x.get('region'),x.get('colour')]))
alt_df["votes"] = alt_df.apply(lambda x: np.random.randint(0, 4), axis=1)

#assign the party colors
parties = ["Conservative", "Labour", "Lib Dem", "Other"]
party_colours = ["darkblue", "red", "orange", "green"]

#this line is random, change to JOIN when new y is available
alt_df['Party'] = alt_df['votes'].apply(lambda x: parties[x] if x < len(parties) else "Other")

##SAVE THIS DATAFRAME AS A CSV SOMEWHERE

###NOW HOW DO I CONNECT THE DATA I GET HERE???
