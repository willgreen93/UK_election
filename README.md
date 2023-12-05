# Forecasting the results of the next UK election

In this project, we use a machine learning model to forecast the results of the next UK election expected in 2024. Given the cencus for England and Wales is done separately to that of Scotland and Northern Ireland, we have restricted the scope of this work to England and Wales only.

We use data on demographics, polling data, and prior election results to train a model at the constituency level, to estimate the way each constituency would vote based on user-defined poll ratings prior to the next election. 

### Methods
Demographic data was taken from the UK census at the consituency level from 2011 and 2021. This gives us the proprtion of each constituency by:
- Age bucket (10 year buckets from 0-9 years to 80+)
- Broad ethnicity (White, Black, Asian, Mixed, Other)
- Living status (Home owner, private renter, social renter)

Historic election data was taken from the House of Commons Library. This gave the number of votes for each party in each previous general election, by constituency.

Polling data was taken from a source of aggregated polling data from 1943. This is available at https://www.markpack.org.uk/opinion-polls/.

Polling data was available at National Level only. This was transformed to constituency level data by weighting the national poll for each constituency by the proportion of votes for each party in the previous election against the national average for each party in the previous election.

Multiple machine learning models were fitted, including Ridge Regression, K Nearest Neighbours (KNN), Gradient Boosted Tree (XGB) and Support Vector Machine (SVC). All models were fitted using the scikit-learn package in R. In this work, we present the output of the XGB model. A grid search was conducted to determine best fitting parameters for n_estimators, learning_rate and max_tree_depth. 

The user interface was created using the streamlit package in Python. The user interface allows users to toggle pre-election poll to infer the impact on results at the consituency and national level.


