from fastapi import FastAPI, WebSocket
import cv2
import numpy as np
import base64
from routes import router
from models.suspicious_model import SuspiciousActivityModel
from models.fire_model import FireDetectionModel
from fastapi.middleware.cors import CORSMiddleware
from config import VIDEO_URL

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Models
suspicious_model = SuspiciousActivityModel()
fire_model = FireDetectionModel()

# Include API routes
app.include_router(router)

@app.websocket("/ws/video")
async def video_stream(websocket: WebSocket):
    """Live stream video frames via WebSocket."""
    await websocket.accept()
    cap = cv2.VideoCapture(VIDEO_URL)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Process frame
        frame, detections1 = suspicious_model.predict(frame)
        frame, detections2 = fire_model.predict(frame)

        detections = detections1 + detections2  # Combine detections

        # Encode frame
        _, buffer = cv2.imencode('.jpg', frame)
        base64_frame = base64.b64encode(buffer).decode("utf-8")

        # Send data to frontend
        await websocket.send_json({"image": base64_frame, "detections": detections})

    cap.release()
    await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
