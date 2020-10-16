import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from matplotlib.backends.backend_template import FigureCanvas
from tkintertable import TableCanvas, TableModel, Tables_IO
from tkinter import scrolledtext
import os
import os.path
import PIL
import shutil as sh
import imgcompare as imgcmp
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import csv
import numpy as np
import time
import glob
import cv2
import moviepy.editor as mp
from matplotlib.backends.backend_tkagg import FigureCanvasTk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure


# from pathlib import Path
# import ttkSimpleDialog
# import sys
# import traceback
# import decompileVideo as dec
# import testColor as tc
# import subtract as sub


'''
NEED TO CHANGE TO PLACE IN PROJECT FOLDERRRRRRRRRRRRRR
'''

debug = False

threshold = 0.003
path = "DecompiledFrames"#directory 1
path2 = "SubtractedFrames"#directory 2
path3 = "BinarizedFrames"
directory = ""
video = ""
current = ""
isDec = False
isSub = False
isBin = False
goingBack = False
activityPage = None
fps = 1
loadedConsoleTable = False
loadedAfflictTable = False
showingTables = False
showingGraph = False
showingFrames = False
decText = []#["hello\n" for i in range(30)]
subText = []
binText = []
vidFramesCount = 0
testCancelled = False
runningTest = False
graphLabelsNeedReset = False
ranOnce = True
analysisTime = None
graphExists = False
currentFrameIndex = 0
vcount = 0
cropping = False
x_start, y_start, x_end, y_end = 0, 0, 0, 0
screen_width, screen_height = 480, 480
num = 0
rectExists = False
app = None
resizePercentage = 100
resizePercentage2 = 100
startTimeInSecs = 0
endTimeInSecs = 0
originalStartTimeInSecs = 0
originalEndTimeInSecs = 0
width, height = 0,0
cropped = False
class StartingPage(tk.Tk):
    def __init__(self):
        super(StartingPage, self).__init__()
        self.initializePage()

    def initializePage(self):
        global goingBack

        self.title("MEDA")
        self.minsize(450,130)
        self.wm_iconbitmap('download.ico')

        self.labelFrame = ttk.LabelFrame(self, text="MEDA")
        # self.labelFrame.grid(column = 0, row = 1, padx = 20, pady = 20)
        self.labelFrame.pack(expand=tk.YES)
        # self.labelFrame.pack(expand=tk.NO)

        self.Video()
        self.Directory()
        self.Current()
        self.Next()
        if goingBack:
            activityPage.destroy()
            goingBack = False

        # self.label = ttk.Label(self.labelFrame, text = "")
        # self.label.grid(row = 3, column = 3)
        # self.label.configure(text = x)

    def createNewWindow(self):
        global activityPage
        global path
        global path2
        global path3
        global directory

        if(len(self.entryDirectory.get()) == 0):
            tk.messagebox.showerror(title="Information Error",
                                              message="The Project Directory was not selected. Please do this.")
            self.initializePage()
        elif(len(self.entryVideo.get()) == 0):
            tk.messagebox.showerror(title="Information Error",
                                              message="The Video File was not selected. Please do this.")
            self.initializePage()
        elif(len(self.entryCurrent.get()) == 0):
            tk.messagebox.showerror(title="Information Error",
                                              message="The Current File was not selected. Please do this.")
            self.initializePage()
        else:
            try:  # making new directory 1, checking to make sure it doesn't already exist
                path = os.path.join(directory, "DecompiledFrames").replace("\\", "/")
                os.mkdir(path)
            except OSError:
                tk.messagebox.showerror(title="file",
                                                  message="The 'DecompiledFrames' folder already exists in the selected project folder. Please delete or choose a different folder")
                return
            try:  # making new directory 2, checking to make sure it doesnt already exist
                path2 = os.path.join(directory, "SubtractedFrames").replace("\\", "/")
                os.mkdir(path2)
            except OSError:
                tk.messagebox.showerror(title="file",
                                                  message="The 'SubtractedFrames' folder already exists in the selected project folder. Please delete or choose a different folder")
                return
            try:  # making new directory 2, checking to make sure it doesnt already exist
                path3 = os.path.join(directory, "BinarizedFrames").replace("\\", "/")
                os.mkdir(path3)
            except OSError:
                warning = tk.messagebox.showerror(title="file",
                                                  message="The 'BinarizedFrames' folder already exists in the selected project folder. Please delete or choose a different folder")
                return
            activityPage = ActivityPage()
            activityPage.mainloop()

    #def button(self):
     #   self.button = ttk.Button(self.labelFrame, text = "Browse A File")


    #     self.Intro()
    #     self.Graph()
    #     self.Next()

    def Video(self):
        global video
        self._labelVideo = ttk.Label(self.labelFrame, text ="Import Video file:", justify=tk.RIGHT)
        self._labelVideo.grid(row=3)
        self.entryVideo = ttk.Entry(self.labelFrame, textvariable=video, width=40)
        self.entryVideo.grid(row=3, column=1)
        self.entryVideo.delete(0, END)
        self.entryVideo.insert(0, video)
        # if len(video) > 0:
        #     print(video)
        video = self.entryVideo.get()
        self.button = ttk.Button(self.labelFrame, text="Browse", command=self.fileDialogVideo)
        self.button.grid(row=3, column=2)
        return video

    def Directory(self):
        global directory
        self._labelDirectory = ttk.Label(self.labelFrame, text ="Select Project folder:", justify=tk.RIGHT)
        self._labelDirectory.grid(row = 2)
        self.entryDirectory = ttk.Entry(self.labelFrame, textvariable=directory, width=40)
        self.entryDirectory.grid(row = 2, column = 1)
        self.entryDirectory.delete(0, END)
        self.entryDirectory.insert(0, directory)
        # if len(directory) > 0:
        #     print(directory)
        directory = self.entryDirectory.get()
        self.button = ttk.Button(self.labelFrame, text="Browse", command = self.fileDialogDirectory)
        self.button.grid(row=2, column=2)

    def Current(self):
        global current
        self._labelCurrent = ttk.Label(self.labelFrame, text ="Import csv file:", justify=tk.RIGHT)
        self._labelCurrent.grid(row = 4)
        self.entryCurrent = ttk.Entry(self.labelFrame, textvariable=current, width=40)
        self.entryCurrent.grid(row = 4, column = 1)
        self.entryCurrent.delete(0, END)
        self.entryCurrent.insert(0, current)
        # if len(current) > 0:
        #     print(current)
        current = self.entryCurrent.get()
        self.button = ttk.Button(self.labelFrame, text="Browse", command = self.fileDialogCurrent)
        self.button.grid(row=4, column=2)

    def fileDialogCurrent(self):
        global current
        self.filename = filedialog.askopenfilename(initialdir = "/", title = "Select A file", filetype = (("CSV Files","*.csv"), ("All Files", "*.*")))
        # self.entryCurrent.delete(0, END)
        # self.entryCurrent.insert(0, str(self.filename))
        # self.label = ttk.Label(self.labelFrame, text="")
        # self.label.grid(column=1, row=4)
        # filename = self.label.configure(text=self.filename)
        current = str(self.filename)
        self.Current()

    def fileDialogVideo(self):
        global video
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select A file", filetype=(("all video format", ".mp4"), ("All Files", "*.*")))
        # self.entryVideo.delete(0, END)
        # self.entryVideo.insert(0, str(self.filename))
        # self.label = ttk.Label(self.labelFrame, text="")
        # self.label.grid(column=1, row=3)
        # filename = self.label.configure(text=self.filename)
        video = str(self.filename)
        self.Video()

    def fileDialogDirectory(self):
        global directory
        self.filename = filedialog.askdirectory()
        # self.entryDirectory.delete(0, END)
        # self.entryDirectory.insert(0, str(self.filename))
        # self.label = ttk.Label(self.labelFrame, text="")
        # self.label.grid(column = 1, row = 2)
        # filename = self.label.configure(text = self.filename)
        directory = str(self.filename)
        self.Directory()

    def Next(self):
        self._button = ttk.Button(self.labelFrame, text="Continue", command=self.createNewWindow)
        self._button.grid(columnspan=2)

