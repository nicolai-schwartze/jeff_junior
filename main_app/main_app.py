# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 13:18:08 2020

@author: Nicolai
----------------
"""

import cv2
import ctypes
from ctypes import cdll
import time
import numpy as np
import sys

sys.path.append('../vision/detection/')
import laserpoint_detection as dect

if __name__ == '__main__':
    
    print("starting main app")
    
    print("loading dll")
    libc = cdll.LoadLibrary("..\\backwards_kinematic\\back_kin_dll\\output\\back_kin.dll")
    robot_start = libc.robot_start
    robot_home = libc.robot_home
    robot_drive = libc.robot_drive
    robot_reached_target = libc.robot_reached_target
    robot_stop = libc.robot_stop
    
    print("starting robot")
    pn = robot_start()
    robot_home(pn)
    
    print("starting opencv")
    leftCameraIndex = 2
    rightCameraIndex = 0
    left = cv2.VideoCapture(leftCameraIndex)
    right = cv2.VideoCapture(rightCameraIndex)
    
    print("loading camera matrix")
    cPML = np.load("../vision/calibration/cameraProjectionMatrixLeft.npy")
    cPMR = np.load("../vision/calibration/cameraProjectionMatrixRight.npy")
    
    print("initialising laser point detection")
    # get point by template matching
    greenTemplate = cv2.imread("../vision/detection/green_template.png")
    greenSize = np.shape(greenTemplate)
    redTemplate = cv2.imread("../vision/detection/red_template.png")
    redSize = np.shape(redTemplate)
    
    while(True):
        
        left.grab()
        right.grab()
        _, leftFrame = left.retrieve()
        _, rightFrame = right.retrieve()
        
        gLP2D = dect.getLaserPointTemplateMatching(leftFrame, rightFrame, greenTemplate)
        gLP3D = dect.get3DPoint(cPML, cPMR, gLP2D)
        
        rLP2D = dect.getLaserPointTemplateMatching(leftFrame, rightFrame, redTemplate)
        rLP3D = dect.get3DPoint(cPML, cPMR, rLP2D)
        
        cv2.rectangle(leftFrame, (gLP2D[0][0], gLP2D[0][1]), \
                      (gLP2D[0][0]+greenSize[0], gLP2D[0][1]+greenSize[1]), \
                      (0,255,0))
            
        cv2.rectangle(rightFrame, (gLP2D[1][0], gLP2D[1][1]), \
                      (gLP2D[1][0]+greenSize[0], gLP2D[1][1]+greenSize[1]), \
                      (0,255,0))
            
        cv2.rectangle(leftFrame, (rLP2D[0][0], rLP2D[0][1]), \
                      (rLP2D[0][0]+redSize[0], rLP2D[0][1]+redSize[1]), \
                      (0,0,255))
            
        cv2.rectangle(rightFrame, (rLP2D[1][0], rLP2D[1][1]), \
                      (rLP2D[1][0]+redSize[0], rLP2D[1][1]+redSize[1]), \
                      (0,0,255))
            
        
        
        cv2.imshow('left', leftFrame)
        cv2.imshow('right', rightFrame)
        key = cv2.waitKey(1) & 0xFF
        if not (key == 255):
            if key == ord('q'):
                break 
            
    cv2.destroyAllWindows()
    
    
    
    
    