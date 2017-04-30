#!/usr/bin/env python
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import itertools
 
class twGraph():
    def topSenti(self, l, number):
        # For those tied with average retweet, the original order of the keyword is used
        # in determining what gets displayed first
        ulist = sorted(l, key=lambda twKeyword: twKeyword.avgSenti, reverse=True)
        ulist = itertools.islice(ulist, number)
        ulist = sorted(ulist, key=lambda twKeyword: twKeyword.avgSenti, reverse=True)
        return ulist
    
    def barGraph(self, topKeys, title):
        # Retreive keyword list
        nameList = []
        avgRtw = []
        maxAvg = 0;
        for key in topKeys:
            nameList.append(key.name)
            avgRtw.append(key.avgRetweet)
            if (maxAvg < key.avgRetweet):
                maxAvg = key.avgRetweet
        
        #print(nameList)
        #print(avgRtw)
        
        y_pos = np.arange(len(nameList))
         
        plt.bar(y_pos, avgRtw, align='center', alpha=0.5)
        plt.xticks(y_pos, nameList)
        plt.ylim([0, int(maxAvg * 1.1)])
        plt.ylabel('Avg # of Retweets', fontsize=14)
        plt.xlabel('Top 10 Keywords', fontsize=14)
        plt.title('@' + title + '\'s Top Retweet Keywords', fontsize=16)
        plt.show()
        
    def stackedBarGraph(self, allKeys, title):
        # Define senti list
        sentiList = ['Neutral', 'Positive', 'Negative']
        avgRtwList = []
        neutralKeys = []
        positiveKeys = []
        negativeKeys = []
        
        # Find top 3 keywords in each senti category
        for key in allKeys:
            if (key.avgSenti >= -0.1 and key.avgSenti <= 0.1):
                neutralKeys.append(key)
            elif (key.avgSenti >= 0.2):
                positiveKeys.append(key)
            elif (key.avgSenti <= -0.2):
                negativeKeys.append(key)

        neutralKeys = self.topSenti(neutralKeys, 3)
        positiveKeys = self.topSenti(positiveKeys, 3)
        negativeKeys = self.topSenti(negativeKeys, 3)          
        
        #print('Neutral')
        #for x in neutralKeys:
        #    print(x.name + ' ' + str(x.avgRetweet) + str(x.avgSenti))
        #print('Positive')
        #for x in positiveKeys:
        #    print(x.name + ' ' + str(x.avgRetweet) + str(x.avgSenti))
        #print('Negative')
        #for x in negativeKeys:
        #    print(x.name + ' ' + str(x.avgRetweet) + str(x.avgSenti))
        
        avgRtw1 = [neutralKeys[0].avgRetweet, positiveKeys[0].avgRetweet, negativeKeys[0].avgRetweet]
        avgRtw2 = [neutralKeys[1].avgRetweet, positiveKeys[1].avgRetweet, negativeKeys[1].avgRetweet]
        avgRtw3 = [neutralKeys[2].avgRetweet, positiveKeys[2].avgRetweet, negativeKeys[2].avgRetweet]
        
        y_pos = np.arange(3)
        plt.bar(y_pos, avgRtw3, align='center', alpha=0.5, color=['#fdffba', '#feaeae', '#bfcfff'], edgecolor='#000000')
        plt.bar(y_pos, avgRtw2, align='center', bottom=avgRtw3, alpha=0.5, color=['#fcfc66', '#fc7171', '#6d90ff'], edgecolor='#000000')
        plt.bar(y_pos, avgRtw1, align='center', bottom=[avgRtw2[j] + avgRtw3[j] for j in range(len(avgRtw2))], alpha=0.5, color=['#ffff00', '#fe7c2c', '#1636ff'], edgecolor='#000000')
        plt.text(0, neutralKeys[2].avgRetweet / 2, neutralKeys[2].name, ha='center', va='center')
        plt.text(0, (neutralKeys[1].avgRetweet / 2) + neutralKeys[2].avgRetweet, neutralKeys[1].name, ha='center', va='center')
        plt.text(0, (neutralKeys[0].avgRetweet / 2) + neutralKeys[1].avgRetweet + neutralKeys[2].avgRetweet, neutralKeys[0].name, ha='center', va='center')
        
        plt.text(1, positiveKeys[2].avgRetweet / 2, positiveKeys[2].name, ha='center', va='center')
        plt.text(1, (positiveKeys[1].avgRetweet / 2) + positiveKeys[2].avgRetweet, positiveKeys[1].name, ha='center', va='center')
        plt.text(1, (positiveKeys[0].avgRetweet / 2) + positiveKeys[1].avgRetweet + positiveKeys[2].avgRetweet, positiveKeys[0].name, ha='center', va='center')
        
        plt.text(2, negativeKeys[2].avgRetweet / 2, negativeKeys[2].name, ha='center', va='center')
        plt.text(2, (negativeKeys[1].avgRetweet / 2) + negativeKeys[2].avgRetweet, negativeKeys[1].name, ha='center', va='center')
        plt.text(2, (negativeKeys[0].avgRetweet / 2) + negativeKeys[1].avgRetweet + negativeKeys[2].avgRetweet, negativeKeys[0].name, ha='center', va='center')
        
        plt.xticks(y_pos, sentiList)
        plt.ylabel('Avg # of Retweets', fontsize=14)
        plt.xlabel('Tweet Sentiments', fontsize=14)
        plt.title('@' + title + '\'s Top Retweet Keywords', fontsize=16)
         
        plt.show()
        
        
        
        
        
        
        
        
        
        
        
        
        