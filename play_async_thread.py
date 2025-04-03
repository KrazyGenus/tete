import asyncio
import threading

async def tweet_handler(tweets):
    await asyncio.sleep(2)  # Simulate async work
    print(f"{tweets}")
    return tweets

# Function to run async function in a separate thread and return result
def run_send_tweet_in_thread(future, tweets):
    def thread_target():
        loop = asyncio.new_event_loop()  # Create a new event loop for the thread
        asyncio.set_event_loop(loop)  # Set the event loop for this thread
        result = loop.run_until_complete(tweet_handler(tweets))
        future.set_result(result)  # Set the result in the future object

    tweet_thread = threading.Thread(target=thread_target, daemon=True)
    tweet_thread.start()  # Start the thread without blocking the main thread

def main():
    future = asyncio.Future()
    
    run_send_tweet_in_thread(future, "Hi, from a black hole")
    
    # The main thread can continue running other tasks here without waiting for the worker thread
    print("Main thread is not blocked.")
    
    # If you need to access the result of the async task, do so later:
    print(f"Result from async task: {future.result()}")

if __name__ == "__main__":
    main()
