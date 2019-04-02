####################################################################################
# This script will help calculate the pearson correlation coefficient from the data
# round AWSEM prediction for the new dump file;
#
# Written by Xingcheng Lin, 04/04/2017
####################################################################################

import math
import subprocess
import os
import math
import numpy as np
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
###########################################


def calPearson(filename):

    matrix = np.loadtxt(filename)
    from scipy import stats

    res = stats.pearsonr(matrix[:, 0], matrix[:, 1])
    print(res)

    return res

############################################################################


if __name__ == "__main__":

    filename = sys.argv[1]
    calPearson(filename)
    print("When the voice of the Silent touches my words,")
    print("I know him and therefore know myself.")
