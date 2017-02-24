from tkinter import *
import cv2
import numpy as np
from PIL import Image, ImageTk
import Converter

"""
ColorRangePicker Class
TODO: COMMENT
"""
def drawRect(color, canvas):
    r = int(color[0])
    g = int(color[1])
    b = int(color[2])
    colorString = '#%02x%02x%02x' % (r, g, b)
    canvas.create_rectangle(0, 52, 200, 233, fill=colorString, outline='white')

class ColorRangePicker():
    def __init__(self, cap, colorChangedEvent):
        self.window = Toplevel()
        self.capture = cap
        self.colorChangedEvent = colorChangedEvent
        self.refreshUI = None
        self.lowerHSV = [69, 16, 27]
        self.upperHSV = [163, 78, 100]

        self.init_UI()
        self.startRoutine()

    def init_UI(self):
        Label(self.window, text="Lower HSV Color", font=("Helvetica", 16)).grid(row=0, column=0, padx=5)
        Label(self.window, text="Upper HSV Color", font=("Helvetica", 16)).grid(row=5, column=0, padx=5)

        self.w1 = Scale(self.window, from_=1, to=360, width=30, length=200, orient=HORIZONTAL)
        self.w1.set(95)
        self.w1.grid(row=1, column=0, padx=20, sticky=S)

        self.w2 = Scale(self.window, from_=1, to=100, width=30, length=200, orient=HORIZONTAL)
        self.w2.set(25)
        self.w2.grid(row=2, column=0, padx=20)

        self.w3 = Scale(self.window, from_=1, to=100, width=30, length=200, orient=HORIZONTAL)
        self.w3.set(30)
        self.w3.grid(row=3, column=0, padx=20, sticky=N)

        self.lowerColorCanvas = Canvas(self.window, width=200)
        self.lowerColorCanvas.grid(row=1, column=1, rowspan=3)
        self.upperColorCanvas = Canvas(self.window, width=200)
        self.upperColorCanvas.grid(row=6, column=1, rowspan=3)

        self.w4 = Scale(self.window, from_=1, to=360, width=30, length=200, orient=HORIZONTAL)
        self.w4.set(151)
        self.w4.grid(row=6, column=0, padx=20, sticky=S)

        self.w5 = Scale(self.window, from_=1, to=100, width=30, length=200, orient=HORIZONTAL)
        self.w5.set(100)
        self.w5.grid(row=7, column=0, padx=20)

        self.w6 = Scale(self.window, from_=1, to=100, width=30, length=200, orient=HORIZONTAL)
        self.w6.set(100)
        self.w6.grid(row=8, column=0, padx=20, sticky=N)

        self.b = Button(self.window, text="apply new range", command=self.button_apply, width=150, height=1)
        self.b.grid(row=9, column=0, columnspan=3, pady=10)
        self.imageLabel = Label(self.window)
        self.imageLabel.grid(row=0, column=2, rowspan=10, padx=10)

    def button_apply(self):
        if self.refreshUI is not None:
            self.imageLabel.after_cancel(self.refreshUI)
            self.window.destroy()
            self.colorChangedEvent(self.lowerHSV, self.upperHSV)

    def startRoutine(self):
        _, frame = self.capture.read()

        rgbLowerLimit, rgbUpperLimit = self._getRGBValuesFromScales()

        drawRect(rgbLowerLimit, self.lowerColorCanvas)
        drawRect(rgbUpperLimit, self.upperColorCanvas)

        neon_green_mask = self.getMask(frame)

        self.showFrameOnUI(neon_green_mask)

        self.refreshUI = self.imageLabel.after(10, self.startRoutine)

    def _getRGBValuesFromScales(self):
        self.lowerHSV = [int(self.w1.get()), int(self.w2.get()), int(self.w3.get())]
        self.upperHSV = [int(self.w4.get()), int(self.w5.get()), int(self.w6.get())]

        rgbUpperLimit = Converter.hsv2rgb(self.upperHSV[0], self.upperHSV[1], self.upperHSV[2])
        rgbLowerLimit = Converter.hsv2rgb(self.lowerHSV[0], self.lowerHSV[1], self.lowerHSV[2])

        return rgbLowerLimit, rgbUpperLimit

    def getMask(self, frame):
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        low_neon_green = np.array(Converter.mapHSVTO255(self.lowerHSV))  # von 360 deg
        high_neon_green = np.array(Converter.mapHSVTO255(self.upperHSV))
        neon_green_mask = cv2.inRange(hsv_frame, low_neon_green, high_neon_green)
        return neon_green_mask

    def showFrameOnUI(self, image):
        img = Image.fromarray(image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.imageLabel.imgtk = imgtk
        self.imageLabel.configure(image=imgtk)
