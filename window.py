from tkinter import *
from collections import deque
import cv2
import numpy as np
import colorsys
from FilterClass import *
from ColorRangePickerClass import *
from EventClass import *
from HandRecognitionClass import *
from FrameDrawingClass import *
from GestureRecognitionClass import *
from PIL import Image, ImageTk
import Converter


def button_change_color_range():
    ColorRangePicker(cap, colorChangedEvent)
    if mainWindowRefresh is not None:
        imageContainer.after_cancel(mainWindowRefresh)


def OnColorChanged(lowerColor, upperColor):
    global defaultLowerHSV, defaultUpperHSV
    defaultLowerHSV = lowerColor
    defaultUpperHSV = upperColor
    show_frame()


def show_frame():
    global mainWindowRefresh
    _, frame = cap.read()
    cts = filter.getContours(frame)
    x, y, radius = hand.getCenterXYRadius(cts)
    frame2 = draw.drawCircles(frame, x, y, radius)

    pts = hand.getPts(cts)
    direction = gesture.trackMovement(pts)

    cv2.putText(frame2, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                0.65, (0, 0, 255), 3)

    showFrameOnUI(frame2)
    mainWindowRefresh = imageContainer.after(10, show_frame)


def showFrameOnUI(frame):
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    imgtk = ImageTk.PhotoImage(image=img)
    imageContainer.imgtk = imgtk
    imageContainer.configure(image=imgtk)

defaultLowerHSV = [95, 25, 30]
defaultUpperHSV = [151, 100, 100]

cap = cv2.VideoCapture(0)

root = Tk()
root.bind('<Escape>', lambda e: root.quit())
b = Button(root, text="set color range", command=button_change_color_range)
b.pack()
imageContainer = Label(root)
imageContainer.pack()

filter = Filter(Converter.mapHSVTO255(defaultLowerHSV), Converter.mapHSVTO255(defaultUpperHSV))
hand = HandRecognizer()
gesture = GestureRecognizer(20)
draw = FrameDrawing()

colorChangedEvent = Event()
mainWindowRefresh = None
colorChangedEvent.append(OnColorChanged)

show_frame()

root.mainloop()
