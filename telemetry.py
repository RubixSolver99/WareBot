from basics import L1_ina
from basics import L1_log as log
from basics import L2_compass_heading as compass
from basics import L2_kinematics as kin
import numpy as np


class Telemetry:
    def __init__(self):
        self.voltage = 0
        self.heading = 0
        self.wheel_left_ang_vel = 0
        self.wheel_right_ang_vel = 0
        self.lin_vel = 0
        self.ang_vel = 0

    def update_all(self):
        # Read & Log INA219 Voltage
        self.voltage = L1_ina.readVolts()
        log.tmpFile(self.voltage, "INA219_Voltage")

        # Read & Log Compass Heading
        self.heading = int(compass.get_heading()) + 180
        log.tmpFile(self.heading, "Compass_Heading")

        # Read & Log Kinematics
        pd = kin.getPdCurrent()
        self.wheel_left_ang_vel = np.round(pd[0], decimals=3)
        self.wheel_right_ang_vel = np.round(pd[1], decimals=3)
        log.tmpFile(self.wheel_left_ang_vel, "Wheel_Left_Ang_Vel")
        log.tmpFile(self.wheel_right_ang_vel, "Wheel_Right_Ang_Vel")

        # Read & Log Inverse Kinematics
        motion = kin.getMotion()
        self.lin_vel = motion[0]
        self.ang_vel = motion[1]
        log.tmpFile(self.lin_vel, "Chassis_Lin_Vel")
        log.tmpFile(self.ang_vel, "Chassis_Ang_Vel")

    def get_all(self):
        return {
            "INA219_Voltage": self.voltage,
            "Compass_Heading": self.heading,
            "Wheel_Left_Ang_Vel": self.wheel_left_ang_vel,
            "Wheel_Right_Ang_Vel": self.wheel_right_ang_vel,
            "Chassis_Lin_Vel": self.lin_vel,
            "Chassis_Ang_Vel": self.ang_vel
        }

