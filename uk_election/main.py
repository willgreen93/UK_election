import pandas as pd
from uk_election.params import LOCAL_DATA_PATH
import os
from uk_election.data.google import load_data_from_gcp
from uk_election.preprocessing.preprocessing import (
    preprocess_general_election_results,
    preprocess_polling_data,
    preprocess_census_age,
    preprocess_census_ethnicity,
    preprocess_census_livingstatus,
    interpolate_data_frame,
)
# import logging

# logging.basicConfig(level=logging.DEBUG)


def preprocess():
    # Step 1: Download from GCP
    load_data_from_gcp()

    # Step 2: Import the data as DFs
    elections_df = pd.read_csv(
        os.path.join(LOCAL_DATA_PATH, "general_election_results.csv")
    )
    polling_df = pd.read_csv(os.path.join(LOCAL_DATA_PATH, "monthly_polling_data.csv"))
    age_df = pd.read_csv(os.path.join(LOCAL_DATA_PATH, "census_data_age_group.csv"))
    living_df = pd.read_csv(
        os.path.join(LOCAL_DATA_PATH, "census_data_livingstatus.csv")
    )
    ethnicity_df = pd.read_csv(
        os.path.join(LOCAL_DATA_PATH, "census_data_ethnicity.csv")
    )

    # Step 3: Preprocess the DFs

    #### 3.1 ELECTION/POLLING DATA ####
    ## 3.1.1: Preprocess general election results
    preprocessed_election_df = preprocess_general_election_results(elections_df)
    ## 3.1.2: Preprocess Polling data
    preprocessed_polling_df = preprocess_polling_data(polling_df)
    ## 3.1.3: Merge election and polling data
    elections_polling_df = preprocessed_election_df.merge(
        preprocessed_polling_df, on="year", how="left"
    )

    #### 3.2 CENSUS DATA ####
    ## 3.2.1: Preprocess Age data
    preprocessed_age_df = preprocess_census_age(age_df)
    ## 3.2.1 Preprocess Living Status data
    preprocessed_living_df = preprocess_census_livingstatus(living_df)
    ## 3.2.2 Preprocess Enthicity
    preprocessed_ethnicity_df = preprocess_census_ethnicity(ethnicity_df)
    ## 3.2.3 Interpolate Census data
    interpolated_age_df = interpolate_data_frame(preprocessed_age_df, 2010, 2024)
    interpolated_living_df = interpolate_data_frame(preprocessed_living_df, 2010, 2024)
    interpolate_ethicity_df = interpolate_data_frame(
        preprocessed_ethnicity_df, 2010, 2024
    )
    ## 3.2.4 Merge Census data
    preprocessed_census_df = pd.merge(
        interpolated_age_df,
        interpolated_living_df,
        on=["constituency_id", "year", "constituency_name"],
        how="inner",
    ).merge(
        interpolate_ethicity_df,
        on=["constituency_id", "year", "constituency_name"],
        how="inner",
    )

    ### JOIN ALL THE DATAFRAMES TOGETHER ###
    preprocessed_final_df = pd.merge(
        preprocessed_census_df,
        elections_polling_df,
        on=["constituency_id", "year"],
        how="inner",
    )
    preprocessed_final_df.rename(
        columns={"constituency_name_x": "constituency_name"}, inplace=True
    )
    preprocessed_final_df.drop(columns=["constituency_name_y"], inplace=True)

    # Step 4: Save the preprocessed DF as CSV
    ## This is just for courtesy and to check data is correct, not beacuse is needed to train the model
    preprocessed_final_df.to_csv(
        os.path.join(LOCAL_DATA_PATH, "preprocessed_final_df.csv"), index=False
    )

    # Train the model

    # Evaluate the model

    print(
        f"""
          BRAVO, PREPROCESSED COMPLETED 🎉🎉🎉🎉🎉🎉🎉🎉
          The file has been saved here:
          {os.path.join(LOCAL_DATA_PATH, "preprocessed_final_df.csv")}
          """
    )

    # logging.info("Preprocessing completed")
    # logging.warning("Preprocessing completed")
    # logging.error("Preprocessing completed")
    return preprocessed_final_df


if __name__ == "__main__":
    preprocess()
