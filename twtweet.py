#!/usr/bin/env python

import time
from datetime import datetime
from email.utils import parsedate_tz, mktime_tz

class twTweet():
    def __init__(self):
        self.id = ''
        self.retweetCount = 0
        self.sentiPolarity = None
        self.sentiSubjectivity = None
        self.createdTime = None
        self.createdDay = None
        self.textLength = 0  # length of tweet without links
        self.wordCount = 0  # number of words in tweet without links
        self.userAcctAgeMonths = 0  # user account age in months
        self.userFollowersCt = None
        self.keyWords = []  # List of keywords from this tweet
        self.linkpic = None  # True/False that this tweet includes a picture or a link

    def addKeyword(self, key):
        self.keyWords.append(key)

    # Convert the tweet created_at timestamp to local time of day and day of week
    def convertTime(self, createdAt, utc_offset):
        timestamp = mktime_tz(parsedate_tz(createdAt))
        if (utc_offset is not None):
            timestamp = timestamp + utc_offset
        s = datetime.fromtimestamp(timestamp)
        day = s.strftime("%a")
        time = s.strftime("%H:%M")
        return [day, time]

    def acctAge(self, createdAt):
        # Calculate age of accounts (months)
        now = datetime.now()
        user_created = time.strptime(createdAt, "%a %b %d %H:%M:%S +0000 %Y")
        monthsNow = (now.year * 12) + now.month
        monthsUser = (user_created.tm_year * 12) + user_created.tm_mon
        monthsDiff = monthsNow - monthsUser
        return monthsDiff