class ActivityPage(tk.Tk):
    def __init__(self):
        super(ActivityPage, self).__init__()
        global path
        global path2
        global path3
        global video
        global current
        global directory
        global isDec
        global fps
        global threshold
        global loadedAfflictTable
        global loadedConsoleTable
        global x_end, y_end
        global resizePercentage
        global startTimeInSecs
        global endTimeInSecs
        global originalStartTimeInSecs
        global originalEndTimeInSecs
        global width, height
        if not debug:
            video = startingPage.entryVideo.get()
            print("Video Path: " + str(video))
            current = startingPage.entryCurrent.get()
            print("Current Path: " + str(current))
            directory = startingPage.entryDirectory.get()
            print("Directory Path: " + str(directory))
            print(video)
            startingPage.destroy()
        self.title("MEDA - Project: " + str(directory))
        self.wm_iconbitmap('download.ico')
        self.minsize(720, 480)
        self.protocol("WM_DELETE_WINDOW", self.checkExitActivityPage)

        cap = cv2.VideoCapture(video)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        x_end = width
        y_end = height
        startTimeInSecs = 0
        endTimeInSecs = mp.VideoFileClip(video).duration
        originalStartTimeInSecs = startTimeInSecs
        originalEndTimeInSecs = endTimeInSecs
        # if(x_end > 1000 or y_end > 1000):
        #     resizePercentage = 50
        # elif(x_end > 700 or y_end > 700):
        #     resizePercentage = 70
        if(x_end > y_end):
            resizePercentage = 400/x_end * 100
        elif(x_end <= y_end):
            resizePercentage = 400/y_end * 100


        isDec = False  # variable to check if video has been decompiled
        # try:  # removing directory 1 - clearing it of all past data
        #     sh.rmtree(path)
        # except OSError:
        #     print("No tmp folder found. Will create now.\n")
        # else:
        #     print("Removed tmp folder previously.\n")
        # try:  # removing directory 2 - clearing it of all past frames
        #     sh.rmtree(path2)
        # except OSError:
        #     print("No stmp folder found. Will create now.\n")
        # else:
        #     print("Removed stmp folder previously.\n")
        # try:  # removing directory 2 - clearing it of all past frames
        #     sh.rmtree(path3)
        # except OSError:
        #     print("No btmp folder found. Will create now.\n")
        # else:
        #     print("Removed btmp folder previously.\n")
        # try:  # making new directory 1, checking to make sure it doesn't already exist
        #     path = os.path.join(directory, "DecompiledFrames").replace("\\", "/")
        #     os.mkdir(path)
        # except OSError:
        #     warning = tk.messagebox.showerror(title="file",
        #                                       message="The 'DecompiledFrames' folder already exists in the selected project folder. Please delete or choose a different folder")
            # print("Directory exists\n")
            # return 1
        # else:
        #     print("Temp made\n")
        # try:  # making new directory 2, checking to make sure it doesnt already exist
        #     path2 = os.path.join(directory, "SubtractedFrames").replace("\\", "/")
        #     os.mkdir(path2)
        # except OSError:
        #     warning = tk.messagebox.showerror(title="file",
        #                                       message="The 'SubtractedFrames' folder already exists in the selected project folder. Please delete or choose a different folder")
        #     # print("Directory exists\n")
        #     return 1
        # else:
        #     print("Stemp made\n")
        # try:  # making new directory 2, checking to make sure it doesnt already exist
        #     path3 = os.path.join(directory, "BinarizedFrames").replace("\\", "/")
        #     os.mkdir(path3)
        # except OSError:
        #     warning = tk.messagebox.showerror(title="file",
        #                                       message="The 'BinarizedFrames' folder already exists in the selected project folder. Please delete or choose a different folder")
        #     # print("Directory exists\n")
        #     return 1
        # # else:
        # #     print("Btemp made\n")

        self.LFMeda = LabelFrame(self, text="MEDA")
        self.LFMeda.grid(row=0, column=1, rowspan=1, sticky="NSEW")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)


        self.FVideoEditor = ttk.Frame(self.LFMeda)
        if debug:
            self.FVideoEditor.grid(column=2, row=0, padx=10, pady=10)
        self.FMenu = ttk.Frame(self)
        self.FMenu.grid(column=0, row=0, sticky="N", ipady=75)

        backButton = Button(self.FMenu, text="Exit Project", command=self.goBack)
        backButton.grid(row=0, column=0, ipadx=10, pady=5, sticky='NW')

        self.FVideoEditor = ttk.Label(self.FMenu, text="Edit Video:")
        self.FVideoEditor.grid(row=4, column=0, sticky='NW')
        self.cropButton = Button(self.FMenu, text="Crop Video", command=self.videoEditor, width=19)
        self.cropButton.grid(row=5, column=0, columnspan=2, sticky='NW')

        self.trimEntryLabel = ttk.Label(self.FMenu, text="Trim Video:")
        self.trimEntryLabel.grid(row=6, column=0, sticky="NW")

        self.FstartTimeEntry = ttk.Frame(self.FMenu)
        self.FstartTimeEntry.grid(row=7, column=0, columnspan=2, sticky="NW")
        self.startTimeLabel = ttk.Label(self.FstartTimeEntry, text="Start:  ", width=12)
        self.startTimeLabel.grid(row=0, column=0, sticky="NW")
        self.startTimeEntryHours = ttk.Entry(self.FstartTimeEntry, width=2)
        self.startTimeEntryHours.insert(tk.INSERT, "{:02d}".format(0))
        self.startTimeEntryHours.grid(row=0, column=1)
        self.startcolon1 = ttk.Label(self.FstartTimeEntry, text=":")
        self.startcolon1.grid(row=0, column=2)
        self.startTimeEntryMinutes = ttk.Entry(self.FstartTimeEntry, width=2)
        self.startTimeEntryMinutes.insert(tk.INSERT, "{:02d}".format(0))
        self.startTimeEntryMinutes.grid(row=0, column=3)
        self.startcolon2 = ttk.Label(self.FstartTimeEntry, text=":")
        self.startcolon2.grid(row=0, column=4)
        self.startTimeEntrySeconds = ttk.Entry(self.FstartTimeEntry, width=2)
        self.startTimeEntrySeconds.insert(tk.INSERT, "{:02d}".format(0))
        self.startTimeEntrySeconds.grid(row=0, column=5)

        self.FendTimeEntry = ttk.Frame(self.FMenu)
        self.FendTimeEntry.grid(row=8, column=0, columnspan=2, sticky="NW")
        self.endTimeLabel = ttk.Label(self.FendTimeEntry, text="End:  ", width=12)
        self.endTimeLabel.grid(row=0, column=0, sticky="NW")
        self.endTimeEntryHours = ttk.Entry(self.FendTimeEntry, width=2)
        self.endTimeEntryHours.insert(tk.INSERT, "{:02d}".format(int(int(originalEndTimeInSecs)/int(3600))))
        self.endTimeEntryHours.grid(row=0, column=1)
        self.endcolon1 = ttk.Label(self.FendTimeEntry, text=":")
        self.endcolon1.grid(row=0, column=2)
        self.endTimeEntryMinutes = ttk.Entry(self.FendTimeEntry, width=2)
        self.endTimeEntryMinutes.insert(tk.INSERT, "{:02d}".format(int(int(originalEndTimeInSecs - (int(int(originalEndTimeInSecs) / int(3600)) * 3600))/int(60))))
        self.endTimeEntryMinutes.grid(row=0, column=3)
        self.endcolon2 = ttk.Label(self.FendTimeEntry, text=":")
        self.endcolon2.grid(row=0, column=4)
        self.endTimeEntrySeconds = ttk.Entry(self.FendTimeEntry, width=2)
        self.endTimeEntrySeconds.insert(tk.INSERT, "{:02d}".format(int(originalEndTimeInSecs - int(int(int(originalEndTimeInSecs - (int(int(originalEndTimeInSecs) / int(3600)) * 3600))/int(60)) * 60))))
        self.endTimeEntrySeconds.grid(row=0, column=5)


        self.fpsEntryLabel = Label(self.FMenu, text="FPS:")
        self.fpsEntryLabel.grid(row=9, column=0, sticky="NW")
        self.fpsEntry = ttk.Entry(self.FMenu, width=7)
        self.fpsEntry.grid(row=9, column=1, sticky="NW")
        self.fpsEntry.delete(0, END)
        self.fpsEntry.insert(0, fps)

        self.thresholdEntryLabel = Label(self.FMenu, text="Threshold:")
        self.thresholdEntryLabel.grid(row=10, column=0, sticky="NW")
        self.thresholdEntry = ttk.Entry(self.FMenu, width=7)
        self.thresholdEntry.grid(row=10, column=1, sticky="NW")
        self.thresholdEntry.delete(0, END)
        self.thresholdEntry.insert(0, threshold)

        self.processButton = Button(self.FMenu, text="Perform Test", command=self.percentChange, width=19)
        self.processButton.grid(row=11, column=0, columnspan=2, sticky="NW")
        self.tableButtonOnMenu = Button(self.FMenu, text=" Show Tables", state="disabled", width=19)
        self.tableButtonOnMenu.grid(row=12, column=0, columnspan=2, sticky="NW")
        self.graphButton = Button(self.FMenu, text=" Show Graph", command=self.showOrHideGraph, state="disabled", width=19)
        self.graphButton.grid(row=13, column=0, columnspan=2, sticky="NW")
        self.framesButtonOnMenu = Button(self.FMenu, text=" Show Frames", command=self.showOrHideFrames, state="disabled", width=19)
        self.framesButtonOnMenu.grid(row=14, column=0, columnspan=2, sticky="NW")
        self.decVidButton = Button(self.FMenu, text=" Original Video ", command=self.createDecVideo, state="disabled",width=19)
        self.decVidButton.grid(row=15, column=0, columnspan=2, sticky="NW")
        self.subVidButton = Button(self.FMenu, text="Subtracted Video", command=self.createSubVideo, state="disabled", width=19)
        self.subVidButton.grid(row=16, column=0, columnspan=2, sticky="NW")
        self.binVidButton = Button(self.FMenu, text=" Binarized Video ", command=self.createBinVideo, state="disabled", width=19)
        self.binVidButton.grid(row=17, column=0, columnspan=2, sticky="NW")

        self.allStatusFalse()

        # self.applyButton = Button(self.FVideoEditor, text="Apply & Save", command=self.printTest)
        # self.applyButton.grid(row=1, column=0)

        self.FGraph = ttk.Frame(self.LFMeda)
        if debug or True:
            self.FGraph.grid(row=0, column=1)

        self.FTables = ttk.Frame(self.LFMeda)
        if debug:
            self.FTables.grid(row=0, column=0, sticky="NS", rowspan=2)

        self.FAfflictTable = ttk.Frame(self.FTables)
        self.FAfflictTable.grid(column=0, row=1, padx=10, pady=10, sticky="NW")

        self.FTestDataScrollable = ttk.Frame(self.FAfflictTable)
        self.FTestDataScrollable.grid(column=0, row=0)

        self.FConsoleTable = ttk.Frame(self.FTables)
        self.FConsoleTable.grid(column=0, row=1, padx=10, pady=10, sticky="NW")

        self.FshowTablesButtons = ttk.Frame(self.FTables)
        self.FshowTablesButtons.grid(row=0, column=0, sticky="S", padx=10)
        self.showConsoleDataTableButton = Button(self.FshowTablesButtons, text="Show Console Data",
                                                 command=self.loadConsoleTable, width=19)
        self.showConsoleDataTableButton.grid(row="0", column="0", sticky="S")
        self.showAfflictTableButton = Button(self.FshowTablesButtons, text="Show Affliction Data",
                                             command=self.showAfflictTable, width=19)
        self.showAfflictTableButton.grid(row="0", column="1", sticky="S")

        # self.FshowFrameButtons = ttk.Frame(self.FVideoEditor)
        # self.FshowFrameButtons.grid(row=0, column=0, sticky="S", pady=3)
        # self.showDecFrameButton = Button(self.FshowFrameButtons, text="Decompiled", command=self.showDecFrame, width=10)
        # self.showDecFrameButton.grid(row="0", column="0", sticky="S")
        # self.showSubFrameButton = Button(self.FshowFrameButtons, text="Subtracted", command=self.showSubFrame, width=10)
        # self.showSubFrameButton.grid(row="0", column="1", sticky="S")
        # self.showBinFrameButton = Button(self.FshowFrameButtons, text="Binarized", command=self.showBinFrame, width=10)
        # self.showBinFrameButton.grid(row="0", column="2", sticky="S")

        # self.FframeVisuals = ttk.Frame(self.FVideoEditor)
        # self.FframeVisuals.grid(row=1, column=0, sticky="N", pady=3)
        # self.FdecFrameVisual = ttk.Frame(self.FframeVisuals)
        # self.FsubFrameVisual = ttk.Frame(self.FframeVisuals)
        # self.FbinFrameVisual = ttk.Frame(self.FframeVisuals)
        self.FdecFrameVisual = ttk.Frame(self.LFMeda)
        self.FsubFrameVisual = ttk.Frame(self.LFMeda)
        self.FbinFrameVisual = ttk.Frame(self.LFMeda)

        self.tableButtonOnMenu.configure(command=self.showOrHideAllTables)


        if debug or (isDec and isSub and isBin):
            self.loadAfflictTable()
            # self.loadConsoleTable()
            # self.consoleTableDec.configure(state="disabled")

    def checkExitActivityPage(self):
        if tk.messagebox.askokcancel("Close Program", "Are you sure you want to exit the program. If you exit, you have to start a new project to continue experimentation, but all test data will remain saved."):
            exit()
        else:
            return

    def printTest(self):
        print("This Works in Between")

    def cancelPerformTest(self):
        global testCancelled
        global runningTest
        self.processButton.configure(text="Perform Test")
        self.cropButton.configure(state="normal")
        # self.showOrHideAllTables()
        print("set to false and true")
        runningTest = False
        testCancelled = True

    def allStatusFalse(self):
        global isDec
        global isSub
        global isBin
        self.subVidButton.configure(state="disabled")
        self.binVidButton.configure(state="disabled")
        self.decVidButton.configure(state="disabled")

        isDec = False
        self.labelD = Label(self.FMenu, text="Decompiled: ")
        self.labelD.grid(row=1, column=0, sticky="NW")
        self.labelDstatus = Label(self.FMenu, text=" False   ", fg="red", width=6)
        self.labelDstatus.grid(row=1, column=1, sticky="NW")
        # self.labelDStatus.configure(text="False", fg="red")
        self.update_idletasks()
        self.update()

        isSub = False
        self.labelS = Label(self.FMenu, text="Subtracted:  ")
        self.labelS.grid(row=2, column=0, sticky="NW")
        self.labelSstatus = Label(self.FMenu, text=" False   ", fg="red", width=6)
        self.labelSstatus.grid(row=2, column=1, sticky="NW")
        # self.labelSstatus.configure(text="False", fg="red")
        self.update_idletasks()
        self.update()

        isBin = False
        self.labelB = Label(self.FMenu, text="Binarized:  ")
        self.labelB.grid(row=3, column=0, sticky="NW")
        self.labelBstatus = Label(self.FMenu, text=" False   ", fg="red", width=6)
        self.labelBstatus.grid(row=3, column=1, sticky="NW")
        # self.labelBstatus.configure(text="False", fg="red")
        self.update_idletasks()
        self.update()

    def loadAfflictTable(self):
        global analysisTime
        global showingTables
        global vcount
        afflicDataTableModel = TableModel()
        if debug:
            afflicDataTableModel.importCSV("D:\\TAMS Stuff\\TAMS Research\\Dr. Chyan Lab\\TAMS Summer Research 2020\\MEDA\\FPS Testing\\Sample 1 TI Device\\S1 Reg B\\Results\\15FPM\\0.25FPS AfflictData.csv", sep=",")
        else:
            print(directory + "/Run" + str(vcount) + "-" + str(fps) + "FPS AfflictData.csv")
            afflicDataTableModel.importCSV(directory + "/Run" + str(vcount) + "-" + str(fps) + "FPS AfflictData.csv")
            print(directory + "/Run" + str(vcount) + "-" + str(fps) + "FPS AfflictData.csv")
            self.testDataScrollableLabel = tk.Label(self.FTestDataScrollable, text="Analysis Chart - Key Data", font=("Times New Roman", 14))
            self.testDataScrollableLabel.grid(column=0, row=0, sticky="NW")
            self.testDataScrollable = scrolledtext.ScrolledText(self.FTestDataScrollable, width=47, height=10, wrap=WORD)
            self.testDataScrollable.grid(column=0, row=1, pady=5, sticky="NW")
            self.testDataScrollable.insert(tk.INSERT, "Analysis Time (HH:MM:SS): " + str(time.strftime('%H:%M:%S', time.gmtime(analysisTime))) + "\n")
            initiationIndex = 0
            for i in range(len(self.data1y)):
                if self.data1y[i] > 0:
                    initiationIndex = i
                    break
            self.testDataScrollable.insert(tk.INSERT, "Initiation Time (M): " + str(self.data1x[initiationIndex]) + "\n\n")

            maxAfflictionIndex = self.data1y.index(max(self.data1y))
            self.testDataScrollable.insert(tk.INSERT, "Max Affliction Time (M): " + str(self.data1x[maxAfflictionIndex]) + "\n")
            self.testDataScrollable.insert(tk.INSERT, "Max Affliction Percentage: " + str(self.data1y[maxAfflictionIndex]) + "\n")
            self.testDataScrollable.insert(tk.INSERT, "Max Absolute Affliction (mm^2): " + str(self.data1y[maxAfflictionIndex] / 100.0 * 0.485) + "\n\n")

            finalAfflictionIndex = len(self.data1y) - 1
            self.testDataScrollable.insert(tk.INSERT, "Final Affliction Time (M): " + str(self.data1x[finalAfflictionIndex]) + "\n")
            self.testDataScrollable.insert(tk.INSERT, "Final Affliction Percentage: " + str(self.data1y[finalAfflictionIndex]) + "\n")
            self.testDataScrollable.insert(tk.INSERT, "Final Absolute Affliction (mm^2): " + str(self.data1y[finalAfflictionIndex] / 100.0 * 0.485) + "\n")

            self.testDataScrollable.configure(state="disabled")

        self.FTableCanvas = tk.Frame(self.FAfflictTable)
        self.FTableCanvas.grid(column=0, row=1)
        self.afflictTable = TableCanvas(self.FTableCanvas, model=afflicDataTableModel, rowheaderwidth=0, read_only=True, cols=3, height=700, width=384)
        self.afflictTable.cellwidth=121
        self.afflictTable.maxcellwidth=121
        self.afflictTable.grid(column=0, row=0, sticky="NSW")
        self.afflictTable.show()
        self.afflictTable.resizeColumn(0, 82)
        self.afflictTable.resizeColumn(1, 123)
        self.afflictTable.resizeColumn(2, 178)
        self.showAfflictTable()

    def loadConsoleTable(self):
        global decText
        global subText
        global binText
        global vidFramesCount
        global fps
        global video
        global ranOnce


        if not (isDec or isSub or isBin):
            self.programLoadingBar = ttk.Progressbar(self.FConsoleTable, orient="horizontal", length=415, mode="determinate")
            if not debug:
                vidFramesCount = fps * (endTimeInSecs - startTimeInSecs)
                vidFramesCount = int(vidFramesCount)
                print(vidFramesCount)
                self.programLoadingBar['maximum'] = vidFramesCount * 3 - 2
            self.programLoadingBar.grid(column=0, row=0, pady=10, sticky="W")

            self.consoleTableDecLabel = tk.Label(self.FConsoleTable, text="Decompilation Console Data")
            self.consoleTableDecLabel.grid(column=0, row=1, sticky="W")
            self.consoleTableDec = scrolledtext.ScrolledText(self.FConsoleTable, width=50, height=15, wrap=WORD)
            self.consoleTableDec.grid(column=0, row=2, pady=10)
            for i in range(len(decText)):
                self.consoleTableDec.insert(tk.INSERT, decText[i])

            self.consoleTableSubLabel = tk.Label(self.FConsoleTable, text="Subtraction Console Data")
            self.consoleTableSubLabel.grid(column=0, row=3, sticky="W")
            self.consoleTableSub = scrolledtext.ScrolledText(self.FConsoleTable, width=50, height=15, wrap=WORD)
            self.consoleTableSub.grid(column=0, row=4, pady=10)
            for i in range(len(subText)):
                self.consoleTableSub.insert(tk.INSERT, subText[i])

            self.consoleTableBinLabel = tk.Label(self.FConsoleTable, text="Binarization Console Data")
            self.consoleTableBinLabel.grid(column=0, row=5, sticky="W")
            self.consoleTableBin = scrolledtext.ScrolledText(self.FConsoleTable, width=50, height=15, wrap=WORD)
            self.consoleTableBin.grid(column=0, row=6, pady=10)
            for i in range(len(binText)):
                self.consoleTableBin.insert(tk.INSERT, binText[i])
        self.showConsoleTable()


    def showConsoleTable(self):
        try:
            self.FAfflictTable.grid_remove()
            if (isDec and isSub and isBin):
                self.showAfflictTableButton.configure(state="normal")
            else:
                self.showAfflictTableButton.configure(state="disabled")
        except:
            pass
        self.FConsoleTable.grid(row=1, column=0)
        self.consoleTableDec.configure(state="disabled")
        self.consoleTableSub.configure(state="disabled")
        self.consoleTableBin.configure(state="disabled")
        # self.consoleTableSub.insert(tk.INSERT, "This works")
        # self.consoleTableSub.configure(state="normal")
        # self.consoleTableSub.insert(tk.INSERT, "This works though")
        # self.consoleTableSub.configure(state="disabled")
        self.showConsoleDataTableButton.configure(state="disabled")

    def showAfflictTable(self):
        try:
            self.FConsoleTable.grid_remove()
        except:
            pass
        self.FAfflictTable.grid(row=1, column=0)
        self.showAfflictTableButton.configure(state="disabled")
        self.showConsoleDataTableButton.configure(state="normal")

    def showOrHideGraph(self):
        global showingGraph
        if showingGraph:
            self.FGraph.grid_remove()
            self.graphButton.configure(text="Show Graph")
            showingGraph = False
            self.framesButtonOnMenu.configure(state="disabled")
        else:
            self.FGraph.grid(row=0, column=1, ipadx=5, ipady=5, sticky="NSEW")#, sticky="center")
            self.LFMeda.grid_columnconfigure(1, weight=4, minsize=420)
            self.LFMeda.grid_rowconfigure(0, weight=1, minsize=320)
            self.graphButton.configure(text="Hide Graph")
            showingGraph = True
            self.framesButtonOnMenu.configure(state="normal")


    def showOrHideAllTables(self):
        global showingTables
        if showingTables:
            if debug:
                print("Got here")
            self.FTables.grid_remove()
            self.tableButtonOnMenu.configure(text="Show Tables")
            showingTables = False
        else:
            if debug:
                print("Got here2")
            self.FTables.grid(row=0, column=0, sticky="NS", rowspan=2)
            # self.LFMeda.grid_columnconfigure(0, weight=1)
            self.tableButtonOnMenu.configure(text="Hide Tables")
            showingTables = True

    def showOrHideFrames(self):
        global showingFrames
        if showingFrames:
            # self.FVideoEditor.grid_remove()
            self.FdecFrameVisual.grid_remove()
            self.FsubFrameVisual.grid_remove()
            self.FbinFrameVisual.grid_remove()
            self.graphButton.configure(state="normal")
            self.framesButtonOnMenu.configure(text="Show Frames")
            showingFrames = False
        else:
            # self.FVideoEditor.grid(row=0, column=2, sticky="NW")
            self.FdecFrameVisual.grid(row=1, column=1)
            self.FsubFrameVisual.grid(row=0, column=2)
            self.FbinFrameVisual.grid(row=1, column=2)
            self.LFMeda.columnconfigure(2, weight=1)
            self.framesButtonOnMenu.configure(text="Hide Frames")
            self.graphButton.configure(state="disabled")
            showingFrames = True

    # def showDecFrame(self):
    #     try:
    #         self.FsubFrameVisual.grid_remove()
    #     except:
    #         pass
    #
    #     try:
    #         self.FbinFrameVisual.grid_remove()
    #     except:
    #         pass
    #     self.FdecFrameVisual.grid(row=0, column=0)
    #
    # def showSubFrame(self):
    #     try:
    #         self.FdecFrameVisual.grid_remove()
    #     except:
    #         pass
    #
    #     try:
    #         self.FbinFrameVisual.grid_remove()
    #     except:
    #         pass
    #     self.FsubFrameVisual.grid(row=0, column=0)
    #
    # def showBinFrame(self):
    #     try:
    #         self.FdecFrameVisual.grid_remove()
    #     except:
    #         pass
    #
    #     try:
    #         self.FsubFrameVisual.grid_remove()
    #     except:
    #         pass
    #     self.FbinFrameVisual.grid(row=0, column=0)


    def buildUp(self, bounding, pathing, directory):
        ##    initFrame = input("Intial frame of dendrite formation?")#getting initial frame from user input
        # img_array = []  # array to stoer image files
        ##    iFrame = int(initFrame)#casting input of user to an int
        bound = len(bounding) - 1  # returns length of the bounding
        iFrame = 0
        text = ""
        saveText = ""
        if "SubtractedFrames" in pathing:
            # print("Going here")
            text = "/isframe"
            saveText = "FPS SubtractedFramesVideo.mp4"
            bound += 1
        elif "BinarizedFrames" in pathing:
            text = "/binarizedim"
            saveText = "FPS BinarizedFramesVideo.mp4"
        elif "DecompiledFrames":
            text = "/frame"
            saveText = "FPS NormalFramesVideo.mp4"
        img = cv2.imread(pathing + text + str(iFrame) + ".png")
        # height, width, layers = img.shape
        height = img.shape[0]
        width = img.shape[1]
        size = (width, height)
        out = cv2.VideoWriter(directory + "/Run" + str(vcount) + "-" + str(fps) + saveText, cv2.VideoWriter_fourcc(*'MP4V'), fps, size)  # need to change##############################
        for i in range(iFrame+1, bound):  # for all the frames
            img = cv2.imread(pathing + text + str(i) + ".png")
            out.write(img)
        out.release()

    def createSubVideo(self):
        print(path2 + "/*.png")
        bound = glob.glob(path2 + "/*.png")  # creating an array of all the new frames' names
        self.buildUp(bound, path2, directory)  # building up a new video using the frames' names array and file path

    def createBinVideo(self):
        print(path3 + "/*.png")
        bound = glob.glob(path3 + "/*.png")  # creating an array of all the new frames' names
        self.buildUp(bound, path3, directory)  # building up a new video using the frames' names array and file path

    def createDecVideo(self):
        print(path + "/*.png")
        bound = glob.glob(path + "/*.png")  # creating an array of all the new frames' names
        self.buildUp(bound, path, directory)

    def videoEditor(self):
        print(video)
        global rectExists
        rectExists = False
        app = ExampleApp()
        app.mainloop()
        app.destroy()

    def breakDown(self, video, pathing, sec, num):  # function to check if video file still has frames
        global decText
        global resizePercentage
        global x_start, y_start
        global x_end, y_end
        global width, height
        video.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)  # set the video to the position in milliseconds (sec*1000)
        hasFrames, frame = video.read()  # set hasFrames and image to get if video has frames, and then reading in image
        if hasFrames:  # if the video has a frame, then write it to a file named "frame#" where # is the frame number
            # if not cropped:
            #     x_end = int(frame.shape[1] * resizePercentage / 100)
            #     y_end = int(frame.shape[0] * resizePercentage / 100)

            image = frame[y_start:y_end, x_start:x_end]
            # dsize = (int(image.shape[1] * resizePercentage2/100), int(image.shape[0] * resizePercentage2/100))
            # image2 = cv2.resize(image, dsize)
            print(str(x_start) + " " + str(y_start) + " " + str(x_end) + " " + str(y_end))
            cv2.imwrite(pathing + "/frame%d.png" % num, image)
            decText.append('Read frame ' + str(num+1) + ': ' + str(hasFrames) + "\n")  # printing if frame has been read
            self.consoleTableDec.configure(state="normal")
            self.consoleTableDec.insert(tk.INSERT, decText[num])
            self.consoleTableDec.see(tk.END)
            self.consoleTableDec.configure(state="disabled")
            self.programLoadingBar['value'] += 1
            self.programLoadingBar.update()
            self.update_idletasks()
            self.update()
        return hasFrames  # return if there is actually a frame

    def decomp(self, video, pathing, framerate):  # function called to break a video down into individual frames to count them up
        global fps
        global testCancelled
        global startTimeInSecs
        global endTimeInSecs
        global resizePercentage
        global x_start, x_end, y_start, y_end
        global resizePercentage2
        fps = framerate
        count = 0  # frame counting variable
        # userInp = input("Full video file path: ")  # Getting file name and path for video to be analyzed
        # print("Video from decomp function: " + str(video))
        if video == "cancel":  # leaving program if userinput is to cancel
            return -1
        vidFile = cv2.VideoCapture(video)  # reading in video file

        sec = startTimeInSecs  # time elapsed
        # fps = 1  # 10 frame -> 1 sec, means 1 frame -> 0.1 sec#####################################
        frameRate = 1.0 / fps
        if cropped:
            x_start = int(x_start / (resizePercentage / 100))
            x_end = int(x_end / (resizePercentage / 100))
            y_start = int(y_start / (resizePercentage / 100))
            y_end = int(y_end / (resizePercentage / 100))

        if(x_end - x_start > y_end - y_start):
            resizePercentage2 = 400/(x_end - x_start) * 100
        else:
            resizePercentage2 = 400/(y_end - y_start) * 100

        success = self.breakDown(vidFile, pathing, sec, count)  # getting success bool from breakdown function (for first frame)

        while success:  # looping while video has more frames to break down into
            if testCancelled:
                return -1
            count += 1  # incrementing frame count
            sec = sec + frameRate  # incrementing seconds counter by frameRate
            sec = round(sec, 2)  # rounds the seconds to the nearest 2nd decimal (why do we need this?)
            if(sec > endTimeInSecs):
                print('poopy')
                print(str(startTimeInSecs) + ", " + str(endTimeInSecs))
                return count - 1
            success = self.breakDown(vidFile, pathing, sec, count)  # calling breakDown function again (for next frame)
        return count - 1  # returning total frames in video

    def changeLineOnGraphFromVideo(self, xpos):
        self.currentLocationLine.set_data([xpos, xpos], [min(self.data2y), max(self.data2y)])
        self.canvas.draw()
        self.update_idletasks()
        self.update()

    def changeLineOnGraphFromClick(self, xpos):
        global currentFrameIndex
        correctIndex1x = 0
        currentIndex1x = 1
        for i in range(len(self.data1x) - 1):
            if (self.data1x[currentIndex1x] > xpos):
                break
            else:
                correctIndex1x += 1
                currentIndex1x += 1
        currentFrameIndex = correctIndex1x

        self.updateGraphLabels(xpos)
        self.currentLocationLine.set_data([xpos, xpos], [min(self.data2y), max(self.data2y)])
        self.canvas.draw()

        self.decFrameMp = cv2.imread(str(path) + "/frame" + str(currentFrameIndex) + ".png")
        self.decFrameMp = self.decFrameMp[..., ::-1]
        self.decFigurePlot.imshow(self.decFrameMp)
        self.decFrameCanvas.draw()

        self.subFrameMp = cv2.imread(str(path2) + "/isframe" + str(currentFrameIndex) + ".png")
        self.subFrameMp = self.subFrameMp[..., ::-1]
        self.subFigurePlot.imshow(self.subFrameMp)
        self.subFrameCanvas.draw()

        self.binFrameMp = cv2.imread(str(path3) + "/binarizedim" + str(currentFrameIndex) + ".png")
        self.binFigurePlot.imshow(self.binFrameMp)
        self.binFrameCanvas.draw()
        # decFrame = Image.open(str(path) + "/frame" + str(currentFrameIndex) + ".png")
        # decFrame = ImageTk.PhotoImage(decFrame)
        # self.decFrameCanvas.itemconfig(self.decFrameCanvasImage, image=decFrame)

        # subFrame = Image.open(str(path2) + "/isframe" + str(currentFrameIndex) + ".png")
        # subFrame = ImageTk.PhotoImage(subFrame)
        # self.subFrameCanvas.itemconfig(self.subFrameCanvasImage, image=subFrame)
        #
        # binFrame = Image.open(str(path3) + "/binarizedim" + str(currentFrameIndex) + ".png")
        # binFrame = ImageTk.PhotoImage(binFrame)
        # self.binFrameCanvas.itemconfig(self.binFrameCanvasImage, image=binFrame)

        self.update_idletasks()
        self.update()

    def scaleDownImage(self, event):
        self.after(100, self.scaleImage, event)

    def scaleImage(self, event):
        if event.width > event.height:
            width, height = self.decFrame2.size
            W2HRatio = float(width)/float(height)
            newImg = self.decFrame2.resize((int(event.height * W2HRatio), int(event.height)))
            photo = ImageTk.PhotoImage(newImg)
            self.decFrameImageLabel.configure(image=photo)
            self.decFrameImageLabel.image = photo
        elif event.width < event.height:
            width, height = self.decFrame2.size
            H2WRatio = float(height) / float(width)
            newImg = self.decFrame2.resize((int(event.width), int(event.width * H2WRatio)))
            photo = ImageTk.PhotoImage(newImg)
            self.decFrameImageLabel.configure(image=photo)
            self.decFrameImageLabel.image = photo


    def loadFrameVisuals(self):
        global currentFrameIndex
        global resizePercentage2
        global x_start, y_start, x_end, y_end

        # # decFrame1 = PIL.Image.open(str(path) + "/frame" + str(currentFrameIndex) + ".png")
        # self.decFrameShower = tk.Toplevel()
        # # root.wm_title("Embedding in Tk")
        # self.decFrame1 = PIL.Image.open(str(path) + "/frame" + str(currentFrameIndex) + ".png")
        # self.decFrame2 = self.decFrame1.copy()
        # print("checking dec path: " + str(path) + "/frame" + str(currentFrameIndex) + ".png")
        # self.decFrame = ImageTk.PhotoImage(self.decFrame1)
        # self.decFrameImageLabel = tk.Label(self.decFrameShower, image=self.decFrame)
        # self.decFrameImageLabel.image = self.decFrame
        # self.decFrameImageLabel.bind('<Configure>', self.scaleDownImage)
        # self.decFrameImageLabel.grid(column=0, row=0, sticky="NSEW")
        # self.root.columnconfigure(0, weight=1)
        # self.root.rowconfigure(0, weight=1)

        if(x_end - x_start > y_end - y_start):
            resizePercentage2 = 400/(x_end - x_start) * 100
        else:
            resizePercentage2 = 400/(y_end - y_start) * 100
        resizePercentage2 = int(resizePercentage2)
        print("after resize " + str(x_start) + " " + str(y_start) + "_" + str(x_end) + " " + str(y_end))
        print("Resize 2 inside loadFrameVisuals: " + str(resizePercentage2))
        # self.decFrameMp = mpimg.imread(str(path) + "/frame" + str(currentFrameIndex) + ".png")
        self.decFrameMp = cv2.imread(str(path) + "/frame" + str(currentFrameIndex) + ".png")
        self.decFrameMp = self.decFrameMp[..., ::-1]
        # decFrameCv = cv2.imread("frame" + str(currentFrameIndex) + ".png")
        decHeight = self.decFrameMp.shape[0] / 100
        decWidth = self.decFrameMp.shape[1] / 100
        print("H: " + str(decHeight) + " " + "W: " + str(decWidth))
        self.decFigure = Figure(figsize=(decWidth, decHeight), dpi=resizePercentage2)
        self.decFigurePlot = self.decFigure.add_subplot(111)
        self.decFigurePlot.set_axis_off()
        self.decFigurePlot.imshow(self.decFrameMp)
        self.decFigure.tight_layout()
        self.decFrameCanvas = FigureCanvasTkAgg(self.decFigure, master=self.FdecFrameVisual)
        self.decFrameCanvasLabel = ttk.Label(self.FdecFrameVisual, text="Original Video Frame", font=("Times New Roman", 14))
        self.decFrameCanvasLabel.grid(row=0, column=0)
        self.decFrameCanvas.draw()
        self.decFrameCanvas.get_tk_widget().grid(row=1, column=0)#.pack(side="top", fill="both", expand=1)
        # self.decFrameCanvas.tkcanvas.grid(row=0, column=0)#.pack(side="top", fill="both", expand=1)

        # self.subFrameMp = mpimg.imread(str(path2) + "/isframe" + str(currentFrameIndex) + ".png")
        self.subFrameMp = cv2.imread(str(path2) + "/isframe" + str(currentFrameIndex) + ".png")
        self.subFrameMp = self.subFrameMp[..., ::-1]

        # subFrameCv = cv2.imread("frame" + str(currentFrameIndex) + ".png")
        subHeight = self.subFrameMp.shape[0] / 100
        subWidth = self.subFrameMp.shape[1] / 100
        self.subFigure = Figure(figsize=(subWidth, subHeight), dpi=resizePercentage2)
        self.subFigurePlot = self.subFigure.add_subplot(111)
        self.subFigurePlot.set_axis_off()
        self.subFigurePlot.imshow(self.subFrameMp)
        self.subFigure.tight_layout()
        self.subFrameCanvas = FigureCanvasTkAgg(self.subFigure, master=self.FsubFrameVisual)
        self.subFrameCanvasLabel = ttk.Label(self.FsubFrameVisual, text="Subtracted Video Frame", font=("Times New Roman", 14))
        self.subFrameCanvasLabel.grid(row=0, column=0)
        self.subFrameCanvas.draw()
        self.subFrameCanvas.get_tk_widget().grid(row=1, column=0)#.pack(side="top", fill="both", expand=1)
        # self.subFrameCanvas.tkcanvas.grid(row=0, column=0)#.pack(side="top", fill="both", expand=1)

        # self.binFrameMp = mpimg.imread((path3) + "/binarizedim" + str(currentFrameIndex) + ".png")
        self.binFrameMp = cv2.imread((path3) + "/binarizedim" + str(currentFrameIndex) + ".png")
        # self.binFrameMp = self.binFrameMp[..., ::-1]
        # binFrameCv = cv2.imread("frame" + str(currentFrameIndex) + ".png")
        binHeight = self.binFrameMp.shape[0] / 100
        binWidth = self.binFrameMp.shape[1] / 100
        self.binFigure = Figure(figsize=(binWidth, binHeight), dpi=resizePercentage2)
        self.binFigurePlot = self.binFigure.add_subplot(111)
        self.binFigurePlot.set_axis_off()
        self.binFigurePlot.imshow(self.binFrameMp)
        self.binFigure.tight_layout()
        self.binFrameCanvas = FigureCanvasTkAgg(self.binFigure, master=self.FbinFrameVisual)
        self.binFrameCanvasLabel = ttk.Label(self.FbinFrameVisual, text="Binarized Video Frame", font=("Times New Roman", 14))
        self.binFrameCanvasLabel.grid(row=0, column=0)
        self.binFrameCanvas.draw()
        self.binFrameCanvas.get_tk_widget().grid(row=1, column=0)#.pack(side="top", fill="both", expand=1)
        # self.binFrameCanvas.tkcanvas.grid(row=0, column=0)#.pack(side="top", fill="both", expand=1)

        # decFrameCv = cv2.imread("frame" + str(currentFrameIndex) + ".png")
        # print("checking dec path: " + "frame" + str(currentFrameIndex) + ".png")
        # decFrame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(decFrameCv))
        # self.decFrameImageLabel = tk.Label(self.FdecFrameVisual, image=decFrame)
        # self.decFrameImageLabel.image = decFrame
        # self.decFrameImageLabel.grid(row=0, column=0)
        # self.decFrameCanvas = tk.Canvas(self.FdecFrameVisual, height = 480, width = 480)
        # self.decFrameCanvas.grid(row=0, column=0)
        # self.decFrameCanvasImage = self.decFrameCanvas.create_image(0, 0, image=decFrame)

        # subFrame = PIL.Image.open(str(path2) + "/isframe" + str(currentFrameIndex) + ".png")
        # subFrame = ImageTk.PhotoImage(subFrame)
        # self.subFrameImageLabel = tk.Label(self.FsubFrameVisual, image=subFrame)
        # self.subFrameImageLabel.image = subFrame
        # self.subFrameImageLabel.grid(row=0, column=0)
        # # self.subFrameCanvas = tk.Canvas(self.FsubFrameVisual)
        # # self.subFrameCanvas.grid(row=0, column=0)
        # # self.subFrameCanvasImage = self.subFrameCanvas.create_image(0, 0, image=subFrame)
        #
        # binFrame = PIL.Image.open(str(path3) + "/binarizedim" + str(currentFrameIndex) + ".png")
        # binFrame = ImageTk.PhotoImage(binFrame)
        # self.binFrameImageLabel = tk.Label(self.FbinFrameVisual, image=binFrame)
        # self.binFrameImageLabel.image = binFrame
        # self.binFrameImageLabel.grid(row=0, column=0)
        # # self.binFrameCanvas = tk.Canvas(self.FbinFrameVisual)
        # # self.binFrameCanvas.grid(row=0, column=0)
        # # self.binFrameCanvasImage = self.binFrameCanvas.create_image(0, 0, image=binFrame)

        self.showOrHideFrames()
        # self.showDecFrame()

    def resetGraphLabels(self):
        global graphLabelsNeedReset
        self.xValOnClickLabel = Label(self.FGraphLabels, text="Time(x): --:--:--", font=("Times New Roman", 14),
                                      justify=RIGHT, width=16)
        self.xValOnClickLabel.grid(row=0, column=0, sticky="E")  # , padx=5)
        self.y1ValOnClickLabel = Label(self.FGraphLabels, text="% Area Change(y1): -------",
                                       font=("Times New Roman", 14), justify=RIGHT, width=26, fg='green')
        self.y1ValOnClickLabel.grid(row=0, column=2, sticky="E")  # , padx=5)
        self.y2ValOnClickLabel = Label(self.FGraphLabels, text="Current(y2): -------", font=("Times New Roman", 14),
                                       justify=RIGHT, width=20, fg='blue')
        self.y2ValOnClickLabel.grid(row=0, column=4, sticky="E")  # , padx=5)
        graphLabelsNeedReset = False

    def updateGraphLabels(self, xpos):
        global graphLabelsNeedReset
        correctIndex1x = 0
        currentIndex1x = 1
        for i in range(len(self.data1x) - 1):
            if (self.data1x[currentIndex1x] > xpos):
                break
            else:
                correctIndex1x += 1
                currentIndex1x += 1

        correctIndex2x = 0
        currentIndex2x = 1
        for i in range(len(self.data2x) - 1):
            if (self.data2x[currentIndex2x] > xpos):
                break
            else:
                correctIndex2x += 1
                currentIndex2x += 1
        xVal = str(time.strftime('%H:%M:%S', time.gmtime(xpos * 60)))
        self.xValOnClickLabel.configure(text="Time(x): " + xVal)

        y1Val = str(round(self.data1y[correctIndex1x], 5))
        self.y1ValOnClickLabel.configure(text="% Area Change(y1): " + y1Val)

        y2Val = str(round(self.data2y[correctIndex2x], 5))
        self.y2ValOnClickLabel.configure(text="Current(y2): " + y2Val)
        graphLabelsNeedReset = True

    def on_click(self, event):
        if event.inaxes is not None and event.xdata >= 0 and event.xdata <= max(self.data2x):
            self.changeLineOnGraphFromClick(event.xdata)

            # plt.axvline(x=event.xdata, color='green')
            # print(plt.vlines)
            # print(plt.axes)
            # print(event.xdata, event.ydata)
        # else:
        #     # print('Clicked ouside axes bounds but inside plot window')

    def plotTest(self, directory, currentfile, bounding, subpathing, binpathing, framerate):
        global fps
        global threshold
        global binText
        global graphExists
        global vcount
        fps = framerate
        x = []
        y = []
        afflictFile = open(directory + "/Run" + str(vcount) + "-" + str(fps) + "FPS AfflictData.csv", "w+")
        afflictFile.write("Time(M),%Change, Af-Area(mm^2)\n")
        imi = str(subpathing) + "/isframe0.png"
        imiread = cv2.imread(imi)
        imireadGrayscale = cv2.cvtColor(imiread, cv2.COLOR_BGR2GRAY)
        retval, binarizedimi = cv2.threshold(imireadGrayscale, 75, 255, cv2.THRESH_BINARY)  # +cv2.THRESH_OTSU)
        cv2.imwrite(str(binpathing) + "/binarizedimi0.png", binarizedimi)
        binarizedimipath = str(binpathing) + "/binarizedimi0.png"
        w = 0
        for i in range(bounding):
            if testCancelled:
                return -1
            im = str(subpathing) + "/isframe" + str(i) + ".png"
            # print("Frame difference with initial " + str(i + 1))
            imread = cv2.imread(im)
            imreadGrayscale = cv2.cvtColor(imread, cv2.COLOR_BGR2GRAY)
            retval, binarizedim = cv2.threshold(imreadGrayscale, 75, 255, cv2.THRESH_BINARY)  # +cv2.THRESH_OTSU)
            cv2.imwrite(str(binpathing) + "/binarizedim" + str(i) + ".png", binarizedim)
            binarizedimpath = str(binpathing) + "/binarizedim" + str(i) + ".png"
            percent = imgcmp.image_diff_percent(binarizedimpath, binarizedimipath)
            # print("Percent of afflicted pixels in subtract: " + str(percent))
            x.append(((i / (fps)) + startTimeInSecs) / 60)  # points on xaxis##########################################
            afflictFile.write(str((((i / (fps)) + startTimeInSecs) / 60)) + ",")  #########################################
            if percent >= threshold:
                y.append(percent)
                afflictFile.write(str(percent) + "," + str(percent / 100.0 * 0.485) + "\n")
                binText.append("%Affliction between Initial and Frame " + str(i + 1) + ":\n  - " + str(percent) + " - Appended Percent\n\n")  # printing if frame has been read
                self.consoleTableBin.configure(state="normal")
                self.consoleTableBin.insert(tk.INSERT, binText[i])
                self.consoleTableBin.see(tk.END)
                self.consoleTableBin.configure(state="disabled")
                self.programLoadingBar['value'] += 1
                self.programLoadingBar.update()
                self.update_idletasks()
                self.update()
                # print("Appended percent.")
                if w == 0:
                    w = percent
                x[i] -= w
            else:
                y.append(0)
                afflictFile.write("0,0\n")
                binText.append("%Affliction between Initial and Frame " + str(i + 1) + ":\n  - " + str(percent) + " - Appended Zero\n\n")
                self.consoleTableBin.configure(state="normal")
                self.consoleTableBin.insert(tk.INSERT, binText[i])
                self.consoleTableBin.see(tk.END)
                self.consoleTableBin.configure(state="disabled")
                self.update_idletasks()
                self.update()
        afflictFile.close()
        #    plt.plot(x, y)
        #    plt.xlabel('Time (secs)')#.1,.2,.3,etc.
        #    plt.ylabel('% area covered')
        #    plt.axis([0, bounding/10, 0, 0.5])
        #    plt.show()

        current = currentfile

        self.data1x = x
        self.data1y = y

        # root = tkinter.Tk()
        # root.wm_title("Embedding in Tk")

        # This is oneeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
        # self.fig = Figure(figsize=(7, 6), dpi=100)
        # self.fig.add_subplot(111).plot(data1x, data1y)
        # axes = self.fig.get_axes()
        # ax1 = axes[0]

        self.fig, ax1 = plt.subplots()
        ax1.set_title("% Change vs Current vs Time", fontweight='bold')

        green = 'tab:green'
        ax1.set_xlabel('Time (Min)', fontweight='bold', labelpad=10)
        ax1.set_ylabel('% Area Covered', color=green, fontweight='bold', labelpad=10)
        ax1.plot(self.data1x, self.data1y, color=green)
        ax1.tick_params(axis='y', labelcolor=green, color=green)
        for tick in ax1.xaxis.get_major_ticks():
            tick.label1.set_fontweight('bold')
        for tick in ax1.yaxis.get_major_ticks():
            tick.label1.set_fontweight('bold')

        ax2 = ax1.twinx()

        self.data2x = []
        self.data2y = []
        with open(current) as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            for row in reader:
                try:
                    if ((float(row[0]) >= (float(startTimeInSecs) / 60.0)) and (float(row[0]) <= (float(endTimeInSecs) / 60.0))):
                        self.data2x.append(float(row[0]))
                        self.data2y.append(float(row[1]) * 1000000)
                    elif(float(row[0]) > (float(endTimeInSecs) / 60.0)):
                        break
                except:
                    pass

        blue = 'tab:blue'
        ax2.set_ylabel('Current (μA)', color=blue, fontweight='bold',
                       labelpad=10)  # we already handled the x-label with ax1
        ax2.plot(self.data2x, self.data2y, color=blue)
        ax2.tick_params(axis='y', labelcolor=blue, color=blue)
        for tick in ax2.yaxis.get_major_ticks():
            tick.label2.set_fontweight('bold')
        for tick in ax2.xaxis.get_major_ticks():
            tick.label2.set_fontweight('bold')
        # ax2.set_aspect(1.5)
        # self.fig.set_dpi(150)
        self.fig.tight_layout()
        tend1 = time.time()
        # plt.show()
        plt.savefig(directory + "/Run" + str(vcount) + "_" + str(fps) + " Graph.png")
        # plt.grid()
        # plt.gcf().canvas.draw()
        # self.fig = plt.figure()
        # plt.axvline(x=20)
        self.FGraphLabels = Frame(self.FGraph)
        self.FGraphLabels.pack(side=tk.TOP)

        self.xValOnClickLabel = Label(self.FGraphLabels, text="Time(x): --:--:--", font=("Times New Roman", 14), justify=RIGHT, width=16)
        self.xValOnClickLabel.grid(row=0, column=0, sticky="E")#, padx=5)
        # self.xValOnClickLabelVal = Label(self.FGraphLabels, text="--:--:--", font=("Times New Roman", 12), justify=LEFT, width=11)
        # self.xValOnClickLabelVal.grid(row=0, column=1, sticky="W")#, padx=5)
        self.y1ValOnClickLabel = Label(self.FGraphLabels, text="% Area Change(y1): -------", font=("Times New Roman", 14), justify=RIGHT, width=26, fg='green')
        self.y1ValOnClickLabel.grid(row=0, column=2, sticky="E")#, padx=5)
        # self.y1ValOnClickLabelVal = Label(self.FGraphLabels, text="-------", font=("Times New Roman", 12), justify=LEFT, width=10)
        # self.y1ValOnClickLabelVal.grid(row=0, column=3, sticky="W")#, padx=5)
        self.y2ValOnClickLabel = Label(self.FGraphLabels, text="Current(y2): -------", font=("Times New Roman", 14), justify=RIGHT, width=20, fg='blue')
        self.y2ValOnClickLabel.grid(row=0, column=4, sticky="E")#, padx=5)
        # self.y2ValOnClickLabelVal = Label(self.FGraphLabels, text="-------", font=("Times New Roman", 12), justify=LEFT, width=10)
        # self.y2ValOnClickLabelVal.grid(row=0, column=5, sticky="W")#, padx=5)


        self.canvas = FigureCanvasTkAgg(self.fig, master=self.FGraph)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

        # self.fig.canvas.callbacks.connect('button_press_event', self.on_click)
        self.fig.canvas.callbacks.connect('button_release_event', self.on_click)
        # self.fig.canvas.callbacks.connect('motion_notify_event', self.on_click)

        self.currentLocationLine, v = plt.plot(int(startTimeInSecs/60), int(startTimeInSecs/60), min(self.data2y), max(self.data2y), color='red', linewidth=2)
        plt.xlim(startTimeInSecs/60-((endTimeInSecs - startTimeInSecs)/60/20), endTimeInSecs/60+((endTimeInSecs - startTimeInSecs)/60/20))

        toolbar = NavigationToolbar2Tk(self.canvas, self.FGraph)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        if showingGraph:
            self.showOrHideGraph()
            self.showOrHideGraph()
        else:
            self.showOrHideGraph()

        graphExists = True
        return tend1

    def initmult(self, bounder, pathing1, pathing2):  # subtracts initial image from each frame and makes that many subtracted ones, makes bound and returns the value
        global subText
        global testCancelled
        count = 0
        for i in range(bounder):
            if testCancelled:
                return -1
            im1 = cv2.imread(pathing1 + "/frame0.png")  # image 1
            im2 = cv2.imread(pathing1 + "/frame" + str(i) + ".png")  # image 2
            polaroid = cv2.subtract(im1, im2)  # subtracting each image
            cv2.imwrite(pathing2 + "/isframe%d.png" % count, polaroid)  # writing to new
            count += 1
            subText.append("Initial frame and frame " + str(i+1) + " subtracted.\n")
            self.consoleTableSub.configure(state="normal")
            self.consoleTableSub.insert(tk.INSERT, subText[i])
            self.consoleTableSub.see(tk.END)
            self.consoleTableSub.configure(state="disabled")
            self.programLoadingBar['value'] += 1
            self.programLoadingBar.update()
            self.update_idletasks()
            self.update()
        return count  # returns how many of the newly subtracted images there are (isframe, not sframe, each are different)

    def percentChange(self):
        global isDec
        global isSub
        global isBin
        global path
        global path2
        global path3
        global video
        global current
        global directory
        global fps
        global threshold
        global decText
        global subText
        global binText
        global testCancelled
        global runningTest
        global analysisTime
        global graphExists
        global startTimeInSecs
        global endTimeInSecs
        global vcount

        if runningTest:
            self.cancelPerformTest()
            return

        runningTest = True
        self.processButton.configure(text="Cancel Test")
        self.tableButtonOnMenu.configure(state="disabled")
        self.graphButton.configure(state="disabled")
        self.framesButtonOnMenu.configure(state="disabled")
        self.cropButton.configure(state="disabled")

        decText = []
        subText = []
        binText = []
        fps = float(self.fpsEntry.get())
        threshold = float(self.thresholdEntry.get())
        self.allStatusFalse()

        print(startTimeInSecs)
        startTimeSeconds = int(self.startTimeEntrySeconds.get())
        startTimeMinutes = int(self.startTimeEntryMinutes.get()) * 60
        startTimeHours = int(self.startTimeEntryHours.get()) * 3600
        print('start' + str(startTimeSeconds) + ':' + str(startTimeMinutes) + ':' + str(startTimeHours))

        startTimeInSecs2 = int(startTimeSeconds) + int(startTimeMinutes) + int(startTimeHours)
        print('startTimeInSecs2 ' + str(startTimeInSecs2))


        endTimeSeconds = int(self.endTimeEntrySeconds.get())
        endTimeMinutes = int(self.endTimeEntryMinutes.get()) * 60
        endTimeHours = int(self.endTimeEntryHours.get()) * 3600
        print('end' + str(endTimeSeconds) + ':' + str(endTimeMinutes) + ':' + str(endTimeHours))

        endTimeInSecs2 = int(endTimeSeconds) + int(endTimeMinutes) + int(endTimeHours)
        print('endTimeInSecs2 ' + str(endTimeInSecs2))

        if(startTimeInSecs2 < originalStartTimeInSecs or endTimeInSecs2 > originalEndTimeInSecs or endTimeInSecs2 <= startTimeInSecs2):
            messagebox.showerror(title="Start/End Time Error", message="Please enter a valid start and end time. The start time cannot be less than zero, the end time must be less than the original video length, and the start time must be less than the end time.")
            self.startTimeEntryHours.delete(0, END)
            self.startTimeEntryHours.insert(tk.INSERT, "{:02d}".format(0))
            self.startTimeEntryMinutes.delete(0, END)
            self.startTimeEntryMinutes.insert(tk.INSERT, "{:02d}".format(0))
            self.startTimeEntrySeconds.delete(0, END)
            self.startTimeEntrySeconds.insert(tk.INSERT, "{:02d}".format(0))

            self.endTimeEntryHours.delete(0, END)
            self.endTimeEntryHours.insert(tk.INSERT, "{:02d}".format(int(int(originalEndTimeInSecs) / int(3600))))
            self.endTimeEntryMinutes.delete(0, END)
            self.endTimeEntryMinutes.insert(tk.INSERT, "{:02d}".format(int(int(originalEndTimeInSecs - (int(int(originalEndTimeInSecs) / int(3600)) * 3600)) / int(60))))
            self.endTimeEntrySeconds.delete(0, END)
            self.endTimeEntrySeconds.insert(tk.INSERT, "{:02d}".format(int(originalEndTimeInSecs - int(int(int(originalEndTimeInSecs - (int(int(originalEndTimeInSecs) / int(3600)) * 3600)) / int(60)) * 60))))

            print('time error - not possible time' + str(endTimeInSecs))
            self.cancelPerformTest()
        else:
            startTimeInSecs = int(startTimeInSecs2)
            endTimeInSecs = int(endTimeInSecs2)
            print(str(startTimeInSecs) + ' to ' + str(endTimeInSecs))
            self.loadConsoleTable()

        if testCancelled:
            runningTest = False
            testCancelled = False
            return

        self.FdecFrameVisual.destroy()
        self.FsubFrameVisual.destroy()
        self.FbinFrameVisual.destroy()
        self.FdecFrameVisual = ttk.Frame(self.LFMeda)
        self.FsubFrameVisual = ttk.Frame(self.LFMeda)
        self.FbinFrameVisual = ttk.Frame(self.LFMeda)

        self.consoleTableDecLabel.configure(text="Decompilation Console Data")
        self.consoleTableSubLabel.configure(text="Subtraction Console Data")
        self.consoleTableBinLabel.configure(text="Binarization Console Data")
        self.update_idletasks()
        self.update()

        if testCancelled:
            runningTest = False
            testCancelled = False
            return

        if showingGraph or graphExists:
            self.FGraph.destroy()
            self.FGraph = ttk.Frame(self.LFMeda)
            graphExists = False
            self.showOrHideGraph()
        if showingTables:
            self.showOrHideAllTables()
            self.showOrHideAllTables()
        else:
            self.showOrHideAllTables()

        if showingFrames:
            self.showOrHideFrames()

        try:  # removing directory 1 - clearing it of all past data
            sh.rmtree(path)
        except OSError:
            pass
            # print("No tmp folder found. Will create now.\n")
        # else:
        #     print("Removed tmp folder previously.\n")
        try:  # removing directory 2 - clearing it of all past frames
            sh.rmtree(path2)
        except OSError:
            pass
            # print("No stmp folder found. Will create now.\n")
        # else:
        #     print("Removed stmp folder previously.\n")
        try:  # removing directory 2 - clearing it of all past frames
            sh.rmtree(path3)
        except OSError:
            pass
            # print("No btmp folder found. Will create now.\n")
        # else:
        #     print("Removed btmp folder previously.\n")
        try:  # making new directory 1, checking to make sure it doesn't already exist
            os.mkdir(path)
        except OSError:
            # print("Directory exists\n")
            return 1
        # else:
        #     print("Temp made\n")
        try:  # making new directory 2, checking to make sure it doesnt already exist
            os.mkdir(path2)
        except OSError:
            # print("Directory exists\n")
            return 1
        # else:
        #     print("Stemp made\n")
        try:  # making new directory 2, checking to make sure it doesnt already exist
            os.mkdir(path3)
        except OSError:
            # print("Directory exists\n")
            return 1
        # else:
        #     print("Btemp made\n")
        self.consoleTableDecLabel.configure(fg='green')
        if testCancelled:
            runningTest = False
            testCancelled = False
            return
        tstartDec = time.time()
        bound = self.decomp(video, path, fps)  # decompiling video and getting the bound from it
        if testCancelled:
            runningTest = False
            testCancelled = False
            return
        tendDec = time.time()
        durationDec = tendDec - tstartDec
        newDecText = "Decompilation Console Data - Analysis Duration: " + str(time.strftime('%H:%M:%S', time.gmtime(durationDec)))
        self.consoleTableDecLabel.configure(fg='black', text=newDecText)


        if bound > 0:
            isDec = True
            # labelD = Label(self.FMenu, text="Decompiled: ")
            # labelD.grid(row=0, column=0)
            labelDstatus = Label(self.FMenu, text=" Success", fg="green", width=6)
            labelDstatus.grid(row=1, column=1)
            self.update_idletasks()
            self.update()
        self.consoleTableSubLabel.configure(fg='green')
        if testCancelled:
            runningTest = False
            testCancelled = False
            return
        tstartSub = time.time()
        bounding = self.initmult(bound, path, path2)
        if testCancelled:
            runningTest = False
            testCancelled = False
            return
        tendSub = time.time()
        durationSub = tendSub - tstartSub
        newSubText = "Subtraction Console Data - Analysis Duration: " + str(time.strftime('%H:%M:%S', time.gmtime(durationSub)))
        self.consoleTableSubLabel.configure(fg='black', text=newSubText)
        # labelS = Label(self.FMenu, text="Subtracted:  ")
        # labelS.grid(row=1, column=0)
        isSub = True
        labelSstatus = Label(self.FMenu, text=" Success", fg="green", width=6)
        labelSstatus.grid(row=2, column=1)
        self.update_idletasks()
        self.update()
        self.consoleTableBinLabel.configure(fg='green')
        if testCancelled:
            runningTest = False
            testCancelled = False
            return
        tstartBin = time.time()
        tendBin = self.plotTest(directory, current, bounding, path2, path3, fps)
        if testCancelled:
            runningTest = False
            testCancelled = False
            return
        durationBin = tendBin - tstartBin
        newBinText = "Binarization Console Data - Analysis Duration: " + str(time.strftime('%H:%M:%S', time.gmtime(durationBin)))
        self.consoleTableBinLabel.configure(fg='black', text=newBinText)
        # labelB = Label(self.FMenu, text="Binarized:  ")
        # labelB.grid(row=2, column=0)
        isBin = True
        labelBstatus = Label(self.FMenu, text=" Success", fg="green", width=6)
        labelBstatus.grid(row=3, column=1)
        self.update_idletasks()
        self.update()

        self.graphButton.configure(state="normal")
        self.tableButtonOnMenu.configure(state="normal")
        self.decVidButton.configure(state="normal")
        self.subVidButton.configure(state="normal")
        self.binVidButton.configure(state="normal")
        self.framesButtonOnMenu.configure(state="normal")
        self.processButton.configure(text="Perform Test")
        if testCancelled:
            runningTest = False
            testCancelled = False
            return
        runningTest = False
        testCancelled = False
        analysisTime = durationDec + durationSub + durationBin
        # if showingFrames:
        #     self.showOrHideFrames()
        #     self.showOrHideFrames()
        # else:
        #     self.showOrHideFrames()
        self.programLoadingBar['value'] = self.programLoadingBar['maximum']
        self.programLoadingBar.update()
        self.update_idletasks()
        self.update()
        self.loadAfflictTable()
        self.loadFrameVisuals()
        cropped = False
        vcount+=1
        # self.showOrHideAllTables()

    def goBack(self):
        global goingBack
        global startingPage
        global vcount
        vcount = 0
        if tk.messagebox.askokcancel("Exit Project", "Are you sure you want to exit the project? If you exit, you have to start a new project to continue experimentation."):
            goingBack = True
            startingPage = StartingPage()
            startingPage.mainloop()
        else:
            return

