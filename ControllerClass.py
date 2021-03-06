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

systemIsWindows = False if platform.system()[0:5] == "Linux" else True

if not systemIsWindows:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    from dbustest import Bluetoothplayer


LITTLE_COLOR = 10
default_camera = 0
resolution = (320, 240)
framerate = 15

class Controller:
    def __init__(self):
        self.colorChangedEvent = Event()
        self.gestureEvent = Event()
        self.colorChangedEvent.append(self.onColorChanged)
        self.gestureEvent.append(self.onGestureRecognized)
        self.mainWindowRefresh = None
        if systemIsWindows:
            global resolution
            self.camera = cv2.VideoCapture(default_camera)
            height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
            width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
            resolution = (width, height)
        else:
            self.camera = PiCamera(resolution=resolution, framerate=framerate)
            self.rawCapture = PiRGBArray(self.camera, size=resolution)
            time.sleep(0.1)
            self.Bluetoothplayer = Bluetoothplayer()

        self.HandRecognizer = HandRecognizer()
        self.GestureRecognizer = GestureRecognizer(resolution, self.gestureEvent)
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
        self.HandRecognizer.filter.set_color_range(lowerColor, upperColor)
        self.process_frame_loop()

    def onGestureRecognized(self, gestureName):
        if not systemIsWindows:
            if gestureName == "Play" and not self.Bluetoothplayer.Playing:
                self.Bluetoothplayer.play()
            if gestureName == "Pause" and self.Bluetoothplayer.Playing:
                self.Bluetoothplayer.pause()
            if gestureName == "Previous":
                self.Bluetoothplayer.prevTrack()
            if gestureName == "Next":
                self.Bluetoothplayer.nextTrack()
        else:
            print(gestureName)

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
