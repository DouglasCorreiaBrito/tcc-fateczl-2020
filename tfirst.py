from twitter import *
import json

TOKEN = "1116688168105979910-OELUUatGSu5uArhG1QGV2NLPWvWmBH"
TOKEN_KEY = "aWBAnGsZS6Dzuol69UbzIdoPbJXsszlqH8PtVi7sMCufh"
CON_SECRET = "1tXe5YXalOSKEEAyD11MCmdK7Brw93HKUaXYf2Ac91syNC1YA6"
CON_SECRET_KEY = "mCnA96cficCAlg6QiW9QVWYVL"

numberOfTweets = 10

t = Twitter(
    auth=OAuth(TOKEN, TOKEN_KEY,
               CON_SECRET_KEY, CON_SECRET))

def showTweets(x, num):
    for i in range(0, num):
        name = (x[i]['user']['screen_name'])
        text = (x[i]['text'])
        #print(name + ": " +text)
        file1 = open("MyFile.json","a") 
        file1.write(json.dumps(x[i]) + ",")
        

def getTweets():
    x = t.statuses.home_timeline(tweet_mode="extended")
    return x


showTweets(getTweets(), numberOfTweets)
