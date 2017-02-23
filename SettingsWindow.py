from tkinter import *
import colorsys
from numpy import interp
import cv2
import numpy as np

class MyWindow():
    def __init__(self, root, cap):
        self.root = root
        self.cap = cap
        self.canvas = None
        self.updateUI = None
        self.w1 = None
        self.w2 = None
        self.w3 = None
        self.w4 = None
        self.w5 = None
        self.w6 = None
        self.b = None

        self.lowerHSV = [69, 16, 27]
        self.upperHSV = [163, 78, 100]

    def initUI(self):
        self.canvas = Canvas(self.root)
        self.canvas.pack()

        self.w1 = Scale(self.root, length=300, from_=1, to=360, orient=HORIZONTAL)
        self.w2 = Scale(self.root, from_=1, to=100, orient=HORIZONTAL)
        self.w3 = Scale(self.root, from_=1, to=100, orient=HORIZONTAL)
        self.w4 = Scale(self.root, length=300, from_=1, to=360, orient=HORIZONTAL)
        self.w5 = Scale(self.root, from_=1, to=100, orient=HORIZONTAL)
        self.w6 = Scale(self.root, from_=1, to=100, orient=HORIZONTAL)

        self.w1.set(69)
        self.w2.set(16)
        self.w3.set(27)
        self.w4.set(163)
        self.w5.set(78)
        self.w6.set(100)

        self.w1.pack()
        self.w2.pack()
        self.w3.pack()
        self.w4.pack()
        self.w5.pack()
        self.w6.pack()

        def cancel():
            if self.updateUI is not None:
                self.canvas.after_cancel(self.updateUI)
                self.updateUI = None
                self.root.destroy()
                self.canvas = None
                self.updateUI = None
                self.w1 = None
                self.w2 = None
                self.w3 = None
                self.w4 = None
                self.w5 = None
                self.w6 = None
                self.b = None
                cv2.destroyWindow('range')

        self.b = Button(self.root, text="apply", command=cancel)
        self.b.pack()
        self.show_values()


    def drawRect(self, color, UpperLeftPoint, LowerRightPoint):
        r = int(color[0])
        g = int(color[1])
        b = int(color[2])
        colorString = '#%02x%02x%02x' % (r, g, b)
        self.canvas.create_rectangle(UpperLeftPoint[0], UpperLeftPoint[1], LowerRightPoint[0], LowerRightPoint[1], fill=colorString)

    def loop(self):
        print("hallo")

    def hsv2rgb(self, h, s, v):
        return tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))

    def show_values(self):
        _, frame = self.cap.read()
        self.lowerHSV = [int(self.w1.get()), int(self.w2.get()), int(self.w3.get())]
        self.upperHSV = [int(self.w4.get()), int(self.w5.get()), int(self.w6.get())]
        upperh = self.upperHSV[0] / 360.0
        uppers = self.upperHSV[1] / 100.0
        upperv = self.upperHSV[2] / 100.0

        lowerh = self.lowerHSV[0] / 360.0
        lowers = self.lowerHSV[1] / 100.0
        lowerv = self.lowerHSV[2] / 100.0

        rgbUpperLimit = self.hsv2rgb(upperh, uppers, upperv)
        rgbLowerLimit = self.hsv2rgb(lowerh, lowers, lowerv)
        self.drawRect(rgbLowerLimit, [0, 0], [200, 200])
        self.drawRect(rgbUpperLimit, [200, 0], [400, 200])

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        low_neon_green = np.array(self.getLowerHsv())  # von 360 deg
        high_neon_green = np.array(self.getUpperHsv())
        neon_green_mask = cv2.inRange(hsv_frame, low_neon_green, high_neon_green)

        cv2.imshow('range', neon_green_mask)
        self.updateUI = self.canvas.after(10, self.show_values)

    def getLowerHsv(self):
        lowerh = int(interp(self.lowerHSV[0], [1, 360], [0, 179]))
        lowers = int(interp(self.lowerHSV[1], [1, 100], [0, 255]))
        lowerv = int(interp(self.lowerHSV[2], [1, 100], [0, 255]))
        return [lowerh, lowers, lowerv]

    def getUpperHsv(self):
        upperh = int(interp(self.upperHSV[0], [1, 360], [0, 179]))
        uppers = int(interp(self.upperHSV[1], [1, 100], [0, 255]))
        upperv = int(interp(self.upperHSV[2], [1, 100], [0, 255]))
        return [upperh, uppers, upperv]