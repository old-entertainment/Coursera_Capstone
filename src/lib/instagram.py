#!/usr/bin/python3
"""Getting posts
   from Instagram in form of dataframe
   with help of https://www.instagram.com/explore/
   https://medium.com/@h4t0n/instagram-data-scraping-550c5f2fb6f1
   https://github.com/h4t0n/instagram-scraper/blob/master/spiders/hashtag.py"""

import re
import datetime as dt
import requests
import pandas as pd
from fake_useragent import UserAgent
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

SNT_CALC = SIA()
UA = UserAgent()


def json_path(json_object, path, default=None):
    """Return json element by path in format: node.subnode[idx].subnode
    If not found, return None.
    """
    path_list = re.split(r'\.|\[|\]', path)
    result = json_object
    for node in path_list:
        if result is None:
            break
        if node == '':
            continue
        if isinstance(result, dict) and node in result:
            result = result.get(node)
        elif re.match(r'\d+', node) and isinstance(result, list) and int(node) < len(result):
            result = result[int(node)]
        else:
            return default
    return result


def get_api_posts_df_instagram(query, results_limit=100):
    """Collect Instagram posts with selected filters and limitations.

    Params:
    - hashtag - instagram hashtag name
    - limit_posts_num - int, posts count limitations (default is 0, unlimited)


    Return DataFrame with columns:
    - Date - datetime
    - text - string


    """

    url_hash = 'https://www.instagram.com/explore/tags/%(hashtag)s/?__a=1'
    url_hash_cursor = 'https://www.instagram.com/explore/tags/%(hashtag)s/?__a=1&max_id=%(cursor)s'
    jpath_page_edges = 'graphql.hashtag.edge_hashtag_to_media.edges'
    jpath_page_hasnextpage = 'graphql.hashtag.edge_hashtag_to_media.page_info.has_next_page'
    jpath_page_cursor = 'graphql.hashtag.edge_hashtag_to_media.page_info.end_cursor'

    jpath_edge_taken = 'node.taken_at_timestamp'
    jpath_edge_text = 'node.edge_media_to_caption.edges[0].node.text'

    output = []

    with requests.session() as web_session:
        headers = {
            'accept': 'application/json',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'no-cache',
            'dnt': '1',
            'pragma': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': UA.google,
        }

        has_next_page = True
        page_num = 1
        empty_page = 0

        while has_next_page:
            page = web_session.get(url_hash %
                                   {'hashtag': query}, headers=headers)
            try:
                json_page = page.json()
            except ValueError as err:
                print('bad query is:', query)
                print(page.text)
                page = web_session.get(url_hash %
                                       {'hashtag': query}, headers=headers)
                json_page = page.json()
            
            edges = json_path(json_page, jpath_page_edges, [])
            empty_page += 1
            for edge in edges:
                post = {}
                taken = int(json_path(edge, jpath_edge_taken))
                post['Date'] = dt.datetime.fromtimestamp(taken)
                post['text'] = str(json_path(edge, jpath_edge_text))
                post['query'] = query

                output.append(post)

            has_next_page = json_path(json_page, jpath_page_hasnextpage)
            if has_next_page:
                cursor = json_path(json_page, jpath_page_cursor)
                url_hash = url_hash_cursor % {
                    'hashtag': query, 'cursor': cursor}

            page_num += 1

            if len(output) > results_limit:
                break
    if output:
        snt_posts_df = pd.DataFrame.from_records(output)
    else:
        snt_posts_df = pd.DataFrame(
            columns=['Date', 'text', 'query'])
    snt_posts_df.set_index('Date', inplace=True)

    snt_df = snt_posts_df['text'].apply(SNT_CALC.polarity_scores)

    res_df = pd.DataFrame.from_records(list(snt_df.values))
    res_df.index = snt_df.index
    merged_df = pd.concat([snt_posts_df, res_df], axis=1,
                          join_axes=[snt_posts_df.index])
    return merged_df


if __name__ == "__main__":
    QUERY = "btc"
    DF_OU = get_api_posts_df_instagram(QUERY)
    print(DF_OU.info())
    print(DF_OU.describe())
