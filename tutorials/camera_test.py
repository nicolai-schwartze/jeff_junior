# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 09:03:08 2019

@author: Nicolai
----------------
"""
import cv2

print("use q to quit the process")
print("use space-bar to take a picture")

# left = cv2.VideoCapture(2)
right = cv2.VideoCapture(0)

while(True):
    if not (right.grab()): # left.grab() and 
        print("could not grab cameras")
        break

    # _, leftFrame = left.retrieve()
    _, rightFrame = right.retrieve()

    # cv2.imshow('left', leftFrame)
    cv2.imshow('right', rightFrame)
    
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('q'):
        break
    if cv2.waitKey(1) & 0xFF == ord(' '):
        print("yeah")

# left.release()
right.release()
cv2.destroyAllWindows()