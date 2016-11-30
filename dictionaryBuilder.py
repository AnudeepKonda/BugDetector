#!/usr/bin/python
#
# This script will be used to create a dictionary of tokens
#
# Lance Simmons, November 2016

import csv     # imports the csv module
import sys      # imports the sys module
import time


## PARAMETERS

# Defines which tokens are considered 'rare'
# Tokens occuring this many times or fewer will be replaced with the rare token id
rareTokenThreshold = 200

def main():

    # create python dictionary
    tokenDict = {}

    # open file of tokens
    try:
        fileHandler = open(sys.argv[1], 'r')
    except:
        print "Error: specify path to token file as argument"
        exit()

    # open file of tokens to read from
    # for line in reader obj
        # for tokens in line
            # if token in dictionary, add 1 to relevant index
            # otherwise, add a new entry and set it to 1

    print "Processing tokens..."
    iterator = 0
    for line in fileHandler:
        tokens = line.split()
        for token in tokens:
            if token in tokenDict:               
                tokenDict[token] += 1
            else:
                tokenDict[token] = 1

        iterator += 1
        if (iterator % 50000) == 0:
            print "Processing token line: " + str(iterator) + "\r",
            sys.stdout.flush()
    
    print "Processing token line: " + str(iterator)
    fileHandler.close()


    # once dictionary is assembled, write it to file
    print "Writing results to tokenCounts.txt file"
    fileHandler = open('tokenCounts.txt', 'w')
    for x in tokenDict:
        lineToPrint = str(x) + " " + str(tokenDict[x]) + "\n"
        fileHandler.write(lineToPrint)
    fileHandler.close()

    # read in all lines into a list
    fileHandler = open('tokenCounts.txt', 'r')
    lines = fileHandler.readlines()
    fileHandler.close()

    # sort those lines
    fileHandler = open('tokenCounts.txt', 'w')
    lines.sort()

    # split lines into tokens and counts
    splitlines = []
    for line in lines:
        tempSplitline = line.split()
        splitlines.append(tempSplitline)

    # start printing out tokens and their counts
    # rare tokens are tallied up and added at the end
    totalTokensInFile = 0
    totalRareTokens = 0
    uniquesConvertedToRares = 0
    for item in splitlines:
        totalTokensInFile += int(item[1])
        if (int(item[1]) <= rareTokenThreshold):
            item[0] = "<RARE_TOKEN>"
            totalRareTokens += int(item[1])
            uniquesConvertedToRares += 1
        else:
            fileHandler.write(item[0] + " " + item[1] + "\n")

    fileHandler.write("<RARE_TOKEN> " + str(totalRareTokens) + "\n")
    fileHandler.close()


    # data file, currently ununsed
    print "Writing token stats to tokenStats.txt file"
    fileHandler = open('tokenStats.txt', 'w')

    # Now, write out total tokens collected
    fileHandler.write("<RARE_TOKEN> " + str(totalRareTokens) + "\n")
    fileHandler.write("<TOTAL_TOKENS_IN_FILE> " + str(totalTokensInFile) + "\n")
    fileHandler.write("<UNIQUE_TOKENS_IN_FILE> " + str(len(tokenDict)) + "\n")

    # This represents the number of distinct tokens we're considering after rare tokens
    # have been coalesced to the rare token tag
    fileHandler.write("<UNIQUE_TOKENS_IN_FILE_POST_REPLACING_RARES> " + str(len(splitlines) - uniquesConvertedToRares + 1) + "\n")

    fileHandler.close()


if __name__ == "__main__":
    main()