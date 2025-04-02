#!/usr/bin/env python3
import datetime
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
# from collections import deque

# while True:
#     # hour_time_stamps_queue = deque([12, 14, 16, 22])
#     # if datetime.datetime.now().hour in hour_time_stamps_queue:
#     #     current_hour = hour_time_stamps_queue.popleft()
#     #     hour_time_stamps_queue.append(current_hour)
#     print(datetime.datetime.now().hour)
#     time.sleep(3600)
# 
# 
def my_task():
    print("Task is being executed.....")


# initialize the scheduleer
scheduler = BackgroundScheduler()
scheduler.add_job(my_task, 'cron', hour=19, minute=57, id="daily_task", max_instances=1)


def update_job_time(scheduler, job_id, new_hour, new_minute):
    """Modiying the existing job to run a new time"""
    scheduler.modify_job(
        job_id = job_id,
        trigger=CronTrigger(hour=new_hour, minute=new_minute)
    )
try:
    while True:
        time.sleep(10)  # Keep script running
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    print("Scheduler stopped.")