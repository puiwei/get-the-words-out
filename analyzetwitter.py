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
import os
#from packages.oldtweets.Exporter import main
from ediblepickle import checkpoint
import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import FuncTickFormatter, Range1d, LinearAxis
from math import pi
from statistics import median
import numpy
import time
import threading

ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_SECRET = os.environ['ACCESS_SECRET']
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']


#use a set if order doesn't matter
#use a dict if order does matter as access key is order(1)
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


def cleanupCache(fileKeyword):
    # go through and clean up old cache files
        path_in_str = 'tweetcache\\' + fileKeyword + '.tweet'
        if os.path.isfile(path_in_str):
            mtime = os.path.getmtime(path_in_str)
            last_modified_date = datetime.fromtimestamp(mtime)
            delta = datetime.now() - last_modified_date
            if delta.days > 7:
                os.remove(path_in_str)


@checkpoint(key=string.Template('{4}-{2}-{5}.tweet'), work_dir='tweetcache')
def retrieveTweets(api, scope, totalTweetsToExtract, tweetsPerCall, searchTerm, result_type='mixed'):
    # Get main twitter
    print("retrieve tweets: " + str(time.time()))

    t = Twitter(auth=OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET))

    tweetData = []
    if (api == 1):
        lastMaxID = 0
        for x in range(int(totalTweetsToExtract / tweetsPerCall)):
            if (scope == 1):
                if (lastMaxID == 0): tweetResults = t.statuses.user_timeline(screen_name=searchTerm, count=tweetsPerCall, include_rts="false", tweet_mode='extended')
                else:                tweetResults = t.statuses.user_timeline(screen_name=searchTerm, count=tweetsPerCall, include_rts="false", tweet_mode='extended', max_id=lastMaxID)
            elif (scope == 2):
                if (lastMaxID == 0): tweetResults = t.search.tweets(q=searchTerm + "' -filter:retweets AND -filter:replies", count=tweetsPerCall, lang="en", tweet_mode='extended')['statuses']
                else:                tweetResults = t.search.tweets(q=searchTerm + "' -filter:retweets AND -filter:replies", count=tweetsPerCall, max_id=lastMaxID, lang="en", tweet_mode='extended', result_type=result_type)['statuses']
            else:
                exit()  # not a Twitter nor a user search, placeholder for other searches

            # Find the last ID for continuation of search
            for tweet in tweetResults:
                if (lastMaxID == 0):
                    lastMaxID = tweet['id'] - 1
                elif (tweet['id'] < lastMaxID):
                    lastMaxID = tweet['id'] - 1

            tweetData.extend(tweetResults)
            #print(json.dumps(tweetResults))
            #print(threading.currentThread().getName(), 'Starting')
            #print(json.dumps(tweetResults))
    # Run https search
    else:
        if (scope == 1):
            params = '--username=' + searchTerm + ' --maxtweets=2000'
        else:
            params = '--querysearch=' + searchTerm + ' --maxtweets=2000 --since 2017-12-10 --until 2017-12-20'
        tweetData = main(params)

    return tweetData


def retrieve_day_of_week(data):
    dict = {'Sun': {'tweet_ct': [], 'retweet_ct': []},
            'Mon': {'tweet_ct': [], 'retweet_ct': []},
            'Tue': {'tweet_ct': [], 'retweet_ct': []},
            'Wed': {'tweet_ct': [], 'retweet_ct': []},
            'Thu': {'tweet_ct': [], 'retweet_ct': []},
            'Fri': {'tweet_ct': [], 'retweet_ct': []},
            'Sat': {'tweet_ct': [], 'retweet_ct': []},}
    df_input = {}
    bucket = {}

    for tweet in data:
        # Get day
        day = tweet['created_at'].split(" ")[0]
        parse = parsedate_tz(tweet['created_at'])
        date = str(parse[1]) + "/" + str(parse[2]) + "/" + str(parse[0])
        retweet = tweet['retweet_count']

        if day + " " + date in bucket:
            bucket[day + " " + date][0] += 1
            bucket[day + " " + date][1] += retweet
        else:
            bucket[day + " " + date] = [1, retweet]

    # Separate into day of the week bins
    for key, value in bucket.items():
        day = key.split(" ")[0]
        if day in dict:
            dict[day]['tweet_ct'].append(value[0])
            dict[day]['retweet_ct'].append(value[1])

    # Calculate
    df_input['day'] = [label for label, value in dict.items()]
    df_input['tweet_ct'] = [numpy.mean(dict[label]['tweet_ct']) for label, value in dict.items()]
    df_input['retweet_ct'] = []
    for label, value in dict.items():
        if value['tweet_ct']:
            df_input['retweet_ct'].append(sum(dict[label]['retweet_ct']) / sum(dict[label]['tweet_ct']))
        else:
            df_input['retweet_ct'].append(0)

    inds1 = numpy.where(numpy.isnan(df_input['tweet_ct']))
    inds2 = numpy.where(numpy.isnan(df_input['retweet_ct']))
    for x in inds1[0]:
        df_input['tweet_ct'][x] = 0
    for x in inds2[0]:
        df_input['retweet_ct'][x] = 0
    # Create data frame
    df = pd.DataFrame(df_input)

    return df


