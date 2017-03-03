import cv2
import numpy as np

"""
FrameDrawing Class
Draws enclosing circles around hand contours, based on calculated center x-y-coords and radius.
Also provides provisions for drawing contours on separate frame/array
"""


class FrameDrawing:
    """
    drawCircles:
    Draws center circle and minimum enclosing circle on provided frame.
    Bases drawing on provided coords and radius
    """

    def drawCircles(self, frame, x, y, radius=0):
        if x is not None and y is not None and radius is not None:
            cv2.circle(frame, (x, y), 5, [0, 0, 255], 2)
            cv2.circle(frame, (x, y), int(radius), (0, 255, 255), 2)

    """
    drawContours
    Traces detected contour on black background.
    Needs contour and frame (to determine size of picture)#
    TODO: Maybe remove frame param or have it drawn on actual frame
    """

    def drawContours(self, frame, main_contour):
        cv2.drawContours(frame, [main_contour], 0, (0, 255, 0), 2)

    def putText(self, frame, text, line=0):
        red = (0, 0, 255)
        origin = (10, 30 + line * 15)
        fontscale = 0.65
        thickness = 2
        cv2.putText(frame, text, origin, cv2.FONT_HERSHEY_SIMPLEX,
                    fontscale, red, thickness)

    def drawLine(self, frame, startpoint, endpoint):
        green = (0, 255, 0)
        cv2.line(frame, startpoint, endpoint, green, 2)

    def drawHand(self, frame, hand):
        self.drawCircles(frame, hand.center[0], hand.center[1], hand.radius)
        self.drawContours(frame, hand.contour)

    def drawGesture(self, frame, gesture):
        self.putText(frame, gesture.status)
        self.drawLine(frame, gesture.startpoint, gesture.endpoint)


if __name__ == "__main__":
    print("Nothing to run here. Please run ControllerClass.")
