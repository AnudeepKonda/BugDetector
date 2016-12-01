#!/usr/bin/python
#
# This script will be used to produce files with set number of tokens on each line.

from __future__ import print_function
import sys, os

# PARAMETERS
TOKENS_PER_LINE = 10

def main():

    if(len(sys.argv) < 2):
        print("Please input some number of tokens files as arguments.")
        exit()

    for argumentNumber in range(len(sys.argv)):
        
        # First, make sure we don't clobber this script
        if argumentNumber == 0: 
            continue

        fp = open(sys.argv[argumentNumber], "r")
        data = fp.readlines()
        fp.close()

        buf = [ ]
        one_big_line = ' '.join(data)
        data = one_big_line.split(' ')
        total_tokens = len(data)

        fp2 = open(sys.argv[argumentNumber], "w")
        count = 0
        while count < total_tokens-TOKENS_PER_LINE:
            if (count % 500000 == 0):
                print( "Processed tokens: " + str(count) + "\r", end = "")
                sys.stdout.flush()
            for i in range(0, (TOKENS_PER_LINE + 1)):
                if data[count+i].find("\n") != -1:
                    buf.append(data[count+i][:-1])
                else:
                    buf.append(data[count+i])
            count = count + TOKENS_PER_LINE
            string_to_write = ' '.join(buf)
            fp2.write(string_to_write+'\n')
            #print(count)
            buf=[ ]
        fp2.close()

        print(sys.argv[argumentNumber] + " now has 100 tokens per line.")

if __name__ == "__main__":
    main()