####################################################################################
# This script will calculate the variance based on the file distance.xvg from gbond

#
# Written by Xingcheng Lin, 04/13/2017
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


def percentCorrect(recordFileX1, recordFileX2, accuracyX1file, accuracyX2file):

    recordX1 = np.loadtxt(recordFileX1)
    recordX2 = np.loadtxt(recordFileX2)
    # The first 3 columns of recordFile are trash;
    resid = recordX1[:, 0]
    recordX1 = recordX1[:, 3:]
    recordX2 = recordX2[:, 3:]

    # Calculate the accuracy;
    accuracyX1 = np.sum(recordX1, axis=0)
    accuracyX2 = np.sum(recordX2, axis=0)

    accuracyX1 = accuracyX1 / np.shape(recordX1)[0]
    accuracyX2 = accuracyX2 / np.shape(recordX2)[0]

    # Output to files;
    np.savetxt(accuracyX1file, accuracyX1, delimiter=' ', fmt='%1.4f')
    np.savetxt(accuracyX2file, accuracyX2, delimiter=' ', fmt='%1.4f')

    return

############################################################################


if __name__ == "__main__":

    recordFileX1 = sys.argv[1]
    recordFileX2 = sys.argv[2]
    accuracyX1file = sys.argv[3]
    accuracyX2file = sys.argv[4]

    percentCorrect(recordFileX1, recordFileX2, accuracyX1file, accuracyX2file)

    print("Love is an endless mystery,")
    print("for it has nothing else to explain it.")
