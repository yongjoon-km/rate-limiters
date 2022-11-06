from datetime import datetime, timedelta
from threading import Thread, Lock
import time

log_stack = []

LIMIT = 10
lock = Lock()
REQUESTS_PER_SEC = 20

def process():
    with lock:
        time_window_front = datetime.now() - timedelta(seconds = 1)
        return len(list(filter(lambda x : x >= time_window_front, log_stack))) < LIMIT


def request():
    res = process()
    if res:
        with lock:
            log_stack.append(datetime.now())
        print(f'{datetime.now():%H%M%S}/ request success')


def request_in_sec():
    while True:
        time.sleep(1 / REQUESTS_PER_SEC)
        request()
    

request_thread = Thread(target=request_in_sec)

request_thread.start()


