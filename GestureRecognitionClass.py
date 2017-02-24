from collections import deque
import cv2
import numpy as np


class GestureRecognizer():
    def __init__(self, maxlen):
        self.counter = 0
        (self.dX, self.dY) = (0, 0)
        self.direction = ""
        self.pts = None


    def trackMovement(self, pts):
        self.pts = pts

        for i in np.arange(1, len(self.pts)):
            if self.pts[i] and self.pts[-10] is None:
                continue
            else:
                dX = self.pts[-10][0] - self.pts[i][0]
                dY = self.pts[-10][1] - self.pts[i][1]
                (dirX, dirY) = ("", "")

<<<<<<< HEAD
                # ensure there is significant movement in the
                # x-direction
                if np.abs(dX) > 30:
                    dirX = "East" if np.sign(dX) == 1 else "West"

                # ensure there is significant movement in the
                # y-direction
                if np.abs(dY) > 30:
                    dirY = "North" if np.sign(dY) == 1 else "South"

                # handle when both directions are non-empty
                if dirX != "" and dirY != "":
                    self.direction = "{}-{}".format(dirY, dirX)

                # otherwise, only one direction is non-empty
=======
                if np.abs(dX) > np.abs(dY) and np.abs(dX) > 20:
                    dirX = "East" if np.sign(dX) == 1 else "West"
                elif np.abs(dX) < np.abs(dY) and np.abs(dY) > 20:
                    dirY = "South" if np.sign(dY) == 1 else "North"
>>>>>>> origin/master
                else:
                    self.direction = dirX if dirX != "" else dirY

                self.direction = dirX if dirX != "" else dirY
        return self.direction


"""
                else:
                    thickness = int(np.sqrt(bufferSize / float(i + 1)) * 2.5)
                    cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

        cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    0.65, (0, 0, 255), 3)
        cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.35, (0, 0, 255), 1)
"""