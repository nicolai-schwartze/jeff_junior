# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 09:03:08 2019

@author: Nicolai
----------------
"""

import cv2

left = cv2.VideoCapture(1)
# left.set(3,160)
# left.set(4,120)
right = cv2.VideoCapture(2)
# right.set(3,160)
# right.set(4,120)


while(True):
    if not (left.grab() and right.grab()): 
        print("No more frames")
        break

    _, leftFrame = left.retrieve()
    _, rightFrame = right.retrieve()

    cv2.imshow('left', leftFrame)
    cv2.imshow('right', rightFrame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

left.release()
right.release()
cv2.destroyAllWindows()