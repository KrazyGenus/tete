#!/usr/bin/env python3
from google import genai

from dotenv import load_dotenv
import os
import json
import aiohttp
import asyncio
import re
load_dotenv()  # Load environment variables from .env file

client = genai.Client(api_key=os.getenv("GOOGLE_GEMENI_KEY"))


async def generate_story_for_tweet():
    img_path = "/home/krazygenus/Desktop/a.png"
    file_ref = client.files.upload(file=img_path)
    print(f'{file_ref=}')
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=["""Create a viral Twitter post for an anime-inspired design that connects with the anime community. The tweet should:
        
        1. Tell a short, engaging story related to the design — something emotional or thought-provoking that anime fans can relate to.
        
        2. Be playful and creative, using humor, emotion, or intrigue to spark engagement.
        
        3. Use popular and trending anime hashtags like #Anime, #Manga, #Otaku, #AnimeArt, #AnimeCommunity, #AnimeFanArt, #Cosplay, and #AnimeLove.
        
        4. Include a call to action (CTA) encouraging followers to share or comment.
        
        5. Be optimized for virality with emojis, clear language, and a tone that matches the excitement of anime fans.""",
                  file_ref])
    
    print(response.text)

    
async def judge_tweet_worthiness(tweet_text):
    """Asks the Twitter guru to judge a tweet's viral potential and returns a JSON schema."""
    prompt = f"""As a seasoned Twitter guru, analyze the following tweet and provide your judgment on its viral potential in the JSON schema format specified below.
    
    Tweet: "{tweet_text}"
    
    Schema:
    {{
        "tweet": "The analyzed tweet content",
        "virality_score": "A numerical score from 0 to 10 indicating the likelihood of the tweet going viral (0 being very unlikely, 10 being highly likely)",
        "discard": "A boolean value (true or false) indicating if the tweet is highly unlikely to gain any significant traction and should likely be discarded"
        }}
    
    Provide your response strictly in this JSON format:
    """
    response = await client.aio.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    return response.text

# Example Usage:
tweet1 = "Just spilled my coffee all over my important documents 😭 Anyone else having a Monday? #MondayMood #CoffeeFail"
judgment1 = asyncio.run(judge_tweet_worthiness(tweet1))
print(judgment1)
# judgment1 = judgment1.strip('```').strip('json')
# judgment1 = json.loads(judgment1)
# print(judgment1)