def retrieve_hour_of_day(data):
    dict = {'0000': {'tweet_ct': [], 'retweet_ct': []},
            '0100': {'tweet_ct': [], 'retweet_ct': []},
            '0200': {'tweet_ct': [], 'retweet_ct': []},
            '0300': {'tweet_ct': [], 'retweet_ct': []},
            '0400': {'tweet_ct': [], 'retweet_ct': []},
            '0500': {'tweet_ct': [], 'retweet_ct': []},
            '0600': {'tweet_ct': [], 'retweet_ct': []},
            '0700': {'tweet_ct': [], 'retweet_ct': []},
            '0800': {'tweet_ct': [], 'retweet_ct': []},
            '0900': {'tweet_ct': [], 'retweet_ct': []},
            '1000': {'tweet_ct': [], 'retweet_ct': []},
            '1100': {'tweet_ct': [], 'retweet_ct': []},
            '1200': {'tweet_ct': [], 'retweet_ct': []},
            '1300': {'tweet_ct': [], 'retweet_ct': []},
            '1400': {'tweet_ct': [], 'retweet_ct': []},
            '1500': {'tweet_ct': [], 'retweet_ct': []},
            '1600': {'tweet_ct': [], 'retweet_ct': []},
            '1700': {'tweet_ct': [], 'retweet_ct': []},
            '1800': {'tweet_ct': [], 'retweet_ct': []},
            '1900': {'tweet_ct': [], 'retweet_ct': []},
            '2000': {'tweet_ct': [], 'retweet_ct': []},
            '2100': {'tweet_ct': [], 'retweet_ct': []},
            '2200': {'tweet_ct': [], 'retweet_ct': []},
            '2300': {'tweet_ct': [], 'retweet_ct': []},
            }
    df_input = {}
    bucket = {}

    for tweet in data:
        # Get hour
        parse = parsedate_tz(tweet['created_at'])
        timestamp = mktime_tz(parse)
        s = datetime.fromtimestamp(timestamp)
        date = s.strftime("%m/%d/%Y")
        hour = s.strftime("%H")
        hour += '0' * (4 - len(hour))
        retweet = tweet['retweet_count']

        if hour + " " + date in bucket:
            bucket[hour + " " + date][0] += 1
            bucket[hour + " " + date][1] += retweet
        else:
            bucket[hour + " " + date] = [1, retweet]

    # Separate into hour of the day bins
    for key, value in bucket.items():
        hour = key.split(" ")[0]
        if hour in dict:
            dict[hour]['tweet_ct'].append(value[0])
            dict[hour]['retweet_ct'].append(value[1])

    # Calculate
    df_input['hour'] = [label for label, value in dict.items()]
    df_input['tweet_ct'] = [numpy.mean(dict[label]['tweet_ct']) for label, value in dict.items()]

    df_input['retweet_ct'] = []
    for label, value in dict.items():
        if value['tweet_ct']:
            df_input['retweet_ct'].append(sum(dict[label]['retweet_ct']) / sum(dict[label]['tweet_ct']))
        else:
            df_input['retweet_ct'].append(0)

    inds1 = numpy.where(numpy.isnan(df_input['tweet_ct']))
    inds2 = numpy.where(numpy.isnan(df_input['retweet_ct']))
    for x in inds1[0]:
        df_input['tweet_ct'][x] = 0
    for x in inds2[0]:
        df_input['retweet_ct'][x] = 0

    # Adjust empty values to 1 so log does not fail
    #for label, value in dict.items():
    #    if not dict[label]['retweet_ct']:
    #        dict[label]['retweet_ct'].append(1)
    #df_input['retweet_ct'] = [median(numpy.log(dict[label]['retweet_ct'])) for label, value in dict.items()]

    # Create data frame
    df = pd.DataFrame(df_input)

    return df


