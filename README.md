# Metline alerts

This app uses the Twitter API to set up bespoke notifications for public transport delays. 

I use London's TfL Metropolitan line to commute every day to and from work. The Metropolitan line has an active Twitter account, [@metline](https://twitter.com/metline?lang=en), where you can find realtime updates on delays and cancellations. But not all Tweets sent from [@metline](https://twitter.com/metline?lang=en) are relevant to me. I built this application to monitor the account [@metline](https://twitter.com/metline?lang=en) for relevant Tweets. Each time a Tweet of interest is created, I receive a notification (by sending a Tweet that @mentions me). 

### Resources

COMING SOON: related blog post to help you reproduce this app.

You will need the following

* Choose a Twitter account that Tweets information of interest (in this case [@metline](https://twitter.com/metline?lang=en)). 
* Twitter account(s) of the notification recipient(s), in other words the commuter(s). For this, I used my primary Twitter account ([@AureliaSpecker](https://twitter.com/AureliaSpecker)).
* Twitter account of the notification sender. For this, I used a secondary Twitter account ([@maddie_testing](https://twitter.com/maddie_testing)).
* [Twitter developer account](https://developer.twitter.com/en/account/get-started): if you don’t have one already, you can apply for one. The developer account should be linked to the Twitter account of the notification sender (in this example: [@maddie_testing](https://twitter.com/maddie_testing)).
* [Twitter developer app](https://developer.twitter.com/en/apps)
* [Access keys and tokens](https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens) for the app you created above
* Set up your [dev environment](https://developer.twitter.com/en/account/environments) for "Search Tweets: 30-DaysSandbox"  to something like dev or prod
* Have [pip](https://pip.pypa.io/en/stable/installing/) installed on your laptop
* Python version 3.6 or above (in your command line, you can check what version of Python is installed by running `$ python --version`)

### Credentials

Create a `credentials.yaml` file and subsequently add it to your `.gitignore` file. 

In `credentials.yaml`, add your access keys and tokens in the format below. Replace {ENV} with the dev environment name you set up in the [developer portal](https://developer.twitter.com/en/account/environments) and insert your access keys and tokens for each field accordingly.

```
search_tweets_api:
  account_type: premium
  endpoint: https://api.twitter.com/1.1/tweets/search/30day/{ENV}.json
  consumer_key: XXXXXXXXXX
  consumer_secret: XXXXXXXXXX
  access_token: XXXXXXXXXX
  access_token_secret: XXXXXXXXXX
```

