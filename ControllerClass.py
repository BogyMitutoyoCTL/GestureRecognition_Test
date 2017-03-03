from tkinter import *

import time
import cv2
import numpy
from PIL import Image, ImageTk

from ColorRangePickerClass import ColorRangePicker
from EventClass import Event
from FrameDrawingClass import FrameDrawing
from GestureRecognitionClass import GestureRecognizer
from HandRecognitionClass import HandRecognizer

LITTLE_COLOR = 10


class Controller:
    def __init__(self):
        self.colorChangedEvent = Event()
        self.colorChangedEvent.append(self.onColorChanged)
        self.mainWindowRefresh = None
        self.camera = cv2.VideoCapture(0)
        self.HandRecognizer = HandRecognizer()
        self.GestureRecognizer = GestureRecognizer()
        self.FrameDrawing = FrameDrawing()

        # UI-Elements:
        self.window, \
        self.colorPickerButton, \
        self.imageContainer = self.initUI()

    def initUI(self):
        window = Tk()
        window.bind('<Escape>', lambda e: window.quit())

        color_picker_button = Button(window, text="set color range", command=self.button_changeColorRange)
        color_picker_button.pack()

        image_container = Label(window)
        image_container.pack()

        return window, color_picker_button, image_container

    def displayFrame(self, frame):
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        imgTk = ImageTk.PhotoImage(image=img)
        self.imageContainer.imgtk = imgTk
        self.imageContainer.configure(image=imgTk)

    def process_images_loop(self):
        self._process_image()
        self.mainWindowRefresh = self.imageContainer.after_idle(self.process_images_loop)

    def _process_image(self):
        _, frame = self.camera.read()
        hand = self.HandRecognizer.getHand(frame)
        if hand is not None:
            self.FrameDrawing.drawHand(frame, hand)
            self.GestureRecognizer.addHandToGestureBuffer(hand)
            gesture = self.GestureRecognizer.getGesture()
            if gesture is not None and gesture.startpoint is not None and gesture.endpoint is not None:
                self.FrameDrawing.drawGesture(frame, gesture)
        else:
            self.FrameDrawing.putText(frame, "No hand detected")
        self.FrameDrawing.putText(frame, "{:06.2f}".format(time.time() - int(time.time() / 100) * 100), line=2)
        self.displayFrame(frame)

    def button_changeColorRange(self):
        ColorRangePicker(self.camera, self.colorChangedEvent)
        if self.mainWindowRefresh is not None:
            self.imageContainer.after_cancel(self.mainWindowRefresh)

    def onColorChanged(self, lowerColor, upperColor):
        self.HandRecognizer.filter.setColor(lowerColor, upperColor)
        self.process_images_loop()

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


if __name__ == "__main__":
    controller = Controller()
    if not controller.camera_is_available():
        print("Kamera funktioniert nicht / keine Kamera gefunden. Programm zweimal gestartet?")
    else:
        controller.window.after(10, controller.process_images_loop)
        controller.window.mainloop()
