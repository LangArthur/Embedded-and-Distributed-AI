#!/usr/bin/env python3
#
# Created on Thu Apr 15 2021
#
# Arthur Lang
# Matcher.py
#

import cv2

class Matcher():
    def __init__(self):
        # use sift since surf is not available in pip package of opencv
        self.sift = cv2.SIFT_create()
        # FLANN parameters
        FLANN_INDEX_KDTREE = 0
        self._matcher = cv2.FlannBasedMatcher(dict(algorithm = FLANN_INDEX_KDTREE, trees = 5), dict(checks=50))
        self._lowesRatioConstant = 0.7 # value taken from Opencv Tutorials

    def match(self, refImg, template):
        # read Pictures
        toMatch = cv2.imread(template, cv2.IMREAD_GRAYSCALE)
        refImg = cv2.imread(refImg, cv2.IMREAD_GRAYSCALE)
        # find the keypoints and descriptors
        toMatchKp, toMatchDes = self.sift.detectAndCompute(toMatch, None)
        refKp, refDes = self.sift.detectAndCompute(refImg, None)
        matches = self._matcher.knnMatch(toMatchDes, refDes, k=2)
        # mask to select only good matches
        matchesMask = [[0,0] for i in range(len(matches))]
        # Lowe's ratio test to remove unusefull matches
        for i, (m, n) in enumerate(matches):
            if m.distance < self._lowesRatioConstant * n.distance:
                matchesMask[i]=[1,0]

        draw_params = dict(matchColor = (0,255,0),
                        singlePointColor = (255,0,0),
                        matchesMask = matchesMask,
                        flags = 0)
        return cv2.drawMatchesKnn(toMatch, toMatchKp, refImg, refKp, matches, None, **draw_params)
