'''
# Thread Safe Deferred Callback
Design and implement a thread-safe class that allows registration of callback methods that are
executed after a user specified time interval in seconds has elapsed.
'''

from threading import Condition
from threading import Thread
import heapq
import time
import math

class DeferredCallbackExecutor():
    def __init__(self):
        self.actions = list()
        self.cond = Condition()
        self.sleep = 0

    def add_action(self, action):
        # add exec_at time for the action
        action.execute_at = time.time() + action.exec_secs_after

        with self.cond:
            heapq.heappush(self.actions, action)
            self.cond.notify()

    def start(self):
        while True:
            with self.cond:
                while len(self.actions) == 0:
                    self.cond.wait()

                while len(self.actions) != 0:
                    # calculate sleep duration
                    next_action = self.actions[0]
                    sleep_for = next_action.execute_at - math.floor(time.time())
                    if sleep_for <= 0:
                        # time to execute action
                        break

                    self.cond.wait(timeout=sleep_for)

                action_to_execute_now = heapq.heappop(self.actions)
                action_to_execute_now.action(*(action_to_execute_now,))



class DeferredAction(object):
    def __init__(self, exec_secs_after, name, action):
        self.exec_secs_after = exec_secs_after
        self.action = action
        self.name = name

    def __lt__(self, other):
        return self.execute_at < other.execute_at


def say_hi(action):
        print("hi, I am {0} executed at {1} and required at {2}".format(action.name, math.floor(time.time()),
                                                                    math.floor(action.execute_at)))


if __name__ == "__main__":
    action1 = DeferredAction(3, ("A",), say_hi)
    action2 = DeferredAction(2, ("B",), say_hi)
    action3 = DeferredAction(1, ("C",), say_hi)
    action4 = DeferredAction(7, ("D",), say_hi)

    executor = DeferredCallbackExecutor()
    t = Thread(target=executor.start, daemon=True)
    t.start()

    executor.add_action(action1)
    executor.add_action(action2)
    executor.add_action(action3)
    executor.add_action(action4)

    # wait for all actions to execute
    time.sleep(15)