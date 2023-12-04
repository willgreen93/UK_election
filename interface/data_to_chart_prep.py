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


def get_election_data(data_source):
    """
    This function takes the url of the election data and returns a dataframe
    with the election data. The dataframe has the following columns:
    constituency_id, constituency, country, incumbent_party
    """
    preds = pd.read_csv(data_source)
    preds_df = preds[["constituency_id", "constituency", "country", "incumbent_party"]]

    return preds_df


def merge_dataframes(basic_df, new_df):
    """
    This function takes the basic_df and new_df and returns a dataframe
    with the election data. The dataframe has the following columns:
    constituency_id, constituency, country, incumbent_party, n, r, q, region
    """
    df = pd.merge(basic_df, new_df, on="constituency_id", how="left")
    return df
