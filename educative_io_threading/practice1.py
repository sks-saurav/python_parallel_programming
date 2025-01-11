from threading import Thread
import time


def worker(num):
    """thread worker function"""
    print('Worker'+num)
    time.sleep(1.3)
    print('End Worker'+num)


t1 = Thread(target=worker, args=('1',))
t2 = Thread(target=worker, args=('2',))

t1.start()
t2.start()
t1.join()
t2.join()

'''
way 2:
'''

class Worker(Thread):
    def __init__(self, num):
        super().__init__()
        self.num = num

    def run(self):
        """thread worker function"""
        print('Worker'+self.num)
        time.sleep(1)
        print('End Worker'+self.num)


t1 = Worker('1')
t1.start()
t2 = Worker('2')
t2.start()

t1.join()
t2.join()