class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        global x_start, y_start, x_end, y_end
        global video
        global path
        global vcount
        global activityPage
        global screen_width
        global screen_height
        global resizePercentage
        global num
        global app
        global cropped
        cropped = True
        self.title("Cursor selects region. Close when done.")
        self.wm_iconbitmap('download.ico')
        if vcount > 0:
            activityPage.cropButton.configure(fg = 'green')
        print('video')
        cap = cv2.VideoCapture(video)
        x_end = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        y_end = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print("Ex.app: x_end = "+ str(x_end) + " y_end = " + str(y_end))
        if(x_end > y_end):
            resizePercentage = (600/x_end) * 100
        elif(x_end <= y_end):
            resizePercentage = (600/y_end) * 100

        # if(x_end > 1000 or y_end > 1000):
        #     resizePercentage = 50
        # elif(x_end > 700 or y_end > 700):
        #     resizePercentage = 70

        while (cap.isOpened()):
            ret, frame = cap.read()
            screen_width = int(frame.shape[1] * resizePercentage / 100)
            screen_height = int(frame.shape[0] * resizePercentage / 100)
            dsize = (screen_width, screen_height)
            resized = cv2.resize(frame, dsize)
            frame = cv2.imwrite(path + "/frame0.png", resized)
            # print("frame read")
            # print("poopy")
            break
        cap.release()
        x_end = screen_width
        y_end = screen_height

        self.x = self.y = 0
        self.canvas = tk.Canvas(self, width=screen_width, height=screen_height, cursor="cross")
        self.canvas.pack(side="top", fill="both", expand=True)


        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)





        self.rect = None

        self.x_start = None
        self.y_start = None
        self.curX = None
        self.curY = None

        self._draw_image()
        messagebox.showinfo(title="Instructions", message = 'Select ROI with the cursor. Close window when satisfied or simply close out without changing in order to keep original.')
        # if num > 1:
        #     self.canvas.unbind("<ButtonPress-1>")
        #     self.canvas.bind("<ButtonPress-1>", self.delete_rect)
        # else:
        #
        #     num = 3


    def _draw_image(self):
        global num
        self.im = Image.open(path + "/frame0.png")
        self.tk_im = ImageTk.PhotoImage(self.im)
        self.canvas.create_image(0,0,anchor="nw",image=self.tk_im)
        print('image opened')

    def delete_rect(self):
        global rectExists
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        self.canvas.delete(self.rect)
        rectExists = False
        return num


    def on_button_press(self, event):
        global num
        global rectExists
        # save mouse drag start position
        # try:
        #     Canvas.delete(self.rect)
        #     print('crop again')
        # except:
        #     print('rectangle print')
        if rectExists:
            self.delete_rect()
        self.x_start = event.x
        self.y_start = event.y
        print ("x =" + str(self.x_start))

        # create rectangle if not yet exist
        #if not self.rect:
        self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline = "black", width = 2)
        rectExists = True

    def on_move_press(self, event):
        self.curX, self.curY = (event.x, event.y)
        print('we movin')
        # expand rectangle as you drag the mouse
        print ('first' + str(self.x_start))
        self.canvas.coords(self.rect, self.x_start, self.y_start, self.curX, self.curY)

    def on_button_release(self, event):
        global x_start, y_start, x_end, y_end
        x_start, y_start, x_end, y_end = self.x_start, self.y_start, self.curX, self.curY
        print('byee' + str(x_start) + str(y_start) + str(x_end) + str(y_end))
        pass

