from tkinter import *
from collections import deque
import cv2
import numpy as np
import colorsys
from ColorRangePicker import ColorRangePicker
from gestures import HandRecognizer
from Event import Event


def button_change_color_range():
    ColorRangePicker(cap,colorChangedEvent)

def OnColorChanged(lowerColor, upperColor):
    global lowerHSV, upperHSV
    lowerHSV = lowerColor
    upperHSV = upperColor


cap = cv2.VideoCapture(0)
root = Tk()
root.bind('<Escape>', lambda e: root.quit())
root.geometry("700x700")
b = Button(root, text="set color range", command=button_change_color_range)
b.pack()

lowerHSV = [69, 16, 27]
upperHSV = [163, 78, 100]

colorChangedEvent = Event()
colorChangedEvent.append(OnColorChanged)

hand = HandRecognizer()
lmain = Label(root)
lmain.pack()
root.mainloop()
