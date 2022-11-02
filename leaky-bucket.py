from collections import deque
from threading import Lock
from datetime import datetime
from threading import Thread
import time
import sys

lock = Lock()
queue = deque()
BUCKET_CAPACITY = 100
LEAK_PER_SEC = 3
REQUEST_PER_SEC = 10

def process():
    if not len(queue):
        return None
    
    with lock:
        return queue.popleft()
        

def process_in_seq():
    while True:
        time.sleep(1 / LEAK_PER_SEC)
        res = process()
        if res:
            print(f'{datetime.now():%H%M%S}/ request processed', res)
        else:
            print(f'{datetime.now()}/ nothing to process', file=sys.stderr)


def request():
    if len(queue) >= BUCKET_CAPACITY:
        return False
    with lock:
        queue.append(datetime.now())
        return True
        
def request_in_seq():
    while True:
        time.sleep(1 / REQUEST_PER_SEC)
        res = request()
        if res:
            print(f'{datetime.now()}/ request success', file=sys.stderr)
        else:
            print(f'{datetime.now()}/ request failed', file=sys.stderr)
            

process_thread = Thread(target=process_in_seq)
process_thread.start()

request_thread = Thread(target=request_in_seq)
request_thread.start()
