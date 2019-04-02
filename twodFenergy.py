###########################################################################
# This script will help calculate the 2D PMF
#
# Written by Xingcheng Lin, 12/12/2016;
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


def twodFenergy(firstFile, secondFile):

    # Get current working directory
    pwd = os.getcwd()

    infile1 = open(firstFile, "r")
    infile2 = open(secondFile, "r")
    outfile1 = open("twoDhist.txt", "w")
    outfile2 = open("twoDpmf.txt", "w")
    outfile3 = open("twoDpmf_offset.txt", "w")

    # the boundary of the free map;
    topRCx = 1.0
    bottomRCx = 0.0
    topRCy = 1.0
    bottomRCy = 0.0
    stepRCx = 0.01
    stepRCy = 0.01

    # Read in lines from the file;

    lines1 = [line.strip() for line in infile1]
    lines2 = [line.strip() for line in infile2]

    infile1.close()
    infile2.close()

    # Length1 should equals to lenght2;
    length1 = len(lines1)
    length2 = len(lines2)

    NoRCBinx = int((topRCx - bottomRCx) / stepRCx + 0.5) + 1
    NoRCBiny = int((topRCy - bottomRCy) / stepRCy + 0.5) + 1

    print((NoRCBinx, NoRCBiny))

    # initialize a histogram matrix;
    shape = (NoRCBinx, NoRCBiny)
    histMatrix = np.zeros(shape)
    # initialize a free-energy matrix;
    freeMatrix = np.zeros(shape)

    # Normalization factor;
    count = 0

    # The first line output from Plumed is not useful;
    for i in my_lt_range(1, length1, 1):

        line1 = lines1[i].split()
        line2 = lines2[i].split()

        # We don't need to consider equilibration here, since that has been taken care of in the selLowT.sh script;
        if (float(line1[0]) >= 0.0):

            rcx = int((float(line1[1]) - bottomRCx) / stepRCx + 0.5)
            rcy = int((float(line2[1]) - bottomRCy) / stepRCy + 0.5)

            histMatrix[rcx][rcy] += 1
            count += 1

    # In the end, we calculate the averaged histogram and free energy as a function of rc;

    for i in my_lt_range(0, NoRCBinx, 1):
        for j in my_lt_range(0, NoRCBiny, 1):

            histMatrix[i][j] = float(histMatrix[i][j]) / count
            if (histMatrix[i][j] != 0):
                freeMatrix[i][j] = -math.log(histMatrix[i][j])
            else:
                freeMatrix[i][j] = 0

    # Select the offset to make free energy plot zero-based.
    #
    offset = 100
    for i in my_lt_range(0, NoRCBinx, 1):
        for j in my_lt_range(0, NoRCBiny, 1):
            if freeMatrix[i][j] != 0:
                if (freeMatrix[i][j] < offset):
                    offset = freeMatrix[i][j]

    # offset and output;
    print(("offset", offset))

    for i in my_lt_range(0, NoRCBinx, 1):
        for j in my_lt_range(0, NoRCBiny, 1):

            xtmp = (i + 0.5) * stepRCx + bottomRCx
            ytmp = (j + 0.5) * stepRCy + bottomRCy

            # Even if histogram is zero, we still output;
            outfile1.write(str(xtmp) + "\t" + str(ytmp) +
                           "\t" + str(histMatrix[i][j]) + "\n")

            if (freeMatrix[i][j] != 0):

                outfile2.write(str(xtmp) + "\t" + str(ytmp) +
                               "\t" + str(freeMatrix[i][j]) + "\n")
                # Make it a zero based plot;
                freeMatrix[i][j] -= offset

                outfile3.write(str(xtmp) + "\t" + str(ytmp) +
                               "\t" + str(freeMatrix[i][j]) + "\n")

    return


############################################################################

if __name__ == "__main__":
    firstFile = sys.argv[1]
    secondFile = sys.argv[2]

    twodFenergy(firstFile, secondFile)
    print("When the voice of the Silent touches my words,")
    print("I know him and therefore know myself.")
