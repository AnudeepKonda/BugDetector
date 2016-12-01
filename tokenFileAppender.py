#!/usr/bin/python
#
# Search a directory and append all files with a
# given extension. Note that this was written in
# Windows, and is possibly not compatible with Unix.
#
# Lance Simmons, December 2016

import os
import sys
import random

# Seed rng
random.seed()

## PARAMETERS

START_FILE_TOKEN = "<START_FILE>"
END_FILE_TOKEN = "<END_FILE>"


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
        
        fileHandlerTrain.write(START_FILE_TOKEN + "\n")

        fileHandlerTemp = open(directoryName + "/" + fileName, "r")
        for line in fileHandlerTemp:
            # Delete consecutive and trailing whitespace
            line =' '.join(line.split())
            # Write line with newline char that was just stripped
            fileHandlerTrain.write(line + "\n")
        fileHandlerTemp.close()

        fileHandlerTrain.write(END_FILE_TOKEN + "\n")

    fileHandlerTrain.close()


    # Writing testing set file
    print("Writing testing set file")
    for fileName in testSet:

        fileHandlerTest.write(START_FILE_TOKEN + "\n")

        fileHandlerTemp = open(directoryName + "/" + fileName, "r")
        for line in fileHandlerTemp:
            # Delete consecutive and trailing whitespace
            line =' '.join(line.split())
            # Write line with newline char that was just stripped
            fileHandlerTest.write(line + "\n")
        fileHandlerTemp.close()

        fileHandlerTest.write(END_FILE_TOKEN + "\n")

    fileHandlerTest.close()


    # Open files for appending names of files in train, test sets
    fileHandlerTrainFileName = open("trainSet_FileNames.txt", 'w')
    fileHandlerTestFileName = open("testSet_FileNames.txt", 'w')

    for fileName in trainSet:
        fileHandlerTrainFileName.write(fileName + "\n")
    fileHandlerTrainFileName.close()

    for fileName in testSet:
        fileHandlerTestFileName.write(fileName + "\n")
    fileHandlerTestFileName.close()


if __name__ == "__main__":
    main()