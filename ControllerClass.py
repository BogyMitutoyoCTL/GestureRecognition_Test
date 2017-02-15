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
from dbustest import Bluetoothplayer

systemIsWindows = False if platform.system()[0:5] == "Linux" else True

if not systemIsWindows:
    from picamera.array import PiRGBArray
    from picamera import PiCamera

LITTLE_COLOR = 10
default_camera = 0
resolution = (640, 480)
framerate = 15


class Controller:
    def __init__(self):
        self.colorChangedEvent = Event()
        self.colorChangedEvent.append(self.onColorChanged)
        self.mainWindowRefresh = None
        if systemIsWindows:
            self.camera = cv2.VideoCapture(default_camera)
        else:
            self.camera = PiCamera(resolution=resolution, framerate=framerate)
            self.rawCapture = PiRGBArray(self.camera, size=resolution)
            time.sleep(0.1)

        self.HandRecognizer = HandRecognizer()
        self.GestureRecognizer = GestureRecognizer()
        self.FrameDrawing = FrameDrawing()
        self.Bluetoothplayer = Bluetoothplayer()
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
            if self.Bluetoothplayer.Playing is not True and not systemIsWindows:
                self.Bluetoothplayer.play()
            self.FrameDrawing.drawHand(frame, hand)
            self.GestureRecognizer.addHandToGestureBuffer(hand)
            gesture = self.GestureRecognizer.getGesture()
            if gesture is not None and gesture.startpoint is not None and gesture.endpoint is not None:
                self.FrameDrawing.drawGesture(frame, gesture)
        else:
            if self.Bluetoothplayer.Playing is True and not systemIsWindows:
                self.Bluetoothplayer.pause()
            self.FrameDrawing.putText(frame, "No hand detected")

    def getNextFrame(self):
        if systemIsWindows:
            _, frame = self.camera.read()
        else:
            self.camera.capture(self.rawCapture, format="bgr", use_video_port=True)
            frame = self.rawCapture.array
            self.rawCapture.truncate(0)
        return frame

    def process_frame_loop(self):
        frame = self.getNextFrame()

        if frame is not None:
            self._process_frame(frame)
            self.displayFrame(frame)
        else:
            message.showerror("Error", "No frame found")

        self.mainWindowRefresh = self.imageContainer.after_idle(self.process_frame_loop)

    def button_changeColorRange(self):
        ColorRangePicker(self.camera, self.colorChangedEvent)
        if self.mainWindowRefresh is not None:
            self.imageContainer.after_cancel(self.mainWindowRefresh)

    def onColorChanged(self, lowerColor, upperColor):
        self.HandRecognizer.filter.setColor(lowerColor, upperColor)
        self.process_frame_loop()

    def camera_is_available(self):
        image = self.getNextFrame()

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
        if not systemIsWindows:
            playerfound = controller.Bluetoothplayer.getPlayer()
            if playerfound is not True:
                print("no player was found")
        controller.window.after(10, controller.process_frame_loop)
        controller.window.mainloop()
