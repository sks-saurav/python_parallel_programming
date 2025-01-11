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