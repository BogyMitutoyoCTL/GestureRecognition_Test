import cv2
import numpy as np

"""
Filter Class
Provides methods to filter and smooth picture of neon gloved hand.
Filtering steps are split into fitting methods.
These methods could have added params to fine tune filtering steps.
"""
class Filter():
    """
    Constructor
    Constructor takes arguments for lower and upper value of color to filter.
    Also sets initial color range, which can be changed later via setColor()-Method
    """
    def __init__(self, lower_hsv=[95, 63, 77], upper_hsv=[151, 255, 255]):        #capture wird im Konstruktor übergeben
        self.hsv_frame = None
        self.lower_hsv = lower_hsv
        self.upper_hsv = upper_hsv
        self.setColor(self.lower_hsv, self.upper_hsv)
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
        med_blur_frame = cv2.medianBlur(self.neon_masked_frame, 15)  # Blur resulting masked Frame
        _, blur_frame_thresh = cv2.threshold(med_blur_frame, 0, 255, cv2.THRESH_BINARY)
        self.blur_frame_thresh = cv2.cvtColor(blur_frame_thresh, cv2.COLOR_BGR2GRAY)

    """
    _extractContours
    Uses Canny Edge Detection to extract edges from thresholded image.
    Canny-filtered picture is fed into cv2.findContours() to get a hierarchical list of detected contours
    """
    def _extractContours(self):
        self.neon_green_edges = cv2.Canny(self.blur_frame_thresh, 100, 200)  # Extract edges (should only be hand)
        _, self.contours, self.hierarchy = cv2.findContours(self.neon_green_edges, cv2.RETR_CCOMP,
                                               cv2.CHAIN_APPROX_SIMPLE)



    """
    _cvtToHSV
    Converts the frame from BGR spectrum to HSV
    """
    def _cvtToHSV(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    """
    getContours
    When provided with a frame, filters Frame and extracts and returns contours.
    """
    def getContours(self, frame):
        self.hsv_frame = self._cvtToHSV(frame)
        self._maskFrame()
        self._reduceNoise()
        self._extractContours()
        return self.contours , self.hierarchy

    """
    getMask
    When provided with a frame, only masks frame and returns it.
    """
    def getMask(self, frame):
        self.hsv_frame = self._cvtToHSV(frame)
        self._maskFrame()
        return self.neon_masked_frame
