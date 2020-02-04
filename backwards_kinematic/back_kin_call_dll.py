# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 16:40:25 2019

@author: Nicolai
----------------
"""

#!/usr/bin/python3
import ctypes
from ctypes import cdll
import time

libc = cdll.LoadLibrary(".\\back_kin_dll\\output\\back_kin.dll")
robot_start = libc.robot_start
robot_home = libc.robot_home
robot_drive = libc.robot_drive
robot_reached_target = libc.robot_reached_target
robot_stop = libc.robot_stop
robot_set_theta = libc.robot_set_theta

robot_get_theta0 = libc.robot_get_theta0
robot_get_theta1 = libc.robot_get_theta1
robot_get_theta2 = libc.robot_get_theta2


# specify return type for function
# standard return type for a cdll function is an int
robot_get_theta0.restype = ctypes.c_float
robot_get_theta1.restype = ctypes.c_float
robot_get_theta2.restype = ctypes.c_float

pn = robot_start()

robot_home(pn)
robot_drive(ctypes.c_float(200), ctypes.c_float(60), ctypes.c_float(15), pn)

while 1:
    retVal = robot_reached_target(ctypes.c_float(200), ctypes.c_float(60), ctypes.c_float(15), pn)
    print("false")
    if retVal:
        print("true")
        break
    
robot_set_theta(ctypes.c_float(0.0), ctypes.c_float(0.0), ctypes.c_float(0.0), pn)
time.sleep(3)

theta0 = robot_get_theta0(pn)
theta1 = robot_get_theta1(pn)
theta2 = robot_get_theta1(pn)
print(str(theta0) + ", " + str(theta1) + ", " + str(theta2))
time.sleep(3)
robot_set_theta(ctypes.c_float(30.0), ctypes.c_float(30.0), ctypes.c_float(-30.0), pn)
time.sleep(3)
theta0 = robot_get_theta0(pn)
theta1 = robot_get_theta1(pn)
theta2 = robot_get_theta2(pn)
print(str(theta0) + ", " + str(theta1) + ", " + str(theta2))
time.sleep(3)

robot_stop(pn)


