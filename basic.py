#!/usr/bin/env python3


from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import time


def my_job():
    print("Job has been executed, ya master!")

    print(time.tzname)

    
    
if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    run_time = datetime.datetime.now() + datetime.timedelta(seconds=5) # run 5 secs from the time the script is run
    scheduler.add_job(my_job, 'date', run_date=run_time)
    scheduler.start()
    
    print("Scheduler started. Press CTRL + C to exit.")
    
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Scheduler stopped.")