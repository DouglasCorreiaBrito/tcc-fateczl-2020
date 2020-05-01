import requests
import tauth

def getTweets(query):
    token = tauth.getBearerToken()

    response = requests.get(
      'https://api.twitter.com/1.1/search/tweets.json?',
      headers={"Authorization": "Bearer " + token},
      params={"q": query})

    if response.status_code is not 200:
      raise Exception("Cannot get a tweets (Status Code %d) Message: %s" % (response.status_code, response.text))

    body = response.json()
    
    for tweet in body['statuses']:
        text = tweet['text']
        
        sentiment = "good|bad|neutral" #analyse text

        finalEntity = {
            "id": tweet['id'],
            "user": tweet['user']['name'],
            "text": text,
            "sentiment": sentiment,
            "favoriteCount": tweet['favorite_count'],
            "retweetCount": tweet['retweet_count'],
            "createdAt": tweet['created_at']
        }

        print(finalEntity)
        #insert entity on DB

getTweets('starwars')