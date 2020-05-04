import requests

CONSUMER_KEY = "mCnA96cficCAlg6QiW9QVWYVL"
CONSUMER_SECRET = "1tXe5YXalOSKEEAyD11MCmdK7Brw93HKUaXYf2Ac91syNC1YA6" 

def getBearerToken():
    response = requests.post(
      'https://api.twitter.com/oauth2/token', 
      auth=(CONSUMER_KEY, CONSUMER_SECRET),
      data={'grant_type': 'client_credentials'})

    if response.status_code is not 200:
      raise Exception("Cannot get a Bearer token (Status Code %d) Message: %s" % (response.status_code, response.text))

    body = response.json()
    return body['access_token']