#!/usr/bin/env python3
#
# Created on Thu Apr 15 2021
#
# Arthur Lang
# problem2.py
#

import sys
import cv2

from src.PersonDetector import PersonDetector

def help():
    print("Usage: ./problem2 imgPath")

def main():
    av = sys.argv
    if (len(av) != 2):
        help()
        return (1)
    # detect = PersonDetector("darknet/yolov3.weights", "darknet/yolov3.cfg", "darknet/coco.names")
    # img = cv2.imread(av[1])
    img=av[1]
    detect = PersonDetector("darknet/yolov3.weights", "darknet/yolov3.cfg", "darknet/coco.names", img)
    # cv2.imshow("readed", img)
    detect.countPeople()
    return 0

if __name__ == "__main__":
    main()