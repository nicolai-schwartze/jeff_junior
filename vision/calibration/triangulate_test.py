# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 10:49:34 2020

@author: Nicolai
----------------
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt

if __name__ == "__main__":
    
    leftCameraIndex = 2
    rightCameraIndex = 0
    
    left = cv2.VideoCapture(leftCameraIndex)
    right = cv2.VideoCapture(rightCameraIndex)
    
    cMR = None
    cML = None
    rM = None
    tV = None
    cMR = np.load("cameraMatrixRight.npy")
    cML = np.load("cameraMatrixLeft.npy")
    dL = np.load("distortionLeft.npy")
    dR = np.load("distortionRight.npy")
    rM = np.load("rotationMatrix.npy")
    tV = np.load("translationVector.npy")
    
    P1 = np.dot(cML, np.array([[1,0,0,0], [0,1,0,0], [0,0,1,0]]))
    RR = np.c_[rM, tV]
    P2 = np.dot(cMR, RR)
    
    left.grab()
    right.grab()
    
    _, leftFrame = left.retrieve()
    _, rightFrame = right.retrieve()
    
    leftFrame = cv2.cvtColor(leftFrame,cv2.COLOR_BGR2GRAY)
    rightFrame = cv2.cvtColor(rightFrame,cv2.COLOR_BGR2GRAY)
    
    cv2.imwrite("line_300_left.png", leftFrame)
    cv2.imwrite("line_300_right.png", rightFrame)

    
    
    
    