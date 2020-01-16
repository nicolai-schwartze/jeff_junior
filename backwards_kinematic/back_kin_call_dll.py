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

libc = cdll.LoadLibrary("C:\\Users\\Admin\\OneDrive\\FH Mechatronik\\3. Semester\\Applied Robotics\\Project\\jeff_junior\\backwards_kinematic\\back_kin_dll\\output\\back_kin.dll")
robot_start = libc.robot_start
robot_home = libc.robot_home
robot_drive = libc.robot_drive
robot_reached_target = libc.robot_reached_target
robot_stop = libc.robot_stop


pn = robot_start()

robot_home(pn)
robot_drive(ctypes.c_float(200), ctypes.c_float(60), ctypes.c_float(15), pn)

while 1:
    retVal = robot_reached_target(ctypes.c_float(200), ctypes.c_float(60), ctypes.c_float(15), pn)
    print("false")
    if retVal:
        print("true")
        break
    
robot_stop(pn)


