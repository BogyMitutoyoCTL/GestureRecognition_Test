from tkinter import *
import tkinter
import time
import tkinter.messagebox as message
import cv2
import numpy
from PIL import Image, ImageTk

from ColorRangePickerClass import ColorRangePicker
from EventClass import Event
from FrameDrawingClass import FrameDrawing
from GestureRecognitionClass import GestureRecognizer
from HandRecognitionClass import HandRecognizer

LITTLE_COLOR = 10
default_camera = 0


class Controller:
    def __init__(self):
        self.colorChangedEvent = Event()
        self.colorChangedEvent.append(self.onColorChanged)
        self.mainWindowRefresh = None
        self.camera = cv2.VideoCapture(default_camera)
        self.HandRecognizer = HandRecognizer()
        self.GestureRecognizer = GestureRecognizer()
        self.FrameDrawing = FrameDrawing()
        # UI-Elements:
        self.window = None
        self.colorPickerButton = None
        self.imageContainer = None

        self.initUI()

    def initUI(self):
        self.window = Tk()
        self.window.bind('<Escape>', lambda e: self.window.quit())

        self.colorPickerButton = Button(self.window, text="set color range", command=self.button_changeColorRange)
        self.colorPickerButton.pack()
        self.imageContainer = Label(self.window)
        self.imageContainer.pack()

    def displayFrame(self, frame):
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        imgTk = ImageTk.PhotoImage(image=img)
        self.imageContainer.imgtk = imgTk
        self.imageContainer.configure(image=imgTk)

    def _process_frame(self, frame):
        hand = self.HandRecognizer.getHand(frame)
        if hand is not None:
            self.FrameDrawing.drawHand(frame, hand)
            self.GestureRecognizer.addHandToGestureBuffer(hand)
            gesture = self.GestureRecognizer.getGesture()
            if gesture is not None and gesture.startpoint is not None and gesture.endpoint is not None:
                self.FrameDrawing.drawGesture(frame, gesture)
        else:
            self.FrameDrawing.putText(frame, "No hand detected")

    def process_frame_loop(self):
        _, frame = self.camera.read()
        if frame is not None:
            self._process_frame(frame)
            self.displayFrame(frame)
        else:
            message.showerror("Error", "No frame found")
        self.mainWindowRefresh = self.imageContainer.after(10, self.process_frame_loop)

    def button_changeColorRange(self):
        ColorRangePicker(self.camera, self.colorChangedEvent)
        if self.mainWindowRefresh is not None:
            self.imageContainer.after_cancel(self.mainWindowRefresh)

    def onColorChanged(self, lowerColor, upperColor):
        self.HandRecognizer.filter.setColor(lowerColor, upperColor)
        self.process_frame_loop()

    def camera_is_available(self):
        _, image = self.camera.read()

        # If we do not get anything, probably no camera is connected
        if image is None:
            return False

        # Check for black image (program started twice)
        if self._is_mostly_black(image):
            return False

        return True

    @staticmethod
    def _is_mostly_black(frame):
        average_color_per_row = numpy.average(frame, axis=0)
        average_color = numpy.average(average_color_per_row, axis=0)
        if average_color[0] < LITTLE_COLOR and average_color[1] < LITTLE_COLOR and average_color[2] < LITTLE_COLOR:
            return True
        return False

print(tkinter.TkVersion)

if __name__ == "__main__":
    controller = Controller()
    if not controller.camera_is_available():
        print("Kamera funktioniert nicht / keine Kamera gefunden. Programm zweimal gestartet?")
    else:
        controller.window.after_idle(controller.process_frame_loop)
        controller.window.mainloop()