@checkpoint(key=string.Template('{0}.bokeh'), work_dir='tweetcache')
def generate_bokeh(user):
    data = retrieveTweets(1, 1, 2000, 200, user, 'mixed')

    # retrieve data frame
    df = retrieve_day_of_week(data)
    if not df.empty:
        # Create plot
        tickers = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        max_range = df['tweet_ct'].max() * 1.2
        p1 = figure(plot_width=750, plot_height=500, title='Day of Week Activity for @' + data[0]['user']['screen_name'], y_range=(0, max_range))

        # Y Axis
        p1.yaxis.axis_label = "Average Tweet Count"
        p1.yaxis.axis_label_text_color = 'blue'
        p1.yaxis.axis_label_text_font_style = 'bold'

        # X Axis
        p1.xaxis.axis_label = "Day of Week"
        p1.xaxis[0].ticker = [0, 1, 2, 3, 4, 5, 6]
        p1.xaxis.axis_label_text_font_style = 'bold'
        p1.xaxis.formatter = FuncTickFormatter(code=""" var labels = %s; return labels[tick]; """ % tickers)

        # Y Axis Right
        max_range_rt = df['retweet_ct'].max() * 1.2
        p1.extra_y_ranges = {"p1": Range1d(start=0, end=max_range_rt)}
        p1.add_layout(LinearAxis(y_range_name="p1", axis_label="Retweet Rate", axis_label_text_color='red', axis_label_text_font_style='bold'), 'right')

        # Draw
        for day, row in df.iterrows():
            p1.vbar(tickers.index(row['day']), .4, row['tweet_ct'], legend='Average Tweet Count')

        days_index = [tickers.index(x) for x in df['day'].tolist()]
        retweets_index = df['retweet_ct'].tolist()
        p1.line(days_index, retweets_index, line_width=2, y_range_name="p1", color='red', legend='Retweet Rate')
        p1.circle(days_index, retweets_index, fill_alpha=1, fill_color="white", size=6, y_range_name="p1", color='red', legend='Retweet Rate')

        # Legend
        p1.legend.location = 'top_center'
        p1.legend.border_line_width = 1
        p1.legend.border_line_color = "gray"
        p1.legend.click_policy = "hide"
        p1.legend.label_text_font_size = "8pt"
        p1.legend.spacing = 1
        p1.legend.padding = 5
        p1.legend.margin = 0

    df2 = retrieve_hour_of_day(data)
    if not df2.empty:
        # Create plot
        tickers = dict = ['0000', '0100', '0200', '0300', '0400', '0500', '0600', '0700', '0800', '0900', '1000',
                          '1100', '1200', '1300', '1400', '1500', '1600', '1700', '1800', '1900', '2000', '2100',
                          '2200', '2300']
        max_range = df2['tweet_ct'].max() * 1.2
        p2 = figure(plot_width=1000, plot_height=500, title='Time of Day Activity for @' + data[0]['user']['screen_name'], y_range=(0, max_range))

        # Y Axis
        p2.yaxis.axis_label = "Average Tweet Count"
        p2.yaxis.axis_label_text_color = 'blue'
        p2.yaxis.axis_label_text_font_style = 'bold'

        # X Axis
        p2.xaxis.axis_label = "Time of Day"
        p2.xaxis.axis_label_text_font_style = 'bold'
        p2.xaxis.major_label_orientation = pi / 2
        p2.xaxis[0].ticker = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
        p2.xaxis.formatter = FuncTickFormatter(code=""" var labels = %s; return labels[tick]; """ % tickers)

        # Y Axis Right
        max_range_rt = df2['retweet_ct'].max() * 1.2
        p2.extra_y_ranges = {"p2": Range1d(start=0, end=max_range_rt)}
        p2.add_layout(LinearAxis(y_range_name="p2", axis_label="Retweet Rate", axis_label_text_color='red', axis_label_text_font_style='bold'), 'right')

        # Draw
        for day, row in df2.iterrows():
            p2.vbar(tickers.index(row['hour']), .4, row['tweet_ct'], legend='Average Tweet Count')

        days_index = [tickers.index(x) for x in df2['hour'].tolist()]
        retweets_index = df2['retweet_ct'].tolist()
        p2.line(days_index, retweets_index, line_width=2, y_range_name="p2", color='red', legend='Retweet Rate')
        p2.circle(days_index, retweets_index, fill_alpha=1, fill_color="white", size=6, y_range_name="p2", color='red', legend='Retweet Rate')

        # Legend
        p2.legend.location = 'top_center'
        p2.legend.border_line_width = 1
        p2.legend.border_line_color = "gray"
        p2.legend.click_policy = "hide"
        p2.legend.label_text_font_size = "8pt"
        p2.legend.spacing = 1
        p2.legend.padding = 5
        p2.legend.margin = 0

    script1, div1 = components(p1)
    script2, div2 = components(p2)
    return script1, div1, script2, div2


