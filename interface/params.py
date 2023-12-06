import altair as alt
from google.cloud import storage


url = "https://storage.googleapis.com/uk_election_model/uk-constituencies-2019-BBC.hexjson"
api_url = "https://ukelection-image-ne4yelgixa-no.a.run.app/predict"
extra_cols = "https://storage.googleapis.com/uk_election_model/Scotland_NI_results.csv"

parties = ["con", "lab", "lib", "oth", "snp", "dup", "sf", "sdlp", "alliance"]
party_colours = [
    "#0087DC",
    "#dc143c",
    "#FAA61A",
    "#005B54",
    "#FDF38E",
    "#D46A4C",
    "#326760",
    "#2AA82C",
    "#F6CB2F",
]
colours_obj = alt.Color(
    "winning_party:N", scale=alt.Scale(domain=parties, range=party_colours)
)
parties_full = [
    "Conservative Party",
    "Labour Party",
    "Liberal Democratic Party",
    "Other Parties",
]
