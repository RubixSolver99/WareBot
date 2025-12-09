#!/usr/bin/python3
# Drive the SCUTTLE while visualizing a simple LIDAR point cloud in NodeRED

import socket
import json
import numpy as np
from basics.L1_lidar import Lidar
import basics.L2_vector as vec
import basics.L2_speed_control as sc
from time import sleep
import time
from threading import Thread

IP = "127.0.0.1"
DASHBOARD_PORT = 3555

CARTESIAN_SCALE_X = 1.5    # Scale factor to convert to meters
CARTESIAN_SCALE_Y = 1.5    # Scale factor to convert to meters

class ObstacleDetection:

    def __init__(self):
        #UPD communication#
        self.dashBoardDatasock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dashBoardDatasock.bind((self.IP, self.port))
        self.dashBoardDatasock.settimeout(.25)

        #NodeRED data in#
        self.dashBoardData = None

        #LIDAR Controller#
        self.lidar = Lidar()
        self.lidar.connect()
        self.lidarControllerThread = self.lidar.run()

        #LIDAR Thread#   
        lidarPubThread = Thread(target=self.scan_loop, daemon=True)
        lidarPubThread.start()

    def scan_loop(self):
        start_time = time.time()
        while True:
            data = self.cartesian_scan()
            data_msg = data.encode('utf-8')
            self.dashBoardDatasock.sendto(data_msg, (IP, DASHBOARD_PORT))
            sleep(0.5)

    def cartesian_scan(self):
        rows = ''
        polar_data = self.lidar.get()
        if polar_data is None:
            return rows

        for d,t in polar_data:
            if d < 3.5:
                cartesian_point = vec.polar2cart(d,t)
                cartesian_point = (cartesian_point[0] * CARTESIAN_SCALE_X, cartesian_point[1] * CARTESIAN_SCALE_Y)
                rows += self.format_row(cartesian_point)

        return rows[:-1]

    # Format the x,y lidar coordinates so that the bubble-chart can display them
    def format_row(self, point, r=3):
        x, y = point
        return '{x: ' + str(x) + ', y: ' + str(y) + ', r:' + str(r) + '},'

if __name__ == "__main__":

    robot = ObstacleDetection()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        robot.lidar.kill(robot.lidarControllerThread)
        print("Stopping robot")