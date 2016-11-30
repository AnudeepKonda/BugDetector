#!/usr/bin/python
#
# This script will be used to produce a file with 100 tokens on each line.

from __future__ import print_function
import sys, os

def main():

    if(len(sys.argv) != 2):
        print("Please input tokens file as first argument.")
        exit()

    fp = open(sys.argv[1], "r")
    data = fp.readlines()
    fp.close()

    buf = [ ]
    one_big_line = ' '.join(data)
    data = one_big_line.split(' ')
    total_tokens = len(data)

    fp2 = open(sys.argv[1], "w")
    count = 0
    while count < total_tokens-100:
        if (count % 500000 == 0):
            print( "Processed tokens: " + str(count) + "\r", end = "")
            sys.stdout.flush()
        for i in range(0, 100):
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

    print(sys.argv[1] + " now has 100 tokens per line.")

if __name__ == "__main__":
    main()