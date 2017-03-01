from collections import deque
import cv2
import numpy as np

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

        for i in np.arange(0, 10):
            x1 = self.handBuffer[i].center[0]
            y1 = self.handBuffer[i].center[1]
            if x1 is None or y1 is None:
                return None, None
            x += [x1]
            y += [y1]


        m, b = np.polyfit(x, y, 1)
        maxX = max(x)
        minX = min(x)

        ptStart = (int(minX), int(m * minX + b))
        ptEnd = (int(maxX), int(m * maxX + b))

        self.dX = (ptStart[0] - ptEnd[0]) * np.sign(x[0] - x[9])
        self.dY = np.abs((ptStart[1] - ptEnd[1])) * np.sign(y[9] - y[0]) 
        return ptStart, ptEnd

    def getDirection(self):
        if np.abs(self.dX) > np.abs(self.dY) and np.abs(self.dX) > 20:
            self.direction = "Right" if np.sign(self.dX) == 1 else "Left"
        elif np.abs(self.dX) < np.abs(self.dY) and np.abs(self.dY) > 20:
            self.direction = "Up" if np.sign(self.dY) == 1 else "Down"
        else:
            self.direction = ""

        return self.direction

    #def getSize(self):


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
