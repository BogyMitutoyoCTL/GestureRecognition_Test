from collections import deque
import cv2
import sys
import numpy as np
"""
HandRecognizer Class
Provides functions to extract hand contours, as well as positional data
from provided contour.
"""
class HandRecognizer():
    """
    Constructor
    :param buffersize
    Constructor initializes deque of size buffersize to track positional data for evaluation of
    hand movement. Initially, deque is filled with zeroes only
    """
    def __init__(self, buffersize = 20):
        self.radius = None
        self.center = None, None
        self.max_area = 0
        self.pts = deque(maxlen=buffersize)
        self.closedcontour = False

    def _getIndexOfMaxContour(self, contours):
        maxArea, index = 0, 0
        for i in range(len(contours)):
            area = cv2.contourArea(contours[i])
            if area > maxArea:
                maxArea = area
                index = i
        return index

    """
    _extractHand
    Can only be called by functions that provide contours.
    Extracts largest contour (assumed to be hand due to filtering) as well as moments
    and derived "center" of contour, and finds minimum enclosing circle and associated radius
    """
    def _extractHand(self, contours, hierarchy):
        # only starts if provided contours are nonempty
        if contours:
            # finds largest contour in provided contours
            index = self._getIndexOfMaxContour(contours)
            cnt = contours[index]
            if hierarchy is not None:
                self.closedcontour = False if hierarchy[0][index][2] < 0 else True
            handLen = cv2.arcLength(cnt, True)
            handContour = cv2.approxPolyDP(cnt, 0.001 * handLen, True)
            self.minX, self.minY, self.handWidth, self.handHeight = cv2.boundingRect(handContour)

            hullHandContour = cv2.convexHull(handContour, returnPoints=False)
            hullPoints = [handContour[i[0]] for i in hullHandContour]
            hullPoints = np.array(hullPoints, dtype=np.int32)
            defects = cv2.convexityDefects(handContour, hullHandContour)


            # finds minimum enclosing circle's radius
            (_, self.radius) = cv2.minEnclosingCircle(cnt)
            # finds optical center of contour by usage of its moments
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                self.center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                if self.radius > 10:
                    # adds current center to deque for tracking
                    self.pts.appendleft(self.center)
                    cnt = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            else:
                self.center = (None,None)

            self.main_contour = cnt
        else:
            self.radius = None
            self.pts.clear()

    """
    getMainContour
    Provides Largest found contour
    """
    def getMainContour(self, contours):
        self._extractHand(contours)
        return self.main_contour

    """
    getCenterXYRadius
    provides X/Y-Coordinates and Radius of calculated "Center" of contour
    """
    def getCenterXYRadius(self, contours, hierarchy):
        self._extractHand(contours, hierarchy)
        return self.center[0], self.center[1], self.radius

    """
    getPts
    provides positional data of hand in deque
    """
    def getPts(self, contours, hierarchy):
        self._extractHand(contours, hierarchy)
        return self.pts