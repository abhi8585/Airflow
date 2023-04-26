import tweepy
import logging
from utils.twitter.twitter_utils import TwitterUtils
from utils.logger import Logger

logger = Logger()

class TwitterClient:

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        try:
            self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
            logger.log_data(f"TwitterClient created successfully")
        except Exception as e:
            logging.exception(f"Error occurred while Authenticating&Creating Twitter client: {str(e)}")

    def get_relevant_hashtags(self, description, no_of_hashtags , count=40):
        try:
            hashtags = []
            search_results = self.api.search_tweets(description, count=count, lang='en')
            for tweet in search_results:
                hashtags.append(TwitterUtils.extract_hashtags(tweet.text))
            logger.log_data(f"Relevant Hashtags for description {description} are {hashtags}")
            return TwitterUtils.get_top_hashtags(hashtags,no_of_hashtags)
        except Exception as e:
            logging.exception("Error occurred while getting relevant hashtags: %s", str(e))

    def tweet_text(self, tweet_content):
        try:
            logger.log_data(f"Tweet content to post : {tweet_content}")
            self.api.update_status(tweet_content)
            logger.log_data("Tweet posted successfully!")
            return dict(tweet_status=True)
        except tweepy.TweepError as e:
            logger.log_data(f"Error posting tweet: {e}")
            return dict(tweet_status=False)
