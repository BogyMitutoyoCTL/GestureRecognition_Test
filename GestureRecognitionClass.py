from collections import deque
import cv2
import numpy as np
import sys

"""
GestureRecognizer Class
Provides functionality to analyze hand movements and recognize gestures
"""
class GestureRecognizer():
    """
    Constructor

    """
    def __init__(self):
        (self.dX, self.dY) = (0, 0)
        self.direction = ""
        self.handBuffer = deque(maxlen=20)

    """
    points: Array with center of mass points for the last few frames
    this function interpolates the points to a line and returns the starting and the end point
    """
    def getInterpolatedLine(self):
        x = []
        y = []

        first_item_timestamp = self.handBuffer[0].timestamp
        for i in np.arange(len(self.handBuffer)):
            x1 = self.handBuffer[i].center[0]
            y1 = self.handBuffer[i].center[1]
            if x1 is None or y1 is None:
                return None, None
            curtime = self.handBuffer[i].timestamp
            if curtime > first_item_timestamp + 1:
                print("gesture detected")
                break

            x += [x1]
            y += [y1]


        m, b = np.polyfit(x, y, 1)

        index_end, maxX = self._getIndexOfMaxPoint(x)
        index_start, minX = self._getIndexOfMinPoint(x)



        ptStart = (int(minX), int(m * minX + b))
        ptEnd = (int(maxX), int(m * maxX + b))

        self.dX = (ptStart[0] - ptEnd[0]) * np.sign(x[0] - x[9])
        self.dY = np.abs((ptStart[1] - ptEnd[1])) * np.sign(y[9] - y[0]) 
        return ptStart, ptEnd

    @staticmethod
    def _getIndexOfMaxPoint(pointlist):
        maxPoint, index = 0, 0
        for i in range(len(pointlist)):
            pt = pointlist[i]
            if pt > maxPoint:
                maxPoint = pt
                index = i
        return index, maxPoint

    @staticmethod
    def _getIndexOfMinPoint(pointlist):
        minPoint, index = sys.maxsize, 0
        for i in range(len(pointlist)):
            pt = pointlist[i]
            if pt < minPoint:
                minPoint = pt
                index = i
        return index, minPoint

    def getDirection(self):
        if np.abs(self.dX) > np.abs(self.dY) and np.abs(self.dX) > 20:
            self.direction = "Right" if np.sign(self.dX) == 1 else "Left"
        elif np.abs(self.dX) < np.abs(self.dY) and np.abs(self.dY) > 20:
            self.direction = "Up" if np.sign(self.dY) == 1 else "Down"
        else:
            self.direction = ""

        return self.direction

    def addHandToGestureBuffer(self, hand):
        if hand is not None:
            self.handBuffer.appendleft(hand)
        else:
            self.handBuffer.clear()



    def getGesture(self):
        if len(self.handBuffer) > 10:
            currentHand = self.handBuffer[0]
            if currentHand.isClosedContour:
                ptStart, ptEnd = self.getInterpolatedLine()
                direction = self.getDirection()
                return Gesture(direction, ptStart, ptEnd)
            else:
                return Gesture("Hand not fully detected", None, None)


class Gesture:
    def __init__(self, status, startpoint, endpoint):
        self.status = status
        self.startpoint = startpoint
        self.endpoint = endpoint


if __name__ == "__main__":
    print("Nothing to run here. Please run ControllerClass.")
