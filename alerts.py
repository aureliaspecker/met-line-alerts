from searchtweets import ResultStream, gen_rule_payload, load_credentials, collect_results
from requests_oauthlib import OAuth1Session
import yaml
import json
import datetime as dt
import pandas as pd

creds = load_credentials(filename="./credentials.yaml",
                        yaml_key="search_tweets_api",
                        env_overwrite=False)

with open('./credentials.yaml') as file:
    data = yaml.safe_load(file)

consumer_key = data["search_tweets_api"]["consumer_key"]
consumer_secret = data["search_tweets_api"]["consumer_secret"]
access_token = data["search_tweets_api"]["access_token"]
access_token_secret = data["search_tweets_api"]["access_token_secret"]

oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

utc = dt.datetime.utcnow() + dt.timedelta(minutes=-1)
utc_time = utc.strftime("%Y%m%d%H%M")
print("toDate:", utc_time)

two_hours = dt.datetime.utcnow() + dt.timedelta(hours=-2, minutes=-1)
two_hours_prior = two_hours.strftime("%Y%m%d%H%M")
print("fromDate:", two_hours_prior)

rule = gen_rule_payload("from:metline -has:mentions",from_date=str(two_hours_prior), to_date=str(utc_time), results_per_call=100) 
print("rule:", rule)

tweets = collect_results(rule, 
                         max_results=100,
                         result_stream_args=creds)

[print(tweet.created_at_datetime, tweet.all_text, end='\n\n') for tweet in tweets[0:10]];

all_trigger = {'closure', 'wembley', 'delays', 'disruption', 'cancelled', 'sorry', 'stadium'}

david_trigger = {'hillingdon', 'harrow'}

aurelia_trigger = {'baker'}

tweet_text = []
tweet_date = []
combined_tweet_text = ''

for tweet in tweets: 
    tweet_text.append(tweet.all_text)
    tweet_date.append(tweet.created_at_datetime)
    combined_tweet_text += tweet.all_text

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