from searchtweets import ResultStream, gen_rule_payload, load_credentials, collect_results
import requests
from requests_oauthlib import OAuth1Session
import yaml
import json
import datetime as dt
import pandas as pd

creds = load_credentials(filename="./credentials.yaml",
                        yaml_key="search_tweets_api",
                        env_overwrite=False)

utc = dt.datetime.utcnow() + dt.timedelta(minutes=-1)
utc_time = utc.strftime("%Y%m%d%H%M")
print("utc time:", utc_time)

two_hours = dt.datetime.utcnow() + dt.timedelta(hours=-2, minutes=-1)
two_hours_prior = two_hours.strftime("%Y%m%d%H%M")
print("UTC -2 hours:", two_hours_prior)

rule = gen_rule_payload("from:metline -has:mentions",from_date=str(two_hours_prior), to_date=str(utc_time), results_per_call=100) 
print("rule:", rule)

tweets = collect_results(rule, 
                         max_results=100,
                         result_stream_args=creds)

[print(tweet.created_at_datetime, tweet.all_text, end='\n\n') for tweet in tweets[0:10]];

tweet_text = []
tweet_date = []

for tweet in tweets: 
    tweet_text.append(tweet.all_text)
    tweet_date.append(tweet.created_at_datetime)

print("Tweet Date", tweet_date)
print("Tweet Text", tweet_text)

df = pd.DataFrame({'tweet':tweet_text, 'date':tweet_date})

print("DF", df.head)


# TODO: simplify to not have all of these elifs 

# delays = ['hillingdon', 'baker street', 'no service', 'closure', 'Wembley Park', 'delays', 'disruption', 'cancelled', 'sorry', 'stadium']

# hillingdon = ['Hillingdon']

# bakerstreet = ['Baker Street']

# if not tweet_text:
#     message = "There are no delays"
# elif [i for i in delays if(i in tweet_text)]:
#     message = "There is a delay"
# else: 
#     pass

if not tweet_text:
    message = "There are no delays"
elif 'no service' in df['tweet'].values[0]:
    message = "@re_testing & David 👋 check https://twitter.com/metline for possible delays"
elif 'closure' in df['tweet'].values[0]:
    message = "@re_testing & David 👋 check https://twitter.com/metline for possible delays"
elif 'Wembley Park' in df['tweet'].values[0]:
    message = "@re_testing & David 👋 check https://twitter.com/metline for possible delays"
elif 'delays' in df['tweet'].values[0]:
    message = "@re_testing & David 👋 check https://twitter.com/metline for possible delays"
elif 'disruption' in df['tweet'].values[0]:
    message = "@re_testing & David 👋 check https://twitter.com/metline for possible delays"
elif 'cancelled' in df['tweet'].values[0]:
    message = "@re_testing & David 👋 check https://twitter.com/metline for possible delays"
elif 'sorry' in df['tweet'].values[0]:
    message = "@re_testing & David 👋 check https://twitter.com/metline for possible delays"
elif 'stadium' in df['tweet'].values[0]:
    message = "@re_testing & David 👋 check https://twitter.com/metline for possible delays"
elif 'Baker Street' in df['tweet'].values[0]:
    message = "@re_testing 👋 Check https://twitter.com/metline for possible delays"
elif 'Hillingdon' in df['tweet'].values[0]:
    message = "David 👋 Check https://twitter.com/metline for possible delays"
else:
    message = "There are no delays"
    pass

print("Message:", message)

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

params = {"status": message}

oauth.post(
    "https://api.twitter.com/1.1/statuses/update.json", params=params
)