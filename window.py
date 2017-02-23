from tkinter import *
from PIL import Image, ImageTk
import cv2
import numpy as np
from matplotlib import pyplot as plt

root = Tk()
root.bind('<Escape>', lambda e:root.quit())
lmain = Label(root)
lmain.pack()
h_lower, s_lower, v_lower, h_upper, s_upper, v_upper = 42, 80, 160, 79, 255, 255

h_l, s_l, v_l, h_h, s_h, v_h = IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar()

h_l_value = Entry(root, textvariable = h_l)
s_l_value = Entry(root, textvariable = s_l)
v_l_value = Entry(root, textvariable = v_l)
h_h_value = Entry(root, textvariable = h_h)
s_h_value = Entry(root, textvariable = s_h)
v_h_value = Entry(root, textvariable = v_h)

for x in (h_l_value, s_l_value, v_l_value, h_h_value, s_h_value, v_h_value):
    x.pack(side=LEFT)

def apply():
    h_lower = h_l.get()
    s_lower = s_l.get()
    v_lower = v_l.get()
    h_upper = h_h.get()
    s_upper = s_h.get()
    v_upper = v_h.get()

apply_button = Button(root, text = "Apply", command = apply)

apply_button.pack()

cap = cv2.VideoCapture(0)

def extract_edges(frame, h_lower, s_lower, v_lower, h_upper, s_upper, v_upper):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    low_neon_green = np.array([h_lower, s_lower, v_lower])  # von 360 deg
    high_neon_green = np.array([h_upper, s_upper, v_upper])

    neon_green_mask = cv2.inRange(hsv_frame, low_neon_green,
                                  high_neon_green)  # alles was sich im neongrünen Farbbereich befindet

    neon_green_mask = cv2.erode(neon_green_mask, None, iterations=2)  # maske verfeinern
    neon_green_mask = cv2.dilate(neon_green_mask, None, iterations=2)

    neon_masked_frame = cv2.bitwise_and(frame, frame, mask=neon_green_mask)  # neongrüne Bereiche werden gefiltert

    med_blur_frame = cv2.medianBlur(neon_masked_frame, 15)  # Blur resulting masked Frame

    _, blur_frame_thresh = cv2.threshold(med_blur_frame, 70, 255, cv2.THRESH_BINARY_INV)

    neon_green_edges = cv2.Canny(blur_frame_thresh, 100, 200)  # Extract edges (should only be hand)

    return neon_green_edges


def show_frame():
    _, frame = cap.read()

    cv2image = extract_edges(frame, h_lower, s_lower, v_lower, h_upper, s_upper, v_upper)

    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image = imgtk)
    lmain.after(10, show_frame)


show_frame()


root.mainloop()
