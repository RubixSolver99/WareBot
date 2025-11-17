import cv2, os, time
import numpy as np

WIDTH  = 240  # width of image to process (pixels)
HEIGHT = 160 # height of image to process (pixels)

PALLET_EXPOSURE_VALUE = 10  # set manual exposure value (lower number = less exposure)
PALLET_COLOR_RANGE = np.array([[35, 80, 5], [65, 255, 240]]) # declare HSV range before overwrighting with user inputs

def start_pallet_filter():
    os.system("v4l2-ctl -c exposure_auto=1")  # set manual exposure
    os.system("v4l2-ctl -c exposure_absolute=" + str(PALLET_EXPOSURE_VALUE))  # set exposure value

    os.system("/usr/local/bin/mjpg_streamer \
              -i \"/usr/local/lib/mjpg-streamer/input_opencv.so \
              --filter /usr/local/lib/mjpg-streamer/cvfilter_py.so \
              --fargs ./vision_filters/pallet.py\" \
              -o \"/usr/local/lib/mjpg-streamer/output_http.so \
              -p 8090 \
              -w /usr/local/share/mjpg-streamer/www\"")

def set_manual_exposure(value):
    os.system("v4l2-ctl -c exposure_auto=1")  # set manual exposure
    os.system("v4l2-ctl -c exposure_absolute=" + str(value))  # set exposure value

def set_auto_exposure():
    os.system("v4l2-ctl -c exposure_auto=3")  # set auto exposure

