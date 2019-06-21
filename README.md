# Coursera_Capstone

## Introduction

Project idea is to compare data about venues from different social networks. There is rating of venues at Foursquare, which is average mark from visitors of this venue, also we may take posts from Instagram and perform sentiment analysis of posts about featured venues. Out of this we will have actual values to compare and see if there is correlation between those social platforms and if people at specific social platform are more "kind" to venues for some reason. Finally we can draw a map where we show not only Foursquare data, but sentiment analysis estimation to give more information to user if place is really good.

## Install

```bash
git clone git@github.com:old-entertainment/Coursera_Capstone.git
cd Coursera_Capstone
virtualenv -p /usr/bin/python3.7 cou_env
source ./cou_env/bin/activate
pip install -r requirements.txt
```

## Data

Data was gathered from three sources: Foursquare, Twitter, Reddit.

- Fousquare

  - dataframe with venues locations and ratings
  - every venue is one row
  - columns: venue, latitude, longtitude, rating, instagram_sentiment

- Instagram

  - dataframe with posts for every venue
  - every venue is one post
  - columns: Date, compound, neg, neu, pos, query, text

- Result

  - dataframe with all information merged together
  - every venue is one row
  - columns: id, name, categories, lat, long, num_checkins, 
             num_likes, price, rating, num_ratings, 
             url_venue, url_foursquare,query, inst_snt

Detailed columns description

- venue: (str) - name of place in FourSquare
- text: (str) - post text from Twitter or Instagram about specific venue
- latitude: (float) - the angular distance of a place north or south of the earth's equator
- longtitude: (float) - the angular distance of a place east or west of the Greenwich meridian
- rating: (float) - FourSquares average mark for venue
- sentiment: (float) - value for an attitude towards venue

## Methodology 

section which represents the main component of the report where you discuss and describe any exploratory data analysis that you did, any inferential statistical testing that you performed, and what machine learnings were used and why.


## Results

Correlation of Instagram sentiment vs Foursquare rating 

- Pearson: 0.03
- Kendall: 0.59
- Spearman: 0.54

San Francisco interactive map with Instagram sentiment and Foursquare ratings for every venue
embedded in popup labels. Can be plotted with corresponding cell from final_assignment.py.
![Alt text](./media/map.jpg?raw=true "Interactive Map")

Graph with Instagram sentiment and Foursquare ratings for every venue. Plotted in order to
figure out visually if there is a dependency between ratings and sentiment.
![Alt text](./media/graph.jpg?raw=true "Rating vs Sentiment")

## Discussion



## Conclusion