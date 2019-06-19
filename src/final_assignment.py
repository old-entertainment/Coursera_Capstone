#!/usr/bin/env python3
"""Module with main data manipulation
P.S. Can be converted to .ipynb"""

# %% [markdown]
# Comparing FourSquare ratings with social sentiments

# %%
# all the imports
import pandas as pd 
from src import get_api_posts_df_instagram, DATASETS_DIR, PROJECT_DIR, prepare_query
# %%
# create dataset with existing ratings
df = pd.read_csv(DATASETS_DIR + 'foursquare_venues.csv')
df_with_rating = df[df['rating'] > 0]
print(df_with_rating.info())
print(df_with_rating.describe())
df_with_rating.to_csv(DATASETS_DIR + 'foursquare.csv')


# %%
tmp_df = get_api_posts_df_instagram("bjburgers")
# print(tmp_df)
tmp_df.to_csv(DATASETS_DIR + "instagram_posts.csv")
# %%
# get sentiment for every venue
df_venues = pd.read_csv(DATASETS_DIR + 'foursquare.csv')
df_venues['query'] = df_venues['name'].apply(prepare_query)
print(df_venues['query'])
df_venues.to_csv(DATASETS_DIR + 'foursquare.csv')
# for index, row in df_venues.iterrows():
#     snt_df = get_api_posts_df_instagram(index['name'])

#%%
df_venues = pd.read_csv(DATASETS_DIR + 'foursquare.csv', index_col=False)

df_venues['query'] = df_venues['query'].apply(lambda s: s[:9])
df_venues.to_csv(DATASETS_DIR + 'foursquare.csv', index=False)
#%%
df_venues = pd.read_csv(DATASETS_DIR + 'foursquare.csv', index_col=False)
df_posts = pd.read_csv(DATASETS_DIR + "instagram_posts.csv", index_col='Date')
snt_list = []
for index, row in df_venues.iterrows():
    try:
        tmp_snt_df = get_api_posts_df_instagram(row['query'])
    # print(type(tmp_snt_df))
    except:
        tmp_snt_df = pd.DataFrame()
    if not tmp_snt_df.empty:
        snt_list.append(tmp_snt_df['compound'].mean())
    else:
        snt_list.append(None)
    df_posts = df_posts.append(tmp_snt_df)
df_posts.to_csv(DATASETS_DIR + "instagram_posts.csv")
df_venues['inst_snt'] = snt_list
df_venues.to_csv(DATASETS_DIR + 'res.csv', index=False)
#%%
df_res = pd.read_csv(DATASETS_DIR + "res.csv", index_col=False)
print(df_res.describe())

#%%
