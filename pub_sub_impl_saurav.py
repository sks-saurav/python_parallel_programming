from collections import defaultdict
import threading
import time

class MessageQueue:
    def __init__(self):
        self.messages = defaultdict(list)  # Messages for each topic
        self.subscriber_offsets = defaultdict(dict)  # Offsets for each subscriber per topic
        self.lock = threading.Lock()

    def publish(self, topic, message):
        """Publish a message to a topic."""
        with self.lock:
            self.messages[topic].append(message)
        print(f"Message published to topic '{topic}': {message}")

    def subscribe(self, subscriber, topic):
        """Subscribe a subscriber to a topic."""
        with self.lock:
            if subscriber not in self.subscriber_offsets[topic]:
                self.subscriber_offsets[topic][subscriber] = 0
        print(f"Subscriber '{subscriber}' subscribed to topic '{topic}'")

    def get_message(self, subscriber, topic):
        """Retrieve the next message for a subscriber on a topic."""
        with self.lock:
            offset = self.subscriber_offsets[topic].get(subscriber, 0)
            if offset < len(self.messages[topic]):
                message = self.messages[topic][offset]
                self.subscriber_offsets[topic][subscriber] += 1
                return message
            return None


class Publisher:
    def __init__(self, queue, name):
        self.queue = queue
        self.name = name

    def publish(self, topic, message):
        print(f"{self.name} publishing to topic '{topic}'")
        self.queue.publish(topic, message)


class Subscriber(threading.Thread):
    def __init__(self, queue, topic, name):
        super().__init__()
        self.queue = queue
        self.topic = topic
        self.name = name

    def run(self):
        self.queue.subscribe(self.name, self.topic)
        while True:
            message = self.queue.get_message(self.name, self.topic)
            if message:
                print(f"{self.name} received from topic '{self.topic}': {message}")
            else:
                time.sleep(1)  # Polling delay


# Main function to demonstrate the implementation
def main():
    message_queue = MessageQueue()

    # Create publishers
    publisher1 = Publisher(message_queue, "Publisher1")
    publisher2 = Publisher(message_queue, "Publisher2")

    # Create subscribers
    subscriber1 = Subscriber(message_queue, "topic1", "Subscriber1")
    subscriber2 = Subscriber(message_queue, "topic1", "Subscriber2")
    subscriber3 = Subscriber(message_queue, "topic2", "Subscriber3")

    # Start subscribers
    subscriber1.start()
    subscriber2.start()
    subscriber3.start()

    # Simulate publishing messages
    time.sleep(1)
    publisher1.publish("topic1", "Message 1 from Publisher1")
    time.sleep(1)
    publisher2.publish("topic1", "Message 2 from Publisher2")
    time.sleep(1)
    publisher1.publish("topic2", "Message 3 from Publisher1")


if __name__ == "__main__":
    main()


'''
# SIMPLE Variant:

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


'''