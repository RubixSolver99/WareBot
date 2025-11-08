import L1_ina as battery_voltage
import L1_log as log 
import time
import numpy as np
import L1_log


while True:
    def getVoltage():
        return battery_voltage.readVolts()
    L1_log.tmpFile(getVoltage(), "Voltage_File")
    time.sleep(1.0)
