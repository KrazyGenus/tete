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
    print(f"Heres whats on my mind: {answer}")
    tweets.append(answer)


def update_job_time(scheduler, job_id, new_hour, new_minute):
    """Update the scheduled job's execution time."""
    print("i am called")
    job = scheduler.get_job(job_id)
    if job:
        print(f"Updating job {job_id} to run at {new_hour}:{new_minute}")
        job.reschedule(trigger='cron', hour=new_hour, minute=new_minute)
    # scheduler.modify_job(
    #     job_id=job_id,  # Specify which job to modify
    #     trigger=CronTrigger(hour=new_hour, minute=new_minute)
    # )

def main(scheduler_instance, message: str, tweets: list):
    """Starts the scheduler and schedules the user prompt job."""
    
    # Add or replace the job dynamically
    scheduler_instance.add_job(
        prompt_user_taks, 
        trigger=CronTrigger(day_of_week='mon-sun', hour=12, minute=47),
        id="user_prompt", 
        args=[tweets], 
        max_instances=1,
        replace_existing=True  # ✅ No need to remove job manually
    )
    # runs the scheduler only when it's not already running
    if not scheduler_instance.running:
        scheduler_instance.start()
        print(f"Scheduler started. Press CTRL + C to exit.")
    else:
        print("Scheduler started Already Running BRo!")
  
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler_instance.shutdown()
        print("Scheduler stopped.")