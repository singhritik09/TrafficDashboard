from celery import shared_task
from myapp.security.traffic_buffer import  get_traffic_buffer_snapshot
import json
import time
from kafka import KafkaProducer

producer= KafkaProducer(
    bootstrap_servers='localhost:9092', 
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    acks=1,# Wait for acknowledgment from leader only
    linger_ms=50, # Batch messages for up to 10ms
    # batch_size=32*1024, # Batch up to 32KB of messages
    # max_request_size=128*1024, # Max size of a single message is 128KB
    retries=3
)

@shared_task(autoretry_for=(Exception,), retry_backoff=3, retry_kwargs={"max_retries": 3})
def push_snapshot_to_kafka(event=None):
    try:
        producer.send('traffic_snapshots', event)
        return f"Pushed snapshot with {event.get('ip', [])}"
    
    except Exception as e:
        print(f"Error getting traffic buffer snapshot: {e}")
        raise e