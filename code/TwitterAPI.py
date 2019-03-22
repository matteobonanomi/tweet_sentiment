import pandas as pd
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''

    #    def __init__(self):
    #        '''
    #        Class constructor or initialization method.
    #        '''
    #        # keys and tokens from the Twitter Dev Console
    #        consumer_key = 'XXXXXXXXXXXXXXXXXXXXXXXX'
    #        consumer_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    #        access_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    #        access_token_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXX'
    #
    #        # attempt authentication
    #        try:
    #            # create OAuthHandler object
    #            self.auth = OAuthHandler(consumer_key, consumer_secret)
    #            # set access token and secret
    #            self.auth.set_access_token(access_token, access_token_secret)
    #            # create tweepy API object to fetch tweets
    #            self.api = tweepy.API(self.auth)
    #        except:
    #            print("Error: Authentication Failed")

    def _clean_tweets(self, tweet_list):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        clean_tweets = [re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', x, flags=re.MULTILINE) for x in
                        tweet_list]
        clean_tweets = [re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", x) for x in clean_tweets]

        return clean_tweets

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(tweet)
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets_from_df(self, author, count=1):
        '''
        Main function to fetch tweets and parse them.
        '''

        tweets_df = pd.read_csv('..//data//tweets_kaggle.csv')[['handle', 'text', 'original_author']]
        tweets_df.original_author = tweets_df.original_author.apply(str)

        tweets_df = tweets_df[tweets_df['original_author'] == 'nan'][['handle', 'text']]
        fetched_tweets = tweets_df[tweets_df.handle == author].text.tolist()

        clean_tweets = self._clean_tweets(fetched_tweets)

        return clean_tweets

    def analyze_tweets(self, fetched_tweets):

        # empty list to store parsed tweets
        tweets = []
        # parsing tweets one by one
        for tweet in fetched_tweets:
            # empty dictionary to store required params of a tweet
            parsed_tweet = {}

            # saving text of tweet
            parsed_tweet['text'] = tweet
            # saving sentiment of tweet
            parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet)

            # appending parsed tweet to tweets list
            tweets.append(parsed_tweet)

            # return parsed tweets
        return tweets

    def get_one_tweet(self, fetched_tweets):
        '''
        Main function to fetch custom tweets and parse them.
        '''
        tweets = []
        try:

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet)

                # appending parsed tweet to tweets list
                tweets.append(parsed_tweet)

                # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))

    def print_tweet_sentiment(self, tweets):

        # picking positive tweets from tweets
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
        # percentage of positive tweets
        print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
        # picking negative tweets from tweets
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        # percentage of negative tweets
        print("Negative tweets percentage: {}%".format(100 * len(ntweets) / len(tweets)))
        # percentage of neutral tweets
        print("Neutral tweets percentage: {}%".format(100 * (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets)))
        print('-------------------------------------------------------------')
        # printing first 5 positive tweets

        print("\nPositive tweets:")
        for tweet in ptweets[:5]:
            print('')
            print(tweet['text'])

        print('-------------------------------------------------------------')
        # printing first 5 negative tweets
        print("\nNegative tweets:")
        for tweet in ntweets[:5]:
            print('')
            print(tweet['text'])

        return
