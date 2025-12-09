import os, time
import numpy as np

PALLET_EXPOSURE_VALUE = 45  # set manual exposure value (lower number = less exposure)

def start_pallet_filter():
    set_manual_exposure(PALLET_EXPOSURE_VALUE)

    os.system("/usr/local/bin/mjpg_streamer \
              -i \"/usr/local/lib/mjpg-streamer/input_opencv.so \
              --filter /usr/local/lib/mjpg-streamer/cvfilter_py.so \
              --fargs ./vision_filters/pallet.py\" \
              -o \"/usr/local/lib/mjpg-streamer/output_http.so \
              -p 3656 \
              -w /usr/local/share/mjpg-streamer/www\"")

def set_manual_exposure(value):
    os.system("v4l2-ctl -c exposure_auto=1")  # set manual exposure
    os.system("v4l2-ctl -c exposure_absolute=" + str(value))  # set exposure value

def set_auto_exposure():
    os.system("v4l2-ctl -c exposure_auto=3")  # set auto exposure

