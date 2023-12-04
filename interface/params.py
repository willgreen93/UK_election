import altair as alt
from google.cloud import storage

# bucket_name = "uk_election_model"
# url = "https://storage.googleapis.com/uk_election_model/uk-constituencies-2019-BBC.hexjson"
# data_source = "https://storage.googleapis.com/uk_election_model/elec_data_2019.csv"

url = "interface/data/uk-constituencies-2019-BBC.hexjson"
api_url = "https://ukelection-image-ne4yelgixa-no.a.run.app/predict"

parties = ["con", "lab", "lib", "oth"]
party_colours = ["blue", "red", "orange", "lightgrey"]
colours_obj = alt.Color(
    "winning_party:N", scale=alt.Scale(domain=parties, range=party_colours)
)
