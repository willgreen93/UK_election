import pandas as pd
import geopandas as gpd
import numpy as np
import requests


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


def fetch_data_from_api(api_url, params=None, headers=None):
    response = requests.get(api_url, params=params, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_election_data(data_source):
    """
    This function takes the url of the election data and returns a dataframe
    with the election data. The dataframe has the following columns:
    constituency_id, constituency, country, incumbent_party
    """
    preds = pd.DataFrame(data_source)
    return preds


def add_scotland_ni_data(extra_cols):
    """
    This add the static data for Scotland and NI constituencies
    """
    scotni_data = pd.read_csv(extra_cols)
    scotni_df = pd.DataFrame(scotni_data)
    scotni_df.rename(columns={"ons_id": "constituency_id"}, inplace=True)
    scotni_df_clean = scotni_df.drop(
        columns=["snp", "dup", "sf", "sdlp", "uup", "alliance"]
    )
    return scotni_df_clean


def merge_dataframes(scotni_df=None, pred_df=None, map_df=None):
    """
    This function takes the basic_df and new_df and returns a dataframe
    with the election data. The dataframe has the following columns:
    constituency_id, constituency, country, incumbent_party, n, r, q, region
    """
    base_df = pd.concat([scotni_df, pred_df], ignore_index=True)
    base_df["winning_party"] = base_df["winning_party"].str.lower()
    df = pd.merge(map_df, base_df, on="constituency_id", how="left")

    return df

