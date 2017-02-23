import cv2

class Capture():
    def __init__(self, source = 0):
        self.cap = cv2.VideoCapture(source)

    def getFrame(self):
        _, frame = self.cap.read()
        return frame

    def getHSVFrame(self):
        hsv_frame = cv2.cvtColor(self.getFrame(), cv2.COLOR_BGR2HSV)
        return hsv_frame