import random
import requests
import threading
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "http://127.0.0.1:8000"
ENDPOINTS = ["/", "/status/"]

MAX_FAILURES = 10        # stop after this many consecutive failures
TIMEOUT = 2

failure_count = 0
lock = threading.Lock()
stop_event = threading.Event()

def hit_endpoint():
    global failure_count

    if stop_event.is_set():
        return

    endpoint = random.choice(ENDPOINTS)
    url = BASE_URL + endpoint

    try:
        r = requests.get(url, timeout=TIMEOUT)

        with lock:
            if r.status_code >= 500:
                failure_count += 1
                print(f"FAIL {endpoint} | {r.status_code}")
            else:
                failure_count = 0
                print(f"OK   {endpoint} | {r.status_code}")

    except Exception as e:
        with lock:
            failure_count += 1
            print(f"ERROR {endpoint} | {e}")

    if failure_count >= MAX_FAILURES:
        print("\n🚨 Failure threshold reached. Stopping load test.\n")
        stop_event.set()


def generate_high_load(workers=5):
    with ThreadPoolExecutor(max_workers=workers) as executor:
        while not stop_event.is_set():
            executor.submit(hit_endpoint)


if __name__ == "__main__":
    generate_high_load(workers=5)
