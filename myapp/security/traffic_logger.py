import time
import datetime
from django.utils.deprecation import MiddlewareMixin
from myapp.tasks import push_snapshot_to_kafka
#MiddlewareMixin wires middleware into django request lifecylce process_req before view and process_res after view 


class TrafficLoggingMiddleware(MiddlewareMixin):
    # Runs before the request reaches the view
    def process_request(self,request):
        request._start_time = time.time()
        
    def process_response(self, request, response):
        try:
            ip=request.META.get('REMOTE_ADDR', '')
            path=request.path
            method=request.method
            status_code=response.status_code
            if request.body:
                bytes_in=len(request.body)
            else:
                bytes_in=0   
            if response.content:
                bytes_out=len(response.content) 
            else:   
                bytes_out=0
            user_agent=request.META.get('HTTP_USER_AGENT', '')

            event={
                'ip': ip,
                'path': path,
                'method': method,
                'status_code': status_code,
                'bytes_in': bytes_in,
                'bytes_out': bytes_out,
                'user_agent': user_agent
            }
            # Sending async event to Celery task to push to Kafka
            push_snapshot_to_kafka.delay(event)
        except Exception as e:
            print(f"Error in TrafficLoggingMiddleware: {e}")

        return response




# Client → Django → Middleware → Celery → Kafka

# Django → Redis (Celery broker queue)
# Celery Worker → Kafka: Takes event from Redis queue
# Executes task
# Calls Kafka producer

# celery -A myapplication worker --loglevel=info

# kafka-console-consumer --bootstrap-server localhost:9092 --topic traffic_snapshots --from-beginning
# Kafka Producer with retries, acks, batching