# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 16:40:25 2019

@author: Nicolai
----------------
"""

#!/usr/bin/python3
import ctypes
from ctypes import cdll

libc = cdll.LoadLibrary("C:\\Users\\Admin\\OneDrive\\FH Mechatronik\\3. Semester\\Applied Robotics\\Project\\LaB3R\\backwards_kinematic\\back_kin_dll\\output\\back_kin.dll")
start_robot = libc.start_robot
home = libc.home
back_kin = libc.back_kin
stop_robot = libc.stop_robot

pn = start_robot()
home(pn)
back_kin(ctypes.c_float(200), ctypes.c_float(60), ctypes.c_float(15), pn)
home(pn)
back_kin(ctypes.c_float(200), ctypes.c_float(-60), ctypes.c_float(15), pn)
home(pn)
back_kin(ctypes.c_float(200), ctypes.c_float(60), ctypes.c_float(15), pn)
home(pn)
back_kin(ctypes.c_float(200), ctypes.c_float(-60), ctypes.c_float(15), pn)
home(pn)
back_kin(ctypes.c_float(200), ctypes.c_float(60), ctypes.c_float(15), pn)
home(pn)
back_kin(ctypes.c_float(200), ctypes.c_float(-60), ctypes.c_float(15), pn)
home(pn)
back_kin(ctypes.c_float(200), ctypes.c_float(60), ctypes.c_float(15), pn)
home(pn)
back_kin(ctypes.c_float(200), ctypes.c_float(-60), ctypes.c_float(15), pn)
stop_robot(pn)


