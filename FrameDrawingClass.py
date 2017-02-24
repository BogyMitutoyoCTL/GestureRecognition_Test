from collections import deque
import cv2
import numpy as np

class FrameDrawing():

    def drawCircles(self, frame, x, y, radius = 0):
        cv2.circle(frame, (x, y), 5, [0, 0, 255], 2)
        cv2.circle(frame, (x, y), int(radius), (0, 255, 255), 2)
        return frame

    def drawContours(self, frame, main_contour):
        drawing = np.zeros(frame.shape, np.uint8)
        cv2.drawContours(drawing, [main_contour], 0, (0, 255, 0), 2)
        return drawing
