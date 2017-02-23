from collections import deque
from tkinter import *
import cv2
import imutils
import numpy as np




cap = cv2.VideoCapture(0)

pt_buffer = deque(maxlen = 64)

while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    low_neon_green = np.array([110, 140, 160])  # von 360 deg
    high_neon_green = np.array([150, 255, 255])

    neon_green_mask = cv2.inRange(hsv_frame, low_neon_green, high_neon_green) #alles was sich im neongrünen Farbbereich befindet

    neon_green_mask = cv2.erode(neon_green_mask, None, iterations=2) #maske verfeinern
    neon_green_mask = cv2.dilate(neon_green_mask, None, iterations=2)

    neon_masked_frame = cv2.bitwise_and(frame, frame, mask = neon_green_mask) #neongrüne Bereiche werden gefiltert

    med_blur_frame = cv2.medianBlur(neon_masked_frame, 15) #Blur resulting masked Frame

    _, blur_frame_thresh = cv2.threshold(med_blur_frame, 70, 255, cv2.THRESH_BINARY_INV)

    neon_green_edges = cv2.Canny(blur_frame_thresh, 100, 200) #Extract edges (should only be hand)

    _, contours, _ = cv2.findContours(neon_green_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    drawing = np.zeros(frame.shape, np.uint8)

    max_area = 0
    if contours:
        for i in range(len(contours)):
            cnt = contours[i]
            area = cv2.contourArea(cnt)
            if (area > max_area):
                max_area = area
                ci = i
        cnt = contours[ci]

        hull = cv2.convexHull(cnt)
        moments = cv2.moments(cnt)
        if moments['m00'] != 0:
            cx = int(moments['m10'] / moments['m00'])  # cx = M10/M00
            cy = int(moments['m01'] / moments['m00'])  # cy = M01/M00

        centr = (cx, cy)

        cv2.circle(frame, centr, 5, [0, 0, 255], 2)
        cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 2)
        cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 2)
        cv2.putText(frame, str(max_area), (10, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 255, 155), 2, cv2.LINE_AA)

        cnt = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        hull = cv2.convexHull(cnt, returnPoints=False)


    cv2.imshow('original', frame)
    cv2.imshow('output', drawing)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()