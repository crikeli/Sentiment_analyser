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

    # A query is passed in this method and is set to itself.
    def setQuery(self, query=''):
        self.query = query

    def set_rt_checking(self, rt_only='false'):
        self.rt_only = rt_only

    def set_with_sent(self, with_sent='false'):
        self.with_sent = with_sent

    # Remove tweet fluff(videos, at mentions, links) using regex.
    def remove_fluff(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(https?\:\/\/)|(\.?@)|(Video\:)", " ", tweet).split())

    def get_sentiment(self, tweet):
        # We access the TextBlob module to analyze individual tweets
        analysis = TextBlob(self.remove_fluff(tweet))
        # Determine the polarity of the tweet(Whether it is positive or negative)
        if analysis.sentiment.polarity > 0:
            return 'Positive :)'
        elif analysis.sentiment.polarity == 0:
            return 'Neutral -_-'
        else:
            return 'Negative :('

    def get_all_tweets(self):
        tweets = []

        # We make the api call to retrieve tweets with a specific query and retrieve the top 150 results
        try:
            received_tweets = self.api.search(q=self.query, count=self.max_tweets)

            if not received_tweets:
                pass
            for tweet in received_tweets:
                # Each parsed tweet is an object that has properties associated with it (sentiment, tweet, user).
                parsed_tweet = {}

                # One property is the tweet text
                parsed_tweet['text'] = tweet.text
                # The other property is the user name
                parsed_tweet['user'] = tweet.user.screen_name

                # If the parsed tweet has a sentiment field, we do sentiment analysis on the tweet.
                if self.with_sent == 1:
                    parsed_tweet['sentiment'] = self.get_sentiment(tweet.text)
                else:
                    parsed_tweet['sentiment'] = "Could not analyze sentiment"

                # Check whether a certain tweet is already in our tweets array, if not append the parsed tweet to the tweets array.
                if tweet.retweet_count > 0 and self.rt_only == 1:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                elif not self.rt_only:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)

                return tweets

        except tweepy.TweepError as e:
            print("Error: " + str(e))
