from tkinter import *

import time
import cv2
from PIL import Image, ImageTk

from ColorRangePickerClass import ColorRangePicker
from EventClass import Event
from FrameDrawingClass import FrameDrawing
from GestureRecognitionClass import GestureRecognizer
from HandRecognitionClass import HandRecognizer


class Controller():
    def __init__(self):
        self.colorChangedEvent = Event()
        self.colorChangedEvent.append(self.onColorChanged)
        self.mainWindowRefresh = None
        self.capture = cv2.VideoCapture(0)
        self.HandRecognizer = HandRecognizer()
        self.GestureRecognizer = GestureRecognizer()
        self.FrameDrawing = FrameDrawing()

        # UI-Elements:
        self.tkinterWindow = None
        self.colorPickerButton = None
        self.imageContainer = None

        self.initUI()

    def initUI(self):
        self.tkinterWindow = Tk()
        self.tkinterWindow.bind('<Escape>', lambda e: self.tkinterWindow.quit())

        self.colorPickerButton = Button(self.tkinterWindow, text="set color range", command=self.button_changeColorRange)
        self.colorPickerButton.pack()
        self.imageContainer = Label(self.tkinterWindow)
        self.imageContainer.pack()

    def displayFrame(self, frame):
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        imgTk = ImageTk.PhotoImage(image=img)
        self.imageContainer.imgtk = imgTk
        self.imageContainer.configure(image=imgTk)

    def routine(self):
        _, frame = self.capture.read()

        hand = self.HandRecognizer.getHand(frame)
        if hand is not None:
            self.FrameDrawing.drawHand(frame, hand)
            self.GestureRecognizer.addHandToGestureBuffer(hand)
            gesture = self.GestureRecognizer.getGesture()
            if gesture is not None and gesture.startpoint is not None and gesture.endpoint is not None:
                self.FrameDrawing.drawGesture(frame, gesture)
        else:
            self.FrameDrawing.putText(frame, "No hand detected")

        self.displayFrame(frame)
        self.mainWindowRefresh = self.imageContainer.after(10, self.routine)

        print(time.time())

    def button_changeColorRange(self):
        ColorRangePicker(self.capture, self.colorChangedEvent)
        if self.mainWindowRefresh is not None:
            self.imageContainer.after_cancel(self.mainWindowRefresh)

    def onColorChanged(self, lowerColor, upperColor):
        self.HandRecognizer.filter.setColor(lowerColor, upperColor)
        self.routine()

if __name__ == "__main__":
    controller = Controller()
    controller.routine()
    controller.tkinterWindow.mainloop()
