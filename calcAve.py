####################################################################################
# This script will calculate the mean and standard deviation based on the input file
#
# Input: data for doing the mean and std
#
# Written by Xingcheng Lin, 10/12/2017
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


def calcAve(dataFile, aveFile):

    data = np.loadtxt(dataFile)

    mean = np.average(data, axis=1)
    std = np.std(data, axis=1)

    outfile = open(aveFile, 'w')

    length = np.shape(mean)[0]

    for i in my_lt_range(0, length, 1):
        outfile.write(str(mean[i]) + "\t" + str(std[i]) + "\n")

    return

############################################################################


if __name__ == "__main__":

    dataFile = sys.argv[1]
    aveFile = sys.argv[2]

    calcAve(dataFile, aveFile)

    print("Love is an endless mystery,")
    print("for it has nothing else to explain it.")
