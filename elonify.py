import os
from twilio.rest import Client
import tweepy
import logging
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

twilio_id = os.getenv('TWILIO_ACCOUNT_SID')
twilio_auth = os.getenv('TWILIO_AUTH_TOKEN')
twilio_number = os.getenv('TWILIO_NUMBER')

twitter_key = os.getenv('TWITTER_KEY')
twitter_secret = os.getenv('TWITTER_SECRET')
twitter_token = os.getenv('TWITTER_TOKEN')
twitter_token_secret = os.getenv('TWITTER_TOKEN_SECRET')


#TWILIO Secret
client = Client(twilio_id, twilio_auth)

keywords = ["stock", "share", "$", "doge", "crypto", "bitcoin", "dogefather", "SNL", "stonk", "dog", ]


# Return path to a given file based on current directory
def get_current_path(filename: str):
    if "src" in os.getcwd():
        return os.path.join(os.path.dirname(os.getcwd()), filename)
    else:
        return os.path.join(os.getcwd(), filename)



# TWITTER
logger = logging.getLogger()
def startup():
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


# TWILIO
def send_sms(body):
    client.messages.create(to="+381628467006", 
                       from_=twilio_number, 
                       body=body)


def tweet_engine(status):

    if any(tweet in status.text.lower() for tweet in keywords) and status.user.id_str == "792718816220422144":
        send_sms(f"Papa Elon Just Tweeted: {status.text}")
        #send_sms(f"Elon tweeted: {status.text} - on {time.ctime()}", False)
    # If no keywords match, check if there is an image



class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        tweet_engine(status)

def main():
    # Connect to the Twitter API
    api = startup()
    elon_tweet_listener = tweepy.Stream(auth=api.auth, listener=MyStreamListener())
    # '44196397' is the ID for the @elonmusk account
    # '792718816220422144' is mine
    elon_tweet_listener.filter(follow=["792718816220422144"], is_async=True)


if __name__ == "__main__":
    main()
