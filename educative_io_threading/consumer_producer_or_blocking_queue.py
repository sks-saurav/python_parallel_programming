# '''
# # Blocking Queue | Bounded Buffer | Consumer Producer
# A blocking queue is defined as a queue which blocks the caller of the enqueue method if there's no more 
# capacity to add the new item being enqueued. Similarly, the queue blocks the dequeue caller if there are 
# no items in the queue. Also, the queue notifies a blocked enqueuing thread when space becomes available 
# and a blocked dequeuing thread when an item becomes available in the queue.
# '''
from threading import Thread, Condition, current_thread
import time
import random

class BlockingQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = []
        self.cond = Condition()
    
    def enqueue(self, item):
        with self.cond:
            while len(self.queue) == self.capacity:
                self.cond.wait()
            self.queue.append(item)
            self.cond.notify_all()
    
    def dequeue(self):
        with self.cond:
            while len(self.queue) == 0:
                self.cond.wait()
            item = self.queue.pop(0)
            self.cond.notify_all()
            return item

def consumer_thread(q):
    while 1:
        item = q.dequeue()
        print("\n{0} consumed item {1}".format(current_thread().name, item), flush=True)
        time.sleep(random.randint(1, 3))


def producer_thread(q, val):
    item = val
    while 1:
        q.enqueue(item)
        item += 1
        time.sleep(0.1)


if __name__ == "__main__":
    blocking_q = BlockingQueue(5)

    consumerThread1 = Thread(target=consumer_thread, name="consumer-1", args=(blocking_q,), daemon=True)
    consumerThread2 = Thread(target=consumer_thread, name="consumer-2", args=(blocking_q,), daemon=True)
    producerThread1 = Thread(target=producer_thread, name="producer-1", args=(blocking_q, 1), daemon=True)
    producerThread2 = Thread(target=producer_thread, name="producer-2", args=(blocking_q, 100), daemon=True)

    consumerThread1.start()
    consumerThread2.start()
    producerThread1.start()
    producerThread2.start()

    time.sleep(15)
    print("Main thread exiting")