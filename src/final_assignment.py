#!/usr/bin/env python3
"""Module with main data manipulation"""

import pandas as pd 
from lib import get_api_posts_df_instagram, DATASETS_DIR

df = pd.read_csv(DATASETS_DIR + 'foursquare_venues.csv')
df_with_rating = df[df['rating'] > 0]
print(df_with_rating.info())
print(df_with_rating.describe())
df_with_rating.to_csv(DATASETS_DIR + 'foursquare.csv')