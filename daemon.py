#!/usr/bin/env python3

import datetime
import time
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from user_prompt import main, update_job_time
from collections import deque
from send_tweet import tweet_handler
from empty_tweet_fallback import fallback_tweet

import asyncio

scheduler_instance = BackgroundScheduler()
job = scheduler_instance.get_job("user_prompt")
tweets = [] # A list of dict containg the tweets with schema
hour_to_ask_for_tweet = deque([6, 12, 14, 16, 22])
hour_to_process_and_send_tweet = deque([15, 18, 23])

"""
{
   tweet: '',
   score: 0
}
"""



def run_main_in_thread(scheduler_instance, message, tweets):
    """Runs main() in a separate thread to avoid blocking execution."""
    main_thread = threading.Thread(target=main, args=(scheduler_instance, message, tweets), daemon=True)
    main_thread.start()

"""
I designed the scheduler as a singleton by instantiating it outside the loop. 
This ensures that we have a single instance managing all scheduled jobs dynamically, 
preventing redundant instances from being created on each iteration. 
This approach maintains state across loop iterations, avoids unnecessary resource usage, 
and allows job scheduling modifications to persist within the same instance.
"""
while True:
 
    
    """
    This this code is existing  for the sole purpose of knowing or watching when it's time to ask me for my thoughts
    """
    if not job:
        run_main_in_thread(scheduler_instance, "Hello from a black hole!", tweets)

    else:
        print("Job exists.")
        if datetime.datetime.now().hour in hour_to_ask_for_tweet:
            current_hour = hour_to_ask_for_tweet.popleft()
            hour_to_ask_for_tweet.append(current_hour)
            #for the minute get the current minute delta and  add seven or 3 or 10 it using delta
            update_job_time(scheduler=scheduler_instance, job_id="user_prompt", new_hour=current_hour, new_minute=21)
        
        
    """
    This code exist for the purpose of processing and sening out the tweets. 📨
    """
    if datetime.datetime.now().hour in hour_to_process_and_send_tweet:
        current_hour = hour_to_process_and_send_tweet.popleft()
        hour_to_process_and_send_tweet.append(current_hour)
        # i need to implment a fallback for when the tweets list empty.
        if len(tweets) == 0:
            fallback_tweet()
        else:
            tweet_handler()
    #run_send_tweet(tweets)
    
    print("Cthulhu has slept a dreamless sleep 😪")
    time.sleep(360)  # Wait for 1 hour before checking again
    print("I have awakened! Mortals 🐦‍🔥")
