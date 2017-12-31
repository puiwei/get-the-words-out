#!/usr/bin/env python

import math
import statistics
import itertools

class twKeyword():
    def __init__(self, name):
        self.name = name
        self.count = 0
        #self.retweetSum = 0
        self.avgRetweet = 0.0
        self.avgLogRetweet = 0.0
        self.medianRetweet = 0.0
        self.medianLogRetweet = 0.0
        self.sentiPolarSum = 0
        self.avgPolarSenti = 0.0
        self.sentiSubjSum = 0
        self.avgSubjSenti = 0.0
        self.retweetHistory = []  # Store retweet ct for each tweet with keyword
        self.logRetweetHistory = []  # Store log(1 + retweet ct) for each tweet with keyword

    def calcAvg(self):
        if (self.count > 0):
            #self.avgRetweet = self.retweetSum / self.count
            self.avgRetweet = sum(self.retweetHistory)/self.count
            self.avgLogRetweet = sum(self.logRetweetHistory)/self.count
            self.avgPolarSenti = self.sentiPolarSum / self.count
            self.avgSubjSenti = self.sentiSubjSum / self.count

    def calcMedian(self):
        if (self.count > 0):
            self.medianRetweet = statistics.median(self.retweetHistory)
            self.medianLogRetweet = statistics.median(self.logRetweetHistory)
        
    def addRetweet(self, retweetCount):
        #self.retweetSum = self.retweetSum + retweetCount
        self.retweetHistory.append(retweetCount)
        self.logRetweetHistory.append(math.log10(1 + retweetCount))
        self.count = self.count + 1

    
    def addSentiScore(self, score):
        self.sentiPolarSum = self.sentiPolarSum + score.polarity
        self.sentiSubjSum = self.sentiSubjSum + score.subjectivity

    # Print the keyword and its key attributes
    def printkey(self):
        print('Key: ' + self.name + ' Count: ' + str(self.count) + ' RetweetSum: ' + str(self.retweetSum) + ' Average: ' + str(self.avgRetweet) + ' Median: ' + str(self.medianRetweet) + ' avgPolarSenti: ' + str(self.avgPolarSenti) + ' avgSubjSenti: ' + str(self.avgSubjSenti) + ' retweetHistory: ' + ', '.join(str(x) for x in self.retweetHistory))
        
        