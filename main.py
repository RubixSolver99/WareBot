import time, os

import telemetry, utils

voltage, heading = 0, 0

print("Starting Main Program...")

while True:
    telemetry.update_all()
    utils.update_screen(telemetry.get_all())
    time.sleep(1)