from tkinter import *
from collections import deque
import cv2
import numpy as np
import colorsys
from numpy import interp
from FilterClass import *
from ColorRangePickerClass import *
from EventClass import *
from PIL import Image, ImageTk


def button_change_color_range():
    ColorRangePicker(cap, colorChangedEvent)
    if mainWindowRefresh is not None:
        imageContainer.after_cancel(mainWindowRefresh)

def OnColorChanged(lowerColor, upperColor):
    global lowerHSV, upperHSV
    lowerHSV = lowerColor
    upperHSV = upperColor
    show_frame()

def show_frame():
    _, frame = cap.read()
    test = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    global mainWindowRefresh
    #contours = filter.getContours(frame)
    img = Image.fromarray(test)
    imgtk = ImageTk.PhotoImage(image=img)
    imageContainer.imgtk = imgtk
    imageContainer.configure(image=imgtk)
    mainWindowRefresh = imageContainer.after(10, show_frame)

def mapHSVTO255(HSVColor):
    H = int(interp(HSVColor[0], [1, 360], [0, 179]))
    S = int(interp(HSVColor[1], [1, 100], [0, 255]))
    V = int(interp(HSVColor[2], [1, 100], [0, 255]))
    return [H, S, V]

cap = cv2.VideoCapture(0)
mainWindowRefresh = None
root = Tk()
root.bind('<Escape>', lambda e: root.quit())
b = Button(root, text="set color range", command=button_change_color_range)
b.pack()

imageContainer = Label(root)
imageContainer.pack()
lowerHSV = [95, 25, 30]
upperHSV = [151, 100, 100]
colorChangedEvent = Event()
colorChangedEvent.append(OnColorChanged)

filter = Filter(mapHSVTO255(lowerHSV), mapHSVTO255(upperHSV))

show_frame()

root.mainloop()
