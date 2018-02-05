#!/usr/bin/env python
from textblob import TextBlob
from twitter import *
import os
import string
from packages.twittercache.twitter_process import TwitterProcess
import pandas as pd
from generate_model import model
from ediblepickle import checkpoint
import statistics

def getRetweetInfo(data):
    tw_list = []
    #top = 0
    #top_text = None
    for x in data:
        #if x['retweet_count'] > top:
        #    top = x['retweet_count']
        #    top_text = x['full_text']
        tw_list.append(x['retweet_count'])

    return statistics.median(tw_list), round(statistics.mean(tw_list),1)



def predictRT(new_user, new_tweet):
    twp = TwitterProcess()

    sentiment = getTweetSentiment(new_tweet)
    user_info = getUserInfo(new_user, 2000)
    #avgRetweet, top, top_text = getRetweetInfo(user_info)
    medRetweet, avgRetweet = getRetweetInfo(user_info)

    if user_info:
        d = {}
        # d['tweet_id'] = '000000000000000001'
        # d['tweet_search_term'] = 'predict'
        d['tweet_retweet_ct'] = ''
        # d['tweet_text'] = new_tweet
        d['user_followers_ct'] = user_info[0]['user']['followers_count']
        # d['user_friends_ct'] = user_info['friends_count']
        # d['user_favorites_ct'] = user_info['favourites_count']
        d['user_statuses_ct'] = user_info[0]['user']['statuses_count']
        # d['user_created_at'] = user_info['created_at']
        # d['tweet_created_at'] = str(datetime.now())
        # d['user_id'] = user_info['id_str']
        # d['user_name'] = user_info['screen_name']
        # tweet_process = twp.process_keywords([(d['tweet_id'], d['tweet_text'])])[0]
        tweet_process = twp.process_keywords([('000000000000000001', new_tweet)])[0]
        d['tweet_keywords'] = tweet_process[1]
        d['tweet_length'] = tweet_process[2]
        d['polarity'] = tweet_process[3]
        d['subjectivity'] = tweet_process[4]
        d['tweet_word_ct'] = tweet_process[5]
        d['tweet_has_links'] = tweet_process[6]

        # Create data frame
        df = pd.DataFrame([d])
        df = df[['tweet_retweet_ct', 'user_followers_ct', 'user_statuses_ct', 'tweet_keywords', 'tweet_length', 'polarity', 'subjectivity', 'tweet_word_ct', 'tweet_has_links']]

        # Call the modal and pass in df
        return str(model(df)), medRetweet, avgRetweet
    return 'Need Valid Twitter Username', 0, 0, 0

@checkpoint(key=string.Template('{0}-{1}-mixed.tweet'), work_dir='tweetcache')
def getUserInfo(user, totalTweetsToExtract = 2000):
    ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
    ACCESS_SECRET = os.environ['ACCESS_SECRET']
    CONSUMER_KEY = os.environ['CONSUMER_KEY']
    CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
    t = Twitter(auth=OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET))
    tweetResults = []
    lastMaxID = 0

    # Fetch # tweets from user
    for x in range(int(totalTweetsToExtract / 200)):
        if (lastMaxID == 0):
            tweets = t.statuses.user_timeline(screen_name=user, count=200, include_rts="false", tweet_mode='extended')
        else:
            tweets = t.statuses.user_timeline(screen_name=user, count=200, include_rts="false", tweet_mode='extended', max_id=lastMaxID)

        for tweet in tweets:
            if (lastMaxID == 0):
                lastMaxID = tweet['id'] - 1
            elif (tweet['id'] < lastMaxID):
                lastMaxID = tweet['id'] - 1

        tweetResults.extend(tweets)

    if len(tweetResults) > 0:
        return tweetResults

    return None

def getTweetSentiment(tweet):
    analysis = TextBlob(tweet)
    return analysis.sentiment
