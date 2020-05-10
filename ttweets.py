import requests
import tauth
from tsentiment import TSentiment

def get_tweets(query):
    token = tauth.get_bearer_token()

    response = requests.get(
      'https://api.twitter.com/1.1/search/tweets.json?',
      headers={"Authorization": "Bearer " + token},
      params={"q": query,
            "tweet_mode": "extended"})

    if response.status_code != 200:
      raise Exception("Cannot get a tweets (Status Code %d) Message: %s" % (response.status_code, response.text))

    body = response.json()

    file1 = open("MyFile.json","a") 
    file1.write(response.text)
    
    for tweet in body['statuses']:
        text = tweet['full_text']
        language = tweet['metadata']['iso_language_code']

        sentiment = TSentiment(text,language)

        final_entity = {
            "id": tweet['id'],
            "user": tweet['user']['name'],
            "text": text,
            "sentiment": sentiment.analyze_feeling(),
            "favoriteCount": tweet['favorite_count'],
            "retweetCount": tweet['retweet_count'],
            "createdAt": tweet['created_at'],
            "countAnalysis": 1
        }
        
        print(final_entity)
        # insert entity on DB



get_tweets('Bolsonaro')
