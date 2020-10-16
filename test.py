import tkinter as tk

import PIL
from PIL import ImageTk
import cv2
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np

currentFrameIndex = 0
root = tk.Tk()
root.wm_title("Embedding in Tk")
decFrameCv = cv2.imread("frame" + str(currentFrameIndex) + ".jpg")
print("checking dec path: " + "frame" + str(currentFrameIndex) + ".jpg")
decFrame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(decFrameCv))
decFrameButton = tk.Button(root, text="hello", command=print("hello"))
decFrameButton.grid(row=0, column=0)
root.mainloop()
decFrameImageLabel = tk.Label(root, image=decFrame)
decFrameImageLabel.image = decFrame
decFrameImageLabel.grid(row=1, column=0)
# root.mainloop()
# decFrame1 = PIL.Image.open("frame" + str(currentFrameIndex) + ".jpg")
# print("checking dec path: " + "frame" + str(currentFrameIndex) + ".jpg")
# decFrame = tk.PhotoImage(file="frame" + str(currentFrameIndex) + ".jpg")
# root.decFrameImageLabel = tk.Label(root, image=decFrame)
# root.decFrameImageLabel.image = decFrame
# root.decFrameImageLabel.grid(row=0, column=0)
# root.mainloop()
# fig = Figure(figsize=(5, 4), dpi=100)
# t = np.arange(0, 3, .01)
# fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
#
# canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
# canvas.draw()
# canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
#
# toolbar = NavigationToolbar2Tk(canvas, root)
# toolbar.update()
# canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
#
#
# def on_key_press(event):
#     print("you pressed {}".format(event.key))
#     key_press_handler(event, canvas, toolbar)
#
#
# canvas.mpl_connect("key_press_event", on_key_press)
#
#
# def _quit():
#     root.quit()     # stops mainloop
#     root.destroy()  # this is necessary on Windows to prevent
#                     # Fatal Python Error: PyEval_RestoreThread: NULL tstate
#
#
# button = tkinter.Button(master=root, text="Quit", command=_quit)
# button.pack(side=tkinter.BOTTOM)
#
# tkinter.mainloop()
# # If you put root.destroy() here, it will cause an error if the window is
# # closed with the window manager.