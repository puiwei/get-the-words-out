class twKeyword():
    def __init__(self, name):
        self.name = name
        self.count = 0
        self.retweetSum = 0
        self.avgRetweet = 0.0
        self.sentiSum = 0
        self.avgSenti = 0.0
        
    def calcAvgs(self):
        if (self.count > 0):
            self.avgRetweet = self.retweetSum / self.count
            self.avgSenti = self.sentiSum / self.count
        
    def addRetweet(self, retweetCount):
        self.retweetSum = self.retweetSum + retweetCount
        self.count = self.count + 1
    
    def addSentiScore(self, score):
        self.sentiSum = self.sentiSum + score
       
    def print(self):
        print('Key: ' + self.name + ' Count: ' + str(self.count) + ' RetweetSum: ' + str(self.retweetSum) + ' Average: ' + str(self.avgRetweet))
        
        