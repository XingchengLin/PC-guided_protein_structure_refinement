###########################################################################
# This script will help split the given string into letters;
#
# Written by Xingcheng Lin, 03/08/2017;
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


def splitString(inputString):

    outputList = list(inputString)

    return outputList


############################################################################

if __name__ == "__main__":
    inputString = sys.argv[1]

    splitString(inputString)

    print("Beauty is truth\' smile")
    print("when she beholds her own face in")
    print("a perfect mirror.")