if __name__ == '__main__':
    if debug:
        activityPage = ActivityPage()
        activityPage.mainloop()
    else:
        startingPage = StartingPage()
        startingPage.mainloop()


    # from tkintertable import TableCanvas, TableModel
    # from tkinter import *
    # import random
    # from collections import OrderedDict
    #
    # # data = {'rec1': {'col1': 99.88, 'col2': 108.79, 'label': 'rec1'},
    # #        'rec2': {'col1': 99.88, 'col2': 321.79, 'label': 'rec3'},
    # #        'rec3': {'col1': 29.88, 'col2': 408.79, 'label': 'rec2'}
    # #        }
    #
    # from tkintertable.Testing import sampledata
    #
    # # data = sampledata()
    #
    #
    # # print(data)
    #
    # class TestApp(Frame):
    #     """Basic test frame for the table"""
    #
    #     def __init__(self, parent=None):
    #         self.parent = parent
    #         Frame.__init__(self)
    #         self.main = self.master
    #         self.main.geometry('800x500+200+100')
    #         self.main.title('Test')
    #         f = Frame(self.main)
    #         f.pack(fill=BOTH, expand=1)
    #         table = TableCanvas(f)#, data=data)
    #         table.importCSV('test.csv')
    #         print(table.model.columnNames)
    #         # table.model.data[1]['a'] = 'XX'
    #         # table.model.setValueAt('YY',0,2)
    #         table.show()
    #         return
    #
    #
    # app = TestApp()
    # app.mainloop()



##
##def bye():
##    Bob.place_forget()
##
##Bob = tk.Button(root, text="a", command = bye)
##Bob.place(x=100,y=5)
##
##root.mainloop()
##import sys
##import PyQt5 as QtGui
##
##
##def window():
##   app = QtGui.QApplication(sys.argv)
##   win = QtGui.QDialog()
##   b1 = QtGui.QPushButton(win)
##   b1.setText("Button1")
##   b1.move(50,20)
##   b1.clicked.connect(b1_clicked)
##
##   b2 = QtGui.QPushButton(win)
##   b2.setText("Button2")
##   b2.move(50,50)
##   QtGui.QObject.connect(b2,SIGNAL("clicked()"),b2_clicked)
##
##   win.setGeometry(100,100,200,100)
##   win.setWindowTitle("PyQt")
##   win.show()
##   sys.exit(app.exec_())
##
##def b1_clicked():
##   print ("Button 1 clicked")
##
##def b2_clicked():
##   print ("Button 2 clicked")
##
##if __name__ == '__main__':
##   window()