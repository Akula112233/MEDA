# function used for breaking down the

# importing libraries
import numpy as np  # not necessary here (I think)
import pandas as pd  # not necessary here (I think)
import cv2  # OpenCV Library
import matplotlib.pyplot as plt
import imageio as imio

def breakDown(video, pathing, sec, num):  # function to check if video file still has frames
    video.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)  # set the video to the position in milliseconds (sec*1000)
    hasFrames, image = video.read()  # set hasFrames and image to get if video has frames, and then reading in image
    if hasFrames:  # if the video has a frame, then write it to a file named "frame#" where # is the frame number
        cv2.imwrite(pathing + "/frame%d.jpg" % num, image)
        print('Read frame ' + str(num) + ' : ', hasFrames)  # printing if frame has been read
    return hasFrames  # return if there is actually a frame


def buildUp(bounding, pathing, directory):
    ##    initFrame = input("Intial frame of dendrite formation?")#getting initial frame from user input
    img_array = []  # array to stoer image files
    ##    iFrame = int(initFrame)#casting input of user to an int
    bound = len(bounding)-1  # returns length of the bounding
    iFrame = 0
    text=""
    saveText=""
    if "SubtractedFrames" in pathing:
        # print("Going here")
        text = "/isframe"
        saveText = "FPS SubtractedFramesVideo.mp4"
        bound += 1
    else:
        text = "/binarizedim"
        saveText = "FPS BinarizedFramesVideo.mp4"
    # print("Bounding: " + str(bound))
    for i in range(iFrame, bound):  # for all the frames
        # print("Opening Image: " + pathing + text + str(i) + ".jpg")
        img = cv2.imread(pathing + text + str(i) + ".jpg")
        #height, width, layers = img.shape
        height = img.shape[0]
        width = img.shape[1]
        size = (width, height)
        img_array.append(img)
    out = cv2.VideoWriter(directory + "/" + str(fps) + saveText, cv2.VideoWriter_fourcc(*'MP4V'), fps, size) # need to change##############################
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()


def remove50():
    inputPath = "stmp"
    outputPath = "sub50"
    for i in range(262):
        inImagePath = inputPath + "//isframe" + str(i) + ".jpg"
        pic = imio.imread(inImagePath)
        low = pic < 50
        pic[low] = 0
        outImagePath = outputPath + "//sub50" + str(i) + ".jpg"
        imio.imwrite(outImagePath, pic[:, :, 0])


def decomp(video, pathing, framerate):  # function called to break a video down into individual frames to count them up
    global fps
    fps = framerate
    count = 0  # frame counting variable
    #userInp = input("Full video file path: ")  # Getting file name and path for video to be analyzed
    # print("Video from decomp function: " + str(video))
    if video == "cancel":  # leaving program if userinput is to cancel
        return
    vidFile = cv2.VideoCapture(video)  # reading in video file
    sec = 0  # time elapsed
    #fps = 1  # 10 frame -> 1 sec, means 1 frame -> 0.1 sec#####################################
    frameRate = 1.0/fps
    success = breakDown(vidFile, pathing, sec, count)  # getting success bool from breakdown function (for first frame)
    while success:  # looping while video has more frames to break down into
        count += 1  # incrementing frame count
        sec = sec + frameRate  # incrementing seconds counter by frameRate
        sec = round(sec, 2)  # rounds the seconds to the nearest 2nd decimal (why do we need this?)
        success = breakDown(vidFile, pathing, sec, count)  # calling breakDown function again (for next frame)
    return count - 1  # returning total frames in video