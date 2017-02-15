from collections import deque
from FilterClass import *
import cv2
import sys
import numpy as np
import time

"""
HandRecognizer Class
Provides functions to extract hand contours, as well as positional data
from provided contour.
"""


class HandRecognizer:
    """
    Constructor
    :param buffersize
    Constructor initializes deque of size buffersize to track positional data for evaluation of
    hand movement. Initially, deque is filled with zeroes only
    """

    def __init__(self):
        self.filter = Filter()
    """
    _getContour
    Takes frame, applies filter and extracts Contours from filtered frame.
    """
    def _getContour(self, frame):
        edges = self.filter.getEdges(frame)
        _, contours, hierarchy = cv2.findContours(edges, cv2.RETR_CCOMP,
                                                  cv2.CHAIN_APPROX_SIMPLE)
        return contours, hierarchy

    @staticmethod
    def _getIndexOfMaxContour(contours):
        maxArea, index = 0, 0
        for i in range(len(contours)):
            area = cv2.contourArea(contours[i])
            if area > maxArea:
                maxArea = area
                index = i
        return index, maxArea

    @staticmethod
    def _isContourClosed(hierarchy, index):
        if hierarchy is not None:
            return False if hierarchy[0][index][2] < 0 else True
        else:
            return False

    @staticmethod
    def _getHandCenter(handContour):
        M = cv2.moments(handContour)
        (_, radius) = cv2.minEnclosingCircle(handContour)
        if M["m00"] != 0:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        else:
            center = (None, None)
        return center, radius

    @staticmethod
    def _getApproximation(maxContour):
        epsilon = 0.01 * cv2.arcLength(maxContour, True)
        handContour = cv2.approxPolyDP(maxContour,epsilon, True)
        return handContour;

    """
    _getHullAndDefects
    extracts convex hull and convexity defects
    NOT USED YET
    """
    @staticmethod
    def _getHullAndDefects(handContour):
        hullHandContour = cv2.convexHull(handContour, returnPoints=False)
        hullPoints = [handContour[i[0]] for i in hullHandContour]
        hullPoints = np.array(hullPoints, dtype=np.int32)
        defects = cv2.convexityDefects(handContour, hullHandContour)
        return hullPoints, defects

    """
    _extractHand
    Can only be called when _getContour has been called with frame first.
    Extracts largest contour (assumed to be hand due to filtering) as well as moments
    and derived "center" of contour, and finds minimum enclosing circle and associated radius
    """
    def _extractHand(self, contours, hierarchy):
        indexOfMaxContour, area = self._getIndexOfMaxContour(contours)
        contourClosed = self._isContourClosed(hierarchy, indexOfMaxContour)
        maxContour = contours[indexOfMaxContour]
        center, radius = self._getHandCenter(maxContour)
        handContour = self._getApproximation(maxContour)
        return Hand(radius, contourClosed, center, maxContour, area)

    def getHand(self, frame):
        contours, hierarchy = self._getContour(frame)
        if contours:
            return self._extractHand(contours, hierarchy)
        else:
            return None


class Hand:
    def __init__(self, radius, isClosedContour, center, contour, area):
        self.radius = radius
        self.isClosedContour = isClosedContour
        self.center = center
        self.contour = contour
        self.area = area


if __name__ == "__main__":
    print("Nothing to run here. Please run ControllerClass.")
