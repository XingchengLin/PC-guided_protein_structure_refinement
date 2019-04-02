###########################################################################
# This script will help you process the file seq.SS from PSSpred into pdbID_psspred
# file of the AWSEM input
#
# Input: seq.SS; output: pdbID_psspred;
#
# Written by Xingcheng Lin, 08/27/2018;
###########################################################################

import time
import subprocess
import os
import math
import sys
import numpy as np

################################################


def my_lt_range(start, end, step):
    while start < end:
        yield start
        start += step


def my_le_range(start, end, step):
    while start <= end:
        yield start
        start += step
#############################################


def processPsspred(inputFile, outputFile):

    # Get current working directory
    pwd = os.getcwd()

    infile = open(inputFile, 'r')
    outfile = open(outputFile, 'w')

    # Read in lines from the file;

    lines = [line.strip() for line in infile]

    infile.close()

    length = len(lines)

    for i in my_lt_range(0, length, 1):

        line = lines[i].split()
        try:
            line[0]
        except IndexError:
            continue
        else:
            # The useful line starts with "SS:"
            if (line[0] == "SS:"):
                outfile.write(str(line[1]))

    outfile.write("\n")
    outfile.close()
    return


############################################################################

if __name__ == "__main__":
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]

    processPsspred(inputFile, outputFile)
    print("When the voice of the Silent touches my words,")
    print("I know him and therefore know myself.")
