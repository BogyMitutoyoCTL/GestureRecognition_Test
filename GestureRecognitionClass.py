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

        self.dX = ptStart[0] - ptEnd[0]
        self.dY = ptStart[1] - ptEnd[1]
        return ptStart, ptEnd

    def getDirection(self):
        if np.abs(self.dX) > np.abs(self.dY) and np.abs(self.dX) > 30:
            self.direction = "East" if np.sign(self.dX) == 1 else "West"
        elif np.abs(self.dX) < np.abs(self.dY) and np.abs(self.dY) > 30:
            self.direction = "South" if np.sign(self.dY) == 1 else "North"
        else:
            self.direction = ""

        return self.direction

    def trackMovement(self, pts):
        self.pts = pts

        for i in np.arange(1, len(self.pts)):
            if self.pts[i] and self.pts[-10] is None:
                continue
            else:
                self.dX = self.pts[-10][0] - self.pts[i][0]
                self.dY = self.pts[-10][1] - self.pts[i][1]
                (dirX, dirY) = ("", "")
                # ensure there is significant movement in the
                # x-direction
                if np.abs(self.dX) > 30:
                    dirX = "East" if np.sign(self.dX) == 1 else "West"

                # ensure there is significant movement in the
                # y-direction
                if np.abs(self.dY) > 30:
                    dirY = "North" if np.sign(self.dY) == 1 else "South"

                # handle when both directions are non-empty
                if dirX != "" and dirY != "":
                    self.direction = "{}-{}".format(dirY, dirX)

                # otherwise, only one direction is non-empty
                if np.abs(self.dX) > np.abs(self.dY) and np.abs(self.dX) > 20:
                    dirX = "East" if np.sign(self.dX) == 1 else "West"
                elif np.abs(self.dX) < np.abs(self.dY) and np.abs(self.dY) > 20:
                    dirY = "South" if np.sign(self.dY) == 1 else "North"
                else:
                    self.direction = dirX if dirX != "" else dirY

                self.direction = dirX if dirX != "" else dirY
        return self.direction