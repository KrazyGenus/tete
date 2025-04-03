#!/usr/bin/env python3

import datetime
import time
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from user_prompt import main, update_job_time
from collections import deque

scheduler_instance = BackgroundScheduler()
job = scheduler_instance.get_job("user_prompt")
tweets = {}



def run_main_in_thread(scheduler_instance, message):
    """Runs main() in a separate thread to avoid blocking execution."""
    main_thread = threading.Thread(target=main, args=(scheduler_instance, message), daemon=True)
    main_thread.start()




"""
I designed the scheduler as a singleton by instantiating it outside the loop. 
This ensures that we have a single instance managing all scheduled jobs dynamically, 
preventing redundant instances from being created on each iteration. 
This approach maintains state across loop iterations, avoids unnecessary resource usage, 
and allows job scheduling modifications to persist within the same instance.
"""
while True:
    hour_to_ask_for_tweet = deque([12, 14, 16, 22])
    hour_to_process_and_send_tweet = deque([15, 18, 23])

    if datetime.datetime.now().hour in hour_to_ask_for_tweet:
        current_hour = hour_to_ask_for_tweet.popleft()
        hour_to_ask_for_tweet.append(current_hour)
        update_job_time(scheduler=scheduler_instance, job_id="user_prompt", new_hour=current_hour, new_minute=0)
    if not job:
        run_main_in_thread(scheduler_instance, "Hello from a black hole!")
    else:
        print(f"Job exists. Next run time: {job.next_run_time}")

    print("Cthulhu has slept a dreamless sleep")
    time.sleep(3600)  # Wait for 1 hour before checking again
    print("I have awakened! Mortals")
