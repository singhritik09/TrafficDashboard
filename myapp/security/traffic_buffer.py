from datetime import datetime
import threading
from collections import defaultdict
from time import time

# MUTEX LOCK FOR THREAD SAFETY while sharing data betweeen multiple threads
buffer_lock = threading.Lock()


#RETURNS DETAILS ABOUT TRAFFIC FROM A SINGLE IP ADDRESS
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
from datetime import datetime

def update_traffic_buffer(ip, path, method, status_code, bytes_in, bytes_out, user_agent):
    timestamp = datetime.utcnow()

    with buffer_lock:
        bucket = TRAFFIC_BUFFER[ip]
        bucket['count'] += 1

        if status_code >= 400:
            bucket['error_count'] += 1

        bucket['bytes_in'] += bytes_in
        bucket['bytes_out'] += bytes_out
        bucket['path'][path] += 1
        bucket['user_agents'][user_agent] += 1
        bucket['last_seen'] = timestamp


def get_traffic_buffer_snapshot():
    with buffer_lock:
        return {
            ip: {
                "count": b["count"],
                "error_count": b["error_count"],
                "bytes_in": b["bytes_in"],
                "bytes_out": b["bytes_out"],
                "path": dict(b["path"]),
                "user_agents": dict(b["user_agents"]),
                "last_seen": b["last_seen"].isoformat() if b["last_seen"] else None,
            }
            for ip, b in TRAFFIC_BUFFER.items()
        }

# O(1) writing data for each request