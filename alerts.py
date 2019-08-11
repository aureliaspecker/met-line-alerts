from searchtweets import ResultStream, gen_rule_payload, load_credentials, collect_results
import json
import datetime as dt
import re
import pandas as pd

creds = load_credentials(filename="./credentials.yaml",
                        yaml_key="search_tweets_api",
                        env_overwrite=False)

mtn = dt.datetime.now() + dt.timedelta(hours=-1, minutes=-1)
maintenant = mtn.strftime("%Y%m%d%H%M")
print(maintenant)

hier = dt.date.today() + dt.timedelta(days=-1)
print(hier)

rule = gen_rule_payload("from:metline",from_date=str(hier), to_date=str(maintenant), results_per_call=100) 
print(rule)

tweets = collect_results(rule, result_stream_args=creds)

[print(tweet.created_at_datetime, tweet.all_text, end='\n\n') for tweet in tweets[0:50]];

tweet_text = []
tweet_date = []

for tweet in tweets: 
    tweet_text.append(tweet.all_text)
    tweet_date.append(tweet.created_at_datetime)

dataframe = pd.DataFrame({'tweet':tweet_text, 'date':tweet_date})

print(dataframe.head)

if 'no service' or 'closure' or 'Wembley Park' or 'Wembley Park station' or 'minor delays' or 'severe delays' or 'disruption' or 'delayed' or 'cancelled' or 'stadium' or 'show' or 'concert' or 'game' in dataframe.values[0]:
    print('Set up Tweet')
elif 'Baker Street station' in dataframe.values[0]:
    print('Send Tweet to Aurelia')
elif 'Hillingdon station' in dataframe.values[0]:
    print('Send Tweet to David')
else:
    pass

# Make sure Tweet is sent only once for each Tweet (i.e. adjust time accordingly
# Set up POST statuses/update with above logic