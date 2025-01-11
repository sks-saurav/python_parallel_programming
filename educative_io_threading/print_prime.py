'''
we have two threads working together to find prime numbers and print them. 
Say the first thread finds the prime number and the second thread is responsible for printing the found prime. 
The first thread (finder) sets a boolean flag whenever it determines an integer is a prime number. 
The second (printer) thread needs to know when the finder thread has hit upon a prime number. 
'''
from threading import Thread, Condition
import time

curr_prime = 0
prime_flag = False

def print_worker():
    global curr_prime, prime_flag  
    while True:
        with cond:
            if not prime_flag:
                cond.wait()
         
        print(curr_prime)
        curr_prime = None
        
        # acquire lock before modifying shared variable
        with cond:
            prime_flag = False
            # remember to wake up the other thread
            cond.notify()
        time.sleep(0.5)
        
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
            if prime_flag:
                cond.wait()
            cond.release()

            cond.acquire()
            curr_prime = i
            prime_flag = True
            cond.notify()
            cond.release()
        i += 1
        time.sleep(0.5)

cond = Condition()
printer = Thread(target=print_worker)
finder = Thread(target=find_prime_worker)

printer.start()
finder.start()

printer.join()
finder.join()
