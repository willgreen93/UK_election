import pandas as pd
import os
from uk_election.params import *
from uk_election.data.google import load_data_from_gcp
from uk_election.preprocessing.preprocessing import (
    preprocess_general_election_results,
    preprocess_polling_data,
    preprocess_census_age,
    preprocess_census_ethnicity,
    preprocess_census_livingstatus,
    interpolate_data_frame,
)
from uk_election.ml_logic.model import (
    make_melted_df,
    prep_data,
    train_model,
    prep_new_data,
    model_predict,
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

    print(
        f"""
          Preprocessed completed
          For courtesy, we saved the file locally at:
          {os.path.join(LOCAL_DATA_PATH, "preprocessed_final_df.csv")}
          """
    )

    # logging.info("Preprocessing completed")
    # logging.warning("Preprocessing completed")
    # logging.error("Preprocessing completed")

    return preprocessed_final_df


def main():
    # Step 1: Preprocess the data
    preprocessed_df = preprocess()
    # Step 2: Reorient the DF so votes for each party become rows
    melted_df = make_melted_df(preprocessed_df)
    # Step 3: Prepare the data for the model
    X_old_encoded, y_old = prep_data(melted_df)
    # Step 4: Train the model
    model = train_model(X_old_encoded, y_old)

    # Step 5: Prepare the new data for prediction
    X_new_encoded = prep_new_data(melted_df, (0.25, 0.44, 0.1, 0.21))
    # Step 6: Predict
    prediction = model_predict(model, X_new_encoded, melted_df)

    # HURRAY! 🎉🎉🎉🎉🎉🎉🎉🎉
    print(
        f"""
          PREDICTED 🎉🎉🎉🎉🎉🎉🎉🎉 This is a sample of the prediction:
          {prediction.head()}
          """
    )


def load_model():
    preprocessed_df = preprocess()
    # Step 2: Reorient the DF so votes for each party become rows
    melted_df = make_melted_df(preprocessed_df)
    # Step 3: Prepare the data for the model
    X_old_encoded, y_old = prep_data(melted_df)
    # Step 4: Train the model
    model = train_model(X_old_encoded, y_old)
    return model, melted_df


if __name__ == "__main__":
    main()
