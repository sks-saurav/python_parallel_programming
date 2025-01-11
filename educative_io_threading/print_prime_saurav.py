'''
we have two threads working together to find prime numbers and print them. 
Say the first thread finds the prime number and the second thread is responsible for printing the found prime. 
The first thread (finder) sets a boolean flag whenever it determines an integer is a prime number. 
The second (printer) thread needs to know when the finder thread has hit upon a prime number. 

IMP (print_worker):
There are however two questions we need to answer:

1. If the printer thread acquires the lock on the condition variable cond_var then how can the finder thread acquire() the lock when it needs to invoke the notify() method?

2. Can the condition, which is the variable found_prime, change once the printer thread is woken up?

The answer to the first question is that when a thread invokes wait() it simultaneously gives up the 
lock associated with the condition variable. Only when the sleeping thread wakes up again on a nofity(), 
will it reacquire the lock.

The second question is very important and leads us to the correct idiomatic usage of the condition variable.
The way we have nested the acquire and wait call under an if statement is incorrect. The reason is that if 
a thread invokes notifyAll() on a condition variable, then all the threads waiting on the condition variable
will be woken up but only one thread will be allowed to make progress. Once the first thread exits the 
critical section and releases the lock associated with the condition variable, another thread, 
from the set of threads that were waiting when the original notifyAll() call was made, is allowed 
to make progress. This may not be appropriate for every use case and certainly not for ours if we 
had multiple printer threads. We would want a printer thread to make progress only when the condition 
found_prime is set to true. This can only be possible with a while loop where we check if the 
condition found_prime is true before allowing a printer thread to move ahead.
[use while loop instead of if loop (line 40)]
'''
from threading import Thread, Condition
import time

curr_prime = 0
prime_flag = False

def print_worker():
    global curr_prime, prime_flag  
    while True:
        with cond:
            while not prime_flag: # if not prime_flag:
                cond.wait()
         
        print(curr_prime)
        curr_prime = None
        
        # acquire lock before modifying shared variable
        with cond: # with -> accquires lock and releases lock
            prime_flag = False
            # remember to wake up the other thread
            cond.notify()
        # time.sleep(0.5)
        
def is_prime(num):
    if num == 2 or num == 3:
        return True
    div = 2
    while div <= num / 2:
        if num % div == 0:
            return False
        div += 1
    return True

def find_prime_worker():
    global curr_prime, prime_flag
    i = 2
    while True:
        if is_prime(i):
            cond.acquire()
            while prime_flag:
                cond.wait()
            cond.release()

            cond.acquire()
            curr_prime = i
            prime_flag = True
            cond.notify()
            cond.release()
        i += 1
        # time.sleep(0.5)

cond = Condition()
printer = Thread(target=print_worker)
finder = Thread(target=find_prime_worker)

printer.start()
finder.start()

printer.join()
finder.join()
