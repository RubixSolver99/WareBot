from basics import L1_ina
from basics import L1_log as log
from basics import L2_compass_heading as compass
from basics import L2_kinematics as kin
import numpy as np

voltage, heading, wheel_left_ang_vel, wheel_right_ang_vel, lin_vel, ang_vel = 0

def update_all():
    global voltage, heading, wheel_left_ang_vel, wheel_right_ang_vel, lin_vel, ang_vel

    # Read & Log INA219 Voltage
    voltage = L1_ina.readVolts()
    log.tmpFile(voltage, "INA219_Voltage")

    # Read & Log Compass Heading
    heading = round(compass.get_heading(), 0)
    log.tmpFile(heading, "Compass_Heading")

    # Read & Log Kinematics
    pd = kin.getPdCurrent()
    log.tmpFile(pd[0], "Wheel_Left_Ang_Vel")
    log.tmpFile(pd[1], "Wheel_Right_Ang_Vel")

    # Read & Log Inverse Kinematics
    motion = kin.getMotion()
    log.tmpFile(motion[0], "Chassis_Lin_Vel")
    log.tmpFile(motion[1], "Chassis_Ang_Vel")

def get_all():
    global voltage, heading
    return {
        "INA219_Voltage": voltage,
        "Compass_Heading": heading
    }
    