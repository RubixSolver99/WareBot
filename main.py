import time

from basics import L1_ina
from basics import L1_log as log

print("""
 _    _               ______       _   
| |  | |              | ___ \     | |  
| |  | | __ _ _ __ ___| |_/ / ___ | |_ 
| |/\| |/ _` | '__/ _ \ ___ \/ _ \| __|
\  /\  / (_| | | |  __/ |_/ / (_) | |_ 
 \/  \/ \__,_|_|  \___\____/ \___/ \__|                                       
      """)

print("Starting Main Program...")

while True:
    print("Reading INA219 Voltage...")
    voltage = L1_ina.readVolts()
    print(f"INA219 Voltage: {voltage} V")
    log.tmpFile(voltage, "INA219 Voltage")
    time.sleep(1)