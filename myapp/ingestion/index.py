from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import requests
# from myapp.security.traffic_buffer import get_traffic_buffer_snapshot

uri="mongodb://127.0.0.1:27017/application-logs"
client = MongoClient(uri)

def check_mongo_connection():
    try:
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
        print("MongoDB connection: Successful")
    except ConnectionFailure:
        print("MongoDB connection: Failed")

# def get_current_traffic_stats():
#     return get_traffic_buffer_snapshot()

def write_log(log_data):
    db = client['application-logs']
    collection = db['traffic_logs']
    
    find_ip=collection.find_one({"ip": log_data.get("127.0.0.1")})
    collection.insert_one(log_data)

def get_logs():
    request=requests.get("http://127.0.0.1:8000/status/")
    return request.json()
if __name__ == "__main__":
    # check_mongo_connection()
    # stats = get_traffic_buffer_snapshot()
    stats = get_logs()
    print(stats)
    write_log(stats)