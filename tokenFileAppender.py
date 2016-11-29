#
# Search a directory and append all files with a
# given extension. Note that this was written in
# Windows, and is probably not compatible with Unix.
# Lance Simmons, December 2016

import os
import sys
import random

# Seed rng
random.seed()

def main():
    # User specifies directory to find token files in with command line arg
    if (len(sys.argv) != 2):
        print("Please specify directory to append token files from as second argument.")
        exit()
    directoryName = sys.argv[1]

    # Lists of names of files to use for training and testing
    allFiles = []
    trainSet = []
    testSet = []

    # Gather all file names in dir
    for fileName in os.listdir(directoryName):
        if fileName.endswith(".code.tokens"):
            allFiles.append(fileName)

    # Shuffle list of filenames to build random test/train sets
    random.shuffle(allFiles)

    # Build lists of file names for train, test sets
    for iterator in range(0,len(allFiles)):
        # Take every Xth file for test set
        # Every 5th file maps to 80/20 test/train split
        if (iterator % 5 == 0):
            testSet.append(allFiles[iterator])
        else:
            trainSet.append(allFiles[iterator])

    print("Training Set Size: " + str(len(trainSet)))
    print("Testing Set Size:  " + str(len(testSet)))

    # Open files for appending tokens
    fileHandlerTrain = open("trainSet.txt", 'w')
    fileHandlerTest = open("testSet.txt", 'w')

    # Writing training set file
    print("Writing training set file")
    for fileName in trainSet:
        fileHandlerTemp = open(directoryName + "/" + fileName, "r")

        for line in fileHandlerTemp:
            fileHandlerTrain.write(line)
        fileHandlerTemp.close()
    fileHandlerTrain.close()

    # Writing testing set file
    print("Writing testing set file")
    for fileName in testSet:
        fileHandlerTemp = open(directoryName + "/" + fileName, "r")

        for line in fileHandlerTemp:
            fileHandlerTest.write(line)
        fileHandlerTemp.close()
    fileHandlerTest.close()


    # Open files for appending names of files in train, test sets
    fileHandlerTrainFileName = open("trainSetFileNames.txt", 'w')
    fileHandlerTestFileName = open("testSetFileNames.txt", 'w')

    for fileName in trainSet:
        fileHandlerTrainFileName.write(fileName + "\n")
    fileHandlerTrainFileName.close()

    for fileName in testSet:
        fileHandlerTestFileName.write(fileName + "\n")
    fileHandlerTestFileName.close()


if __name__ == "__main__":
    main()