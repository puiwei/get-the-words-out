#!/usr/bin/env python
from psycopg2 import extras
from datetime import datetime
import psycopg2
import pandas as pd
import sqlalchemy

class TwitterDB:
    def __init__(self):
        try:
            self.conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='postgres'")
            self.cur = self.conn.cursor()

        except:
            print("I am unable to connect to the database")

    def get_data_frame(self):
        engine = sqlalchemy.create_engine('postgresql+psycopg2://postgres:postgres@localhost/postgres')
        name_of_table = 'twitter'
        df = pd.read_sql_query("select tweet_retweet_ct, user_followers_ct, user_statuses_ct, tweet_keywords, tweet_length, tweet_word_ct, polarity, subjectivity, tweet_has_links from %s tablesample system (100) repeatable(1) limit 500000;" % name_of_table, engine)
        #df = pd.read_sql_table(name_of_table, engine)
        return df

    def write_db(self, word, twitter_results, recent=True):
        # Process results
        processed_results_list = []
        last_tweet_id = 9999999999999999999

        for result in twitter_results:
            # Create dictionary
            list_result = []
            list_result.append(result['id_str'])                         # tweet id
            list_result.append(word)                                     # tweet search term
            list_result.append(int(result['retweet_count']))             # tweet retweet count
            list_result.append(result['full_text'])                      # tweet text
            list_result.append(int(result['user']['followers_count']))   # user followers ct
            list_result.append(int(result['user']['friends_count']))     # user user_friends_ct ct
            list_result.append(int(result['user']['favourites_count']))  # user_favorites_ct
            list_result.append(int(result['user']['statuses_count']))    # user_statuses_ct followers ct
            list_result.append(result['user']['created_at'])             # user_created_at
            list_result.append(result['created_at'])                     # tweet_created_at
            list_result.append(result['user']['id_str'])                 # user id
            list_result.append(result['user']['screen_name'])            # user name
            if result['id'] < last_tweet_id:
                last_tweet_id = result['id']

            # Add to list
            processed_results_list.append(list_result)

        print('Writing ' + str(len(processed_results_list)) + ' records for (' + word + ') Last ID: ' + str(last_tweet_id))

        # Write to DB
        try:
            extras.execute_values(self.cur, """INSERT INTO twitter3(tweet_id, tweet_search_term, tweet_retweet_ct, tweet_text, user_followers_ct, user_friends_ct, user_favorites_ct, user_statuses_ct, user_created_at, tweet_created_at, user_id, user_name) VALUES %s ON CONFLICT DO NOTHING""", processed_results_list)
            if recent:
                self.cur.execute("""INSERT INTO twitter_id(tweet_search_term, token) VALUES (%s, %s) ON CONFLICT (tweet_search_term) DO UPDATE SET token = %s""", (word, str(last_tweet_id), str(last_tweet_id)))
            else:
                self.cur.execute("""INSERT INTO popular_id(tweet_search_term, token) VALUES (%s, %s) ON CONFLICT (tweet_search_term) DO UPDATE SET token = %s""", (word, str(last_tweet_id), str(last_tweet_id)))
            self.conn.commit()

        except Exception as e:
            print("DB Error:" + str(e))

    def get_token(self, word):
        try:
            self.cur.execute("""SELECT token from twitter_id WHERE tweet_search_term=%s""", (word,))
            row = self.cur.fetchone()
            if row:
                return row[0]
        except Exception as e:
            print("DB Error:" + str(e))

        return '0'

    def get_popular_token(self, word):
        try:
            self.cur.execute("""SELECT token from popular_id WHERE tweet_search_term=%s""", (word,))
            row = self.cur.fetchone()
            if row:
                return row[0]
        except Exception as e:
            print("DB Error:" + str(e))

        return '0'

    def write_db_done(self, word):
        self.cur.execute("""INSERT INTO popular_id(tweet_search_term, token) VALUES (%s, %s) ON CONFLICT (tweet_search_term) DO UPDATE SET token = %s""", (word, 'Done', 'Done'))
        self.conn.commit()

    def pull_keyword_entries(self):
        try:
            self.cur.execute("""SELECT tweet_id, tweet_text from twitter2 WHERE tweet_keywords is NULL LIMIT 200""")
            row = self.cur.fetchall()
            if row:
                return row
        except Exception as e:
            print("DB Error:" + str(e))

        return []

    def pull_keyword_entries_missing_fields(self):
        try:
            self.cur.execute("""SELECT tweet_id, tweet_text from twitter3  WHERE tweet_has_links is NULL LIMIT 200""")
            row = self.cur.fetchall()
            if row:
                return row
        except Exception as e:
            print("DB Error:" + str(e))

        return []

    def write_calculations(self, db_data):
        try:
            print('Writing ' + str(len(db_data)) + ' records at ' + str(datetime.now().strftime('%m/%d/%Y %I:%M:%S%p')))
            extras.execute_values(self.cur, """UPDATE twitter3 SET tweet_keywords=data.v1, tweet_length=data.v2, polarity=data.v3, subjectivity=data.v4, tweet_word_ct=data.v5, tweet_has_links=data.v6 FROM (VALUES %s) AS data (id, v1, v2, v3, v4, v5, v6) WHERE twitter3.tweet_id=data.id""", db_data)
            self.conn.commit()
        except Exception as e:
            print("DB Error:" + str(e))

    def finalize(self):
        self.cur.close()
        self.conn.close()
