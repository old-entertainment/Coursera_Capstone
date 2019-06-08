#!/usr/bin/env python3
"""Module with all data manipulations
   P.S. Can be converted to .ipynb"""
# %% [markdown]
# Segmenting and Clustering Neighborhoods in Toronto

# %%
# all the imports
import pandas as pd
import folium
from geopy.geocoders import Nominatim 

# %% [markdown]
## Scrapping the table with pandas
# %%
tables = pd.read_html('https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M')
df = tables[0]
df = df[df.Borough != 'Not assigned']
df.drop_duplicates(inplace=True)
print(df)

# %% [markdown]
## Convert table to proper format
#%%
series = df.groupby(['Postcode','Borough'])['Neighbourhood'].apply(lambda x: ", ".join(x.astype(str)))
postal_df = series.reset_index()
print(postal_df.head(10))

#%%
print(postal_df.shape)


# %% [markdown]
## Add latitude longtitude data
#%%
lat_long = pd.read_csv('datasets/Geospatial_Coordinates.csv')
lat_long.rename(columns={'Postal Code': 'Postcode'}, inplace=True)
print(lat_long)
#%%
df_merged = postal_df.merge(lat_long, how='left', on='Postcode')
df_merged = df_merged[['PostalCode', 'Borough', 'Neighborhood', 'Latitude', 'Longtitude']]
print(df_merged.head(10))


# %% [markdown]
## Draw a map of Toronto
#%%
address = 'Toronto'
geolocator = Nominatim()
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The geograpical coordinate of Toronto are {}, {}.'.format(latitude, longitude))

#%%
# create map of Manhattan using latitude and longitude values
map_toronto = folium.Map(location=[latitude, longitude], zoom_start=11)

# add markers to map
for lat, lng, label in zip(df_merged['Latitude'], df_merged['Longitude'], df_merged['Neighborhood']):
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_toronto)  
    
map_toronto