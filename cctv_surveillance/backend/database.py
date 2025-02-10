from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def save_detection(detection_data):
    """Save detection event to MongoDB."""
    collection.insert_one(detection_data)

def get_detections():
    """Fetch detection history."""
    return list(collection.find({}, {"_id": 0}))
