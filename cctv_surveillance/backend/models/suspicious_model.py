import cv2
import torch
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO("yolov8x.pt")  # Use the larger model for better accuracy

# Define detection categories (Modify these if using a custom-trained model)
labels = {0: "Person", 1: "Fire", 2: "Weapon", 3: "Accident"}

# Load video file
video_path = "carcrash.mp4"  # Change this to your video file
cap = cv2.VideoCapture(video_path)

# Get video properties
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Define output video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter("output_video.mp4", fourcc, fps, (frame_width, frame_height))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess frame
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    frame = cv2.resize(frame, (640, 640))  # Resize to fit the model input size

    # Run YOLO detection
    results = model(frame, iou=0.4)  # Adjust IoU threshold for NMS

    # Draw detections
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0].item()
            cls = int(box.cls[0].item())

            if cls in labels and conf > 0.7:  # Increased confidence threshold
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{labels[cls]} ({conf:.2f})",
                            (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Write frame to video
    out.write(frame)
    cv2.imshow("Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
