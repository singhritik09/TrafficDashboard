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
# Key → ip  &  Value → traffic bucket

# This function is called on every request (usually from middleware).

#IF IP EXISTS bucket=TRAFFIC_BUFFER[ip] ELSE bucket=traffic_bucket() and then updates the bucket with new stats and stores it back in TRAFFIC_BUFFER[ip]

def update_traffic_buffer(ip, path, method, status_code, bytes_in, bytes_out, user_agent):
    timestamp = datetime.utcnow()

    with buffer_lock:
        bucket = TRAFFIC_BUFFER[ip]
        bucket['count'] += 1

        if status_code >= 500:
            bucket['error_count'] += 1

        bucket['bytes_in'] += bytes_in
        bucket['bytes_out'] += bytes_out
        bucket['path'][path] += 1
        bucket['user_agents'][user_agent] += 1
        bucket['last_seen'] = timestamp
        # print(f"Keys of bucket for IP{ip}: {bucket.keys()}")

# 
def get_traffic_buffer_snapshot():
    with buffer_lock:
        snapshot=[]
        for ip,data in TRAFFIC_BUFFER.items():
            snapshot.append({
                'ip': ip,
                'count': data['count'],
                'error_count': data['error_count'],
                'bytes_in': data['bytes_in'],
                'bytes_out': data['bytes_out'],
                'path': dict(data['path']),
                'user_agents': dict(data['user_agents']),
                'last_seen': data['last_seen'].isoformat()
            })
        # print(f"Traffic Buffer Snapshot: {TRAFFIC_BUFFER.keys()}")
        # print(f"Traffic Buffer Snapshot: {(snapshot)}")
        # print(f"length of snapshot: {len(snapshot)}")
        TRAFFIC_BUFFER.clear()
        return snapshot
# O(1) writing data for each request