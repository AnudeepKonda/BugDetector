#!/usr/bin/python
#
# Parser for token and entropy files.
# Looks up and records tokens and entropies.
#
# Lance Simmons, November 2016

import csv  
import errno
import fnmatch
import os
import random
import sys
import time

# Seed rng
random.seed()


def createDirectory(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def main():

    # User specifies directory to find token files in with command line arg
    if (len(sys.argv) != 2):
        print("Please specify directory to search as second argument.")
        exit()

    # Recursively search directory for needed files
    directoryToSearch = sys.argv[1]

    tokenFilePaths = []
    for root, dirnames, filenames in os.walk(directoryToSearch):
        for filename in fnmatch.filter(filenames, '*.code.tokens'):
            tokenFilePaths.append(os.path.join(root, filename))

    entropyFilePaths = []
    for root, dirnames, filenames in os.walk(directoryToSearch):
        for filename in fnmatch.filter(filenames, '*.code.tokens.sentence.entropies'):
            entropyFilePaths.append(os.path.join(root, filename))

    tokenFilePaths.sort()
    entropyFilePaths.sort()

    # Sanity test printing paths
    # for index in range(0,len(tokenFilePaths)):
    #     print(tokenFilePaths[index])
    #     print(entropyFilePaths[index])
    #     print("\n")

    # Sanity test, ensure we have equal number of token files and entropy files
    if (len(tokenFilePaths) != len(entropyFilePaths)):
        print("Couldn't find even number of token and entropy files")
        exit()

    # Sanity test regarding the nature of entropy files
    for filePath in entropyFilePaths:
        fileHandler = open(filePath, 'r')

        lineNumbers = []
        for line in fileHandler:
            temp = int(line.split(',')[0]) # line number
            lineNumbers.append(temp)

        for index in range(0,len(lineNumbers)):
            if lineNumbers[index] == (index + 1):
                pass
                # print("ok")
            else:
                print("ERROR: Found index not matching line number")
                exit()


    # Sanity check counting lines
    for index in range(0,len(tokenFilePaths)):
        fileHandlerToken = open(tokenFilePaths[index], 'r')
        fileHandlerEntropy = open(entropyFilePaths[index], 'r')

        tokenLines = fileHandlerToken.readlines()
        entropyLines = fileHandlerEntropy.readlines()

        if (len(tokenLines) == len(entropyLines)):
            pass
            # print(len(tokenLines))
        else:
            print("ERROR: Mismatched line count between token and entropy files")
            exit()



    # Lists of names of files to use for training and testing
    tokenTrainSet = []
    tokenTestSet = []
    entropyTrainSet = []
    entropyTestSet = []


    # Select 20% of files to be used for training
    indicesOfTestSet = random.sample(range(len(tokenFilePaths)), len(tokenFilePaths)/5)

    for index in range(0,len(tokenFilePaths)):
        if index in indicesOfTestSet:
            tokenTestSet.append(tokenFilePaths[index])
            entropyTestSet.append(entropyFilePaths[index])
        else:
            tokenTrainSet.append(tokenFilePaths[index])
            entropyTrainSet.append(entropyFilePaths[index])

    # createDirectory("processedData")

    print(len(tokenTrainSet))
    print(len(tokenTestSet))
    print(len(entropyTrainSet))
    print(len(entropyTestSet))

    ## TRAINING SET
    fileHandlerWriter = open("trainingLinesWithEntropies.txt", 'w')
    for index in range(0,len(tokenTrainSet)):
        fileHandlerToken = open(tokenTrainSet[index], 'r')
        fileHandlerEntropy = open(entropyTrainSet[index], 'r')

        tokenLines = fileHandlerToken.readlines()
        entropyLines = fileHandlerEntropy.readlines()

        fileHandlerWriter.write("<START_FILE>\n")
        for lineIndex in range(0,len(tokenLines)):    
            tempLine = ""
            tempLine = tempLine + tokenLines[lineIndex]
            tempLine = tempLine.split('\n')[0]
            tempLine = ' '.join(tempLine.split())
            # append entropy scores
            tempLine = tempLine + " " + entropyLines[lineIndex].split(',')[1]
            fileHandlerWriter.write(tempLine)
        fileHandlerWriter.write("<END_FILE>\n")

    ## TESTING SET
    fileHandlerWriter = open("testingLinesWithEntropies.txt", 'w')
    for index in range(0,len(tokenTestSet)):
        fileHandlerToken = open(tokenTestSet[index], 'r')
        fileHandlerEntropy = open(entropyTestSet[index], 'r')

        tokenLines = fileHandlerToken.readlines()
        entropyLines = fileHandlerEntropy.readlines()

        fileHandlerWriter.write("<START_FILE>\n")
        for lineIndex in range(0,len(tokenLines)):    
            tempLine = ""
            tempLine = tempLine + tokenLines[lineIndex]
            tempLine = tempLine.split('\n')[0]
            tempLine = ' '.join(tempLine.split())
            # append entropy scores
            tempLine = tempLine + " " + entropyLines[lineIndex].split(',')[1]
            fileHandlerWriter.write(tempLine)
        fileHandlerWriter.write("<END_FILE>\n")

    exit()


if __name__ == "__main__":
    main()