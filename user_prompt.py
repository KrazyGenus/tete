#!/usr/bin/env python3
import questionary
from questionary import Style
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.background import BackgroundScheduler
import time

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



if __name__ == "__main__":
    bg_job = BackgroundScheduler()
    bg_job.add_job(prompt_user_taks, 'cron', day_of_week='mon-sun', hour=12, minute=45, max_instances=1)
    bg_job.start()
    
    print("Scheduler started. Press CTRL + C to exit.")
    
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        bg_job.shutdown()
        print("Scheduler stopped.")