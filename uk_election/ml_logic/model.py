import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV


def make_melted_df(preprocessed_data):
    """
    This function takes the preprocessed data and returns a melted dataframe with the votes for each party as a column
    """
    preprocessed_data.drop(preprocessed_data.columns[0], axis=1, inplace=True)

    preprocessed_data["con_pre_ge_adjusted"] = (
        preprocessed_data["con_share_prev"]
        / preprocessed_data["mean_con_share_ge"]
        * preprocessed_data["con_pre_ge_poll"]
    )
    preprocessed_data["lab_pre_ge_adjusted"] = (
        preprocessed_data["lab_share_prev"]
        / preprocessed_data["mean_lab_share_ge"]
        * preprocessed_data["lab_pre_ge_poll"]
    )
    preprocessed_data["lib_pre_ge_adjusted"] = (
        preprocessed_data["lib_share_prev"]
        / preprocessed_data["mean_lib_share_ge"]
        * preprocessed_data["lib_pre_ge_poll"]
    )
    preprocessed_data["oth_pre_ge_adjusted"] = (
        preprocessed_data["oth_share_prev"]
        / preprocessed_data["mean_oth_share_ge"]
        * preprocessed_data["oth_pre_ge_poll"]
    )

    melted_df = pd.melt(
        preprocessed_data,
        id_vars=[
            "constituency_id",
            "year",
            "Private_renters",
            "Social_renters",  #'Home_owners',
            "0-9",
            "10-19",
            "20-29",
            "30-39",
            "40-49",
            "50-59",
            "60-69",
            "70-79",  #'80+',
            "White",
            "Asian",
            "Black",
            "Mixed",  #'Other',
            "con_pre_ge_adjusted",
            "lab_pre_ge_adjusted",
            "lib_pre_ge_adjusted",
            "oth_pre_ge_adjusted",
            "con_share_prev",
            "mean_con_share_ge",
            "lab_share_prev",
            "mean_lab_share_ge",
            "lib_share_prev",
            "mean_lib_share_ge",
            "oth_share_prev",
            "mean_oth_share_ge",
        ],
        value_vars=["con_votes", "lab_votes", "lib_votes", "oth_votes"],
        var_name="party",
        value_name="votes",
    )

    return melted_df


def prep_data(melted_df):
    """
    This function takes the melted dataframe and returns the X and y dataframes for the model
    """
    columns_to_drop = [
        "year",
        "constituency_id",
        "votes",
        "con_share_prev",
        "mean_con_share_ge",
        "lab_share_prev",
        "mean_lab_share_ge",
        "lib_share_prev",
        "mean_lib_share_ge",
        "oth_share_prev",
        "mean_oth_share_ge",
    ]

    X_old = melted_df[melted_df["year"] != 2024].drop(columns=columns_to_drop)
    y_old = melted_df[["votes"]][melted_df["year"] != 2024]

    column_to_encode = "party"
    one_hot_encoded = pd.get_dummies(X_old[column_to_encode], prefix=column_to_encode)
    X_old_encoded = pd.concat([X_old, one_hot_encoded], axis=1)
    X_old_encoded = X_old_encoded.drop(column_to_encode, axis=1)

    return X_old_encoded, y_old


def train_model(X_old_encoded, y_old):
    """
    This function takes the X and y dataframes and returns the optimised trained model
    """
    gb_regressor = GradientBoostingRegressor()

    # Already picked the best ones, if you want to run the grid search remove the comments
    param_grid = {
        "n_estimators": [60],  # , 100, 140],
        "learning_rate": [0.1],  # , 0.5, 1],
        "max_depth": [8],
    }  # [6, 7, 8]}

    grid_search_tree = GridSearchCV(
        estimator=gb_regressor,
        param_grid=param_grid,
        scoring="neg_mean_squared_error",
        cv=5,
    )

    grid_search_tree.fit(X_old_encoded, y_old)

    best_model_gb = grid_search_tree.best_estimator_

    print("Best Score:", grid_search_tree.best_score_)

    return best_model_gb


def prep_new_data(melted_df, con_lab_lib_oth_support):
    """
    This function takes the melted dataframe and the polls for each party and returns the X dataframe for the new data
    """
    columns_to_drop = [
        "year",
        "constituency_id",
        "votes",
        "con_share_prev",
        "mean_con_share_ge",
        "lab_share_prev",
        "mean_lab_share_ge",
        "lib_share_prev",
        "mean_lib_share_ge",
        "oth_share_prev",
        "mean_oth_share_ge",
    ]

    X_new = melted_df[melted_df["year"] == 2024]

    X_new["con_pre_ge_adjusted"] = (
        X_new["con_share_prev"]
        / X_new["mean_con_share_ge"]
        * con_lab_lib_oth_support[0]
    )
    X_new["lab_pre_ge_adjusted"] = (
        X_new["lab_share_prev"]
        / X_new["mean_lab_share_ge"]
        * con_lab_lib_oth_support[1]
    )
    X_new["lib_pre_ge_adjusted"] = (
        X_new["lib_share_prev"]
        / X_new["mean_lib_share_ge"]
        * con_lab_lib_oth_support[2]
    )
    X_new["oth_pre_ge_adjusted"] = (
        X_new["oth_share_prev"]
        / X_new["mean_oth_share_ge"]
        * con_lab_lib_oth_support[3]
    )

    X_new.drop(columns=columns_to_drop, inplace=True)

    column_to_encode = "party"

    one_hot_encoded2 = pd.get_dummies(X_new[column_to_encode], prefix=column_to_encode)
    X_new_encoded = pd.concat([X_new, one_hot_encoded2], axis=1).drop(
        column_to_encode, axis=1
    )

    return X_new_encoded


def model_predict(model, X_new_encoded, melted_df):
    """
    This function takes the model and the X dataframe for the new data and returns the predicted results
    """
    X_new = melted_df[melted_df["year"] == 2024]
    y_new = model.predict(X_new_encoded)
    y_new = y_new.round(0).astype(int)

    X_new_predicted = X_new
    X_new_predicted["votes"] = y_new
    X_new_predicted["constituency_id"] = melted_df[melted_df["year"] == 2024][
        "constituency_id"
    ]

    X_new_min = X_new_predicted[["constituency_id", "party", "votes"]]
    output = X_new_min.pivot(index="constituency_id", columns="party", values="votes")

    output["winning_party"] = output.idxmax(axis=1)
    output["winning_party"] = output["winning_party"].str.replace("_votes", "")

    return output
