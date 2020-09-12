import requests
import keys

CONSUMER_KEY = keys.CONSUMER_KEY
CONSUMER_SECRET = keys.CONSUMER_SECRET


def get_bearer_token():
    response = requests.post(
        'https://api.twitter.com/oauth2/token',
        auth=(CONSUMER_KEY, CONSUMER_SECRET),
        data={'grant_type': 'client_credentials'})

    if response.status_code != 200:
        raise Exception(
            "Cannot get a Bearer token (Status Code %d) Message: %s" % (response.status_code, response.text))

    body = response.json()
    return body['access_token']
