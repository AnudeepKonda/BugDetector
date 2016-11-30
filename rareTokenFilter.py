#!/usr/bin/python
#
# DEPRECATED? I don't remember if this is needed.
# I think dictionaryBuilder covers this functionality already
#
# This script can be used to pre-process a file, replacing rare tokens with rare token flag
# Assumes input: unprocessedTokensFile, dictionaryFile
#
# Lance Simmons, November 2016

import csv
import sys
import time


## PARAMETERS

def main():

    # open file of tokens
    try:
        fileHandlerTokens = open(sys.argv[1], 'r')
    except:
        print "Error: specify path to token file as argument 1"
        exit()

    # open file of dictionary
    try:
        fileHandlerTokenDictionary = open(sys.argv[2], 'r')
    except:
        print "Error: specify path to token dictionary file as argument 2"
        exit()


    # Read lines into dictionary
    tokensDictionary = {}

    for line in fileHandlerTokenDictionary:
        splitLine = line.split()

        tempKey = splitLine[0]
        tempValue = splitLine[1]

        tokensDictionary[tempKey] = tempValue

    fileHandlerTokenDictionary.close()


    # Read all the lines from file
    linesFromFile = fileHandlerTokens.readlines()
    fileHandlerTokens.close()

    # Create a file handler for output file
    fileHandlerOutput = open(sys.argv[1], 'w')

    for line in linesFromFile:
        splitLine = line.split()
        for element in splitLine:
            if element not in tokensDictionary:
                element = "<RARE_TOKEN>"
            fileHandlerOutput.write(element + " ")
        fileHandlerOutput.write("\n")

    print("File: " + str(sys.argv[1]) + " has had rare tokens replaced.")
    exit()

if __name__ == "__main__":
    main()