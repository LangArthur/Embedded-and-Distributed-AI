#!/usr/bin/env python3

#
# Created on Mon Apr 12 2021
#
# Arthur Lang
# main.py
#

import cv2
import sys

from src.ROIDetector import ROIDetector

REF_IMG = "ressources/test-image.jpg"

def extractObj(img):
    return img

def saveRefImg():
    roiDetector = ROIDetector()
    refImg = cv2.imread(REF_IMG, cv2.IMREAD_COLOR)
    if (roiDetector.askRoi(refImg) == 0): # everything went good with roi
        rois = roiDetector.crop(refImg)
        for i, roi in enumerate(rois):
            cv2.imwrite("ressources/template-" + str(i + 1) + ".jpg", extractObj(roi))

def main():
    av = sys.argv
    if (len(av) > 1 and (av[1] == "--extract" or av[1] == "-e")):
        saveRefImg()
    return 0

if __name__ == "__main__":
    main()