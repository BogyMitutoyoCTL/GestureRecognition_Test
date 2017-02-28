import cv2
from tkinter import *
from PIL import Image, ImageTk
from ColorRangePickerClass import ColorRangePicker
from EventClass import Event
from FilterClass import Filter
from FrameDrawingClass import FrameDrawing
from GestureRecognitionClass import GestureRecognizer
from HandRecognitionClass import HandRecognizer
import Converter

class Controller():
    def __init__(self, camera=[0]):
        self.camera = camera
        self.initUI()
        self.colorChangedEvent = Event()
        self.mainWindowRefresh = None

    def initUI(self):
        self.root = Tk()
        self.root.bind('<Escape>', lambda e: self.root.quit())

        self.b = Button(self.root, text="set color range", command=self.button_change_color_range)
        self.b.pack()
        self.imageContainer = Label(self.root)
        self.imageContainer.pack()

    def run(self):
        self.capture = cv2.VideoCapture(self.camera)
        filter = Filter(Converter.mapHSVTO255(defaultLowerHSV), Converter.mapHSVTO255(defaultUpperHSV))
        hand = HandRecognizer()
        gesture = GestureRecognizer()
        draw = FrameDrawing()


Controller(0).run()
