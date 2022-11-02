import time
import threading 
from datetime import datetime
import sys
from threading import Thread

lock = threading.Lock()
bucket = []
BUCKET_CAPACITY = 10
BUCKET_FILLED_PER_SEC = 1
REQUEST_PER_SEC = 20

def fill_bucket():
    if len(bucket) >= BUCKET_CAPACITY:
        return
    bucket.extend([1] * (BUCKET_CAPACITY - len(bucket)))

def fill_bucket_in_time_window():
    while True:
        time.sleep(1 / BUCKET_FILLED_PER_SEC)
        fill_bucket()
        print(f'{datetime.now():%H%M%S}/ bucket filled', file=sys.stderr)
    
def process():
    with lock:
        if len(bucket) <= 0:
            return False
        bucket.pop()
        return True

def request_in_sec():
    while True:
        time.sleep(1 / REQUEST_PER_SEC)
        res = process()
        if res:
            print(f'{datetime.now():%H%M%S}/ request processed')
        else:
            print(f'{datetime.now()}/ request failed', file=sys.stderr)


t = Thread(target=request_in_sec)
t.start()


t = Thread(target=fill_bucket_in_time_window)
t.start()

