#!/usr/bin/env python3
"""Module with FourSquare API usage to get data"""

import os
import datetime
import json
import time
import requests
import pandas as pd

# Get all Venue IDs for venues within the bounding box.
cfg = {
    'client_id': os.environ['FOURSQ_ID'],
    'client_secret': os.environ['FOURSQ_SECRET'],

    'left_bound': -122.516441,
    'bottom_bound': 37.702072,
    'right_bound': -122.37276,
    'top_bound': 37.811818,

    # Number of API calls to /venue endpoint will be grid_size^2
    'grid_size': 5

}


def get_delta(lower, upper, length):
    return (upper - lower)/length


lat_delta = get_delta(cfg['top_bound'], cfg['bottom_bound'], cfg['grid_size'])
long_delta = get_delta(cfg['left_bound'], cfg['right_bound'], cfg['grid_size'])

search_params = {
    'client_id': cfg['client_id'],
    'client_secret': cfg['client_secret'],
    'intent': 'browse',
    'limit': 50,
    'v': '20180218'
}

venue_ids = set()
search_count = 0

for lat in range(cfg['grid_size']):
    for long in range(cfg['grid_size']):
        ne_lat = cfg['top_bound'] + lat * lat_delta
        ne_long = cfg['left_bound'] + (long+1) * long_delta

        search_params.update({'ne': '{},{}'.format(ne_lat, ne_long),
                              'sw': '{},{}'.format(ne_lat + lat_delta,
                                                   ne_long - long_delta)})

        r = requests.get('https://api.foursquare.com/v2/venues/search',
                         params=search_params)

        if 'venues' in r.json()['response']:
            venues = r.json()['response']['venues']

            for venue in venues:
                venue_ids.add(venue['id'])

        search_count += 1

        if search_count % 1000 == 0:
            print('{} Searched: {}'.format(search_count,
                                           datetime.datetime.now()))

        # gets fussy when more than 5000 requests/hr
        if search_count % 5000 == 0:
            time.sleep(60*60)

        time.sleep(0.1)

print('{} Unique Venues Scraped: {}.'.format(
    len(venue_ids), datetime.datetime.now()))

# Get and process the data for each unique Venue.

venue_params = {
    'client_id': cfg['client_id'],
    'client_secret': cfg['client_secret'],
    'v': '20180218'
}

venue_ids_list = list(venue_ids)   # cannot iterate a set, so must coerce list

results_list = []

for venue_id in venue_ids_list:
    r = requests.get(
        'https://api.foursquare.com/v2/venues/{}'.format(venue_id),
        params=venue_params)
    
    try:

        if 'venue' in r.json()['response']:
            venue = r.json()['response']['venue']
            tmp_dict = {}

            tmp_dict['id'] = venue_id
            tmp_dict['name'] = venue.get('name', '')
            tmp_dict['lat'] = venue.get('location', {}).get('lat', '')
            tmp_dict['long'] = venue.get('location', {}).get('lng', '')
            tmp_dict['num_checkins'] = venue.get('stats', {}).get('checkinsCount', '')
            tmp_dict['num_likes'] = venue.get('likes', {}).get('count', '')
            tmp_dict['rating'] = venue.get('rating', '')
            tmp_dict['num_ratings'] = venue.get('ratingSignals', '')
            tmp_dict['price'] = venue.get('price', {}).get('tier')
            tmp_dict['url_venue'] = venue.get('url', '')
            tmp_dict['url_foursquare'] = venue.get('shortUrl', '')

            

            results_list.append(tmp_dict)
            print(len(results_list))

            
        else:
            print(r.text)
            print('#'*100)
        

        if len(results_list) % 100 == 0:
            print('{} Retrieved: {}'.format(len(results_list),
                                            datetime.datetime.now()))
            print(results_list[-10:])

    except json.decoder.JSONDecodeError:
        print('Json fail')
        print(r.text)
        print('#'*100)

    time.sleep(0.1)

df = pd.DataFrame(results_list)

df.to_csv('fsq.csv')