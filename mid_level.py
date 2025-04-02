#!/usr/bin/env python3

import asyncio
import aiohttp
import questionary
from questionary import Style
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.background import BackgroundScheduler

# Define the task to be executed
async def my_task(): 
    async with aiohttp.ClientSession() as session:
        async with session.get('https://jsonplaceholder.typicode.com/todos/1') as response:
            print(response.status)
            parsed_json = await response.json()
            print(f'Parsed JSON: {parsed_json}')


def prompt_user_taks():
    custom_style_fancy = Style([
        ('qmark', 'fg:#00bcd4 bold'),       # token in front of the question, giving it a calm but distinct tone
        ('question', 'fg:#4caf50 bold'),    # question text, with a confident and grounded green to signify logic and thoughtfulness
        ('answer', 'fg:#ff5722 bold'),      # submitted answer text, stands out with a vibrant orange for energy
        ('pointer', 'fg:#673ab7 bold'),     # pointer used in select and checkbox prompts, maintaining some personality here
        ('highlighted', 'fg:#009688 bold'), # pointed-at choice in select and checkbox prompts, a cool teal for focus
        ('selected', 'fg:#cc5454'),         # style for a selected item, fiery red to emphasize choice and commitment
        ('separator', 'fg:#9e9e9e'),        # separator in lists, subtle and neutral for better readability
        ('instruction', 'fg:#8e24aa italic'), # user instructions, adding some personality with a bit of purple
        ('text', 'fg:#fafafa'),             # plain text, light and easy on the eyes
        ('disabled', 'fg:#bdbdbd italic')   # disabled choices, soft grey for clarity but not distracting
    ])

    question = questionary.text("What's on your mind ?", style=custom_style_fancy)
    answer = question.ask()
    print(f"Heres whats on my mind: {answer} and it's types id {type(answer)}")


# Callback function to handle job event
def job_listener(event):
    if event.exception:
        print(f"Job {event.job_id} failed")
    else:
        print(f"Job {event.job_id} passed.")


# Create AsyncIOScheduler instance
scheduler = AsyncIOScheduler()
background_scheduler = BackgroundScheduler()

scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)


# Add job listener
scheduler.add_job(my_task, 'interval', seconds=5)
background_scheduler.add_job(prompt_user_taks, 'interval', seconds=5)


# Function to run the event loop
async def main():
    # Start the scheduler (this will integrate with the event loop)
    scheduler.start()
    background_scheduler.start()
    
    # Keep the event loop running
    await asyncio.sleep(1000)  # You can use this to keep the loop running indefinitely

# Run the event loop using asyncio.run()
asyncio.run(main())
