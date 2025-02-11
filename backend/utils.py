import cv2
import base64

def encode_image(image):
    """Convert OpenCV image to base64."""
    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode('utf-8')
