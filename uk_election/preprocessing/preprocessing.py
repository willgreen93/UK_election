import pandas as pd


def preprocess_general_election_results(input_df: pd.DataFrame):
    """Clean the general election results data from UK parliament website"""
    # Remove space from column names
    input_df.columns = input_df.columns.str.strip()
    # Fill the NaN with 0 (when NaN means 0, since no votes)
    input_df.fillna(0, inplace=True)
    # Remove and rename columns
    input_df.drop(["electorate", "turnout"], axis=1, inplace=True)
    input_df.rename(columns={"election": "year"}, inplace=True)
    # group oth and natSW, and drop the ones that are not needed
    input_df["other_votes"] = input_df["natSW_votes"] + input_df["oth_votes"]
    input_df["other_share"] = input_df["natSW_share"] + input_df["oth_share"]
    input_df.drop(
        ["natSW_votes", "oth_votes", "natSW_share", "oth_share"], axis=1, inplace=True
    )
    # Get previous share per party by constituency
    input_df["con_share_prev"] = input_df.groupby("constituency_id")["con_share"].shift(
        1
    )
    input_df["lib_share_prev"] = input_df.groupby("constituency_id")["lib_share"].shift(
        1
    )
    input_df["lab_share_prev"] = input_df.groupby("constituency_id")["lab_share"].shift(
        1
    )
    input_df["other_share_prev"] = input_df.groupby("constituency_id")[
        "other_share"
    ].shift(1)
    # Drop the NaN rows (13 rows in 2010)
    input_df.dropna(inplace=True)
    return input_df
