###########################################################################
# This script will get the corresponding section from Gromacs .top file
#
# Written by Xingcheng Lin, 05/03/2017;
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


def getSection(inputFile, outputFile, startSection, endSection):

    # Get current working directory
    pwd = os.getcwd()

    infile = open(inputFile, 'r')
    outfile = open(outputFile, 'w')

    # Read in lines from the file;

    lines = [line.strip() for line in infile]

    infile.close()

    length = len(lines)

    # Flag for output records;
    flag = 0

    for i in my_lt_range(0, length, 1):

        if (lines[i] == endSection):
            flag = 0

        # If section reached, output the second round after flag being changed;
        # If section ends, stop output immediately after flag being changed;
        if (flag == 1):
            outfile.write(lines[i] + "\n")

        if (lines[i] == startSection):
            flag = 1

    outfile.close()
    return


############################################################################

if __name__ == "__main__":
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]
    startSection = sys.argv[3]
    endSection = sys.argv[4]

    getSection(inputFile, outputFile, startSection, endSection)
    print("When the voice of the Silent touches my words,")
    print("I know him and therefore know myself.")
