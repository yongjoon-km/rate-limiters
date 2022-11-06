from threading import Thread, Lock
from datetime import datetime
import time
import sys

BUCKET_CAPACITY = 10
bucket = [1] * BUCKET_CAPACITY

BUCKET_FILLED_PER_SEC = 1
REQUEST_PER_SEC = 20

lock = Lock()

def fill_bucket():
    global bucket
    with lock:
        bucket = [1] * BUCKET_CAPACITY
    
def can_allow_request():
    global bucket
    with lock:
        if len(bucket) <= 0:
            return False
        bucket.pop()
        return True
    
def fill_bucket_in_time_window():
    while True:
        time.sleep(1 / BUCKET_FILLED_PER_SEC)
        fill_bucket()

def request_in_sec():
    while True:
        time.sleep(1 / REQUEST_PER_SEC)
        if can_allow_request():
            print(f'{datetime.now():%H%M%S}/ request processed')


request_thread = Thread(target=request_in_sec)
request_thread.start()

fill_bucket_thread = Thread(target=fill_bucket_in_time_window)
fill_bucket_thread.start()
