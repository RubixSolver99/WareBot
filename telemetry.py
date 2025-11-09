from basics import L1_ina
from basics import L1_log as log
from basics import L2_compass_heading as compass
from basics import L2_kinematics as kin
import numpy as np

voltage = 0
heading = 0
wheel_left_ang_vel = 0
wheel_right_ang_vel = 0
lin_vel = 0
ang_vel = 0

def update_all():
    global voltage, heading, wheel_left_ang_vel, wheel_right_ang_vel, lin_vel, ang_vel

    # Read & Log INA219 Voltage
    voltage = L1_ina.readVolts()
    log.tmpFile(voltage, "INA219_Voltage")

    # Read & Log Compass Heading
    heading = int(compass.get_heading()) + 180
    log.tmpFile(heading, "Compass_Heading")

    # Read & Log Kinematics
    pd = kin.getPdCurrent()
    wheel_left_ang_vel = pd[0]
    wheel_right_ang_vel = pd[1]
    log.tmpFile(wheel_left_ang_vel, "Wheel_Left_Ang_Vel")
    log.tmpFile(wheel_right_ang_vel, "Wheel_Right_Ang_Vel")

    # Read & Log Inverse Kinematics
    motion = kin.getMotion()
    lin_vel = motion[0]
    ang_vel = motion[1]
    log.tmpFile(lin_vel, "Chassis_Lin_Vel")
    log.tmpFile(ang_vel, "Chassis_Ang_Vel")

def get_all():
    global voltage, heading, wheel_left_ang_vel, wheel_right_ang_vel, lin_vel, ang_vel

    return {
        "INA219_Voltage": voltage,
        "Compass_Heading": heading,
        "Wheel_Left_Ang_Vel": wheel_left_ang_vel,
        "Wheel_Right_Ang_Vel": wheel_right_ang_vel,
        "Chassis_Lin_Vel": lin_vel,
        "Chassis_Ang_Vel": ang_vel
    }

