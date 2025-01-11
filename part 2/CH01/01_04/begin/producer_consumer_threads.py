#!/usr/bin/env python3
""" Producers serving soup for Consumers to eat """

import queue
import threading
import time

serving_line = queue.Queue(maxsize=5)

def soup_producer():
    for i in range(200): # serve 20 bowls of soup
        serving_line.put('Bowl #'+str(i), block=False)
        print('Served Bowl #', str(i), '- remaining capacity:', \
            serving_line.maxsize-serving_line.qsize())
        time.sleep(0.2) # time to serve a bowl of soup

def soup_consumer():
    while True:
        bowl = serving_line.get(block=False)
        print('Ate', bowl)
        time.sleep(0.11) # time to eat a bowl of soup

if __name__ == '__main__':
    threading.Thread(target=soup_consumer).start()
    threading.Thread(target=soup_consumer).start()
    threading.Thread(target=soup_producer).start()
