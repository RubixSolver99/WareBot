import time, signal, sys
from multiprocessing import Process

from motor_control import MotorController
import telemetry, utils, vision

motor_controller = None
vision_process = None

def vision_worker():
    vision.start_pallet_filter()

def terminate_handler(signum, frame):
    print("Terminating processes...")

    if vision_process is not None:
        vision_process.terminate()
        time.sleep(2)
        vision_process.join()

    if motor_controller is not None:
        motor_controller.exit()

    print("Done.")

    sys.exit(0)

print("Starting Main Program...")

signal.signal(signal.SIGINT, terminate_handler)

motor_controller = MotorController()
time.sleep(1)                                       # Allow motor controller to initialize

vision_process = Process(target=vision_worker)
vision_process.start()
time.sleep(3)                                       # Allow vision process to initialize

while True:
    telemetry.update_all()
    utils.update_screen(telemetry.get_all())

    time.sleep(1)

