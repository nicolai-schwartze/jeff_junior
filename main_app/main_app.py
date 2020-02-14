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
import tkinter as tk

sys.path.append('../vision/detection/')
import laserpoint_detection as dect
import template_creation_app as tca

if __name__ == '__main__':
    
    print("starting main app")
    
    print("configurate template")
    WIDTH, HEIGHT = 640, 570
    window = tk.Tk()
    window.title("Configurate Laser Template")
    window.geometry('%sx%s' % (WIDTH, HEIGHT))
    window.configure(background='grey')
    templatePath = "../vision/detection/"
    
    appWindow = tca.TemplateCalibrationApp(window, templatePath)
    
    appWindow.videoStream()
    window.mainloop()
    print("closing template creation app")
    
    print("loading dll")
    libc = cdll.LoadLibrary("..\\backwards_kinematic\\back_kin_dll\\output\\back_kin.dll")
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
        
        
        theta0 = robot_get_theta0(pn)
        theta1 = robot_get_theta1(pn)
        theta2 = robot_get_theta2(pn)
        
            
        gLPB = dect.transformPointFromCameraToBase(gLP3D, theta0, theta1, theta2)
        
        
        r_theta0 = np.arctan(gLPB[1]/gLPB[0])
        r_theta1 = np.array([0.0])
        r_theta2 = (-1)*np.arctan((gLPB[2] - 100 - 100*np.cos(np.deg2rad(theta1)))/(np.sqrt(gLPB[0]**2 + gLPB[1]**2) - 50 -100*np.sin(np.deg2rad(theta1))))
       
        r_theta0 = np.rad2deg(r_theta0)
        r_theta1 = np.rad2deg(r_theta1)
        r_theta2 = np.rad2deg(r_theta2)
        
        
        robot_set_theta(ctypes.c_float(r_theta0[0]), ctypes.c_float(r_theta1[0]), ctypes.c_float(r_theta2[0]), pn)
        
        
        
        cv2.imshow('left', leftFrame)
        cv2.imshow('right', rightFrame)
        key = cv2.waitKey(1) & 0xFF
        if not (key == 255):
            if key == ord('q'):
                break 
            
    robot_stop(pn)
    cv2.destroyAllWindows()
    
    
    
    
    