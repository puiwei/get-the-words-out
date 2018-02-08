# Get The Words Out (GTWO)
GTWO is a marketing tool that helps users enhance brand recognition and social media exposure, by optimzing tweets to generate more retweets.

## Web App URL
[https://get-the-words-out.herokuapp.com/](https://get-the-words-out.herokuapp.com/)

## How It Works

### Data Extraction & Processing
This app uses a Python Twitter API to extract tweets from a user's timeline and search results of a search term. The tweets are then processed for meta-information like the user account attributes, tweet attributes, and sentiment analysis scores calculated using the TextBlob library. Then, the tweets are parsed to remove punctuations, special characters, numbers, links, duplicate words, and stop words, and then split into individual keywords.

The WordCloud visualization from "Get Ideas" are generated from a modified Python WordCloud library, with the size of each keyword based on their associated log-median retweets, and the color of each keyword based on their sentiment polarity score (range from shades of red to purple to blue).

### Machine Learning Model
The Retweet Prediction Model is comprised of a feature union of the Keywords Model and the Meta-Information Model, fitted with linear support vector regression. This model is trained with 900,000 tweets that are downloaded from the Twitter Search API results for the Top 10 most common English words (i.e. "the", "be", "to", etc) as a proxy for random tweets.

The Keywords Model is constructed by doing one-hot encoding based on term frequency of parsed keywords in the tweets, and then fitting with linear ridge regression.

The Meta-Information Model involves user account attributes (i.e. followers count, number of past tweets) and tweet attributes (i.e. tweet length, whether there are links or pictures, sentiment polarity score, sentiment subjectivity score), fitted with linear support vector regression.



