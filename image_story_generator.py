#!/usr/bin/env python3
import google.generativeai as genai

from dotenv import load_dotenv
from send_tweet import tweet_handler
import os
import asyncio

load_dotenv()  # Load environment variables from .env file

# Configure the Gemini API
try:
    api_key = os.getenv("GOOGLE_GEMENI_KEY")
    if not api_key:
        raise EnvironmentError("GOOGLE_GEMENI_KEY environment variable not set. Please create a .env file with this key.")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except EnvironmentError as e:
    print(f"Error: {e}")
    exit()
except Exception as e:
    print(f"Error initializing Gemini API: {e}")
    exit()

async def generate_story_for_tweet(image_path):
    """Generates a viral tweet with a short story related to an image."""
    try:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
        
        contents = [
            {
                "role": "user",
                "parts": [
                    "Create a single, viral Twitter post for this anime-inspired design. The tweet should:\n\n",
                    "1. Tell a short, emotional or thought-provoking story about the design that anime fans can relate to.\n\n",
                    "2. Be playful, creative, and engaging, using humor or emotion to spark interest.\n\n",
                    "3. Use only **four** popular anime hashtags like #Anime and #Manga.\n\n",
                    "4. Include a clear call to action (CTA) encouraging followers to click on the link to get the merch.\n\n",
                    "5. Stay within Twitter's 280-character limit, including emojis.\n\n",
                    {
                        "mime_type": "image/png",
                        "data": image_data
                    }
                ]
            }
        ]


        response =  model.generate_content(contents)
        response.resolve() # This will raise an exception if the response has an error

        if response.text:
            print("Generated Tweet:")
            print(response.text)
            tweet_handler(response.text, image_path)
        else:
            print("No text generated in the response.")

    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    image_file_path = "/home/krazygenus/Desktop/a.png"  # Replace with the actual path to your image
    asyncio.run(generate_story_for_tweet(image_file_path))