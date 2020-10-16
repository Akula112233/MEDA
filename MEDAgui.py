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
decText = []#["hello\n" for i in range(30)]
subText = []
binText = []
vidFramesCount = 0
testCancelled = False
runningTest = False


class StartingPage(Tk):
    def __init__(self):
        super(StartingPage, self).__init__()
        self.initializePage()

    def initializePage(self):
        global goingBack

        self.title("MEDA")
        self.minsize(450,130)
        #self.wm_iconbitmap('icon.ico')

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
            activityPage.protocol("WM_DELETE_WINDOW", activityPage.destroy)
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

class ActivityPage(Tk):
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
        if not debug:
            video = startingPage.entryVideo.get()
            print("Video Path: " + str(video))
            current = startingPage.entryCurrent.get()
            print("Current Path: " + str(current))
            directory = startingPage.entryDirectory.get()
            print("Directory Path: " + str(directory))
            # print(video)
            startingPage.destroy()
        self.title("MEDA")

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
        self.FVideoEditor.grid(column=2, row=0, padx=10, pady=10)
        self.FMenu = ttk.Frame(self)
        self.FMenu.grid(column=0, row=0, sticky="N", ipady=75)

        backButton = Button(self.FMenu, text="Exit Project", command=self.goBack)
        backButton.grid(row=0, column=0, ipadx=10, pady=5, sticky='NW')

        self.fpsEntryLabel = Label(self.FMenu, text="FPS:")
        self.fpsEntryLabel.grid(row=4, column=0, sticky="NW")
        self.fpsEntry = ttk.Entry(self.FMenu, width=6)
        self.fpsEntry.grid(row=4, column=1, sticky="NW")
        self.fpsEntry.delete(0, END)
        self.fpsEntry.insert(0, fps)

        self.thresholdEntryLabel = Label(self.FMenu, text="Threshold:")
        self.thresholdEntryLabel.grid(row=5, column=0, sticky="NW")
        self.thresholdEntry = ttk.Entry(self.FMenu, width=6)
        self.thresholdEntry.grid(row=5, column=1, sticky="NW")
        self.thresholdEntry.delete(0, END)
        self.thresholdEntry.insert(0, threshold)

        self.processButton = Button(self.FMenu, text="Perform Test", command=self.percentChange, width=19)
        self.processButton.grid(row=6, column=0, columnspan=2, sticky="NW")
        self.graphButton = Button(self.FMenu, text=" Show Graph", command=self.showOrHideGraph, state="disabled", width=19)
        self.graphButton.grid(row=7, column=0, columnspan=2, sticky="NW")
        self.tableButtonOnMenu = Button(self.FMenu, text=" Show Tables", state="disabled", width=19)
        self.tableButtonOnMenu.grid(row=8, column=0, columnspan=2, sticky="NW")
        self.subVidButton = Button(self.FMenu, text="Subtracted Video", command=self.createSubVideo, state="disabled", width=19)
        self.subVidButton.grid(row=9, column=0, columnspan=2, sticky="NW")
        self.binVidButton = Button(self.FMenu, text=" Binarized Video ", command=self.createBinVideo, state="disabled", width=19)
        self.binVidButton.grid(row=10, column=0, columnspan=2, sticky="NW")

        self.allStatusFalse()

        self.applyButton = Button(self.FVideoEditor, text="Apply & Save", command=self.printTest)
        self.applyButton.grid(row=1, column=0)

        self.FGraph = ttk.Frame(self.LFMeda)
        if debug or True:
            self.FGraph.grid(row=0, column=1)

        self.FTables = ttk.Frame(self.LFMeda)
        if debug:
            self.FTables.grid(row=0, column=0, sticky="NS", rowspan=2)

        self.FAfflictTable = ttk.Frame(self.FTables)
        self.FAfflictTable.grid(column=0, row=1, padx=10, pady=10, sticky="NW")

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

        self.tableButtonOnMenu.configure(command=self.showOrHideAllTables)

        if debug or (isDec and isSub and isBin):
            self.loadAfllictTable()
            # self.loadConsoleTable()
            # self.consoleTableDec.configure(state="disabled")

    def printTest(self):
        print("This Works in Between")

    def cancelPerformTest(self):
        global testCancelled
        global runningTest
        self.processButton.configure(text="Perform Test")
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

    def loadAfllictTable(self):
        global showingTables
        afflicDataTableModel = TableModel()
        if debug:
            afflicDataTableModel.importCSV("D:\\TAMS Stuff\\TAMS Research\\Dr. Chyan Lab\\TAMS Summer Research 2020\\MEDA\\FPS Testing\\Sample 1 TI Device\\S1 Reg B\\Results\\15FPM\\0.25FPS AfflictData.csv", sep=",")
        else:
            print(directory + "/" + str(fps) + "FPS AfflictData.csv")
            afflicDataTableModel.importCSV(directory + "/" + str(fps) + "FPS AfflictData.csv")
        self.afflictTable = TableCanvas(self.FAfflictTable, model=afflicDataTableModel, rowheaderwidth=0, read_only=True, cols=3, height=865, width=384)
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

        if not (isDec or isSub or isBin):
            self.programLoadingBar = ttk.Progressbar(self.FConsoleTable, orient="horizontal", length=415, mode="determinate")
            if not debug:
                vidFramesCount = fps * mp.VideoFileClip(video).duration
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
            "hello"

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
            "hello"
        self.FAfflictTable.grid(row=1, column=0)
        self.showAfflictTableButton.configure(state="disabled")
        self.showConsoleDataTableButton.configure(state="normal")

    def showOrHideGraph(self):
        global showingGraph
        if showingGraph:
            self.FGraph.grid_remove()
            self.graphButton.configure(text="Show Graph")
            showingGraph = False
        else:
            self.FGraph.grid(row=0, column=1, sticky="EW")
            self.LFMeda.grid_columnconfigure(1, weight=5, minsize=480)
            self.LFMeda.grid_rowconfigure(0, weight=1, minsize=320)
            self.graphButton.configure(text="Hide Graph")
            showingGraph = True

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
        else:
            text = "/binarizedim"
            saveText = "FPS BinarizedFramesVideo.mp4"
        img = cv2.imread(pathing + text + str(iFrame) + ".jpg")
        # height, width, layers = img.shape
        height = img.shape[0]
        width = img.shape[1]
        size = (width, height)
        out = cv2.VideoWriter(directory + "/" + str(fps) + saveText, cv2.VideoWriter_fourcc(*'MP4V'), fps, size)  # need to change##############################
        for i in range(iFrame+1, bound):  # for all the frames
            img = cv2.imread(pathing + text + str(i) + ".jpg")
            out.write(img)
        out.release()

    def createSubVideo(self):
        print(path2 + "/*.jpg")
        bound = glob.glob(path2 + "/*.jpg")  # creating an array of all the new frames' names
        self.buildUp(bound, path2, directory)  # building up a new video using the frames' names array and file path

    def createBinVideo(self):
        print(path3 + "/*.jpg")
        bound = glob.glob(path3 + "/*.jpg")  # creating an array of all the new frames' names
        self.buildUp(bound, path3, directory)  # building up a new video using the frames' names array and file path

    def breakDown(self, video, pathing, sec, num):  # function to check if video file still has frames
        global decText
        video.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)  # set the video to the position in milliseconds (sec*1000)
        hasFrames, image = video.read()  # set hasFrames and image to get if video has frames, and then reading in image
        if hasFrames:  # if the video has a frame, then write it to a file named "frame#" where # is the frame number
            cv2.imwrite(pathing + "/frame%d.jpg" % num, image)
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
        fps = framerate
        count = 0  # frame counting variable
        # userInp = input("Full video file path: ")  # Getting file name and path for video to be analyzed
        # print("Video from decomp function: " + str(video))
        if video == "cancel":  # leaving program if userinput is to cancel
            return -1
        vidFile = cv2.VideoCapture(video)  # reading in video file
        sec = 0  # time elapsed
        # fps = 1  # 10 frame -> 1 sec, means 1 frame -> 0.1 sec#####################################
        frameRate = 1.0 / fps
        success = self.breakDown(vidFile, pathing, sec, count)  # getting success bool from breakdown function (for first frame)
        while success:  # looping while video has more frames to break down into
            if testCancelled:
                return -1
            count += 1  # incrementing frame count
            sec = sec + frameRate  # incrementing seconds counter by frameRate
            sec = round(sec, 2)  # rounds the seconds to the nearest 2nd decimal (why do we need this?)
            success = self.breakDown(vidFile, pathing, sec, count)  # calling breakDown function again (for next frame)
        return count - 1  # returning total frames in video

    def changeLineOnGraph(self, xpos):
        self.currentLocationLine.set_data([xpos, xpos], [min(self.data2y), max(self.data2y)])
        self.canvas.draw()
        self.update_idletasks()
        self.update()

    def on_click(self, event):
        if event.inaxes is not None and event.xdata >= 0 and event.xdata <= max(self.data2x):
            self.changeLineOnGraph(event.xdata)
            # plt.axvline(x=event.xdata, color='green')
            # print(plt.vlines)
            # print(plt.axes)
            # print(event.xdata, event.ydata)
        # else:
        #     # print('Clicked ouside axes bounds but inside plot window')

    def loadGraph(self):
        "hello"

    def plotTest(self, directory, currentfile, bounding, subpathing, binpathing, framerate):
        global fps
        global threshold
        global binText
        fps = framerate
        x = []
        y = []
        afflictFile = open(directory + "/" + str(fps) + "FPS AfflictData.csv", "w+")
        afflictFile.write("Time(M),%Change, Af-Area(mm^2)\n")
        imi = str(subpathing) + "/isframe0.jpg"
        imiread = cv2.imread(imi)
        imireadGrayscale = cv2.cvtColor(imiread, cv2.COLOR_BGR2GRAY)
        retval, binarizedimi = cv2.threshold(imireadGrayscale, 75, 255, cv2.THRESH_BINARY)  # +cv2.THRESH_OTSU)
        cv2.imwrite(str(binpathing) + "/binarizedimi0.jpg", binarizedimi)
        binarizedimipath = str(binpathing) + "/binarizedimi0.jpg"
        w = 0
        for i in range(bounding):
            if testCancelled:
                return -1
            im = str(subpathing) + "/isframe" + str(i) + ".jpg"
            # print("Frame difference with initial " + str(i + 1))
            imread = cv2.imread(im)
            imreadGrayscale = cv2.cvtColor(imread, cv2.COLOR_BGR2GRAY)
            retval, binarizedim = cv2.threshold(imreadGrayscale, 75, 255, cv2.THRESH_BINARY)  # +cv2.THRESH_OTSU)
            cv2.imwrite(str(binpathing) + "/binarizedim" + str(i) + ".jpg", binarizedim)
            binarizedimpath = str(binpathing) + "/binarizedim" + str(i) + ".jpg"
            percent = imgcmp.image_diff_percent(binarizedimpath, binarizedimipath)
            # print("Percent of afflicted pixels in subtract: " + str(percent))
            x.append((i / (fps)) / 60)  # points on xaxis##########################################
            afflictFile.write(str((i / (fps)) / 60) + ",")  #########################################
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
        ax1.set_title("% Area Change vs Current vs Time", fontweight='bold')

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
                    self.data2x.append(float(row[0]))
                except:
                    pass
                try:
                    self.data2y.append(float(row[1]) * 1000000)
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
        self.fig.set_dpi(150)
        self.fig.tight_layout()
        tend1 = time.time()
        # plt.show()
        plt.savefig(directory + "/" + str(fps) + " Graph.jpg")
        # plt.grid()
        # plt.gcf().canvas.draw()
        # self.fig = plt.figure()
        # plt.axvline(x=20)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.FGraph)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # self.fig.canvas.callbacks.connect('button_press_event', self.on_click)
        self.fig.canvas.callbacks.connect('button_release_event', self.on_click)
        # self.fig.canvas.callbacks.connect('motion_notify_event', self.on_click)



        self.currentLocationLine, v = plt.plot(0, 0, min(self.data2y), max(self.data2y), color='red', linewidth=2)

        toolbar = NavigationToolbar2Tk(self.canvas, self.FGraph)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        if showingGraph:
            self.showOrHideGraph()
            self.showOrHideGraph()
        else:
            self.showOrHideGraph()
        return tend1

    def initmult(self, bounder, pathing1,
                 pathing2):  # subtracts initial image from each frame and makes that many subtracted ones, makes bound and returns the value
        global subText
        global testCancelled
        count = 0
        for i in range(bounder):
            if testCancelled:
                return -1
            im1 = cv2.imread(pathing1 + "/frame0.jpg")  # image 1
            im2 = cv2.imread(pathing1 + "/frame" + str(i) + ".jpg")  # image 2
            polaroid = cv2.subtract(im1, im2)  # subtracting each image
            cv2.imwrite(pathing2 + "/isframe%d.jpg" % count, polaroid)  # writing to new
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

        if runningTest:
            self.cancelPerformTest()
            return

        runningTest = True
        self.processButton.configure(text="Cancel Test")
        self.tableButtonOnMenu.configure(state="disabled")
        self.graphButton.configure(state="disabled")
        decText = []
        subText = []
        binText = []
        fps = float(self.fpsEntry.get())
        threshold = float(self.thresholdEntry.get())
        self.allStatusFalse()
        self.loadConsoleTable()

        if testCancelled:
            runningTest = False
            testCancelled = False
            return

        if showingGraph:
            self.showOrHideGraph()
            self.FGraph.destroy()
            self.FGraph = ttk.Frame(self.LFMeda)
        if showingTables:
            self.showOrHideAllTables()
            self.showOrHideAllTables()
        else:
            self.showOrHideAllTables()
        try:  # removing directory 1 - clearing it of all past data
            sh.rmtree(path)
        except OSError:
            print("No tmp folder found. Will create now.\n")
        # else:
        #     print("Removed tmp folder previously.\n")
        try:  # removing directory 2 - clearing it of all past frames
            sh.rmtree(path2)
        except OSError:
            print("No stmp folder found. Will create now.\n")
        # else:
        #     print("Removed stmp folder previously.\n")
        try:  # removing directory 2 - clearing it of all past frames
            sh.rmtree(path3)
        except OSError:
            print("No btmp folder found. Will create now.\n")
        # else:
        #     print("Removed btmp folder previously.\n")
        try:  # making new directory 1, checking to make sure it doesn't already exist
            os.mkdir(path)
        except OSError:
            print("Directory exists\n")
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
            print("Directory exists\n")
            return 1
        # else:
        #     print("Btemp made\n")
        self.consoleTableDecLabel.configure(fg='green')
        if testCancelled:
            runningTest = False
            testCancelled = False
            return
        bound = self.decomp(video, path, fps)  # decompiling video and getting the bound from it
        if testCancelled:
            runningTest = False
            testCancelled = False
            return
        self.consoleTableDecLabel.configure(fg='black')
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
        bounding = self.initmult(bound, path, path2)
        if testCancelled:
            runningTest = False
            testCancelled = False
            return
        self.consoleTableSubLabel.configure(fg='black')
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
        tend1 = self.plotTest(directory, current, bounding, path2, path3, fps)
        if testCancelled:
            runningTest = False
            testCancelled = False
            return
        self.consoleTableBinLabel.configure(fg='black')
        # labelB = Label(self.FMenu, text="Binarized:  ")
        # labelB.grid(row=2, column=0)
        isBin = True
        labelBstatus = Label(self.FMenu, text=" Success", fg="green", width=6)
        labelBstatus.grid(row=3, column=1)
        self.update_idletasks()
        self.update()

        self.graphButton.configure(state="normal")
        self.tableButtonOnMenu.configure(state="normal")
        self.subVidButton.configure(state="normal")
        self.binVidButton.configure(state="normal")
        self.processButton.configure(text="Perform Test")
        if testCancelled:
            runningTest = False
            testCancelled = False
            return
        runningTest = False
        testCancelled = False
        self.loadAfllictTable()
        # self.showOrHideAllTables()

    def goBack(self):
        global goingBack
        global startingPage
        if messagebox.askokcancel("Exit Project", "Are you sure you want to exit the project? If you exit, you have to start a new project to continue experimentation."):
            goingBack = True
            startingPage = StartingPage()
            startingPage.mainloop()
        else:
            return

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