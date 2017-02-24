from collections import deque
import cv2

class HandRecognizer():
    def __init__(self, buffersize = 20):
        self.contours = None
        self.radius = 0
        self.center = 0,0
        self.max_area = 0
        self.pts = deque(maxlen = buffersize)

    def _extractHand(self):
        if self.contours:
            cnt = max(self.contours, key=cv2.contourArea)
            ((x, y), self.radius) = cv2.minEnclosingCircle(cnt)

            M = cv2.moments(cnt)
            if M["m00"] != 0:
                self.center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                if self.radius > 10:
                    self.pts.appendleft(self.center)
                    cnt = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            self.main_contour = cnt

    def getMainContour(self, contours):
        self.contours = contours
        self._extractHand()
        return self.main_contour

    def getCenterXYRadius(self, contours):
        self.contours = contours
        self._extractHand()
        return self.center[0], self.center[1], self.radius

    def getPts(self, contours):
        self.contours = contours
        self._extractHand()
        return self.pts