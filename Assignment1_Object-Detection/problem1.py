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

from src.Matcher import Matcher

REF_IMG = "ressources/test-image.jpg"
TEMPLATE = "ressources/template.jpg"

# if need to remove background: https://towardsdatascience.com/background-removal-with-python-b61671d1508a

def saveROI():
    refImg = cv2.imread(REF_IMG, cv2.IMREAD_COLOR)
    # select roi
    roi = cv2.selectROI(refImg)
    if (roi[0] != 0 and roi[1] != 0 and roi[2] != 0 and roi[3] != 0): # everything went good with roi
        imgCrop = refImg[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
        cv2.imwrite("ressources/template.jpg", imgCrop)
    cv2.destroyAllWindows()

def help():
    res = "Usage: ./problem1.py [OPTION]\nMatch a picture from a template."
    res += "\n\n  -e, --extract\t\t\tgenerate a template image that can be extract by the program."
    res += "\n  -h, --help\t\t\tDislay help."
    return res

def main():
    av = sys.argv
    if (len(av) > 1):
        if (av[1] == "--extract" or av[1] == "-e"):
            saveROI()
        elif (av[1] == "--help" or av[1 == "-h"]):
            print(help())
            return
    mtch = Matcher()
    cv2.imshow("Matches", mtch.match(REF_IMG, TEMPLATE))
    cv2.waitKey()
    return 0

if __name__ == "__main__":
    main()
