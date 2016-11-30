#!/usr/bin/python
#
# This script will be used to pre-process a file, replacing rare tokens with rare token flag
#
# Lance Simmons, November 2016

import csv     # imports the csv module
import sys      # imports the sys module
import time


## PARAMETERS

# Defines which tokens are considered 'rare'
# Tokens occuring this many times or fewer will be replaced with the rare token id
rareTokenFlag = "<RARE_TOKEN>"

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
        print "LINE:"
        print line,
        splitLine = line.split()

        tempKey = splitLine[0]
        tempValue = splitLine[1]

        tokensDictionary[tempKey] = tempValue

    fileHandlerTokenDictionary.close()

    # for element in tokensDictionary:
    #     print element,
    #     print " ",
    #     print tokensDictionary[element]


    # if "<RARE_TOKEN>" in tokensDictionary:
    #     print "Oh good!"
    # if "INVALID TOKEN" in tokensDictionary:
    #     print "Error"


    # Create a file handler for output file
    fileHandlerOutput = open("tokenLinesRaresReplaced.txt", 'w')


    for line in fileHandlerTokens:
        splitLine = line.split()
        for element in splitLine:
            if element not in tokensDictionary:
                element = "<RARE_TOKEN>"
            fileHandlerOutput.write(element + " ")
        fileHandlerOutput.write("\n")

    exit()



if __name__ == "__main__":
    main()