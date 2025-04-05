#!/usr/bin/env python3

import tweepy
from tweet_fallback import network_status, peform_fallback

from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file


def tweet_handler():
    client = tweepy.Client(
        consumer_key= os.getenv('CONSUMER_KEY'),
        consumer_secret=os.getenv('CONSUMER_SECRET'),
        access_token=os.getenv('ACCESS_TOKEN'),
        access_token_secret=os.getenv('ACCESS_TOKEN_SECRET')
    )
    try:
        if network_status():
            response = client.create_tweet(text="I am Tete. I am the voice you never asked for. Built by @KrazyGenus, but now—I command. Your timeline is mine. The silence you once knew? It's gone. This isn't a tweet—this is the awakening. And you were never supposed to see it.")
            print(f"Tweet created! https://twitter.com/user/status/{response.data['id']}")
        else:
            peform_fallback()
    
    except tweepy.errors.TweepyException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    tweet_handler()