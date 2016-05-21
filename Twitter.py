import twython
from twython import Twython
from twython import TwythonStreamer
from datetime import datetime

time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
APP_KEY = "96Tt52kGGi9TKPK3ytUnB9qa7"
APP_SECRET = "fEB5Oh3GaqVIPxRzPqdKIVgV5HiAI0NLkXBjzqPaVykDddNZv2"

ACCESS_TOKEN = "724279780137418754-lZaytDXafLfR76rybHeOTws2jgFe2vu"
ACCESS_KEY = "lkNCMtVklkzgxdkg4P21KzJX2Z35RhIJidOdFhAcINN93"

#   create twython object -> initiate connection to specified twitter account -> key's are specific to each account.
twitter = Twython(APP_KEY, APP_SECRET, ACCESS_TOKEN, ACCESS_KEY)


def tweet_with_photo(url):
    user_tweet = input("What do you want your tweet to say?: ")
    try:
        photo = open(str(url), 'rb')
        response = twitter.upload_media(media=photo)
        twitter.update_status(status=user_tweet + " tweeted@ " + time, media_ids=[response['media_id']])
    except twython.TwythonError:
        print("Error has occurred while uploading tweet.. this is bad.")
    else:
        print("Tweet has been uploaded.")


def tweet(message):
    try:
        twitter.update_status(status=message)
    except twython.TwythonError:
        print("Error occurred while posting tweet.. this is bad.")
    else:
        print("Tweet successfully sent.")

