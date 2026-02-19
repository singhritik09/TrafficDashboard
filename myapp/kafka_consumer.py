# import json
# from kafka import KafkaConsumer
# from collections import defaultdict
# from datetime import datetime
# import threading

# store_lock = threading.Lock()

# KAFKA_TRAFFIC_STORE = defaultdict(lambda: {
#     'count': 0,
#     'error_count': 0,
#     'bytes_in': 0,
#     'bytes_out': 0,
#     'paths': defaultdict(int),
#     'user_agents': defaultdict(int),
#     'last_seen': None
# })  


# def start_consumer():
#     consumer = KafkaConsumer(
#         'traffic_snapshots',
#         bootstrap_servers=['localhost:9092'],
#         value_deserializer=lambda x: json.loads(x.decode('utf-8'))
#         auto_offset_reset='earliest',
#         enable_auto_commit=True,
#         group_id='traffic-consumers-group'
#     )
#     print("Kafka Consumer started, listening to traffic_snapshots topic...")
#     for message in consumer:
#         event=message.value
#         # process_event(event)
#         with store_lock:
#             ip = event['ip']
#             KAFKA_TRAFFIC_STORE[ip]['count'] += 1
#             KAFKA_TRAFFIC_STORE[ip]['bytes_in'] += event['bytes_in']
#             KAFKA_TRAFFIC_STORE[ip]['bytes_out'] += event['bytes_out']
#             KAFKA_TRAFFIC_STORE[ip]['paths'][event['path']] += 1
#             KAFKA_TRAFFIC_STORE[ip]['user_agents'][event['user_agent']] += 1
#             KAFKA_TRAFFIC_STORE[ip]['last_seen'] = datetime.now()
        
# if __name__ == "__main__":
#     start_consumer()    
        