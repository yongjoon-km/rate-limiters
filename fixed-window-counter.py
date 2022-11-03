import threading
from threading import Thread
import time
from datetime import datetime
import sys

COUNTER_PER_SEC = 1
REQUEST_PER_SEC = 30
WINDOW_SIZE_SEC = 10

time_window = None
counter = 0

lock = threading.Lock()

def reset_counter():
    global counter, time_window
    if time_window == f'{datetime.now():%H%M%S}':
        return
    with lock:
        counter = 0
        time_window = f'{datetime.now():%H%M%S}'
        print('reset counter', file=sys.stderr)

def process():
    global counter
    reset_counter()
    with lock:
        if counter >= WINDOW_SIZE_SEC:
            return False
        counter += 1
        return True

def request_in_sec():
    while True:
        time.sleep(1 / REQUEST_PER_SEC)
        res = process()
        if res:
            print(f'{datetime.now():%H%M%S}/ success')
        else:
            print(f'{datetime.now():%H%M%S}/ failed', file=sys.stderr)

            
request_thread = Thread(target=request_in_sec)
request_thread.start()

