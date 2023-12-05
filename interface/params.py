import altair as alt

url = "uk-constituencies-2019-BBC.hexjson"
data_source = "elec_data_2019.csv"

parties = ["conservative", "labour", "liberal_democrats", "other_parties"]
party_colours = ["#F78DA7", "blue", "orange", "lightgrey"]
colours_obj = alt.Color(
    "incumbent_party:N", scale=alt.Scale(domain=parties, range=party_colours)
)
