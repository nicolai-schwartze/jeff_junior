# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 09:03:08 2019

@author: Nicolai
----------------
"""
import cv2
import numpy as np

# define configuration here
leftPath = "./chessboard_data/camera_left/"
rightPath = "./chessboard_data/camera_right/"
chessboardSize = (8,8)
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

# left = cv2.VideoCapture(leftCameraIndex)
right = cv2.VideoCapture(rightCameraIndex)

point3D = np.zeros((chessboardSize[0]*chessboardSize[1],3), np.float32)
point3D[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

points3DList = [] 
cornersListRight = [] 
cornersListLeft = []

while(True):
    if not (right.grab()): # and left.grab()
        print("")
        print(50*"=")
        print("could not grab cameras")
        print("quitting")
        print(50*"=")
        print("")
        break
    
    # take images from camera
    # _, leftFrame = left.retrieve()
    _, rightFrame = right.retrieve()
    
    # convert to gray-scale 
    # leftFrame = cv2.cvtColor(leftFrame,cv2.COLOR_BGR2GRAY)
    rightFrame = cv2.cvtColor(rightFrame,cv2.COLOR_BGR2GRAY)

    # cv2.imshow('left', leftFrame)
    cv2.imshow('right', rightFrame)
    
    key = cv2.waitKey(1) & 0xFF
    
    if not (key == 255):
        if key == ord('q'):
            break
        if key == ord(' '):
            print("")
            print(50*"=")
            print("checking for chessboard")
            # retLeft, cornersLeft = cv2.findChessboardCorners(leftFrame, chessboardSize,None)
            
            retRight, cornersRight = cv2.findChessboardCorners(rightFrame, chessboardSize,None)
            if (retRight): # and retLeft
                # cornersLeft = cv2.cornerSubPix(leftFrame,cornersLeft, (5,5), (-1,-1), subPixelingCriteria)
                cornersRight = cv2.cornerSubPix(rightFrame,cornersRight, (5,5), (-1,-1), subPixelingCriteria)
                points3DList.append(point3D)
                cornersListRight.append(cornersRight)
                # cornersListLeft.apeend(cornersLeft)
                print("picture number: " + str(pictureCounter))
                print("found chessboard corners")
                if(saveImages):
                    pictureNameL = "left_" + str(pictureCounter) + ".png"
                    print("save picture: " + pictureNameL)
                    #cv2.imwrite(leftPath + pictureNameL, leftFrame)
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

# left.release()
right.release()
cv2.destroyAllWindows()

if pictureCounter >= minNrImages:
    print("")
    print(50*"=")
    print("calibrating camera")
    print(50*"=")
    print("")
    
    retRight, cameraMatrixRight, distortionRight, rvecsRight, tvecsRight = cv2.calibrateCamera(points3DList, cornersListRight, rightFrame.shape[::-1], None, None)
    # retLeft, cameraMatrixLeft, distortionLeft, rvecsLeft, tvecsLeft = cv2.calibrateCamera(points3DList, cornersListLeft, leftFrame.shape[::-1], None, None)
    # TERMINATION_CRITERIA = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # (_, _, _, _, _, rotationMatrix, translationVector, _, _) = cv2.stereoCalibrate(points3DList, cornersListLeft, cornersListRight, cameraMatrixLeft, leftDistortionCoefficients, cameraMatrixRight, distortionRight, rightFrame.shape[::-1], None, None, None, None, cv2.CALIB_FIX_INTRINSIC, TERMINATION_CRITERIA)

