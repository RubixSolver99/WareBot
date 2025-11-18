import time, os
from multiprocessing import Process

import telemetry, utils, vision

def vision_worker():
    vision.start_pallet_filter()

print("Starting Main Program...")

vision_process = Process(target=vision_worker)
vision_process.start()

while True:
    telemetry.update_all()
    utils.update_screen(telemetry.get_all())

    time.sleep(1)