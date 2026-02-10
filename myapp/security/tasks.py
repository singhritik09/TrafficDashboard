from celery import shared_task
from .traffic_buffer import  get_traffic_buffer_snapshot
import json
import time
from kafka import KafkaProducer

producer= KafkaProducer(
    bootstrap_servers='localhost:9092', 
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    linger_ms=100,          # batch messages
    retries=5
)

@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={'max_retries': 5}
)

def push_snapshot_to_kafka(self):
    try:
        snapshot=get_traffic_buffer_snapshot()
        
        if snapshot==None:
            print("No traffic data to send.")
            return
        
        message={
            "type":"traffic_snapshot",
            "timestamp": time.time(),
            "data": snapshot
        }
        producer.send('traffic_snapshots', message)
        
        producer.flush()
        
        return f"Pushed snapshot with {len(snapshot)} IPs"
    
    except Exception as e:
        print(f"Error getting traffic buffer snapshot: {e}")
        raise e