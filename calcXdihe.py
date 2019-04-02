####################################################################################
# This script will calculate the frequency for the side-chain angles to fall within
# the range of native values, i.e., native +- 40;
#
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


def calcXdihe(Xfile, Xnativefile, freqFile, extractResid, recordFileX1, recordFileX2, X2_symIndexFile):

    Xangles = np.loadtxt(Xfile)
    Xnativeangle = np.loadtxt(Xnativefile)
    X2_symIndex = np.loadtxt(X2_symIndexFile, dtype=str).tolist()

    out_recordFileX1 = open(recordFileX1, 'w')
    out_recordFileX2 = open(recordFileX2, 'w')

    # Calculate the variance of X1 and X2;

    varX1 = np.var(Xangles[:, 0], axis=0)
    varX2 = np.var(Xangles[:, 1], axis=0)

#    X1zscore = (Xangles[:, 0] - Xnativeangle[0]) / varX1;
#    X2zscore = (Xangles[:, 1] - Xnativeangle[1]) / varX2;

    X1diff = Xangles[:, 0] - Xnativeangle[0]
    X2diff = Xangles[:, 1] - Xnativeangle[1]

    # If the difference in absolute value is larger than 180, then we need to use the net value from 360;
    for i in my_lt_range(0, len(X1diff), 1):
        if X1diff[i] > 180:
            X1diff[i] = 360 - X1diff[i]
        elif X1diff[i] < -180:
            X1diff[i] = X1diff[i] + 360
        else:
            # Use the absolute value to show difference;
            X1diff[i] = np.absolute(X1diff[i])

    # Count the number of frames within 40 degrees of the native state;
    countX1 = 0
    for i in my_lt_range(0, len(X1diff), 1):
        if X1diff[i] <= 40:
            out_recordFileX1.write(str(1) + " ")
            countX1 += 1
        else:
            out_recordFileX1.write(str(0) + " ")

    # Output the newliner;
    out_recordFileX1.write("\n")

    # Count the frequency for X1 to be within 40 degrees of the native state;
    freqX1 = float(countX1) / float(len(X1diff))

    for i in my_lt_range(0, len(X2diff), 1):
        if X2diff[i] > 180:
            X2diff[i] = 360 - X2diff[i]
        elif X2diff[i] < -180:
            X2diff[i] = X2diff[i] + 360
        else:
            # Use the absolute value to show difference;
            X2diff[i] = np.absolute(X2diff[i])

    # Count the number of frames within 40 degrees of the native state;
    # Note for X2, PHE, TYR, ASP have 2-fold symmetry, need to take those into account;
    countX2 = 0

    if int(extractResid in X2_symIndex):
        # For the 2-fold symmetry, offset by 180 and see if it is still within the threshold;
        for i in my_lt_range(0, len(X2diff), 1):
            if (np.absolute(X2diff[i]) <= 40 or np.absolute(X2diff[i] - 180) < 40 or np.absolute(X2diff[i] + 180) < 40):
                out_recordFileX2.write(str(1) + " ")
                countX2 += 1
            else:
                out_recordFileX2.write(str(0) + " ")
    else:
        for i in my_lt_range(0, len(X2diff), 1):
            if X2diff[i] <= 40:
                out_recordFileX2.write(str(1) + " ")
                countX2 += 1
            else:
                out_recordFileX2.write(str(0) + " ")

    # Output the newliner;
    out_recordFileX2.write("\n")

    # Count the frequency for X1 to be within 40 degrees of the native state;
    freqX2 = float(countX2) / float(len(X2diff))


#    Xzscore = np.column_stack((X1zscore, X2zscore));

    # Calculate the average of dihedral difference;
#    X1diffave = np.average(X1diff);
#    X2diffave = np.average(X2diff);
    #X1diffave = X1diff[2000];
    #X2diffave = X2diff[2000];

    outfile = open(freqFile, 'a')

    outfile.write(str(extractResid) + " " +
                  str(freqX1) + " " + str(freqX2) + "\n")

    outfile.close()

#    np.savetxt(zScoreFile, Xzscore, fmt='%1.3f');

    return

############################################################################


if __name__ == "__main__":

    Xfile = sys.argv[1]
    Xnativefile = sys.argv[2]
    freqFile = sys.argv[3]
    # Residue index from the corresponding file, pass by argument;
    extractResid = sys.argv[4]
    # Record file for whether this specific side-chain dihedral is within 40 degrees of the native
    recordFileX1 = sys.argv[5]
    recordFileX2 = sys.argv[6]
    # Residue index file for PHE, TYR and ASP, they have 2-fold symmetry for X2;
    X2_symIndexFile = sys.argv[7]

    calcXdihe(Xfile, Xnativefile, freqFile, extractResid,
              recordFileX1, recordFileX2, X2_symIndexFile)

    print("Love is an endless mystery,")
    print("for it has nothing else to explain it.")
