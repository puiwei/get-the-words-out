#!/usr/bin/env python
import re
from textblob import TextBlob
import spacy
from .twitter_db import TwitterDB

class TwitterProcess:
    def __init__(self):
        self.db = TwitterDB()
        self.nlp = spacy.load('en_core_web_sm')
        self.stop_words = self.load_stopwords()
        self.apostrophe_words = self.load_stopwords()
        self.memory_ct = 0

    def get_tweet_sentiment(self, tweet):
        # Create text string from tokens
        analysis = TextBlob(tweet)
        return analysis.sentiment.polarity, analysis.sentiment.subjectivity

    def load_stopwords(self):
        # Load stop words list from file
        with open('StopWords.txt', 'r') as stopwords_file:
            stopwords = stopwords_file.readlines()
        return [x.strip().lower() for x in stopwords]

    def load_apostrophe_words(self):
        with open('ApostropheWords.txt', 'r') as ApostropheWordsFile:
            apostrophe_words = ApostropheWordsFile.readlines()
        return [x.strip() for x in apostrophe_words]

    def skip_token(self, word, tag):
        if tag == 'PUNCT' or tag == 'SYM' or tag == 'X' or tag == 'NUM':
            return True

        if word.lower() in self.stop_words:
            return True

        if word.lower() in self.apostrophe_words:
            return True

        if len(word.strip()) <= 2:
            return True

        if 'http' in word:
            return True

        return False

    def process_token(self, token):
        replacements = [('w/', 'with'),
                        ('\o/', ''),
                        ("i'm", ''),
                        ('mt.', 'mount'),
                        ("’re", 'are'),
                        ("'re", 'are'),
                        ("’ve", 'have'),
                        ("'ve", 'have'),
                        ("n’t", 'not'),
                        ("n't", 'not'),
                        ("’ll", 'will'),
                        ("'ll", 'will')
                        ]
        word = token.text
        for k, v in replacements:
            word = word.replace(k, v)

        # Strip non-alpha
        word = re.sub(r'\W+', '', word)

        return word.lower()

    def process_tokens(self, text):
        # Spacy memory issues - Reload spacy
        self.memory_ct += 1
        if self.memory_ct > 5000:
            self.memory_ct = 0
            self.nlp = spacy.load('en_core_web_sm')

        doc = self.nlp(text)
        tokens = ""
        for token in doc:
            word = self.process_token(token)
            if self.skip_token(word, token.pos_):
                continue

            tokens += word + " "

        return tokens.strip()

    def has_links(self, text):
        if 'http' in text:
            return True
        if 'www.' in text:
            return True

        if '.com' in text:
            return True

        if '.net' in text:
            return True

        return False

    def process_keywords_missing_fields(self):
        while True:
            data = self.db.pull_keyword_entries_missing_fields()
            if not data:
                break

            db_data = []
            # Process each record
            for tweet_id, text, tokens in data:
                word_ct = len(tokens.split(" "))
                haslinks = self.has_links(text)
                db_data.append([tweet_id, word_ct, haslinks])

            self.db.write_calculations(db_data)

    def process_keywords(self, data):
        db_data = []
        # Process each record
        for tweet_id, text in data:
            tokens = self.process_tokens(text)
            tweet_length = len(text)
            polarity, subjectivity = self.get_tweet_sentiment(text)
            word_ct = len(tokens.split(" "))
            has_links = self.has_links(text)
            db_data.append([tweet_id, tokens, tweet_length, polarity, subjectivity, word_ct, has_links])

        return db_data

    def run(self):
        while True:
            data = self.db.pull_keyword_entries_missing_fields()
            if not data:
                break

            db_data = self.process_keywords(data)
            self.db.write_calculations(db_data)


# Main Execution
#process = TwitterProcess()
#process.run()
