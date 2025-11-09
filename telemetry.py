from basics import L1_ina
from basics import L1_log as log
from basics import L2_compass_heading as compass

voltage, heading = 0, 0

def update_all():
    global voltage, heading
    # Read INA219 Voltage
    voltage = L1_ina.readVolts()
    log.tmpFile(voltage, "INA219_Voltage")

    # Read Compass Heading
    heading = round(compass.get_heading(), 0)
    log.tmpFile(heading, "Compass_Heading")

def get_all():
    global voltage, heading
    return {
        "INA219_Voltage": voltage,
        "Compass_Heading": heading
    }
    