###########################################################################
# This script will help calculate the PMF
#
# Written by Xingcheng Lin, 12/12/2016;
###########################################################################

import time
import subprocess
import os
import math
import sys

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


def fenergy(firstFile):

    # Get current working directory
    pwd = os.getcwd()

    infile = open(firstFile, "r")
    outfile1 = open("hist.txt", "w")
    outfile2 = open("pmf.txt", "w")
    outfile3 = open("pmf_offset.txt", "w")

    # Read in lines from the file;

    lines = [line.strip() for line in infile]
    infile.close()

    length = len(lines)

    # the boundary of the free map;
    topRC = 1.0
    bottomRC = 0.0
    stepRC = 0.01

    NoRCBin = int((topRC - bottomRC) / stepRC + 0.5) + 1

    # Histogram list;
    hist = [0] * NoRCBin
    # Free energy list;
    free = [0] * NoRCBin

    # Normalization factor;
    count = 0

    # The first line output from Plumed is not useful;
    for i in my_lt_range(1, length, 1):

        line = lines[i].split()

        rci = int((float(line[1]) - bottomRC) / stepRC + 0.5)

        hist[rci] += 1
        count += 1

    # In the end, we calculate the averaged histogram and free energy as a function of rc;

    for i in my_lt_range(0, NoRCBin, 1):

        hist[i] = float(hist[i]) / count
        if (hist[i] != 0):
            free[i] = -math.log(hist[i])
        else:
            free[i] = 0

    # Select the offset to make free energy plot zero-based.
    #
    offset = 100
    for i in my_lt_range(0, NoRCBin, 1):
        if free[i] != 0:
            if (free[i] < offset):
                offset = free[i]

    # offset and output;

    for i in my_lt_range(0, NoRCBin, 1):

        xtmp = (i + 0.5) * stepRC + bottomRC

        # Even if histogram is zero, we still output;
        outfile1.write(str(xtmp) + "\t" + str(hist[i]) + "\n")

        if (free[i] != 0):

            outfile2.write(str(xtmp) + "\t" + str(free[i]) + "\n")
            # Make it a zero based plot;
            free[i] -= offset

            outfile3.write(str(xtmp) + "\t" + str(free[i]) + "\n")

    return

############################################################################


if __name__ == "__main__":
    firstFile = sys.argv[1]

    fenergy(firstFile)
    print("When the voice of the Silent touches my words,")
    print("I know him and therefore know myself.")
