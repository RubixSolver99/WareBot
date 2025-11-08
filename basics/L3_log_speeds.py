import L1_log as log
import L2_kinematics as k
import L1_motor as motor
import time, numpy as np
from time import sleep
from L1_log import tmpFile

while True:
    pd = k.getPdCurrent()
    motion = np.matmul(k.A, pd)
    print("PDL,PDR: ", pd, "xdot,thetadot: ", motion)
    tmpFile(pd[0], "PDL")         
    tmpFile(pd[1], "PDR")
    tmpFile(motion[0], "xdot")  
    tmpFile(motion[1], "thetadot")
    time.sleep(0.3)
    

