# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 09:30:11 2020

@author: Nicolai
----------------
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt



def getRedLaserPoint(videoCaptureLeft, videoCaptureRight, \
                     cProjectionMatrixLeft, cProjectionMatrixRight):
    point = np.zeros((4,1))
    
    # take images
    videoCaptureLeft.grab()
    videoCaptureRight.grab()
    _, leftFrame = videoCaptureLeft.retrieve()
    _, rightFrame = videoCaptureRight.retrieve()
    
    # find red point
    print("asdf")
    
    # multiply with camera matrix
    
    return (leftFrame, rightFrame)


def getGreenLaserPoint(videoCaptureLeft, videoCaptureRight, \
                     cProjectionMatrixLeft, cProjectionMatrixRight):
    point = np.zeros((4,1))
    
    # take images
    videoCaptureLeft.grab()
    videoCaptureRight.grab()
    _, leftFrame = videoCaptureLeft.retrieve()
    _, rightFrame = videoCaptureRight.retrieve()
    
    # find green point
    greenDot = cv2.inRange(leftFrame, (155, 174, 138), (165, 180, 145))
    np.mean(np.argwhere(greenDot>=255),0)
    
    # triangulate with camera matrix
    
    # remove 4th element of vector
    
    return (leftFrame, rightFrame)
    



if __name__ == "__main__":
    print("start test")
    
    leftCameraIndex = 2
    rightCameraIndex = 0
    left = cv2.VideoCapture(leftCameraIndex)
    right = cv2.VideoCapture(rightCameraIndex)
    cPML = np.load("..\calibration\cameraProjectionMatrixLeft.npy")
    cPMR = np.load("..\calibration\cameraProjectionMatrixRight.npy")
    (leftFrame, rightFrame) = getGreenLaserPoint(left, right, cPML, cPMR)
    
    