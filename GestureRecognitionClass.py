from collections import deque
import cv2
import numpy as np


class GestureRecognizer():
    def __init__(self):
        self.counter = 0
        (self.dX, self.dY) = (0, 0)
        self.direction = ""

    def trackMovement(self, pts):
        self.pts = pts

        for i in np.arange(1, len(self.pts)):
            if self.pts[i] is None:
                continue
            if self.counter >= 10 and i == 1 and self.pts[-10] is not None:

                dX = self.pts[-10][0] - self.pts[i][0]
                dY = self.pts[-10][1] - self.pts[i][1]
                (dirX, dirY) = ("", "")

                # ensure there is significant movement in the
                # x-direction
                if np.abs(dX) > 20:
                    dirX = "East" if np.sign(dX) == 1 else "West"

                # ensure there is significant movement in the
                # y-direction
                if np.abs(dY) > 20:
                    dirY = "North" if np.sign(dY) == 1 else "South"

                # handle when both directions are non-empty
                if dirX != "" and dirY != "":
                    self.direction = "{}-{}".format(dirY, dirX)

                # otherwise, only one direction is non-empty
                else:
                    self.direction = dirX if dirX != "" else dirY
        self.counter += 1
        return self.direction
