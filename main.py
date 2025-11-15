import time, os

import telemetry, utils, vision

voltage, heading = 0, 0

print("Starting Main Program...")

vision.start_camera()

while True:
    telemetry.update_all()
    utils.update_screen(telemetry.get_all())
    
    vision.update_camera()

    time.sleep(1)