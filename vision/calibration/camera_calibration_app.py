# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 09:03:08 2019

@author: Nicolai
----------------
"""
import cv2
import numpy as np
import os

# define configuration here
leftPath = "./chessboard_data/camera_left/"
rightPath = "./chessboard_data/camera_right/"
chessboardSize = (10,8)
squareSize = 20.5
leftCameraIndex = 2
rightCameraIndex = 0
minNrImages = 15
subPixelingCriteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

print("")
print(50*"=")
print("Instruction: ")
print(50*"=")
print("press | q | to quit the process")
print("press | space-bar | to take a picture")
print(50*"=")
print("")

# user inputs 
saveImages = False
print("")
print(50*"=")
print("do you want to save the pictures")
userAnswer = ""
userAnswer = input()
if(userAnswer == "yes" or userAnswer == "y"): 
    saveImages = True
elif (userAnswer == ""):
    print("no")
else:
    print("images are not saved")
print(50*"=")
print("")


pictureCounter = 0

if (saveImages):
    left = cv2.VideoCapture(leftCameraIndex)
    right = cv2.VideoCapture(rightCameraIndex)

point3D = np.zeros((chessboardSize[0]*chessboardSize[1],3), np.float32)
point3D[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)
point3D = point3D * squareSize

points3DList = [] 
cornersListRight = [] 
cornersListLeft = []

while(saveImages):
    if not (right.grab() and left.grab()):
        print("")
        print(50*"=")
        print("could not grab cameras")
        print("quitting")
        print(50*"=")
        print("")
        break
    
    # take images from camera
    _, leftFrame = left.retrieve()
    _, rightFrame = right.retrieve()
    
    # convert to gray-scale 
    leftFrame = cv2.cvtColor(leftFrame,cv2.COLOR_BGR2GRAY)
    rightFrame = cv2.cvtColor(rightFrame,cv2.COLOR_BGR2GRAY)

    cv2.imshow('left', leftFrame)
    cv2.imshow('right', rightFrame)
    
    key = cv2.waitKey(1) & 0xFF
    
    if not (key == 255):
        if key == ord('q'):
            break
        if key == ord(' '):
            print("")
            print(50*"=")
            print("checking for chessboard")
            retLeft, cornersLeft = cv2.findChessboardCorners(leftFrame, chessboardSize,None)
            retRight, cornersRight = cv2.findChessboardCorners(rightFrame, chessboardSize,None)
            if (retRight and retLeft): 
                cornersLeft = cv2.cornerSubPix(leftFrame,cornersLeft, (5,5), (-1,-1), subPixelingCriteria)
                cornersRight = cv2.cornerSubPix(rightFrame,cornersRight, (5,5), (-1,-1), subPixelingCriteria)
                points3DList.append(point3D)
                cornersListRight.append(cornersRight)
                cornersListLeft.append(cornersLeft)
                print("picture number: " + str(pictureCounter))
                print("found chessboard corners")
                if(saveImages):
                    pictureNameL = "left_" + str(pictureCounter) + ".png"
                    print("save picture: " + pictureNameL)
                    cv2.imwrite(leftPath + pictureNameL, leftFrame)
                    pictureNameR = "right_" + str(pictureCounter) + ".png"
                    print("save picture: " + pictureNameR)
                    cv2.imwrite(rightPath + pictureNameR, rightFrame)
                print(50*"=")
                print("")
                pictureCounter += 1
            else: 
                print("corners not found")
                print("try again")
                print(50*"=")
                print("")

if (saveImages):
    left.release()
    right.release()
    cv2.destroyAllWindows()

if (pictureCounter >= minNrImages) or not saveImages:
    print("")
    print(50*"=")
    print("reading files")
    print(50*"=")
    print("Insruction: ")
    print("| y | take image")
    print("| n | ignore image")
    print(50*"=")

    if(not saveImages):
        (_, _, filenames) = next(os.walk(leftPath))
        fileCount = len(filenames)
        for i in range(fileCount):
            leftFrameBGR = cv2.imread(leftPath+"/left_"+str(i)+".png")
            leftFrame = cv2.cvtColor(leftFrameBGR, cv2.COLOR_BGR2GRAY)
            retLeft, cornersLeft = cv2.findChessboardCorners(leftFrame, chessboardSize,None)
            cornersLeft = cv2.cornerSubPix(leftFrame,cornersLeft, (5,5), (-1,-1), subPixelingCriteria)
            rightFrameBGR = cv2.imread(rightPath+"right_"+str(i)+".png")
            rightFrame = cv2.cvtColor(rightFrameBGR, cv2.COLOR_BGR2GRAY)
            retRight, cornersRight = cv2.findChessboardCorners(rightFrame, chessboardSize,None)
            cornersRight = cv2.cornerSubPix(rightFrame,cornersRight, (5,5), (-1,-1), subPixelingCriteria)
            
            cv2.drawChessboardCorners(leftFrameBGR, chessboardSize, cornersLeft, retLeft)
            cv2.imshow('left', leftFrameBGR)
            cv2.drawChessboardCorners(rightFrameBGR, chessboardSize, cornersRight, retRight)
            cv2.imshow('right', rightFrameBGR)
            while(True):
                key = cv2.waitKey(1) & 0xFF
                if not (key == 255):
                    if key == ord('y') or key == ord('n'):
                        break 
            if key == ord('y'):
                points3DList.append(point3D)
                cornersListLeft.append(cornersLeft)
                cornersListRight.append(cornersRight)
            else: 
                continue
            
    cv2.destroyAllWindows()
    print("calibrating camera")
    print(50*"=")
    (_ , cameraMatrixRight, distortionRight, _, _) = cv2.calibrateCamera(points3DList, cornersListRight, \
                                                                         rightFrame.shape[::-1], None, None)
    (_, cameraMatrixLeft, distortionLeft, _, _) = cv2.calibrateCamera(points3DList, cornersListLeft, \
                                                                      leftFrame.shape[::-1], None, None)
        
    TERMINATION_CRITERIA = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    (_, _, _, _, _, rotationMatrix, translationVector, _, _) = cv2.stereoCalibrate(points3DList, cornersListLeft, cornersListRight, cameraMatrixLeft, distortionLeft, cameraMatrixRight, distortionRight, rightFrame.shape[::-1], None, None, None, None, cv2.CALIB_FIX_INTRINSIC, TERMINATION_CRITERIA)

    print("saving numpy files")
    print(50*"=")
    
    np.save("cameraMatrixRight.npy", cameraMatrixRight)
    np.save("cameraMatrixLeft.npy", cameraMatrixLeft)
    np.save("distortionLeft.npy", distortionLeft)
    np.save("distortionRight.npy", distortionRight)
    np.save("rotationMatrix.npy", rotationMatrix)
    np.save("translationVector.npy", translationVector)
    
    cameraProjectionMatrixLeft = np.dot(cameraMatrixLeft, np.c_[np.eye(3), np.zeros((3,1))])
    cameraProjectionMatrixRight = np.dot(cameraMatrixRight, np.c_[rotationMatrix, translationVector])
    
    np.save("cameraProjectionMatrixLeft.npy", cameraProjectionMatrixLeft)
    np.save("cameraProjectionMatrixRight.npy", cameraProjectionMatrixRight)
    
    print("finished")
    print(50*"=")
    print("")
    
    
    
    