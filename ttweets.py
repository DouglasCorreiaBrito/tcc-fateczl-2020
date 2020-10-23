from nltk import tokenize
import requests
import tauth
import db_utils
import text_treatment
from Result import Result
from sentiment import Sentiment


def get_tweets(query):
    list_of_results = []
    negative_words = []
    positive_words = []
    token = tauth.get_bearer_token()

    response = requests.get(
        'https://api.twitter.com/1.1/search/tweets.json?',
        headers={"Authorization": "Bearer " + token},
        params={"q": query,
                "tweet_mode": "extended",
                "lang": "pt"})

    if response.status_code != 200:
        raise Exception("Cannot get a tweets (Status Code %d) Message: %s" % (
            response.status_code, response.text))

    body = response.json()
    if not body['statuses']:
        raise Exception("We don't have tweets to show")
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

            text_wordcloud = text_treatment.treat_for_wordcloud(text)
            token_space = tokenize.WhitespaceTokenizer()
            word_list = token_space.tokenize(text_wordcloud)
            for word in word_list:
                sentiment = Sentiment(word, language)
                analyzed_word = sentiment.analyze_feeling()
                positive_words.append(
                    word) if analyzed_word == 'pos' else negative_words.append(word)

    persist_search(query=query, results=list_of_results)
    return list_of_results, ' '.join(positive_words), ' '.join(negative_words)

def persist_search(query, results):
    query = text_treatment.treat_search_terms(query)
    query_array = query.split(' ')
    term_list = "','".join(query.split(' '))

    print(term_list)

    values = []
    for value in query_array:
        values.append((value, 0))

    db_utils.execute_many(sql='INSERT IGNORE INTO search_terms (term, search_qty) VALUES (%s, %s)', values=values)

    db_utils.execute(sql="UPDATE search_terms SET search_qty = (search_qty + 1) WHERE term IN ('"+ term_list +"')")

    db_utils.batch_tweet_insertion(results)

    return