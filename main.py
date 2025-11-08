import time, os

from basics import L1_ina
from basics import L1_log as log

voltage = 0

def update_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("""
    _    _               ______       _   
    | |  | |              | ___ \     | |  
    | |  | | __ _ _ __ ___| |_/ / ___ | |_ 
    | |/\| |/ _` | '__/ _ \ ___ \/ _ \| __|
    \  /\  / (_| | | |  __/ |_/ / (_) | |_ 
    \/  \/ \__,_|_|  \___\____/ \___/ \__|                                       
        """)
    print("\n\nMAIN DASHBOARD\n\n")
    print(f"INA219 Voltage: {voltage} V")

print("Starting Main Program...")

while True:
    print("Reading INA219 Voltage...")
    voltage = L1_ina.readVolts()
    log.tmpFile(voltage, "INA219 Voltage")
    update_screen()
    time.sleep(1)