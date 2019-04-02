####################################################################################
# This script will calculate levels of locality for motions in each PCs

#
# Input: eigenvector.txt file from PCA
#
# Written by Xingcheng Lin, 07/26/2018
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


def calcLocalMotion(dataFile, entropyFile):

    data = np.loadtxt(dataFile)


    # We calculate the vector length of each trinity of cartesian cooridnates, x, y, z, of each CA atom;
    NoPCs = int(np.shape(data)[1]);
    NoResidues = int(np.shape(data)[0] / 3);

    dataSquare = np.power(data, 2)

    for i in my_lt_range(0, NoResidues, 1):
        
        index = 3 * i 
        
        vector_length_square = dataSquare[:, index] + dataSquare[:, index+1] + dataSquare[:, index+2]

        if i == 0:
            eigenVectorLength_square = vector_length_square;
        else:
            # Concatenate the data (column wised) for each residue;
            eigenVectorLength_square = np.vstack((eigenVectorLength_square, vector_length_square))

    np.savetxt('eigenVectorLength_square.txt', eigenVectorLength_square, fmt='%.5f')

    # Compute the sum for the Shannon Entropy, i.e., S = Sum(plog(p))
    # Note after the stacking, the column index becomes each PC component, while the row index becomes each residue;
    # so we need to sum across rows;
    #S = -np.sum(np.multiply(eigenVectorLength_square, np.log(eigenVectorLength_square)), axis=0);
    S = np.std(eigenVectorLength_square, axis=0);
    
    outfile = open(entropyFile, 'w');

    length = np.shape(S)[0]
    
    for i in my_lt_range(0, length, 1):
        outfile.write(str(S[i]) + "\n")
    
    return

############################################################################


if __name__ == "__main__":

    dataFile = sys.argv[1]
    aveFile = sys.argv[2]

    calcLocalMotion(dataFile, aveFile)

    print("Love is an endless mystery,")
    print("for it has nothing else to explain it.")
