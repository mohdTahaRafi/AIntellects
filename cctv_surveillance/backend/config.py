import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "cctv_surveillance")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "detections")
VIDEO_URL = os.getenv("VIDEO_URL", "rtsp://your_cctv_ip_address")  # CCTV stream URL
