import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt
import csv
import imgcompare as imgcmp
import time

threshold = 0.003

def test(image):
    count = 0
    height = image.shape[0]  # only working w/ one dimension
    width = image.shape[1]
    for i in range(height):
        for j in range(width):
            if np.greater(image[i, j], [50, 50, 50]).all():  # image color should be brighter than [50,50,50]
                print("Afflicted at: " + str(i) + ", " + str(j))  # point where dendrite is located
                print("Value: " + str(image[i, j]))
                print("\n")
                count += 1
    count /= (height * width)
    return count

def timeTest(bounding, pathing):  # gives a range of percent formations
    for i in range(bounding):
        im = cv2.imread(pathing + "/sframe" + str(i) + ".jpg")  # load indicated file
        print("Frame difference " + str(i + 1))  # the amt btwn this frame and first frame
        percent = test(im) * 100  # amt. of shapes / total area * 100
        print("Percent of afflicted pixels in subtract: " + str(percent))
        # repeats multiple times for each occurance
        if percent >= threshold:
            print("Dendrite formation starts between frames " + str(i) + " and " + str(
                i + 5))  # checks frame and 5 after frame
            cv2.imwrite("multp-subtract.jpg", im)
            break
        if i == bounding - 5:
            print("No formation dedected.\n")
            break


def iTimeTest(bounding, pathing):
    for i in range(bounding):
        im = cv2.imread(pathing + "/isframe" + str(i) + ".jpg")
        print("Frame difference with initial " + str(i + 1))
        percent = test(im) * 100
        print("Percent of afflicted pixels in subtract: " + str(percent))
        if percent >= threshold:  # that is when it is of significant size
            print("Dendrite formation starts at frame " + str(i))
            cv2.imwrite("multp-subtract-init.jpg", im)
            break
        elif i == bounding - 2:  # ?
            print("No formation dedected.\n")
            break


def plotTest(directory, currentfile, bounding, subpathing, binpathing, framerate):
    global fps
    fps = framerate
    x = []
    y = []
    afflictFile = open(directory + "/" + str(fps) + "FPS AfflictData.csv", "w+")
    afflictFile.write("Time(M),%Change, Af-Area(mm^2)\n")
    imi = str(subpathing) + "/isframe0.jpg"
    imiread = cv2.imread(imi)
    imireadGrayscale = cv2.cvtColor(imiread, cv2.COLOR_BGR2GRAY)
    retval, binarizedimi = cv2.threshold(imireadGrayscale, 75, 255, cv2.THRESH_BINARY)#+cv2.THRESH_OTSU)
    cv2.imwrite(str(binpathing) + "/binarizedimi0.jpg", binarizedimi)
    binarizedimipath = str(binpathing) + "/binarizedimi0.jpg"
    w = 0;
    for i in range(bounding):
        im = str(subpathing) + "/isframe" + str(i) + ".jpg"
        print("Frame difference with initial " + str(i + 1))
        imread = cv2.imread(im)
        imreadGrayscale = cv2.cvtColor(imread, cv2.COLOR_BGR2GRAY)
        retval, binarizedim = cv2.threshold(imreadGrayscale, 75, 255, cv2.THRESH_BINARY)#+cv2.THRESH_OTSU)
        cv2.imwrite(str(binpathing) + "/binarizedim" + str(i) + ".jpg", binarizedim)
        binarizedimpath = str(binpathing) + "/binarizedim" + str(i) + ".jpg"
        percent = imgcmp.image_diff_percent(binarizedimpath, binarizedimipath)
        print("Percent of afflicted pixels in subtract: " + str(percent))
        x.append((i / (fps))/60)  # points on xaxis##########################################
        afflictFile.write(str((i / (fps))/60) + ",")#########################################
        if percent >= threshold:
            y.append(percent)
            afflictFile.write(str(percent) + "," + str(percent / 100.0 * 0.485) +"\n")
            print("Appended percent.")
            if w == 0:
                w = percent
            x[i] -= w
        else:
            y.append(0)
            afflictFile.write("0,0\n")
            print("Appended 0.")
    afflictFile.close()
    ##    plt.plot(x, y)
    ##    plt.xlabel('Time (secs)')#.1,.2,.3,etc.
    ##    plt.ylabel('% area covered')
    ##    plt.axis([0, bounding/10, 0, 0.5])
    ##    plt.show()

    current = currentfile

    data1x = x
    data1y = y

    fig, ax1 = plt.subplots()
    ax1.set_title("% Area Change vs Current vs Time", fontweight='bold')

    red = 'tab:red'
    ax1.set_xlabel('Time (Min)', fontweight='bold', labelpad=10)
    ax1.set_ylabel('% Area Covered', color=red, fontweight='bold', labelpad=10)
    ax1.plot(data1x, data1y, color=red)
    ax1.tick_params(axis='y', labelcolor=red, color=red)
    for tick in ax1.xaxis.get_major_ticks():
        tick.label1.set_fontweight('bold')
    for tick in ax1.yaxis.get_major_ticks():
        tick.label1.set_fontweight('bold')

    ax2 = ax1.twinx()

    data2x = []
    data2y = []
    with open(current) as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        for row in reader:
            try:
                data2x.append(float(row[0]))
            except:
                pass
            try:
                data2y.append(float(row[1]) * 1000000)
            except:
                pass

    blue = 'tab:blue'
    ax2.set_ylabel('Current (μA)', color=blue, fontweight='bold',
                   labelpad=10)  # we already handled the x-label with ax1
    ax2.plot(data2x, data2y, color=blue)
    ax2.tick_params(axis='y', labelcolor=blue, color=blue)
    for tick in ax2.yaxis.get_major_ticks():
        tick.label2.set_fontweight('bold')
    for tick in ax2.xaxis.get_major_ticks():
        tick.label2.set_fontweight('bold')

    fig.tight_layout()
    tend1 = time.time()
    # plt.show()
    plt.savefig(directory + "/" + str(fps) + " Graph.jpg")
    return tend1


##    with open(current) as f:
##        reader = csv.reader(f, delimiter=',', quotechar='"')
##        rowNum = 0
##        for row in reader:
##            try:
##                x2.append(float(row[4]))
##            except ValueError:
##                pass
##            try:
##                y2.append(float(row[2]))
##            except ValueError:
##                pass
##            rowNum+=1
##
##    fig, ax1 = plt.subplots()
##    fig.subplots_adjust(right=0.75)
##    plt.xlabel('Time (secs)')
##
##    ax2 = ax1.twinx()
##    p1, = ax1.plot(x, y, "b-", label="% area covered")
##    p2, = ax2.plot(x2, y2, "r-", label="Current")
##    lines = [p1, p2]
##    ax1.legend(lines, [l.get_label() for l in lines])
##    plt.show()


def color(userInp):  # can perform function on imput of choice
    im = cv2.imread(userInp)
    output = test(im)
    print("Percent of afflicted pixels: " + str(100 * output))  #


if __name__ == "__main__":
    userInput = input("File to color test: ")
    color(userInput)