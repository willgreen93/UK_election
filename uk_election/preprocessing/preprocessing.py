import pandas as pd
import numpy as np
from scipy.interpolate import interp1d


# Function for cleaning the GE results
def preprocess_general_election_results(elections_df: pd.DataFrame):
    """
    Clean the general election results data from UK parliament website.
    Returns a cleaned dataframe with:
    - constituency_id and name
    - year (general election year)
    - party name and share of votes, divided in Con, Lab, Lib, Oth (other)
    """
    clean_election_results = elections_df.copy()
    # Clean the column names
    clean_election_results.columns = clean_election_results.columns.str.strip()
    # Fill the NaN with 0 (when NaN means 0, since no votes)
    clean_election_results = clean_election_results.fillna(0)
    # Remove and rename columns
    clean_election_results.drop(["electorate", "turnout"], axis=1, inplace=True)
    clean_election_results.rename(columns={"election": "year"}, inplace=True)
    # group oth and natSW, and drop the ones that are not needed
    clean_election_results["oth_votes"] = (
        clean_election_results["natSW_votes"] + clean_election_results["oth_votes"]
    )
    clean_election_results["oth_share"] = (
        clean_election_results["natSW_share"] + clean_election_results["oth_share"]
    )
    clean_election_results.drop(["natSW_votes", "natSW_share"], axis=1, inplace=True)
    # Get previous share per party by constituency
    clean_election_results["con_share_prev"] = clean_election_results.groupby(
        "constituency_id"
    )["con_share"].shift(1)
    clean_election_results["lib_share_prev"] = clean_election_results.groupby(
        "constituency_id"
    )["lib_share"].shift(1)
    clean_election_results["lab_share_prev"] = clean_election_results.groupby(
        "constituency_id"
    )["lab_share"].shift(1)
    clean_election_results["oth_share_prev"] = clean_election_results.groupby(
        "constituency_id"
    )["oth_share"].shift(1)
    # select data from 2010 onwards, and reset index
    clean_election_results = clean_election_results[
        clean_election_results.year != 2005
    ].reset_index(drop=True)
    # in 2010, do not have previous data for 13 constituencies (new ones), so we drop
    clean_election_results.dropna(inplace=True)
    # reorder columns
    column_order = [
        "year",
        "constituency_id",
        "constituency_name",
        "country/region",
        "total_votes",
        "con_votes",
        "lab_votes",
        "lib_votes",
        "oth_votes",
        "con_share",
        "lab_share",
        "lib_share",
        "oth_share",
        "con_share_prev",
        "lab_share_prev",
        "lib_share_prev",
        "oth_share_prev",
    ]
    clean_election_results = clean_election_results[column_order]
    # I need to  manually create data for 2024
    future_df = clean_election_results[clean_election_results.year == 2019]
    future_df["year"] = 2024
    future_df[
        ["con_share_prev", "lab_share_prev", "lib_share_prev", "oth_share_prev"]
    ] = future_df[["con_share", "lab_share", "lib_share", "oth_share"]]
    future_df[
        [
            "total_votes",
            "con_votes",
            "lab_votes",
            "lib_votes",
            "oth_votes",
            "con_share",
            "lab_share",
            "lib_share",
            "oth_share",
        ]
    ] = np.nan
    clean_election_results = pd.concat(
        [clean_election_results, future_df], ignore_index=True
    )
    # Calculate the avg for GE
    clean_election_results["mean_con_share_ge"] = clean_election_results.groupby(
        "year"
    )["con_share_prev"].transform("mean")
    clean_election_results["mean_lab_share_ge"] = clean_election_results.groupby(
        "year"
    )["lab_share_prev"].transform("mean")
    clean_election_results["mean_lib_share_ge"] = clean_election_results.groupby(
        "year"
    )["lib_share_prev"].transform("mean")
    clean_election_results["mean_oth_share_ge"] = clean_election_results.groupby(
        "year"
    )["oth_share_prev"].transform("mean")
    return clean_election_results


