#!/usr/bin/env python
# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from twitter library
from twitter import *

# Rest of imports
from twkeyword import twKeyword
from twgraph import twGraph
import string
import itertools
from textblob import TextBlob

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '857833880157429760-RlbPRm15HjQnILgswmSxfFfjBd3u5vx'
ACCESS_SECRET = 'v9796ixcaFdWfbAjDPBH2NuZMXdV0kPRAS84qmgPud5cx'
CONSUMER_KEY = 'KdAnszTrQFCyQ95yw7vJMZd7K'
CONSUMER_SECRET = 'yUREO2rQ72WIM9hY2mwJU9unRdCFprtgVT8nx4y7lIeuojvlY8'

def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist

def topKeywords(l, number):
    # For those tied with average retweet, the original order of the keyword is used
    # in determining what gets displayed first
    ulist = sorted(l, key=lambda twKeyword: twKeyword.avgRetweet, reverse=True)
    return itertools.islice(ulist, number)

def getTweetSentiment(tweet):
    analysis = TextBlob(tweet)
    #print('Analyzing ' + tweet)
    #print('   Score: ' + str(analysis.sentiment.polarity))
    return analysis.sentiment.polarity
    
# Get main twitter
t = Twitter(auth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET))

# Define variables
user = "BarackObama"
totalTweetsToExtract = 1000
tweetsPerCall = 200
topKeywordNumber = 10
keywordLib = {}
printable = set(string.printable)

# Load stop words list from file
stopWordsFile = open('StopWords.txt', 'r')
stopWords = stopWordsFile.readlines()
stopWords = [x.strip() for x in stopWords]
stopWordsFile.close()

# Retrieve tweets
lastMaxID = 0
for x in range(int(totalTweetsToExtract / tweetsPerCall)):
    if (lastMaxID == 0):
        #print('Requesting ' + str(tweetsPerCall) + ' tweets')
        tweetResults = t.statuses.user_timeline(screen_name=user, count=tweetsPerCall, include_rts="false")
    else:
        tweetResults = t.statuses.user_timeline(screen_name=user, count=tweetsPerCall, include_rts="false", max_id=lastMaxID)
    #print(json.dumps(tweetResults))
    
    # Process the result
    #print('Processing ' + str(len(tweetResults)) + ' tweets')
    for tweet in tweetResults:
        if (tweet['user']['screen_name'] != user):
            continue
            
        lastMaxID = tweet['id']
        
        # Extract text
        text = tweet['text']
        #if (tweet.get('quoted_status')):
        #    text = text + " " + tweet['quoted_status']['text']
        
        # Extract retweet count
        retweetCt = tweet['retweet_count']

        # Remove punctuation
        text = text.translate(text.maketrans(',?!:;."()\'-', '00000000000'))
        
        # Remove unnecessary characters
        text = ' '.join(unique_list(text.split()))                  # Remove duplicate keywords within one tweet
        text = ''.join([i for i in text if not i.isdigit()])        # Remove numbers
        text = ''.join(i for i in text if ord(i) < 128)             # Remove unicode

        # Retrieve tweet sentiment
        sentiScore = getTweetSentiment(text)
        
        # Process the keywords
        keywords = text.split(' ')
        
        for key in keywords:
            # Exclude common words
            if key.lower() in stopWords:
                continue

            # Remove links
            if ('http' in key):
                continue
            
            if (key == ''):
                continue
            
            if (key not in keywordLib):
                keyClass = twKeyword(key)
                keywordLib[key] = keyClass
            else:
                keyClass = keywordLib.get(key)
                
            keyClass.addRetweet(retweetCt)
            keyClass.addSentiScore(sentiScore)

# Calculate average retweets
for x in keywordLib.values():
    x.calcAvgs()
    #x.print()
    
# Retrieve the top keywords list
topKeys = topKeywords(keywordLib.values(), topKeywordNumber)

#for y in topKeys:
    #print(y.name + ': ' + str(y.avgRetweet) + ' ' + str(y.avgSenti))

graph = twGraph()

# Display graph 1 - Top Retweet Keywords by Avg # of Retweets
graph.barGraph(topKeys, user)

# Display graph 2 - Top Retweet Keywords for each Sentiment category by Avg # of Retweets
graph.stackedBarGraph(keywordLib.values(), user)













