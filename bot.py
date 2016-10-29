#!/usr/bin/env python
import sys
from time import sleep
from twython import Twython, TwythonError
import subprocess

CONSUMER_KEY = 'xxxx'
CONSUMER_SECRET = 'xxxx'
ACCESS_TOKEN = 'xxxx'
ACCESS_SECRET = 'xxxx'

twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

def every_other(acc):
    try:
        orig_tl = twitter.get_user_timeline(screen_name=acc, count=1)
        orig_twt = orig_tl[0]
        orig_id = orig_twt['id_str']

        id = orig_id

        while True:
            g_timeline = twitter.get_user_timeline(screen_name=acc, count=1)
            g_tweet = g_timeline[0]
            g_id = g_tweet['id_str']
            if g_id != id:
                g_tweet = g_tweet['text'].split()
                g_tweet = ' '.join(g_tweet[::2])
                if 'http' in g_tweet:
                    link = g_tweet.index('http')
                    g_tweet = g_tweet[:link]
                twitter.update_status(status=g_tweet)
                print('tweeted: ' + g_tweet)
                id = g_id
                sleep(20)
                continue
            else:
                sleep(20)
                continue
    except TwythonError as e:
        print(e)        
        sleep(20)
        every_other(acc)

# prints a random tweet
def random():
    try:
        while True:
            for letter in string.lowercase:
                results = twitter.search(q=letter + ' filter:safe', count=1, lang='en')
                for result in results['statuses']:
                    tweet = result['text']
                    tweet = tweet.split()
                    for item in tweet[:]:
                        if '@' in item or 'http' in item:
                            tweet.remove(item)
                    tweet = ' '.join(tweet)
                    twitter.update_status(status=tweet + '\n')
                    print('tweeted: ' + tweet + '\n')
                    sleep(300)
    except TwythonError as e:
        print(e)
        sleep(20)
        random()
        
random()
