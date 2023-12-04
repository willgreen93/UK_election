import pandas as pd
import geopandas as gpd
import numpy as np

def get_basemap(url):
    """
    This function takes the url of the hexjson file and returns a dataframe
    with the hexjson data. The dataframe has the following columns:
    constituency_id, n, r, q, region
    """
    alt_data = pd.read_json(url)
    alt_df = pd.DataFrame(alt_data)

    alt_df[["n", "r", "q", "region"]] = alt_df["hexes"].apply(
        lambda x: pd.Series([x.get("n"), x.get("r"), x.get("q"), x.get("region")])
    )

    new_df = alt_df.rename_axis("constituency_id").reset_index().drop(columns=["hexes"])
    return new_df
