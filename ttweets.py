import requests
import tauth
import db_utils
from Result import Result
from sentiment import Sentiment


def get_tweets(query):
    list_of_results = []
    token = tauth.get_bearer_token()

    response = requests.get(
        'https://api.twitter.com/1.1/search/tweets.json?',
        headers={"Authorization": "Bearer " + token},
        params={"q": query,
                "tweet_mode": "extended",
                "lang": "pt"})

    if response.status_code != 200:
        raise Exception("Cannot get a tweets (Status Code %d) Message: %s" % (response.status_code, response.text))

    body = response.json()
    if not body['statuses']:
        raise Exception("We don't have tweets to show");
    else:
        for tweet in body['statuses']:
            text = tweet['full_text']
            language = tweet['metadata']['iso_language_code']

            sentiment = Sentiment(text, language)

            result = Result(
                tweet['id'],
                tweet['user']['name'],
                text,
                sentiment.analyze_feeling(),
                tweet['favorite_count'],
                tweet['retweet_count'],
                tweet['created_at'],
            )
            list_of_results.append(result)

    db_utils.batch_tweet_insertion(list_of_results)

    return list_of_results
