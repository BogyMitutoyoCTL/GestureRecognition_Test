from collections import deque
import cv2
import numpy as np

class HandRecognizer():
    def __init__(self, contours, frame):
        self.contours = contours
        self.frame = frame
        self.drawing = np.zeros(self.frame.shape, np.uint8)
        self.max_area = 0

    def extractHand(self):
        if self.contours:
            for i in range(len(self.contours)):
                cnt = self.contours[i]
                area = cv2.contourArea(cnt)
                if (area > self.max_area):
                    self.max_area = area
                    ci = i
            cnt = self.contours[ci]
            hull = cv2.convexHull(cnt)

            moments = cv2.moments(cnt)
            if moments['m00'] != 0:
                cx = int(moments['m10'] / moments['m00'])  # cx = M10/M00
                cy = int(moments['m01'] / moments['m00'])  # cy = M01/M00

            self.center = (cx, cy)

            cv2.circle(self.frame, self.center, 5, [0, 0, 255], 2)
            cv2.drawContours(self.drawing, [cnt], 0, (0, 255, 0), 2)
            cv2.drawContours(self.drawing, [hull], 0, (0, 0, 255), 2)
            cv2.putText(self.frame, str(self.max_area), (10, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 255, 155), 2, cv2.LINE_AA)

            cnt = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            self.hull = cv2.convexHull(cnt, returnPoints=False)
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