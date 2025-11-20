# Motors Program for SCUTTLE running RasPi
# This example sends commands to two motors on the appropriate pins for H-bridge
# For pin mapping, see Wiring Guide Pi on the SCUTTLE webpage.
# Last update: 2020.11 with improved PWM method

# Import external libraries
import gpiozero                             # used for PWM outputs
from gpiozero import PWMOutputDevice as pwm # for driving motors, LEDs, etc
import time                                 # for keeping time
import numpy as np                          # for handling arrays

drive_freq = 150                            # motor driving frequency

# Broadcom (BCM) pin numbering for RasPi is as follows:             PHYSICAL:       NAME:
left_drive_chA  = pwm(17, frequency=drive_freq,initial_value=0)     # PIN 11        GPIO17
left_drive_chB  = pwm(18, frequency=drive_freq,initial_value=0)     # PIN 12        GPIO18
right_drive_chA = pwm(22, frequency=drive_freq,initial_value=0)     # PIN 15        GPIO22
right_drive_chB = pwm(23, frequency=drive_freq,initial_value=0)     # PIN 16        GPIO23
forklift_chA    = pwm(24, frequency=drive_freq,initial_value=0)     # PIN 18        GPIO24
forklift_chB    = pwm(25, frequency=drive_freq,initial_value=0)     # PIN 22        GPIO25

def compute_pwm(speed):              # take an argument in range [-1,1]
    if speed == 0:
        x = np.array([0,0])         # set all PWM to zero
    else:
        x = speed + 1.0             # change the range to [0,2]
        chA = 0.5 * x               # channel A sweeps low to high
        chB = 1 - (0.5 * x)         # channel B sweeps high to low
        x = np.array([chA, chB])    # store values to an array
        x = np.round(x,2)           # round the values
    return(x)

def set_left_motor_vel(vel):          # takes at least 0.3 ms
    pwm_val = compute_pwm(vel)
    left_drive_chB.value = pwm_val[0]
    left_drive_chA.value = pwm_val[1]

def set_right_motor_vel(vel):         # takes at least 0.3 ms
    pwm_val = compute_pwm(vel)
    right_drive_chB.value = pwm_val[0]
    right_drive_chA.value = pwm_val[1]

def set_forklift_pos(pos):            # takes at least 0.3 ms
    pwm_val = compute_pwm(pos)
    forklift_chB.value = pwm_val[0]
    forklift_chA.value = pwm_val[1]

set_forklift_pos(0)  # Initialize forklift to neutral position