import time
import datetime
from django.utils.deprecation import MiddlewareMixin
from security.traffic_buffer import update_traffic_buffer

class TrafficLoggingMiddleware(MiddlewareMixin):
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
                
            update_traffic_buffer(
                ip=ip,
                path=path,
                method=method,
                status_code=status_code,
                bytes_in=bytes_in,
                bytes_out=bytes_out,
                timestamp=datetime.datetime.now(),
                user_agent=request.META.get('HTTP_USER_AGENT', '-') )   
            
        except Exception:
            pass

        return response
