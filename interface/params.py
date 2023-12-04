import altair as alt
from google.cloud import storage

bucket_name = "uk_election_model"
url = "https://storage.googleapis.com/uk_election_model/uk-constituencies-2019-BBC.hexjson"
data_source = "https://storage.googleapis.com/uk_election_model/elec_data_2019.csv"

# url = "data/uk-constituencies-2019-BBC.hexjson"
# data_source = "data/elec_data_2019.csv"

parties = ["conservative", "labour", "liberal_democrats", "other_parties"]
party_colours = ["#F78DA7", "blue", "orange", "lightgrey"]
colours_obj = alt.Color(
    "incumbent_party:N", scale=alt.Scale(domain=parties, range=party_colours)
)
