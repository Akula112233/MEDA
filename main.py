###Main Program File - Brings together all 3 sub-files: (decompiling, subtracting, and graph making)
mainStoreFolder = "D:\TAMS Stuff\TAMS Research\Dr. Chyan Lab\All Runs Data"


#importing libraries
import testColor as tc
import subtract as sub
import decompileVideo as dec
import os#used for dealing with file directories (making)
import shutil as sh#also dealing with file directories (removing)
import glob#dealing with getting all files within directory
import time

path = "tmp"#directory 1
path2 = "stmp"#directory 2
path3 = "btmp"
def run():
    decompiled = False#variable to check if video has been decompiled
    try:#removing directory 1 - clearing it of all past data
        sh.rmtree(path)
    except OSError:
        print("No tmp folder found. Will create now.\n")
    else:
        print("Removed tmp folder previously.\n")
    try:#removing directory 2 - clearing it of all past frames
        sh.rmtree(path2)
    except OSError:
        print("No stmp folder found. Will create now.\n")
    else:
        print("Removed stmp folder previously.\n")
    try:#removing directory 2 - clearing it of all past frames
        sh.rmtree(path3)
    except OSError:
        print("No btmp folder found. Will create now.\n")
    else:
        print("Removed btmp folder previously.\n")
    try:#making new directory 1, checking to make sure it doesn't already exist
        os.mkdir(path)
    except OSError:
        print("Directory exists\n")
        return 1
    else:
        print("Temp made\n")
    try:#making new directory 2, checking to make sure it doesnt already exist
        os.mkdir(path2)
    except OSError:
        print("Directory exists\n")
        return 1
    else:
        print("Stemp made\n")
    try:#making new directory 2, checking to make sure it doesnt already exist
        os.mkdir(path3)
    except OSError:
        print("Directory exists\n")
        return 1
    else:
        print("Btemp made\n")
    while True:#main program to loop through
        #printing all analysis options
        print("Analysis to be done? Type number by option:\n")
        print("1. First and last frame subtraction.")
        print("2. Find initial time of dendrite formation through frame-frame subtraction.")
        print("3. Find initial time of dendrite formation through initial frame subtraction.")
        print("4. Plot percentages against frame data using threshold value.")
        if decompiled:#fifth option if video has been decompiled
            print("5. Video creation from decompiled dendrite formation.")
        print("0. Quit program.")#option for quitting program
        userInput = input("Selection:")
        if int(userInput) == 1:#calling subtraction of first and last frame
            lastNum = dec.decomp(path)#returns the number of frames and stores into lastNum
            polaroid = sub.fandl(0, lastNum, path)#makes a subtracted image of the first and last images
            tc.color(polaroid)#prints out percent of afflicted pixels (dendrites) in first and last frame
        elif int(userInput) == 2:#Finding initial time of dendrite formation using frame-frame subtraction
            bound = dec.decomp(path)#getting total frames and decompiling video as well
            bound2 = sub.multract(bound, path, path2)#getting bound for all subtracted images, comparing each frame to 5 after it
            tc.timeTest(bound2, path2)#gives frame for where the major dendrite growth starts
        elif int(userInput) == 3:#Finding initial time of dendrite formation using initial frame subtraction
            bound = dec.decomp(path)#decompiling and getting bound
            if bound > 0:#checking if decompiled
                decompiled = True
            bound2 = sub.initmult(bound, path, path2)#making a new bound with all newly subtracted images, subtracting initial frame from each one
            tc.iTimeTest(bound2, path2)#same as timeTest, but with reference to original image rather than 5 earlier
        elif int(userInput) == 4:#plotting and making graph of percent changes (basically making the area graph?)
            tstart1 = time.time()
            bound = dec.decomp(path)#decompiling video and getting the bound from it
            if bound > 0:
                decompiled = True
            bound2 = sub.initmult(bound, path, path2)
            tend1 = tc.plotTest(bound2, path2, path3)#function to plot the area change
            duration1 = tend1-tstart1
            print("Affliction Computation Time: " + str(duration1) + " seconds.")
        elif int(userInput) == 5 and decompiled:
            tstart2 = time.time()
            bound = glob.glob(path3 + "/*.jpg")#creating an array of all the new frames' names
            dec.buildUp(bound, path3)#building up a new video using the frames' names array and file path
            tend2 = time.time()
            duration2 = tend2 - tstart2
            print("Recompilation Time: " + str(duration2) + " seconds.")
        elif int(userInput) == 0:#Option for quitting the program
            print("Quitting program.")
            break
        else:#option for defualt, just in case wrong input is given
            print("Unknown number input. Please try again.")
            continue#goes back to top of loop, (but not necessary bc it should happen anyway)
    try:#clearing up all data by removing the temporary folders created for the frames
        sh.rmtree(path)
        sh.rmtree(path2)
    except OSError:
        print("Directory(ies) failed to delete\n")
        return 2
    else:
        print("Cleaning up...\n")
        return 0

if __name__ == "__main__":#used for actually running (don't fully understand how)
    run()

