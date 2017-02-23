from tkinter import *
from collections import deque
import cv2
import numpy as np
import colorsys
from SettingsWindow import MyWindow
from gestures import HandRecognizer




def loop():
    print(window.getLowerHsv(), window.getUpperHsv())
    lmain.after(1000, loop)
def buttonSettings():
    window.initUI()


cap = cv2.VideoCapture(0)

root = Tk()
root.bind('<Escape>', lambda e:root.quit())
root.geometry("700x700")
b = Button(root, text="set color range", command=buttonSettings)
b.pack()
#hand = HandRecognizer()
t = Toplevel()
window = MyWindow(t, cap)
lmain = Label(root)
lmain.pack()
loop()
root.mainloop()

