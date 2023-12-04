from fastapi import FastAPI
from uk_election.main import load_model
from uk_election.ml_logic.model import (
    prep_new_data,
    model_predict,
)


app = FastAPI()
app.state.model = load_model()


@app.get("/")
def hello_world():
    return {"message": "Hello World!"}


@app.get("/predict")
def predict(
    con_poll: float = 0.25,
    lab_poll: float = 0.44,
    lib_poll: float = 0.1,
    oth_poll: float = 0.21,
):
    model, melted_df = app.state.model
    # Step 5: Prepare the new data for prediction
    X_new_encoded = prep_new_data(melted_df, (con_poll, lab_poll, lib_poll, oth_poll))
    # Step 6: Predict
    prediction = model_predict(model, X_new_encoded, melted_df).reset_index()

    return prediction.to_dict(orient="records")
