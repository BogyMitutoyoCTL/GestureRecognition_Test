from collections import deque
from FilterClass import *
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
        self.filter = Filter()

    """
    _getContour
    Takes frame, applies filter and extracts Contours from filtered frame.
    """
    def _getContour(self, frame):
        edges = self.filter.getEdges(frame)
        _, self.contours, self.hierarchy = cv2.findContours(edges, cv2.RETR_CCOMP,
                                                            cv2.CHAIN_APPROX_SIMPLE)

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
    Can only be called when _getContour has been called with frame first.
    Extracts largest contour (assumed to be hand due to filtering) as well as moments
    and derived "center" of contour, and finds minimum enclosing circle and associated radius
    """
    def _extractHand(self):
        # only starts if provided contours are nonempty
        if self.contours:
            # finds largest contour in provided contours
            index = self._getIndexOfMaxContour(self.contours)
            cnt = self.contours[index]
            if self.hierarchy is not None:
                self.closedcontour = False if self.hierarchy[0][index][2] < 0 else True
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
    def getMainContour(self, frame):
        self._getContour(frame)
        self._extractHand()
        return self.main_contour

    """
    getCenterXYRadius
    provides X/Y-Coordinates and Radius of calculated "Center" of contour
    """
    def getCenterXYRadius(self, frame):
        self._getContour(frame)
        self._extractHand()
        return self.center[0], self.center[1], self.radius

    """
    getPts
    provides positional data of hand in deque
    """
    def getPts(self, frame):
        self._getContour(frame)
        self._extractHand()
        return self.pts