from nltk import tokenize
import requests
import tauth
import text_treatment
from sentiment import Sentiment
import illustrator


def get_tweets(query):
    negative_words = list()
    positive_words = list()
    token = tauth.get_bearer_token()

    response = requests.get(
        'https://api.twitter.com/1.1/search/tweets.json?',
        headers={"Authorization": "Bearer " + token},
        params={"q": query, "tweet_mode": "extended"})

    if response.status_code != 200:
        raise Exception("Cannot get a tweets (Status Code %d) Message: %s" % (response.status_code, response.text))

    body = response.json()
    for tweet in body['statuses']:
        text = tweet['full_text']
        language = tweet['metadata']['iso_language_code']
        text = text_treatment.treat_for_wordcloud(text)
        token_space = tokenize.WhitespaceTokenizer()
        word_list = token_space.tokenize(text)
        for word in word_list:
            sentiment = Sentiment(word, language)
            analyzed_word = sentiment.analyze_feeling()
            positive_words.append(word) if analyzed_word == 'pos' else negative_words.append(word)

    return ' '.join(negative_words), ' '.join(positive_words)
