from tkinter import *
from collections import deque
import cv2
import numpy as np
from numpy import interp
import colorsys


bufferSize = 20
pts = deque(maxlen=bufferSize)

class HandRecognizer:
    def __init__(self):
        self.counter = 0
        (self.dX, self.dY) = (0, 0)
        self.direction = ""

    def process_frame(self, frame):

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        low_neon_green = np.array([lowerh, lowers, lowerv])  # von 360 deg
        high_neon_green = np.array([upperh, uppers, upperv])
        neon_green_mask = cv2.inRange(hsv_frame, low_neon_green, high_neon_green)

        neon_green_mask = cv2.erode(neon_green_mask, None, iterations=2)  # maske verfeinern
        neon_green_mask = cv2.dilate(neon_green_mask, None, iterations=2)
        neon_masked_frame = cv2.bitwise_and(frame, frame,
                                            mask=neon_green_mask)  # neongrüne Bereiche werden gefiltert
        med_blur_frame = cv2.medianBlur(neon_masked_frame, 15)  # Blur resulting masked Frame
        _, blur_frame_thresh = cv2.threshold(med_blur_frame, 70, 255, cv2.THRESH_BINARY)
        blur_frame_thresh = cv2.cvtColor(blur_frame_thresh, cv2.COLOR_BGR2GRAY)
        neon_green_edges = cv2.Canny(blur_frame_thresh, 100, 200)  # Extract edges (should only be hand)
        _, contours, _ = cv2.findContours(neon_green_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        drawing = np.zeros(frame.shape, np.uint8)
        max_area = 0

        if contours:
            cnt = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(cnt)
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                if radius > 10:
                    # cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)
                    pts.appendleft(center)
                    cnt = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
                    hull = cv2.convexHull(cnt)
                    cv2.drawContours(frame, [hull], 0, (0, 255, 0), 2)

            for i in np.arange(1, len(pts)):
                if pts[i] is None:
                    continue
                if counter >= 10 and i == 1 and pts[-10] is not None:

                    dX = pts[-10][0] - pts[i][0]
                    dY = pts[-10][1] - pts[i][1]
                    (dirX, dirY) = ("", "")

                    # ensure there is significant moveme    nt in the
                    # x-direction
                    if np.abs(dX) > 20:
                        dirX = "East" if np.sign(dX) == 1 else "West"

                    # ensure there is significant movement in the
                    # y-direction
                    if np.abs(dY) > 20:
                        dirY = "North" if np.sign(dY) == 1 else "South"

                    # handle when both directions are non-empty
                    if dirX != "" and dirY != "":
                        direction = "{}-{}".format(dirY, dirX)

                    # otherwise, only one direction is non-empty
                    else:
                        direction = dirX if dirX != "" else dirY
                else:
                    thickness = int(np.sqrt(bufferSize / float(i + 1)) * 2.5)
                    cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

        cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    0.65, (0, 0, 255), 3)
        cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.35, (0, 0, 255), 1)
        counter += 1
        return frame