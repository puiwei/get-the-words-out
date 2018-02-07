# Get The Words Out (GTWO)
GTWO is a marketing tool that helps users enhance brand recognition and social media exposure, by optimzing tweets to generate more retweets.

## Web App URL
[https://get-the-words-out.herokuapp.com/](https://get-the-words-out.herokuapp.com/)

## How It Works

### Data Extraction & Processing
- Python Twitter API
- Parse keywords
  - punctuations
  - special characters
  - links
  - Stop Words

### Machine Learning Model
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



