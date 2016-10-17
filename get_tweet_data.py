#!/usr/bin/env python
"""Simple script to fetch data from the bslparlour home stream"""

import datetime
import os
import subprocess as sp
import yaml

import tweepy

import myconf

def dictify(results):
    return_dict = dict()
    for result in results:
        return_dict[result.id] = result

    return return_dict


def merge_all_yamls(tweet_data_dir="tweet_data"):
    yamls = []
    for f in os.listdir(tweet_data_dir):
        yamls.append(yaml.load(open(os.path.join(tweet_data_dir, f), "r")))

    all_yamls_gen = (dictify(x) for x in yamls)
    all_yamls = dict()
    for x in all_yamls_gen:
        all_yamls.update(x)

    return all_yamls

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

    all_yamls = merge_all_yamls()
    try:
        all_yamls_previous = yaml.load(open("tweet_data/tweepy_all.yaml", "r"))
    except FileNotFoundError:
        all_yamls_previous = dict()

    if len(all_yamls_previous) < len(all_yamls):
        with open("tweet_data/tweepy_all.yaml", "w") as f:
            yaml.dump(all_yamls, f)

        # Commit to repo
        sp.check_call("git add tweet_data/* && git commit -m 'Automated data commit.' && git push",
                      shell=True)


if __name__ == '__main__':
    main()
