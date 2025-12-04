import time, signal, socket, sys
from multiprocessing import Process

from motor_control import MotorController
from telemetry import Telemetry
import utils, vision

motor_controller = None
vision_process = None

def vision_worker():
    vision.start_pallet_filter()

def telemetry_worker():
    telemetry = Telemetry()
    while True:
        telemetry.update_all()
        utils.update_screen(telemetry.get_all())
        time.sleep(1)

def terminate_handler(signum, frame):
    print("Terminating processes...")

    if vision_process is not None:
        vision_process.terminate()
        time.sleep(2)
        vision_process.join()

    if motor_controller is not None:
        motor_controller.exit()

    if telemetry_process is not None:
        telemetry_process.terminate()
        time.sleep(2)

    print("Done.")

    sys.exit(0)

print("Starting Main Program...")

signal.signal(signal.SIGINT, terminate_handler)

vision_process = Process(target=vision_worker)
vision_process.start()
time.sleep(3)                                             # Allow vision process to initialize

telemetry = Telemetry()
telemetry_process = Process(target=telemetry_worker)
telemetry_process.start()
time.sleep(1)                                             # Allow telemetry process to initialize

motor_controller = MotorController()
time.sleep(1)                                             # Allow motor controller to initialize

pallet_data_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # Create UDP socket for receiving pallet bounding box data
pallet_data_socket.bind(("127.0.0.1", 3657))
pallet_data_socket.setblocking(False)

while True:

    data = None

    while True:
        try:
            data, addr = pallet_data_socket.recvfrom(1024)
            break
        except BlockingIOError:
            pass

    if data is not None:
        msg = data.decode().strip()

    if msg.startswith("PALLET_FOUND"):
        # Remove the "PALLET_FOUND," prefix and split the data fields
        parts = msg.replace("PALLET_FOUND,", "").split(",")

        # Parse the values
        width, angle = map(float, parts)
        print(f"Pallet Found - Width: {width}, Angle: {angle}")

