#!/usr/bin/env python3

import tweepy
from tweet_fallback import network_status, peform_fallback

from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file


# OAuth 1.0a for both v1.1 and v2
auth = tweepy.OAuth1UserHandler(
    consumer_key= os.getenv('CONSUMER_KEY'),
    consumer_secret=os.getenv('CONSUMER_SECRET'),
    access_token=os.getenv('ACCESS_TOKEN'),
    access_token_secret=os.getenv('ACCESS_TOKEN_SECRET')
) 

# Create both API and Client
api = tweepy.API(auth)  # v1.1 (for media upload)
client = tweepy.Client(
    consumer_key= os.getenv('CONSUMER_KEY'),
    consumer_secret=os.getenv('CONSUMER_SECRET'),
    access_token=os.getenv('ACCESS_TOKEN'),
    access_token_secret=os.getenv('ACCESS_TOKEN_SECRET')
)

def tweet_handler(tweet:str, image_path:str):
    try:
        if network_status():
            # upload media using the V1 API
            media = api.media_upload(image_path)
            # Post tweet using API v2 and the uploaded media_id
            print(image_path, type(tweet))
            response = client.create_tweet(text="Lost in the bustling souk, he found solace only in the call to prayer.  This anime-inspired art captures that quiet strength, that moment of peace amidst the chaos.  Relatable? 🥺  Get your own piece of this soulful story! ✨ [Link to merch] #Anime #Manga #Otaku #AnimeArt", media_ids=[media.media_id])
            print(f"Tweet created! https://twitter.com/user/status/{response.data['id']}")
        else:
            peform_fallback()
    
    except tweepy.errors.TweepyException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    tweet_handler()