import altair as alt
from google.cloud import storage


url = "interface/data/uk-constituencies-2019-BBC.hexjson"
api_url = "https://ukelection-image-ne4yelgixa-no.a.run.app/predict"

parties = ["con", "lab", "lib", "oth"]
party_colours = ["blue", "red", "orange", "lightgrey"]
colours_obj = alt.Color(
    "winning_party:N", scale=alt.Scale(domain=parties, range=party_colours)
)
parties_full = [
    "Conservative Party",
    "Labor Party",
    "Liberal Democratic Party",
    "Other Parties",
]