def analyze(user_input, scope, lock):
    # cleanupCache(user_input)

    with lock:
        tweetList = []
        keywordLib = {}
        printable = set(string.printable)
        wordCloudText = ""
        api = 1  # 1 = twitter api, 2 = http search
        result_type = 'mixed'

        #can move out as a separate function
        if (scope == 1):
            totalTweetsToExtract = 2000  # max 3200 total tweets for user timeline search, and max 180 API calls per 15 mins
            tweetsPerCall = 200  # max 200 tweets per call for user timeline
            searchTerm = user_input

        else:
            totalTweetsToExtract = 1000  # max 180 API calls per 15 mins, so can max extract 18K tweets per 15 mins for twitter search
            tweetsPerCall = 100  # max 100 tweets per call for Twitter search
            searchTerm = user_input

        # Load apostrophe words list from file
        # Can also make .py file with a python list, in a global folder, import it
        with open('ApostropheWords.txt', 'r') as ApostropheWordsFile:
            ApostropheWords = ApostropheWordsFile.readlines()
        ApostropheWords = [x.strip() for x in ApostropheWords]

        # Can redo this simliarly as apostropke word
        # Load stop words list from file
        stopWordsFile = open('StopWords.txt', 'r')
        stopWords = stopWordsFile.readlines()
        stopWords = [x.strip() for x in stopWords]
        stopWordsFile.close()

    tweetData = retrieveTweets(api, scope, totalTweetsToExtract, tweetsPerCall, searchTerm, result_type)

    # Process the result
    # print('Processing ' + str(len(tweetResults)) + ' tweets')
    '''with open('outputs/json_raw', 'w') as f:
        f.write(json.dumps(tweetData))
    f.close()'''

    print("process tweets: " + str(time.time()))

    with lock:
        for tweet in tweetData:
            if (scope == 1) and (tweet['user']['screen_name'].lower() != searchTerm.lower()):  # for user search, skip any tweets NOT from user
                continue

            # Extract
            text = tweet['full_text']
            retweetCt = tweet['retweet_count']

            # Remove links
            text = re.sub(r"http\S+", "", text)

            # Retrieve tweet sentiment
            sentiScore = getTweetSentiment(text)

            # Populate the tweet class
            tweetClass = twTweet()
            tweetClass.id = tweet['id_str']
            tweetClass.retweetCount = tweet['retweet_count']
            tweetClass.userAcctAgeMonths = tweetClass.acctAge(tweet['user']['created_at'])
            tweetClass.userFollowersCt = tweet['user']['followers_count']
            tweetClass.sentiPolarity = sentiScore.polarity
            tweetClass.sentiSubjectivity = sentiScore.subjectivity
            tweetClass.createdTime = (tweetClass.convertTime(tweet['created_at'], tweet['user']['utc_offset']))[1]
            tweetClass.createdDay = (tweetClass.convertTime(tweet['created_at'], tweet['user']['utc_offset']))[0]
            tweetClass.textLength = len(text.lstrip(' ').rstrip(' '))
            tweetClass.wordCount = len(text.lstrip(' ').rstrip(' ').split(' '))
            tweetClass.linkpic = "http" in text
            tweetList.append(tweetClass)

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

            #Look at CountVectorizor, can pass in StopWords, a matrix
            #in scikit-learn.featureextraction
            #ML idea: bag of words - understand sentiment - often used as a classifier
            #given a tweet, can train a classifer given a topic/name, and this model can predict how likely it gets retweet

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
                tweetClass.addKeyword(key)

                if key not in keywordLib:
                    keyClass = twKeyword(key)
                    keywordLib[key] = keyClass
                else:
                    keyClass = keywordLib.get(key)

                keyClass.addRetweet(retweetCt)
                keyClass.addSentiScore(sentiScore)

    # Print the tweets and their attributes to CSV
    #print("write to csv: " + str(time.time()))

    '''if (scope == 1):
        csvfile1 = "outputs/" + "tweetsInfo" + searchTerm + "T.csv"
        csvfile2 = "outputs/" + "keywordInfo" + searchTerm + "T.csv"
    elif (scope == 2):
        searchPhraseName = searchTerm.replace('"','')
        csvfile1 = "outputs/" + "tweetsInfo" + searchPhraseName + "T.csv"
        csvfile2 = "outputs/" + "keywordInfo" + searchPhraseName + "T.csv"'''


    '''with open(csvfile1, "w", newline='') as fp1:
        wr1 = csv.writer(fp1, delimiter=',')
        wr1.writerow(('ID', 'RetweetCt', 'Polarity', 'Subjectivity', 'CreatedTime', 'CreatedDay', 'TextLength', 'WordCt', 'AccountAgeMo', 'UserFollowersCt', 'Keywords', 'HasLinks'))
        for t in tweetList:
            wr1.writerow(('"' + t.id + '"', t.retweetCount, t.sentiPolarity, t.sentiSubjectivity, t.createdTime, t.createdDay, t.textLength, t.wordCount, t.userAcctAgeMonths, t.userFollowersCt, t.keyWords, t.linkpic))'''

    # Calculate retweet score
    with lock:
        for x in keywordLib.values():
            x.calcAvg()
            x.calcMedian()
            # x.print()  # print the keywords and their key attributes


    '''with open(csvfile2, "w", newline='') as fp2:
        wr2 = csv.writer(fp2, delimiter=',')
        wr2.writerow(('Name', 'Count', 'avgRetweet', 'medianRetweet', 'avgLogRetweet', 'medianLogRetweet', 'avgPolarSenti', 'avgSubjSenti'))
        for k in keywordLib.values():
            wr2.writerow((k.name, k.count, k.avgRetweet, k.medianRetweet, k.avgLogRetweet, k.medianLogRetweet, k.avgPolarSenti, k.avgSubjSenti))'''

    graph = twGraph()

    # Histogram of Retweet Count
    #graph.histogram(csvfile1, label)

    # Create text for word cloud
    print("WordCloud: " + str(time.time()))

    with lock:
        retweetKeywordLib = {}
        for graphKey, graphValue in keywordLib.items():
            if graphValue.medianLogRetweet > 0:
                retweetKeywordLib[graphKey] = graphValue

        for wordCloudKey in retweetKeywordLib.values():
            wordCloudText += wordCloudKey.name + ":" + str(wordCloudKey.medianLogRetweet) + ":" + str(wordCloudKey.avgPolarSenti) + " "

        script = graph.wordCloudGraph(wordCloudText, stopWords, searchTerm, totalTweetsToExtract)

    print("Done in AnalyzeTwitter: " + str(time.time()))

    # Display graph 1 - Top Retweet Keywords by Retweet scores
    #graph.barGraph(retweetKeywordLib.values(), label)

    # Display graph 2 - Top Retweet Keywords for each Sentiment category by Avg # of Retweets
    #graph.stackedBarGraphPolarity(retweetKeywordLib.values(), label)

    # Display graph 3 - Top Retweet Keywords for each Sentiment category by Avg # of Retweets
    #graph.stackedBarGraphSubjectivity(retweetKeywordLib.values(), label)

    # Return HTML and JavaScript to app.py, for embedding in index.html
    return script
