from tkinter import *
import colorsys
from numpy import interp
import cv2
import numpy as np
from PIL import Image, ImageTk


class ColorRangePicker():
    def __init__(self, cap, colorChangedEvent):
        self.root = Toplevel()
        self.cap = cap
        self.colorChangedEvent = colorChangedEvent
        self.updateUI = None
        self.lowerHSV = [69, 16, 27]
        self.upperHSV = [163, 78, 100]

        self.init_UI()
        self.show_values()

    def apply_changes(self):
        if self.updateUI is not None:
            self.imageLabel.after_cancel(self.updateUI)
            self.root.destroy()
            self.colorChangedEvent(self.lowerHSV, self.upperHSV)

    def init_UI(self):
        Label(self.root, text="Lower HSV Color", font=("Helvetica", 16)).grid(row=0, column=0, padx=5)
        Label(self.root, text="Upper HSV Color", font=("Helvetica", 16)).grid(row=5, column=0, padx=5)

        self.w1 = Scale(self.root, from_=1, to=360, width=30, length=200, orient=HORIZONTAL)
        self.w1.set(95)
        self.w1.grid(row=1, column=0, padx=20, sticky=S)

        self.w2 = Scale(self.root, from_=1, to=100, width=30, length=200, orient=HORIZONTAL)
        self.w2.set(25)
        self.w2.grid(row=2, column=0, padx=20)

        self.w3 = Scale(self.root, from_=1, to=100, width=30, length=200, orient=HORIZONTAL)
        self.w3.set(30)
        self.w3.grid(row=3, column=0, padx=20, sticky=N)

        self.lowerColorCanvas = Canvas(self.root, width=200)
        self.lowerColorCanvas.grid(row=1, column=1, rowspan=3)
        self.upperColorCanvas = Canvas(self.root, width=200)
        self.upperColorCanvas.grid(row=6, column=1, rowspan=3)

        self.w4 = Scale(self.root, from_=1, to=360, width=30, length=200, orient=HORIZONTAL)
        self.w4.set(151)
        self.w4.grid(row=6, column=0, padx=20, sticky=S)

        self.w5 = Scale(self.root, from_=1, to=100, width=30, length=200, orient=HORIZONTAL)
        self.w5.set(100)
        self.w5.grid(row=7, column=0, padx=20)

        self.w6 = Scale(self.root, from_=1, to=100, width=30, length=200, orient=HORIZONTAL)
        self.w6.set(100)
        self.w6.grid(row=8, column=0, padx=20, sticky=N)

        self.b = Button(self.root, text="apply new range", command=apply, width=150, height=1)
        self.b.grid(row=9, column=0, columnspan=3, pady=10)
        self.imageLabel = Label(self.root)
        self.imageLabel.grid(row=0, column=2, rowspan=10, padx=10)

    def drawRect(self, color, canvas):
        r = int(color[0])
        g = int(color[1])
        b = int(color[2])
        colorString = '#%02x%02x%02x' % (r, g, b)
        canvas.create_rectangle(0, 52, 200, 233, fill=colorString, outline='white')

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
        self.drawRect(rgbLowerLimit, self.lowerColorCanvas)
        self.drawRect(rgbUpperLimit, self.upperColorCanvas)

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        low_neon_green = np.array(self.getLowerHsv())  # von 360 deg
        high_neon_green = np.array(self.getUpperHsv())
        neon_green_mask = cv2.inRange(hsv_frame, low_neon_green, high_neon_green)

        img = Image.fromarray(neon_green_mask)
        imgtk = ImageTk.PhotoImage(image=img)
        self.imageLabel.imgtk = imgtk
        self.imageLabel.configure(image=imgtk)

        self.updateUI = self.imageLabel.after(10, self.show_values)


    def getUpperHsv(self):
        upperh = int(interp(self.upperHSV[0], [1, 360], [0, 179]))
        uppers = int(interp(self.upperHSV[1], [1, 100], [0, 255]))
        upperv = int(interp(self.upperHSV[2], [1, 100], [0, 255]))
        return [upperh, uppers, upperv]