def clean_election_results(election_results: pd.DataFrame):
    """Clean the election results data"""
    clean_election_results = election_results.copy()
    # Clean the column names
    clean_election_results.columns = clean_election_results.columns.str.strip()
    # Fill the NaN with 0 (when NaN means 0, since no votes)
    clean_election_results = clean_election_results.fillna(0)
    # Remove and rename columns
    clean_election_results.drop(["electorate", "turnout"], axis=1, inplace=True)
    clean_election_results.rename(columns={"election": "year"}, inplace=True)
    # group oth and natSW, and drop the ones that are not needed
    clean_election_results["oth_votes"] = (
        clean_election_results["natSW_votes"] + clean_election_results["oth_votes"]
    )
    clean_election_results["oth_share"] = (
        clean_election_results["natSW_share"] + clean_election_results["oth_share"]
    )
    clean_election_results.drop(["natSW_votes", "natSW_share"], axis=1, inplace=True)
    # Get previous share per party by constituency
    clean_election_results["con_share_prev"] = clean_election_results.groupby(
        "constituency_id"
    )["con_share"].shift(1)
    clean_election_results["lib_share_prev"] = clean_election_results.groupby(
        "constituency_id"
    )["lib_share"].shift(1)
    clean_election_results["lab_share_prev"] = clean_election_results.groupby(
        "constituency_id"
    )["lab_share"].shift(1)
    clean_election_results["oth_share_prev"] = clean_election_results.groupby(
        "constituency_id"
    )["oth_share"].shift(1)
    # select data from 2010 onwards, and reset index
    clean_election_results = clean_election_results[
        clean_election_results.year != 2005
    ].reset_index(drop=True)
    # in 2010, do not have previous data for 13 constituencies (new ones), so we drop
    clean_election_results.dropna(inplace=True)
    # reorder columns
    column_order = [
        "year",
        "constituency_id",
        "constituency_name",
        "country/region",
        "total_votes",
        "con_votes",
        "lab_votes",
        "lib_votes",
        "oth_votes",
        "con_share",
        "lab_share",
        "lib_share",
        "oth_share",
        "con_share_prev",
        "lab_share_prev",
        "lib_share_prev",
        "oth_share_prev",
    ]
    clean_election_results = clean_election_results[column_order]
    # I need to  manually create data for 2024
    future_df = clean_election_results[clean_election_results.year == 2019]
    future_df["year"] = 2024
    future_df[
        ["con_share_prev", "lab_share_prev", "lib_share_prev", "oth_share_prev"]
    ] = future_df[["con_share", "lab_share", "lib_share", "oth_share"]]
    future_df[
        [
            "total_votes",
            "con_votes",
            "lab_votes",
            "lib_votes",
            "oth_votes",
            "con_share",
            "lab_share",
            "lib_share",
            "oth_share",
        ]
    ] = np.nan
    clean_election_results = clean_election_results.append(future_df)
    # Calculate the avg for GE
    clean_election_results["mean_con_share_ge"] = clean_election_results.groupby(
        "year"
    )["con_share_prev"].transform("mean")
    clean_election_results["mean_lab_share_ge"] = clean_election_results.groupby(
        "year"
    )["lab_share_prev"].transform("mean")
    clean_election_results["mean_lib_share_ge"] = clean_election_results.groupby(
        "year"
    )["lib_share_prev"].transform("mean")
    clean_election_results["mean_oth_share_ge"] = clean_election_results.groupby(
        "year"
    )["oth_share_prev"].transform("mean")
    return clean_election_results


# Function to clean the polling data
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
    # # Calculate shate for the other parties
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
        "con_pre_ge_poll",
        "lab_pre_ge_poll",
        "lib_pre_ge_poll",
        "oth_pre_ge_poll",
    ]
    return cleaned_polling_df


###################### CENSUS DATA PREPROCESSING ############################


# Function for cleaning age data
def preprocess_census_age(age_df: pd.DataFrame):
    """
    Clean the census age data. Return a cleaned dataframe with:
    - year (census year)
    - constituency_id and name
    - percentage of population in each age group (0-9, 10-19, 20-29, 30-39, 40-49, 50-59, 60-69, 70-79, 80+)
    """
    # Step 1: Selecting specific columns
    cleaned_age_df = age_df[
        ["Age group", "ConstituencyName", "ONSConstID", "RegionName", "Date", "Const%"]
    ]
    # Step 2: Renaming columns
    cleaned_age_df.columns = [
        "age",
        "constituency_name",
        "constituency_id",
        "region",
        "year",
        "percentage",
    ]
    # Step 3: Converting 'Year' to integer
    cleaned_age_df["year"] = cleaned_age_df["year"].astype(int)
    # Step 4: Converting 'Percentage' to numeric
    cleaned_age_df["percentage"] = (
        pd.to_numeric(cleaned_age_df["percentage"].str[:-1]) / 100
    )
    # Step 5: Spreading data using pivot
    cleaned_age_df = cleaned_age_df.pivot(
        index=["year", "constituency_name", "constituency_id"],
        columns="age",
        values="percentage",
    ).reset_index()
    # Step 6: Convert year to integer
    cleaned_age_df["year"] = cleaned_age_df["year"].astype(int)
    return cleaned_age_df


