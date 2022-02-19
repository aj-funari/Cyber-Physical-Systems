#!/usr/bin/env python3
from curses_interface import curses_inter
import struct
import redis
import numpy as np
import cv2
import os
import pickle
import time

Curses = curses_inter()

def toRedis(r,a,n,fnum):
   h, w = a.shape[:2]             # Shape of the h, w and not the 3 colors in the depth of the image
   shape = struct.pack('>II',h,w) # Pack the height and the width variables into variable shape
                                  # Big Endian
   encoded = shape + a.tobytes()  # concatenate the shape variable and the encoded image
   r.hmset(n,{'frame':fnum,'image':encoded})
   return

if __name__ == '__main__':

    r = redis.Redis('140.182.152.47', port=6379, db=0)
    cam = cv2.VideoCapture(0)
    cam.set(3, 320)
    cam.set(4, 240)

    if os.path.exists('../Final_Project/calibration.pckl'):
        f = open('../Final_Project/calibration.pckl', 'rb')
        cameraMatrix, distCoeffs = pickle.load(f)
        f.close()
    else:
        print("You need to calibrate the camera you'll be using. See calibration script.")

    aruco_dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_7X7_250)
    parameters = cv2.aruco.DetectorParameters_create()

    key = 0  
    count = 0
    maximum = 20        # variable for PID loop
    integral = 0        # variable for PID loop
    previous_error = 0  # variable for PID loop
    while key != 27:

        ret, img = cam.read()
        key = cv2.waitKey(1) & 0xFF
        toRedis(r, img, 'latest',count)
        count += 1
        Curses.stdscr.addstr(7, 1, str(count))

        start_time = time.perf_counter()

        if Curses.checking_keys() == 'm':  # Enter manual mode
            while True:
                start_time = time.perf_counter()
                if Curses.checking_keys() == 'q':
                    Curses.stdscr.addstr(3, 1, 'quit manual mode')
                    break
                Curses.manual()
                Curses.stdscr.addstr(3, 1, 'manual mode')
                runtime = (time.perf_counter() - start_time)
                Curses.stdscr.addstr(5, 1, 'manual mode runtime: ')
                Curses.stdscr.addstr(5, 22, str(runtime))

        if Curses.checking_keys() == 'a':  # Enter autonomous mode
            while True:
                start_time = time.perf_counter()
                if Curses.checking_keys() == 'q':
                    Curses.stdscr.addstr(3, 1, 'quit autonomous mode')
                    break
                Curses.stdscr.addstr(3, 1, 'autonomous mode ')

                ret, img = cam.read()
                key = cv2.waitKey(1) & 0xFF
                toRedis(r, img, 'latest',count)
                # count += 1
                # print(count)

                aruco_dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_7X7_250)
                parameters = cv2.aruco.DetectorParameters_create()

                corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(img, aruco_dictionary, parameters=parameters)
                if ids is not None:
                    x = (corners[0][0][0][0] + corners[0][0][1][0] + corners[0][0][2][0] + corners[0][0][3][0])
                    position = (x / 4)
                    
                    # PID Loop
                    error = position - 160                # when arUco is centered, error is 0
                    Curses.stdscr.addstr(7, 1, "error value: ")
                    Curses.stdscr.addstr(7, 18, str(error))

                    integral += error                     # an accumulation of all error values -> large number
                    derivative = error - previous_error   # difference between each previous error -> small number
                    previous_error = error

                    Curses.adjust_PID()
                    p = float(Curses.P)
                    pterm = error * p
                    # iterm = 0
                    i = float(Curses.I)
                    iterm = integral * i
                    # dterm = 0
                    d = float(Curses.D)
                    dterm = derivative * d

                    output = pterm + iterm + dterm
                    Curses.stdscr.addstr(9, 1, "output value: ")
                    Curses.stdscr.addstr(9, 15, str(output))

                    if (output > maximum):
                        output = maximum
                    if (output < -maximum):
                        output = -maximum
        
                    if (output < 0):
                        left = maximum + output             # left < right
                        right = maximum                     # right wheel spinning faster than left
                        Curses.Ab.setMotor(-right, -left)   # result -> left turn
                    else:  # output > 0
                        left = maximum                      # right > left
                        right = maximum - output            # left wheel spinning faster than left
                        Curses.Ab.setMotor(-right, -left)   # result -> right turn

                runtime = (time.perf_counter() - start_time)
                Curses.stdscr.addstr(5, 1, 'autonomous mode runtime: ')
                Curses.stdscr.addstr(5, 26, str(runtime))

        runtime = (time.perf_counter() - start_time)
        Curses.stdscr.addstr(5, 1, 'main loop runtime: ')
        Curses.stdscr.addstr(5, 20, str(runtime))
