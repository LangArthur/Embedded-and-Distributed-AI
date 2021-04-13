#!/usr/bin/env python3

#
# Created on Mon Apr 12 2021
#
# Arthur Lang
# main.py
#

import cv2
import sys
import numpy

REF_IMG = "ressources/test-image.jpg"

# if need to remove background: https://towardsdatascience.com/background-removal-with-python-b61671d1508a

def saveROI():
    refImg = cv2.imread(REF_IMG, cv2.IMREAD_COLOR)
    # select roi
    roi = cv2.selectROI(refImg)
    if (roi[0] != 0 and roi[1] != 0 and roi[2] != 0 and roi[3] != 0): # everything went good with roi
        imgCrop = refImg[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
        cv2.imwrite("ressources/template.jpg", imgCrop)

def main():
    av = sys.argv
    if (len(av) > 1 and (av[1] == "--extract" or av[1] == "-e")):
        saveROI()
    return 0

if __name__ == "__main__":
    main()
