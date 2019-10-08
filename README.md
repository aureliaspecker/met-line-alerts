# Metline alerts

This app uses the Twitter API to set up bespoke notifications related to public transport delays. 

I use London's TfL Metropolitan line to commute every day to and from work. The Metropolitan line has an active Twitter account, [@metline](https://twitter.com/metline?lang=en), where you can find realtime updates on delays and cancellations. But not all Tweets sent from [@metline](https://twitter.com/metline?lang=en) are relevant to me. I built this application to monitor the account [@metline](https://twitter.com/metline?lang=en) for relevant Tweets. Each time a Tweet of interest is created, I receive a notification (via a Tweet that @mentions). 

### Resources

You can follow the steps outlined in this blog post[INSERT LINK] to reproduce this application.

You will also need:
* [Twitter developer account](https://developer.twitter.com/en/account/get-started)
* [Twitter developer app](https://developer.twitter.com/en/apps)
* [Search Tweets Python wrapper](https://github.com/twitterdev/search-tweets-python)
* A Twitter account to monitor for Tweets of interest, in this case [@metline](https://twitter.com/metline?lang=en)
* Two Twitter accounts: one from which to post about delays and another from which to receive notifications
