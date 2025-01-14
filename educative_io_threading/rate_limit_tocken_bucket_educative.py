'''
# Rate Limiting Using Token Bucket Filter
This is an actual interview question asked at Uber and Oracle.

Imagine you have a bucket that gets filled with tokens at the rate of 1 token per second. 
The bucket can hold a maximum of N tokens. Implement a thread-safe class that lets threads 
get a token when one is available. If no token is available, then the token-requesting threads should block.

The class should expose an API called get_token() that various threads can call to get a token.
'''

'''
=======================================================
    Type 1: filler as demon thread
=======================================================
'''


from threading import Thread
from threading import Condition
from threading import current_thread
import time

class TokenBucketFilterFactory:
    @staticmethod
    def makeTokenBucketFilter(capacity):
        tbf = MultithreadedTokenBucketFilter(capacity)
        tbf.initialize()
        return tbf


class MultithreadedTokenBucketFilter:
    def __init__(self, maxTokens):
        self.MAX_TOKENS = int(maxTokens)
        self.possibleTokens  = int(0)
        self.ONE_SECOND = int(1)
        self.cond = Condition()

    def initialize(self):
        dt = Thread(target = self.daemonThread)
        dt.daemon = True
        dt.start()
                
    def daemonThread(self):
        while True:
            with self.cond:
                if self.possibleTokens < self.MAX_TOKENS:
                    self.possibleTokens = self.possibleTokens + 1
                self.cond.notify() 
            
            time.sleep(self.ONE_SECOND)
    
    def getToken(self):
        with self.cond:
            while self.possibleTokens == 0:
                self.cond.wait()

            self.possibleTokens = self.possibleTokens - 1

        print("Granting " + current_thread().name + " token at " + str(time.time()))

def token_consumer_worker(tbf):
    for i in range(10):
        tbf.getToken()
        time.sleep(0.5)

if __name__ == '__main__':
    tbf = TokenBucketFilterFactory.makeTokenBucketFilter(5)
    threads = []
    for i in range(10):
        t = Thread(target = token_consumer_worker, args = (tbf,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()


'''
=======================================================
    Type 1: fill bucket without using a seperate thread worker
=======================================================
'''

# from threading import Thread
# from threading import current_thread
# from threading import Semaphore
# from threading import current_thread
# from threading import Lock
# from threading import Barrier
# import random
# import time


# class TokenBucketFilter:

#     def __init__(self, MAX_TOKENS):
#         self.MAX_TOKENS = MAX_TOKENS
#         self.last_request_time = time.time()
#         self.possible_tokens = 0
#         self.lock = Lock()

#     def get_token(self):

#         with self.lock:
#             self.possible_tokens += int((time.time() - self.last_request_time))

#             if self.possible_tokens > self.MAX_TOKENS:
#                 self.possible_tokens = self.MAX_TOKENS

#             if self.possible_tokens == 0:
#                 time.sleep(1)
#             else:
#                 self.possible_tokens -= 1

#             self.last_request_time = time.time()

#             print("Granting {0} token at {1} ".format(current_thread().getName(), int(time.time())));


# if __name__ == "__main__":

#     token_bucket_filter = TokenBucketFilter(1)

#     threads = list()
#     for _ in range(0, 10):
#         threads.append(Thread(target=token_bucket_filter.get_token))

#     for thread in threads:
#         thread.start()

#     for thread in threads:
#         thread.join()