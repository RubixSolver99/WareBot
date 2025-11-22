import time, signal, sys
from multiprocessing import Process

import telemetry, utils, vision

vision_process = None

def vision_worker():
    vision.start_pallet_filter()

def terminate_handler(signum, frame):
    print("Terminating processes...")

    if vision_process is not None:
        vision_process.terminate()
        vision_process.join()

    print("Done.")

    sys.exit(0)

print("Starting Main Program...")

signal.signal(signal.SIGINT, terminate_handler)

vision_process = Process(target=vision_worker)
vision_process.start()
time.sleep(3)                                       # Allow vision process to initialize

while True:
    telemetry.update_all()
    utils.update_screen(telemetry.get_all())

    time.sleep(1)