import os
import re
# Module that interfaces with the twitter API
import tweepy
from tweepy import OAuthHandler
# Module that carries out sentiment analysis
from textblob import TextBlob

# os.environ['CONSKEY'] = "qc3xNBhXKoeuaNyOdr1FDWwzZ"
# os.environ['CONSSECRET'] = "HW6z7h9DYFFJZmZTrQfcGkMONa5k5X1HYmE2Qv0JuOgCIBXRBg"
# os.environ['ACCTOKEN'] = "4900371912-CPNC1CIg0uDKylFEPClYJqw7fKLqoyfZ2MczCjl"
# os.environ['ACCSECRET'] = "7n8dkQi3NBtJFm4bEgo5sftaNFv5IRkts1R7gpjV2UbOT"

# Declared a twitter class that is the "control-center" of the app.
class Twitter(object):
    # object instance initialized parametrized by itself, a query and a couple of booleans describing tweet attributes
    def __init__(self, query, retweets_only = False, with_sentiment = False):
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
            self.retweets_only = retweets_only
            self.with_sentiment = with_sentiment
            # Actual Authentication with the twitter api
            self.api = tweepy.API(self.auth)
            self.tweet_count_max = 100
            print("AUTH SUCCESSFUL")
        except:
            print("AUTH FAILED")

    # A query is passed in this method and is set to itself.
    def set_query(self, query=''):
        self.query = query

    def set_retweet_checking(self, retweets_only='false'):
        self.retweets_only = retweets_only

    def set_with_sentiment(self, with_sentiment='false'):
        self.with_sentiment = with_sentiment


    # def remove_fluff(self, tweet):
    #     tweet = re.sub("https?\:\/\/", "", tweet)   #links
    #     tweet = re.sub("#\S+", "", tweet)           #hashtags
    #     tweet = re.sub("\.?@", "", tweet)           #at mentions
    #     tweet = re.sub("RT.+", "", tweet)           #Retweets
    #     tweet = re.sub("Video\:", "", tweet)        #Videos
    #     tweet = re.sub("\n", "", tweet)             #new lines
    #     tweet = re.sub("^\.\s.", "", tweet)         #leading whitespace
    #     tweet = re.sub("\s+", " ", tweet)           #extra whitespace
    #     tweet = re.sub("&amp;", "and", tweet)       #encoded ampersands
    #     return tweet

    # Remove tweet fluff(at mentions, links) using regex.
    def remove_fluff(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(\.?@)|(https?\:\/\/)|(\n)", " ", tweet).split())

    def get_sentiment(self, tweet):
        # We access the TextBlob module to analyze individual tweets
        analysis = TextBlob(self.remove_fluff(tweet))
        # Determine the polarity of the tweet(Whether it is positive or negative)
        if analysis.sentiment.polarity > 0:
            return 'Positive'
        elif analysis.sentiment.polarity == 0:
            return 'Neutral'
        else:
            return 'Negative'

    def get_tweets(self):
        tweets = []

        # We make the api call to retrieve tweets with a specific query and retrieve the top 150 results
        try:
            received_tweets = self.api.search(q=self.query, count=self.tweet_count_max)
            if not received_tweets:
                pass
            for tweet in received_tweets:
                parsed_tweet = {}

                # Each parsed tweet is an object that has properties associated with it (sentiment, tweet, user).
                parsed_tweet['text'] = tweet.text
                parsed_tweet['user'] = tweet.user.screen_name


                # If the parsed tweet has a sentiment field, we do sentiment analysis on the tweet.
                if self.with_sentiment == 1:
                    parsed_tweet['sentiment'] = self.get_sentiment(tweet.text)
                else:
                    parsed_tweet['sentiment'] = 'unavailable'

                # Check whether a certain tweet is already in our tweets array, if not append the parsed tweet to the tweets array.
                if tweet.retweet_count > 0 and self.retweets_only == 1:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                elif not self.retweets_only:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                        print tweets
                        # SAMPLE :
                        # [{'text': u'RT @ranman09: Elizabeth Warren Shows Trump Exactly What \u201cNasty Women\u201d Are Going To Do On Election Day via @politicususa https://t.co/7mbIC7\u2026', 'user': u'chirpydove', 'sentiment': 'negative'}]

            return tweets

        except tweepy.TweepError as e:
            print("Error : " + str(e))
