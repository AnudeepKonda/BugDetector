#!/usr/bin/python
#
# This script will be used to create a dictionary of tokens and a stats file.
# Also strips rare tokens.
#
# Lance Simmons, November 2016

import csv     # imports the csv module
import sys      # imports the sys module
import time


def main():

    # create python dictionary
    tokenDict = {}

    # open file of tokens to read from
    try:
        fileHandler = open(sys.argv[1], 'r')
    except:
        print "Error: specify path to token file as argument"
        exit()

    # Defines which tokens are considered 'rare'
    # Tokens occuring this many times or fewer will be replaced with the rare token id
    # Set to 0 to disable this feature
    rareTokenThreshold = 0

    if len(sys.argv) == 3:
        print("User set rareTokenThreshold: " + sys.argv[2])
        # User can specify alternate rareTokenThreshold
        rareTokenThreshold = int(sys.argv[2])
    else:
        print("rareTokenThreshold defaults to 0.")


    # Set dictionary name based on token file name
    dictionaryName = sys.argv[1]
    dictionaryName = dictionaryName.split(".")[0]
    statsFileName = dictionaryName + "_Stats.txt"
    dictionaryName += "_Dictionary.txt"

    print "Processing tokens..."
    iterator = 0
    # for line in reader obj
    for line in fileHandler:
        tokens = line.split()
        # Strip the last token from the line if it's an entropy score
        if tokens[0] not in ["<START_FILE>", "<END_FILE>"]:
            tokens = tokens[:-1]
        
        # for tokens in line
        for token in tokens:
            # if token in dictionary, add 1 to relevant index
            if token in tokenDict:               
                tokenDict[token] += 1
            # otherwise, add a new entry and set it to 1
            else:
                tokenDict[token] = 1

        iterator += 1
        if (iterator % 50000) == 0:
            print "Processing token line: " + str(iterator) + "\r",
            sys.stdout.flush()
    
    print "Processing token line: " + str(iterator)
    fileHandler.close()


    # once dictionary is assembled, write it to file
    print "Writing results to dictionary file"
    fileHandler = open(dictionaryName, 'w')
    for x in tokenDict:
        lineToPrint = str(x) + " " + str(tokenDict[x]) + "\n"
        fileHandler.write(lineToPrint)
    fileHandler.close()

    # read in all lines into a list
    fileHandler = open(dictionaryName, 'r')
    lines = fileHandler.readlines()
    fileHandler.close()

    # sort those lines
    fileHandler = open(dictionaryName, 'w')
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
        if ((int(item[1]) <= rareTokenThreshold) and (item[0] not in ["<START_FILE>", "<END_FILE>", "</a>", "<a>"])):
            item[0] = "<RARE_TOKEN>"
            totalRareTokens += int(item[1])
            uniquesConvertedToRares += 1
        else:
            fileHandler.write(item[0] + " " + item[1] + "\n")

    fileHandler.write("<RARE_TOKEN> " + str(totalRareTokens) + "\n")
    fileHandler.close()


    # data file, currently ununsed
    print "Writing token stats to stats file"
    fileHandler = open(statsFileName, 'w')

    # Now, write out total tokens collected
    fileHandler.write("<RARE_TOKEN> " + str(totalRareTokens) + "\n")
    fileHandler.write("<RARE_TOKEN_THRESHOLD> " + str(rareTokenThreshold) + "\n")
    fileHandler.write("<TOTAL_TOKENS_IN_FILE> " + str(totalTokensInFile) + "\n")
    fileHandler.write("<UNIQUE_TOKENS_IN_FILE> " + str(len(tokenDict)) + "\n")

    # This represents the number of distinct tokens we're considering after rare tokens
    # have been coalesced to the rare token tag
    fileHandler.write("<UNIQUE_TOKENS_IN_FILE_POST_REPLACING_RARES> " + str(len(splitlines) - uniquesConvertedToRares + 1) + "\n")

    fileHandler.close()


    ## Now, filter all rare tokens out of file
    # open file of tokens
    fileHandlerTokens = open(sys.argv[1], 'r')

    # open file of dictionary
    fileHandlerTokenDictionary = open(dictionaryName, 'r')

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
    
    filteredFileName = sys.argv[1][:-4] + "_NoRares.txt"
    filteredFileName2 = sys.argv[1][:-4] + "_NoRaresOrEntropies.txt"
    
    fileHandlerOutput = open(filteredFileName, 'w')
    fileHandlerOutput2 = open(filteredFileName2, 'w')

    for line in linesFromFile:
        splitLine = line.split()
        for element in splitLine[:-1]:
            if (element not in tokensDictionary) and (element not in ["<START_FILE>", "<END_FILE>", "</a>", "<a>"]):
                element = "<RARE_TOKEN>"
            fileHandlerOutput.write(element + " ")
            fileHandlerOutput2.write(element + " ")
        fileHandlerOutput.write(splitLine[-1] + "\n")
        if splitLine[-1] in ["<START_FILE>", "<END_FILE>"]:
            fileHandlerOutput2.write(splitLine[-1] + "\n")
        else:
            fileHandlerOutput2.write("\n")

    print("File: " + filteredFileName + " has had rare tokens replaced.")
    exit()







if __name__ == "__main__":
    main()