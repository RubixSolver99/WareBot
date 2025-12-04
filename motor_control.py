#!/usr/bin/python3
# Drive the SCUTTLE while receiving commands from NodeRED dashboard

import os
import socket
import json
import numpy as np
import basics.L2_speed_control as sc
import time
from threading import Thread

from gpiozero import Servo as servo                # pyright: ignore[reportMissingImports]
from gpiozero.pins.pigpio import PiGPIOFactory     # pyright: ignore[reportMissingImports]

SERVO_UP_POS = 0.25
SERVO_DOWN_POS = 0.85
PALLET_TARGET_WIDTH = 200  # Target width of pallet in pixels when close enough

class MotorController:

    def __init__(self):

        #Kinematics#
        self.wheelRadius = 0.04
        self.wheelBase = 0.1
        self.A_matrix = np.array([[1/self.wheelRadius, -self.wheelBase/self.wheelRadius], [1/self.wheelRadius, self.wheelBase/self.wheelRadius]])
        self.max_xd = 0.4
        self.max_td = (self.max_xd/self.wheelBase)

        #Forklift Servo Setup#
        os.system('sudo systemctl start pigpiod')               # Start pigpio daemon for precise servo control
        time.sleep(1)                                           # Allow pigpio daemon to initialize

        factory = PiGPIOFactory()
        self.forklift_servo_A = servo(24, pin_factory=factory)                   # PIN 18        GPIO24
        self.forklift_servo_B = servo(25, pin_factory=factory)                   # PIN 22        GPIO25
        self.forklift_down()

        #UPD communication#
        self.IP = "127.0.0.1"
        self.port = 3655
        self.dashBoardDatasock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dashBoardDatasock.bind((self.IP, self.port))
        self.dashBoardDatasock.settimeout(.25)

        #NodeRED data in#
        self.dashBoardData = None

        #NodeRED Data Thread#
        self.dashBoardDataThread = Thread(target=self._dashBoardDataLoop, daemon=True)
        self.dashBoardDataThread.start()

        #Motor Control Thread#
        self.controlThread = Thread(target=self._controlLoop, daemon=True)
        self.controlThread.start()


    def _dashBoardDataLoop(self):
        while True:
            try:
                dashBoardData,recvAddr = self.dashBoardDatasock.recvfrom(1024)
                self.dashBoardData = json.loads(dashBoardData)

            except socket.timeout:
                self.dashBoardData = None

    def _controlLoop(self):
        while True:
            if self.dashBoardData != None:
                try:
                    userInput = self.dashBoardData['one_joystick']['vector']
                    wheelSpeedTarget = self._getWheelSpeed(userInput)
                    sc.driveOpenLoop(wheelSpeedTarget)
                except: 
                    pass

                try:
                    userInput = self.dashBoardData['one_joystick']['buttons']

                    if userInput['A']:
                        print("Forklift Up")
                        self.forklift_up()
                    elif userInput['B']:
                        print("Forklift Down")
                        self.forklift_down()
                except:
                    pass

    def _getWheelSpeed(self,userInputTarget):
        try:
            robotTarget = self._mapSpeeds(np.array([userInputTarget['y'],-1*userInputTarget['x']]))
            wheelSpeedTarget = self._calculateWheelSpeed(robotTarget)
            return wheelSpeedTarget
        except:
            pass
    
    def _mapSpeeds(self,original_B_matrix):
        B_matrix = np.zeros(2)
        B_matrix[0] = self.max_xd * original_B_matrix[0]
        B_matrix[1] = self.max_td * original_B_matrix[1]
        return B_matrix

    def _calculateWheelSpeed(self,B_matrix):
        C_matrix = np.matmul(self.A_matrix,B_matrix)
        C_matrix = np.round(C_matrix,decimals=3)
        return C_matrix


    def getdashBoardData(self):
        return self.dashBoardData
    

    def forklift_down(self):
        for i in range(int(SERVO_UP_POS*100), int(SERVO_DOWN_POS*100), 5):
            pos = i / 100.0
            self.forklift_servo_A.value = pos
            self.forklift_servo_B.value = -pos
            time.sleep(0.05)

    def forklift_up(self):
        self.forklift_servo_A.value = SERVO_UP_POS
        self.forklift_servo_B.value = -SERVO_UP_POS

    def approach_pallet(self, width, angle):
        # Simple proportional controller to drive towards pallet
        Kp_lin = 0.002  # Proportional gain for linear velocity
        Kp_ang = 0.05   # Proportional gain for angular velocity

        lin_vel = Kp_lin * (PALLET_TARGET_WIDTH - width)  # Target width is 200 pixels
        ang_vel = Kp_ang * angle

        # Limit velocities
        lin_vel = max(min(lin_vel, self.max_xd), -self.max_xd)
        ang_vel = max(min(ang_vel, self.max_td), -self.max_td)

        B_matrix = np.array([lin_vel, ang_vel])
        wheelSpeedTarget = self._calculateWheelSpeed(B_matrix)
        sc.driveOpenLoop(wheelSpeedTarget)

        # wheel_measured = kin.getPdCurrent()                     # Wheel speed measurements

        # # If robot is facing target
        # if abs(angle) < angle_margin:                                 
        #     e_width = target_width - w                          # Find error in target width and measured width

        #     # If error width is within acceptable margin
        #     if abs(e_width) < width_margin:
        #         sc.driveOpenLoop(np.array([0.,0.]))             # Stop when centered and aligned
        #         print("Aligned! ",w)
        #         continue

        #     fwd_effort = e_width/target_width                   
            
        #     wheel_speed = ik.getPdTargets(np.array([0.8*fwd_effort, -0.5*angle]))   # Find wheel speeds for approach and heading correction
        #     sc.driveClosedLoop(wheel_speed, wheel_measured, 0)  # Drive closed loop
        #     print("Angle: ", angle, " | Target L/R: ", *wheel_speed, " | Measured L\R: ", *wheel_measured)
        #     continue

        # wheel_speed = ik.getPdTargets(np.array([0, -1.1*angle]))    # Find wheel speeds for only turning

        # sc.driveClosedLoop(wheel_speed, wheel_measured, 0)          # Drive robot
        # print("Angle: ", angle, " | Target L/R: ", *wheel_speed, " | Measured L\R: ", *wheel_measured)

    def exit(self):
        self.forklift_down()
        self.forklift_servo_A.detach()
        self.forklift_servo_B.detach()

        os.system('sudo systemctl stop pigpiod')        # Stop pigpio daemon to prevent servos from constantly running

