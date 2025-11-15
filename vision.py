import cv2
import os
import time

# Folder where Node-RED will read images
IMAGE_PATH = "/tmp/vision/frame.jpg"
MIN_INTERVAL = 0.03  # 30 FPS max (adjust as desired)
_last_save = 0
cap = None


def send_frame(frame):
    """Save frame to disk for Node-RED to read"""
    global _last_save

    now = time.time()
    if now - _last_save < MIN_INTERVAL:
        return  # limit frame rate to avoid SD wear

    _last_save = now
    cv2.imwrite(IMAGE_PATH, frame)

def start_camera():
    global cap

    # Create folder if missing
    os.makedirs(os.path.dirname(IMAGE_PATH), exist_ok=True)

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    cap.set(cv2.CAP_PROP_FPS, 30)  # Requesting 30 FPS from the camera

    if not cap.isOpened():
        print("Camera failed to open.")
        exit()

def update_camera():
    global cap
    
    ret, frame = cap.read()
    if not ret:
        return None

    # Process your frame however you want here...

    # Send frame to Node-RED
    send_frame(frame)

    # No imshow → avoids GTK crash