# Function for cleaning ethnicity data
def preprocess_census_ethnicity(ethnicity_df: pd.DataFrame):
    """
    Clean the census ethnicity data. Return a cleaned dataframe with:
    - year (census year)
    - constituency_id and name
    - percentage of population in each ethnicity group (Asian, Black, Mixed, Other, White)
    """
    # Select columns
    cleaned_ethnicity_df = ethnicity_df[
        [
            "ConstituencyName",
            "ONSConstID",
            "broad_ethnic_groups",
            "con_pc_2021",
            "con_pc_2011",
        ]
    ]
    # Rename columns
    cleaned_ethnicity_df.columns = [
        "constituency_name",
        "constituency_id",
        "group",
        "2021",
        "2011",
    ]
    # Replace values in the 'group' column
    cleaned_ethnicity_df["group"] = cleaned_ethnicity_df["group"].replace(
        {"Mixed or Multiple ethnic groups": "Mixed"}
    )
    # Gather columns
    cleaned_ethnicity_df = pd.melt(
        cleaned_ethnicity_df,
        id_vars=["constituency_name", "constituency_id", "group"],
        var_name="year",
        value_name="percentage",
    )
    # Spread data
    cleaned_ethnicity_df = cleaned_ethnicity_df.pivot_table(
        index=["constituency_id", "constituency_name", "year"],
        columns="group",
        values="percentage",
        fill_value=0,
    ).reset_index()
    # Set year as integer
    cleaned_ethnicity_df["year"] = cleaned_ethnicity_df["year"].astype(int)
    return cleaned_ethnicity_df


# Function for cleaning living status data
def preprocess_census_livingstatus(living_df: pd.DataFrame):
    """
    Clean the census living status data. Return a cleaned dataframe with:
    - year (census year)
    - constituency_id and name
    - percentage of population in each living status group (Home owners, Private renters, Social renters)
    """
    # Select columns
    cleaned_living_df = living_df[
        ["ConstituencyName", "ONSConstID", "groups", "con_num", "con_2011_num"]
    ]
    # Rename columns
    cleaned_living_df.columns = [
        "constituency_name",
        "constituency_id",
        "group",
        "2021",
        "2011",
    ]
    # Gather columns
    cleaned_living_df = pd.melt(
        cleaned_living_df,
        id_vars=["constituency_name", "constituency_id", "group"],
        var_name="year",
        value_name="N_housing",
    )
    # Group by Constituency and Year
    grouped_data = cleaned_living_df.groupby(["constituency_id", "year"])
    # Calculate p_housing
    cleaned_living_df["p_housing"] = grouped_data["N_housing"].transform(
        lambda x: x / x.sum()
    )
    # Drop N_housing column
    cleaned_living_df = cleaned_living_df.drop("N_housing", axis=1)
    # Spread data
    cleaned_living_df = cleaned_living_df.pivot_table(
        index=["year", "constituency_id", "constituency_name"],
        columns="group",
        values="p_housing",
        fill_value=0,
    ).reset_index()
    # Rename columns
    cleaned_living_df.columns = [
        col.replace(" ", "_") for col in cleaned_living_df.columns
    ]
    # Convert year to integer
    cleaned_living_df["year"] = cleaned_living_df["year"].astype(int)
    return cleaned_living_df


# Interpolate census data for years 2010-2024
def interpolate_data_frame(
    df: pd.DataFrame, year_start: int, year_end: int, start_col=3
):
    """
    Interpolate the data for the years 2010-2024.
    Return a dataframe with the interpolated values.
    """
    years_sequence = list(range(year_start, year_end + 1))
    interpolated_df_hold = pd.DataFrame()

    for cons in df["constituency_name"].unique():
        df_filtered = df[df["constituency_name"] == cons]

        interpolated_values = {
            "constituency_name": cons,
            "constituency_id": df_filtered["constituency_id"].iloc[0],
            "year": years_sequence,
        }

        for col in df_filtered.columns[start_col:]:
            interpolator = interp1d(
                df_filtered["year"],
                df_filtered[col],
                kind="linear",
                fill_value="extrapolate",
            )
            interpolated_values[col] = interpolator(years_sequence)

        interpolated_df = pd.DataFrame(interpolated_values)

        if interpolated_df_hold.empty:
            interpolated_df_hold = interpolated_df
        else:
            interpolated_df_hold = pd.concat([interpolated_df_hold, interpolated_df])

    return interpolated_df_hold
