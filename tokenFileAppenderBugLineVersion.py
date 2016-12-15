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
    tokenFilePaths.sort()

    # Clean up paths on windows
    for x in range(0,len(tokenFilePaths)):
        # print(tokenFilePaths[x])
        # print(tokenFilePaths[x].replace("\\", "/"))
        tokenFilePaths[x] = tokenFilePaths[x].replace("\\", "/")
    
    for entry in tokenFilePaths:
        print(entry)
    # time.sleep(3)
    # exit()

    # Holds the list of buggyLine files
    bugFilePaths = []
    # Each project file name acts a hash to a list of subdirectories
    projectDirectories = {}

    # Build dictionary of lines and bug values
    # We must have an entropy file for each line
    for item in os.listdir(directoryToSearch):
        if os.path.isfile(os.path.join(directoryToSearch, item)):
            # print("BuggyLineFile: " + item)
            bugFilePaths.append(os.path.join(directoryToSearch, item))
        else:
            # print("ProjectDir:    " + item)
            # Adding a new entry to the projectDirectories dictionary
            projectDirectories[item] = []
            tempDir = os.path.join(directoryToSearch, item)
            for subDirName in os.listdir(tempDir):
                if not os.path.isfile(os.path.join(tempDir, subDirName)):
                    # print("  SnapshotDir:   " + subDirName)
                    projectDirectories[item].append(subDirName)


    # Sanity testing file/dir paths
    # print(bugFilePaths)
    # exit()
    # print(projectDirectories)

    # time.sleep(2)

    # This is a hash of tokenfiles to line numbers
    # Which are in turn hashes to buggy statuses
    codeTokenPaths = {}

    # go through each bugFile
    # assembling hashes relating files to token line numbers to bug status
    for bugFile in bugFilePaths:
        print(bugFile)
        # exit()
        fileHandler = open(bugFile, 'r')
        skipFirstLineFlag = True
        for line in fileHandler:
            
            # skip the first line, as it's only denoting field names
            if skipFirstLineFlag:
                skipFirstLineFlag = False
                continue

            # Get the various field values, storing the ones we need
            lineValues = line.split(",")
            # print(lineValues)
            project = lineValues[0][1:-1] # project
            # print(project) 
            snapshot = lineValues[1] # snapshot
            # print(snapshot)
            filename = lineValues[2][1:-1] # filename (of Java file)
            # print(filename)
            token_line = lineValues[4] # token_line (number)
            # print(token_line)
            is_bug = lineValues[7] # is_bug (0 or 1)
            # print(is_bug)

            # fullTokenFileName will hold the name of the appopriate token file
            fullTokenFileName = project + "/" + snapshot + "/" + filename
            # replace java file extension
            fullTokenFileName = "projects/" + fullTokenFileName[:-4] + "code.tokens"
            # print(fullTokenFileName)
            # print("\n")


            # check to see if the snapshot is being used. If not, continute to next line
            if snapshot not in projectDirectories[project]:
                # print (project)
                # print (snapshot)
                # print (projectDirectories[project])
                # print ("DIFFERENT!!!!!")
                continue
            else:
                # snapshot of line matches a snapshot we're using
                # So map some hashes...

                # print("Same.")

                # If this file not already in codeTokenPaths, add it
                if fullTokenFileName not in codeTokenPaths:
                    codeTokenPaths[fullTokenFileName] = {}

                # Set this line equal to a bug flag
                codeTokenPaths[fullTokenFileName][token_line] = is_bug

                # print(project)
                # print (snapshot)
                # print(projectDirectories[project])

                # print(fullTokenFileName)
                # print(codeTokenPaths[fullTokenFileName]) #lines with bug flags
                # print("\n")
                # print(token_line)
                # print(codeTokenPaths[fullTokenFileName][token_line]) # is_bug
                pass

    # Sanity check    
    # Print out files, followed by the hashes of lines to bugflags
    # for filePath in codeTokenPaths:
    #     codeTokenPaths[filePath]
    #     for subDir in codeTokenPaths[filePath]:
    #         print(filePath)
    #         print(codeTokenPaths[filePath])
    #         print("\n")


    for entry in codeTokenPaths:
        print(entry)
    print("\n\n----\n\n")
    time.sleep(1)



    # Lists of names of files to use for training and testing
    # These lists are populated from tokenFilePaths, which is filled by
    # scanning the given directory for token files
    tokenTrainSet = []
    tokenTestSet = []
    # entropyTrainSet = []
    # entropyTestSet = []


    # Select 20% of files to be used for training
    indicesOfTestSet = random.sample(range(len(tokenFilePaths)), len(tokenFilePaths)/5)

    for index in range(0,len(tokenFilePaths)):
        if index in indicesOfTestSet:
            tokenTestSet.append(tokenFilePaths[index])
        else:
            tokenTrainSet.append(tokenFilePaths[index])

    # createDirectory("processedData")

    print("Files in token train set: " + str(len(tokenTrainSet)))
    print("Files in token test set:  " + str(len(tokenTestSet)))

    ## TRAINING SET
    fileHandlerWriter = open("trainingLinesWithBugIndicators.txt", 'w')
    for index in range(0,len(tokenTrainSet)):
        fileHandlerToken = open(tokenTrainSet[index], 'r')
        pathname = tokenTrainSet[index]
        # print(pathname)
        tokenLines = fileHandlerToken.readlines()
        # entropyLines = fileHandlerEntropy.readlines()

        print("Building training set from: " + pathname)
        # If this is true, then we have a match
        lineLookupFlag = False
        if pathname in codeTokenPaths:
            lineLookupFlag = True


        fileHandlerWriter.write("<START_FILE>\n")
        for lineIndex in range(0,len(tokenLines)):
            tempLine = ""
            tempLine = tempLine + tokenLines[lineIndex]
            tempLine = tempLine.split('\n')[0]
            tempLine = ' '.join(tempLine.split())
            # append entropy scores
            # tempLine = tempLine + " " + entropyLines[lineIndex].split(',')[1]
            
            # Look up the line's bugginess in the appropriate hash
            # If we found a match, resolve the hash and append the bugflag
            if lineLookupFlag and (str((lineIndex+1)) in codeTokenPaths[pathname]):
                tempLine = tempLine + " " + str(codeTokenPaths[pathname][str(lineIndex+1)])
            else:
                # No match, so assume the line is not buggy (we have no information about it)
                tempLine = tempLine + " 0"
            fileHandlerWriter.write(tempLine + "\n")
        fileHandlerWriter.write("<END_FILE>\n")






    ## TESTING SET
    fileHandlerWriter = open("testingLinesWithBugIndicators.txt", 'w')
    for index in range(0,len(tokenTestSet)):
        fileHandlerToken = open(tokenTestSet[index], 'r')
        pathname = tokenTestSet[index]
        # print(pathname)
        tokenLines = fileHandlerToken.readlines()
        # entropyLines = fileHandlerEntropy.readlines()

        print("Building testing set from: " + pathname)
        # If this is true, then we have a match
        lineLookupFlag = False
        if pathname in codeTokenPaths:
            lineLookupFlag = True


        fileHandlerWriter.write("<START_FILE>\n")
        for lineIndex in range(0,len(tokenLines)):
            tempLine = ""
            tempLine = tempLine + tokenLines[lineIndex]
            tempLine = tempLine.split('\n')[0]
            tempLine = ' '.join(tempLine.split())
            # append entropy scores
            # tempLine = tempLine + " " + entropyLines[lineIndex].split(',')[1]
            
            # Look up the line's bugginess in the appropriate hash
            # If we found a match, resolve the hash and append the bugflag
            if lineLookupFlag and (str((lineIndex+1)) in codeTokenPaths[pathname]):
                tempLine = tempLine + " " + str(codeTokenPaths[pathname][str(lineIndex+1)])
            else:
                # No match, so assume the line is not buggy (we have no information about it)
                tempLine = tempLine + " 0"
            fileHandlerWriter.write(tempLine + "\n")
        fileHandlerWriter.write("<END_FILE>\n")

    exit()


if __name__ == "__main__":
    main()