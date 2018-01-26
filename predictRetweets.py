#!/usr/bin/env python
from textblob import TextBlob
from twitter import *
import os
from datetime import datetime
from packages.twittercache.twitter_process import TwitterProcess
from packages.twittercache.twitter_db import TwitterDB
import pandas as pd
from generate_model import model


def predictRT(new_user, new_tweet):
    twp = TwitterProcess()

    sentiment = getTweetSentiment(new_tweet)
    user_info = getUserInfo(new_user)
    if user_info:
        d = {}
        d['tweet_id'] = '000000000000000001'
        d['tweet_search_term'] = 'predict'
        d['tweet_retweet_ct'] = ''
        d['tweet_text'] = new_tweet
        d['user_followers_ct'] = user_info['followers_count']
        d['user_friends_ct'] = user_info['friends_count']
        d['user_favorites_ct'] = user_info['favourites_count']
        d['user_statuses_ct'] = user_info['statuses_count']
        d['user_created_at'] = user_info['created_at']
        d['tweet_created_at'] = str(datetime.now())
        d['user_id'] = user_info['id_str']
        d['user_name'] = user_info['screen_name']
        tweet_process = twp.process_keywords([(d['tweet_id'], d['tweet_text'])])[0]
        d['tweet_keywords'] = tweet_process[1]
        d['tweet_length'] = tweet_process[2]
        d['polarity'] = tweet_process[3]
        d['subjectivity'] = tweet_process[4]
        d['tweet_word_ct'] = tweet_process[5]
        d['tweet_has_links'] = tweet_process[6]

        # Create data frame
        df = pd.DataFrame([d])
        df = df[['tweet_id', 'tweet_search_term', 'tweet_retweet_ct', 'tweet_text', 'user_followers_ct', 'user_friends_ct',
                 'user_favorites_ct', 'user_statuses_ct', 'user_created_at', 'tweet_created_at', 'user_id', 'user_name',
                 'tweet_keywords', 'tweet_length', 'polarity', 'subjectivity', 'tweet_word_ct', 'tweet_has_links']]

        # Call the modal and pass in df
        return str(model(df))
    return 'Need Valid Twitter Username'

def getUserInfo(user):
    ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
    ACCESS_SECRET = os.environ['ACCESS_SECRET']
    CONSUMER_KEY = os.environ['CONSUMER_KEY']
    CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
    t = Twitter(auth=OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET))
    max_tweets = 1000
    # Fetch # tweets from user

    tweetResults = t.statuses.user_timeline(screen_name=user, count=1, include_rts="false", tweet_mode='extended')
    if len(tweetResults) > 0:
        return tweetResults[0]['user']

    return None

def getTweetSentiment(tweet):
    analysis = TextBlob(tweet)
    return analysis.sentiment
