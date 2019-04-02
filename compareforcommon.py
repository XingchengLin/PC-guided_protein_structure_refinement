####################################################################################
# This script will compare two files and print out the data based on a shared
# column

#
# Written by Xingcheng Lin, 09/30/2017
####################################################################################

import math
import subprocess
import os
import math
import numpy as np
import sys
import time

################################################


def my_lt_range(start, end, step):
    while start < end:
        yield start
        start += step


def my_le_range(start, end, step):
    while start <= end:
        yield start
        start += step
###########################################


def compareforcommon(inputFile1, compareColnIndex1, desiredColnIndex1, inputFile2, compareColnIndex2, desiredColnIndex2, outputFile):

    # Get current working directory
    pwd = os.getcwd()

    infile1 = open(inputFile1, 'r')
    infile2 = open(inputFile2, 'r')
    outfile = open(outputFile, 'w')

    # Read in lines from the file;

    lines1 = [line.strip() for line in infile1]
    lines2 = [line.strip() for line in infile2]

    infile1.close()
    infile2.close()

    length1 = len(lines1)
    length2 = len(lines2)

    for i in my_lt_range(0, length1, 1):

        line1 = lines1[i].split()

        for j in my_lt_range(0, length2, 1):

            line2 = lines2[j].split()

            if (line1[compareColnIndex1 - 1] == line2[compareColnIndex2 - 1]):

                outfile.write(str(line1[compareColnIndex1 - 1]) + "\t" + str(
                    line1[desiredColnIndex1 - 1]) + "\t" + str(line2[desiredColnIndex2 - 1]) + "\n")

    outfile.close()
    return

############################################################################


if __name__ == "__main__":

    inputFile1 = sys.argv[1]
    compareColnIndex1 = int(sys.argv[2])
    desiredColnIndex1 = int(sys.argv[3])
    inputFile2 = sys.argv[4]
    compareColnIndex2 = int(sys.argv[5])
    desiredColnIndex2 = int(sys.argv[6])
    outputFile = sys.argv[7]

    compareforcommon(inputFile1, compareColnIndex1, desiredColnIndex1,
                     inputFile2, compareColnIndex2, desiredColnIndex2, outputFile)

    print("Love is an endless mystery,")
    print("for it has nothing else to explain it.")
