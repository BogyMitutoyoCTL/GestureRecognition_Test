from tkinter import *
from collections import deque
import cv2
import numpy as np
import colorsys
from numpy import interp
from FilterClass import *
from ColorRangePickerClass import *
from EventClass import *
from HandRecognitionClass import *
from GestureRecognitionClass import *
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
    global mainWindowRefresh
    cts = filter.getContours(frame)
    frame2, _ = hand.getFrameDrawing(cts, frame)
    pts = hand.getPts(cts, frame)
    direction = gesture.trackMovement(pts)

    cv2.putText(frame2, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                0.65, (0, 0, 255), 3)


    img = Image.fromarray(cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB))
    imgtk = ImageTk.PhotoImage(image=img)
    imageContainer.imgtk = imgtk
    imageContainer.configure(image=imgtk)
    mainWindowRefresh = imageContainer.after(10, show_frame)

def mapHSVTO255(HSVColor):
    H = int(interp(HSVColor[0], [1, 360], [0, 179]))
    S = int(interp(HSVColor[1], [1, 100], [0, 255]))
    V = int(interp(HSVColor[2], [1, 100], [0, 255]))
    return [H, S, V]

lowerHSV = [95, 25, 30]
upperHSV = [151, 100, 100]

cap = cv2.VideoCapture(0)
filter = Filter(mapHSVTO255(lowerHSV), mapHSVTO255(upperHSV))
root = Tk()
hand = HandRecognizer()
gesture = GestureRecognizer()
colorChangedEvent = Event()
imageContainer = Label(root)
b = Button(root, text="set color range", command=button_change_color_range)

mainWindowRefresh = None
root.bind('<Escape>', lambda e: root.quit())
colorChangedEvent.append(OnColorChanged)
b.pack()
imageContainer.pack()
show_frame()
root.mainloop()
