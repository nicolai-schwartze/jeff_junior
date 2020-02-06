# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 09:30:11 2020

@author: Nicolai
----------------
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt


def getLaserPointBlobDetection(leftFrame, rightFrame, lowHSV, highHSV):
    
    # find dot points
    leftFrame_hsv = cv2.cvtColor(leftFrame, cv2.COLOR_BGR2HSV)
    leftDotImage = cv2.inRange(leftFrame_hsv, lowHSV, highHSV)
    rightFrame_hsv = cv2.cvtColor(rightFrame, cv2.COLOR_BGR2HSV)
    rightDotImage = cv2.inRange(rightFrame_hsv, lowHSV, highHSV)
    
    # make dot bigger with dialate
    kernel = np.ones((30,30),np.uint8)
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
    
    return [lP, rP]
    




def getLaserPointTemplateMatching(leftFrame, rightFrame, template):
    
    resLeft = cv2.matchTemplate(leftFrame,template,cv2.TM_CCOEFF_NORMED)
    resRight = cv2.matchTemplate(rightFrame,template,cv2.TM_CCOEFF_NORMED)
    
    # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(resLeft)
    _, _, _, locLeft = cv2.minMaxLoc(resLeft)
    _, _, _, locRight = cv2.minMaxLoc(resRight)
    
    lP = np.array([[locLeft[0]],[locLeft[1]]],dtype=np.float)
    rP = np.array([[locRight[0]],[locRight[1]]],dtype=np.float)
    
    return [lP, rP]




def get3DPoint(cPrpjectionMatrixL, cProjectionMatrixR, listPoints2D):
    
    # triangulate with camera matrix
    P = cv2.triangulatePoints(cPrpjectionMatrixL, cProjectionMatrixR, \
                              listPoints2D[0], listPoints2D[1])
    
    # remove 4th element of vector
    P = P/P[3][0]
    
    return P[0:3,:]


def transformPointFromCameraToBase(pointC, theta0, theta1, theta2):
    
    pointC = np.array([pointC[0], pointC[1], pointC[2], [1]])
    
    D1 = 100
    A2 = 50
    A3 = 100
    DF = 68

    c1 = np.cos(np.deg2rad(theta0))
    s1 = np.sin(np.deg2rad(theta0))
    c2 = np.cos(np.deg2rad(theta1))
    s2 = np.sin(np.deg2rad(theta1))
    c3 = np.cos(np.deg2rad(theta2))
    s3 = np.sin(np.deg2rad(theta2))


    T = np.array([[ -c1*c2*s3 -c1*c3*s2, -s1, c1*c2*c3 - c1*s2*s3, \
                    A2*c1 + DF*(c1*c2*c3 - c1*s2*s3) + A3*c1*s2], \
                  [ -c2*s1*s3 - c3*s1*s2, c1, c2*c3*s1 - s1*s2*s3, \
                    A2*s1 + DF*(c2*c3*s1 - s1*s2*s3) + A3*s1*s2], \
                  [ s2*s3 - c2*c3, 0.0, -c2*s3 - c3*s2,             \
                    D1 + A3*c2 - DF*(c2*s3 + c3*s2)],
                  [ 0.0, 0.0, 0.0, 1.0 ]])
        
    HE = np.array([[0.0, 1.0, 0.0, -28.5], [-1.0, 0.0, 0.0, 45.0], \
                   [0.0, 0.0, 1.0, 28.0], [0.0, 0.0, 0.0, 1.0]])

    pointB = np.dot(np.dot(T, HE), pointC)
    return pointB
    
    




if __name__ == "__main__":
    
    print("start test")
    
    leftCameraIndex = 2
    rightCameraIndex = 0
    left = cv2.VideoCapture(leftCameraIndex)
    right = cv2.VideoCapture(rightCameraIndex)
    cPML = np.load("..\calibration\cameraProjectionMatrixLeft.npy")
    cPMR = np.load("..\calibration\cameraProjectionMatrixRight.npy")
    
    # get point by blob detection
    redLowHSV = (1,94,200)
    redHighHSV = (67, 145, 255)
    greenLowHSV = (67,51,200)
    greenHighHSV = (113,145,255)
    
    # get point by template matching
    greenTemplate = cv2.imread("green_template.png")
    greenSize = np.shape(greenTemplate)
    redTemplate = cv2.imread("red_template.png")
    redSize = np.shape(redTemplate)
    
    while(True):
        
        left.grab()
        right.grab()
        _, leftFrame = left.retrieve()
        _, rightFrame = right.retrieve()
        
        # gLP2D = getLaserPointTemplateMatching(leftFrame, rightFrame, greenTemplate)
        # gLP3D = get3DPoint(cPML, cPMR, gLP2D)
        # gLPB = transformPointFromCameraToBase(gLP3D, 0.0, 0.0, 0.0)
        # print(gLPB)
        
        rLP2D = getLaserPointTemplateMatching(leftFrame, rightFrame, redTemplate)
        rLP3D = get3DPoint(cPML, cPMR, rLP2D)
        rLPB = transformPointFromCameraToBase(rLP3D, 0.0, 0.0, 0.0)
        print(rLPB)
        
        # print(np.linalg.norm(rLP3D - gLP3D))
        # print(50*"-")
        
        # cv2.rectangle(leftFrame, (gLP2D[0][0], gLP2D[0][1]), \
        #               (gLP2D[0][0]+greenSize[0], gLP2D[0][1]+greenSize[1]), \
        #               (0,255,0))
            
        # cv2.rectangle(rightFrame, (gLP2D[1][0], gLP2D[1][1]), \
        #               (gLP2D[1][0]+greenSize[0], gLP2D[1][1]+greenSize[1]), \
        #               (0,255,0))
            
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
    
    
    
    
    