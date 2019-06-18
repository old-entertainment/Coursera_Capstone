#!/usr/bin/env python3
"""Module with FourSquare API usage to get data"""

import os
import logging
import requests
import pandas as pd

LIMIT = 50
VERSION = "20180323"
CLIENT_ID = os.environ['FOURSQ_ID']
CLIENT_SECRET = os.environ['FOURSQ_SECRET']
HYDEPARK_LATITUDE = 51.5052
HYDEPARK_LONGTITUDE = -0.1582


def get_nearby_venues(latitudes, longitudes, radius=500):
    """Search venues near location"""

    venues_list = []

    # create the API request URL
    url_search = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&\
client_secret={}&v={}&ll={},{}&radius={}&limit={}'.format(
        CLIENT_ID,
        CLIENT_SECRET,
        VERSION,
        latitudes,
        longitudes,
        radius,
        LIMIT)

    print(requests.get(url_search).json()["response"])
    results = requests.get(url_search).json()["response"]["venues"]

    for venue in results:
        tmp_dict = {'name': venue['name'],
                    'id': venue['id'],
                    'latitide': venue['location']['lat'],
                    'longitude': venue['location']['lng'],
                    # 'postal_code': venue['location']['postalCode']
                    }
        rating = get_venue_rating(tmp_dict['id'])

        if isinstance(rating, float):
            tmp_dict['rating'] = rating
            venues_list.append(tmp_dict)

        print(tmp_dict)

    venue_df = pd.DataFrame(venues_list)

    return venue_df


def get_venue_rating(venue_id):
    """Venue details"""

    res_dict = {'rating': None, 'error': None}

    url_details = 'https://api.foursquare.com/v2/venues/{}?&client_id={}&\
client_secret={}&v={}'.format(
        venue_id,
        CLIENT_ID,
        CLIENT_SECRET,
        VERSION
    )

    results = requests.get(url_details).json()

    if results['meta']['code'] == 200:
        if 'rating' in results['response']['venue']:
            res_dict['rating'] = float(results['response']['venue']['rating'])
        else:
            res_dict['error'] = 'No rating for this venue'
            logging.info('foursquare : get_venue_rating : no rating for venue')
    else:
        res_dict['error'] = results
        logging.error('foursquare : get_venue_rating : %s', res_dict)

    # print(results['response']['venue'])
    # print('#'*100)

    return res_dict


if __name__ == "__main__":
    
    # logging.setLevel(logging.DEBUG)
    # res = get_nearby_venues(HYDEPARK_LATITUDE, HYDEPARK_LONGTITUDE)
    # # print(res)
    # for i in res:
    #     print(i)
    #     print('#'*100)

    # res = get_venue_rating('4b4dbf69f964a520b9d626e3')
    # print(res)

    venue_df_ou = get_nearby_venues(HYDEPARK_LATITUDE, HYDEPARK_LONGTITUDE)
    venue_df_ou.to_csv('./datasets/foursquare.csv')
