import cv2
import numpy as np

"""
FrameDrawing Class
Draws enclosing circles around hand contours, based on calculated center x-y-coords and radius.
Also provides provisions for drawing contours on separate frame/array
"""


class FrameDrawing():
    """
    drawCircles:
    Draws center circle and minimum enclosing circle on provided frame.
    Bases drawing on provided coords and radius
    """

    def drawCircles(self, frame, x, y, radius=0):
        cv2.circle(frame, (x, y), 5, [0, 0, 255], 2)
        cv2.circle(frame, (x, y), int(radius), (0, 255, 255), 2)
        return frame

    """
    drawContours
    Traces detected contour on black background.
    Needs contour and frame (to determine size of picture)#
    TODO: Maybe remove frame param or have it drawn on actual frame
    """

    def drawContours(self, frame, main_contour):
        drawing = np.zeros(frame.shape, np.uint8)
        cv2.drawContours(drawing, [main_contour], 0, (0, 255, 0), 2)
        return drawing

    def putText(self, frame, text):
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    0.65, (0, 0, 255), 3)
        return frame

    def drawLine(self, frame, startpoint, endpoint):
        cv2.line(frame, startpoint, endpoint, (0, 255, 0), 2)

    def drawHand(self, frame, hand):
        self.drawCircles(frame, hand.center[0], hand.center[1], hand.radius)
        self.drawContours(frame, hand.contour)

    def drawGesture(self, frame, gesture):
        self.putText(frame, gesture.status)
        self.drawLine(frame,gesture.startpoint, gesture.endpoint)
