from tkinter import *
import tkinter.messagebox as message
import cv2
import numpy
import time
from PIL import Image, ImageTk
from ColorRangePickerClass import ColorRangePicker
from EventClass import Event
from FrameDrawingClass import FrameDrawing
from GestureRecognitionClass import GestureRecognizer
from HandRecognitionClass import HandRecognizer
import platform

if platform.system()[0:5] == "Linux":
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    systemIsWindows = False
else:
    systemIsWindows = True

LITTLE_COLOR = 10
default_camera = 0
resolution = (640, 480)

class Controller:
    def __init__(self):
        self.colorChangedEvent = Event()
        self.colorChangedEvent.append(self.onColorChanged)
        self.mainWindowRefresh = None
        if systemIsWindows:
            self.camera = cv2.VideoCapture(default_camera)
            print(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
            print(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        else:
            self.camera = PiCamera()
            self.camera.resolution = (320,240)
            self.camera.framerate = 20
            self.rawCapture = PiRGBArray(self.camera, size=(320, 240))
            time.sleep(0.1)

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
            self.GestureRecognizer.clearBuffer()

    def process_frame_loop(self):
        if systemIsWindows:
            _, frame = self.camera.read()
        else:
            self.camera.capture(self.rawCapture, format="bgr", use_video_port=True)
            frame = self.rawCapture.array

        if frame is not None:
            self._process_frame(frame)
            self.displayFrame(frame)
        else:
            message.showerror("Error", "No frame found")

        self.mainWindowRefresh = self.imageContainer.after_idle(self.process_frame_loop)
        if not systemIsWindows:
            self.rawCapture.truncate(0)

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


if __name__ == "__main__":
    controller = Controller()
    if not controller.camera_is_available():
        print("Kamera funktioniert nicht / keine Kamera gefunden. Programm zweimal gestartet?")
    else:
        controller.window.after(1, controller.process_frame_loop)
        controller.window.mainloop()
