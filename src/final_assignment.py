#!/usr/bin/env python3
"""Module with main data manipulation
P.S. Can be converted to .ipynb"""

# %% [markdown]
# Comparing FourSquare ratings with social sentiments

# %%
# all the imports
import pandas as pd 
from src import get_api_posts_df_instagram, DATASETS_DIR, PROJECT_DIR
# %%
# create dataset with existing ratings
df = pd.read_csv(DATASETS_DIR + 'foursquare_venues.csv')
df_with_rating = df[df['rating'] > 0]
print(df_with_rating.info())
print(df_with_rating.describe())
df_with_rating.to_csv(DATASETS_DIR + 'foursquare.csv')


# %%
tmp_df = get_api_posts_df_instagram("Burgers")
tmp_df.to_csv(DATASETS_DIR + "instagram_posts.csv")
# %%
# get sentiment for every venue
df_venues = pd.read_csv(DATASETS_DIR + 'foursquare.csv')
for index, row in df_venues.iterrows():
    snt_df = get_api_posts_df_instagram(index['name'])

#%%
