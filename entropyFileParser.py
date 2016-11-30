#!/usr/bin/python
#
# Parser for entropy file.
# Looks up and records source lines, tokens, entropies, and bug flags.
#
# Lance Simmons, November 2016

import csv     # imports the csv module
import sys      # imports the sys module
import time

def main():

    ## Start reading in lines
    # Read in first line, then ignore it.
    #read in \buggy_year_data\entropies_1month\atmosphere.csv

    # keep lists of token and source lines
    tokenLinesList = []
    sourceLinesList = []
    entropyList = []
    isBuggyList = []


    fileHandler = open("buggy_year_data/entropies_1month/atmosphere.csv", 'rb') # opens the csv file # sys.argv[1]
    try:
        reader = csv.reader(fileHandler)  # creates the reader object
        reader.next() # drop the first line, it's just column names

        iterator = 0
        for row in reader:

            # get row contents
            projectName = row[0]
            snapshotDate = row[1]
            pathToFile = row[2]
            source_line = row[3]
            token_line = row[4]
            ast_type = row[5]
            entropy = row[6]
            is_bug = row[7]

            # print "- projectName:  " + projectName
            # print "- snapshotDate: " + snapshotDate
            # print "- pathToFile:   " + pathToFile
            # print "- source_line:  " + source_line
            # print "- token_line:   " + token_line
            # # print "- ast_type:     " + ast_type
            # print "- entropy:      " + entropy
            # print "- is_bug:       " + is_bug
            # print ""

            ## fetch the source lines from file
            fullPathName = "buggy_year_data/snapshots/" + projectName + "/" + str(snapshotDate) + "/" + pathToFile
            tempLines = open(fullPathName, 'r').readlines() # .read().splitlines() to get without newlines

            lineToGet = tempLines[int(source_line) - 1] # Dataset indices start from 1
            sourceLinesList.append(lineToGet)

            ## fetch the token lines from file
            fullPathName = "buggy_year_data/snapshots/" + projectName + "/" + str(snapshotDate) + "/" + pathToFile
            fullPathName = fullPathName[:-4] + "code.tokens" # strip "java", add tokens extension
            tempLines = open(fullPathName, 'r').readlines()

            lineToGet = tempLines[int(token_line) - 1] # Dataset indices start from 1
            tokenLinesList.append(lineToGet)

            ## record the entropy, bug flag
            entropyList.append(entropy)
            isBuggyList.append(is_bug)

            ## Print out lines and line details
            # print "Tokens:"
            # print tokenLinesList[iterator],
            # print "Source:"
            # print sourceLinesList[iterator],
            # print "Entropy:"
            # print entropyList[iterator]
            # print "Buggy Flag:"
            # print isBuggyList[iterator]
            # print ""

            iterator += 1
            # print iterator
            if (iterator % 1000) == 0:
                print iterator
    finally:
        fileHandler.close()      # closing

    fileHandler = open('tokenLines.txt', 'w')
    for item in tokenLinesList:
        fileHandler.write(item)
    fileHandler.close()

    fileHandler = open('sourceLines.txt', 'w')
    for item in sourceLinesList:
        fileHandler.write(item)
    fileHandler.close()

    fileHandler = open('entropy.txt', 'w')
    for item in entropyList:
        fileHandler.write(str(item) + "\n")
    fileHandler.close()

    fileHandler = open('bugFlag.txt', 'w')
    for item in isBuggyList:
        fileHandler.write(str(item) + "\n")
    fileHandler.close()



    fp = open("tokenLines.txt", "r")
    data = fp.readlines()

    #fp = open("tokensLines_25.txt")
    buf = [ ]
    one_big_line = ' '.join(data)
    data = one_big_line.split(' ')
    total_tokens = len(data)

    fp2 = open("tokenLines_100.txt", "w")
    count = 0
    while count < total_tokens-100:
        for i in range(0, 101):
            if data[count+i].find("\n") != -1:
                buf.append(data[count+i][:-1])
            else:
                buf.append(data[count+i])
        count = count + 100
        string_to_write = ' '.join(buf)
        fp2.write(string_to_write+'\n')
        #print(count)
        buf=[ ]
    fp2.close()
    fp.close()


    ## FIXME: Use this to simplify process?

    # fp = open("tokenLines.txt", "r")
    # data = fp.readlines()
    # fp.close()

    # buf = [ ]
    # one_big_line = ' '.join(data)
    # data = one_big_line.split(' ')
    # total_tokens = len(data)

    # fp2 = open("tokenLines.txt", "w")
    # count = 0
    # while count < total_tokens-100:
    #     for i in range(0, 101):
    #         if data[count+i].find("\n") != -1:
    #             buf.append(data[count+i][:-1])
    #         else:
    #             buf.append(data[count+i])
    #     count = count + 100
    #     string_to_write = ' '.join(buf)
    #     fp2.write(string_to_write+'\n')
    #     #print(count)
    #     buf=[ ]
    # fp2.close()


if __name__ == "__main__":
    main()