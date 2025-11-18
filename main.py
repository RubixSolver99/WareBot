import time, os
from multiprocessing import Process

import telemetry, utils, vision

def vision_worker():
    vision.start_pallet_filter()

print("Starting Main Program...")

vision_process = Process(target=vision_worker)
vision_process.start()
time.sleep(3)  # Allow vision process to initialize

while True:
    telemetry.update_all()
    utils.update_screen(telemetry.get_all())

    time.sleep(1)