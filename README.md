# Coursera_Capstone

Project idea is to compare data about venues from different social networks. There is rating of venues at Foursquare, which is average mark from visitors of this venue, also we may take posts from platforms like Twitter, Instagram, etc., and perform sentiment analysis of posts about featured venues. Out of this we will have actual values to compare and see if there is correlation between those social platforms and if people at specific social platform are more "kind" to venues for some reason. Finally we can draw a map where we show not only Foursquare data, but sentiment analysis estimation to give more information to user if place is really good.

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
  - dataframe with 100 venues locations and ratings
  - every venue is one row
  - 3 columns: venue, latitude, longtitude, rating, twitter_sentiment, instagram_sentiment

- Twitter
  - dataframe with 100 posts for every venue
  - 100K rows for every post about venue
  - columns: venue, text, sentiment

- Instagram
  - dataframe with 100 posts for every venue
  - 100K rows for every post about venue
  - columns: venue, text, sentiment

Detailed columns description

- venue: (str) - name of place in FourSquare
- text: (str) - post text from Twitter or Instagram about specific venue
- latitude: (float) - the angular distance of a place north or south of the earth's equator
- longtitude: (float) - the angular distance of a place east or west of the Greenwich meridian
- rating: (float) - FourSquares average mark for venue
- sentiment: (float) - value for an attitude towards venue


## Results

Correlation of Instagram sentiment vs Foursquare rating 

- Pearson: 0.03
- Kendall: 0.59
- Spearman: 0.54

![Alt text](./media/map.jpg?raw=true "Interactive Map")

![Alt text](./media/graph.jpg?raw=true "Rating vs Sentiment")