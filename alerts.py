from requests_oauthlib import OAuth1Session
import urllib.parse
import requests
from requests.auth import AuthBase
import datetime as dt
import yaml
import json

#Authentication
with open('./credentials.yaml') as file:
    data = yaml.safe_load(file)

consumer_key = data["labs_search_tweets_api"]["consumer_key"]
consumer_secret = data["labs_search_tweets_api"]["consumer_secret"]
access_token = data["labs_search_tweets_api"]["access_token"]
access_token_secret = data["labs_search_tweets_api"]["access_token_secret"]

oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

#Generate bearer token with consumer key and consumer secret via https://api.twitter.com/oauth2/token.
class BearerTokenAuth(AuthBase):
    def __init__(self, consumer_key, consumer_secret):
        self.bearer_token_url = "https://api.twitter.com/oauth2/token"
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.bearer_token = self.get_bearer_token()

    def get_bearer_token(self):
        response = requests.post(
            self.bearer_token_url,
            auth=(self.consumer_key, self.consumer_secret),
            data={'grant_type': 'client_credentials'},
            headers={'User-Agent': 'LabsRecentSearchQuickStartPython'})

        if response.status_code is not 200:
            raise Exception(f"Cannot get a Bearer token (HTTP %d): %s" % (response.status_code, response.text))

        body = response.json()
        return body['access_token']

    def __call__(self, r):
        r.headers['Authorization'] = f"Bearer %s" % self.bearer_token
        r.headers['User-Agent'] = 'LabsResearchSearchQuickStartPython'
        return r

#Create Bearer Token for authenticating
bearer_token = BearerTokenAuth(consumer_key, consumer_secret)

#Generate start_time and end_time parameters
utc = dt.datetime.utcnow() + dt.timedelta(minutes = -1)
utc_time = utc.strftime("%Y-%m-%dT%H:%M:%SZ")
print("end_time:", utc_time)

two_hours = dt.datetime.utcnow() + dt.timedelta(hours = -2, minutes = -1)
two_hours_prior = two_hours.strftime("%Y-%m-%dT%H:%M:%SZ")
print("start_time", two_hours_prior)

#Generate query and other parameters
query = urllib.parse.quote(f"from:metline -has:mentions")
print(query)
start_time = urllib.parse.quote(f"{two_hours_prior}")
print(start_time)
end_time = urllib.parse.quote(f"{utc_time}")
print(end_time)
tweet_format = urllib.parse.quote(f"compact")
print(tweet_format)

#Request URL
url = f"https://api.twitter.com/labs/1/tweets/search?query={query}&start_time={start_time}&end_time={end_time}&format={tweet_format}"
print(url)

#Request headers
headers = {
    "Accept-Encoding": "gzip"
}

response = requests.get(url, auth = bearer_token, headers = headers)

if response.status_code is not 200:
    raise Exception(f"Request reurned an error:{response.status_code}, {response.text}")

#Convert response to JSON & pull out Tweet text and creation date
parsed_response = json.loads(response.text)
print(parsed_response)
try:
    tweet_text = [tweet['text'] for tweet in parsed_response['data']]
    combined_tweet_text = " ".join(tweet_text)
    print(combined_tweet_text)
except:
    combined_tweet_text = " "

#Analyse Tweets
all_trigger = {'closure', 'wembley', 'delays', 'disruption', 'cancelled', 'sorry', 'stadium'}

david_trigger = {'hillingdon', 'harrow'}

aurelia_trigger = {'baker'}

tweet_words = set(combined_tweet_text.lower().split())

if len(tweet_words.intersection(all_trigger)) != 0: 
    message = "@AureliaSpecker and @_dormrod 👋 check https://twitter.com/metline for possible delays, [{}]".format(utc_time)
elif len(tweet_words.intersection(david_trigger)) != 0: 
    message = "@_dormrod Check https://twitter.com/metline for possible delays, [{}]".format(utc_time)
elif len(tweet_words.intersection(aurelia_trigger)) != 0:
    message = "@AureliaSpecker 👋 Check https://twitter.com/metline for possible delays, [{}]".format(utc_time)
else:
    message = "There are no delays"
    pass

print("Message:", message)

params = {"status": message}

oauth.post(
    "https://api.twitter.com/1.1/statuses/update.json", params=params
)