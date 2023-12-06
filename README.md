# TL;DR
<ins>Check our app [here](https://uk-elec.streamlit.app/), and forecast 2024 UK election results!</ins>



# Forecasting the results of the next UK election

In this project, we use a machine learning model to forecast the results of the next UK election expected in 2024. Given the census for England and Wales is done separately to that of Scotland and Northern Ireland, we have restricted the scope of this work to England and Wales only.

We use data on demographics, polling data, and prior election results to train a model at the constituency[^1] level, to estimate the way each constituency would vote based on user-defined poll ratings prior to the next election. 
[^1]: A constituency is a geographical area that elects a representative to serve in the Parliament.

## Methods

### Demographic data
Demographic data was taken from the UK census (source House of Commons, [link](https://commonslibrary.parliament.uk/topic/home-affairs/communities/demography/census/)) at the consituency level from 2011 and 2021. This gives us the proportion of each constituency by:
- Age bucket (10 year buckets from 0-9 years to 80+)
- Broad ethnicity (White, Black, Asian, Mixed, Other)
- Living status (Home owner, private renter, social renter)

Due to nature of census data, they are collected every 10 years. We interpolated the data for misisng years (i.e. 2015, 2017, 2024) using a linear interpolation function.

### General election results data
Historic general election data was taken from the House of Commons Library ([link](https://commonslibrary.parliament.uk/research-briefings/cbp-8647/)). This gave the number of votes for each party in each previous general election, by constituency.

### Polling data
Polling data was taken from a source of aggregated polling data from 1943 ([link](https://www.markpack.org.uk/opinion-polls/)).

Polling data was available at National Level only. This was transformed to constituency level data by weighting the national poll for each constituency by the proportion of votes for each party in the previous election against the national average for each party in the previous election.

### Machine learning models
Multiple machine learning models were fitted, including Ridge Regression, K Nearest Neighbours (KNN), Gradient Boosted Tree (XGB) and Support Vector Machine (SVC). All models were fitted using the scikit-learn package in R. In this work, we present the output of the XGB model. A grid search was conducted to determine best fitting parameters for n_estimators, learning_rate and max_tree_depth. 


### Interface
The user interface was created using the streamlit package in Python. The user interface allows users to toggle pre-election poll to infer the impact on results at the consituency and national level.
You can test the interface [here](https://uk-elec.streamlit.app/).


