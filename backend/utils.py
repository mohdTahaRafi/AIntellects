import cv2
import base64
import numpy as np

def encode_image(image):
    """Convert OpenCV image to base64."""
    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode('utf-8')

def decode_image(base64_str):
    """Convert base64 string to OpenCV image."""
    img_data = base64.b64decode(base64_str)
    np_arr = np.frombuffer(img_data, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
