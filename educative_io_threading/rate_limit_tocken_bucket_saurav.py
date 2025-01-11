'''
# Rate Limiting Using Token Bucket Filter
This is an actual interview question asked at Uber and Oracle.

Imagine you have a bucket that gets filled with tokens at the rate of 1 token per second. 
The bucket can hold a maximum of N tokens. Implement a thread-safe class that lets threads 
get a token when one is available. If no token is available, then the token-requesting threads should block.

The class should expose an API called get_token() that various threads can call to get a token.
'''

from threading import Thread, Condition, current_thread
import time

class TockenBucket():
    def __init__(self, capacity, fill_rate):
        self.capacity = capacity
        self.fill_rate = fill_rate
        self.cond = Condition()
        self.avl_tokens = 0

    def get_token(self):
        with self.cond:
            while self.avl_tokens == 0:
                self.cond.wait()

            self.avl_tokens -= 1
            self.cond.notify_all()
            return True

    def add_token(self):
        while True:
            with self.cond:
                if self.avl_tokens < self.capacity:
                    self.avl_tokens += 1
                    self.cond.notify_all()
            time.sleep(self.fill_rate)

def token_filler_worker(bucket):
    print('Token filler started')
    bucket.add_token()

def token_consumer_worker(bucket):
    for i in range(10):
        if bucket.get_token():
            print(f'{current_thread().name} Got token at {time.time()}')
        time.sleep(0.5)


if __name__ == "__main__":
    bucket = TockenBucket(5, 0.4)
    filler_thread = Thread(target=token_filler_worker, args=(bucket,))
    filler_thread.daemon = True
    filler_thread.start()

    consumer_threads = []
    for i in range(5):
        thread = Thread(target=token_consumer_worker, args=(bucket,), name=f'consumer{i}')
        consumer_threads.append(thread)
        thread.start()

    for thread in consumer_threads:
        thread.join()    






































# class Bucket():
#     def __init__(self, capacity, fill_rate):
#         self.capacity = capacity
#         self.fill_rate = fill_rate
#         self.tokens = 0
#         self.cond = Condition()

#     def get_token(self):
#         with self.cond:
#             while self.tokens == 0:
#                 self.cond.wait()
#             self.tokens -= 1
#             self.cond.notify_all()

#     def add_token(self):
#         with self.cond:
#             while self.tokens == self.capacity:
#                 self.cond.wait()
#             self.tokens += 1
#             self.cond.notify_all()