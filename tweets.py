import os
import re
# Module that interfaces with the twitter API
import tweepy
from tweepy import OAuthHandler
# Module that carries out sentiment analysis
from textblob import TextBlob

# Declared a twitter class that is the "control-center" of the app.
class Twitter(object):
    # object instance initialized parametrized by itself, a query and a couple of booleans describing tweet attributes
    def __init__(self, query, rt_only = False, with_sent = False):
        # Twitter Keys
        consumer_key = os.environ['CONSKEY']
        consumer_secret = os.environ['CONSSECRET']
        access_token = os.environ['ACCTOKEN']
        access_secret = os.environ['ACCSECRET']

        # Begin auth -
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_secret)
            self.query = query
            self.rt_only = rt_only
            self.with_sent = with_sent
            # Actual Authentication with the twitter api
            self.api = tweepy.API(self.auth)
            # 200 tweets is the limit per call.
            self.max_tweets = 150
            print("AUTH SUCCESSFUL")
        except:
            print("AUTH FAILED")
