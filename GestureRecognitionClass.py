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
        self.pts = None

    """
    points: Array with center of mass points for the last few frames
    this function interpolates the points to a line and returns the starting and the end point
    """
    def getInterpolatedLine(self, points):
        x = []
        y = []
        if len(points) < 10:
            return None, None
        for i in np.arange(0, 10):
            if points[i] is not None:
                x += [points[i][0]]
                y += [points[i][1]]
            else:
                return None, None

        m, b = np.polyfit(x, y, 1)
        maxX = max(x)
        minX = min(x)

        ptStart = (int(minX), int(m * minX + b))
        ptEnd = (int(maxX), int(m * maxX + b))

        self.dX = (ptStart[0] - ptEnd[0]) * np.sign(x[0] - x[9])
        self.dY =(ptStart[1] - ptEnd[1]) * np.sign(y[0] - y[9])
        return ptStart, ptEnd

    def getDirection(self):
        if np.abs(self.dX) > np.abs(self.dY) and np.abs(self.dX) > 20:
            self.direction = "Right" if np.sign(self.dX) == 1 else "Left"
        elif np.abs(self.dX) < np.abs(self.dY) and np.abs(self.dY) > 20:
            self.direction = "Up" if np.sign(self.dY) == 1 else "Down"
        else:
            self.direction = ""

        return self.direction
