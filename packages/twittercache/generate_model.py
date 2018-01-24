#!/usr/bin/env python
from packages.twittercache.twitter_db import TwitterDB


db = TwitterDB()
df = db.get_data_frame()
a = 5