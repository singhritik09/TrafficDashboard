import time
import datetime
import os

class TrafficLoggingMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.log_dir="traffic_logs"
        
        os.makedirs(self.log_dir, exist_ok=True)
    
    def __call__(self, request):
        start_time=time.time()
        response = self.get_response(request)
        duration=time.time() - start_time
        
        now = datetime.datetime.now()
        log_filename = now.strftime("traffic-%Y-%m-%d-%H.log")
        log_path = os.path.join(self.log_dir, log_filename)
        log_line = (
            f"{now.isoformat()} | "
            f"IP={request.META.get('REMOTE_ADDR')} | "
            f"PATH={request.path} | "
            f"METHOD={request.method} | "
            f"STATUS={response.status_code} | "
            f"TIME={duration:.4f}s\n"
        )

        with open(log_path, "a") as f:
            f.write(log_line)

        return response
