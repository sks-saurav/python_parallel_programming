import threading
import time
import random

buffer = []
condition = threading.Condition()
BUFFER_LIMIT = 5

def producer():
    while True:
        with condition:  # Acquire the condition lock
            while len(buffer) >= BUFFER_LIMIT:
                print("Buffer is full. Producer is waiting...")
                condition.wait()  # Wait until notified

            # Produce an item and add it to the buffer
            item = random.randint(1, 100)
            buffer.append(item)
            print(f"Produced: {item}. Buffer: {buffer}")

            # Notify consumers that an item is available
            condition.notify()

        time.sleep(random.uniform(0.5, 1.5))  # Simulate production time

def consumer():
    while True:
        with condition:  # Acquire the condition lock
            while not buffer:
                print("Buffer is empty. Consumer is waiting...")
                condition.wait()  # Wait until notified

            # Consume an item from the buffer
            item = buffer.pop(0)
            print(f"Consumed: {item}. Buffer: {buffer}")

            # Notify producers that space is available
            condition.notify()

        time.sleep(random.uniform(0.5, 2.0))  # Simulate consumption time

# Create and start producer and consumer threads
producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

producer_thread.start()
consumer_thread.start()

# Let threads run indefinitely
producer_thread.join()
consumer_thread.join()
