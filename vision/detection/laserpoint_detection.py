# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 09:30:11 2020

@author: Nicolai
----------------
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt


def getLaserPoint(videoCaptureLeft, videoCaptureRight, \
                  cProjectionMatrixLeft, cProjectionMatrixRight, \
                  lowHSV, highHSV):
    
    # take images
    videoCaptureLeft.grab()
    videoCaptureRight.grab()
    _, leftFrame = videoCaptureLeft.retrieve()
    _, rightFrame = videoCaptureRight.retrieve()
    
    # find dot points
    leftFrame_hsv = cv2.cvtColor(leftFrame, cv2.COLOR_BGR2HSV)
    leftDotImage = cv2.inRange(leftFrame_hsv, lowHSV, highHSV)
    rightFrame_hsv = cv2.cvtColor(rightFrame, cv2.COLOR_BGR2HSV)
    rightDotImage = cv2.inRange(rightFrame_hsv, lowHSV, highHSV)
    
    # make dot bigger with dialate
    kernel = np.ones((10,10),np.uint8)
    leftDil = cv2.dilate(leftDotImage, kernel)
    rightDil = cv2.dilate(rightDotImage, kernel)
    
    # find blobs in image
    leftBlob, _ = cv2.findContours(leftDil,cv2.RETR_TREE,\
                                   cv2.CHAIN_APPROX_SIMPLE)
    rightBlob, _ = cv2.findContours(rightDil,cv2.RETR_TREE,\
                                    cv2.CHAIN_APPROX_SIMPLE)
        
    # standard value of M when no Point found
    lM = {"m10": 0, "m01": 0, "m00": 1}
    rM = {"m10": 0, "m01": 0, "m00": 1}
    
    if len(leftBlob) >= 1:
        lM = cv2.moments(leftBlob[0])
    
    if len(rightBlob) >= 1:
        rM = cv2.moments(rightBlob[0])
 
    lX = int(lM["m10"] / lM["m00"])
    lY = int(lM["m01"] / lM["m00"])
    
    lP = np.array([[lX], [lY]],dtype=np.float)
    
    rX = int(rM["m10"] / rM["m00"])
    rY = int(rM["m01"] / rM["m00"])
    
    rP = np.array([[rX], [rY]],dtype=np.float)
    
    # triangulate with camera matrix
    P = cv2.triangulatePoints(cProjectionMatrixLeft, cProjectionMatrixRight,\
                              lP, rP)
    
    # remove 4th element of vector
    P = P/P[3][0]
    
    return P[0:3,0]
    



if __name__ == "__main__":
    print("start test")
    
    leftCameraIndex = 2
    rightCameraIndex = 0
    left = cv2.VideoCapture(leftCameraIndex)
    right = cv2.VideoCapture(rightCameraIndex)
    cPML = np.load("..\calibration\cameraProjectionMatrixLeft.npy")
    cPMR = np.load("..\calibration\cameraProjectionMatrixRight.npy")
    redLowHSV = (1,94,200)
    redHighHSV = (67, 145, 255)
    greenLowHSV = (67,51,200)
    greenHighHSV = (113,145,255)
    laserPoint = getLaserPoint(left, right, cPML, cPMR, \
                               greenLowHSV, greenHighHSV)
    print(laserPoint)
    
    