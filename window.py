from tkinter import *
from collections import deque
import cv2
import numpy as np
import colorsys
from numpy import interp
from FilterClass import *
from ColorRangePickerClass import *
from gestures import *
from EventClass import *
from PIL import Image, ImageTk
from CaptureClass import *


def button_change_color_range():
    ColorRangePicker(cap,colorChangedEvent)

def OnColorChanged(lowerColor, upperColor):
    global lowerHSV, upperHSV
    lowerHSV = lowerColor
    upperHSV = upperColor

def show_frame():
    mask = filter.getMask(cap.getHSVFrame())
    img = Image.fromarray(mask)
    imgtk = ImageTk.PhotoImage(image=img)
    imageContainer.imgtk = imgtk
    imageContainer.configure(image=imgtk)
    imageContainer.after(10, show_frame)

def mapHSVTO255(HSVColor):
    H = int(interp(HSVColor[0], [1, 360], [0, 179]))
    S = int(interp(HSVColor[1], [1, 100], [0, 255]))
    V = int(interp(HSVColor[2], [1, 100], [0, 255]))
    return [H, S, V]

cap = Capture()

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
#show_frame()


#hand = HandRecognizer()

root.mainloop()
