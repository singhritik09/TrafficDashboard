import threading
from collections import defaultdict
from time import time

# MUTEX LOCK FOR THREAD SAFETY while sharing data betweeen multiple threads
buffer_lock = threading.Lock()


#RETURNS DETAULS ABOUT TRAFFIC FROM A SINGLE IP ADDRESS
def traffic_bucket():
    return{
        'count': 0,
        'error_count': 0,
        'bytes_in': 0,
        'bytes_out': 0,
        'path': defaultdict(int),
        'user_agents': defaultdict(int),
        'last_seen': 0
    }   

#The first time an IP appears, Django automatically creates this bucket
TRAFFIC_BUFFER = defaultdict(traffic_bucket)

# This function is called on every request (usually from middleware).
def update_traffic_buffer(ip, path, method, status_code, bytes_in, bytes_out, user_agent):
    now = time()
    
    with buffer_lock:
        bucket = TRAFFIC_BUFFER[ip]
        # If IP is new: traffic_bucket() is called automaticallyA fresh stats container is created
        bucket['count'] += 1
        if status_code >= 400:
            bucket['error_count'] += 1
        bucket['bytes_in'] += bytes_in
        bucket['bytes_out'] += bytes_out
        bucket['path'][path] += 1
        bucket['user_agents'][user_agent] += 1
        bucket['last_seen'] = now
        
# O(1) writing data for each request