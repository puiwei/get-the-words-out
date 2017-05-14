#!/usr/bin/env python
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import itertools
import pandas as pd
import math
from PIL import Image
from wordcloud import WordCloud, STOPWORDS

class twGraph():

    def topSentiAvg(self, list, number, polarsubj):
        # For those tied with average retweet, the original order of the keyword is used in determining what gets displayed first
        if (polarsubj == 1):  # polarity
            ulist = sorted(list, key=lambda twKeyword: twKeyword.avgPolarSenti, reverse=True)
            ulist = itertools.islice(ulist, number)
            ulist = sorted(ulist, key=lambda twKeyword: twKeyword.avgPolarSenti, reverse=True)

        elif (polarsubj == 2):  # subjectivity
            ulist = sorted(list, key=lambda twKeyword: twKeyword.avgSubjSenti, reverse=True)
            ulist = itertools.islice(ulist, number)
            ulist = sorted(ulist, key=lambda twKeyword: twKeyword.avgSubjSenti, reverse=True)

        return ulist

    def barGraphAvgRetweet(self, keywordValues, title, ax):
        # Retrieve the top keywords list
        ulist = sorted(keywordValues, key=lambda twKeyword: twKeyword.avgRetweet, reverse=True)
        topKeys = itertools.islice(ulist, 10)

        # Retrieve keyword list
        nameList = []
        avgRtw = []
        maxAvg = 0
        for key in topKeys:
            nameList.append(key.name)
            avgRtw.append(key.avgRetweet)
            if (maxAvg < key.avgRetweet):
                maxAvg = key.avgRetweet

        y_pos = np.arange(len(nameList))
        ax.bar(y_pos, avgRtw, align='center', alpha=0.5)
        ax.set_xticks(y_pos)
        ax.set_xticklabels(nameList, size=6)
        ax.set_ylim([0, int(maxAvg * 1.1)])
        ax.set_ylabel('Avg # of Retweets', fontsize=14)
        ax.set_xlabel('Top 10 Keywords', fontsize=14)
        ax.set_title('Top Retweet Keywords for ' + title, fontsize=16)

    def barGraphMedRetweet(self, keywordValues, title, ax):
        # Retrieve the top keywords list
        ulist = sorted(keywordValues, key=lambda twKeyword: twKeyword.medianRetweet, reverse=True)
        topKeys = itertools.islice(ulist, 10)

        # Retrieve keyword list
        nameList = []
        avgRtw = []
        maxAvg = 0
        for key in topKeys:
            nameList.append(key.name)
            avgRtw.append(key.medianRetweet)
            if (maxAvg < key.medianRetweet):
                maxAvg = key.medianRetweet

        y_pos = np.arange(len(nameList))
        ax.bar(y_pos, avgRtw, align='center', alpha=0.5)
        ax.set_xticks(y_pos)
        ax.set_xticklabels(nameList, size=6)
        ax.set_ylim([0, int(maxAvg * 1.1)])
        ax.set_ylabel('Median # of Retweets', fontsize=14)
        ax.set_xlabel('Top 10 Keywords', fontsize=14)
        ax.set_title('Top Retweet Keywords for ' + title, fontsize=16)

    def barGraphAvgLogRetweet(self, keywordValues, title, ax):
        # Retrieve the top keywords list
        ulist = sorted(keywordValues, key=lambda twKeyword: twKeyword.avgLogRetweet, reverse=True)
        topKeys = itertools.islice(ulist, 10)

        # Retrieve keyword list
        nameList = []
        avgRtw = []
        maxAvg = 0
        for key in topKeys:
            nameList.append(key.name)
            avgRtw.append(key.avgLogRetweet)
            if (maxAvg < key.avgLogRetweet):
                maxAvg = key.avgLogRetweet

        y_pos = np.arange(len(nameList))
        ax.bar(y_pos, avgRtw, align='center', alpha=0.5)
        ax.set_xticks(y_pos)
        ax.set_xticklabels(nameList, size=6)
        ax.set_ylim([0, maxAvg * 1.1])
        ax.set_ylabel('Avg of Log(Retweets)', fontsize=14)
        ax.set_xlabel('Top 10 Keywords', fontsize=14)
        ax.set_title('Top Retweet Keywords for ' + title, fontsize=16)

    def barGraphMedLogRetweet(self, keywordValues, title, ax):
        # Retrieve the top keywords list
        ulist = sorted(keywordValues, key=lambda twKeyword: twKeyword.medianLogRetweet, reverse=True)
        topKeys = itertools.islice(ulist, 15)

        # Retrieve keyword list
        nameList = []
        avgRtw = []
        polarList = []
        #colorList = []
        maxAvg = 0
        for key in topKeys:
            nameList.append(key.name)
            polarList.append(key.avgPolarSenti)
            avgRtw.append(key.medianLogRetweet)
            if (maxAvg < key.medianLogRetweet):
                maxAvg = key.medianLogRetweet

        ''' # Set bar colors according to sentiment polarity
        for n in range(int(len(polarList))):
            if (polarList[n] > 0.1):
                colorList.append((polarList[n]*255,0,0)) # Red range for positive sentiment
            elif (polarList[n] < -0.1):
                colorList.append((0,0,abs(polarList[n])*255))  # Blue range for negative sentiment
            elif (polarList[n] == 0):
                colorList.append((255,255,0))  # Yellow for neutral sentiment
            elif (polarList[n] >= -0.1 and polarList[n] < 0):
                colorList.append((255,255*abs(polarList[n]),0))
            elif (polarList[n] <= 0.1 and polarList[n] > 0):
                colorList.append((255*polarList[n], 255, 0))
        '''

        y_pos = np.arange(len(nameList))
        ax.bar(y_pos, avgRtw, align='center', alpha=0.5)  #color=colorList
        ax.set_xticks(y_pos)
        ax.set_xticklabels(nameList, size=8)
        ax.set_ylim([0, maxAvg * 1.1])
        ax.set_ylabel('Retweet Score', fontsize=12)  # Median(Log(RetweetCt))
        ax.set_xlabel('Top 15 Keywords', fontsize=12)
        ax.set_title('Top Retweet Keywords for ' + title, fontsize=14)

    def barGraph(self, keywordValues, title):
        fig, ax = plt.subplots(nrows=1, ncols=1)
        #ax0, ax1, ax2, ax3 = ax.flatten()
        #fig.tight_layout()

        #self.barGraphAvgRetweet(keywordValues, title, ax0)
        #self.barGraphMedRetweet(keywordValues, title, ax1)
        #self.barGraphAvgLogRetweet(keywordValues, title, ax2)
        self.barGraphMedLogRetweet(keywordValues, title, ax)

        fig = plt.gcf()
        DPI = fig.get_dpi()
        fig.set_size_inches(1427.0 / float(DPI), 836.0 / float(DPI))
        fig.tight_layout()

        plt.show()

    def stackedBarAvgRetweetPol(self, neutralKeys, positiveKeys, negativeKeys, ax, sentiPolarList, title):
        ulist = sorted(neutralKeys, key=lambda twKeyword: twKeyword.avgRetweet, reverse=True)
        ulist = itertools.islice(ulist, 3)
        neutralKeys = sorted(ulist, key=lambda twKeyword: twKeyword.avgRetweet, reverse=True)

        ulist = sorted(positiveKeys, key=lambda twKeyword: twKeyword.avgRetweet, reverse=True)
        ulist = itertools.islice(ulist, 3)
        positiveKeys = sorted(ulist, key=lambda twKeyword: twKeyword.avgRetweet, reverse=True)

        ulist = sorted(negativeKeys, key=lambda twKeyword: twKeyword.avgRetweet, reverse=True)
        ulist = itertools.islice(ulist, 3)
        negativeKeys = sorted(ulist, key=lambda twKeyword: twKeyword.avgRetweet, reverse=True)

        avgRtw1 = [neutralKeys[0].avgRetweet, positiveKeys[0].avgRetweet, negativeKeys[0].avgRetweet]
        avgRtw2 = [neutralKeys[1].avgRetweet, positiveKeys[1].avgRetweet, negativeKeys[1].avgRetweet]
        avgRtw3 = [neutralKeys[2].avgRetweet, positiveKeys[2].avgRetweet, negativeKeys[2].avgRetweet]
        maxArray = [neutralKeys[0].avgRetweet + neutralKeys[1].avgRetweet + neutralKeys[2].avgRetweet,
                    positiveKeys[0].avgRetweet + positiveKeys[1].avgRetweet + positiveKeys[2].avgRetweet,
                    negativeKeys[0].avgRetweet + negativeKeys[1].avgRetweet + negativeKeys[2].avgRetweet]

        y_pos = np.arange(3)
        ax.bar(y_pos, avgRtw3, align='center', alpha=0.5, color=['#fdffba', '#feaeae', '#bfcfff'], edgecolor='#000000')
        ax.bar(y_pos, avgRtw2, align='center', bottom=avgRtw3, alpha=0.5, color=['#fcfc66', '#fc7171', '#6d90ff'], edgecolor='#000000')
        ax.bar(y_pos, avgRtw1, align='center', bottom=[avgRtw2[j] + avgRtw3[j] for j in range(len(avgRtw2))], alpha=0.5, color=['#ffff00', '#fe7c2c', '#1636ff'], edgecolor='#000000')
        ax.text(0, neutralKeys[2].avgRetweet / 2, neutralKeys[2].name, ha='center', va='center')
        ax.text(0, (neutralKeys[1].avgRetweet / 2) + neutralKeys[2].avgRetweet, neutralKeys[1].name, ha='center', va='center')
        ax.text(0, (neutralKeys[0].avgRetweet / 2) + neutralKeys[1].avgRetweet + neutralKeys[2].avgRetweet, neutralKeys[0].name, ha='center', va='center')
        ax.text(1, positiveKeys[2].avgRetweet / 2, positiveKeys[2].name, ha='center', va='center')
        ax.text(1, (positiveKeys[1].avgRetweet / 2) + positiveKeys[2].avgRetweet, positiveKeys[1].name, ha='center', va='center')
        ax.text(1, (positiveKeys[0].avgRetweet / 2) + positiveKeys[1].avgRetweet + positiveKeys[2].avgRetweet, positiveKeys[0].name, ha='center', va='center')

        #if
        ax.text(2, negativeKeys[2].avgRetweet / 2, negativeKeys[2].name, ha='center', va='center')
        ax.text(2, (negativeKeys[1].avgRetweet / 2) + negativeKeys[2].avgRetweet, negativeKeys[1].name, ha='center', va='center')
        ax.text(2, (negativeKeys[0].avgRetweet / 2) + negativeKeys[1].avgRetweet + negativeKeys[2].avgRetweet, negativeKeys[0].name, ha='center', va='center')

        ax.set_xticks(y_pos)
        ax.set_xticklabels(sentiPolarList, size=8)
        ax.set_ylabel('Avg # of Retweets', fontsize=10)
        ax.set_xlabel('Tweet Sentiments Polarity', fontsize=10)
        ax.set_title('Top Retweet Keywords for ' + title, fontsize=12)
        ax.set_ylim([0, max(maxArray) * 1.1])

    def stackedBarMedRetweetPol(self, neutralKeys, positiveKeys, negativeKeys, ax, sentiPolarList, title):
        ulist = sorted(neutralKeys, key=lambda twKeyword: twKeyword.medianRetweet, reverse=True)
        ulist = itertools.islice(ulist, 3)
        neutralKeys = sorted(ulist, key=lambda twKeyword: twKeyword.medianRetweet, reverse=True)

        ulist = sorted(positiveKeys, key=lambda twKeyword: twKeyword.medianRetweet, reverse=True)
        ulist = itertools.islice(ulist, 3)
        positiveKeys = sorted(ulist, key=lambda twKeyword: twKeyword.medianRetweet, reverse=True)

        ulist = sorted(negativeKeys, key=lambda twKeyword: twKeyword.medianRetweet, reverse=True)
        ulist = itertools.islice(ulist, 3)
        negativeKeys = sorted(ulist, key=lambda twKeyword: twKeyword.medianRetweet, reverse=True)

        avgRtw1 = [neutralKeys[0].medianRetweet, positiveKeys[0].medianRetweet, negativeKeys[0].medianRetweet]
        avgRtw2 = [neutralKeys[1].medianRetweet, positiveKeys[1].medianRetweet, negativeKeys[1].medianRetweet]
        avgRtw3 = [neutralKeys[2].medianRetweet, positiveKeys[2].medianRetweet, negativeKeys[2].medianRetweet]
        maxArray = [neutralKeys[0].medianRetweet + neutralKeys[1].medianRetweet + neutralKeys[2].medianRetweet,
                    positiveKeys[0].medianRetweet + positiveKeys[1].medianRetweet + positiveKeys[2].medianRetweet,
                    negativeKeys[0].medianRetweet + negativeKeys[1].medianRetweet + negativeKeys[2].medianRetweet]

        y_pos = np.arange(3)
        ax.bar(y_pos, avgRtw3, align='center', alpha=0.5, color=['#fdffba', '#feaeae', '#bfcfff'], edgecolor='#000000')
        ax.bar(y_pos, avgRtw2, align='center', bottom=avgRtw3, alpha=0.5, color=['#fcfc66', '#fc7171', '#6d90ff'], edgecolor='#000000')
        ax.bar(y_pos, avgRtw1, align='center', bottom=[avgRtw2[j] + avgRtw3[j] for j in range(len(avgRtw2))], alpha=0.5, color=['#ffff00', '#fe7c2c', '#1636ff'], edgecolor='#000000')
        ax.text(0, neutralKeys[2].medianRetweet / 2, neutralKeys[2].name, ha='center', va='center')
        ax.text(0, (neutralKeys[1].medianRetweet / 2) + neutralKeys[2].medianRetweet, neutralKeys[1].name, ha='center', va='center')
        ax.text(0, (neutralKeys[0].medianRetweet / 2) + neutralKeys[1].medianRetweet + neutralKeys[2].medianRetweet, neutralKeys[0].name, ha='center', va='center')
        ax.text(1, positiveKeys[2].medianRetweet / 2, positiveKeys[2].name, ha='center', va='center')
        ax.text(1, (positiveKeys[1].medianRetweet / 2) + positiveKeys[2].medianRetweet, positiveKeys[1].name, ha='center', va='center')
        ax.text(1, (positiveKeys[0].medianRetweet / 2) + positiveKeys[1].medianRetweet + positiveKeys[2].medianRetweet, positiveKeys[0].name, ha='center', va='center')
        ax.text(2, negativeKeys[2].medianRetweet / 2, negativeKeys[2].name, ha='center', va='center')
        ax.text(2, (negativeKeys[1].medianRetweet / 2) + negativeKeys[2].medianRetweet, negativeKeys[1].name, ha='center', va='center')
        ax.text(2, (negativeKeys[0].medianRetweet / 2) + negativeKeys[1].medianRetweet + negativeKeys[2].medianRetweet, negativeKeys[0].name, ha='center', va='center')

        ax.set_xticks(y_pos)
        ax.set_xticklabels(sentiPolarList, size=8)
        ax.set_ylabel('Median # of Retweets', fontsize=10)
        ax.set_xlabel('Tweet Sentiments Polarity', fontsize=10)
        ax.set_title('Top Retweet Keywords for ' + title, fontsize=12)
        ax.set_ylim([0, max(maxArray) * 1.1])

    def stackedBarAvgLogRetweetPol(self, neutralKeys, positiveKeys, negativeKeys, ax, sentiPolarList, title):
        ulist = sorted(neutralKeys, key=lambda twKeyword: twKeyword.avgLogRetweet, reverse=True)
        ulist = itertools.islice(ulist, 3)
        neutralKeys = sorted(ulist, key=lambda twKeyword: twKeyword.avgLogRetweet, reverse=True)

        ulist = sorted(positiveKeys, key=lambda twKeyword: twKeyword.avgLogRetweet, reverse=True)
        ulist = itertools.islice(ulist, 3)
        positiveKeys = sorted(ulist, key=lambda twKeyword: twKeyword.avgLogRetweet, reverse=True)

        ulist = sorted(negativeKeys, key=lambda twKeyword: twKeyword.avgLogRetweet, reverse=True)
        ulist = itertools.islice(ulist, 3)
        negativeKeys = sorted(ulist, key=lambda twKeyword: twKeyword.avgLogRetweet, reverse=True)

        avgRtw1 = [neutralKeys[0].avgLogRetweet, positiveKeys[0].avgLogRetweet, negativeKeys[0].avgLogRetweet]
        avgRtw2 = [neutralKeys[1].avgLogRetweet, positiveKeys[1].avgLogRetweet, negativeKeys[1].avgLogRetweet]
        avgRtw3 = [neutralKeys[2].avgLogRetweet, positiveKeys[2].avgLogRetweet, negativeKeys[2].avgLogRetweet]
        maxArray = [neutralKeys[0].avgLogRetweet + neutralKeys[1].avgLogRetweet + neutralKeys[2].avgLogRetweet,
                    positiveKeys[0].avgLogRetweet + positiveKeys[1].avgLogRetweet + positiveKeys[2].avgLogRetweet,
                    negativeKeys[0].avgLogRetweet + negativeKeys[1].avgLogRetweet + negativeKeys[2].avgLogRetweet]

        y_pos = np.arange(3)
        ax.bar(y_pos, avgRtw3, align='center', alpha=0.5, color=['#fdffba', '#feaeae', '#bfcfff'], edgecolor='#000000')
        ax.bar(y_pos, avgRtw2, align='center', bottom=avgRtw3, alpha=0.5, color=['#fcfc66', '#fc7171', '#6d90ff'], edgecolor='#000000')
        ax.bar(y_pos, avgRtw1, align='center', bottom=[avgRtw2[j] + avgRtw3[j] for j in range(len(avgRtw2))], alpha=0.5, color=['#ffff00', '#fe7c2c', '#1636ff'], edgecolor='#000000')
        ax.text(0, neutralKeys[2].avgLogRetweet / 2, neutralKeys[2].name, ha='center', va='center')
        ax.text(0, (neutralKeys[1].avgLogRetweet / 2) + neutralKeys[2].avgLogRetweet, neutralKeys[1].name, ha='center', va='center')
        ax.text(0, (neutralKeys[0].avgLogRetweet / 2) + neutralKeys[1].avgLogRetweet + neutralKeys[2].avgLogRetweet, neutralKeys[0].name, ha='center', va='center')
        ax.text(1, positiveKeys[2].avgLogRetweet / 2, positiveKeys[2].name, ha='center', va='center')
        ax.text(1, (positiveKeys[1].avgLogRetweet / 2) + positiveKeys[2].avgLogRetweet, positiveKeys[1].name, ha='center', va='center')
        ax.text(1, (positiveKeys[0].avgLogRetweet / 2) + positiveKeys[1].avgLogRetweet + positiveKeys[2].avgLogRetweet, positiveKeys[0].name, ha='center', va='center')
        ax.text(2, negativeKeys[2].avgLogRetweet / 2, negativeKeys[2].name, ha='center', va='center')
        ax.text(2, (negativeKeys[1].avgLogRetweet / 2) + negativeKeys[2].avgLogRetweet, negativeKeys[1].name, ha='center', va='center')
        ax.text(2, (negativeKeys[0].avgLogRetweet / 2) + negativeKeys[1].avgLogRetweet + negativeKeys[2].avgLogRetweet, negativeKeys[0].name, ha='center', va='center')

        ax.set_xticks(y_pos)
        ax.set_xticklabels(sentiPolarList, size=8)
        ax.set_ylabel('Avg of Log(Retweets)', fontsize=10)
        ax.set_xlabel('Tweet Sentiments Polarity', fontsize=10)
        ax.set_title('Top Retweet Keywords for ' + title, fontsize=12)
        ax.set_ylim([0, max(maxArray) * 1.1])

    def stackedBarMedLogRetweetPol(self, neutralKeys, positiveKeys, negativeKeys, ax, sentiPolarList, title):
        ulist = sorted(neutralKeys, key=lambda twKeyword: twKeyword.medianLogRetweet, reverse=True)
        ulist = itertools.islice(ulist, 3)
        neutralKeys = sorted(ulist, key=lambda twKeyword: twKeyword.medianLogRetweet, reverse=True)

        ulist = sorted(positiveKeys, key=lambda twKeyword: twKeyword.medianLogRetweet, reverse=True)
        ulist = itertools.islice(ulist, 3)
        positiveKeys = sorted(ulist, key=lambda twKeyword: twKeyword.medianLogRetweet, reverse=True)

        ulist = sorted(negativeKeys, key=lambda twKeyword: twKeyword.medianLogRetweet, reverse=True)
        ulist = itertools.islice(ulist, 3)
        negativeKeys = sorted(ulist, key=lambda twKeyword: twKeyword.medianLogRetweet, reverse=True)

        avgRtw1 = [neutralKeys[0].medianLogRetweet, positiveKeys[0].medianLogRetweet, negativeKeys[0].medianLogRetweet]
        avgRtw2 = [neutralKeys[1].medianLogRetweet, positiveKeys[1].medianLogRetweet, negativeKeys[1].medianLogRetweet]
        avgRtw3 = [neutralKeys[2].medianLogRetweet, positiveKeys[2].medianLogRetweet, negativeKeys[2].medianLogRetweet]
        maxArray = [neutralKeys[0].medianLogRetweet + neutralKeys[1].medianLogRetweet + neutralKeys[2].medianLogRetweet,
                    positiveKeys[0].medianLogRetweet + positiveKeys[1].medianLogRetweet + positiveKeys[2].medianLogRetweet,
                    negativeKeys[0].medianLogRetweet + negativeKeys[1].medianLogRetweet + negativeKeys[2].medianLogRetweet]

        y_pos = np.arange(3)
        ax.bar(y_pos, avgRtw3, align='center', alpha=0.5, color=['#fdffba', '#feaeae', '#bfcfff'], edgecolor='#000000')
        ax.bar(y_pos, avgRtw2, align='center', bottom=avgRtw3, alpha=0.5, color=['#fcfc66', '#fc7171', '#6d90ff'], edgecolor='#000000')
        ax.bar(y_pos, avgRtw1, align='center', bottom=[avgRtw2[j] + avgRtw3[j] for j in range(len(avgRtw2))], alpha=0.5, color=['#ffff00', '#fe7c2c', '#1636ff'], edgecolor='#000000')
        ax.text(0, neutralKeys[2].medianLogRetweet / 2, neutralKeys[2].name, ha='center', va='center')
        ax.text(0, (neutralKeys[1].medianLogRetweet / 2) + neutralKeys[2].medianLogRetweet, neutralKeys[1].name, ha='center', va='center')
        ax.text(0, (neutralKeys[0].medianLogRetweet / 2) + neutralKeys[1].medianLogRetweet + neutralKeys[2].medianLogRetweet, neutralKeys[0].name, ha='center', va='center')
        ax.text(1, positiveKeys[2].medianLogRetweet / 2, positiveKeys[2].name, ha='center', va='center')
        ax.text(1, (positiveKeys[1].medianLogRetweet / 2) + positiveKeys[2].medianLogRetweet, positiveKeys[1].name, ha='center', va='center')
        ax.text(1, (positiveKeys[0].medianLogRetweet / 2) + positiveKeys[1].medianLogRetweet + positiveKeys[2].medianLogRetweet, positiveKeys[0].name, ha='center', va='center')
        ax.text(2, negativeKeys[2].medianLogRetweet / 2, negativeKeys[2].name, ha='center', va='center')
        ax.text(2, (negativeKeys[1].medianLogRetweet / 2) + negativeKeys[2].medianLogRetweet, negativeKeys[1].name, ha='center', va='center')
        ax.text(2, (negativeKeys[0].medianLogRetweet / 2) + negativeKeys[1].medianLogRetweet + negativeKeys[2].medianLogRetweet, negativeKeys[0].name, ha='center', va='center')

        ax.set_xticks(y_pos)
        ax.set_xticklabels(sentiPolarList, size=10)
        ax.set_ylabel('Retweet Score', fontsize=12)
        ax.set_xlabel('Tweet Sentiments: Polarity', fontsize=12)
        ax.set_title('Top Retweet Keywords for ' + title, fontsize=14)
        ax.set_ylim([0, max(maxArray) * 1.1])

    def stackedBarGraphPolarity(self, allKeys, title):
        # Define senti list
        sentiPolarList = ['Neutral', 'Positive', 'Negative']
        neutralKeys = []
        positiveKeys = []
        negativeKeys = []

        # Find top 3 keywords in each senti category
        for key in allKeys:
            if (key.avgPolarSenti >= -0.1 and key.avgPolarSenti <= 0.1):
                neutralKeys.append(key)
            elif (key.avgPolarSenti > 0.1):
                positiveKeys.append(key)
            elif (key.avgPolarSenti < -0.1):
                negativeKeys.append(key)

        fig, ax = plt.subplots(nrows=1, ncols=1)
        #ax0, ax1, ax2, ax3 = ax.flatten()
        #fig.tight_layout()

        #self.stackedBarAvgRetweetPol(neutralKeys, positiveKeys, negativeKeys, ax0, sentiPolarList, title)
        #self.stackedBarMedRetweetPol(neutralKeys, positiveKeys, negativeKeys, ax1, sentiPolarList, title)
        #self.stackedBarAvgLogRetweetPol(neutralKeys, positiveKeys, negativeKeys, ax2, sentiPolarList, title)
        self.stackedBarMedLogRetweetPol(neutralKeys, positiveKeys, negativeKeys, ax, sentiPolarList, title)

        fig = plt.gcf()
        DPI = fig.get_dpi()
        fig.set_size_inches(550.0 / float(DPI), 582.0 / float(DPI))

        plt.show()

    def stackedBarAvgRetweetSub(self, objKeys, subjKeys, ax, sentiSubjList, title):
        ulist = sorted(objKeys, key=lambda twKeyword: twKeyword.avgRetweet, reverse=True)
        ulist = itertools.islice(ulist, 3)
        objKeys = sorted(ulist, key=lambda twKeyword: twKeyword.avgRetweet, reverse=True)

        ulist = sorted(subjKeys, key=lambda twKeyword: twKeyword.avgRetweet, reverse=True)
        ulist = itertools.islice(ulist, 3)
        subjKeys = sorted(ulist, key=lambda twKeyword: twKeyword.avgRetweet, reverse=True)

        avgRtw4 = [objKeys[0].avgRetweet, subjKeys[0].avgRetweet]
        avgRtw5 = [objKeys[1].avgRetweet, subjKeys[1].avgRetweet]
        avgRtw6 = [objKeys[2].avgRetweet, subjKeys[2].avgRetweet]
        maxArray = [objKeys[0].avgRetweet + objKeys[1].avgRetweet + objKeys[2].avgRetweet,
                    subjKeys[1].avgRetweet + subjKeys[1].avgRetweet + subjKeys[2].avgRetweet]

        # Sentiment subjectivity graph
        y_pos = np.arange(2)
        ax.bar(y_pos, avgRtw6, align='center', alpha=0.5, color=['#fdffba', '#feaeae'], edgecolor='#000000')
        ax.bar(y_pos, avgRtw5, align='center', bottom=avgRtw6, alpha=0.5, color=['#fcfc66', '#fc7171'], edgecolor='#000000')
        ax.bar(y_pos, avgRtw4, align='center', bottom=[avgRtw5[j] + avgRtw6[j] for j in range(len(avgRtw5))], alpha=0.5, color=['#ffff00', '#fe7c2c'], edgecolor='#000000')
        ax.text(0, objKeys[2].avgRetweet / 2, objKeys[2].name, ha='center', va='center')
        ax.text(0, (objKeys[1].avgRetweet / 2) + objKeys[2].avgRetweet, objKeys[1].name, ha='center', va='center')
        ax.text(0, (objKeys[0].avgRetweet / 2) + objKeys[1].avgRetweet + objKeys[2].avgRetweet, objKeys[0].name, ha='center', va='center')
        ax.text(1, subjKeys[2].avgRetweet / 2, subjKeys[2].name, ha='center', va='center')
        ax.text(1, (subjKeys[1].avgRetweet / 2) + subjKeys[2].avgRetweet, subjKeys[1].name, ha='center', va='center')
        ax.text(1, (subjKeys[0].avgRetweet / 2) + subjKeys[1].avgRetweet + subjKeys[2].avgRetweet, subjKeys[0].name, ha='center', va='center')

        ax.set_xticks(y_pos)
        ax.set_xticklabels(sentiSubjList, size=8)
        ax.set_ylabel('Avg # of Retweets', fontsize=10)
        ax.set_xlabel('Tweet Sentiments Subjectivity', fontsize=10)
        ax.set_title('Top Retweet Keywords for ' + title, fontsize=12)
        ax.set_ylim([0, max(maxArray) * 1.1])

    def stackedBarMedRetweetSub(self, objKeys, subjKeys, ax, sentiSubjList, title):
        ulist = sorted(objKeys, key=lambda twKeyword: twKeyword.medianRetweet, reverse=True)
        ulist = itertools.islice(ulist, 3)
        objKeys = sorted(ulist, key=lambda twKeyword: twKeyword.medianRetweet, reverse=True)

        ulist = sorted(subjKeys, key=lambda twKeyword: twKeyword.medianRetweet, reverse=True)
        ulist = itertools.islice(ulist, 3)
        subjKeys = sorted(ulist, key=lambda twKeyword: twKeyword.medianRetweet, reverse=True)

        avgRtw4 = [objKeys[0].medianRetweet, subjKeys[0].medianRetweet]
        avgRtw5 = [objKeys[1].medianRetweet, subjKeys[1].medianRetweet]
        avgRtw6 = [objKeys[2].medianRetweet, subjKeys[2].medianRetweet]
        maxArray = [objKeys[0].medianRetweet + objKeys[1].medianRetweet + objKeys[2].medianRetweet,
                    subjKeys[1].medianRetweet + subjKeys[1].medianRetweet + subjKeys[2].medianRetweet]

        # Sentiment subjectivity graph
        y_pos = np.arange(2)
        ax.bar(y_pos, avgRtw6, align='center', alpha=0.5, color=['#fdffba', '#feaeae'], edgecolor='#000000')
        ax.bar(y_pos, avgRtw5, align='center', bottom=avgRtw6, alpha=0.5, color=['#fcfc66', '#fc7171'], edgecolor='#000000')
        ax.bar(y_pos, avgRtw4, align='center', bottom=[avgRtw5[j] + avgRtw6[j] for j in range(len(avgRtw5))], alpha=0.5, color=['#ffff00', '#fe7c2c'], edgecolor='#000000')
        ax.text(0, objKeys[2].medianRetweet / 2, objKeys[2].name, ha='center', va='center')
        ax.text(0, (objKeys[1].medianRetweet / 2) + objKeys[2].medianRetweet, objKeys[1].name, ha='center', va='center')
        ax.text(0, (objKeys[0].medianRetweet / 2) + objKeys[1].medianRetweet + objKeys[2].medianRetweet, objKeys[0].name, ha='center', va='center')
        ax.text(1, subjKeys[2].medianRetweet / 2, subjKeys[2].name, ha='center', va='center')
        ax.text(1, (subjKeys[1].medianRetweet / 2) + subjKeys[2].medianRetweet, subjKeys[1].name, ha='center', va='center')
        ax.text(1, (subjKeys[0].medianRetweet / 2) + subjKeys[1].medianRetweet + subjKeys[2].medianRetweet, subjKeys[0].name, ha='center', va='center')

        ax.set_xticks(y_pos)
        ax.set_xticklabels(sentiSubjList, size=8)
        ax.set_ylabel('Median # of Retweets', fontsize=10)
        ax.set_xlabel('Tweet Sentiments Subjectivity', fontsize=10)
        ax.set_title('Top Retweet Keywords for ' + title, fontsize=12)
        ax.set_ylim([0, max(maxArray) * 1.1])

    def stackedBarAvgLogRetweetSub(self, objKeys, subjKeys, ax, sentiSubjList, title):
        ulist = sorted(objKeys, key=lambda twKeyword: twKeyword.avgLogRetweet, reverse=True)
        ulist = itertools.islice(ulist, 3)
        objKeys = sorted(ulist, key=lambda twKeyword: twKeyword.avgLogRetweet, reverse=True)

        ulist = sorted(subjKeys, key=lambda twKeyword: twKeyword.avgLogRetweet, reverse=True)
        ulist = itertools.islice(ulist, 3)
        subjKeys = sorted(ulist, key=lambda twKeyword: twKeyword.avgLogRetweet, reverse=True)

        avgRtw4 = [objKeys[0].avgLogRetweet, subjKeys[0].avgLogRetweet]
        avgRtw5 = [objKeys[1].avgLogRetweet, subjKeys[1].avgLogRetweet]
        avgRtw6 = [objKeys[2].avgLogRetweet, subjKeys[2].avgLogRetweet]
        maxArray = [objKeys[0].avgLogRetweet + objKeys[1].avgLogRetweet + objKeys[2].avgLogRetweet,
                    subjKeys[1].avgLogRetweet + subjKeys[1].avgLogRetweet + subjKeys[2].avgLogRetweet]

        # Sentiment subjectivity graph
        y_pos = np.arange(2)
        ax.bar(y_pos, avgRtw6, align='center', alpha=0.5, color=['#fdffba', '#feaeae'], edgecolor='#000000')
        ax.bar(y_pos, avgRtw5, align='center', bottom=avgRtw6, alpha=0.5, color=['#fcfc66', '#fc7171'], edgecolor='#000000')
        ax.bar(y_pos, avgRtw4, align='center', bottom=[avgRtw5[j] + avgRtw6[j] for j in range(len(avgRtw5))], alpha=0.5, color=['#ffff00', '#fe7c2c'], edgecolor='#000000')
        ax.text(0, objKeys[2].avgLogRetweet / 2, objKeys[2].name, ha='center', va='center')
        ax.text(0, (objKeys[1].avgLogRetweet / 2) + objKeys[2].avgLogRetweet, objKeys[1].name, ha='center', va='center')
        ax.text(0, (objKeys[0].avgLogRetweet / 2) + objKeys[1].avgLogRetweet + objKeys[2].avgLogRetweet, objKeys[0].name, ha='center', va='center')
        ax.text(1, subjKeys[2].avgLogRetweet / 2, subjKeys[2].name, ha='center', va='center')
        ax.text(1, (subjKeys[1].avgLogRetweet / 2) + subjKeys[2].avgLogRetweet, subjKeys[1].name, ha='center', va='center')
        ax.text(1, (subjKeys[0].avgLogRetweet / 2) + subjKeys[1].avgLogRetweet + subjKeys[2].avgLogRetweet, subjKeys[0].name, ha='center', va='center')

        ax.set_xticks(y_pos)
        ax.set_xticklabels(sentiSubjList, size=8)
        ax.set_ylabel('Avg of Log(Retweets)', fontsize=10)
        ax.set_xlabel('Tweet Sentiments Subjectivity', fontsize=10)
        ax.set_title('Top Retweet Keywords for ' + title, fontsize=12)
        ax.set_ylim([0, max(maxArray) * 1.1])

    def stackedBarMedLogRetweetSub(self, objKeys, subjKeys, ax, sentiSubjList, title):
        ulist = sorted(objKeys, key=lambda twKeyword: twKeyword.medianLogRetweet, reverse=True)
        ulist = itertools.islice(ulist, 3)
        objKeys = sorted(ulist, key=lambda twKeyword: twKeyword.medianLogRetweet, reverse=True)

        ulist = sorted(subjKeys, key=lambda twKeyword: twKeyword.medianLogRetweet, reverse=True)
        ulist = itertools.islice(ulist, 3)
        subjKeys = sorted(ulist, key=lambda twKeyword: twKeyword.medianLogRetweet, reverse=True)

        avgRtw4 = [objKeys[0].medianLogRetweet, subjKeys[0].medianLogRetweet]
        avgRtw5 = [objKeys[1].medianLogRetweet, subjKeys[1].medianLogRetweet]
        avgRtw6 = [objKeys[2].medianLogRetweet, subjKeys[2].medianLogRetweet]
        maxArray = [objKeys[0].medianLogRetweet + objKeys[1].medianLogRetweet + objKeys[2].medianLogRetweet,
                    subjKeys[1].medianLogRetweet + subjKeys[1].medianLogRetweet + subjKeys[2].medianLogRetweet]

        # Sentiment subjectivity graph
        y_pos = np.arange(2)
        ax.bar(y_pos, avgRtw6, align='center', alpha=0.5, color=['#fdffba', '#feaeae'], edgecolor='#000000')
        ax.bar(y_pos, avgRtw5, align='center', bottom=avgRtw6, alpha=0.5, color=['#fcfc66', '#fc7171'], edgecolor='#000000')
        ax.bar(y_pos, avgRtw4, align='center', bottom=[avgRtw5[j] + avgRtw6[j] for j in range(len(avgRtw5))], alpha=0.5, color=['#ffff00', '#fe7c2c'], edgecolor='#000000')
        ax.text(0, objKeys[2].medianLogRetweet / 2, objKeys[2].name, ha='center', va='center')
        ax.text(0, (objKeys[1].medianLogRetweet / 2) + objKeys[2].medianLogRetweet, objKeys[1].name, ha='center', va='center')
        ax.text(0, (objKeys[0].medianLogRetweet / 2) + objKeys[1].medianLogRetweet + objKeys[2].medianLogRetweet, objKeys[0].name, ha='center', va='center')
        ax.text(1, subjKeys[2].medianLogRetweet / 2, subjKeys[2].name, ha='center', va='center')
        ax.text(1, (subjKeys[1].medianLogRetweet / 2) + subjKeys[2].medianLogRetweet, subjKeys[1].name, ha='center', va='center')
        ax.text(1, (subjKeys[0].medianLogRetweet / 2) + subjKeys[1].medianLogRetweet + subjKeys[2].medianLogRetweet, subjKeys[0].name, ha='center', va='center')

        ax.set_xticks(y_pos)
        ax.set_xticklabels(sentiSubjList, size=10)
        ax.set_ylabel('Retweet Score', fontsize=12)
        ax.set_xlabel('Tweet Sentiments: Subjectivity', fontsize=12)
        ax.set_title('Top Retweet Keywords for ' + title, fontsize=14)
        ax.set_ylim([0, max(maxArray) * 1.1])

    def stackedBarGraphSubjectivity(self, allKeys, title):
        # Define senti list
        sentiSubjList = ['Objective', 'Subjective']
        objKeys = []
        subjKeys = []

        # Find top 3 keywords in each senti category
        for key in allKeys:
            if (key.avgSubjSenti > 0.5):
                subjKeys.append(key)
            elif (key.avgSubjSenti < 0.5):
                objKeys.append(key)

        fig, ax = plt.subplots(nrows=1, ncols=1)
        #ax0, ax1, ax2, ax3 = ax.flatten()
        #fig.tight_layout()

        #self.stackedBarAvgRetweetSub(objKeys, subjKeys, ax0, sentiSubjList, title)
        #self.stackedBarMedRetweetSub(objKeys, subjKeys, ax1, sentiSubjList, title)
        #self.stackedBarAvgLogRetweetSub(objKeys, subjKeys, ax2, sentiSubjList, title)
        self.stackedBarMedLogRetweetSub(objKeys, subjKeys, ax, sentiSubjList, title)

        fig = plt.gcf()
        DPI = fig.get_dpi()
        fig.set_size_inches(550.0 / float(DPI), 582.0 / float(DPI))

        plt.show()

    def histogram(self, csv, title):
        df = pd.read_csv(csv)
        fig, ax = plt.subplots(nrows=2, ncols=1)
        ax0, ax1 = ax.flatten()
        #ax0, ax1, ax2, ax3 = ax.flatten()
        fig.tight_layout()

        ax0.set_title('Histogram for ' + title, fontsize=14)
        ax0.set_xlabel('Retweet Count', fontsize=12)
        ax0.set_ylabel('Tweet Count', fontsize=12)

        ax1.set_title('Histogram for ' + title, fontsize=14)
        ax1.set_xlabel('Log(Retweet Count)', fontsize=12)
        ax1.set_ylabel('Tweet Count', fontsize=12)

        #ax2.set_title('Histogram')
        #ax2.set_xlabel('Normalized Retweet Count')
        #ax2.set_ylabel('Number of Tweets')

        #ax3.set_title('Histogram')
        #ax3.set_xlabel('Sqrt(Retweet)')
        #ax3.set_ylabel('Number of Tweets')

        ax0.hist(df['RetweetCt'], bins=50)

        df1 = [math.log10(x + 1) for x in df['RetweetCt']]
        ax1.hist(df1, bins=50)

        #normalized_df = (df['RetweetCt'] - df['RetweetCt'].min()) / (df['RetweetCt'].max() - df['RetweetCt'].min())
        #ax2.hist(normalized_df, bins=10)
        #ax2.set_yscale('log', nonposy='clip')

        #df3 = [math.sqrt(x) for x in df['RetweetCt']]
        #ax3.hist(df3, bins=20)

        mean = df['RetweetCt'].mean()
        median = df['RetweetCt'].median()
        max = df['RetweetCt'].max()

        fig = plt.gcf()
        DPI = fig.get_dpi()
        fig.set_size_inches(1024.0 / float(DPI), 968.0 / float(DPI))

        plt.show()

    def wordCloudGraph(self, text, stopWords):
        # read the mask image
        # text = open('alice.txt').read()
        mask = np.array(Image.open("twitter_mask.png"))

        wc = WordCloud(background_color="black", max_words=200000, mask=mask, collocations=False, normalize_plurals=False)
        wc.generate(text)

        # store to file
        # wc.to_file("twWordCloud.png")

        # show
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        plt.show()