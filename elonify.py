import os
from twilio.rest import Client
import tweepy
import logging
from dotenv import load_dotenv

load_dotenv()

#Secrets
twilio_id = os.getenv('TWILIO_ACCOUNT_SID')
twilio_auth = os.getenv('TWILIO_AUTH_TOKEN')
twilio_number = os.getenv('TWILIO_NUMBER')

my_number = os.getenv('MY_NUMBER')

twitter_key = os.getenv('TWITTER_KEY')
twitter_secret = os.getenv('TWITTER_SECRET')
twitter_token = os.getenv('TWITTER_TOKEN')
twitter_token_secret = os.getenv('TWITTER_TOKEN_SECRET')


#TWILIO
client = Client(twilio_id, twilio_auth)

keywords = ["dogefather",  "dog", "doge", "stock", "stonk", "share", "$", "crypto", "bitcoin", "btc" "SNL", "AI", "hodl"]

logger = logging.getLogger()
def startup():
    # TWITTER
    auth = tweepy.OAuthHandler(twitter_key, twitter_secret)
    auth.set_access_token(twitter_token, twitter_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
    try:
        api.verify_credentials()
    except tweepy.TweepError as e:
        logger.error("Check credentials!!!", exc_info=True)
        raise e
    logger.info("Started")
    return api


def send_sms(body):
    # twilio
    client.messages.create(to=my_number, 
                       from_=twilio_number, 
                       body=body)


def tweet_engine(status):
    #check for tweets
    if any(tweet in status.text.lower() for tweet in keywords) and status.user.id_str == "792718816220422144":
        send_sms(f"Papa Elon Just Tweeted:\n{status.text}.\n URL : https://mobile.twitter.com/elonmusk/status/{status.id}")

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        tweet_engine(status)

def main():
    # Connect to the Twitter API
    api = startup()
    elon_tweet_listener = tweepy.Stream(auth=api.auth, listener=MyStreamListener())
    # '44196397' is the ID for the @elonmusk account
    # '792718816220422144' is mine, for testing purposes
    elon_tweet_listener.filter(follow=["792718816220422144"], is_async=True)


if __name__ == "__main__":
    main()
