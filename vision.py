import cv2
import os
import time

# Folder where Node-RED will read images
IMAGE_PATH = "/tmp/vision/frame.jpg"

# Create folder if missing
os.makedirs(os.path.dirname(IMAGE_PATH), exist_ok=True)

_last_save = 0
MIN_INTERVAL = 0.1  # 10 FPS max (adjust as desired)


def send_frame(frame):
    """Save frame to disk for Node-RED to read"""
    global _last_save

    now = time.time()
    if now - _last_save < MIN_INTERVAL:
        return  # limit frame rate to avoid SD wear

    _last_save = now
    cv2.imwrite(IMAGE_PATH, frame)

def start_camera():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Camera failed to open.")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        # Process your frame however you want here...

        # Send frame to Node-RED
        send_frame(frame)

        # No imshow → avoids GTK crash
