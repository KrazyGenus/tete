#!/usr/bin/env python3
import questionary
from questionary import Style
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.triggers.cron import CronTrigger

import time

def prompt_user_taks(tweets:list):
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
    tweets.append({'tweet':answer,'score': 0}) # All tweet will start with a score of 0 to be increased by the LLM


def update_job_time(scheduler, job_id, new_hour, new_minute):
    scheduler.modify_job(
        job_id = job_id,
        trigger=CronTrigger(hour=new_hour, minute=new_minute)
    )

def main(scheduler_instance, message:str, tweets:list):
    scheduler_instance.add_job(prompt_user_taks, 'cron', day_of_week='mon-sun', hour=14, minute=2, id="user_prompt", args=[tweets], max_instances=1)
    scheduler_instance.start()
    
    print(f"Scheduler started. Press CTRL + C to exit. with the message {message}")
    
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler_instance.shutdown()
        print("Scheduler stopped.")
