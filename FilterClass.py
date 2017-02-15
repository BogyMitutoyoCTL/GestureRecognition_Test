import cv2
import numpy as np
import time
"""
Filter Class
Provides methods to filter and smooth picture of neon gloved hand.
Filtering steps are split into fitting methods.
These methods could have added params to fine tune filtering steps.
"""


class Filter:
    """
    Constructor
    Constructor takes arguments for lower and upper value of color to filter.
    Also sets initial color range, which can be changed later via setColor()-Method
    """
    def __init__(self, lower_hsv=[46, 61, 36], upper_hsv=[74, 255, 255]):        #capture wird im Konstruktor übergeben
        self.hsv_frame = None
        self.low_neon_green = lower_hsv
        self.high_neon_green = upper_hsv
        self.setColor(self.low_neon_green, self.high_neon_green)
        self.hierarchy = None

    """
    setColor
    Used to set color range to filter from frame.
    Called when class is constructed.
    """
    def setColor(self, lower_hsv, upper_hsv):
        self.low_neon_green = np.array(lower_hsv)  # von 360 deg
        self.high_neon_green = np.array(upper_hsv)

    """
    getColor
    Used to get current color range.
    """
    def getColor(self):
        return self.low_neon_green, self.high_neon_green

    """
    _maskFrame
    Applies range of color to filter to frame as mask,
    erodes and dilates filtered frame to make it more even
    """
    def _maskFrame(self):
        neon_green_mask = cv2.inRange(self.hsv_frame, self.low_neon_green, self.high_neon_green)
        neon_green_mask = cv2.erode(neon_green_mask, None, iterations=2)  # maske verfeinern
        neon_green_mask = cv2.dilate(neon_green_mask, None, iterations=2)
        self.neon_masked_frame = cv2.bitwise_and(self.hsv_frame, self.hsv_frame, mask=neon_green_mask)  # neongrüne Bereiche werden gefiltert

    """
    _reduceNoise
    Blurs frame and thresholds it with values to reduce back- and foreground noise
    """
    def _reduceNoise(self):
        reftim = time.clock()
        med_blur_frame = cv2.medianBlur(self.neon_masked_frame, 15)  # Blur resulting masked Frame
        time1 = time.clock()
        _, blur_frame_thresh = cv2.threshold(med_blur_frame, 0, 255, cv2.THRESH_BINARY)
        time2 = time.clock()
        self.blur_frame_thresh = cv2.cvtColor(blur_frame_thresh, cv2.COLOR_BGR2GRAY)
        time3 = time.clock()
        print("blur: " + str(time1 - reftim))
        print("threshold: " + str(time2 - time1))
        print("cvt: " + str(time3 - time2))


    """
    _extractEdges
    Uses Canny Edge Detection to extract edges from thresholded image.
    """
    def _extractEdges(self):
        self.neon_green_edges = cv2.Canny(self.blur_frame_thresh, 100, 200)  # Extract edges (should only be hand)


    """
    _cvtToHSV
    Converts the frame from BGR spectrum to HSV
    """
    def _cvtToHSV(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    """
    getEdges
    When provided with a frame, filters Frame and extracts and returns edges.
    """
    def getEdges(self, frame):
        refTime = time.clock()
        self.hsv_frame = self._cvtToHSV(frame)
        tim1 = time.clock()
        self._maskFrame()
        tim2 = time.clock()
        self._reduceNoise()
        tim3 = time.clock()
        self._extractEdges()
        tim4 = time.clock()
        print("cvttohsv:" + str(tim1-refTime))
        print("mask:" + str(tim2-tim1))
        print("reduce:" + str(tim3-tim2))
        print("edges:" + str(tim4-tim3))
        return self.neon_green_edges

    """
    getMask
    When provided with a frame, only masks frame and returns it.
    """
    def getMask(self, frame):
        self.hsv_frame = self._cvtToHSV(frame)
        self._maskFrame()
        return self.neon_masked_frame


if __name__ == "__main__":
    print("Nothing to run here. Please run ControllerClass.")
