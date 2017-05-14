#!/usr/bin/env python
# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from twitter library
from twitter import *

# Rest of imports
from twkeyword import *
from twtweet import *
from twgraph import twGraph
import string
import re
import csv
from textblob import TextBlob
from difflib import SequenceMatcher

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '857833880157429760-RlbPRm15HjQnILgswmSxfFfjBd3u5vx'
ACCESS_SECRET = 'v9796ixcaFdWfbAjDPBH2NuZMXdV0kPRAS84qmgPud5cx'
CONSUMER_KEY = 'KdAnszTrQFCyQ95yw7vJMZd7K'
CONSUMER_SECRET = 'yUREO2rQ72WIM9hY2mwJU9unRdCFprtgVT8nx4y7lIeuojvlY8'


def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist

def getTweetSentiment(tweet):
    analysis = TextBlob(tweet)
    # print('Analyzing ' + tweet)
    # print('   Polarity Score: ' + str(analysis.sentiment.polarity))
    # print('   Subjectivity Score: ' + str(analysis.sentiment.polarity))
    return analysis.sentiment


# Get main twitter
t = Twitter(auth=OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET))


# Define variables for search
scope = 1
user = "BarackObama"  # scope = 1 search user timeline, max 3200 total tweets
#searchPhrase = '"Affordable Care Act" OR "Obamacare"' # scope = 2 search Twitter for popular results in the past 7 days
searchPhrase = '"American Health Care Act" OR "Trumpcare"' # scope = 2 search Twitter for popular results in the past 7 days

totalTweetsToExtract = 3200
if (scope == 1):
    tweetsPerCall = 200  # max 200 tweets per call for user timeline
else:
    tweetsPerCall = 100  # max 100 tweets per call for Twitter search

tweetLib = {}
keywordLib = {}
printable = set(string.printable)
wordCloudText = ""

# Load apostrophe words list from file
ApostropheWordsFile = open('ApostropheWords.txt', 'r')
ApostropheWords = ApostropheWordsFile.readlines()
ApostropheWords = [x.strip() for x in ApostropheWords]
ApostropheWordsFile.close()

# Load stop words list from file
stopWordsFile = open('StopWords.txt', 'r')
stopWords = stopWordsFile.readlines()
stopWords = [x.strip() for x in stopWords]
stopWordsFile.close()

# Retrieve tweets
lastMaxID = 0
for x in range(int(totalTweetsToExtract / tweetsPerCall)):
    if (scope == 1):
        if (lastMaxID == 0):
            # print('Requesting ' + str(tweetsPerCall) + ' tweets')
            tweetResults = t.statuses.user_timeline(screen_name=user, count=tweetsPerCall, include_rts="false")
        else:
            tweetResults = t.statuses.user_timeline(screen_name=user, count=tweetsPerCall, include_rts="false",
                                                    max_id=lastMaxID)
    elif (scope == 2):
        if (lastMaxID == 0):
            # print('Requesting ' + str(tweetsPerCall) + ' tweets')
            tweetResults = t.search.tweets(q=searchPhrase + "' -filter:retweets AND -filter:replies", count=tweetsPerCall, lang="en")['statuses']
        else:
            tweetResults = t.search.tweets(q=searchPhrase + "' -filter:retweets AND -filter:replies", count=tweetsPerCall, max_id=lastMaxID, lang="en")['statuses'] #result_type="popular",
    else:
        exit()  # not a Twitter nor a user search, placeholder for other searches
    print(json.dumps(tweetResults))

    # Process the result
    # print('Processing ' + str(len(tweetResults)) + ' tweets')
    for tweet in tweetResults:
        if (scope == 1) and (tweet['user']['screen_name'] != user):  # for user search, skip any tweets NOT from user
            continue

        if (lastMaxID == 0):
            lastMaxID = tweet['id'] - 1
        elif (tweet['id'] < lastMaxID):
            lastMaxID = tweet['id'] - 1

        # Extract text
        text = tweet['text']

        # Extract retweet count
        retweetCt = tweet['retweet_count']

        # Remove links
        containsHttp = ("http") in text
        text = re.sub(r"http\S+", "", text)

        # Retrieve tweet sentiment
        sentiScore = getTweetSentiment(text)

        # Populate the tweet class
        if (lastMaxID not in tweetLib):
            tweetClass = twTweet()
            tweetClass.id = tweet['id_str']
            tweetClass.retweetCount = tweet['retweet_count']
            tweetClass.userAcctAgeMonths = tweetClass.acctAge(tweet['user']['created_at'])
            tweetClass.userFollowersCt = tweet['user']['followers_count']
            tweetClass.sentiPolarity = sentiScore.polarity
            tweetClass.sentiSubjectivity = sentiScore.subjectivity
            tweetClass.createdTime = (tweetClass.convertTime(tweet['created_at'],tweet['user']['utc_offset']))[1]
            tweetClass.createdDay = (tweetClass.convertTime(tweet['created_at'],tweet['user']['utc_offset']))[0]
            tweetClass.textLength = len(text.lstrip(' ').rstrip(' '))
            tweetClass.wordCount = len(text.lstrip(' ').rstrip(' ').split(' '))
            tweetClass.linkpic = containsHttp
            tweetLib[lastMaxID] = tweetClass

        # Exclude common apostrophe words
        for apos in ApostropheWords:
            text = text.lower().replace(apos, "")

        # Remove punctuation
        text = text.translate(text.maketrans('[]&*,?!:;."()\'', '              '))  # Replace punctuation with space
        text = text.translate(text.maketrans('-', '0'))  # Remove hyphens

        # Remove unnecessary characters
        text = ' '.join(unique_list(text.split()))  # Remove duplicate keywords within one tweet
        text = ''.join([i for i in text if not i.isdigit()])  # Remove numbers
        text = ''.join([i if ord(i) < 128 else ' ' for i in text])  # Replace unicode with space

        # Process the keywords
        keywords = text.split(' ')

        for key in keywords:
            # Exclude common words
            if key.lower() in stopWords:
                continue

            if (key == ''):
                continue

            if (len(key) <= 2):
                continue

            if ("w/" in key):
                key = key.replace("w/", "  ").strip()

            # Add keyword to tweet class keyword list
            tweetLib[lastMaxID].addKeyword(key)

            if key not in keywordLib:
                keyClass = twKeyword(key)
                keywordLib[key] = keyClass
            else:
                keyClass = keywordLib.get(key)

            keyClass.addRetweet(retweetCt)
            keyClass.addSentiScore(sentiScore)


