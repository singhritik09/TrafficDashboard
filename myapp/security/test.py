from kafka import KafkaProducer
import json
import time

producer= KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

message={
    "type":"health_check",
    "message":"Application is running NEW CHECK",
    "timestamp": time.time(),
    "status":"ok"
    }
producer.send('traffic_snapshots', message)
producer.flush()

print("Health check message sent to Kafka topic 'traffic_snapshots'")