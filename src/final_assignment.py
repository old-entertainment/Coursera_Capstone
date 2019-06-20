#!/usr/bin/env python3
"""Module with main data manipulation
P.S. Can be converted to .ipynb"""

# %% [markdown]
# Comparing FourSquare ratings with social sentiments

# %%
# all the imports
import random
import pandas as pd 
import matplotlib
matplotlib.use('TkAgg')  # specific only for mac bug graph plot
import matplotlib.pyplot as plt
%matplotlib inline
from src import get_api_posts_df_instagram, DATASETS_DIR, PROJECT_DIR, prepare_query
# %%
# create dataset with existing ratings
df = pd.read_csv(DATASETS_DIR + 'foursquare_venues.csv')
df_with_rating = df[df['rating'] > 0]
print(df_with_rating.info())
print(df_with_rating.describe())
df_with_rating.to_csv(DATASETS_DIR + 'foursquare.csv')


# %%
# remove unnecessary characters from name to form proper query
df_venues = pd.read_csv(DATASETS_DIR + 'foursquare.csv')
df_venues['query'] = df_venues['name'].apply(prepare_query)
print(df_venues['query'])
df_venues.to_csv(DATASETS_DIR + 'foursquare.csv')


#%%
# making query shorter for instagram api
df_venues = pd.read_csv(DATASETS_DIR + 'foursquare.csv', index_col=False)
df_venues['query'] = df_venues['query'].apply(lambda s: s[:9])
df_venues.to_csv(DATASETS_DIR + 'foursquare.csv', index=False)
#%%
# get posts and average sentiments for venues
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
# plot sentiments and rating
df_final = pd.read_csv(DATASETS_DIR + 'result.csv', index_col=False)


color_list = ['#0000FF', '#01DF01', '#FF0000',
              '#BB12BE', '#CBC81B', '#00FFFF']
matplotlib.rcParams.update(matplotlib.rcParamsDefault)
style_list = ['dark_background', 'ggplot']
matplotlib.pyplot.style.use(random.choice(style_list))
figure = matplotlib.pyplot.figure(tight_layout=False)
matplotlib.pyplot.legend(loc="best", fancybox=True, framealpha=0.1)

ax = matplotlib.pyplot.subplot2grid((8, 1), (0, 0), rowspan=4, colspan=1)
ax2 = matplotlib.pyplot.subplot2grid((8, 1), (5, 0), rowspan=3, colspan=1)

ax.plot(df_final['name'].index.values, df_final['inst_snt'].values,
        color_list[0], label='instagram sentiment')

matplotlib.pyplot.title("Rating vs sentiment")
ax.set_ylabel('Sentiment')
ax2.plot(df_final['name'].values, df_final['rating'].values,
        color_list[1], label='foursquare_rating')

ax2.set_ylabel('Rating')
matplotlib.pyplot.xlabel('Name')
matplotlib.pyplot.ylabel('Rating')

ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(5))
ax2.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(5))

plt.show()

#%%
