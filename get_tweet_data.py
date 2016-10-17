#!/usr/bin/env python
"""Simple script to fetch data from the bslparlour home stream"""

import yaml
import datetime
import tweepy

import myconf

def main():
    tweepy_auth = tweepy.OAuthHandler(
        myconf.consumer_key,
        myconf.consumer_secret,
    )
    tweepy_auth.set_access_token(
        myconf.access_key,
        myconf.access_secret,
    )
    tweepy_api = tweepy.API(tweepy_auth)
    timestamp = datetime.datetime.now().timestamp()
    with open("tweet_data/tweepy_{}.yaml".format(timestamp), "w") as f:
        yaml.dump(tweepy_api.home_timeline(count=40), f)

if __name__ == '__main__':
    main()
