from fastapi import APIRouter, File, UploadFile
import numpy as np
import cv2
from database import save_detection, get_detections
from models.suspicious_model import SuspiciousActivityModel
from models.fire_model import FireDetectionModel
from utils import encode_image
from datetime import datetime

router = APIRouter()

# Load Models
suspicious_model = SuspiciousActivityModel()
fire_model = FireDetectionModel()

@router.post("/detect_suspicious_activity/")
async def detect_suspicious_activity(file: UploadFile = File(...)):
    """Detect objects in an uploaded image."""
    contents = await file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Process frame with both models
    frame, detections1 = suspicious_model.predict(image)
    frame, detections2 = fire_model.predict(frame)

    # Merge results
    detections = detections1 + detections2

    # Save to database
    for d in detections:
        save_detection({
            "label": d["label"],
            "confidence": d["confidence"],
            "timestamp": datetime.now(),
            "image": encode_image(frame)
        })

    # Convert to base64
    encoded_image = encode_image(frame)
    return {"image": encoded_image, "detections": detections}

@router.get("/get_detections/")
async def get_detections():
    """Fetch detection history."""
    detections = get_detections()
    return {"detections": detections}

