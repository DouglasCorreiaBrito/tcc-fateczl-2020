from twitter import *
import json

TOKEN = "1116688168105979910-OELUUatGSu5uArhG1QGV2NLPWvWmBH"
TOKEN_KEY = "aWBAnGsZS6Dzuol69UbzIdoPbJXsszlqH8PtVi7sMCufh"
CON_SECRET = "1tXe5YXalOSKEEAyD11MCmdK7Brw93HKUaXYf2Ac91syNC1YA6"
CON_SECRET_KEY = "mCnA96cficCAlg6QiW9QVWYVL"

numberOfTweets = 10

twitter_stream = TwitterStream(
    auth=OAuth(TOKEN, TOKEN_KEY,
               CON_SECRET_KEY, CON_SECRET))

iterator = twitter_stream.statuses.sample()

for tweet in iterator:
    if('text' in tweet):
        print(tweet['text'])