# Get The Words Out (GTWO)
GTWO is a marketing tool that helps users enhance brand recognition and social media exposure, by optimzing tweets to generate more retweets.

## Web App URL
[https://get-the-words-out.herokuapp.com/](https://get-the-words-out.herokuapp.com/)

## How It Works

### Data Extraction & Processing
GTWO uses a Python Twitter API to extract tweets from a user's timeline and search results of a search term. The tweets are then processed for meta-information like the user's account attributes, tweet attributes, and sentiment analysis scores calculated using the TextBlob library. Then, the tweets are parsed to remove punctuations, special characters, numbers, links, duplicate words, and stop words, and then split into individual keywords.

### Machine Learning Model
The retweet prediction model consists of the feature union of 

Feature Union of Keywords Model and Meta-Information Model
Linear Support Vector Regression

Keywords Model:
- One-hot encoding
- Term frequency
- Stop Words
- Ridge

Meta-Information Model:
- User account attributes
- New tweet attributes
- Linear Support Vector Regression



