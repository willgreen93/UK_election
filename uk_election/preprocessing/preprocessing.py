import pandas as pd


# Function for cleaning the GE results
def preprocess_general_election_results(elections_df: pd.DataFrame):
    """
    Clean the general election results data from UK parliament website.
    Returns a cleaned dataframe with:
    - constituency_id and name
    - year (general election year)
    - party name and share of votes, divided in Con, Lab, Lib, Oth (other)
    """
    cleaned_elections_df = elections_df.copy()
    # Remove space from column names
    cleaned_elections_df.columns = cleaned_elections_df.columns.str.strip()
    # Fill the NaN with 0 (when NaN means 0, since no votes)
    cleaned_elections_df.fillna(0, inplace=True)
    # Remove and rename columns
    cleaned_elections_df.drop(["electorate", "turnout"], axis=1, inplace=True)
    cleaned_elections_df.rename(columns={"election": "year"}, inplace=True)
    # group oth and natSW, and drop the ones that are not needed
    cleaned_elections_df["other_votes"] = (
        cleaned_elections_df["natSW_votes"] + cleaned_elections_df["oth_votes"]
    )
    cleaned_elections_df["other_share"] = (
        cleaned_elections_df["natSW_share"] + cleaned_elections_df["oth_share"]
    )
    cleaned_elections_df.drop(
        ["natSW_votes", "oth_votes", "natSW_share", "oth_share"], axis=1, inplace=True
    )
    # Get previous share per party by constituency
    cleaned_elections_df["con_share_prev"] = cleaned_elections_df.groupby(
        "constituency_id"
    )["con_share"].shift(1)
    cleaned_elections_df["lib_share_prev"] = cleaned_elections_df.groupby(
        "constituency_id"
    )["lib_share"].shift(1)
    cleaned_elections_df["lab_share_prev"] = cleaned_elections_df.groupby(
        "constituency_id"
    )["lab_share"].shift(1)
    cleaned_elections_df["other_share_prev"] = cleaned_elections_df.groupby(
        "constituency_id"
    )["other_share"].shift(1)
    # Drop the NaN rows (13 rows in 2010)
    cleaned_elections_df.dropna(inplace=True)
    return cleaned_elections_df


# Function to clean the polling datA
def preprocess_polling_data(polling_df: pd.DataFrame):
    """
    Clean the polling data. Return a cleaned dataframe with:
    - year (general election year)
    - national polling (share) pre GE for Con, Lab, Lib, Oth (other)
    """
    cleaned_polling_df = polling_df.copy()
    # fill the missing values for year
    cleaned_polling_df["Year"] = cleaned_polling_df["Year"].ffill().astype(int)
    # Take the rows before the general election
    pre_GE_rows = cleaned_polling_df.loc[cleaned_polling_df["Month"] == "GE"].index - 1
    cleaned_polling_df = cleaned_polling_df.loc[pre_GE_rows[1:]]
    # Identify columns with float dtype (assuming percentage columns are floats)
    percentage_columns = cleaned_polling_df.select_dtypes(include="float64").columns
    # Divide columns by 100 if they are percentage columns
    cleaned_polling_df[percentage_columns] = (
        cleaned_polling_df[percentage_columns] / 100
    )
    # Calculate shate for the other parties
    cleaned_polling_df["oth_pre_ge"] = (
        1.0
        - cleaned_polling_df["Conservative"]
        - cleaned_polling_df["Labour"]
        - cleaned_polling_df["LD"]
    )
    cleaned_polling_df = cleaned_polling_df[
        ["Year", "Conservative", "Labour", "LD", "oth_pre_ge"]
    ].reset_index(drop=True)
    cleaned_polling_df.columns = [
        "year",
        "national_con_pre_ge",
        "national_lab_pre_ge",
        "national_lib_pre_ge",
        "national_oth_pre_ge",
    ]
    return cleaned_polling_df


###################### CENSUS DATA ############################

# Function for cleanind age data
