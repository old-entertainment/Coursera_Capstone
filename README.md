# Coursera_Capstone

Project idea is to compare data about venues from different social networks. There is rating of venues at Foursquare, which is average mark from visitors of this venue, also we may take posts from platforms like Twitter, Instagram, etc., and perform sentiment analysis of posts about featured venues. Out of this we will have actual values to compare and see if there is correlation between those social platforms and if people at specific social platform are more "kind" to venues for some reason. Finally we can draw a map where we show not only Foursquare data, but sentiment analysis estimation to give more information to user if place is really good.

## Data

Data was gathered from three sources: Foursquare, Twitter, Reddit.

- Fousquare
  - dataframe with 100 venues locations and ratings
  - every venue is one row
  - 3 columns: latitude, longtitude, rating

- Twitter
  - dataframe with 1K posts for every venue
  - 100K rows for every post about venue
  - columns: venue, text, sentiment 

- Instagram
  - dataframe with 1K posts for every venue
  - 100K rows for every post about venue
  - columns: venue, text, sentiment 
