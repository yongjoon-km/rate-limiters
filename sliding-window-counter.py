from datetime import datetime, timedelta
from threading import Thread, Lock
from collections import Counter
from math import floor
import time



counter = Counter()
LIMIT = 10
REQUEST_PER_SEC = 5
lock = Lock()

def process():
    current_time = datetime.now()
    current_window_key = f'{current_time:%H%M%S}'
    prev_window_key = f'{current_time - timedelta(seconds = 1):%H%M%S}'
    prev_window_weight = (1000000 - current_time.microsecond) / 1000000
    with lock:
        request_count = counter[prev_window_key] * prev_window_weight + counter[current_window_key]
        request_count = floor(request_count)
#         print(request_count, counter[prev_window_key], counter[current_window_key])
        if request_count >= LIMIT:
            return False
        counter[current_window_key] += 1
        return True

def request_in_sec():
    while True:
        time.sleep(1 / REQUEST_PER_SEC)
        res = process()
        if res:
            print(f'{datetime.now():%H%M%S}/ request success')

request_thread = Thread(target=request_in_sec)
request_thread.start()