# Print the tweets and their attributes to CSV
if (scope == 1):
    csvfile1 = "outputs/" + "tweetsInfo" + user + "T.csv"
    csvfile2 = "outputs/" + "keywordInfo" + user + "T.csv"
elif (scope == 2):
    searchPhraseName = searchPhrase.replace('"','')
    csvfile1 = "outputs/" + "tweetsInfo" + searchPhraseName + "T.csv"
    csvfile2 = "outputs/" + "keywordInfo" + searchPhraseName + "T.csv"


with open(csvfile1, "w", newline='') as fp1:
    wr1 = csv.writer(fp1, delimiter=',')
    wr1.writerow(('ID', 'RetweetCt', 'Polarity', 'Subjectivity', 'CreatedTime', 'CreatedDay', 'TextLength', 'WordCt', 'AccountAgeMo', 'UserFollowersCt', 'Keywords', 'HasLinks'))
    for t in tweetLib.values():
        wr1.writerow(('"' + t.id + '"', t.retweetCount, t.sentiPolarity, t.sentiSubjectivity, t.createdTime, t.createdDay, t.textLength, t.wordCount, t.userAcctAgeMonths, t.userFollowersCt, t.keyWords, t.linkpic))

# Calculate retweet score
for x in keywordLib.values():
    x.calcAvg()
    x.calcMedian()
    # x.print()  # print the keywords and their key attributes


with open(csvfile2, "w", newline='') as fp2:
    wr2 = csv.writer(fp2, delimiter=',')
    wr2.writerow(('Name', 'Count', 'avgRetweet', 'medianRetweet', 'avgLogRetweet', 'medianLogRetweet', 'avgPolarSenti', 'avgSubjSenti'))
    for k in keywordLib.values():
        wr2.writerow((k.name, k.count, k.avgRetweet, k.medianRetweet, k.avgLogRetweet, k.medianLogRetweet, k.avgPolarSenti, k.avgSubjSenti))

graph = twGraph()

if (scope == 1):
    label = "@" + user
elif (scope == 2):
    label = "\"" + searchPhrase + "\""


# Histogram of Retweet Count
graph.histogram(csvfile1, label)

# Create text for word cloud
for wordCloudKey in keywordLib.values():
    wordCloudText += wordCloudKey.name + ":" + str(wordCloudKey.medianLogRetweet) + ":" + str(wordCloudKey.avgPolarSenti) + " "

graph.wordCloudGraph(wordCloudText, stopWords)

# Display graph 1 - Top Retweet Keywords by Retweet scores
graph.barGraph(keywordLib.values(), label)

# Display graph 2 - Top Retweet Keywords for each Sentiment category by Avg # of Retweets
graph.stackedBarGraphPolarity(keywordLib.values(), label)

# Display graph 3 - Top Retweet Keywords for each Sentiment category by Avg # of Retweets
graph.stackedBarGraphSubjectivity(keywordLib.values(), label)


