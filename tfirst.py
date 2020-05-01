from twitter import *

TOKEN = ""
TOKEN_KEY = ""
CON_SECRET = ""
CON_SECRET_KEY = ""

numberOfTweets = 10

t = Twitter(
    auth=OAuth(TOKEN, TOKEN_KEY,
               CON_SECRET, CON_SECRET_KEY))

def showTweets(x, num):
    for i in range(0, num):
        name = (x[i]['user']['screen_name'])
        text = (x[i]['text'])
        print(name + ": " +text)

def getTweets():
    x = t.statuses.home_timeline(screen_name="gustuxd2")
    return x


showTweets(getTweets(), numberOfTweets)
