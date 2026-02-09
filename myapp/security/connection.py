import pymongo
from myapp.security.traffic_buffer import get_traffic_buffer_snapshot
from myapp.ingestion.index import check_mongo_connection

URL="mongodb://127.0.0.1:27017/application-logs"
connection=pymongo.MongoClient(URL)

def connect_to_mongo():
    try:
        client=pymongo.MongoClient(URL,serverSelectionTimeoutMS=5000)        
        print("MongoDB connection: Successful")
    except pymongo.errors.ConnectionFailure as e:
        print("MongoDB connection: Failed")
        raise e
    
def get_db():
    db=connection['application-logs']
    collection=db.list_collection_names()
    print(f"Collections in 'application-logs' database: {collection}")
    return db

def get_traffic_logs():
    db=get_db()
    collection=db['traffic_logs']
    logs=collection.find()
    for log in logs:
        print(log)

if __name__ == "__main__":
    check_mongo_connection()
    get_traffic_logs()
    traffic_stats = get_traffic_buffer_snapshot()
    print(f"TRAFFIC STATS: {traffic_stats}")