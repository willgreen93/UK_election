import altair as alt

parties = ["conservative", "labour", "liberal_democrats", "other_parties"]
party_colours = ["#F78DA7", "blue", "orange", "lightgrey"]
colours_obj = alt.Color(
    "incumbent_party:N", scale=alt.Scale(domain=parties, range=party_colours)
)
