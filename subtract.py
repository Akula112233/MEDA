#importing libraries
import numpy as np #not necessary here (I think)
import pandas as pd #not necessary here (I think)
import cv2

def subtract(image1, image2):#function for subtacting one image from the other, and then returning filename of subtacted image
    polaroid = cv2.subtract(image1, image2)
    cv2.imwrite("p-subtract.jpg", polaroid)
    print("Subtraction sucess\n")
    return "p-subtract.jpg"

def multract(bounder, pathing1, pathing2):#function for subtracting all frames with 5 ahead of them (excluding last 5)
    count = 0
    for i in range(bounder-4):#looping through all frames in bound-4 to subtract and write to new images
        im1 = cv2.imread(pathing1 + "/frame" + str(i) + ".jpg")#image 1
        im2 = cv2.imread(pathing1 + "/frame" + str(i+5) + ".jpg")#image 2 (5 files over)
        polaroid = cv2.subtract(im1, im2)#subtracting the two
        cv2.imwrite(pathing2 + "/sframe%d.jpg" % count, polaroid)#writing as new, subtracted image, in stemp directory
        count += 1#incrementing count of subtracted frames
        print("Frames " + str(i) + " and " + str(i+5) + " subtracted.")#display what frames were subtracted
    return count#return how many new, subtracted images were made

def initmult(bounder, pathing1, pathing2):#subtracts initial image from each frame and makes that many subtracted ones, makes bound and returns the value
    count = 0
    for i in range(bounder):
        im1 = cv2.imread(pathing1 + "/frame0.jpg")#image 1
        im2 = cv2.imread(pathing1 + "/frame" + str(i) + ".jpg")#image 2
        polaroid = cv2.subtract(im1, im2)#subtracting each image
        cv2.imwrite(pathing2 + "/isframe%d.jpg" % count, polaroid)#writing to new
        count += 1
        print("Initial frame and frame " + str(i) + " subtracted.")
    return count#returns how many of the newly subtracted images there are (isframe, not sframe, each are different)

def fandl(num1, num2, pathing):#function for reading in two image files (frames) and then subtracting and returning result
    im1 = cv2.imread(pathing + "/frame" + str(num1) + ".jpg")#read image 1
    im2 = cv2.imread(pathing + "/frame" + str(num2) + ".jpg")#read image 2
    file = subtract(im1, im2)#calling subtract functions on two frames
    return file#returning result

if __name__ == "__main__":#used for scripting (somehow?, need explanation)
    userInput1 = input("Number on first frame? ")
    userInput2 = input("Number on second frame? ")
    fandl(userInput1, userInput2, "tmp")