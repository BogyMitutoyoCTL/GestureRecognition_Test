from collections import deque
import cv2
import numpy as np

class HandRecognizer():
    def __init__(self, contours, frame, buffersize = 20):
        self.contours = contours
        self.frame = frame
        self.drawing = np.zeros(self.frame.shape, np.uint8)
        self.max_area = 0
        self.pts = deque(maxlen = buffersize)

    def extractHand(self):
        if self.contours:
            cnt = max(self.contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(cnt)

            M = cv2.moments(cnt)
            if M["m00"] != 0:
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                if radius > 10:
                    cv2.circle(self.frame, self.center, 5, [0, 0, 255], 2)
                    cv2.circle(self.frame, self.center, int(radius), (0, 255, 255), 2)
                    self.pts.appendleft(center)
                    cnt = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
                    self.hull = cv2.convexHull(cnt)
                    #cv2.drawContours(self.drawing, [self.main_contour], 0, (0, 255, 0), 2)
                    cv2.drawContours(self.drawing, [self.hull], 0, (0, 0, 255), 2)

            self.main_contour = cnt

    def getMainContour(self):
        self.extractHand()
        return self.main_contour

    def getHull(self):
        self.extractHand()
        return self.hull

    def getFrameDrawing(self):
        self.extractHand()
        return self.frame, self.drawing

    def getPts(self):
        self.extractHand()
        return self.pts