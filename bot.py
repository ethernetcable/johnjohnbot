#!/usr/bin/env python
from time import sleep
from twython import Twython, TwythonError
import string

# get your own api stuff you lazy so and so
CONSUMER_KEY = 'xxxx'
CONSUMER_SECRET = 'xxxx'
ACCESS_TOKEN = 'xxxx'
ACCESS_SECRET = 'xxxx'

twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

# tweets every other word of someone's tweets for some reason
def every_other(acc):
    try:
        # get id of latest tweet
        orig_tl = twitter.get_user_timeline(screen_name=acc, count=1)
        orig_twt = orig_tl[0]
        orig_id = orig_twt['id_str']
        while True:
            # gets id of latest tweet on timeline every 20 secs
            g_timeline = twitter.get_user_timeline(screen_name=acc, count=1)
            g_tweet = g_timeline[0]
            g_id = g_tweet['id_str']
            if g_id != orig_id: # in case of new tweet
                g_tweet = g_tweet['text'].split()
                g_tweet = ' '.join(g_tweet[::2])
                # remove links
                if 'http' in g_tweet:
                    link = g_tweet.index('http')
                    g_tweet = g_tweet[:link]
                # tweet the thing
                twitter.update_status(status=g_tweet)
                print('tweeted: ' + g_tweet)
                orig_id = g_id
                sleep(20)
                continue
            else:
                sleep(20)
                continue
    # in case of random death
    except TwythonError as e:
        print(e)        
        sleep(20)
        every_other(acc)

# tweets a first tweet on searching a letter of the alphabet - essentially random
def random():
    try:
        while True:
            # search each letter of the alphabet
            for letter in string.lowercase:
                results = twitter.search(q=letter + ' filter:safe', count=1, lang='en')
                for result in results['statuses']:
                    tweet = result['text']
                    tweet = tweet.split()
                    # remove usernames, links and RT
                    for item in tweet[:]:
                        if '@' in item or 'http' in item or 'RT' in item:
                            tweet.remove(item)
                    tweet = ' '.join(tweet)
                    # tweet the thing
                    twitter.update_status(status=tweet + '\n')
                    print('tweeted: ' + tweet + '\n')
                    sleep(300)
    # in case of random death
    except TwythonError as e:
        print(e)
        sleep(20)
        random()
