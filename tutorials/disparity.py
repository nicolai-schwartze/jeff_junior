# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 17:39:25 2019

@author: Nicolai
"""

import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
imgL = cv.imread('camera_left.jpg',0)
imgR = cv.imread('camera_right.jpg',0)
stereo = cv.StereoBM_create(numDisparities=32, blockSize=15)

disparity = stereo.compute(imgL,imgR)
plt.imshow(disparity,'gray')
plt.show()